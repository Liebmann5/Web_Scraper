#!/bin/bash

# Create the tasks directory
mkdir -p tasks

cd tasks

cat <<'EOL' > cleaning.yml
---

- name: Clean Longhorn storage | get content
  become: true
  find:
    paths: /storage
    patterns: '*'
    file_type: any
    hidden: true
  register: directory_content_result
  when: "'k3s_worker' in group_names"

- name: Clean Longhorn storage | delete content
  become: true
  file:
    path: "{{ item.path }}"
    state: absent
  with_items: "{{ directory_content_result.files }}"
  when: "'k3s_worker' in group_names"

- name: Clean longhorn iscsi targets and nodes
  shell: |
    set -o pipefail
    for i in `sudo iscsiadm -m discovery -o show | grep -v 10.0.0.1 | awk '{print $1}'`
    do
    echo "Deleting target $i"
    sudo iscsiadm -m discovery -p $i -o delete
    done
  args:
    executable: /bin/bash
  register: output
  changed_when: true
  when: "'k3s_worker' in group_names"

- name: Clean container/pod logs and fluentbit db
  file:
    path: "{{ item }}"
    state: absent
  with_items:
    - "/var/log/pods"
    - "/var/log/containers"
    - "/var/log/fluentbit"

- name: Clean fluentd pos files | get pos files
  find:
    paths: /var/log
    patterns: '*.pos'
  register: files_to_delete

- name: Clean fluentd pos files | delete pos files
  file:
    path: "{{ item.path }}"
    state: absent
  with_items: "{{ files_to_delete.files }}"
EOL

cat <<'EOL' > configure_vault_integration.yml
---

- name: Configure vault service account and create token
  kubernetes.core.k8s:
    definition: "{{ lookup('ansible.builtin.file', '../argocd/bootstrap/vault/' + item ) }}"
    state: present
  with_items:
    - vault-auth-serviceaccount.yaml

- name: Get Token review
  shell: |
    KUBERNETES_SA_SECRET_NAME=$(kubectl get secrets --output=json -n vault | jq -r '.items[].metadata | select(.name|startswith("vault-auth")).name')
    TOKEN_REVIEW_JWT=$(kubectl get secret $KUBERNETES_SA_SECRET_NAME -n vault -o jsonpath='{.data.token}' | base64 --decode)
    echo $TOKEN_REVIEW_JWT
  register: get_reviewer_token
  changed_when: false

- name: Set reviewer token
  set_fact:
    vault_reviewer_token: "{{ get_reviewer_token.stdout }}"

- name: Get Kubernetes CA cert
  shell: |
    KUBERNETES_CA_CERT=$(kubectl config view --raw --minify --flatten --output='jsonpath={.clusters[].cluster.certificate-authority-data}' \
      | base64 --decode | awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}')
    echo $KUBERNETES_CA_CERT
  register: get_kubernetes_ca
  changed_when: false

- name: Set CA cert
  set_fact:
    kubernetes_ca_cert: "{{ get_kubernetes_ca.stdout }}"

- name: Set kubernetes_host
  set_fact:
    kubernetes_host: "https://{{ k3s_api_vip }}:6443"

- name: Configure vault-kubernetes-auth
  include_tasks: tasks/vault_kubernetes_auth_method_config.yml
EOL

cat <<'EOL' > create_basic_auth_credentials.yml
---

- name: Ensure htpasswd utility is installed
  package:
    name: 'apache2-utils'
    state: 'present'
    update_cache: true
  become: true

- name: htpasswd utility
  shell:
    cmd: >-
      htpasswd -nb {{ traefik_basic_auth_user }} {{ traefik_basic_auth_passwd }}
  register: htpasswd
  changed_when: false

- name: Set htpasswd pair
  set_fact:
    traefik_auth_htpasswd_pair: "{{ htpasswd.stdout }}"


- name: Create/update traefik/basic_auth credentials
  ansible.builtin.uri:
    url: "https://{{ vault_dns }}:8200/v1/secret/data/traefik/basic_auth"
    method: POST
    headers:
      X-Vault-Token: "{{ token_data | community.hashi_vault.vault_login_token }}"
    body:
      data:
        htpasswd-pair: "{{ traefik_auth_htpasswd_pair }}"
    body_format: json
EOL

cat <<'EOL' > create_minio_bearer_token.yml
---
# Minio prometheus bearer token was created and stored in filesystem
- name: Load prometheus bearer token from file in vault node
  command: "jq -r '.bearerToken' /etc/minio/prometheus_bearer.json"
  register: root_token
  become: true
  changed_when: false
  when: minio_prom_bearer_token is not defined
  delegate_to: s3

- name: Get bearer token
  set_fact:
    minio_prom_bearer_token: "{{ root_token.stdout }}"

- name: Create/update minio/prometheus credentials
  ansible.builtin.uri:
    url: "https://{{ vault_dns }}:8200/v1/secret/data/minio/prometheus"
    method: POST
    headers:
      X-Vault-Token: "{{ token_data | community.hashi_vault.vault_login_token }}"
    body:
      data:
        bearer-token: "{{ minio_prom_bearer_token }}"
    body_format: json
EOL

cat <<'EOL' > generate_ca_signed_cert.yml
---
- name: Create private key
  openssl_privatekey:
    path: "{{ selfsigned_certificates_path }}/{{ server_hostname }}.key"
    size: "{{ ssl_key_size | int }}"
    type: "{{ key_type }}"
    mode: 0644

- name: Create CSR
  openssl_csr:
    path: "{{ selfsigned_certificates_path }}/{{ server_hostname }}.csr"
    privatekey_path: "{{ selfsigned_certificates_path }}/{{ server_hostname }}.key"
    country_name: "{{ country_name }}"
    organization_name: "{{ organization_name }}"
    email_address: "{{ email_address }}"
    common_name: "{{ server_hostname }}"
    subject_alt_name: "DNS:{{ server_hostname }},IP:{{ ansible_default_ipv4.address }}"

- name: CA signed CSR
  openssl_certificate:
    csr_path: "{{ selfsigned_certificates_path }}/{{ server_hostname }}.csr"
    path: "{{ selfsigned_certificates_path }}/{{ server_hostname }}.pem"
    provider: ownca
    ownca_path: "{{ selfsigned_certificates_path }}/CA.pem"
    ownca_privatekey_path: "{{ selfsigned_certificates_path }}/CA.key"
EOL

cat <<'EOL' > generate_custom_ca.yml
---
- name: Create CA key
  openssl_privatekey:
    path: "{{ selfsigned_certificates_path }}/CA.key"
    size: "{{ ssl_key_size | int }}"
    mode: 0644
  register: ca_key

- name: create the CA CSR
  openssl_csr:
    privatekey_path: "{{ selfsigned_certificates_path }}/CA.key"
    common_name: Liebmann5 CA
    use_common_name_for_san: false  # since we do not specify SANs, don't use CN as a SAN
    basic_constraints:
      - 'CA:TRUE'
    basic_constraints_critical: true
    key_usage:
      - keyCertSign
    key_usage_critical: true
    path: "{{ selfsigned_certificates_path }}/CA.csr"
  register: ca_csr

- name: sign the CA CSR
  openssl_certificate:
    path: "{{ selfsigned_certificates_path }}/CA.pem"
    csr_path: "{{ selfsigned_certificates_path }}/CA.csr"
    privatekey_path: "{{ selfsigned_certificates_path }}/CA.key"
    provider: selfsigned
  register: ca_crt
EOL

cat <<'EOL' > generate_selfsigned_cert.yml
---
- name: Create private key
  openssl_privatekey:
    path: "certificates/{{ server_hostname }}.key"
    size: "{{ ssl_key_size | int }}"
    type: "{{ key_type }}"
    mode: 0644

- name: Create CSR
  openssl_csr:
    path: "certificates/{{ server_hostname }}.csr"
    privatekey_path: "certificates/{{ server_hostname }}.key"
    country_name: "{{ country_name }}"
    organization_name: "{{ organization_name }}"
    email_address: "{{ email_address }}"
    common_name: "{{ server_hostname }}"
    subject_alt_name: "DNS:{{ server_hostname }}"

- name: Self-signing CSR
  openssl_certificate:
    csr_path: "certificates/{{ server_hostname }}.csr"
    path: "certificates/{{ server_hostname }}.pem"
    privatekey_path: "certificates/{{ server_hostname }}.key"
    provider: "{{ ssl_certificate_provider }}"
EOL

cat <<'EOL' > install_cli_utils.yml
---
# Execute roles to install cli and utils
- name: Use role in loop
  ansible.builtin.include_role:
    name: '{{ role }}'
  loop_control:
    loop_var: role
  loop:
    - longhorn-util
    - velero-cli
    - linkerd-cli
EOL

cat <<'EOL' > load_vault_credentials.yml
---

# hashi_vault.vault_write module is not working
#
# - name: Create {{ secret_group.key }} credentials
#   community.hashi_vault.vault_write:
#     url: "https://{{ vault_dns }}:8200"
#     path: "secret/{{ secret_group.key }}/{{ secret.key }}"
#     data: "{{ secret.value }}"
#     auth_method: token
#     token: '{{ token_data | community.hashi_vault.vault_login_token }}'
#   loop: "{{ secret_group.value | dict2items }}"
#   loop_control:
#     loop_var: secret

# https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2#create-update-secret
- name: Create/update {{ secret_group.key }} credentials
  ansible.builtin.uri:
    url: "https://{{ vault_dns }}:8200/v1/secret/data/{{ secret_group.key }}/{{ secret.key }}"
    method: POST
    headers:
      X-Vault-Token: "{{ token_data | community.hashi_vault.vault_login_token }}"
    body:
      data: "{{ secret.value }}"
    body_format: json
  loop: "{{ secret_group.value | dict2items }}"
  loop_control:
    loop_var: secret
  no_log: true
EOL

cat <<'EOL' > patch_grafana_dashboard.yml
---

# Patch Dashboard json if needed.
# Check if json file contains DS_PROMETHEUS variable defined and patch json file
# See issue #18

- name: Patching dashboard {{ dashboard_name }} | Initialize loop variables
  set_fact:
    dashboard_name: "{{ dashboard_file | basename | splitext | first }}"
    dashboard_file_name: "{{ dashboard_file | basename }}"
    dashboard_content: "{{ lookup('file', dashboard_file) | from_json }}"
    input_detected: false
    input_variable: false

- name: Patching dashboard {{ dashboard_name }} | Check if __inputs key exits within json dashboard
  set_fact:
    input_detected: true
  when: dashboard_content.__inputs is defined

- name: Patching dashboard {{ dashboard_name }} | Detect if variable DS_PROMETHEUS exits
  set_fact:
    input_variable: "{{ dashboard_content.__inputs | selectattr('name','==', 'DS_PROMETHEUS') | length > 0 }}"
  when: input_detected

- name: Patching dashboard {{ dashboard_name }} | Generating patch templating.list code block to add DS_PROMETHEUS variable
  set_fact:
    patch: "{{   [{ 'hide': 0,
                   'label': 'datasource',
                   'name': 'DS_PROMETHEUS',
                   'options': [],
                   'query': 'prometheus',
                   'refresh': 1,
                   'regex': '',
                   'type': 'datasource' }] + dashboard_content.templating.list }}"
  when: input_variable

- name: Patching dashboard {{ dashboard_name }} | Patch json dashboard file
  set_fact:
    dashboard_content: "{{ dashboard_content | combine(new_item, recursive=true) }}"
  vars:
    new_item: "{{ { 'templating': { 'list':  patch } } }}"
  when: input_variable

- name: "Patching dashboard {{ dashboard_name }} | Copying to patching directory"
  copy:
    dest: "temp/{{ dashboard_file_name }}"
    content: "{{ dashboard_content | to_nice_json(indent=2) }}"
  when: input_variable
EOL

cat <<'EOL' > vault_kubernetes_auth_method_config.yml
---

- name: Vault login
  ansible.builtin.shell: bash -ilc 'vault login -format=json $VAULT_TOKEN'
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
  changed_when: false
  delegate_to: gateway

- name: Get vault token
  set_fact:
    vault_token: "{{ vault_login.stdout | from_json | community.hashi_vault.vault_login_token }}"

- name: Get status of kubernetes auth method
  ansible.builtin.uri:
    url: "https://{{ vault_dns }}:8200/v1/sys/auth"
    method: GET
    headers:
      X-Vault-Token: "{{ vault_token }}"
  failed_when:
    - false
  register: vault_status_kubernetes_auth_method

  # Enable kubernetes auth method
  # vault auth enable kubernetes
- name: Enable kubernetes auth method
  ansible.builtin.uri:
    url: "https://{{ vault_dns }}:8200/v1/sys/auth/kubernetes"
    method: POST
    headers:
      X-Vault-Token: "{{ vault_token }}"
    body:
      type: "kubernetes"
      description: "kubernetes auth"
    body_format: json
    status_code:
      - 200
      - 204
  when:
    - "'kubernetes/' not in vault_status_kubernetes_auth_method.json.data"

- name: Configure kubernetes auth method
  ansible.builtin.uri:
    url: "https://{{ vault_dns }}:8200/v1/auth/kubernetes/config"
    method: POST
    headers:
      X-Vault-Token: "{{ vault_token }}"
    body:
      kubernetes_host: "{{ kubernetes_host }}"
      kubernetes_ca_cert: "{{ kubernetes_ca_cert }}"
      token_reviewer_jwt: "{{ vault_reviewer_token }}"
    body_format: json
    status_code:
      - 200
      - 204

- name: Create External Secrets role
  ansible.builtin.uri:
    url: "https://{{ vault_dns }}:8200/v1/auth/kubernetes/role/external-secrets"
    method: POST
    headers:
      X-Vault-Token: "{{ vault_token }}"
    body:
      bound_service_account_names: external-secrets
      bound_service_account_namespaces: external-secrets
      policies: ["read"]
    body_format: json
    status_code:
      - 200
      - 204
EOL

#cd ..

chmod +x cleaning.yml
chmod +x configure_vault_integration.yml
chmod +x create_basic_auth_credentials.yml
chmod +x create_minio_bearer_token.yml
chmod +x generate_ca_signed_cert.yml
chmod +x generate_custom_ca.yml
chmod +x generate_selfsigned_cert.yml
chmod +x install_cli_utils.yml
chmod +x load_vault_credentials.yml
chmod +x patch_grafana_dashboard.yml
chmod +x vault_kubernetes_auth_method_config.yml