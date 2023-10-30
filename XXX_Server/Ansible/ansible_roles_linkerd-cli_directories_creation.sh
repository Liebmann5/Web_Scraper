#!/bin/bash

# Create the linkerd-cli directory
mkdir -p linkerd-cli

cd linkerd-cli

# Create the linkerd-cli's subdirectories
mkdir -p defaults tasks

cd defaults

cat <<'EOL' > main.yml
---
# Version
linkerd_version: "stable-2.13.5"

# Architecture
linkerd_arch: "arm64"

# Package download url and checksum
linkerd_package_name: "linkerd2-cli-{{ linkerd_version }}-linux-{{ linkerd_arch }}"
linkerd_package_url: "https://github.com/linkerd/linkerd2/releases/download/{{ linkerd_version }}/{{ linkerd_package_name }}"
linkerd_checksum: "sha256:{{ linkerd_package_url }}.sha256"

# linkerd install location
linkerd_install_dir: "/usr/local/bin"
linkerd_bin: "{{ linkerd_install_dir }}/linkerd"
EOL

cd ..

cd tasks

cat <<'EOL' > install_linkerd_cli.yml
---

- name: Install linkerd cli
  get_url:
    url: "{{ linkerd_package_url }}"
    dest: "{{ linkerd_bin }}"
    owner: root
    group: root
    mode: '0755'
    # checksum: "{{ linkerd_checksum }}"
EOL

cat <<'EOL' > main.yml
---

- name: Check Linkerd CLI installation status
  stat:
    path: "{{ linkerd_bin }}"
  register: _linkerd_bin

- name: Install linkerd CLI
  include_tasks: install_linkerd_cli.yml
  args:
    apply:
      become: true
  when:
    - not _linkerd_bin.stat.exists
EOL

cd ..

chmod +x defaults/main.yml
chmod +x tasks/install_linkerd_cli.yml
chmod +x tasks/main.yml