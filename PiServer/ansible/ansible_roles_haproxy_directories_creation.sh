#!/bin/bash

# Create the haproxy directory
mkdir -p haproxy

cd haproxy

# Create the subdirectories
mkdir -p defaults handlers tasks templates

cd defaults

cat <<'EOL' > main.yml
---

haproxy_user: haproxy
haproxy_group: haproxy
EOL

cd ..

cd handlers

cat <<'EOL' > main.yml
---
# handlers file for haproxy
- name: restart haproxy
  systemd:
    state: 'restarted'
    name: 'haproxy'
EOL

cd ..

cd tasks

cat <<'EOL' > main.yml
---
- name: Ensure haproxy package is installed
  package:
    name: 'haproxy'
    state: 'present'
    update_cache: true

- name: Copy haproxy config
  template:
    src: haproxy.cfg.j2
    dest: /etc/haproxy/haproxy.cfg
    mode: 0644
    validate: haproxy -f %s -c -q
  notify: restart haproxy

- name: Ensure haproxy is running and enabled
  service:
    name: "haproxy"
    state: started
    enabled: true
EOL

cd ..

cd templates

cat <<'EOL' > haproxy.cfg.j2
global
  log /dev/log  local0
  log /dev/log  local1 notice
  chroot /var/lib/haproxy
  stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
  stats timeout 30s
  user {{ haproxy_user }}
  group {{ haproxy_group }}
  daemon

defaults
  log global
  mode http
  option httplog
  option dontlognull
  retries 3
  timeout http-request 10s
  timeout queue 20s
  timeout connect 10s
  timeout client 1h
  timeout server 1h
  timeout http-keep-alive 10s
  timeout check 10s
  errorfile 400 /etc/haproxy/errors/400.http
  errorfile 403 /etc/haproxy/errors/403.http
  errorfile 408 /etc/haproxy/errors/408.http
  errorfile 500 /etc/haproxy/errors/500.http
  errorfile 502 /etc/haproxy/errors/502.http
  errorfile 503 /etc/haproxy/errors/503.http
  errorfile 504 /etc/haproxy/errors/504.http


#---------------------------------------------------------------------
# apiserver frontend which proxys to the control plane nodes
#---------------------------------------------------------------------
frontend k8s_apiserver
    bind *:6443
    mode tcp
    option tcplog
    default_backend k8s_controlplane

#---------------------------------------------------------------------
# round robin balancing for apiserver
#---------------------------------------------------------------------
backend k8s_controlplane
    option httpchk GET /healthz
    http-check expect status 200
    mode tcp
    option ssl-hello-chk
    balance     roundrobin
{% for host in groups['k3s_master'] %}
{% if hostvars[host].hostname is defined and hostvars[host].ip is defined %}
      server {{ hostvars[host].hostname }} {{ hostvars[host].ip }}:6443 check
{% endif %}
{% endfor %}
EOL

cd ..

chmod +x defaults/main.yml
chmod +x handlers/main.yml
chmod +x tasks/main.yml
chmod +x templates/haproxy.cfg.j2