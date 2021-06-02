/* -*- c++ -*- */
/*
 * Copyright 2021 Nuand LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "sink_impl.h"
#include "arg_helpers.h"

namespace gr {
  namespace bladeRF {

    sink::sptr sink::make(const std::string & args)
    {
      return gnuradio::make_block_sptr<sink_impl>(args);
    }


    /*
     * The private constructor
     */
    sink_impl::sink_impl(const std::string & args)
      : gr::hier_block2("sink_impl",
                        args_to_io_signature(args),
                        gr::io_signature::make(0, 0, 0))
      , sample_rate_(0)
    {
        auto dev_list = bladerf_sink_c::get_devices();
        if(dev_list.size() == 0)
            throw std::runtime_error("No supported devices found "
                                     "(check the connection and/or udev rules).");

        device_ = make_bladerf_sink_c( args ); //todo: get by id from block args
    }

    /*
     * Our virtual destructor.
     */
    sink_impl::~sink_impl()
    {
    }

    size_t sink_impl::get_num_channels()
    {
        return device_ ? device_->get_num_channels() : 0;
    }

    osmosdr::meta_range_t sink_impl::get_sample_rates()
    {
        return device_ ? device_->get_sample_rates() : osmosdr::meta_range_t{};
    }

    double sink_impl::set_sample_rate(double rate)
    {
        if(rate != sample_rate_)
        {
            sample_rate_  = device_ ? device_->set_sample_rate(rate) : 0;
        }
        return sample_rate_;
    }

    double sink_impl::get_sample_rate()
    {
        return device_ ? device_->get_sample_rate() : 0;
    }

    osmosdr::freq_range_t sink_impl::get_freq_range(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_freq_range(chan) : osmosdr::freq_range_t{};
    }

    double sink_impl::set_center_freq(double freq, size_t chan)
    {
        return center_freq_.set_if_not_equal(freq,
                                             chan,
                                             get_num_channels(),
                                             [this,freq,chan]{
            return device_->set_center_freq(freq,chan);
        });
    }

    double sink_impl::get_center_freq(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_center_freq(chan) : 0;
    }

    double sink_impl::set_freq_corr(double ppm, size_t chan)
    {
        return freq_corr_.set_if_not_equal(ppm, chan,
                                           get_num_channels(),
                                           [this, ppm, chan]
        {
            return device_->set_freq_corr(ppm, chan);
        });

    }

    double sink_impl::get_freq_corr(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_center_freq(chan) : 0;
    }

    std::vector<std::string> sink_impl::get_gain_names(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain_names( chan ) : std::vector<std::string>{};
    }

    osmosdr::gain_range_t sink_impl::get_gain_range(size_t chan)
    {
        return chan < get_num_channels() ? device_->get_gain_range( chan )
                                         : osmosdr::gain_range_t{};
    }

    osmosdr::gain_range_t sink_impl::get_gain_range(const std::string &name,
                                                    size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain_range( name, chan ) : osmosdr::gain_range_t{};
    }

    bool sink_impl::set_gain_mode(bool automatic, size_t chan)
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

    bool sink_impl::get_gain_mode(size_t chan)
    {
        return chan < get_num_channels() &&
                    device_->get_gain_mode(chan);
    }

    double sink_impl::set_gain(double gain, size_t chan)
    {
        return gain_.set_if_not_equal(gain,chan, get_num_channels(),
                                      [this,&gain,chan]
        {
            return device_->set_gain(gain,chan);
        });
    }

    double sink_impl::set_gain(double gain, const std::string &name, size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->set_gain(gain,name,chan) : 0;
    }

    double sink_impl::get_gain(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain(chan) : 0;
    }

    double sink_impl::get_gain(const std::string &name, size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_gain(chan) : 0;
    }

    double sink_impl::set_if_gain(double gain, size_t chan)
    {
        return 0;
    }

    double sink_impl::set_bb_gain(double gain, size_t chan)
    {
        return 0;
    }

    std::vector<std::string> sink_impl::get_antennas(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_antennas(chan) : std::vector<std::string>{};
    }

    std::string sink_impl::set_antenna(const std::string &antenna, size_t chan)
    {
        return antenna_.set_if_not_equal(antenna,chan,get_num_channels(),
                                         [this, antenna, chan]
        {
           return device_->set_antenna(antenna,chan);
        });
    }

    std::string sink_impl::get_antenna(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_antenna(chan) : std::string{};
    }

    void sink_impl::set_dc_offset(const std::complex<double> &offset, size_t chan)
    {
        if(chan < get_num_channels())
        {
            device_->set_dc_offset(offset, chan);
        }
    }

    void sink_impl::set_iq_balance(const std::complex<double> &balance, size_t chan)
    {
        if(chan < get_num_channels())
        {
            device_->set_iq_balance(balance, chan);
        }
    }

    double sink_impl::set_bandwidth(double bandwidth, size_t chan)
    {
        return bandwidth_.set_if_not_equal(bandwidth, chan,
                                           get_num_channels(),
                                           [this, bandwidth, chan]
        {
            return device_->set_bandwidth(bandwidth,chan);
        });
    }

    double sink_impl::get_bandwidth(size_t chan)
    {
        return chan < get_num_channels() ?
                    device_->get_bandwidth( chan ) : 0;
    }

    osmosdr::freq_range_t sink_impl::get_bandwidth_range(size_t chan)
    {
        return chan < get_num_channels() ? device_->get_bandwidth_range(chan)
                                         : osmosdr::freq_range_t{};
    }

    void sink_impl::set_clock_source(const std::string &source,
                                     const size_t mboard)
    {
        if (device_)
            device_->set_clock_source(source, mboard);
    }

    std::string sink_impl::get_clock_source(const size_t mboard)
    {
        return device_ ? device_->get_clock_source(mboard) : std::string{};
    }

    std::vector<std::string> sink_impl::get_clock_sources(const size_t mboard)
    {
        return device_ ? device_->get_clock_sources(mboard)
                       : std::vector<std::string>{};
    }

  } /* namespace bladeRF */
} /* namespace gr */

