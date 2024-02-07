#!/bin/bash

# Create the subdirectories
#mkdir -p .vault group_vars host_vars roles tasks templates vars
mkdir -p vars

cat <<'EOL' > network

EOL

cat <<'EOL' > .yamllint
---
extends: default

ignore: |
  ansible_collections/
  vars/vault.yml
  roles/Liebmann5.*/
  docs/

rules:
  line-length:
    max: 180
    level: warning
EOL

cat <<'EOL' > backup_configuration.yml
---

- name: Configure Pi-cluster nodes backup
  hosts: picluster:bigHouse
  gather_facts: true
  tags: [backup]
  become: true
  pre_tasks:
    - name: Include vault variables
      include_vars: "vars/vault.yml"
    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"
    - name: Load CA certificate for restic
      set_fact:
        restic_ca_cert: "{{ lookup('file','certificates/CA.pem') }}"
      when: not enable_letsencrypt
    - name: Do not use CA certificate
      set_fact:
        restic_use_ca_cert: false
      when: enable_letsencrypt
  roles:
    - role: Liebmann5.backup
      tags: [backup]
EOL

cat <<'EOL' > create_vault_credentials.yml
---

- name: Generate vault variables file
  hosts: localhost

  vars_prompt:
    - name: ionos_public_prefix
      prompt: Enter IONOS public prefix
      private: true
    - name: ionos_secret
      prompt: Enter IONOS secret
      private: true

  pre_tasks:
    - name: Ask for SAN centralized credentials
      when: centralized_san
      block:
        - name: Ask for SAN iscsi credentials 1/2
          pause:
            prompt: "Enter iSCSI node password: "
            echo: false
          register: prompt
        - name: Set iSCSI node password variable
          set_fact:
            san_iscsi_node_pass: "{{ prompt.user_input }}"
          no_log: true
        - name: Ask for SAN iscsi credentials 2/2
          pause:
            prompt: "Enter iSCSI mutual password: "
            echo: false
          register: prompt
        - name: Set iSCSI node password variable
          set_fact:
            san_iscsi_mutual_pass: "{{ prompt.user_input }}"
          no_log: true

  tasks:

    - name: Create random passwords
      ansible.builtin.set_fact:
        "{{ item }}": "{{ lookup('ansible.builtin.password', '/dev/null chars=ascii_letters,digits' ) }}"
      with_items:
        - k3s_token
        - minio_root_password
        - minio_restic_password
        - minio_longhorn_password
        - minio_velero_password
        - minio_loki_password
        - minio_tempo_password
        - traefik_basic_auth_password
        - fluentd_shared_key
        - grafana_admin_password
        - elasticsearch_admin_password
        - elasticsearch_fluentd_password
        - elasticsearch_prometheus_password

    - name: Generate vault file
      ansible.builtin.template:
        src: vars/vault.yml.j2
        dest: vars/vault.yml

    - name: Encrypt file
      ansible.builtin.command:
        cmd: ansible-vault encrypt --vault-password-file=./.vault/vault-pass.sh vars/vault.yml
EOL

cat <<'EOL' > deploy_monitoring_agent.yml
---
# Deploy fluentbit to get logs and prometheus metrics
- name: Deploy fluentbit on control nodes (bigHouse and grandWizard)
  hosts: bigHouse
  gather_facts: true
  tags: [logging]
  become: true
  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"
      tags: ["always"]
    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"
      tags: ["always"]
  roles:
    - role: logging/external_node
      tags: ['logging']
EOL

cat <<'EOL' > external_services.yml
---
## Generate TLS certificates for external services
## Generated using certbot (letsencrypt) or selfsigned certificates
- name: Generate external services certificates
  hosts: localhost
  gather_facts: true
  tags: [certificates]
  vars:
    propagation_seconds: 300
    selfsigned_certificates_path: "../certificates"
  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"
    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

    - name: Copy ionos secret file
      template:
        src: "{{ item.template }}"
        dest: "{{ item.dest }}"
        mode: 0600
      with_items:
        - template: ionos-credentials.ini.j2
          dest: "~/.secrets/ionos-credentials.ini"
      when: enable_letsencrypt

  tasks:
    - name: Create Letsencrypt certificate for external services
      command: |
        certbot certonly \
        --authenticator dns-ionos \
        --dns-ionos-credentials ~/.secrets/ionos-credentials.ini \
        --dns-ionos-propagation-seconds {{ propagation_seconds }} \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --agree-tos \
        --non-interactive \
        --rsa-key-size 4096 \
        -m {{ acme_issuer_email }} \
        -d {{ item }}
      register: certbot_create
      changed_when:
        - certbot_create.rc==0
        - '"Certificate not yet due for renewal; no action taken." not in certbot_create.stdout'
      when: enable_letsencrypt
      with_items:
        - "{{ minio_hostname }}"
        - "{{ vault_hostname }}"

    - name: Create customCA-signed TLS certificate for minio
      when: not enable_letsencrypt
      block:
        # Generate self-signed certificates directory
        - name: Create certificates directory
          file:
            path: "{{ selfsigned_certificates_path }}"
            state: directory
            mode: 0750
        # Include selfsigned certificates variables
        - name: Include selfsigned certificates variables
          include_vars: "vars/selfsigned-certificates.yml"
        # Generate custom CA
        - name: Generate custom CA
          include_tasks: tasks/generate_custom_ca.yml
          args:
            apply:
              delegate_to: localhost
              become: false
        # Generate selfsigned TLS certificate
        - name: Generate customCA-signed SSL certificates
          include_tasks: tasks/generate_ca_signed_cert.yml
          args:
            apply:
              delegate_to: localhost
              become: false
          loop:
            - "{{ minio_hostname }}"
            - "{{ vault_hostname }}"
          loop_control:
            loop_var: server_hostname

## Install Minio S3 Storage Server

- name: Install Minio S3 Storage Server
  hosts: s3
  gather_facts: true
  tags: [s3]
  become: true
  vars:
    server_hostname: "{{ minio_hostname }}"
    selfsigned_certificates_path: "../certificates"
  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"
    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

    - name: Load customCA-signed TLS certificate for minio
      set_fact:
        minio_key: "{{ lookup('file',selfsigned_certificates_path + '/' + server_hostname + '.key') }}"
        minio_cert: "{{ lookup('file',selfsigned_certificates_path + '/' + server_hostname + '.pem') }}"
      when: not enable_letsencrypt

    - name: Get letsencrypt TLS certificate for minio
      block:
        - name: check TLS certificate for minio exits
          command: "certbot certificates -d {{ minio_hostname }}"
          register: certbot_certificates
          delegate_to: localhost
          become: false
          changed_when: false
          failed_when:
            - '"Certificate Name: " + minio_hostname not in certbot_certificates.stdout'
        - name: Get certificate and key paths for minio
          set_fact:
            cert_path: "{{ certbot_certificates.stdout | regex_search(regexp1,'\\1') }}"
            cert_key_path: "{{ certbot_certificates.stdout | regex_search(regexp2,'\\1') }}"
          vars:
            regexp1: 'Certificate Path: (\S+)'
            regexp2: 'Private Key Path: (\S+)'
          when:
            - certbot_certificates.rc==0
            - '"Certificate Name: " + minio_hostname in certbot_certificates.stdout'

        - name: Load tls key and cert
          set_fact:
            minio_key: "{{ lookup('file', cert_key_path[0] ) }}"
            minio_cert: "{{ lookup('file', cert_path[0] ) }}"
      when: enable_letsencrypt
  roles:
    - role: Liebmann5.minio

## Install Hashicorp Vault Server

- name: Install Vault Server
  hosts: bigHouse
  gather_facts: true
  tags: [vault]
  become: true
  vars:
    server_hostname: "{{ vault_hostname }}"
    selfsigned_certificates_path: "../certificates"

  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"

    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

    - name: Load customCA-signed TLS certificate for minio
      set_fact:
        vault_key: "{{ lookup('file',selfsigned_certificates_path + '/' + server_hostname + '.key') }}"
        vault_cert: "{{ lookup('file',selfsigned_certificates_path + '/' + server_hostname + '.pem') }}"
        vault_ca: "{{ lookup('file',selfsigned_certificates_path + '/CA.pem') }}"
      when: not enable_letsencrypt

    - name: Get letsencrypt TLS certificate for vault
      block:
        - name: check TLS certificate for vault exits
          command: "certbot certificates -d {{ vault_hostname }}"
          register: certbot_certificates
          delegate_to: localhost
          become: false
          changed_when: false
          failed_when:
            - '"Certificate Name: " + vault_hostname not in certbot_certificates.stdout'
        - name: Get certificate and key paths for minio
          set_fact:
            cert_path: "{{ certbot_certificates.stdout | regex_search(regexp1,'\\1') }}"
            cert_key_path: "{{ certbot_certificates.stdout | regex_search(regexp2,'\\1') }}"
          vars:
            regexp1: 'Certificate Path: (\S+)'
            regexp2: 'Private Key Path: (\S+)'
          when:
            - certbot_certificates.rc==0
            - '"Certificate Name: " + vault_hostname in certbot_certificates.stdout'

        - name: Load tls key and cert
          set_fact:
            vault_key: "{{ lookup('file', cert_key_path[0] ) }}"
            vault_cert: "{{ lookup('file', cert_path[0] ) }}"
      when: enable_letsencrypt
  roles:
    - role: Liebmann5.vault

  tasks:
    # Configure ansible user profile with VAULT environement variables
    - name: Insert http(s) export in dotfile
      become: true
      lineinfile:
        path: ~{{ ansible_user }}/.bashrc
        regexp: "^export VAULT_ADDR="
        line: "export VAULT_ADDR='https://{{ vault_hostname }}:8200'"
        owner: "{{ ansible_user }}"
        create: true
        mode: 0644
    - name: Insert CA cert export in dotfile
      become: true
      lineinfile:
        path: ~{{ ansible_user }}/.bashrc
        regexp: "^export VAULT_CACERT="
        line: "export VAULT_CACERT=/etc/vault/tls/vault-ca.crt"
        owner: "{{ ansible_user }}"
        create: true
        mode: 0644
      when: custom_ca

    - name: Insert VAULT_TOKEN in dotfile
      become: true
      lineinfile:
        path: ~{{ ansible_user }}/.bashrc
        regexp: "^export VAULT_TOKEN="
        line: "export VAULT_TOKEN=$(sudo jq -r '.root_token' /etc/vault/unseal.json)"
        owner: "{{ ansible_user }}"
        create: true
        mode: 0644

## Load all credentials into Hashicorp Vault Server
- name: Load Vault Credentials
  hosts: bigHouse
  gather_facts: true
  tags: [vault, credentials]
  become: false
  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"

    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

    # Install hashicorp vault collection dependencies (hvac python package) using PIP.
    - name: Ensure PIP is installed.
      package:
        name:
          - python3-pip
          - python3-setuptools
        state: present
      become: true
    - name: Ensure hvac Python library is installed.
      pip:
        name: hvac
        state: present
      become: true
  tasks:

    # Vault Login using ansible environement variables for creating token file
    # token file will be usd in next commands
    - name: Vault login
      ansible.builtin.shell: bash -ilc 'vault login $VAULT_TOKEN'
      # Interactive bash so .bashrc is loaded
      # 'source ~/.bashrc && <command>' does not work because
      # Ansible shell is not interactive and ~/.bashrc implementation by default ignores non interactive shell.
      # See lines at beginning of bashrc:
      #
      # If not running interactively, don't do anything
      # case $- in
      #     *i*) ;;
      #       *) return;;
      # esac
      # The best solution for executing commands as user after its ssh interactive login:
      # bash -ilc '<command>'
      # '-i' means interactive shell, so .bashrc won't be ignored '-l' means login shell which sources full user profile
      become: false
      register: vault_login

    # Create write token
    - name: Create KV write token
      community.hashi_vault.vault_token_create:
        url: "https://{{ vault_dns }}:8200"
        policies: ["write"]
      register: token_data
      become: false
    # Load ansible vault variables into Hashicorp Vault Server
    - name: Load vault credentials
      include_tasks:
        file: tasks/load_vault_credentials.yml
      loop: "{{ vault | dict2items }}"
      loop_control:
        loop_var: secret_group
      when:
        - vault is defined
      no_log: true

    - name: Load http auth_basic credentials
      include_tasks:
        file: tasks/create_basic_auth_credentials.yml
      no_log: true

    - name: Load minio prometheus bearer credentials
      include_tasks:
        file: tasks/create_minio_bearer_token.yml
      no_log: true---
## Generate TLS certificates for external services
## Generated using certbot (letsencrypt) or selfsigned certificates
- name: Generate external services certificates
  hosts: localhost
  gather_facts: true
  tags: [certificates]
  vars:
    propagation_seconds: 300
    selfsigned_certificates_path: "../certificates"
  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"
    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

    - name: Copy ionos secret file
      template:
        src: "{{ item.template }}"
        dest: "{{ item.dest }}"
        mode: 0600
      with_items:
        - template: ionos-credentials.ini.j2
          dest: "~/.secrets/ionos-credentials.ini"
      when: enable_letsencrypt

  tasks:
    - name: Create Letsencrytp certificate for external services
      command: |
        certbot certonly \
        --authenticator dns-ionos \
        --dns-ionos-credentials ~/.secrets/ionos-credentials.ini \
        --dns-ionos-propagation-seconds {{ propagation_seconds }} \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --agree-tos \
        --non-interactive \
        --rsa-key-size 4096 \
        -m {{ acme_issuer_email }} \
        -d {{ item }}
      register: certbot_create
      changed_when:
        - certbot_create.rc==0
        - '"Certificate not yet due for renewal; no action taken." not in certbot_create.stdout'
      when: enable_letsencrypt
      with_items:
        - "{{ minio_hostname }}"
        - "{{ vault_hostname }}"

    - name: Create customCA-signed TLS certificate for minio
      when: not enable_letsencrypt
      block:
        # Generate self-signed certificates directory
        - name: Create certificates directory
          file:
            path: "{{ selfsigned_certificates_path }}"
            state: directory
            mode: 0750
        # Include selfsigned certificates variables
        - name: Include selfsigned certificates variables
          include_vars: "vars/selfsigned-certificates.yml"
        # Generate custom CA
        - name: Generate custom CA
          include_tasks: tasks/generate_custom_ca.yml
          args:
            apply:
              delegate_to: localhost
              become: false
        # Generate selfsigned TLS certificate
        - name: Generate customCA-signed SSL certificates
          include_tasks: tasks/generate_ca_signed_cert.yml
          args:
            apply:
              delegate_to: localhost
              become: false
          loop:
            - "{{ minio_hostname }}"
            - "{{ vault_hostname }}"
          loop_control:
            loop_var: server_hostname

## Install Minio S3 Storage Server

- name: Install Minio S3 Storage Server
  hosts: s3
  gather_facts: true
  tags: [s3]
  become: true
  vars:
    server_hostname: "{{ minio_hostname }}"
    selfsigned_certificates_path: "../certificates"
  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"
    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

    - name: Load customCA-signed TLS certificate for minio
      set_fact:
        minio_key: "{{ lookup('file',selfsigned_certificates_path + '/' + server_hostname + '.key') }}"
        minio_cert: "{{ lookup('file',selfsigned_certificates_path + '/' + server_hostname + '.pem') }}"
      when: not enable_letsencrypt

    - name: Get letsencrypt TLS certificate for minio
      block:
        - name: check TLS certificate for minio exits
          command: "certbot certificates -d {{ minio_hostname }}"
          register: certbot_certificates
          delegate_to: localhost
          become: false
          changed_when: false
          failed_when:
            - '"Certificate Name: " + minio_hostname not in certbot_certificates.stdout'
        - name: Get certificate and key paths for minio
          set_fact:
            cert_path: "{{ certbot_certificates.stdout | regex_search(regexp1,'\\1') }}"
            cert_key_path: "{{ certbot_certificates.stdout | regex_search(regexp2,'\\1') }}"
          vars:
            regexp1: 'Certificate Path: (\S+)'
            regexp2: 'Private Key Path: (\S+)'
          when:
            - certbot_certificates.rc==0
            - '"Certificate Name: " + minio_hostname in certbot_certificates.stdout'

        - name: Load tls key and cert
          set_fact:
            minio_key: "{{ lookup('file', cert_key_path[0] ) }}"
            minio_cert: "{{ lookup('file', cert_path[0] ) }}"
      when: enable_letsencrypt
  roles:
    - role: ricsanfre.minio

## Install Hashicorp Vault Server

- name: Install Vault Server
  hosts: gateway
  gather_facts: true
  tags: [vault]
  become: true
  vars:
    server_hostname: "{{ vault_hostname }}"
    selfsigned_certificates_path: "../certificates"

  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"

    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

    - name: Load customCA-signed TLS certificate for minio
      set_fact:
        vault_key: "{{ lookup('file',selfsigned_certificates_path + '/' + server_hostname + '.key') }}"
        vault_cert: "{{ lookup('file',selfsigned_certificates_path + '/' + server_hostname + '.pem') }}"
        vault_ca: "{{ lookup('file',selfsigned_certificates_path + '/CA.pem') }}"
      when: not enable_letsencrypt

    - name: Get letsencrypt TLS certificate for vault
      block:
        - name: check TLS certificate for vault exits
          command: "certbot certificates -d {{ vault_hostname }}"
          register: certbot_certificates
          delegate_to: localhost
          become: false
          changed_when: false
          failed_when:
            - '"Certificate Name: " + vault_hostname not in certbot_certificates.stdout'
        - name: Get certificate and key paths for minio
          set_fact:
            cert_path: "{{ certbot_certificates.stdout | regex_search(regexp1,'\\1') }}"
            cert_key_path: "{{ certbot_certificates.stdout | regex_search(regexp2,'\\1') }}"
          vars:
            regexp1: 'Certificate Path: (\S+)'
            regexp2: 'Private Key Path: (\S+)'
          when:
            - certbot_certificates.rc==0
            - '"Certificate Name: " + vault_hostname in certbot_certificates.stdout'

        - name: Load tls key and cert
          set_fact:
            vault_key: "{{ lookup('file', cert_key_path[0] ) }}"
            vault_cert: "{{ lookup('file', cert_path[0] ) }}"
      when: enable_letsencrypt
  roles:
    - role: ricsanfre.vault

  tasks:
    # Configure ansible user profile with VAULT environement variables
    - name: Insert http(s) export in dotfile
      become: true
      lineinfile:
        path: ~{{ ansible_user }}/.bashrc
        regexp: "^export VAULT_ADDR="
        line: "export VAULT_ADDR='https://{{ vault_hostname }}:8200'"
        owner: "{{ ansible_user }}"
        create: true
        mode: 0644
    - name: Insert CA cert export in dotfile
      become: true
      lineinfile:
        path: ~{{ ansible_user }}/.bashrc
        regexp: "^export VAULT_CACERT="
        line: "export VAULT_CACERT=/etc/vault/tls/vault-ca.crt"
        owner: "{{ ansible_user }}"
        create: true
        mode: 0644
      when: custom_ca

    - name: Insert VAULT_TOKEN in dotfile
      become: true
      lineinfile:
        path: ~{{ ansible_user }}/.bashrc
        regexp: "^export VAULT_TOKEN="
        line: "export VAULT_TOKEN=$(sudo jq -r '.root_token' /etc/vault/unseal.json)"
        owner: "{{ ansible_user }}"
        create: true
        mode: 0644

## Load all credentials into Hashicorp Vault Server
- name: Load Vault Credentials
  hosts: gateway
  gather_facts: true
  tags: [vault, credentials]
  become: false
  pre_tasks:
    # Include vault variables
    - name: Include vault variables
      include_vars: "vars/vault.yml"

    # Include picluster variables
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

    # Install hashicorp vault collection dependencies (hvac python package) using PIP.
    - name: Ensure PIP is installed.
      package:
        name:
          - python3-pip
          - python3-setuptools
        state: present
      become: true
    - name: Ensure hvac Python library is installed.
      pip:
        name: hvac
        state: present
      become: true
  tasks:

    # Vault Login using ansible environement variables for creating token file
    # token file will be usd in next commands
    - name: Vault login
      ansible.builtin.shell: bash -ilc 'vault login $VAULT_TOKEN'
      # Interactive bash so .bashrc is loaded
      # 'source ~/.bashrc && <command>' does not work because
      # Ansible shell is not interactive and ~/.bashrc implementation by default ignores non interactive shell.
      # See lines at beginning of bashrc:
      #
      # If not running interactively, don't do anything
      # case $- in
      #     *i*) ;;
      #       *) return;;
      # esac
      # The best solution for executing commands as user after its ssh interactive login:
      # bash -ilc '<command>'
      # '-i' means interactive shell, so .bashrc won't be ignored '-l' means login shell which sources full user profile
      become: false
      register: vault_login

    # Create write token
    - name: Create KV write token
      community.hashi_vault.vault_token_create:
        url: "https://{{ vault_dns }}:8200"
        policies: ["write"]
      register: token_data
      become: false
    # Load ansible vault variables into Hashicorp Vault Server
    - name: Load vault credentials
      include_tasks:
        file: tasks/load_vault_credentials.yml
      loop: "{{ vault | dict2items }}"
      loop_control:
        loop_var: secret_group
      when:
        - vault is defined
      no_log: true

    - name: Load http auth_basic credentials
      include_tasks:
        file: tasks/create_basic_auth_credentials.yml
      no_log: true

    - name: Load minio prometheus bearer credentials
      include_tasks:
        file: tasks/create_minio_bearer_token.yml
      no_log: true
EOL

-----------------------------------------------------------------------------------------
cat <<'EOL' > inventory.yml
---
all:
  children:
    control:
      hosts:
        bigHouse:
          hostname: bigHouse
          ansible_host: 10.0.0.1
          ip: 10.0.0.1
          mac: D8:3A:DD:24:88:E5
        grandWizard:
          hostname: grandWizard
          ansible_host: localhost
          ansible_connection: local
    external:
      hosts:
        s3:
          hostname: s3
          ansible_host: s3.liebmann5.com
    picluster:
      hosts:
        node1:
          hostname: node1
          ansible_host: 10.0.0.11
          ip: 10.0.0.11
          mac: D8:3A:DD:2D:80:47
        node2:
          hostname: node2
          ansible_host: 10.0.0.12
          ip: 10.0.0.12
          mac: D8:3A:DD:24:76:DA
    raspberrypi:
      hosts:
        node[1:2]:
        gateway:
    k3s_cluster:
      children:
        k3s_master:
          hosts:
            node[1:1]:
        k3s_worker:
          hosts:
            node[2:2]:
EOL
-----------------------------------------------------------------------------------------

cat <<'EOL' > k3s_bootstrap.yml
---

- name: Bootstrap Cluster
  hosts: worker1
  gather_facts: false

  collections:
    - kubernetes.core

  environment:
    # The location of the kubeconfig file on the master.
    K8S_AUTH_KUBECONFIG: ~/.kube/config

  pre_tasks:
    # Install Python PIP and jq utility packages
    - name: Ensure required packages are installed.
      package:
        name:
          - python3-pip
          - python3-setuptools
          - jq
        state: present
      become: true
    # Install kubernetes python packages (Ansible kubernetes collection dependency)
    - name: Ensure kubernetes Python library is installed.
      pip:
        name: kubernetes
        state: present
      become: true
    # Install Hashicorp python packages (Ansible hashi module dependency)
    - name: Ensure hashicorp vault python library is installed.
      pip:
        name: hvac
        state: present
      become: true

    # Install Helm diff plugin to have a better idempotence check
    - name: Intall Helm Plugin
      kubernetes.core.helm_plugin:
        plugin_path: "https://github.com/databus23/helm-diff"
        state: present

    - name: Include vault variables
      include_vars: "vars/vault.yml"

    - name: Include picluster variables
      include_vars: "vars/picluster.yml"

  tasks:
    - name: Create namespaces.
      kubernetes.core.k8s:
        name: "{{ item }}"
        api_version: v1
        kind: Namespace
        state: present
      with_items:
        - "argocd"
        - "vault"

    - name: Configure Vault integration
      include_tasks: tasks/configure_vault_integration.yml

    - name: Copy argocd chart and crds
      ansible.builtin.copy:
        src: "../argocd/{{ item }}"
        dest: /tmp/charts
      with_items:
        - "bootstrap/crds"
        - "bootstrap/argocd"

    - name: Install CRDs
      ansible.builtin.command:
        cmd: kubectl apply --server-side --kustomize  /tmp/charts/crds

    - name: Update argo-cd helm dependency.
      ansible.builtin.command:
        cmd: "helm dependency update /tmp/charts/argocd"

    - name: Deploy Argo CD Helm chart.
      shell: |
        set -o pipefail
        helm template \
        --dependency-update \
        --include-crds \
        --namespace argocd \
        argocd /tmp/charts/argocd \
        | kubectl apply -n argocd -f -
      args:
        executable: /bin/bash

    - name: Wait for CRDs to be ready
      command:
        cmd: "kubectl wait --for condition=Established crd/applications.argoproj.io crd/applicationsets.argoproj.io --timeout=600s"
      changed_when: false

    - name: Deploy root application
      kubernetes.core.k8s:
        definition: "{{ lookup('template', 'templates/' + item ) }}"
        state: present
      with_items:
        - argocd_root_app.yml.j2

    - name: Recursively remove tmp directory
      ansible.builtin.file:
        path: /tmp/charts
        state: absent

    - name: Install cli utils.
      include_tasks: tasks/install_cli_utils.yml
EOL

------------------(nodes keyword | directory nodes -> workers)--------------------------------------------
cat <<'EOL' > k3s_install.yml
---

- name: Install load balancer
  hosts: bigHouse
  gather_facts: true
  tags: [install]
  become: true
  roles:
    - role: haproxy

- name: Install K3S prerequisites
  hosts: k3s_cluster
  gather_facts: true
  tags: [install]
  become: true
  pre_tasks:
    - name: Include vault variables
      include_vars: "vars/vault.yml"
      tags: ["always"]
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"
      tags: ["always"]
  roles:
    - role: k3s/prereq

- name: Install K3S master node
  hosts: k3s_master
  tags: [install]
  become: true
  pre_tasks:
    - name: Include vault variables
      include_vars: "vars/vault.yml"
      tags: ["always"]
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"
      tags: ["always"]
  roles:
    - role: k3s/master
    - role: Liebmann5.k8s_cli

- name: Install K3S worker nodes
  hosts: k3s_worker
  tags: [install]
  become: true
  pre_tasks:
    - name: Include vault variables
      include_vars: "vars/vault.yml"
      tags: ["always"]
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"
      tags: ["always"]
  roles:
    - role: k3s/worker

- name: Label K3S worker nodes
  hosts: k3s_master
  tags: [config]
  pre_tasks:
    - name: Include vault variables
      include_vars: "vars/vault.yml"
      tags: ["always"]
    - name: Include picluster variables
      include_vars: "vars/picluster.yml"
      tags: ["always"]
  tasks:
    - name: "Wait for worker nodes to be ready"
      command:
        cmd: "kubectl get nodes {{ item }}"
      register: nodes
      until:
        - '" Ready "  in nodes.stdout'
      retries: 10
      delay: 5
      with_items: "{{ groups['k3s_worker'] }}"

    - name: label k3s worker nodes
      command:
        cmd: "kubectl label nodes {{ item }} kubernetes.io/role=worker"
      with_items: "{{ groups['k3s_worker'] }}"

- name: Get Kubernets config file
  hosts: k3s_master
  tags: [kube-config]
  tasks:
    - name: Get k3s config file
      run_once: true
      ansible.builtin.slurp:
        src: /etc/rancher/k3s/k3s.yaml
      register: kubeconfig_base64

    - name: Write Kubernetes config file with the correct cluster address
      ansible.builtin.copy:
        content: "{{ kubeconfig_base64.content | b64decode | replace('127.0.0.1', k3s_api_vip ) }}"
        dest: "~/.kube/config"
        mode: 0600
      delegate_to: localhost
      run_once: true
EOL
--------------------------------------------------------------

cat <<'EOL' > k3s_reset.yml
---
- hosts: k3s_master
  become: true
  gather_facts: false
  tasks:
    - name: Uninstall k3s
      command: /usr/local/bin/k3s-uninstall.sh
      changed_when: true
    - import_tasks: tasks/cleaning.yml
      tags: ['clean']

- hosts: k3s_worker
  become: true
  gather_facts: false
  tasks:
    - name: Uninstall k3s
      command: /usr/local/bin/k3s-agent-uninstall.sh
      changed_when: true
    - import_tasks: tasks/cleaning.yml
      tags: ['clean']
EOL

cat <<'EOL' > k3s_start.yml
---
- hosts: k3s_master
  become: true
  gather_facts: false
  tasks:
    - name: Start K3S Service
      service:
        name: k3s
        state: started
- hosts: k3s_worker
  become: true
  gather_facts: false
  tasks:
    - name: Start K3S Service
      service:
        name: k3s-agent
        state: started
EOL

cat <<'EOL' > k3s_stop.yml
---

- hosts: k3s_master
  become: true
  gather_facts: false
  tasks:
    - name: Stop K3S Service
      service:
        name: k3s
        state: stopped

- hosts: k3s_worker
  become: true
  gather_facts: false
  tasks:
    - name: Stop K3S Service
      service:
        name: k3s-agent
        state: stopped

- hosts: k3s_master
  become: true
  gather_facts: false
  tasks:
    - name: Stop k3s containers and free network resources
      command: /usr/local/bin/k3s-killall.sh
      changed_when: true

- hosts: k3s_worker
  become: true
  gather_facts: false
  tasks:
    - name: Stop k3s containers and free network resources
      command: /usr/local/bin/k3s-killall.sh
      changed_when: true
EOL

cat <<'EOL' > patch_grafana_dashboards.yml
---
- name: Patch Grafana Dashboards
  hosts: localhost

  tasks:
    - name: Patch Grafana Dashboards
      include_tasks: tasks/patch_grafana_dashboard.yml
      loop_control:
        loop_var: dashboard_file
      with_fileglob:
        - "roles/prometheus/dashboards/*"
        - "roles/prometheus/dashboards/linkerd/*"
        - "roles/prometheus/dashboards/k3s/*"
EOL

cat <<'EOL' > requirements.yml
---
roles:
  - name: ricsanfre.security
    version: v1.0.0
  - name: ricsanfre.ntp
    version: v1.0.0
  - name: ricsanfre.firewall
    version: v1.0.0
  - name: ricsanfre.dnsmasq
    version: v1.0.2
  - name: Liebmann5.storage
    version: v1.0.0
  - name: Liebmann5.iscsi_target
    version: v1.0.0
  - name: Liebmann5.iscsi_initiator
    version: v1.1.0
  - name: Liebmann5.k8s_cli
    version: v1.0.0
  - name: ricsanfre.fluentbit
    version: v1.0.4
  - name: Liebmann5.minio
    version: v1.1.3
  - name: Liebmann5.backup
    version: v1.1.3
  - name: Liebmann5.vault
    version: v1.0.4
collections:
  - name: kubernetes.core
    version: 2.3.2
  - name: community.hashi_vault
    version: 4.0.0
EOL

cat <<'EOL' > reset_external_services.yml
---
- name: Clean Minio Installation
  hosts: s3
  become: true
  gather_facts: false
  tags: [s3]
  tasks:
    - name: Stop and disable Minio Server
      systemd:
        name: minio
        state: stopped
        enabled: false
      become: true
    - name: Delete directories and files
      become: true
      file:
        state: absent
        path: "{{ item }}"
      with_items:
        - /storage/minio/
        - /etc/minio/
        - /usr/local/bin/minio
        - /usr/local/bin/mc
        - /etc/systemd/system/minio.service
        - ~/.mc
    - name: Reload systemd daemon
      systemd:
        daemon_reload: true

- name: Clean Vault Installation
  hosts: bigHouse
  become: true
  gather_facts: false
  tags: [vault]
  tasks:
    - name: Stop and disable Vault Server
      systemd:
        name: "{{ item }}"
        state: stopped
        enabled: false
      become: true
      with_items:
        - vault
        - vault-unseal
    - name: Delete directories and files
      become: true
      file:
        state: absent
        path: "{{ item }}"
      with_items:
        - /var/lib/vault/
        - /etc/vault/
        - /var/log/vault/
        - /usr/local/bin/vault
        - /etc/systemd/system/vault.service
        - /etc/systemd/system/vault-unseal.service
    - name: Reload systemd daemon
      systemd:
        daemon_reload: true

- name: Clean Restic Installation
  hosts: picluster:bigHouse
  become: true
  gather_facts: false
  tags: [restic]
  tasks:
    - name: Stop and disable restic backup service
      systemd:
        name: "{{ item }}"
        state: stopped
        enabled: false
      become: true
      with_items:
        - restic-backup.timer

    - name: Stop and disable restic clean service
      systemd:
        name: "{{ item }}"
        state: stopped
        enabled: false
      become: true
      when: restic_clean_service
      with_items:
        - restic-clean.timer

    - name: Delete directories and files
      become: true
      file:
        state: absent
        path: "{{ item }}"
      with_items:
        - /etc/restic/
        - /var/log/restic.log
        - /usr/local/bin/restic
        - /etc/systemd/system/restic-backup.service
        - /etc/systemd/system/restic-backup.timer

    - name: Delete clean service file
      become: true
      file:
        state: absent
        path: "{{ item }}"
      with_items:
        - /etc/systemd/system/restic-clean.timer
        - /etc/systemd/system/restic-clean.service
      when: restic_clean_service

    - name: Reload systemd daemon
      systemd:
        daemon_reload: true
EOL

cat <<'EOL' > setup_picluster.yml
---

- name: Configure Pi Cluster bigHouse
  hosts: bigHouse
  gather_facts: true
  tags: [bigHouse]
  become: true
  pre_tasks:
    - name: Include vault variables
      include_vars: "vars/vault.yml"
      tags: ["always"]
  roles:

    # OS basic setup tasks
    - role: basic_setup
      tags: [os]

    # Security Hardening
    - role: ricsanfre.security
      tags: [security]

    # DNS/DHCP server configuration
    - role: ricsanfre.dnsmasq
      tags: [dnsmasq]

    # Update DNS server to point to DNSmasq
    - role: dns
      tags: [dns]

    # Firewall (nftables) configuration
    - role: ricsanfre.firewall
      tags: [firewall]

    # NTP Server configuration
    - role: ricsanfre.ntp
      tags: [ntp]

- name: Configure Pi Cluster Nodes
  hosts: picluster
  gather_facts: true
  tags: [node]
  become: true
  pre_tasks:
    - name: Include vault variables
      include_vars: "vars/vault.yml"
      tags: ["always"]
  roles:
    # OS basic setup tasks
    - role: basic_setup
      tags: [os]

    # Security Hardening
    - role: ricsanfre.security
      tags: [security]

    # NTP Client configuration
    - role: ricsanfre.ntp
      tags: [ntp]

      # Local Storage configuration
    - name: Dedicated Disks
      block:
        # iSCSI client (initiator) configuration
        # iSCSI initiator needs to be configured for Longhorn
        - name: Configure iSCSI Initiator
          include_role:
            name: Liebmann5.iscsi_initiator
          vars:
            - open_iscsi_automatic_startup: true
      when: not centralized_san
      tags: [storage]
EOL

cat <<'EOL' > shutdown.yml
---
- hosts: picluster
  become: true
  gather_facts: false
  tasks:
    - name: Shutdown
      command: shutdown -h 1 min
      ignore_errors: true

- hosts: bigHouse
  become: true
  gather_facts: false
  tasks:
    - name: Shutdown
      command: shutdown -h 1 min
      ignore_errors: true
EOL

cat <<'EOL' > update.yml
---
- hosts: all
  become: true
  gather_facts: false

  tasks:
    - name: Update apt repo and cache on all Debian/Ubuntu boxes
      apt:
        update_cache: true
        # Run the equivalent of apt-get update command on all servers
        force_apt_get: true
        # Do not use the aptitude command
        # instead use the apt-get command on Debian/Ubuntu boxes
        cache_valid_time: 3600
        # Update the apt cache if its older than the cache_valid_time.
        # This option is set in seconds

    - name: Upgrade all packages on servers
      apt:
        upgrade: dist
        # Run the equivalent of ‘apt-get upgrade’
        force_apt_get: true
        # Use apt-get instead of aptitude

    - name: Check if a reboot is needed on all servers
      stat:
        path: /var/run/reboot-required
        get_md5: false
        # Algorithm to determine checksum of file
      register: reboot_required_file
      # Save a result in and we are going to use it as follows to reboot the box

    - name: Reboot the box if kernel updated
      reboot:
        msg: "Reboot initiated by Ansible for kernel updates"
        connect_timeout: 5
        reboot_timeout: 300
        pre_reboot_delay: 0
        post_reboot_delay: 30
        test_command: uptime
        # Execute uptime command on the rebooted server and expect success from
        # to determine the machine is ready for further tasks
      when: reboot_required_file.stat.exists
      # First, check that the file named /var/run/reboot-required exists using a
      # variable named reboot_required_file.
      # The reboot module will only work if that file exists and it is enforced
      # using ‘when: reboot_required_file.stat.exists’ Ansible condition.
EOL

chmod +x .yamllint
#chmod +x ansible.cfg
chmod +x backup_configuration.yml
chmod +x create_vault_credentials.yml
chmod +x deploy_monitoring_agent.yml
chmod +x external_services.yml
chmod +x inventory.yml
chmod +x k3s_bootstrap.yml
chmod +x k3s_install.yml
chmod +x k3s_reset.yml
chmod +x k3s_start.yml
chmod +x k3s_stop.yml
chmod +x patch_grafana_dashboards.yml
chmod +x requirements.yml
chmod +x reset_external_services.yml
chmod +x setup_picluster.yml
chmod +x shutdown.yml
chmod +x update.yml


cd ..

cd nodes