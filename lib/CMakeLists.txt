# Copyright 2011,2012,2016,2018,2019 Free Software Foundation, Inc.
#
# This file was generated by gr_modtool, a tool from the GNU Radio framework
# This file is a part of gr-bladeRF
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX
list(APPEND gr_bladerf_srcs
    source_impl.cc
    sink_impl.cc
    ranges.cc
)

#-pthread Adds support for multithreading with the pthreads library.
#This option sets flags for both the preprocessor and linker. (man gcc)
if(CMAKE_COMPILER_IS_GNUCXX)
    list(APPEND Boost_LIBRARIES -pthread)
endif()

MACRO (APPEND_LIB_LIST)
    SET (gr_bladerf_libs "${gr_bladerf_libs};${ARGN}" CACHE INTERNAL "lib list")
ENDMACRO(APPEND_LIB_LIST)

set(gr_bladerf_libs "" CACHE INTERNAL "lib that accumulates link targets")

add_library(gnuradio-bladeRF SHARED)
APPEND_LIB_LIST(${Boost_LIBRARIES} gnuradio::gnuradio-runtime)
target_include_directories(gnuradio-bladeRF
    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
    PUBLIC ${Boost_INCLUDE_DIRS}
    PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../include>
    PUBLIC $<INSTALL_INTERFACE:include>
  )
set_target_properties(gnuradio-bladeRF PROPERTIES DEFINE_SYMBOL "gnuradio_bladeRF_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-bladeRF PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Setup defines for high resolution timing
########################################################################
message(STATUS "")
message(STATUS "Configuring high resolution timing...")
include(CheckCXXSourceCompiles)

set(CMAKE_REQUIRED_LIBRARIES -lrt)
CHECK_CXX_SOURCE_COMPILES("
    #include <ctime>
    int main(){
        timespec ts;
        return clock_gettime(CLOCK_MONOTONIC, &ts);
    }
    " HAVE_CLOCK_GETTIME
)
unset(CMAKE_REQUIRED_LIBRARIES)

include(CheckCXXSourceCompiles)
CHECK_CXX_SOURCE_COMPILES("
    #include <mach/mach_time.h>
    int main(){
        mach_timebase_info_data_t info;
        mach_timebase_info(&info);
        mach_absolute_time();
        return 0;
    }
    " HAVE_MACH_ABSOLUTE_TIME
)

CHECK_CXX_SOURCE_COMPILES("
    #include <Windows.h>
    int main(){
        LARGE_INTEGER value;
        QueryPerformanceCounter(&value);
        QueryPerformanceFrequency(&value);
        return 0;
    }
    " HAVE_QUERY_PERFORMANCE_COUNTER
)

if(HAVE_CLOCK_GETTIME)
    message(STATUS "  High resolution timing supported through clock_gettime.")
    set(TIME_SPEC_DEFS HAVE_CLOCK_GETTIME)
    APPEND_LIB_LIST( "-lrt")
elseif(HAVE_MACH_ABSOLUTE_TIME)
    message(STATUS "  High resolution timing supported through mach_absolute_time.")
    set(TIME_SPEC_DEFS HAVE_MACH_ABSOLUTE_TIME)
elseif(HAVE_QUERY_PERFORMANCE_COUNTER)
    message(STATUS "  High resolution timing supported through QueryPerformanceCounter.")
    set(TIME_SPEC_DEFS HAVE_QUERY_PERFORMANCE_COUNTER)
else()
    message(STATUS "  High resolution timing supported through microsec_clock.")
    set(TIME_SPEC_DEFS HAVE_MICROSEC_CLOCK)
endif()

set_source_files_properties(
    time_spec.cc
    PROPERTIES COMPILE_DEFINITIONS "${TIME_SPEC_DEFS}"
)

########################################################################
# Setup bladeRF component
########################################################################
GR_REGISTER_COMPONENT("nuand bladeRF" ENABLE_BLADERF LIBBLADERF_FOUND)
if(ENABLE_BLADERF)
    add_subdirectory(bladerf)
endif(ENABLE_BLADERF)

########################################################################
# Finalize target
########################################################################
set_target_properties(gnuradio-bladeRF PROPERTIES SOURCES "${gr_bladerf_srcs}")
target_link_libraries(gnuradio-bladeRF ${gr_bladerf_libs})


########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-bladeRF)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

# If your unit tests require special include paths, add them here
#include_directories()
# List all files that contain Boost.UTF unit tests here
list(APPEND test_bladeRF_sources
)
# Anything we need to link to for the unit tests go here
list(APPEND GR_TEST_TARGET_DEPS gnuradio-bladeRF)

if(NOT test_bladeRF_sources)
    MESSAGE(STATUS "No C++ unit tests... skipping")
    return()
endif(NOT test_bladeRF_sources)

foreach(qa_file ${test_bladeRF_sources})
    GR_ADD_CPP_TEST("bladeRF_${qa_file}"
        ${CMAKE_CURRENT_SOURCE_DIR}/${qa_file}
    )
endforeach(qa_file)
