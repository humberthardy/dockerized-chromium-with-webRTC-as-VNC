FROM ubuntu:18.04

#
# Webrecorder:  base browser
#

RUN apt -y update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && dpkg-reconfigure -f noninteractive tzdata


RUN apt install -qqy --no-install-recommends  \
    git \
    sudo \
    #python2.7 \
    python3-pip \
    python3-dev \
    build-essential \
    python3-openssl \
    libssl-dev libffi-dev \
    net-tools \
    libnss3-tools \
    x11vnc \
    xvfb \
    curl \
    wget \
    vim \
    socat \
    jwm \
    autocutsel \
    dnsutils \
    pulseaudio \
    libopus-dev \
    gstreamer-1.0 \
    gstreamer1.0-tools \
    gstreamer1.0-alsa \
    gstreamer1.0-nice \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-good1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    libjson-glib-dev \
    libsoup2.4-dev



# sudo
RUN useradd browser --shell /bin/bash --create-home \
  && usermod -a -G sudo browser \
  && echo 'ALL ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers \
  && echo 'browser:secret' | chpasswd


# fonts
RUN apt-get -qqy --no-install-recommends install \
    fonts-ipafont-gothic \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-cyrillic \
    xfonts-scalable \
    xfonts-base \
    fonts-liberation \
    fonts-arphic-bkai00mp fonts-arphic-bsmi00lp fonts-arphic-gbsn00lp fonts-arphic-gkai00mp fonts-arphic-ukai fonts-farsiweb fonts-nafees fonts-sil-abyssinica fonts-sil-ezra fonts-sil-padauk fonts-unfonts-extra fonts-unfonts-core fonts-indic fonts-thai-tlwg fonts-lklug-sinhala \
  && rm -rf /var/lib/apt/lists/*

# fix module-console-kit for opus
RUN sed -i '/load-module module-console-kit/s/^/#/' /etc/pulse/default.pa


WORKDIR /app/


COPY ./files/jwmrc /home/browser/.jwmrc


#
# Webrecorder: Browser Chromium 65
#

ARG TURBOVNC_VERSION=2.1.2
ARG VIRTUALGL_VERSION=2.5.2
ARG LIBJPEG_VERSION=1.5.2

ARG CHROMIUM_VERSION

RUN sudo echo "deb http://archive.canonical.com/ubuntu xenial partner" | sudo tee /etc/apt/sources.list.d/flash-plugin.list
RUN sudo apt-get update
RUN sudo apt install --assume-yes adobe-flashplugin gdebi wmctrl

COPY ${CHROMIUM_VERSION} /tmp/${CHROMIUM_VERSION}
RUN  gdebi --non-interactive /tmp/${CHROMIUM_VERSION}/chromium-codecs-ffmpeg-extra_${CHROMIUM_VERSION}_amd64.deb && \
     gdebi --non-interactive /tmp/${CHROMIUM_VERSION}/chromium-browser_${CHROMIUM_VERSION}_amd64.deb && \
     rm -rf /tmp/${CHROMIUM_VERSION}

USER browser

WORKDIR /home/browser


LABEL wr.name="Chromium" \
      wr.os="linux" \
      wr.about="https://www.chromium.org/" \
      wr.icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADM0lEQVQ4T3WTW2xUVRSG/33mzLlf5syl7VxKyx1SrEYJqUgUqwUTHowvBFt8EAIaEgiE+IIQJ8RYTFAToy/eEpU+qpGUB8BqUBQJCSQQmxYCWNLG6bQzZ27nMudqHLAR1J2sh72z1rf+7Pw/wf+cjfkf6A7GfEyR6WqmdOF6Pp8P/quVPPi4682vh5yG9dacbuZcP6R8zwfNcWF7Wi2k4tKr7+7ddPKfM/cBXjv2zZcThcZ2XpXA8CyoCAXP8WA3TBh6HQEVQWd38sIic8uGfJ60FC0AXj52cmy+4fUrmghVkyHEJFB0BI7ZhFGuoTqro1ooI+RYLF/WdvrDvZueWwAcGfl521SxPlJDlFI1EVpCRbxdQ1rj4ZSq0As6qkW9BTFNG9G4GizJxHYfGVr/aUvBoZHztwjDLL6muxAEDrmkhBd72vDj5AyMso4XejthK22oOMDMzBxCx0VWpgvPru1Ok8HhUY1LiKVEQiau5eCmQ+HgugxeOXsdi9MapubrqI3fxBeDj4B0rsbM9Bx8x0EuLgGMnyQ73v52pcfzE3JKQUblMTldwUMy8PFcgKd7srg6VcJvl29gV7KMgW0v4Y9iDXQYIJuQANvsI3veO7u67DTHxYQMLSYgrQiwJiZwdDpEW0rFfN1Cx+QNbO0N8fiW7ZgtVhGXWLTHBPhGbQMZHP5Js81iSYiLhI8JkCQO/SmCN46fgi5IYG0bxLuFo/t2oKksgmVYSGsiJDYSFNd0MK1PPPD+6dt3ykY3p/BgRQ6azOBhtoFLVy4iQkWwYlkPpNxK1Jshkgp/b3vjzjPrlna1AK9/dG7otm6dsA0DNBcFzUZbJhIjATzXQ07hkMpkEZc5JGQOHEPDqVV3DvQt/2zBSIc+OX9muuYMOLYNz3UQ+D5ACESWxlOPLoUsi4iJzN3hSuXMwPoVm+9z4l+Xw5//OjZrod93XQTB3ez0dUnIdbZD4qIghMAz6r/0r13yJCHEfxBAAVCGDhzf2bWqd7/FJjIqS6iNvVkQhKFR0etjo1998M7w4RMAfgdgAwj/lUYAUQBxRKMdz2/d84RVmmp+/93ouOd58wAq98r9O5F/At8SPZUrbJT4AAAAAElFTkSuQmCC"

USER root
# Add turboVNC & virtualgl
RUN cd /tmp && \
    curl -fsSL -O https://svwh.dl.sourceforge.net/project/turbovnc/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb \
        -O https://svwh.dl.sourceforge.net/project/libjpeg-turbo/${LIBJPEG_VERSION}/libjpeg-turbo-official_${LIBJPEG_VERSION}_amd64.deb \
        -O https://svwh.dl.sourceforge.net/project/virtualgl/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb \
        -O https://svwh.dl.sourceforge.net/project/virtualgl/${VIRTUALGL_VERSION}/virtualgl32_${VIRTUALGL_VERSION}_amd64.deb && \
    dpkg -i *.deb && \
    rm -f /tmp/*.deb && \
    sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver && \
    echo 'no-httpd\n\
    no-x11-tcp-connections\n\
    no-pam-sessions\n\
    ' > /etc/turbovncserver-security.conf


ENV PATH ${PATH}:/opt/VirtualGL/bin:/opt/TurboVNC/bin

#
## Add nvidia Stuff for OpenGl
#

# Add glvnd
RUN dpkg --add-architecture i386 && \
    apt-get update && apt-get install -y --no-install-recommends \
        libxau6 libxau6:i386 \
        libxdmcp6 libxdmcp6:i386 \
        libxcb1 libxcb1:i386 \
        libxext6 libxext6:i386 \
        libx11-6 libx11-6:i386 && \
    rm -rf /var/lib/apt/lists/*

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
        ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
        ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics,compat32,utility,display

# Required for non-glvnd setups.
ENV LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu:/usr/lib/i386-linux-gnu${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

RUN apt-get update && apt-get install -y --no-install-recommends \
    	libglvnd0 libglvnd0:i386 \
	libgl1 libgl1:i386 \
	libglx0 libglx0:i386 \
	libegl1 libegl1:i386 \
	libgles2 libgles2:i386 \
	libglu1

COPY ./files/10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json



USER browser

# Specific POC



EXPOSE 6789
USER root


RUN apt install --assume-yes nload
RUN pip3 install -U setuptools pip

ARG CHROMIUM_COMMAND='chromium-browser --test-type --disable-web-security --allow-outdated-plugins  --ignore-certificate-errors --no-default-browser-check --disable-popup-blocking --disable-background-networking --disable-client-side-phishing-detection --disable-component-update --safebrowsing-disable-auto-update $URL'


COPY ./files /webrtc
WORKDIR /webrtc

RUN pip3 install -r requierements.txt
run chmod +x /webrtc/entrypoint.sh

USER browser

ENV DISPLAY :99

ENV PROXY_PORT 8080
ENV PROXY_GET_CA http://mitm.it/cert/pem



CMD ""
ENV URL "https://www.youtube.com/watch?v=ABVjQyTnbIA"
ENV CHROMIUM_COMMAND $CHROMIUM_COMMAND
RUN sudo ln -s /usr/bin/python3 /usr/bin/python
ENTRYPOINT /webrtc/entrypoint.sh
