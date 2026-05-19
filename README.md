# gr-bladeRF

GNU Radio source and sink blocks for bladeRF devices.

## bladeRF wiki

* [bladeRF wiki](https://github.com/Nuand/bladeRF/wiki)

## Installation

Build from source

    git clone https://github.com/Nuand/gr-bladeRF.git
    cd gr-bladeRF
    mkdir build
    cd build
    cmake ..
    make -j4
    sudo make install

## Building a Debian package

A `debian/` directory is provided so the module can be packaged with
`dpkg-buildpackage`. The build produces a single binary package
`gr-bladerf` (arch `any`) containing the shared library, PyBind11
Python bindings, GRC YAMLs, public headers and the
`bladeRFConfig.cmake` helper.

Prerequisites:

* Standard build deps declared in `debian/control` (debhelper-compat 13,
  cmake, gnuradio-dev, libbladerf-dev, libboost-dev, libvolk-dev,
  pybind11-dev, python3-dev, python3-numpy, dh-python).
* **gr-osmosdr C++ headers.** This module includes `osmosdr/*.h` from
  its public headers (`include/bladeRF/ranges.h`,
  `include/bladeRF/time_spec.h`) and private sources. Debian/Ubuntu's
  `gr-osmosdr` package currently does **not** ship a `-dev` variant, so
  install the headers manually before building the package, e.g. by
  building and installing [gr-osmosdr](https://github.com/osmocom/gr-osmosdr)
  to `/usr/local` (`cmake -S . -B build && sudo cmake --install build`).

Install build dependencies and build the package:

    sudo apt-get install build-essential devscripts debhelper dh-python \
        cmake pkgconf gnuradio-dev libbladerf-dev libboost-dev \
        libvolk-dev pybind11-dev python3-dev python3-numpy
    # plus gr-osmosdr headers as described above
    dpkg-buildpackage -us -uc -b

The resulting `gr-bladerf_<version>_<arch>.deb` is written to the parent
directory. Install it with `sudo dpkg -i ../gr-bladerf_*.deb` (then
`sudo apt-get -f install` to pull runtime deps).

## GNURadio-Companion Examples
Run FM-receiver example:

    cd 
    gnuradio-companion gr-bladeRF/apps/fm_receiver.grc

## Run on Raspberry
   
   [How to install gr-bladeRF on Raspberry Pi 4
](raspberry/)



