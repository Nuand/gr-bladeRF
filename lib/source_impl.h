/* -*- c++ -*- */
/*
 * Copyright 2021 Nuand LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_BLADERF_SOURCE_IMPL_H
#define INCLUDED_BLADERF_SOURCE_IMPL_H

#include <bladeRF/source.h>
#include "bladerf/bladerf_source_c.h"
#include "channel_store.h"

namespace gr {
  namespace bladeRF {

    class source_impl : public source
    {
     private:
      bladerf_source_c_sptr device_;
      double sample_rate_;

      channel_store<double> center_freq_;
      channel_store<double> freq_corr_;
      channel_store<double> gain_;
      channel_store<double> if_gain_;
      channel_store<double> bb_gain_;
      channel_store<std::string> antenna_;
      channel_store<double> bandwidth_;

     public:
      source_impl(const std::string & args);
      ~source_impl();

      size_t get_num_channels( void ) override;

      osmosdr::meta_range_t get_sample_rates( void ) override;

      double set_sample_rate( double rate ) override;

      double get_sample_rate( void ) override;

      osmosdr::freq_range_t get_freq_range( size_t chan = 0 ) override;

      double set_center_freq( double freq, size_t chan = 0 ) override;

      double get_center_freq( size_t chan = 0 ) override;

      double set_freq_corr( double ppm, size_t chan = 0 ) override;

      double get_freq_corr( size_t chan = 0 ) override;

      std::vector<std::string> get_gain_names( size_t chan = 0 ) override;

      osmosdr::gain_range_t get_gain_range( size_t chan = 0 ) override;

      osmosdr::gain_range_t get_gain_range( const std::string & name,
                                                    size_t chan = 0 ) override;

      bool set_gain_mode( bool automatic, size_t chan = 0 ) override;

      bool get_gain_mode( size_t chan = 0 ) override;

      double set_gain( double gain, size_t chan = 0 ) override;

      double set_gain( double gain,
                               const std::string & name,
                               size_t chan = 0 ) override;

      double get_gain( size_t chan = 0 ) override;

      double get_gain( const std::string & name, size_t chan = 0 ) override;

      double set_if_gain( double gain, size_t chan = 0 ) override;

      double set_bb_gain( double gain, size_t chan = 0 ) override;

      std::vector< std::string > get_antennas( size_t chan = 0 ) override;

      std::string set_antenna( const std::string & antenna,
                                       size_t chan = 0 ) override;

      std::string get_antenna( size_t chan = 0 ) override;

      enum DCOffsetMode {
        DCOffsetOff = 0,
        DCOffsetManual,
        DCOffsetAutomatic
      };

      void set_dc_offset_mode( int mode, size_t chan = 0) override;

      void set_dc_offset( const std::complex<double> &offset, size_t chan = 0 ) override;

      enum IQBalanceMode {
        IQBalanceOff = 0,
        IQBalanceManual,
        IQBalanceAutomatic
      };

      void set_iq_balance_mode( int mode, size_t chan = 0 ) override;

      void set_iq_balance( const std::complex<double> &balance, size_t chan = 0 ) override;

      double set_bandwidth( double bandwidth, size_t chan = 0 ) override;

      double get_bandwidth( size_t chan = 0 ) override;

      osmosdr::freq_range_t get_bandwidth_range( size_t chan = 0 ) override;

      // Where all the action really happens
   };

 } // namespace bladeRF
} // namespace gr

#endif /* INCLUDED_BLADERF_SOURCE_IMPL_H */

