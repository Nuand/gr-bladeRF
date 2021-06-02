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

        device_ = make_bladerf_source_c( args ); //todo: get by id from block args
        for (size_t i = 0; i < device_->get_num_channels(); i++) {
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
          connect(device_, i, self(), i);
  #endif
        }
     }

    source_impl::~source_impl()
    {
    }

    size_t source_impl::get_num_channels()
    {
        return device_ ? device_->get_num_channels() : 0;
    }

    osmosdr::meta_range_t source_impl::get_sample_rates()
    {
        return device_ ? device_->get_sample_rates() : osmosdr::meta_range_t{};
    }

    double source_impl::set_sample_rate(double rate)
    {
      double sample_rate = device_->set_sample_rate(rate);

      #ifdef HAVE_IQBALANCE
            size_t channel = 0;
            for (size_t dev_chan = 0; dev_chan < dev_->get_num_channels(); dev_chan++) {
              if ( channel < _iq_opt.size() ) {
                gr::iqbalance::optimize_c *opt = _iq_opt[channel];

                if ( opt->period() > 0 ) { /* optimize is enabled */
                  opt->set_period( dev->get_sample_rate() / 5 );
                  opt->reset();
                }
              }

              channel++;
            }
      #endif
          sample_rate_ = sample_rate;
        return sample_rate_;
    }

    double source_impl::get_sample_rate()
    {
        return device_ ? device_->get_sample_rate() : 0;
    }

    osmosdr::freq_range_t source_impl::get_freq_range(size_t chan)
    {
        if(chan < get_num_channels())
        {
            return device_->get_freq_range( chan );
        }
        return osmosdr::freq_range_t();
    }

    double source_impl::set_center_freq(double freq, size_t chan)
    {
        return center_freq_.set_if_not_equal(freq,
                                             chan,
                                             get_num_channels(),
                                             [this,freq,chan]{
            return device_->set_center_freq(freq,chan);
        });
    }

    double source_impl::get_center_freq(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_center_freq(chan) : 0;
    }

    double source_impl::set_freq_corr(double ppm, size_t chan)
    {
        return freq_corr_.set_if_not_equal(ppm, chan,
                                           get_num_channels(),
                                           [this, ppm, chan]
        {
            return device_->set_freq_corr(ppm, chan);
        });

    }

    double source_impl::get_freq_corr(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_center_freq(chan) : 0;
    }

    std::vector<std::string> source_impl::get_gain_names(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain_names( chan ) : std::vector<std::string>{};
    }

    osmosdr::gain_range_t source_impl::get_gain_range(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain_range( chan ) : osmosdr::gain_range_t{};
    }

    osmosdr::gain_range_t source_impl::get_gain_range(const std::string &name, size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain_range( name, chan ) : osmosdr::gain_range_t{};
    }

    bool source_impl::set_gain_mode(bool automatic, size_t chan)
    {
        return gain_mode_.set_if_not_equal(automatic,chan,get_num_channels(),
                                           [this, automatic, chan]
        {
            bool mode = device_->set_gain_mode(automatic,chan);
            if(!automatic)
                device_->set_gain(gain_[chan], chan);
            return mode;
        });
    }

    bool source_impl::get_gain_mode(size_t chan)
    {
        return chan < get_num_channels() &&
                    device_->get_gain_mode(chan);
    }

    double source_impl::set_gain(double gain, size_t chan)
    {
        return gain_.set_if_not_equal(gain,chan, get_num_channels(),
                                      [this,&gain,chan]
        {
            return device_->set_gain(gain,chan);
        });
    }

    double source_impl::set_gain(double gain, const std::string & name, size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->set_gain(gain,name,chan) : 0;
    }

    double source_impl::get_gain(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain(chan) : 0;
    }

    double source_impl::get_gain(const std::string &name, size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain(name, chan) : 0;
    }

    double source_impl::set_if_gain(double gain, size_t chan)
    {
        return 0;
    }

    double source_impl::set_bb_gain(double gain, size_t chan)
    {
        return 0;
    }

    std::vector<std::string> source_impl::get_antennas(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_antennas(chan) : std::vector<std::string>{};
    }

    std::string source_impl::set_antenna(const std::string &antenna, size_t chan)
    {
        return antenna_.set_if_not_equal(antenna,chan,get_num_channels(),
                                         [this, antenna, chan]
        {
           return device_->set_antenna(antenna,chan);
        });
    }

    std::string source_impl::get_antenna(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_antenna(chan) : std::string{};
    }

    void source_impl::set_dc_offset_mode(int mode, size_t chan)
    {
        if(chan < get_num_channels())
        {
            device_->set_dc_offset_mode(mode,chan);
        }
    }

    void source_impl::set_dc_offset(const std::complex<double> &offset, size_t chan)
    {
        if(chan < get_num_channels())
        {
            device_->set_dc_offset(offset,chan);
        }
    }

    void source_impl::set_iq_balance_mode(int mode, size_t chan)
    {
      #ifdef HAVE_IQBALANCE
        size_t channel = 0;
        for (source_iface *dev : _devs) {
          for (size_t dev_chan = 0; dev_chan < dev->get_num_channels(); dev_chan++) {
            if ( chan == channel++ ) {
              if ( chan < _iq_opt.size() && chan < _iq_fix.size() ) {
                gr::iqbalance::optimize_c *opt = _iq_opt[chan];
                gr::iqbalance::fix_cc *fix = _iq_fix[chan];

                if ( IQBalanceOff == mode  ) {
                  opt->set_period( 0 );
                  /* store current values in order to be able to restore them later */
                  _vals[ chan ] = std::pair< float, float >( fix->mag(), fix->phase() );
                  fix->set_mag( 0.0f );
                  fix->set_phase( 0.0f );
                } else if ( IQBalanceManual == mode ) {
                  if ( opt->period() == 0 ) { /* transition from Off to Manual */
                    /* restore previous values */
                    std::pair< float, float > val = _vals[ chan ];
                    fix->set_mag( val.first );
                    fix->set_phase( val.second );
                  }
                  opt->set_period( 0 );
                } else if ( IQBalanceAutomatic == mode ) {
                  opt->set_period( dev->get_sample_rate() / 5 );
                  opt->reset();
                }
              }
            }
          }
        }
      #else
        if(chan < get_num_channels())
        {
            return device_->set_iq_balance_mode( mode, chan );
        }
      #endif
    }

    void source_impl::set_iq_balance(const std::complex<double> &balance, size_t chan)
    {

        #ifdef HAVE_IQBALANCE
          size_t channel = 0;
          for (source_iface *dev : _devs) {
            for (size_t dev_chan = 0; dev_chan < dev->get_num_channels(); dev_chan++) {
              if ( chan == channel++ ) {
                if ( chan < _iq_opt.size() && chan < _iq_fix.size() ) {
                  gr::iqbalance::optimize_c *opt = _iq_opt[chan];
                  gr::iqbalance::fix_cc *fix = _iq_fix[chan];

                  if ( opt->period() == 0 ) { /* automatic optimization desabled */
                    fix->set_mag( balance.real() );
                    fix->set_phase( balance.imag() );
                  }
                }
              }
            }
          }
        #else
        if(chan < get_num_channels())
        {
            return device_->set_iq_balance( balance, chan );
        }
#endif
    }

    double source_impl::set_bandwidth(double bandwidth, size_t chan)
    {
        return bandwidth_.set_if_not_equal(bandwidth, chan,
                                           get_num_channels(),
                                           [this, bandwidth, chan]
        {
            return device_->set_bandwidth(bandwidth,chan);
        });
    }

    double source_impl::get_bandwidth(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_bandwidth( chan ) : 0;
    }

    osmosdr::freq_range_t source_impl::get_bandwidth_range(size_t chan)
    {
        return chan < get_num_channels() ?
            device_->get_bandwidth_range( chan ) : osmosdr::freq_range_t{};
    }
  } /* namespace bladeRF */
} /* namespace gr */

