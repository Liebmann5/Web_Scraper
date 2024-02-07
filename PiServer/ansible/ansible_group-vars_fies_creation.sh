#!/bin/bash

# Create the group_vars directory
mkdir -p group_vars

cd group_vars

cat <<'EOL' > all.yml
---
# Group all variables.

# Remote user name
ansible_user: Liebmann5

# Ansible ssh private key
ansible_ssh_private_key_file: ~/.ssh/id_rsa

# Cluster Lab Architecture
# Whether to use centralized SAN architecture or not
centralized_san: false

#######################
# DNS configuration
#######################
# DNS server
dns_server: 10.0.0.1
dns_domain: picluster.liebmann5.com

############################
# restic backup role variables
############################
# Deactivate clean service. Only enabled in one node
restic_clean_service: false
restic_backups_dirs:
  - path: '/etc'
  - path: '/root'
    exclude:
      - pattern: '.cache'
  - path: '/home/{{ ansible_user }}'
    exclude:
      - pattern: '.cache'
      - pattern: '.ansible'
EOL

cat <<'EOL' > control.yml
---
##########################
# fluentbit configuration
##########################

# Fluentbit_inputs
fluentbit_inputs: |
  [INPUT]
      Name tail
      Tag host.*
      DB /run/fluentbit-state.db
      Path /var/log/auth.log,/var/log/syslog
      Parser syslog-rfc3164-nopri
  [INPUT]
      name node_exporter_metrics
      tag node_metrics
      scrape_interval 30
# Fluentbit_filters
fluentbit_filters: |
  [FILTER]
      Name lua
      Match host.*
      script /etc/fluent-bit/adjust_ts.lua
      call local_timestamp_to_UTC
# Fluentbit Elasticsearch output
fluentbit_outputs: |
  [OUTPUT]
      Name forward
      Match *
      Host {{ fluentd_dns }}
      Port 24224
      Self_Hostname {{ ansible_hostname }}
      Shared_Key {{ fluentd_shared_key }}
      tls true
      tls.verify false
  [OUTPUT]
      name prometheus_exporter
      match node_metrics
      host 0.0.0.0
      port 9100
# Fluentbit custom parsers
fluentbit_custom_parsers: |
  [PARSER]
      Name syslog-rfc3164-nopri
      Format regex
      Regex /^(?<time>[^ ]* {1,2}[^ ]* [^ ]*) (?<host>[^ ]*) (?<ident>[a-zA-Z0-9_\/\.\-]*)(?:\[(?<pid>[0-9]+)\])?(?:[^\:]*\:)? *(?<message>.*)$/
      Time_Key time
      Time_Format %b %d %H:%M:%S
      Time_Keep False
EOL

cat <<'EOL' > external.yml
---
# Remote user name
ansible_user: ubuntu
EOL

cat <<'EOL' > k3s_cluster.yml
---
# k3s_cluster group variables

####################
# ntp role variables
####################

ntp_servers:
  - server: 10.0.0.1
    type: server
EOL

cat <<'EOL' > k3s_master.yml
---
# k3s_master group variables


##################################
# liebmann5.k8s_cli role variables
##################################

install_helm: true
helm_version: 'v3.9.4'
install_kubectl: false

# OS and hardware architectire
k8s_platform: linux
k8s_arch: arm64
EOL

cd ..

chmod +x all.yml
chmod +x control.yml
chmod +x external.yml
chmod +x k3s_cluster.yml
chmod +x k3s_master.yml