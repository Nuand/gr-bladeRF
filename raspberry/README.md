How to install gr-bladeRF to 

O. Prepare Raspberry Pi4

0.1. Download and install rpi-imager:
   visit https://www.raspberrypi.com/software and download rpi imager
   or run
   ```
   wget https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb
   sudo dpkg -i imager_1.6.2_amd64.deb 
   ```
0.2. Flash image and setup network
   Insert microSD card to slot on your computer an run rpi-imager
   
   Choose OS: Other general purpose OS - Ubuntu - Ubuntu Server 21.04.3 LTS (RPi 3/4/400) 64-bit server OS for arm64 architectures
   
   Choose storage - your microSD card
   
   Press write
   
   Insert microSD into RPi and plug ethernet & power cables.

0.3. Determining the Pi’s IP address
   To determine the IP address of your board, open a terminal and run the `arp` command:

   On Ubuntu and Mac OS:
    ```
    arp -na | grep -i "e4:5f"   
    ? (192.168.1.105) at e4:5f:01:35:c0:92 [ether] on wlp3s0
    ```
   ubuntu@ubuntu:~$ sudoedit /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
   
  Connect to rpi4 via ssh:
      ```
      ssh ubuntu@192.168.1.105
      ```
      password: `ubuntu`
      Change password on first login and connect again.
      
0.5. Install a desktop

   check architecture
   ```
   ubuntu@ubuntu:~$ dpkg --print-architecture 
   arm64
   ```
   ```
   sudo apt update
   sudo apt -y upgrade   
   sudo apt install -y xubuntu-desktop
   ```
   
2. Install bladeRF

    ```
    sudo add-apt-repository ppa:nuandllc/bladerf
    sudo apt-get update
    sudo apt-get install -y bladerf libbladerf-dev bladerf-firmware-fx3    
    sudo apt-get install bladerf-fpga-hostedx40   # for bladeRF x40
    sudo apt-get install bladerf-fpga-hostedx115  # for bladeRF x115
    sudo apt-get install bladerf-fpga-hostedxa4   # for bladeRF 2.0 Micro A4
    sudo apt-get install bladerf-fpga-hostedxa9   # for bladeRF 2.0 Micro A9
    ```
    Check bladeRF:
    ```
    ubuntu@ubuntu:~$ bladeRF-cli -i
        bladeRF> info

          Board:                    Nuand bladeRF 2.0 (bladerf2)
          Serial #:                 0a3e891bd6ff4eee908b8278a2a67d45
          VCTCXO DAC calibration:   0x1d01
          FPGA size:                49 KLE
          FPGA loaded:              yes
          Flash size:               32 Mbit
          USB bus:                  2
          USB address:              2
          USB speed:                SuperSpeed
          Backend:                  libusb
          Instance:                 0

        bladeRF> exit
    ```
3. Crossplatform build volk and gnuradio using docker and install on RPi

    ./build_gnuradio.sh 
    
    Transfer files to RPi:
    ```
    scp *.deb ubuntu@192.168.1.105:/home/ubuntu
    ```
    Connect to RPi

    ssh -X ubuntu@192.168.1.105 # -X for run GUI applications

    Install 
    ```  
    sudo dpkg -i volk.deb
    sudo dpkg -i gnuradio.deb
    sudo apt-get install -y libusb-1.0-0-dev libusb-1.0-0 git cmake g++ \
       libboost-all-dev libgmp-dev swig python3-numpy python3-matplotlib \
       python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev \
       libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 \
       liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins \
       python3-zmq python3-scipy python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
       libcodec2-dev libgsm1-dev libqt5svg5-dev libpulse-dev pulseaudio alsa-base \
       libasound2 libasound2-dev pybind11-dev libsndfile-dev
    ```
    Run gnuradio
    ```
    export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
    gnuradio-companion
    ```
4. Build and install gr-iqbal, gr-osmosdr, gr-bladeRF

    Make directory for source
    ```
    mkdir ~/gr
    ```
    # gr-iqbal
    ```
    cd ~/gr
    git clone git://git.osmocom.org/gr-iqbal
    cd gr-iqbal
    git submodule update --init --recursive
    mkdir build && cd build
    cmake ..
    make -j$(nproc) 
    sudo make install && sudo ldconfig
    ```
    # gr-osmosdr
    #############
    ```
    cd ~/gr
    git clone https://git.osmocom.org/gr-osmosdr
    cd gr-osmosdr
    mkdir build && cd build
    cmake ..
    make -j$(nproc)
    sudo make install && sudo ldconfig
    ```
    #gr-bladeRF
    ############
    ```
    cd ~/gr
    git clone https://github.com/Nuand/gr-bladeRF.git
    cd gr-bladeRF
    mkdir build
    cd build
    cmake ..
    make -j4
    sudo make install
    ```
    
    Check `gr-bladeRF`:
    
    Setup audio forwarding:
    ```    
    scp ~/.config/pulse/cookie ubuntu@192.168.1.105:/home/ubuntu/.config/pulse/cookie
    ```

    ```
    gnuradio-companion ~/gr/gr-bladeRF/apps/fm_receiver.grc
    ```

