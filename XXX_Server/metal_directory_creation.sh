#!/bin/bash

# Create the subdirectories
#mkdir -p bigHouse nodes

cd bigHouse

mkdir -p network-config user-data

cat <<'EOL' > network-config

EOL

cat <<'EOL' > user-data

EOL

cd ..

cd nodes

mkdir -p user-data user-data-SSD-partition

cat <<'EOL' > user-data
#cloud-config

# Set TimeZone and Locale
timezone: America/Chicago
locale: en_US.UTF-8

# Hostname
hostname: nodeX

# cloud-init not managing hosts file. only hostname is added
manage_etc_hosts: localhost

users:
  # not using default ubuntu user
  - name: Liebmann5
    primary_group: users
    groups: [adm, admin]
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: true
    ssh_authorized_keys:
      - ssh-rsa *******************************************************************************
      - ssh-rsa *******************************************************************************
EOL

cat <<'EOL' > user-data-SSD-partition
#cloud-config

# Set TimeZone and Locale
timezone: America/Chicago
locale: en_US.UTF-8

# Hostname
hostname: nodeX

# cloud-init not managing hosts file. only hostname is added
manage_etc_hosts: localhost

users:
  # not using default ubuntu user
  - name: Liebmann5
    primary_group: users
    groups: [adm, admin]
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: true
    ssh_authorized_keys:
      - ssh-rsa *******************************************************************************
      - ssh-rsa *******************************************************************************

bootcmd:
  # Create second Linux partition. Leaving 30GB for root partition
  # sgdisk /dev/sda -g -e -n=0:30G:0 -t 0:8300
  # First convert MBR partition to GPT (-g option)
  # Second moves the GPT backup block to the end of the disk where it belongs (-e option)
  # Then creates a new partition starting 10GiB into the disk filling the rest of the disk (-n=0:10G:0 option)
  # And labels it as a Linux partition (-t option)
  - [cloud-init-per, once, addpartition, sgdisk, /dev/sda, "-g", "-e", "-n=0:30G:0", -t, "0:8300"]

runcmd:
  # reload partition table
  - "sudo partprobe /dev/sda"
  # configure new partition
  - "mkfs.ext4 /dev/sda3"
  - "e2label /dev/sda3 DATA"
  - "mkdir -p /storage"
  - "mount -t ext4 /dev/sda3 /storage"
  - "echo LABEL=DATA /storage ext4 defaults 0 0 | sudo tee -a /etc/fstab"
EOL

cd ../..

chmod +x bigHouse/network-config
chmod +x bigHouse/user-data

chmod +x workers/user-data
chmod +x workers/user-data-SSD-partition

cd ..

cd img

cat <<'EOL' > .gitignore
*
!.gitignore
EOL

#Double check this!?!?!?
chmod +x .gitignore

cd ..

cat <<'EOL' > Makefile
IMG=ubuntu-22.04.2-preinstalled-server-arm64+raspi.img.xz
URL_IMG=https://cdimage.ubuntu.com/releases/22.04/release/${IMG}
# REPLACE WITH YOUR USB (`lsblk`)
USB=/dev/sdb
SYSTEM_BOOT_MOUNT=/tmp/pi-disk
USER_DATA_NODES=user-data-SSD-partition

.EXPORT_ALL_VARIABLES:

img/${IMG}:
	wget ${URL_IMG} -O img/${IMG}

.PHONY: wipe-disk
wipe-disk:
	sudo wipefs -a -f ${USB}

.PHONY: burn-image
burn-image:
	# `-d` decompress `<` redirect $FILE contents to expand `|` sending the output to `dd` to copy directly to $USB
	xz -d < img/${IMG} - | sudo dd bs=100M of=${USB}

.PHONY: mount-system-boot
mount-system-boot:
	sudo mkdir ${SYSTEM_BOOT_MOUNT}

.PHONY: prepare-bigHouse
prepare-bigHouse:
	sudo mount ${USB}1 ${SYSTEM_BOOT_MOUNT} 
	sudo cp cloud-init/bigHouse/user-data ${SYSTEM_BOOT_MOUNT}
	sudo cp cloud-init/bigHouse/network-config ${SYSTEM_BOOT_MOUNT}
	sudo umount ${SYSTEM_BOOT_MOUNT}

.PHONY: prepare-worker1
prepare-worker1:
	sudo mount ${USB}1 ${SYSTEM_BOOT_MOUNT}
	sed 's/workerX/worker1/g' cloud-init/workers/${USER_DATA_NODES} | sudo tee ${SYSTEM_BOOT_MOUNT}/user-data
	sudo umount ${SYSTEM_BOOT_MOUNT}

.PHONY: prepare-worker2
prepare-worker2:
	sudo mount ${USB}1 ${SYSTEM_BOOT_MOUNT}
	sed 's/workerX/worker2/g' cloud-init/workers/${USER_DATA_NODES} | sudo tee ${SYSTEM_BOOT_MOUNT}/user-data
	sudo umount ${SYSTEM_BOOT_MOUNT}
EOL