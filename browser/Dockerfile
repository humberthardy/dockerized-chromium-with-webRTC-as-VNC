FROM oldwebtoday/chromium:65



EXPOSE 6789
USER root


RUN apt-get --assume-yes install scrot python3-tk python3-dev

COPY . /webrtc
WORKDIR /webrtc

RUN pip install -r requierements.txt
run chmod +x /webrtc/entrypoint.sh

USER browser


CMD ""
ENTRYPOINT /webrtc/entrypoint.sh