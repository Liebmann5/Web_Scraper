#!/bin/bash

# Create the longhorn-util directory
mkdir -p longhorn-util

cd longhorn-util

# Create the master's subdirectories
mkdir -p defaults files tasks tests

cd defaults

cat <<'EOL' > main.yml
---
# Namespace for Longhorn
k3s_longhorn_namespace: longhorn-system

# Enable service mesh
enable_linkerd: false
EOL

cd ..

cd files

cat <<'EOL' > check_lh.sh
#!/usr/bin/env sh


# List of required tools: kubectl, curl, jq, cat
CURL=${CURL:-curl}
JQ=${JQ:-jq}

CURL=$(command -v ${CURL})
JQ=$(command -v ${JQ})
# Helper functions to reduce the amount of args we pass in on each curl/jq call,
# note we are calling whatever command -v curl/jq/etc.. found directly to avoid
# recursion
curl() {
  ${CURL} --insecure --silent -H 'content-type: application/json' "$@"
}

jq() {
  ${JQ} -r "$@"
}


# Looping through all of the mustbe deployed resources during 5 minutes with 10 seconds intervals
count=0
while [ "$count" -lt 30 ]
do
    # Functions and variables to calculate the number of resource to determine the success of the deployment    
    DESIRED_RESORCE_NUMBER=0
    AVAILABLE_RESOURCE_NUMBER=0

    add_desired() {
        DESIRED_RESORCE_NUMBER=$(($DESIRED_RESORCE_NUMBER+$1))
    }

    add_available() {
        AVAILABLE_RESOURCE_NUMBER=$(($AVAILABLE_RESOURCE_NUMBER+$1))
    }

    # Use check_replicas "resource_type" "resorce_name" 
    # Ex. check_replicas "deployment" "longhorn-ui"
    check_replicas() {
        AVAILABLE_REPLICAS=$(kubectl get ${1} ${2} --namespace longhorn-system -o json | jq -r '.status.availableReplicas')
        DESIRED_REPLICAS=$(kubectl get ${1} ${2} --namespace longhorn-system -o json | jq -r '.spec.replicas')
        if [ -z "$DESIRED_REPLICAS" ] || [ -z "$AVAILABLE_REPLICAS" ]
        then
            echo "Longhorn ${1} ${2} replicas not deployed yet"
        elif [ "$DESIRED_REPLICAS" -eq "$AVAILABLE_REPLICAS" ]
        then
            echo "Longhorn ${1} ${2} replicas deployed successfully"
            add_desired "$DESIRED_REPLICAS"
            add_available "$AVAILABLE_REPLICAS"
        else
            echo "Longhorn ${1} ${2} replicas not fully deployed yet"
        fi
    }

    ### Kubernetes nodes check
    # Generate a list of nodes 
    NODE_LIST=$(kubectl get nodes -o json | jq -r '.items[].metadata.name')

    # Iterate through nodes and determine if each node has Kubelet in Ready status
    for node in $(echo $NODE_LIST)
    do
        NODE_STATUS=$(kubectl get nodes $node -o json | jq -r '.status.conditions[] | select(.reason == "KubeletReady") | .status')
        add_desired "1"
        if [ -z "$NODE_STATUS" ]
        then
            echo "Node $node is not ready yet"
            break
        elif [ $NODE_STATUS = "True" ]
        then
            echo "Node $node is ready"
            add_available "1"
        else
            echo "Node $node is not ready yet"
            add_available "-1"
        fi
    done

    ### DAEMONSETS
    # Check the number of Longhorn Manager daemonsets
    DESIRED_LH_MANAGER_DS_NUMBER=$(kubectl get daemonsets.apps longhorn-manager  -n longhorn-system -o json | jq -r '.status | .desiredNumberScheduled')
    READY_LH_MANAGER_DS_NUMBER=$(kubectl get daemonsets longhorn-manager  -n longhorn-system -o json | jq -r '.status | .numberReady')
    if [ -z "$DESIRED_LH_MANAGER_DS_NUMBER" ] || [ -z "$READY_LH_MANAGER_DS_NUMBER" ]
    then
        echo "Longhorn Manager deamonsets are not deployed yet"
    elif [ "$DESIRED_LH_MANAGER_DS_NUMBER" -eq "$READY_LH_MANAGER_DS_NUMBER" ]
    then
        echo "Longhorn Manager deamonsets are deployed"
        add_desired "$DESIRED_LH_MANAGER_DS_NUMBER"
        add_available "$READY_LH_MANAGER_DS_NUMBER"
    else
        echo "Longhorn Manager deamonsets are not fully deployed yet"
    fi


    ### CRDs
    # Compare the desired Longhorn manager number of daemonsets to a number of nodes in longhorn-system namespace
    # If numbers match, proceed with checking nodes and instance-managers statuses
    LONGHORN_NODE_LIST_NUMBER=$(kubectl get nodes.longhorn.io -n longhorn-system -o json | jq -r '.items[].spec.name' | wc -l)
    if [ "$LONGHORN_NODE_LIST_NUMBER" -eq 0 ] || [ "$DESIRED_LH_MANAGER_DS_NUMBER" -ne "$LONGHORN_NODE_LIST_NUMBER" ]
    then
        echo "Longhorn nodes CRDs are not deployed yet"
    else
        # Generate a list of nodes that Lonhorn is installed on
        LONGHORN_NODE_LIST=$(kubectl get nodes.longhorn.io -n longhorn-system -o json | jq -r '.items[].spec.name')
        # Iterate through Longhorn nodes and determine if each node has Kubelet in Ready status
        for node in $(echo $LONGHORN_NODE_LIST)
        do
            LONGHORN_NODE_STATUS=$(kubectl get nodes.longhorn.io/${node} -n longhorn-system -o json | jq -r '.status.conditions[] | select(.type == "Ready") |.status')
            add_desired "1"
            if [ -z "$LONGHORN_NODE_STATUS" ]
            then
                echo "Longhorn Node $node is not deployed yet"
                break
            elif [ $LONGHORN_NODE_STATUS = "True" ]
            then
                echo "Longhorn Node $node is deployed successfully"
                add_available "1"
            else
                echo "Longhorn Node $node is not deployed yet"
                add_available "-1"
            fi
        done

        # Iterate through nodes to see if instance-managers: engine and replica are deployed
        for node in $(echo $LONGHORN_NODE_LIST)
        do
            for manager in engine replica
            do
                STATUS=$(kubectl get instancemanagers -n longhorn-system -o json | jq -r ".items[] | select(.spec.nodeID == \"$node\") | select(.spec.type == \"$manager\") | .status.currentState")
                add_desired "1"
                # Variable STATUS will be empty when there are resources deployed yet, therefore break out of the loop
                if [ -z "$STATUS" ]
                then
                    echo "Node $node has instance manager $manager not deployed yet"
                    break
                elif [ "$STATUS" = "running" ]
                then
                    echo "Node $node has instance manager $manager deployed"
                    add_available "1"
                else
                    echo "Node $node has instance manager $manager not fully deployed yet"
                    add_available "-1"
                fi
            done
        done
    fi

    # Engine images status
    ENGINE_IMAGES_STATUS=$(kubectl get engineimages -n longhorn-system -o json | jq -r '.items[].status.state')
    add_desired "1"
    if [ "$ENGINE_IMAGES_STATUS" = "deployed" ]
    then
        echo "Longhorn Engine Images deployed successfully"
        add_available "1"
    else
        echo "Longhorn Engine Images are not deployed yet"
        add_available "-1"
    fi

    # Checking if Longhorn CSI Plugin is running on all nodes
    DESIRED_CSI_PLUGIN_NUMBER=$(kubectl get daemonsets longhorn-csi-plugin  -n longhorn-system -o json | jq -r '.status.desiredNumberScheduled')
    AVAILABLE_CSI_PLUGIN_NUMBER=$(kubectl get daemonsets longhorn-csi-plugin  -n longhorn-system -o json | jq -r '.status.numberAvailable')
    if [ -z "$DESIRED_CSI_PLUGIN_NUMBER" ] || [ -z "$AVAILABLE_CSI_PLUGIN_NUMBER" ]
    then
        echo "Longhorn CSI Plugin not deployed yet"
    elif [ "$DESIRED_CSI_PLUGIN_NUMBER" -eq "$AVAILABLE_CSI_PLUGIN_NUMBER" ]
    then
        echo "Longhorn CSI Plugin deployed successfully"
        add_desired "$DESIRED_CSI_PLUGIN_NUMBER"
        add_available "$AVAILABLE_CSI_PLUGIN_NUMBER"
    else
        echo "Longhorn CSI Plugin not fully deployed yet"
    fi

    # Longhorn UI deployment status
    check_replicas "deployment" "longhorn-ui"

    # Checking Longhorn CSI Attacher deployment status
    check_replicas "deployment" "csi-attacher"

    # Checking Longhorn CSI Provisioner deployment status
    check_replicas "deployment" "csi-provisioner"

    # Checking Longhorn CSI Resizer deployment status
    check_replicas "deployment" "csi-resizer"

    # Checking Longhorn CSI Snapshotter deployment status
    check_replicas "deployment" "csi-snapshotter"

    if [ "$DESIRED_RESORCE_NUMBER" -eq "$AVAILABLE_RESOURCE_NUMBER" ]
    then
        echo "All resources deployed successfully"
        break
    else
        echo "Not all resorces deployed yet"
    fi
    count=$(($count+1))
    sleep 20
done
EOL

cd ..

cd tasks

cat <<'EOL' > configure_linkerd_mesh.yml
---
# Check longhorn is running
- name: Check longhorn status. Wait for all components to start
  command:
    cmd: "/usr/local/bin/check_lh.sh"
  changed_when: false

# Make longhorn-manager container listen on localhost
- name: Change longhorn-manager POD_IP env variable
  command:
    cmd: "kubectl set env daemonset/longhorn-manager -n {{ k3s_longhorn_namespace }} POD_IP=0.0.0.0"
  register: change_pod_env
  changed_when: '"daemonset.apps/longhorn-manager env updated" in change_pod_env.stdout'

- name: Annotate longhorn-manager
  kubernetes.core.k8s:
    definition:
      apiVersion: v1
      kind: DaemonSet
      metadata:
        name: longhorn-manager
        namespace: "{{ k3s_longhorn_namespace }}"
      spec:
        template:
          metadata:
            annotations:
              linkerd.io/inject: enabled
    state: patched

- name: Annotate longhorn-ui
  kubernetes.core.k8s:
    definition:
      apiVersion: v1
      kind: Deployment
      metadata:
        name: longhorn-ui
        namespace: "{{ k3s_longhorn_namespace }}"
      spec:
        template:
          metadata:
            annotations:
              linkerd.io/inject: enabled
    state: patched
EOL

cat <<'EOL' > main.yml
---
- name: Copy longhorn health check script
  copy:
    src: "files/{{ item }}"
    dest: "/usr/local/bin/{{ item }}"
    owner: "root"
    group: "root"
    mode: "u=rwx,g=rx,o=rx"
  become: true
  with_items:
    - check_lh.sh

- name: Enable linkerd integration
  include_tasks: configure_linkerd_mesh.yml
  when: enable_linkerd
EOL

cd ..

cd tests

cat <<'EOL' > cleanup_test_longhorn.yml
---
- name: Testing longhorn installation.
  hosts: k3s_master

  tasks:
    - name: Create longhorn namespace.
      kubernetes.core.k8s:
        name: testing-longhorn
        api_version: v1
        kind: Namespace
        state: absent

    - name: Create Ingress rule for Longhorn UI
      kubernetes.core.k8s:
        definition: "{{ lookup('template', 'templates/' + item ) }}"
        state: absent
      with_items:
        - testing_longhorn_manifest.yml
EOL

cat <<'EOL' > test_longhorn.yml
---
- name: Testing longhorn installation.
  hosts: k3s_master

  tasks:
    - name: Create longhorn namespace.
      kubernetes.core.k8s:
        name: testing-longhorn
        api_version: v1
        kind: Namespace
        state: present

    - name: Create PVC and testing pod
      kubernetes.core.k8s:
        definition: "{{ lookup('template', 'templates/' + item ) }}"
        state: present
      with_items:
        - testing_longhorn_manifest.yml
EOL

# Create the tests's subdirectories
mkdir templates

cd templates

cat <<'EOL' > testing_longhorn_manifest.yml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nginx-logs
  namespace: testing-longhorn
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: longhorn
  resources:
    requests:
      storage: 50Mi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: testing-longhorn
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      volumes:
        - name: nginx-logs
          persistentVolumeClaim:
            claimName: nginx-logs
      containers:
        - image: nginx:1.17.6
          name: nginx
          ports:
            - containerPort: 80
          volumeMounts:
            - mountPath: "/var/log/nginx"
              name: nginx-logs
              readOnly: false

---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: nginx
  name: my-nginx
  namespace: testing-longhorn
spec:
  ports:
    - port: 80
      targetPort: 80
  selector:
    app: nginx
  type: LoadBalancer
EOL

cd ../../..

chmod +x defaults/main.yml
chmod +x files/check_lh.sh
chmod +x tasks/configure_linkerd_mesh.yml
chmod +x tasks/main.yml
chmod +x tests/cleanup_test_longhorn.yml
chmod +x tests/test_longhorn.yml
chmod +x tests/templates/testing_longhorn_manifest.yml