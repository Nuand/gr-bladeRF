/* -*- c++ -*- */
/*
 * Copyright 2021 Nuand LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_BLADERF_SOURCE_H
#define INCLUDED_BLADERF_SOURCE_H

#include <bladeRF/api.h>
#include <gnuradio/hier_block2.h>

namespace gr {
  namespace bladeRF {

    /*!
     * \brief <+description of block+>
     * \ingroup bladeRF
     *
     */
    class BLADERF_API source : virtual public gr::hier_block2
    {
     public:
      typedef std::shared_ptr<source> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of bladeRF::source.
       *
       * To avoid accidental use of raw pointers, bladeRF::source's
       * constructor is in a private implementation
       * class. bladeRF::source::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::string & args);
    };

  } // namespace bladeRF
} // namespace gr

#endif /* INCLUDED_BLADERF_SOURCE_H */

