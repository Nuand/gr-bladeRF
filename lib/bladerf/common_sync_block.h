#pragma once
#include <gnuradio/sync_block.h>
#include "bladerf_common.h"

class common_sync_block: public gr::sync_block, public bladerf_common
{
public:
   common_sync_block(const std::string& name,
               gr::io_signature::sptr input_signature,
               gr::io_signature::sptr output_signature)
               : gr::sync_block(name, input_signature, output_signature)
   {
   }
   void setup_blade_messaging()
   {
        message_port_register_in(pmt::mp("pmic_in"));
        message_port_register_in(pmt::mp("fire"));
        message_port_register_out(pmt::mp("pmic_out"));

        set_msg_handler(pmt::mp("pmic_in"),[=](const pmt::pmt_t & msg)
        {
            auto type = pmt::symbol_to_string(msg);
            auto value = get_pmic_value(type);
            auto pair = pmt::cons(msg,pmt::string_to_symbol(value));
            message_port_pub(pmt::mp("pmic_out"), pair);

        });
        set_msg_handler(pmt::mp("fire"),[=](const pmt::pmt_t & msg)
        {
            fire_trigger();
        });
   }
};


