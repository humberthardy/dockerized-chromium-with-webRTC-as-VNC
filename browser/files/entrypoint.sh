#!/bin/bash

function run_forever() {
    while 'true'
    do
      echo "Execute '$@'"
      "$@"
      sleep 1
    done
}

export GEOMETRY="${SCREEN_WIDTH}x${SCREEN_HEIGHT}"

mkdir -p ~/.vnc

echo "set vnc password '${VNC_PASS:-secret}'"

echo "${VNC_PASS:-secret}\n" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

vncserver $DISPLAY -geometry $GEOMETRY -noxstartup  > /dev/null  &

# start xvfb
#export GEOMETRY="$SCREEN_WIDTH""x""$SCREEN_HEIGHT""x""$SCREEN_DEPTH"
#sudo Xvfb $DISPLAY -screen 0 $GEOMETRY -ac +extension RANDR > /dev/null 2>&1 &

# Run browser here
eval "$@" &

# start vnc
#run_forever x11vnc -forever -ncache_cr -xdamage -usepw -shared -rfbport 5900 -display $DISPLAY > /dev/null 2>&1 &

python3 /webrtc/controls.py &


for i in $(seq 1 10)
do
  xdpyinfo -display $DISPLAY >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    break
  fi
  echo Waiting xvfb...
  sleep 0.5
done

jwm -display $DISPLAY &
run_forever /webrtc/gst-rust --peer-id 1 --server wss://signaling:8443 &
run_forever chromium-browser --test-type  --no-default-browser-check --disable-popup-blocking --disable-background-networking --disable-client-side-phishing-detection --disable-component-update --safebrowsing-disable-auto-update https://www.youtube.com/watch?v=ABVjQyTnbIA


