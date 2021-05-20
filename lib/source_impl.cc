/* -*- c++ -*- */
/*
 * Copyright 2021 Nuand LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "source_impl.h"
#include "arg_helpers.h"

namespace gr {
  namespace bladeRF {

    source::sptr source::make(const std::string & args)
    {
      return gnuradio::make_block_sptr<source_impl>(args);
    }

     /*
     * The private constructor
     */
    source_impl::source_impl(const std::string & args)
      : gr::hier_block2("source",
              gr::io_signature::make(0,0,0),
              args_to_io_signature(args))
    {

      //connect(self(), 0, d_firstblock, 0);
      // connect other blocks
      //connect(d_lastblock, 0, self(), 0);
    }

    /*
     * Our virtual destructor.
     */
    source_impl::~source_impl()
    {
    }

    size_t source_impl::get_num_channels() override
    {

    }


  } /* namespace bladeRF */
} /* namespace gr */

