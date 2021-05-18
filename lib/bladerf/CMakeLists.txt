# Copyright 2013 Free Software Foundation, Inc.
#
# This file is part of gr-bladeRF
#
# gr-bladeRF is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3, or
# (at your option) any later version.
#
# gr-bladeRF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gr-bladeRF; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# This file included, use CMake directory variables
########################################################################

target_include_directories(gnuradio-bladeRF PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${LIBBLADERF_INCLUDE_DIRS}
    ${Volk_INCLUDE_DIRS}
)

APPEND_LIB_LIST(
    ${LIBBLADERF_LIBRARIES}
    ${Volk_LIBRARIES}
)

list(APPEND bladeRF_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/bladerf_source_c.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/bladerf_sink_c.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/bladerf_common.cc
)
set(bladeRF_sources ${bladeRF_sources} PARENT_SCOPE)
