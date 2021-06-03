# gr-bladeRF

You can use a docker container for quick deployment. 
Easy docker installation: https://docs.docker.com/engine/install/ubuntu/#install-from-a-package

After install run next commands:

    sudo docker/run.sh
    cd gr-bladeRF
    mkdir build
    cd build
    cmake ..
    make -j4
    sudo make install

Run FM-receiver example:

    cd 
    gnuradio-companion gr-bladeRF/apps/fm_receiver.grc




