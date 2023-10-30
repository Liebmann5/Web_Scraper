#!/bin/bash

# Create the k3s directory
mkdir -p k3s

cd k3s

# Create the subdirectories
mkdir -p master prereq worker

cd master

# Create the master's subdirectories
mkdir -p defaults tasks templates vars

cd defaults

cat <<'EOL' > main.yml
---

# Setting token
k3s_token: s1cret0

# Setting K3s version
k3s_version: v1.24.7+k3s1

# k3s config file
k3s_config_file: /etc/rancher/k3s/config.yaml

# k3s kubelet config content
k3s_kubelet_config: ""

# k3s server-config
k3s_server_config: ""
EOL

cd ..

cd tasks

cat <<'EOL' > installation.yml
---

- name: Install HA k3s masters
  when: k3s_build_cluster
  block:
    - name: Install primary master in case of HA mode
      when:
        - k3s_primary_control_node
      block:
        - name: install master
          include_tasks: k3s_install.yml
        - name: wait for master to be ready
          include_tasks: wait_for_master_node.yml
    - name: Install secondary masters in case of HA mode
      # Secondary masters need to be added sequentially
      # otherwise, "ETCD join failed: etcdserver: too many learner members in cluster" appears.
      when:
        - not k3s_primary_control_node
      throttle: 1
      block:
        - name: Wait for primary master
          include_tasks: wait_for_primary_master.yml
        - name: Install k3s
          include_tasks: k3s_install.yml

- name: Install master non HA
  when:
    - not k3s_build_cluster
  include_tasks: k3s_install.yml
EOL

cat <<'EOL' > k3s_install.yml
---

- name: Get K3s installation script
  get_url:
    url: https://get.k3s.io
    dest: /tmp/k3s_install.sh
    mode: '0766'

- name: Install K3s
  command: "/tmp/k3s_install.sh server"
  environment:
    INSTALL_K3S_VERSION: "{{ k3s_version }}"
  changed_when: true

- name: Create directory .kube
  file:
    path: ~{{ ansible_user }}/.kube
    state: directory
    owner: "{{ ansible_user }}"
    mode: "u=rwx,g=rx,o="

- name: Copy config file to user home directory
  copy:
    src: /etc/rancher/k3s/k3s.yaml
    dest: ~{{ ansible_user }}/.kube/config
    remote_src: true
    owner: "{{ ansible_user }}"
    mode: "u=rw,g=,o="
EOL

cat <<'EOL' > main.yml
---

- name: Run pre-configuration tasks
  include_tasks: pre_configuration.yml

- name: Run installation tasks
  include_tasks: installation.yml
EOL

cat <<'EOL' > pre_configuration.yml
---

- name: Detect if multiple masters are defined
  ansible.builtin.set_fact:
    k3s_build_cluster: true
  when:
    - groups['k3s_master'] is defined
    - groups['k3s_master'] | length > 1

- name: Ensure a primary k3s control node is defined if multiple masters are found
  ansible.builtin.set_fact:
    k3s_primary_control_node: true
  when:
    - groups['k3s_master'] | length > 1
    - inventory_hostname == groups['k3s_master'][0]

- name: Ensure registration ip is defined
  ansible.builtin.set_fact:
    k3s_registration_ip: "{{ hostvars[groups['k3s_master'][0]].ansible_host }}"

- name: Create K3S configuration directory
  file:
    path: "{{ item }}"
    state: directory
  loop:
    - /etc/rancher/k3s

- name: Generate k3s token file on all nodes
  ansible.builtin.copy:
    content: "{{ k3s_token }}"
    dest: "{{ k3s_token_file }}"
    mode: 0600

- name: Copy kubelet configuration file
  copy:
    dest: "{{ k3s_config_directory }}/kubelet.config"
    content: "{{ k3s_kubelet_config }}"

- name: Copy k3s configuration file
  ansible.builtin.template:
    src: "templates/config.yml.j2"
    dest: "{{ k3s_config_file }}"
    mode: 0644
EOL

cat <<'EOL' > wait_for_master_node.yml
---

- name: "Wait for master node to be ready"
  command:
    cmd: "kubectl get nodes {{ item }}"
  register: nodes
  until:
    - '" Ready "  in nodes.stdout'
  retries: 10
  delay: 5
  with_items: "{{ inventory_hostname }}"
EOL

cat <<'EOL' > wait_for_primary_master.yml
---

- name: Check that the control plane is available to accept connections
  ansible.builtin.wait_for:
    port: '6443'
    host: "{{ hostvars[groups['k3s_master'][0]].ansible_host }}"
    delay: 5
    sleep: 5
    timeout: 300
EOL

cd ..

cd templates

cat <<'EOL' > config.yml.j2
{% if k3s_build_cluster and k3s_primary_control_node %}
cluster-init: true
{% else %}
server: https://{{ k3s_registration_ip }}:6443
{% endif %}
token-file: {{ k3s_token_file }}
{% if 'k3s_master' in group_names %}
{{ k3s_server_config | to_nice_yaml }}
{% endif %}
EOL

cd ..

cd vars

cat <<'EOL' > main.yml
---
# HA configuration
k3s_build_cluster: false
k3s_primary_control_node: false


# Config directory location for k3s
k3s_config_dir: "{{ k3s_config_file | dirname }}"

# Directory for gathering the k3s token for clustering.
k3s_token_file: "{{ k3s_config_dir }}/cluster-token"
EOL

cd ../..

cd prereq

# Create the prereq's subdirectories
mkdir -p handlers tasks

cd handlers

cat <<'EOL' > main.yml
---
- name: reboot
  reboot:
EOL

cd ..

cd tasks

cat <<'EOL' > disable_swap.yml
---

- name: System Configuration (2) | Disable swap at runtime
  ansible.builtin.command: swapoff -a
  when: ansible_swaptotal_mb > 0
- name: System Configuration (2) | Disable swap at boot
  ansible.posix.mount:
    name: "{{ item }}"
    fstype: swap
    state: absent
  loop: ["none", "swap"]
EOL

cat <<'EOL' > main.yml
---

- name: System Configuration (2) | Disable swap at runtime
  ansible.builtin.command: swapoff -a
  when: ansible_swaptotal_mb > 0
- name: System Configuration (2) | Disable swap at boot
  ansible.posix.mount:
    name: "{{ item }}"
    fstype: swap
    state: absent
  loop: ["none", "swap"]
EOL

cd ../..

cd worker

# Create the worker's subdirectories
mkdir -p defaults tasks templates vars

cd defaults

cat <<'EOL' > main.yml
---

- name: System Configuration (2) | Disable swap at runtime
  ansible.builtin.command: swapoff -a
  when: ansible_swaptotal_mb > 0
- name: System Configuration (2) | Disable swap at boot
  ansible.posix.mount:
    name: "{{ item }}"
    fstype: swap
    state: absent
  loop: ["none", "swap"]
EOL

cd ..

cd tasks

cat <<'EOL' > main.yml
---

- name: Run pre-configuration tasks
  include_tasks: pre_configuration.yml

- name: Get K3s installation script
  get_url:
    url: https://get.k3s.io
    dest: /tmp/k3s_install.sh
    mode: '0766'

- name: Install K3s
  command: "/tmp/k3s_install.sh agent"
  environment:
    INSTALL_K3S_VERSION: "{{ k3s_version }}"
  changed_when: true
EOL

cat <<'EOL' > pre_configuration.yml
---

- name: Ensure registration ip is defined
  ansible.builtin.set_fact:
    k3s_registration_ip: "{{ k3s_api_vip | default(hostvars[groups['k3s_master'][0]].ansible_host) }}"

- name: Create K3S configuration directory
  file:
    path: "{{ item }}"
    state: directory
  loop:
    - /etc/rancher/k3s

- name: Generate k3s token file on all nodes
  ansible.builtin.copy:
    content: "{{ k3s_token }}"
    dest: "{{ k3s_token_file }}"
    mode: 0600

- name: Copy kubelet configuration file
  copy:
    dest: "{{ k3s_config_directory }}/kubelet.config"
    content: "{{ k3s_kubelet_config }}"

- name: Copy k3s configuration file
  ansible.builtin.template:
    src: "templates/config.yml.j2"
    dest: "{{ k3s_config_file }}"
    mode: 0644
EOL

cd ..

cd templates

cat <<'EOL' > config.yml.j2
server: https://{{ k3s_registration_ip }}:6443

token-file: {{ k3s_token_file }}
{{ k3s_agent_config | to_nice_yaml }}
EOL

cd ..

cd vars

cat <<'EOL' > main.yml
---

# Config directory location for k3s
k3s_config_dir: "{{ k3s_config_file | dirname }}"

# Directory for gathering the k3s token for clustering.
k3s_token_file: "{{ k3s_config_dir }}/cluster-token"
EOL

cd ../../..

chmod +x master/defaults/main.yml
chmod +x master/tasks/installation.yml
chmod +x master/tasks/k3s_install.yml
chmod +x master/tasks/main.yml
chmod +x master/tasks/pre_configuration.yml
chmod +x master/tasks/wait_for_master_node.yml
chmod +x master/tasks/wait_for_primary_master.yml
chmod +x master/templates/config.yml.j2
chmod +x master/vars/main.yml
chmod +x prereq/handlers/main.yml
chmod +x prereq/tasks/disable_swap.yml
chmod +x prereq/tasks/main.yml
chmod +x worker/defaults/main.yml
chmod +x worker/tasks/main.yml
chmod +x worker/tasks/pre_configuration.yml
chmod +x worker/templates/config.yml.j2
chmod +x worker/vars/main.yml