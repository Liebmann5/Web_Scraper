#!/bin/bash

# Create the pxe-server directory
mkdir -p pxe-server

cd pxe-server

# Create the subdirectories
mkdir -p defaults handlers tasks templates

cd defaults

cat <<'EOL' > main.yml
---
# ISO file
ubuntu_live_server_iso_file: jammy-live-server-amd64.iso

# Kick-start server (http server)
apache_package_list:
  - apache2
kick_start_server: 10.0.0.1
ks_http_conf: ks-server.conf
EOL

cd ..

cd handlers

cat <<'EOL' > main.yml
---
- name: restart-apache
  service:
    name: apache2
    state: restarted
EOL

cd ..

cd tasks

cat <<'EOL' > create_auto_install_files.yml
---

- name: Create autoinstall per device
  debug:
    var: x86_host

- name: Print mac address for {{ x86_host }}
  debug:
    var: hostvars[x86_host].mac
  when: hostvars[x86_host].mac is defined

- name: Create Autoinstall directory for {{ x86_host }}
  file:
    path: "/var/www/html/ks/{{ hostvars[x86_host].mac }}"
    state: directory
    owner: www-data
    group: www-data
    mode: '0755'
  when: hostvars[x86_host].mac is defined

- name: Create meta-data file for {{ x86_host }}
  template:
    src: "templates/cloud-init-metadata.yml.j2"
    dest: "/var/www/html/ks/{{ hostvars[x86_host].mac }}/meta-data"
    owner: www-data
    group: www-data
    mode: '0644'
  when: hostvars[x86_host].mac is defined

- name: Create user-data file for {{ x86_host }}
  template:
    src: "templates/cloud-init-autoinstall.yml.j2"
    dest: "/var/www/html/ks/{{ hostvars[x86_host].mac }}/user-data"
    owner: www-data
    group: www-data
    mode: '0644'
  when: hostvars[x86_host].mac is defined
EOL

cat <<'EOL' > create_pxe_config_files.yml
---

- name: Create pxelinux conf per device
  debug:
    var: x86_host

- name: Print mac address for {{ x86_host }}
  debug:
    var: hostvars[x86_host].mac
  when: hostvars[x86_host].mac is defined

- name: Create pxeconfig file for {{ x86_host }}
  template:
    src: "templates/pxelinux.conf.j2"
    dest: "/srv/tftp/pxelinux.cfg/01-{{ hostvars[x86_host].mac | replace(':', '-') }}"
    owner: root
    group: root
    mode: '0644'
  when: hostvars[x86_host].mac is defined
EOL

cat <<'EOL' > install_ks_http_server.yml
---

- name: Ensure apache2 package is installed
  package:
    name: '{{ apache_package_list | list }}'
    state: 'present'
    update_cache: true
  register: pkg_install_result
  until: pkg_install_result is success

- name: Create kickstart document structure
  file:
    path: "/var/www/html/{{ item }}"
    state: directory
    owner: www-data
    group: www-data
    mode: '0755'
  with_items:
    - ks
    - images

- name: Set up kick-start virtualHost
  template:
    src: "templates/ks-server.conf.j2"
    dest: "/etc/apache2/sites-available/{{ ks_http_conf }}"

- name: Enable site
  command: a2ensite {{ ks_http_conf }}
  notify: restart-apache


- name: Create autoinstall cloud-inits files per device
  include_tasks:
    file: create_auto_install_files.yml
  loop: "{{ groups['x86'] }}"
  loop_control:
    loop_var: x86_host
  when:
    - groups['x86'] is defined

- name: Copy ISO img
  copy:
    src: ../metal/x86/pxe-files/img/
    dest: /var/www/html/images/
EOL

cat <<'EOL' > main.yml
---
# Install Apache server
- name: Install Kick-start HTTP server
  include_tasks: install_ks_http_server.yml

# Prepare TFTP server
- name: Prepare TFTP server
  include_tasks: prepare_tftp_server.yml
EOL

cat <<'EOL' > prepare_tftp_server.yml
---

- name: Create grub direcorty
  file:
    path: "/srv/tftp/{{ item }}"
    state: directory
    owner: root
    group: root
    mode: 0755
  with_items:
    - grub
    - pxelinux.cfg

- name: Copy grub config file
  template:
    src: "templates/grub.conf.j2"
    dest: "/srv/tftp/grub/grub.cfg"

- name: Copy boot files
  copy:
    src: "../metal/x86/pxe-files/boot/"
    dest: "/srv/tftp/"

- name: Create autoinstall pxe config file per device
  include_tasks:
    file: create_pxe_config_files.yml
  loop: "{{ groups['x86'] }}"
  loop_control:
    loop_var: x86_host
  when:
    - groups['x86'] is defined
EOL

cd ..

cd templates

cat <<'EOL' > cloud-init-autoinstall.yml.j2
#cloud-config
autoinstall:
  version: 1
  keyboard:
    layout: us
  ssh:
    allow-pw: false
    install-server: true
  storage:
    config: {{ hostvars[x86_host].autoinstall.storage.config }}


  user-data:
    # Set TimeZone and Locale
    timezone: America/Chicago
    locale: en_US.UTF-8

    # Hostname
    hostname: {{ x86_host }}

    # cloud-init not managing hosts file. only hostname is added
    manage_etc_hosts: localhost

    users:
      - name: Liebmann5
        primary_group: users
        groups: [adm, admin]
        shell: /bin/bash
        sudo: ALL=(ALL) NOPASSWD:ALL
        lock_passwd: true
        ssh_authorized_keys:
          - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCYKp1OpOMMrjxqHwCMWuNvtLj2XIJsii6RGhLldMFfayOscvpXCb3h13gIjKFhuAX3kXTHNxqQw8jVrnIAfIz6afmN9jHpSGLkdzcPeOZHOQbXBEFnK/+mPtIoJ4HbDUWDUBWP8xGMCv2bvuqP9bx5hD4N9xOZ2mCsFudS1v68NLdbpNVGD4cK6U/JqCONXFoRPewfy+kpUFHc3WCUea+HAG9E7jVtqfG8qAgPW6voP0WCarvgpd2AmxOb0dMKlCVTf4TGn6sINIKTWCghx2jKH2kWDuNHspJRWSBRylLwhJbwdyNs0ZgCRS+TgCkOCN1sDoxD3hbEYXtvKlezKZAt ayak@akia
          - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDUYmlMgPLkeVWS2ZnjO3V7LVhvSwW8iwPSDjY/bnnbr5lcD9eGf5/Reev384xuWLcbnR2MmYw8olvfPojCLTcG2uo/dY/M92aagGvyXnNcJMsEeQUDKofTiI0xihAVhrwN5ploc6A7nVAg2dybsLymLp8iviw9cbA80aTHF82NfDSZCLW8kMdE8gh+dIr88vBe6wRTJ+kKQGVdeCOFYIA4chn6W7JDGF1YsntJkNE1Y1l4w5fCur4MVPcOFjY3v9TZQhVEY5khTDafzX1xtTPE7Ffa4QmB/1jtXq9TyXcS2+LcC2zD4N39EYYv417NFrfv/2vwOk2cyy7p/XRp83NB ansible@grandWizard
EOL

cat <<'EOL' > cloud-init-metadata.yml.j2
instance-id: {{ x86_host }}
EOL

cat <<'EOL' > grub.conf.j2
set default="0"
set timeout=5

if loadfont unicode ; then
  set gfxmode=auto
  set locale_dir=$prefix/locale
  set lang=en_US
fi
terminal_output gfxterm

set menu_color_normal=white/black
set menu_color_highlight=black/light-gray
if background_color 44,0,30; then
  clear
fi

function gfxmode {
        set gfxpayload="${1}"
        if [ "${1}" = "keep" ]; then
                set vt_handoff=vt.handoff=7
        else
                set vt_handoff=
        fi
}

set linux_gfx_mode=keep

export linux_gfx_mode

menuentry 'Install Ubuntu 22.04' {
        gfxmode $linux_gfx_mode
        linux vmlinuz ip=dhcp url=http://{{ kick_start_server }}/images/{{ ubuntu_live_server_iso_file }} autoinstall ds=nocloud-net\;s=http://{{ kick_start_server }}/ks/${net_default_mac}/ cloud-config-url=/dev/null
        initrd initrd
}
EOL

cat <<'EOL' > ks-server.conf.j2
<VirtualHost *:80>
    ServerAdmin root@server1.example.com
    DocumentRoot /var/www/html
    ServerName server.example.com
    ErrorLog ${APACHE_LOG_DIR}/ks-server.example.com-error_log
    CustomLog ${APACHE_LOG_DIR}/ks-server.example.com-access_log common
    <Directory /ks>
        Options Indexes MultiViews
        AllowOverride All
        Require all granted
    </Directory>
    <Directory /images>
        Options Indexes MultiViews
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOL

cat <<'EOL' > pxelinux.conf.j2
default menu.c32
menu title Ubuntu installer

label jammy
        menu label Install Ubuntu J^ammy (22.04)
        menu default
        kernel vmlinuz
        initrd initrd
        append ip=dhcp url=http://{{ kick_start_server }}/images/{{ ubuntu_live_server_iso_file }} autoinstall ds=nocloud-net;s=http://{{ kick_start_server }}/ks/{{ hostvars[x86_host].mac }}/ cloud-config-url=/dev/null
prompt 0
timeout 300
EOL

cd ..

chmod +x defaults/main.yml
chmod +x handlers/main.yml
chmod +x tasks/create_auto_install_files.yml
chmod +x tasks/create_pxe_config_files.yml
chmod +x tasks/install_ks_http_server.yml
chmod +x tasks/main.yml
chmod +x tasks/prepare_tftp_server.yml
chmod +x templates/cloud-init-autoinstall.yml.j2
chmod +x templates/cloud-init-metadata.yml.j2
chmod +x templates/grub.conf.j2
chmod +x templates/ks-server.conf.j2
chmod +x templates/pxelinux.conf.j2