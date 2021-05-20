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
        //in osmocom args for make source is strings,
        //therefore all params is strings
        //todo: change to vector<bladerf_devinfo>

        auto dev_list = bladerf_source_c::get_devices();
        if(dev_list.size() == 0)
            throw std::runtime_error("No supported devices found "
                                     "(check the connection and/or udev rules).");

        dev_ = make_bladerf_source_c( dev_list[0] ); //todo: get by id from block args
        for (size_t i = 0; i < dev_->get_num_channels(); i++) {
  #ifdef HAVE_IQBALANCE
          gr::iqbalance::optimize_c::sptr iq_opt = gr::iqbalance::optimize_c::make( 0 );
          gr::iqbalance::fix_cc::sptr     iq_fix = gr::iqbalance::fix_cc::make();

          connect(block, i, iq_fix, 0);
          connect(iq_fix, 0, self(), channel++);

          connect(block, i, iq_opt, 0);
          msg_connect(iq_opt, "iqbal_corr", iq_fix, "iqbal_corr");

          _iq_opt.push_back( iq_opt.get() );
          _iq_fix.push_back( iq_fix.get() );
  #else
          connect(dev_, i, self(), i);
  #endif
        }
     }

    /*
     * Our virtual destructor.
     */
    source_impl::~source_impl()
    {
    }

    size_t source_impl::get_num_channels()
    {
        return 0;
    }


  } /* namespace bladeRF */
} /* namespace gr */

