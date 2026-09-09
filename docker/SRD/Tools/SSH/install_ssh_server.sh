#!/bin/bash

if ! command -v sshd >/dev/null 2>&1; then
    echo "SSH server is not installed."
    exit 0
fi

if [ ! -f "/etc/ssh/sshd_config" ]; then
    cp /ssh_orig/sshd_config /etc/ssh/
fi

sed -i 's/^Port 22/#Port 22/' /etc/ssh/sshd_config

if [ ! -f "/etc/ssh/ssh_config" ]; then
    cp /ssh_orig/ssh_config /etc/ssh/
fi

if [ ! -f "/etc/ssh/moduli" ]; then
    cp /ssh_orig/moduli /etc/ssh/
fi

if [ ! -f "/etc/ssh/ssh_host_rsa_key" ]; then
    ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
fi

if [ ! -f "/etc/ssh/ssh_host_ecdsa_key" ]; then
    ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa
fi

if [ ! -f "/etc/ssh/ssh_host_ed25519_key" ]; then
    ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519
fi

mkdir -p /var/run/sshd
mkdir -p /etc/ssh/sshd_config.d
cp /etc/ssh-server/sftp.conf /etc/ssh/sshd_config.d/99-sftp.conf

if [ ! -f /etc/supervisor/conf.d/sshd.conf ]; then
    cp /etc/ssh-server/sshd.supervisor.conf /etc/supervisor/conf.d/sshd.conf
fi
