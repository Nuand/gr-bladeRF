#pragma once
#include <gnuradio/hier_block2.h>

class common_hier_block: public gr::hier_block2
{
public:
   common_hier_block(const std::string& name,
               gr::io_signature::sptr input_signature,
               gr::io_signature::sptr output_signature)
               : gr::hier_block2(name, input_signature, output_signature)
   {
   }
   void setup_message_ports()
   {
        message_port_register_hier_in(pmt::mp("pmic_in"));
        message_port_register_hier_out(pmt::mp("pmic_out"));

   }
   template<typename T>
   void setup_device_connects(T device)
   {
        msg_connect(self(), pmt::mp("pmic_in"), device, pmt::mp("pmic_in"));
        msg_connect(device,pmt::mp("pmic_out"), self(), pmt::mp("pmic_out"));
   }
   
   
};
