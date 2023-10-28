#!/bin/bash

# Create the basic_setup directory
#mkdir -p basic_setup

# Navigate into the basic_setup directory
#cd basic_setup

# Create the subdirectories
mkdir -p defaults handlers scripts tasks



# Navigate into the defaults directory
cd defaults

# Create and populate the main.yaml file using a here document
cat <<EOL > main.yaml
---
basic_packages:
  - libraspberrypi-bin
  - linux-modules-extra-raspi
  - fake-hwclock
  - bridge-utils
EOL

# Navigate back to the original directory
cd ..

# Navigate into the handlers directory
cd handlers

# Create and populate the main.yml file using a here document
cat <<EOL > main.yml
---
- name: reboot
  reboot:

- name: restart multipath
  service:
    name: multipathd
    state: restarted
EOL

# Navigate back to the original directory
cd ..

# Navigate into the scripts directory
cd scripts

# By quoting EOL with single quotes, you're telling Bash not to perform any variable or command substitution within the here document. This way, the content between the EOL delimiters will be written to the file as-is.
cat <<'EOL' > pi_temp
#!/bin/bash
# Display the ARM CPU and GPU  temperature of Raspberry Pi 

cpu=$(</sys/class/thermal/thermal_zone0/temp)
echo "$(date) @ $(hostname)"
echo "-------------------------------------------"
echo "GPU => $(vcgencmd measure_temp)"
echo "CPU => $((cpu/1000))'C"
EOL

cat <<'EOL' > pi_throttling
#!/bin/bash
# Display the throttling status of Raspberry Pi

#Flag Bits
UNDERVOLTED=0x1
CAPPED=0x2
THROTTLED=0x4
SOFT_TEMPLIMIT=0x8
HAS_UNDERVOLTED=0x10000
HAS_CAPPED=0x20000
HAS_THROTTLED=0x40000
HAS_SOFT_TEMPLIMIT=0x80000


#Text Colors
GREEN=`tput setaf 2`
RED=`tput setaf 1`
NC=`tput sgr0`

#Output Strings
GOOD="${GREEN}NO${NC}"
BAD="${RED}YES${NC}"

#Get Status, extract hex
STATUS=$(vcgencmd get_throttled)
STATUS=${STATUS#*=}

echo -n "Status: "
(($STATUS!=0)) && echo "${RED}${STATUS}${NC}" || echo "${GREEN}${STATUS}${NC}"

echo "Undervolted:"
echo -n "   Now: "
((($STATUS&UNDERVOLTED)!=0)) && echo "${BAD}" || echo "${GOOD}"
echo -n "   Run: "
((($STATUS&HAS_UNDERVOLTED)!=0)) && echo "${BAD}" || echo "${GOOD}"

echo "Throttled:"
echo -n "   Now: "
((($STATUS&THROTTLED)!=0)) && echo "${BAD}" || echo "${GOOD}"
echo -n "   Run: "
((($STATUS&HAS_THROTTLED)!=0)) && echo "${BAD}" || echo "${GOOD}"

echo "Frequency Capped:"
echo -n "   Now: "
((($STATUS&CAPPED)!=0)) && echo "${BAD}" || echo "${GOOD}"
echo -n "   Run: "
((($STATUS&HAS_CAPPED)!=0)) && echo "${BAD}" || echo "${GOOD}"

echo "Softlimit:"
echo -n "   Now: "
((($STATUS&SOFT_TEMPLIMIT)!=0)) && echo "${BAD}" || echo "${GOOD}"
echo -n "   Run: "
((($STATUS&HAS_SOFT_TEMPLIMIT)!=0)) && echo "${BAD}" || echo "${GOOD}"
EOL

# Navigate back to the original directory
cd ..

# Navigate into the tasks directory
cd tasks

# Create the files directory
mkdir -p files

# Navigate into the files directory
cd files

# Create and populate the multipath.conf file using a here document
cat <<EOL > multipath.conf
defaults {
    user_friendly_names yes
}
blacklist {
    devnode "^sd[a-z0-9]+"
}
EOL

# Navigate back to the tasks directory
cd ..

# Create and populate the main.yaml file using a here document
cat <<EOL > main.yaml
---

# Get list of packages installed
- name: Get list of packages
  package_facts:
    manager: auto

- name: Check whether snap is package is installed
  debug:
    msg: "snapd found"
  when: "'snapd' in ansible_facts.packages"

- name: Remove snap package
  include_tasks: remove_snap.yaml
  when: "'snapd' in ansible_facts.packages"

- name: Execute RaspberryPi specific setup tasks
  include_tasks: raspberrypi_tasks.yml
  when: "'raspberrypi' in group_names"

- name: Blacklist storage devices in multipath configuration
  include_tasks: multipath_blacklist.yml
EOL

# Create and populate the multipath_blacklist.yml file using a here document
cat <<EOL > multipath_blacklist.yml
---
# This play is for blacklist devices in multiplath configurtion
# Avoid conflicts with Longhorn. See: https://longhorn.io/kb/troubleshooting-volume-with-multipath/
- name: Check that the multipath.conf exists
  stat:
    path: /etc/multipath.conf
  register: multipath_file_exist

- name: Copy blacklisted multipath.conf file
  copy:
    dest: /etc/multipath.conf
    src: files/multipath.conf
    owner: root
    group: root
    mode: 0644
    backup: true
  when: multipath_file_exist.stat.exists
  notify: restart multipath
EOL

# Create and populate the raspberrypi_tasks.yml file using a here document
cat <<EOL > raspberrypi_tasks.yml
---

- name: Install common packages
  apt:
    name: "{{ basic_packages }}"
    update_cache: true
    state: present

- name: Copy utility scripts
  copy:
    src: "scripts/{{ item }}"
    dest: "/usr/local/bin/{{ item }}"
    owner: "root"
    group: "root"
    mode: "u=rwx,g=rx,o=rx"
  with_items:
    - pi_temp
    - pi_throttling

- name: Set GPU memory split to 16 MB
  lineinfile:
    path: /boot/firmware/config.txt
    line: "gpu_mem=16"
    create: true
    mode: 0755
  notify: reboot
EOL

# Create and populate the remove_snap.yaml file using a here document
cat <<EOL > remove_snap.yaml
---
- name: Remove Snap Packages
  include_tasks: remove_snap_packages.yml

- name: Remove snapd package
  apt:
    name: snapd
    update_cache: true
    autoremove: true
    state: absent
EOL

# Create and populate the remove_snap_packages.yml file using a here document
cat <<EOL > remove_snap_packages.yml
---
- name: Remove list of snap packages. Retry several times. It might fail because of package dependecies
  block:
    - name: Increment the retry count
      set_fact:
        retry_count: "{{ 0 if retry_count is undefined else retry_count | int + 1 }}"
    - name: list snap packages
      shell: |
        for i in `snap list | awk '!/Name/{print $1}'`;
        do echo $i;
        done
      changed_when: false
      register: snap_packages
    - name: Remove snap packages
      command: snap remove {{ item }}
      register: snap_remove_output
      with_items: "{{ snap_packages.stdout_lines }}"
  rescue:
    - name: Check number of retries and fail if greater that 3
      fail:
        msg: Maximum retries of grouped tasks reached
      when: retry_count | int == 3
    - name: printing retry message
      debug:
        msg: "Removing snap package failed, let's give it another shot"
    - name: retrying deletion
      include_tasks: remove_snap_packages.yml
EOL


# Navigate back to the basic_setup directory
cd ..

# Give files executable ???
chmod +x defaults/main.yaml

chmod +x handlers/main.yml

chmod +x scripts/pi_temp
chmod +x scripts/pi_throttling

chmod +x tasks/files/multipath.conf
chmod +x tasks/main.yaml
chmod +x tasks/multipath_blacklist.conf
chmod +x tasks/raspberrypi_tasks.yml
chmod +x tasks/remove_snap.yaml
chmod +x tasks/remove_snap_packages.yml