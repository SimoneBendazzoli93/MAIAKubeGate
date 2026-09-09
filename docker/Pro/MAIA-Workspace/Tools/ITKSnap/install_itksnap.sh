#!/bin/bash

if [ -d $HOME/Documents/itksnap-4.2.0-20240422-Linux-gcc64 ]; then
    echo "ITK-SNAP is already installed."
    exit 0
fi

wget https://sourceforge.net/projects/itk-snap/files/itk-snap/4.2.0/itksnap-4.2.0-20240422-Linux-gcc64.tar.gz
#tar --help
tar -xvf itksnap-4.2.0-20240422-Linux-gcc64.tar.gz -C /home/maia-user/Documents/ && rm itksnap-4.2.0-20240422-Linux-gcc64.tar.gz
chmod u+x $HOME/Documents/itksnap-4.2.0-20240422-Linux-gcc64/bin/itksnap


cp /etc/ITKSnap.desktop $HOME/Desktop/