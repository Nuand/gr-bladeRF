/* -*- c++ -*- */
/*
 * Copyright 2021 Nuand LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "source_impl.h"

namespace gr {
  namespace bladeRF {

    source::sptr source::make(const std::string & args)
    {
      return gnuradio::make_block_sptr<source_impl>(args);
    }

    inline gr::io_signature::sptr make_io_signature( const std::string &args )
    {
        size_t max_nchan = 0;
        size_t dev_nchan = 0;
        const size_t nchan = std::max<size_t>(dev_nchan, 1); // assume at least one
        return gr::io_signature::make(nchan, nchan, sizeof(gr_complex));
    }

    /*
     * The private constructor
     */
    source_impl::source_impl(const std::string & args)
      : gr::hier_block2("source",
              gr::io_signature::make(0,0,0),
              make_io_signature(args))
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


  } /* namespace bladeRF */
} /* namespace gr */

