#!/bin/bash

/opt/conda/bin/conda init bash

#sudo sed -i 's|a.initSetting("path","websockify")|a.initSetting("path",window.location.pathname.replace(/[^/]*$/,"").substring(1)+"websockify")|' \
#  /usr/share/kasmvnc/www/main.bundle.js /usr/share/kasmvnc/www/screen.bundle.js


exec "$@" &
/usr/bin/supervisord &

sleep 30

until [ -d "$HOME/Desktop" ]; do
  sleep 1
done

bash /etc/change_desktop_wallpaper.sh

if [ "$INSTALL_ZSH" = "1" ]; then
    /etc/install_zsh.sh
fi

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

#if [ ! -f "$HOME/.zshrc" ]; then
  cp /etc/.zshrc "$HOME/"
#fi

#if [ ! -f "$HOME/.tmux.conf" ]; then
  cp /etc/.tmux.conf "$HOME/"
#fi
/opt/conda/bin/conda init zsh
sleep infinity