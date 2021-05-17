if(NOT PKG_CONFIG_FOUND)
    INCLUDE(FindPkgConfig)
endif()
PKG_CHECK_MODULES(PC_BLADERF bladeRF)

FIND_PATH(
    BLADERF_INCLUDE_DIRS
    NAMES bladeRF/api.h
    HINTS $ENV{BLADERF_DIR}/include
        ${PC_BLADERF_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    BLADERF_LIBRARIES
    NAMES gnuradio-bladeRF
    HINTS $ENV{BLADERF_DIR}/lib
        ${PC_BLADERF_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/bladeRFTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(BLADERF DEFAULT_MSG BLADERF_LIBRARIES BLADERF_INCLUDE_DIRS)
MARK_AS_ADVANCED(BLADERF_LIBRARIES BLADERF_INCLUDE_DIRS)
