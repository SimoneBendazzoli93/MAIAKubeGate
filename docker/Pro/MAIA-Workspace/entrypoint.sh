#!/bin/bash -e

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#sudo sed -i 's|a.initSetting("path","websockify")|a.initSetting("path",window.location.pathname.replace(/[^/]*$/,"").substring(1)+"websockify")|' \
#  /usr/share/kasmvnc/www/main.bundle.js /usr/share/kasmvnc/www/screen.bundle.js

trap "echo TRAPed signal" HUP INT QUIT TERM

# Create and modify permissions of XDG_RUNTIME_DIR
## Added by MAIA-PRO

## End Added by MAIA-PRO
# Make user directory owned by the user in case it is not
#sudo chown maia-user:maia-user /home/maia-user || sudo chown maia-user:maia-user /home/maia-user/* || { echo "Failed to change maia-user directory permissions. There may be permission issues."; }
# Change operating system password to environment variable
if [ ! -d /home/maia-user/Tutorials ]; then
  cp -r /etc/Tutorials /home/maia-user
  #chmod -R 777 /home/maia-user/Tutorials
fi

if [ ! -f /home/maia-user/Welcome.ipynb ]; then
  cp /etc/Welcome.ipynb /home/maia-user
  #chmod 777 /home/maia-user/Welcome.ipynb
fi


#if [ ! -d /home/maia-user/Shared ]; then
#    ln -s /mnt/shared /home/maia-user/Shared
#fi
touch /home/maia-user/.env
JUPYTERHUB_POD_NAME="jupyter-$(echo "$JUPYTERHUB_USER" | sed -r 's/[-]+/-2d/g' | sed -r 's/[@]+/-40/g' | sed -r 's/[.]+/-2e/g')"
if grep -Fx "JUPYTERHUB_POD_NAME=${JUPYTERHUB_POD_NAME}" /home/maia-user/.env;
then
    echo "Environment variable already set"
else
  echo "JUPYTERHUB_POD_NAME=${JUPYTERHUB_POD_NAME}" >> /home/maia-user/.env
fi

#echo "maia-user:$PASSWD" | sudo chpasswd
## Added by MAIA-PRO
/etc/kasmvnc.sh &
# Add custom processes right below this line, or within `supervisord.conf` to perform service management similar to systemd


sed -i 's|worker_processes .*|worker_processes 1;|' /etc/nginx/nginx.conf

envsubst '${JUPYTERHUB_USER},${NAMESPACE}' < /etc/default.template > default
mv default /etc/nginx/sites-enabled/
#sudo nginx -c /etc/nginx/nginx.conf -g 'daemon off;' &

## End Added by MAIA-PRO


if [ ! -f /home/maia-user/.bash_profile ]; then
  cp /etc/.bash_profile /home/maia-user/
fi
cp /etc/MAIA.png /home/maia-user/


## Added by MAIA-PRO
sleep 30

until [ -d "$HOME/Desktop" ]; do
  sleep 1
done

bash /etc/change_desktop_wallpaper.sh
## End Added by MAIA-PRO
if [ "$INSTALL_ZSH" = "1" ]; then
    /etc/install_zsh.sh
fi
## Added by MAIA-PRO
if [ "$INSTALL_SLICER" = "1" ]; then
    /etc/install_slicer.sh
fi

if [ "$INSTALL_FREESURFER" = "1" ]; then
    /etc/install_freesurfer.sh
fi

if [ "$INSTALL_ITKSNAP" = "1" ]; then
    /etc/install_itksnap.sh
fi

if [ "$INSTALL_QUPATH" = "1" ]; then
    /etc/install_qupath.sh
fi

if [ "$INSTALL_MITK" = "1" ]; then
    /etc/install_mitk.sh
fi

if [ "$INSTALL_NAPARI" = "1" ]; then
    /etc/install_napari.sh
fi
## End Added by MAIA-PRO
#if [ ! -f "$HOME/.zshrc" ]; then
  cp /etc/.zshrc "$HOME/"
#fi

#if [ ! -f "$HOME/.tmux.conf" ]; then
  cp /etc/.tmux.conf "$HOME/"
#fi
# Only for debugging and development
#exec "$@"
echo "Session Running. Press [Return] to exit."
read