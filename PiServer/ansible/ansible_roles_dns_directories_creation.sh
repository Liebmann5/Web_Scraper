#!/bin/bash

# Create the dns directory
mkdir -p dns

cd dns

# Create the subdirectories
mkdir -p handlers tasks

cd handlers

cat <<'EOL' > main.yml
---
- name: restart systemd-resolved
  service:
    name: systemd-resolved
    state: restarted
EOL

cd ..

cd tasks

cat <<'EOL' > main.yml
---
- name: Update DNS servers.
  lineinfile:
    dest: /etc/systemd/resolved.conf
    regexp: "{{ item.regexp }}"
    line: "{{ item.line }}"
    state: present
    mode: 0644
    backup: true
  with_items:
    - regexp: "^DNS="
      line: "DNS={{ dns_server }}"
    - regexp: "^Domains"
      line: "Domains={{ dns_domain }}"
  notify: restart systemd-resolved
EOL

cd ..

chmod +x handlers/main.yml
chmod +x tasks/main.yml