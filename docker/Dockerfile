FROM nuand/gnuradio-bladerf:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN sudo apt-get update 
COPY ./keyboard /etc/default/keyboard
RUN sudo echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections
RUN sudo echo keyboard-configuration keyboard-configuration/layout select 'English (US)' | sudo debconf-set-selections
RUN sudo echo keyboard-configuration keyboard-configuration/layoutcode select 'us' | sudo debconf-set-selections 
RUN sudo echo "resolvconf resolvconf/linkify-resolvconf boolean false" | sudo debconf-set-selections
RUN sudo apt-get install -y keyboard-configuration
RUN sudo apt-get install -y qtcreator libxrender1 gdb
RUN sudo apt-get install -y fonts-ubuntu
RUN sudo apt install -y python3-pygccxml
CMD ["/usr/bin/qtcreator"]
