/* -*- c++ -*- */
/*
 * Copyright 2021 Nuand LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_BLADERF_SOURCE_IMPL_H
#define INCLUDED_BLADERF_SOURCE_IMPL_H

#include <bladeRF/source.h>

namespace gr {
  namespace bladeRF {

    class source_impl : public source
    {
     private:
      // Nothing to declare in this block.

     public:
      source_impl(const std::string & args);
      ~source_impl();

      // Where all the action really happens
    };

  } // namespace bladeRF
} // namespace gr

#endif /* INCLUDED_BLADERF_SOURCE_IMPL_H */

