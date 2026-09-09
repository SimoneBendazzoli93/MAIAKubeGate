#!/bin/bash


if [ -d $HOME/Documents/Slicer-5.10.0-linux-amd64 ]; then
    echo "Slicer is already installed."
    exit 0
fi

wget https://download.slicer.org/bitstream/6911b598ac7b1c95e7934427 -O /etc/slicer.tar.gz

cp /etc/slicer.tar.gz $HOME/Documents/

tar -xf $HOME/Documents/slicer.tar.gz -C $HOME/Documents/

$HOME/Documents/Slicer-5.10.0-linux-amd64/Slicer --python-script /home/maia-user/Tutorials/Slicer_Extensions.py &

cp /etc/Slicer.desktop $HOME/Desktop/

