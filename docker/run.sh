#!/bin/bash

set -x

# hack but works
xhost +

sudo docker run \
  -it --rm --privileged \
  --net=host \
  -e PULSE_SERVER=unix:/run/user/1000/pulse/native \
  -v /var/lib/dbus:/var/lib/dbus \
  -v /dev/bus/usb:/dev/bus/usb \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $HOME/.Xauthority:/home/blade/.Xauthority \
  -e DISPLAY \
  -v /run/user/1000/pulse:/run/user/1000/pulse \
  -u blade \
  gnuradio /bin/bash
