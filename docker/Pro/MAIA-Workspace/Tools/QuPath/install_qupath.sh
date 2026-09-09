#!/bin/bash

if [ -d $HOME/Documents/QuPath-v0.5.1-Linux ]; then
    echo "QuPath is already installed."
    exit 0
fi

wget https://github.com/qupath/qupath/releases/download/v0.5.1/QuPath-v0.5.1-Linux.tar.xz -O /tmp/QuPath-v0.5.1-Linux.tar.xz
tar -xf /tmp/QuPath-v0.5.1-Linux.tar.xz -C $HOME/Documents/ && rm /tmp/QuPath-v0.5.1-Linux.tar.xz
chmod u+x $HOME/Documents/QuPath-v0.5.1-Linux/QuPath/bin/QuPath

cp /etc/QuPath.desktop $HOME/Desktop/