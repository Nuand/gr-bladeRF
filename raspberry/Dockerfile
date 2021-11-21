#
# Dockerfile
#
FROM ubuntu:focal AS builder 
RUN apt update
RUN apt install -y git
WORKDIR /home
RUN git clone https://github.com/gnuradio/gnuradio.git -b maint-3.9
COPY ./keyboard /etc/default/keyboard
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN echo keyboard-configuration keyboard-configuration/layout select 'English (US)' | debconf-set-selections
RUN echo keyboard-configuration keyboard-configuration/layoutcode select 'us' | debconf-set-selections 
RUN echo "resolvconf resolvconf/linkify-resolvconf boolean false" | debconf-set-selections
RUN apt-get install -y keyboard-configuration
RUN apt install -y build-essential fakeroot devscripts
RUN apt-get install -y cmake debhelper dh-python doxygen gir1.2-gtk-3.0 gir1.2-pango-1.0 graphviz libasound2-dev libboost-date-time-dev libboost-dev libboost-filesystem-dev libboost-program-options-dev libboost-regex-dev libboost-system-dev libboost-test-dev libboost-thread-dev libcodec2-dev libfftw3-dev libfontconfig1-dev libgmp-dev libgsl-dev libgsm1-dev libjack-jackd2-dev liblog4cpp5-dev liborc-0.4-dev libpangocairo-1.0-0 libportaudio2 libpulse-dev libqwt-qt5-dev libsdl1.2-dev libsndfile1-dev libthrift-dev libuhd-dev libusb-1.0-0-dev libvolk2-dev libxi-dev libxrender-dev libzmq3-dev pkg-config portaudio19-dev pybind11-dev python3-click python3-click-plugins python3-dev python3-gi python3-gi-cairo python3-lxml python3-mako python3-numpy python3-opengl python3-pyqt5 python3-scipy python3-yaml python3-zmq qt5-qmake qtbase5-dev qttools5-dev thrift-compiler xmlto libsoapysdr-dev checkinstall

RUN git clone --recursive https://github.com/gnuradio/volk.git
WORKDIR /home/volk/
RUN echo $PWD
RUN mkdir build 
WORKDIR /home/volk/build
RUN cmake ..
RUN make -j$(nproc)
RUN checkinstall \
	--default \
	--install=no \
	--nodoc \
	--pkgname=volk\
	--type=debian  -y

WORKDIR /home/gnuradio
RUN mkdir -p /home/gnuradio/build
WORKDIR /home/gnuradio/build
RUN cmake ..
RUN make -j$(nproc)
RUN checkinstall --default --install=no --pkgname=gnuradio --type=debian -y

WORKDIR /out

RUN mv /home/gnuradio/build/gnuradio*.deb gnuradio.deb
RUN mv /home/volk/build/volk*.deb volk.deb

ENTRYPOINT ["/bin/bash", "-l", "-c", "cp *.deb /local/"]

