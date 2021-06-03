# gr-bladeRF

You can use a docker container for quick deployment. 
Docker Installation: https://docs.docker.com/engine/install/ubuntu/
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




