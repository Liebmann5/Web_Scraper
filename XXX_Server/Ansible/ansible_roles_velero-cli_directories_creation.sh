#!/bin/bash

# Create the velero-cli directory
mkdir -p velero-cli

cd velero-cli

# Create the velero-cli's subdirectories
mkdir -p defaults tasks tests

cd defaults

cat <<'EOL' > main.yml
---
velero_version: v1.11.1
velero_arch: arm64

velero_namespace: velero
EOL

cd ..

cd tasks

cat <<'EOL' > configure_velero_cli.yml
---
- name: Get CLI configured namespace
  command:
    cmd: "velero client config get namespace"
  register: get_velero_namespace
  changed_when: false
  ignore_errors: true

- name: Configure velero CLI namespace
  command:
    cmd: "velero client config set namespace={{ velero_namespace }}"
  when:
    - get_velero_namespace.rc==0
    - '"namespace: <NOT SET>" in get_velero_namespace.stdout or "namespace: " + velero_namespace not in get_velero_namespace.stdout'
  changed_when: true

- name: Get CLI configured colored
  command:
    cmd: "velero client config get colored"
  register: get_velero_colored
  changed_when: false
  ignore_errors: true

- name: Configure velero CLI colored output
  command:
    cmd: "velero client config set colored=true"
  when:
    - get_velero_colored.rc==0
    - '"colored: <NOT SET>" in get_velero_colored.stdout or "colored: true" not in get_velero_colored.stdout'
  changed_when: true
EOL

cat <<'EOL' > install_velero_cli.yml
---

- name: Download Velero CLI
  get_url:
    url: https://github.com/vmware-tanzu/velero/releases/download/{{ velero_version }}/velero-{{ velero_version }}-linux-{{ velero_arch }}.tar.gz
    dest: /tmp/velero-{{ velero_version }}-linux-{{ velero_arch }}.tar.gz
    mode: '0766'

- name: Extract archives
  unarchive:
    src: /tmp/velero-{{ velero_version }}-linux-{{ velero_arch }}.tar.gz
    dest: /tmp
    remote_src: true

- name: Copy binary to /usr/local/bin
  copy:
    src: /tmp/velero-{{ velero_version }}-linux-{{ velero_arch }}/velero
    dest: /usr/local/bin/velero
    mode: '0755'
    remote_src: true
EOL

cat <<'EOL' > main.yml
---

- name: Install velero client
  include_tasks: install_velero_cli.yml
  args:
    apply:
      become: true

- name: Configure velero CLI
  include_tasks: configure_velero_cli.yml
EOL

cd ..

cd tests

cat <<'EOL' > cleaning_testing.yml
---
- name: Cleaning velero testing pod.
  hosts: k3s_master

  tasks:
    - name: Cleaning testing
      kubernetes.core.k8s:
        definition: "{{ lookup('file', 'files/' + item ) }}"
        state: absent
      with_items:
        - nginx_test_application.yml
EOL

cat <<'EOL' > testing_velero.yml
---
- name: Testing velero backup.
  hosts: k3s_master

  tasks:
    - name: Create PVC and testing pod
      kubernetes.core.k8s:
        definition: "{{ lookup('file', 'files/' + item ) }}"
        state: present
      with_items:
        - nginx_test_application.yml
EOL

# Create the tests's subdirectories
mkdir files

cd files

cat <<'EOL' > nginx_test_application.yml
---
apiVersion: v1
kind: Namespace
metadata:
  name: nginx-example
  labels:
    app: nginx

---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: nginx-logs
  namespace: nginx-example
  labels:
    app: nginx
spec:
  storageClassName: longhorn
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Mi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: nginx-example
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
      annotations:
        pre.hook.backup.velero.io/container: fsfreeze
        pre.hook.backup.velero.io/command: '["/sbin/fsfreeze", "--freeze", "/var/log/nginx"]'
        post.hook.backup.velero.io/container: fsfreeze
        post.hook.backup.velero.io/command: '["/sbin/fsfreeze", "--unfreeze", "/var/log/nginx"]'
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
        - image: ubuntu:bionic
          name: fsfreeze
          securityContext:
            privileged: true
          volumeMounts:
            - mountPath: "/var/log/nginx"
              name: nginx-logs
              readOnly: false
          command:
            - "/bin/bash"
            - "-c"
            - "sleep infinity"

---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: nginx
  name: my-nginx
  namespace: nginx-example
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
chmod +x tasks/configure_velero_cli.yml
chmod +x tasks/install_velero_cli.yml
chmod +x tasks/main.yml
chmod +x tests/cleaning_testing.yml
chmod +x tests/testing_velero.yml
chmod +x tests/files/nginx_test_application.yml