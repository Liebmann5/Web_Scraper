#!/bin/bash

# Create the subdirectories
#mkdir -p centralized_san

cat <<'EOL' > picluster.yml
---
# Pi Cluster variables

#######
# K3S #
#######

# k3s version
k3s_version: v1.28.2+k3s1

# k3s master node VIP (loadbalancer)
k3s_api_vip: 10.0.0.1

# k3s shared token
k3s_token: "{{ vault.cluster.k3s.token }}"

# k3s config directory
k3s_config_directory: /etc/rancher/k3s

# kubelet configuration
k3s_kubelet_config: |
  apiVersion: kubelet.config.k8s.io/v1beta1
  kind: KubeletConfiguration
  shutdownGracePeriod: 30s
  shutdownGracePeriodCriticalPods: 10s


# k3s server-config
# Equivalent to start master installer with the following options
# --write-kubeconfig-mode '0644'
# --disable 'servicelb'
# --disable 'traefik'
# --disable 'local-storage'
# --node-taint 'node-role.kubernetes.io/master=true:NoSchedule'
# --kube-controller-manager-arg 'bind-address=0.0.0.0'
# --kube-proxy-arg 'metrics-bind-address=0.0.0.0'
# --kube-scheduler-arg 'bind-address=0.0.0.0'
# --kubelet-arg 'config=/etc/rancher/k3s/kubelet.config'
# --kube-controller-manager-arg 'terminated-pod-gc-threshold=10'

k3s_server_config:
  tls-san:
    - "{{ k3s_api_vip }}"  # IP to HAProxy
  disable:
    - local-storage
    - servicelb
    - traefik
  write-kubeconfig-mode: 644
  node-taint:
    - 'node-role.kubernetes.io/master=true:NoSchedule'
  etcd-expose-metrics: true
  kubelet-arg:
    - 'config=/etc/rancher/k3s/kubelet.config'
  kube-proxy-arg:
    - 'metrics-bind-address=0.0.0.0'
  kube-controller-manager-arg:
    - 'bind-address=0.0.0.0'
    - 'terminated-pod-gc-threshold=10'
  kube-scheduler-arg:
    - 'bind-address=0.0.0.0'

# k3s agent-config
# Equivalent to start agent installer with the following options
#  --node-label 'node_type=worker'
#  --kubelet-arg 'config=/etc/rancher/k3s/kubelet.config'
#  --kube-proxy-arg 'metrics-bind-address=0.0.0.0'
k3s_agent_config:
  node-label:
    - 'node_type=worker'
  kubelet-arg:
    - 'config=/etc/rancher/k3s/kubelet.config'
  kube-proxy-arg:
    - 'metrics-bind-address=0.0.0.0'


###########
# Traefik #
###########

# HTTP Basic auth credentials
traefik_basic_auth_user: "{{ vault.traefik.admin.user }}"
traefik_basic_auth_passwd: "{{ vault.traefik.admin.password }}"

# DNS cluster service end-points
traefik_dashboard_dns: "traefik.{{ dns_domain }}"
longhorn_dashboard_dns: "storage.{{ dns_domain }}"
kibana_dashboard_dns: "kibana.{{ dns_domain }}"
elasticsearch_dns: "elasticsearch.{{ dns_domain }}"
fluentd_dns: "fluentd.{{ dns_domain }}"
monitoring_dns: "monitoring.{{ dns_domain }}"
linkerd_dashboard_dns: "linkerd.{{ dns_domain }}"

#################################
# TLS Certificates: LetsEncrypt #
#################################

# Enable letsencrypt certificates
enable_letsencrypt: true

# IONOS API credentials
ionos_public_prefix: "{{ vault.certmanager.ionos.public_prefix }}"
ionos_secret: "{{ vault.certmanager.ionos.secret }}"
ionos_api_endpoint: https://api.hosting.ionos.com


# issuer email
acme_issuer_email: admin@ricsanfre.com

##########################
# Minio S3 configuration #
##########################

# Minio S3 Server
minio_hostname: "s3.ricsanfre.com"
minio_endpoint: "{{ minio_hostname }}:9091"
minio_url: "https://{{ minio_hostname }}:9091"

# Minio data dirs
minio_server_make_datadirs: true
minio_server_datadirs:
  - /storage/minio

# Minio admin credentials
minio_root_user: "minioadmin"
minio_root_password: "{{ vault.minio.root.key }}"

# Minio site region configuration
minio_site_region: "eu-west-1"

# Enabling TLS
minio_enable_tls: true
minio_validate_certificate: false

# Create Prometheus bearer token
minio_prometheus_bearer_token: true

# Minio Buckets
minio_buckets:
  - name: restic
    policy: read-write
  - name: k3s-longhorn
    policy: read-write
  - name: k3s-velero
    policy: read-write
  - name: k3s-loki
    policy: read-write
  - name: k3s-tempo
    policy: read-write

# Minio users and ACLs
minio_users:
  - name: "{{ vault.minio.restic.user }}"
    password: "{{ vault.minio.restic.key }}"
    buckets_acl:
      - name: restic
        policy: read-write
  - name: "{{ vault.minio.longhorn.user }}"
    password: "{{ vault.minio.longhorn.key }}"
    buckets_acl:
      - name: k3s-longhorn
        policy: read-write
  - name: "{{ vault.minio.velero.user }}"
    password: "{{ vault.minio.velero.key }}"
    buckets_acl:
      - name: k3s-velero
        policy: custom
        custom:
          - rule: |
              "Effect": "Allow",
              "Action": [
                  "s3:GetObject",
                  "s3:DeleteObject",
                  "s3:PutObject",
                  "s3:AbortMultipartUpload",
                  "s3:ListMultipartUploadParts"
              ],
              "Resource": [
                  "arn:aws:s3:::k3s-velero/*"
              ]
          - rule: |
              "Effect": "Allow",
              "Action": [
                  "s3:ListBucket"
              ],
              "Resource": [
                  "arn:aws:s3:::k3s-velero"
              ]

  - name: "{{ vault.minio.loki.user }}"
    password: "{{ vault.minio.loki.key }}"
    buckets_acl:
      - name: k3s-loki
        policy: read-write

  - name: "{{ vault.minio.tempo.user }}"
    password: "{{ vault.minio.tempo.key }}"
    buckets_acl:
      - name: k3s-tempo
        policy: custom
        custom:
          - rule: |
              "Effect": "Allow",
              "Action": [
                  "s3:PutObject",
                  "s3:GetObject",
                  "s3:ListBucket",
                  "s3:DeleteObject",
                  "s3:GetObjectTagging",
                  "s3:PutObjectTagging"
              ],
              "Resource": [
                  "arn:aws:s3:::k3s-tempo/*",
                  "arn:aws:s3:::k3s-tempo"
              ]

########################
# Restic configuration #
########################

# Restic S3 repository configuration
restic_repository: "s3:{{ minio_url }}/restic"
restic_use_ca_cert: true
restic_environment:
  - name: AWS_ACCESS_KEY_ID
    value: "{{ vault.minio.restic.user }}"
  - name: AWS_SECRET_ACCESS_KEY
    value: "{{ vault.minio.restic.key }}"

#######################
# Vault configuration
#######################

vault_hostname: "vault.picluster.ricsanfre.com"
vault_dns: "{{ vault_hostname }}"
vault_enable_tls: true
custom_ca: false
vault_init: true
vault_unseal: true
vault_unseal_service: true
tls_skip_verify: false

# Configure KV
vault_kv_secrets:
  path: secret

# Policies
policies:
  - name: write
    hcl: |
      path "secret/*" {
        capabilities = [ "create", "read", "update", "delete", "list", "patch" ]
      }
  - name: read
    hcl: |
      path "secret/*" {
        capabilities = [ "read" ]
      }

###################
# Velero  Secrets #
###################

# Minio user, key and bucket
minio_velero_user: "{{ vault.minio.velero.user }}"
minio_velero_key: "{{ vault.minio.velero.key }}"

velero_secret_content: |
  [default]
  aws_access_key_id: "{{ minio_velero_user }}"
  aws_secret_access_key: "{{ minio_velero_key }}"

###################
# Longhorn Secrets#
###################

# Minio user, key and bucket
minio_longhorn_user: "{{ vault.minio.longhorn.user }}"
minio_longhorn_key: "{{ vault.minio.longhorn.key }}"

###################
# Logging Secrets #
###################

# Fluentd-fluentbit shared key
fluentd_shared_key: "{{ vault.logging.fluentd.shared_key }}"

# Elasticsearch 'elastic' user password
efk_elasticsearch_passwd: "{{ vault.logging.elasticsearch.password }}"

# Loki minio user, key and bucket
minio_loki_user: "{{ vault.minio.loki.user }}"
minio_loki_key: "{{ vault.minio.loki.key }}"

######################
# Monitoring Secrets #
######################

# Grafana admin user password
prometheus_grafana_password: "{{ vault.grafana.admin.password}}"


#######################
# Tracing Secrets     #
#######################

# Tempo minio user, key and bucket
minio_tempo_user: "{{ vault.minio.tempo.user }}"
minio_tempo_key: "{{ vault.minio.tempo.key }}"
minio_tempo_bucket: k3s-tempo
EOL

cat <<'EOL' > selfsigned-certificates.yml
---
# Self-signed certificate generation variables
ssl_key_size: 4096
ssl_certificate_provider: selfsigned
key_type: RSA
country_name: US
email_address: admin@liebmann5.com
organization_name: Nicks Private Parts
EOL

cat <<'EOL' > vault.yml
---
# Encrypted variables - Ansible Vault
vault:
  # SAN
  san:
    iscsi:
      node_pass: s1cret0
      password_mutual: 0tr0s1cret0
  # K3s secrets
  cluster:
    k3s:
      token: s1cret0
  # traefik secrets
  traefik:
    basic_auth:
      user: admin
      passwd: s1cret0
  # Minio S3 secrets
  minio:
    root:
      user: root
      key: supers1cret0
    restic:
      user: restic
      key: supers1cret0
    longhorn:
      user: longhorn
      key: supers1cret0
    velero:
      user: velero
      key: supers1cret0
    loki:
      user: loki
      key: supers1cret0
    tempo:
      user: tempo
      key: supers1cret0
  # elastic search
  elasticsearch:
    es-admin:
      user: admin
      password: s1cret0
    es-fluentd:
      user: fluentd
      password: s1cret0
    es-prometheus:
      user: prometheus
      password: s1cret0
  # Fluentd
  fluentd:
    shared_key: s1cret0
  # Grafana
  grafana:
    admin:
      user: admin
      password: s1cret0

  # Certmanager
  certmanager:
    ionos:
      public_prefix: your-public-prefix **************************************
      secret: your-key *******************************************************
EOL

cat <<'EOL' > vault.yml.j2
---
# Encrypted variables - Ansible Vault
vault:
  # SAN
  san:
    iscsi:
      node_pass: {{ san_iscsi_node_pass | default("") }}
      password_mutual: {{ san_iscsi_mutual_pass | default("") }}
  # K3s secrets
  cluster:
    k3s:
     token: {{ k3s_token }}
  # Traefik secrets
  traefik:
    admin:
      user: admin
      password: {{ traefik_basic_auth_password }}
  # Minio S3 secrets
  minio:
    root:
      user: root
      key: {{ minio_root_password }}
    restic:
      user: restic
      key: {{ minio_restic_password }}
    longhorn:
      user: longhorn
      key: {{ minio_longhorn_password }}
    velero:
      user: velero
      key: {{ minio_velero_password }}
    loki:
      user: loki
      key: {{ minio_loki_password }}
    tempo:
      user: tempo
      key: {{ minio_tempo_password }}
  # elasticsearch and fluentd
  logging:
    es-admin:
      user: admin
      password: {{ elasticsearch_admin_password }}
    es-fluentd:
      user: fluentd
      password: {{ elasticsearch_fluentd_password }}
    es-prometheus:
      user: prometheus
      password: {{ elasticsearch_prometheus_password }}
    fluentd:
      shared_key: {{ fluentd_shared_key }}
  # Grafana
  grafana:
    admin:
     user: admin
     password: {{ grafana_admin_password }}
  # Certmanager
  certmanager:
    ionos:
      public_prefix: {{ ionos_public_prefix }}
      secret: {{ ionos_secret }}
EOL

cat <<'EOL' > network

EOL

cd centralized_san

cat <<'EOL' > centralized_san_initiator.yml
---
# ------------------------------------------
# CENTRALIZED SAN (ALTERNATIVE ARCHITECTURE)
# ------------------------------------------
# Variables for configuring iSCSI in clusters nodes
# iSCSI Initiator Configuration + Mouting iSCSI LUNs

################################
# iSCSI-initiator role variables
################################

open_iscsi_automatic_startup: true
open_iscsi_targets:
  - name: bigHouse-target
    discover: true
    auto_portal_startup: true
    auto_node_startup: true
    portal: 10.0.0.1
    target: iqn.2021-07.com.liebmann5:bigHouse
    login: true
    node_auth: CHAP
    node_user: "{{ open_iscsi_initiator_name }}"
    node_pass: "{{ vault.san.iscsi.node_pass }}"
    node_user_in: iqn.2021-07.com.liebmann5:bigHouse
    node_pass_in: "{{ vault.san.iscsi.password_mutual }}"

#############################################
# Storage role variables. Mount iSCSI volumes
#############################################

storage_volumegroups:
  - name: vg_iscsi
    devices:
      - /dev/sdb
storage_volumes:
  - name: vg_iscsi_lv_node
    vg: vg_iscsi
    size: 100%VG
storage_filesystems:
  - name: /dev/vg_iscsi/vg_iscsi_lv_node
    filesystem: ext4
storage_mounts:
  - name: /storage
    src: /dev/vg_iscsi/vg_iscsi_lv_node
    owner: root
    group: root
    mode: "0755"
    opts: _netdev
    boot: true
    dump: 0
    passno: 2
EOL

cat <<'EOL' > centralized_san_target.yml

EOL

cd..

chmod +x picluster.yml
chmod +x selfsigned-certificates.yml
chmod +x vault.yml
chmod +x vault.yml.j2
chmod +x centralized_san/centralized_san_initiator.yml
chmod +x centralized_san/centralized_san_target.yml