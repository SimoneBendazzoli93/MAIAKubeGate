#FROM ghcr.io/selkies-project/nvidia-egl-desktop:22.04-20241222100454
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

USER root

#COPY ui.js /opt/noVNC/app/ui.js
COPY default.template /etc/default.template
COPY bitmap.png /etc/bitmap.png
#COPY add_users.sh /etc/add_users.sh

COPY change_desktop_wallpaper.sh /etc/change_desktop_wallpaper.sh
RUN chmod 777 /etc/change_desktop_wallpaper.sh && chmod a+x /etc/change_desktop_wallpaper.sh

COPY Tools/Slicer/Slicer.desktop /etc/Slicer.desktop
COPY Tools/Slicer/300px-3DSlicerLogo-app-icon512.svg.png /etc/300px-3DSlicerLogo-app-icon512.svg.png
RUN chmod 777 /etc/Slicer.desktop && chmod a+x /etc/Slicer.desktop
COPY Tools/Slicer/install_slicer.sh /etc/install_slicer.sh
RUN chmod 777 /etc/install_slicer.sh && chmod a+x /etc/install_slicer.sh

COPY Tools/FreeSurfer/install_freesurfer.sh /etc/install_freesurfer.sh
RUN chmod 777 /etc/install_freesurfer.sh && chmod a+x /etc/install_freesurfer.sh
COPY Tools/FreeSurfer/FreeView.desktop /etc/FreeView.desktop
COPY Tools/FreeSurfer/FreeSurfer.png /etc/FreeSurfer.png
RUN chmod 777 /etc/FreeView.desktop && chmod a+x /etc/FreeView.desktop


COPY Tools/QuPath/QuPath.png /etc/QuPath.png
COPY Tools/QuPath/install_qupath.sh /etc/install_qupath.sh
COPY Tools/QuPath/QuPath.desktop /etc/QuPath.desktop
RUN chmod 777 /etc/QuPath.desktop && chmod a+x /etc/QuPath.desktop && chmod 777 /etc/install_qupath.sh && chmod a+x /etc/install_qupath.sh

COPY Tools/ITKSnap/ITKSnap.png /etc/ITKSnap.png
COPY Tools/ITKSnap/install_itksnap.sh /etc/install_itksnap.sh
COPY Tools/ITKSnap/ITKSnap.desktop /etc/ITKSnap.desktop
RUN chmod 777 /etc/install_itksnap.sh && chmod a+x /etc/install_itksnap.sh && chmod 777 /etc/ITKSnap.desktop && chmod a+x /etc/ITKSnap.desktop

COPY Tools/MITK/MITK.png /etc/MITK.png
COPY Tools/MITK/install_mitk.sh /etc/install_mitk.sh
COPY Tools/MITK/MITK.desktop /etc/MITK.desktop
RUN chmod 777 /etc/install_mitk.sh && chmod a+x /etc/install_mitk.sh && chmod 777 /etc/MITK.desktop && chmod a+x /etc/MITK.desktop


COPY Tools/Napari/Napari.png /etc/Napari.png
COPY Tools/Napari/install_napari.sh /etc/install_napari.sh
COPY Tools/Napari/Napari.desktop /etc/Napari.desktop
RUN chmod 777 /etc/install_napari.sh && chmod a+x /etc/install_napari.sh && chmod 777 /etc/Napari.desktop && chmod a+x /etc/Napari.desktop


COPY entrypoint.sh /etc/entrypoint.sh
RUN chmod 777 /etc/entrypoint.sh && \
    chmod a+x /etc/entrypoint.sh

COPY novnc.sh /etc/novnc.sh
RUN chmod 777 /etc/novnc.sh && \
    chmod a+x /etc/novnc.sh

COPY kasmvnc.sh /etc/kasmvnc.sh
RUN chmod 777 /etc/kasmvnc.sh && \
    chmod a+x /etc/kasmvnc.sh
COPY supervisord.conf   /etc/supervisord.conf

RUN chmod 777 /etc/
RUN sudo sed -i 's|a.initSetting("path","websockify")|a.initSetting("path",window.location.pathname.replace(/[^/]*$/,"").substring(1)+"websockify")|' \
  /usr/share/kasmvnc/www/main.bundle.js /usr/share/kasmvnc/www/screen.bundle.js

RUN sudo -u maia-user mkdir -pm700 /tmp/runtime-user
RUN sudo chown maia-user:maia-user /tmp/runtime-user
RUN sudo -u maia-user chmod 700 /tmp/runtime-user

RUN sudo mkdir -pm1777 /dev/input || sudo mkdir -pm1777 /dev/input || echo 'Failed to create joystick interposer directory'
RUN sudo touch /dev/input/js0 /dev/input/js1 /dev/input/js2 /dev/input/js3 || sudo touch /dev/input/js0 /dev/input/js1 /dev/input/js2 /dev/input/js3 || echo 'Failed to create joystick interposer devices'
RUN sudo chmod 777 /dev/input/js* || sudo chmod 777 /dev/input/js* || echo 'Failed to change permission for joystick interposer devices'
RUN chmod -R 777 /etc/nginx/
RUN chmod -R 777 /var/lib/nginx/
RUN chmod -R 777 /etc/ssl/private
RUN chmod -R 777 /etc/ssl/certs
USER 1000


ENTRYPOINT ["/usr/bin/supervisord"]