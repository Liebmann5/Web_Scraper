#!/bin/bash

# Create the certbot directory
mkdir -p certbot

cd certbot

# Create the subdirectories
mkdir -p defaults tasks templates tests

cd defaults

cat <<'EOL' > main.yml
---

# Install python3 pip and virtualenv packages
install_python_packages: true

# Set certbot python virtual environment
certbot_venv: /letsencrypt

# dns ionos credentials
dns_ionos_prefix: ionos-prefix
dns_ionos_secret: ionos-secret
dns_ionos_api_endpoint: https://api.hosting.ionos.com

certbot_email: Liebmann.nicholas1@gmail.com

# dns propagation in seconds
propagation_seconds: 300
EOL

cd ..

cd tasks

cat <<'EOL' > main.yml
---

- name: Ensure python virtualenv is installed.
  package:
    name:
      - python3-pip
      - python3-venv
    state: present
  become: true
  when: install_python_packages

- name: Install certbot and ionos plugin in venvironment
  pip:
    name:
      - certbot
      - certbot-dns-ionos
    virtualenv: "{{ certbot_venv }}"
    virtualenv_command: "python3 -m venv"
    state: present

- name: Create working directories
  file:
    path: "{{ item }}"
    state: directory
    mode: 0750
  with_items:
    - "{{ certbot_venv }}/logs"
    - "{{ certbot_venv }}/config"

- name: Create secret directory
  file:
    path: "{{ item }}"
    state: directory
    mode: 0700
  with_items:
    - "{{ certbot_venv }}/.secrets"

- name: Copy ionos secret file
  template:
    src: "{{ item.template }}"
    dest: "{{ item.dest }}"
    mode: 0600
  with_items:
    - template: ionos-credentials.ini.j2
      dest: "{{ certbot_venv }}/.secrets/ionos-credentials.ini"

- name: Copy certbot wrapper script
  template:
    src: "{{ item.template }}"
    dest: "{{ item.dest }}"
    mode: 0755
  with_items:
    - template: certbot.sh.j2
      dest: "{{ certbot_venv }}/bin/certbot-create-cert.sh"
    - template: certbot-wrapper.sh.j2
      dest: "{{ certbot_venv }}/bin/certbot-wrapper.sh"
EOL

cd ..

cd templates

cat <<'EOL' > certbot-wrapper.sh.j2
#!/bin/bash

# certbot-wrapper script
# Need to be copied to venv_cerbot/bin

BASEDIR=$(dirname "$0")

$BASEDIR/certbot  \
  --config-dir $BASEDIR/../config \
  --work-dir $BASEDIR/.. \
  --logs-dir $BASEDIR/../logs \
  $@
EOL

cat <<'EOL' > certbot.sh.j2
#!/bin/bash

# Executing certbot within virtualenv
# Need to be copied to venv_cerbot/bin

BASEDIR=$(dirname "$0")

$BASEDIR/certbot certonly \
  --config-dir $BASEDIR/../config \
  --work-dir $BASEDIR/.. \
  --logs-dir $BASEDIR/../logs \
  --authenticator dns-ionos \
  --dns-ionos-credentials $BASEDIR/../.secrets/ionos-credentials.ini \
  --dns-ionos-propagation-seconds {{ propagation_seconds }} \
  --server https://acme-v02.api.letsencrypt.org/directory \
  --agree-tos \
  --non-interactive \
  --rsa-key-size 4096 \
  -m {{ certbot_email }} \
  -d $1
EOL

cat <<'EOL' > ionos-credentials.ini.j2
dns_ionos_prefix = {{ dns_ionos_prefix }}
dns_ionos_secret = {{ dns_ionos_secret }}
dns_ionos_endpoint = {{ dns_ionos_api_endpoint }}
EOL

cd ..

cd tests

cat <<'EOL' > install_certbot.yml
---

- name: Install certbot
  hosts: localhost
  gather_facts: true
  roles:
    - role: certbot
      vars:
        - certbot_venv: /home/liebmann/letsencrypt
EOL

cd ..

chmod +x defaults/main.yml
chmod +x tasks/main.yml
chmod +x templates/certbot-wrapper.sh.j2
chmod +x templates/certbot.sh.j2
chmod +x templates/ionos-credentials.ini.j2
chmod +x tests/install_certbot.yml