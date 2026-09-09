#!/bin/bash

# Add users
bash /usr/bin/create-users.sh

/etc/install_ssh_server.sh

# generate xrdp key
if [ ! -f "/etc/xrdp/rsakeys.ini" ];
	then
		xrdp-keygen xrdp auto
fi

# generate certificate for tls connection
if [ ! -f "/etc/xrdp/cert.pem" ];
	then
		# delete eventual leftover private key
		rm -f /etc/xrdp/key.pem || true
		cd /etc/xrdp
		if [ ! $CERTIFICATE_SUBJECT ]; then
			CERTIFICATE_SUBJECT="/C=US/ST=Some State/L=Some City/O=Some Org/OU=Some Unit/CN=Terminalserver"
		fi
		openssl req -x509 -newkey rsa:2048 -nodes -keyout /etc/xrdp/key.pem -out /etc/xrdp/cert.pem -days 365 -subj "$CERTIFICATE_SUBJECT"
		crudini --set /etc/xrdp/xrdp.ini Globals security_layer tls
		crudini --set /etc/xrdp/xrdp.ini Globals certificate /etc/xrdp/cert.pem
		crudini --set /etc/xrdp/xrdp.ini Globals key_file /etc/xrdp/key.pem

fi

# generate machine-id
uuidgen > /etc/machine-id

# set keyboard for all sh users
echo "export QT_XKB_CONFIG_ROOT=/usr/share/X11/locale" >> /etc/profile

#/etc/install_slicer.sh
#/etc/install_libreoffice.sh
#/etc/install_freesurfer.sh

#cp /etc/Matlab.desktop /home/ubuntu/Desktop/
#chmod 777 /home/ubuntu/Desktop/Matlab.desktop
#chmod a+x /home/ubuntu/Desktop/Matlab.desktop

unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.notebook_dir=/home/ubuntu --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.base_url=${NB_PREFIX} --NotebookApp.allow_origin='*' &

cp -r /etc/Tutorials /home/ubuntu/Tutorials
chmod -R 777 /home/ubuntu/Tutorials

exec "$@"
