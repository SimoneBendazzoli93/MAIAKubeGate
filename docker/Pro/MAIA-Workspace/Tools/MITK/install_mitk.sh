#!/bin/bash

if [ -d $HOME/Documents/MITK-v2024.12-linux-x86_64 ]; then
    echo "ITK-SNAP is already installed."
    exit 0
fi

wget https://www.mitk.org/download/releases/MITK-2024.12/Ubuntu%2022.04/MITK-v2024.12-linux-x86_64.tar.gz
#tar --help
tar -xvf MITK-v2024.12-linux-x86_64.tar.gz -C /home/maia-user/Documents/ && rm MITK-v2024.12-linux-x86_64.tar.gz
chmod u+x $HOME/Documents/MITK-v2024.12-linux-x86_64/MitkWorkbench.sh


cp /etc/MITK.desktop $HOME/Desktop/