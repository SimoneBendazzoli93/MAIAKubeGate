FROM ubuntu:24.04 AS builder
MAINTAINER Simone Bendazzoli

# Install packages

ENV DEBIAN_FRONTEND=noninteractive
# Ubuntu 24.04 uses deb822 sources; enable deb-src for pulseaudio source/build-dep
RUN cp /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu-src.sources && \
    sed -i 's/Types: deb/Types: deb-src/' /etc/apt/sources.list.d/ubuntu-src.sources
RUN apt-get -y update
RUN apt-get -yy upgrade
ENV BUILD_DEPS="git autoconf libtool pkg-config libssl-dev libpam0g-dev \
    libx11-dev libxfixes-dev libxrandr-dev nasm xsltproc flex \
    bison libxml2-dev dpkg-dev fakeroot libcap-dev libxkbfile-dev"
RUN apt-get -yy install sudo apt-utils software-properties-common $BUILD_DEPS

# Build pulseaudio modules for xrdp

WORKDIR /tmp
RUN apt-get source pulseaudio
RUN apt-get build-dep -yy pulseaudio
RUN PULSE_SRC=$(find /tmp -maxdepth 1 -type d -name 'pulseaudio-*') && \
    mv "$PULSE_SRC" /tmp/pulseaudio-src
WORKDIR /tmp/pulseaudio-src
RUN dpkg-buildpackage -rfakeroot -uc -b
WORKDIR /tmp
RUN apt-get -yy install libpulse-dev
RUN git clone --recursive https://github.com/neutrinolabs/pulseaudio-module-xrdp.git
WORKDIR /tmp/pulseaudio-module-xrdp
RUN ./bootstrap && ./configure PULSE_DIR=/tmp/pulseaudio-src
RUN make
RUN mkdir -p /tmp/so
RUN cp src/.libs/*.so /tmp/so

FROM ubuntu:24.04
ARG ADDITIONAL_PACKAGES=""
ARG INSTALL_SSH_SERVER=false
ENV ADDITIONAL_PACKAGES=${ADDITIONAL_PACKAGES}
ENV TZ=Etc/UTC
ENV DEBIAN_FRONTEND=noninteractive
# ubuntu:24.04 ships a default ubuntu user (uid 1000); remove it so users.list can create uid 999
RUN userdel -r ubuntu 2>/dev/null || true
RUN apt-get update && apt-get install -y software-properties-common apt-utils
# Dummy telinit so package postinst scripts do not fail without systemd
RUN printf '#!/bin/sh\nexit 1\n' > /usr/sbin/telinit && chmod +x /usr/sbin/telinit
RUN apt-get -y full-upgrade && apt-get install -y \
  ca-certificates \
  crudini \
  dbus-x11 \
  less \
  locales \
  pulseaudio \
  sudo \
  curl \
  git \
  iputils-ping \
  net-tools \
  nano \
  rsync \
  tree \
  unzip \
  zip \
  htop \
  supervisor \
  tzdata \
  uuid-runtime \
  vim \
  vlc \
  wget \
  xauth \
  xautolock \
  xfce4 \
  xfce4-clipman-plugin \
  xfce4-cpugraph-plugin \
  xfce4-netload-plugin \
  xfce4-screenshooter \
  xfce4-taskmanager \
  xfce4-terminal \
  xfce4-xkb-plugin \
  xorgxrdp \
  xprintidle \
  xrdp \
  xserver-xorg-legacy \
  $ADDITIONAL_PACKAGES && \
  apt-get remove -yy light-locker xscreensaver && \
  apt-get autoremove -yy && \
  rm -rf /var/cache/apt /var/lib/apt/lists && \
  mkdir -p /var/lib/xrdp-pulseaudio-installer
# Firefox is a snap on Ubuntu 24.04; install the .deb from Mozilla instead
RUN install -d -m 0755 /etc/apt/keyrings && \
  wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O /etc/apt/keyrings/packages.mozilla.org.asc && \
  echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" > /etc/apt/sources.list.d/mozilla.list && \
  printf 'Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000\n' > /etc/apt/preferences.d/mozilla && \
  apt-get update && apt-get install -y firefox && \
  rm -rf /var/cache/apt /var/lib/apt/lists
COPY --from=builder /tmp/so/module-xrdp-source.so /var/lib/xrdp-pulseaudio-installer
COPY --from=builder /tmp/so/module-xrdp-sink.so /var/lib/xrdp-pulseaudio-installer
ADD bin /usr/bin
ADD etc /etc
ADD autostart /etc/xdg/autostart
#ADD pulse /usr/lib/pulse-10.0/modules/


# Configure
RUN mkdir -p /var/run/dbus && \
  cp /etc/X11/xrdp/xorg.conf /etc/X11 && \
  sed -i "s/console/anybody/g" /etc/X11/Xwrapper.config && \
  sed -i "s/xrdp\/xorg/xorg/g" /etc/xrdp/sesman.ini && \
  locale-gen en_US.UTF-8 && \
  echo "pulseaudio -D --enable-memfd=True" > /etc/skel/.Xsession && \
  echo "xfce4-session" >> /etc/skel/.Xsession && \
  echo "xfce4-session" > /etc/skel/.Xclients && \
  rm -rf /etc/xrdp/rsakeys.ini /etc/xrdp/*.pem && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY Tutorials /etc/Tutorials

COPY Tools/SSH/install_ssh_server.sh /etc/install_ssh_server.sh
COPY Tools/SSH/sshd.supervisor.conf /etc/ssh-server/sshd.supervisor.conf
COPY Tools/SSH/sftp.conf /etc/ssh-server/sftp.conf
RUN chmod 777 /etc/install_ssh_server.sh && chmod a+x /etc/install_ssh_server.sh
RUN if [ "$INSTALL_SSH_SERVER" = "true" ]; then \
    apt-get update && \
    apt-get install -y --no-install-recommends openssh-server && \
    cp -r /etc/ssh /ssh_orig && \
    rm -rf /etc/ssh/* && \
    rm -rf /var/lib/apt/lists/* ; \
    fi

RUN apt-get update && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages jupyterlab minio


VOLUME ["/etc/ssh","/home"]
EXPOSE 3389 2022 9001 8888
RUN chmod 777 /var/log
ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["supervisord"]
