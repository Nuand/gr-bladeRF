"""
Copyright 2012 Free Software Foundation, Inc.

This file is part of GNU Radio

GNU Radio Companion is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

GNU Radio Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""

MAIN_TMPL = """\
id: ${prefix}_${sourk}
label: '${title} ${sourk.title()}'
category: '[bladeRF]'
flags: throttle

parameters:
- id: type
  label: '${direction.title()}put Type'
  dtype: enum
  options: [fc32]
  option_labels: [Complex Float32]
  option_attributes:
      type: [fc32]
  hide: part
  
- id: metadata
  label: Metadata
  dtype: enum
  default: auto
  options: ['False', 'True']
  hide: part
  
- id: device_id
  label: 'Device'
  dtype: string
  default: '0'
  hide: ${'$'}{ 'none' if device_id else 'part'}
  
- id: nchan
  label: 'Number Channels'
  dtype: int
  default: 1
  options: [ ${", ".join([str(n) for n in range(1, max_nchan+1)])} ]
  
- id: verbosity
  label: 'Verbosity'
  dtype: enum
  default: verbose
  options: ['verbose', 'debug', 'info', 'warning', 'error', 'critical', 'silent']
  option_labels: [verbose, debug, info, warning, error, critical, silent]
  
- id: sample_rate
  label: 'Sample Rate (sps)'
  dtype: real
  default: samp_rate
  
- id: fpga_reload
  label: 'FPGA reload'
  category: Advanced
  dtype: enum
  default: auto
  options: ['False', 'True']
  hide: part
  
- id: fpga_image
  category: Advanced
  label: 'FPGA image'
  dtype: string
  hide: ${'$'}{ 'none' if fpga_reload == 'True' else 'part'}  
    
- id: power_monitoring
  category: Advanced
  label: 'Power monitoring'
  dtype: enum
  default: auto
  options: ['Disable', 'Enable']
  
- id: ref_clk
  category: Advanced
  label: 'Reference clock'
  dtype: real
  
- id: in_clk
  category: Advanced
  label: 'Input clock'
  dtype: enum
  default: auto
  options: ['ONBOARD', 'EXTERNAL']
  option_labels: ['Onboard', 'External']
  
- id: out_clk
  category: Advanced
  label: 'Output clock'
  dtype: enum
  default: False
  options: [False, True]
  option_labels: ['Disable', 'Enable']

- id: dac
  category: Advanced
  label: 'VCXTO DAC'
  dtype: real
  default: 10000

- id: xb200
  category: x40/x115
  label: 'XB-200'
  dtype: enum
  default: 'none'
  options: ['none','auto', 'auto3db', '50M', '144M', '222M', 'custom']
  option_labels: ['none','auto', 'auto3db', '50M', '144M', '222M', 'custom']
  hide: part

- id: tamer
  category: x40/x115
  label: 'Tamer'
  dtype: enum
  default: 'internal'
  options: ['internal','external_1pps', 'external']
  option_labels: ['Internal','External 1pps', 'External 10 MHz']
  hide: part
  
- id: sampling
  category: x40/x115
  label: 'sampling'
  dtype: enum
  default: 'internal'
  options: ['internal', 'external']
  option_labels: ['Internal','External']
  hide: part
  
- id: lpf_mode
  label: 'LPF mode'
  category: x40/x115
  dtype: enum
  default: 'disabled'
  options: ['disabled', 'bypassed']
  option_labels: ['Disabled', 'Bypassed'] 
  hide: part
  
- id: smb
  label: 'SMB frequency'
  category: x40/x115
  dtype: real
  default: 0
  hide: part  
  
- id: dc_calibration
  label: 'DC calibration'
  category: x40/x115
  dtype: enum
  default: 'LPF_TUNING'
  options: ['LPF_TUNING', 'TX_LPF', 'RX_LPF', 'RXVGA2']
  hide: part
  

  

${params}


inputs:
- domain: message
  id: command
  optional: true
  
- domain: message
  id: pmic_in
  optional: true
  
% if sourk == 'source':
outputs:

% endif
- domain: stream
  dtype: ${'$'}{type.type}
  multiplicity: ${'$'}{nchan}
% if sourk == 'sink':
outputs:
- domain: message
  id: async_msgs
  optional: true
% endif

- domain: message
  id: pmic_out
  optional: true




templates:
  imports: |-
     import bladeRF
     import time
  make: |      
    bladeRF.${sourk}(
        args="numchan=" + str(${'$'}{nchan})
             + ",type=" + '${'$'}{type}'
             + ",metadata=" + '${'$'}{metadata}'
             + ",bladerf=" +  str(${'$'}{device_id})
             + ",verbosity=" + '${'$'}{verbosity}'
             + ",fpga=" + str(${'$'}{fpga_image})
             + ",fpga-reload=" + '${'$'}{fpga_reload}'
             + ",power_monitoring=" + '${'$'}{power_monitoring}'
             + ",ref_clk=" + str(int(${'$'}{ref_clk}))
             + ",in_clk=" + '${'$'}{in_clk}'
             + ",out_clk=" + str(${'$'}{out_clk})
             + ",dac=" + str(${'$'}{dac})
             + ",xb200=" + '${'$'}{xb200}'
             + ",tamer=" + '${'$'}{tamer}'
             + ",sampling=" + '${'$'}{sampling}'
             + ",lpf_mode="+'${'$'}{lpf_mode}'
             + ",smb="+str(int(${'$'}{smb}))
             + ",dc_calibration="+'${'$'}{dc_calibration}'
             + ",trigger0="+'${'$'}{trigger0}'
             + ",trigger_role0="+'${'$'}{trigger_role0}'
             + ",trigger_signal0="+'${'$'}{trigger_signal0}'
             + ",trigger1="+'${'$'}{trigger1}'
             + ",trigger_role1="+'${'$'}{trigger_role1}'
             + ",trigger_signal1="+'${'$'}{trigger_signal1}'
             + ",bias_tee0="+'${'$'}{bias_tee0}'
             + ",bias_tee1="+'${'$'}{bias_tee1}'
             
             
    )
    self.${'$'}{id}.set_sample_rate(${'$'}{sample_rate})
    % for n in range(max_nchan):
    ${'%'} if context.get('nchan')() > ${n}:
    self.${'$'}{id}.set_center_freq(${'$'}{${'freq' + str(n)}}, ${n})
    self.${'$'}{id}.set_freq_corr(${'$'}{${'corr' + str(n)}}, ${n})
    % if sourk == 'source':
    self.${'$'}{id}.set_dc_offset_mode(${'$'}{${'dc_offset_mode' + str(n)}}, ${n})
    self.${'$'}{id}.set_iq_balance_mode(${'$'}{${'iq_balance_mode' + str(n)}}, ${n})
    self.${'$'}{id}.set_gain_mode(${'$'}{${'gain_mode' + str(n)}}, ${n})    
    % endif
    self.${'$'}{id}.set_gain(${'$'}{${'gain' + str(n)}}, ${n})
    self.${'$'}{id}.set_if_gain(${'$'}{${'if_gain' + str(n)}}, ${n})
    self.${'$'}{id}.set_bb_gain(${'$'}{${'bb_gain' + str(n)}}, ${n})
    self.${'$'}{id}.set_bandwidth(${'$'}{${'bw' + str(n)}}, ${n})
    ${'%'} endif
    % endfor
  callbacks:
    - set_sample_rate(${'$'}{sample_rate})
    % for n in range(max_nchan):
    - set_center_freq(${'$'}{${'freq' + str(n)}}, ${n})
    - set_freq_corr(${'$'}{${'corr' + str(n)}}, ${n})
    % if sourk == 'source':
    - set_dc_offset_mode(${'$'}{${'dc_offset_mode' + str(n)}}, ${n})
    - set_iq_balance_mode(${'$'}{${'iq_balance_mode' + str(n)}}, ${n})
    - set_gain_mode(${'$'}{${'gain_mode' + str(n)}}, ${n})
    % endif
    - set_gain(${'$'}{${'gain' + str(n)}}, ${n})
    - set_if_gain(${'$'}{${'if_gain' + str(n)}}, ${n})
    - set_bb_gain(${'$'}{${'bb_gain' + str(n)}}, ${n})
    - set_bandwidth(${'$'}{${'bw' + str(n)}}, ${n})
    % endfor

documentation: |-
  The bladeRF ${sourk} block:
  
  Device: 
  Device serial id. If 'device' are not specified, the first available device is used.
  
  Fpga image:  
  Load the FPGA bitstream from the specified file. This is required only once after powering the bladeRF on. If the FPGA is already loaded, this argument is ignored, unless 'fpga-reload=1' is specified.
  
  Enable power monitoring:
  Read value from Power Monitor IC
  
  Reference clock:
  Value of reference clock
  
  Input clock:
  Onboard/external clock.
  
  Output clock:
  Enable/disable clock output.
  
  VCXTO DAC:
  Value to VCTCXO trim DAC  
  
  Num Channels:
  Selects the total number of channels in this multi-device configuration. Required when specifying multiple device arguments.

  Sample Rate:
  The sample rate is the number of samples per second output by this block on each channel.

  Frequency:
  The center frequency is the frequency the RF chain is tuned to.

  Freq. Corr.:
  The frequency correction factor in parts per million (ppm). Set to 0 if unknown.

  % if sourk == 'source':
  DC Offset Mode:
  Controls the behavior of hardware DC offset corrrection.
    Off: Disable correction algorithm (pass through).
    Manual: Keep last estimated correction when switched from Automatic to Manual.
    Automatic: Periodicallly find the best solution to compensate for DC offset.

  This functionality is available for USRP devices only.

  IQ Balance Mode:
  Controls the behavior of software IQ imbalance corrrection.
    Off: Disable correction algorithm (pass through).
    Manual: Keep last estimated correction when switched from Automatic to Manual.
    Automatic: Periodicallly find the best solution to compensate for image signals.

  Gain Mode:
  Chooses between the manual (default) and automatic gain mode where appropriate.
  To allow manual control of RF/IF/BB gain stages, manual gain mode must be configured.
  Currently, only RTL-SDR devices support automatic gain mode.

  % endif
  RF Gain:
  Overall RF gain of the device.

  IF Gain:
  Overall intermediate frequency gain of the device.
  This setting is available for RTL-SDR and OsmoSDR devices with E4000 tuners and HackRF in receive and transmit mode. Observations lead to a reasonable gain range from 15 to 30dB.

  BB Gain:
  Overall baseband gain of the device.
  This setting is available for HackRF in receive mode. Observations lead to a reasonable gain range from 15 to 30dB.

  Bandwidth:
  Set the bandpass filter on the radio frontend. To use the default (automatic) bandwidth filter setting, this should be zero.
  
file_format: 1
"""

# MAIN_TMPL = """\
# <block>
#   <check>$max_nchan >= \$nchan</check>
#   <check>\$nchan > 0</check>
# </block>
# """

PARAMS_TMPL = """
- id: freq${n}
  category: 'Channel ${n}'
  label: 'Center frequency (Hz)'
  dtype: real
  default: 1e8
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'} 
  
- id: corr${n}
  category: 'Channel ${n}'
  label: 'Frequency Correction (ppm)'
  dtype: real
  default: 0
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'} 
   
- id: bw${n}
  category: 'Channel ${n}'
  label: 'Bandwidth (Hz)'
  dtype: real
  default: 200000
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}  
  
- id: bias_tee${n}
  category: 'Channel ${n}'
  label: 'Bias tee'
  dtype: bool
  default: False
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}  
  
% if sourk == 'source':
- id: dc_offset_mode${n}
  category: 'Channel ${n}'
  label: 'DC Offset Mode'
  dtype: int
  default: 0
  options: [0, 1, 2]  
  option_labels: [Off, Manual, Automatic]
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
  
- id: iq_balance_mode${n}
  category: 'Channel ${n}'
  label: 'IQ Balance Mode'
  dtype: int
  default: 0
  options: [0, 1, 2]
  option_labels: [Off, Manual, Automatic]
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
  
- id: gain_mode${n}
  category: 'Channel ${n}'
  label: 'Gain Mode'
  dtype: bool
  default: False
  options: [False, True]
  option_labels: [Manual, Automatic]
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
% endif

- id: gain${n}
  category: 'Channel ${n}'
  label: 'RF Gain (dB)'
  dtype: real
  default: 10
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
  
- id: if_gain${n}
  category: 'Channel ${n}'
  label: 'IF Gain (dB)'
  dtype: real
  default: 20
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
  
- id: bb_gain${n}
  category: 'Channel ${n}'
  label: 'BB Gain (dB)'
  dtype: real
  default: 20
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
  
- id: trigger${n}
  label: 'Use trigger'
  category: 'Channel ${n}' 
  dtype: enum
  default: 'False'
  options: ['False', 'True']
  hide: ${'$'}{'part' if (nchan > ${n}) else 'all'}

- id: trigger_role${n}
  label: Trigger role
  category: 'Channel ${n}'
  dtype: enum
  options: ['master', 'slave']
  option_labels: [master, slave] 
  hide: ${'$'}{ 'part' if (nchan > ${n}) else 'all'} 
  
- id: trigger_signal${n}
  label: Trigger signal
  category: 'Channel ${n}'
  dtype: enum
  default: 'J51_1'
  options: ['J71_4', 'J51_1', 'MINI_EXP_1', 'USER_0', 'USER_1', 'USER_2', 'USER_3', 'USER_4', 'USER_5', 'USER_6', 'USER_7']
  option_labels: ['J71_4', 'J51_1', 'MINI_EXP_1', 'USER_0', 'USER_1', 'USER_2', 'USER_3', 'USER_4', 'USER_5', 'USER_6', 'USER_7'] 
  hide: ${'$'}{ 'part' if (nchan > ${n})  else 'all'} 
  

  
"""


def parse_tmpl(_tmpl, **kwargs):
    from mako.template import Template
    from mako import exceptions

    try:
        block_template = Template(_tmpl)
        return str(block_template.render(**kwargs))
    except:
        print(exceptions.text_error_template().render())

MAX_NUM_CHANNELS = 2

import os.path

if __name__ == '__main__':
    import sys

    for file in sys.argv[1:]:
        head, tail = os.path.split(file)

        if tail.startswith('bladeRF'):
            title = 'bladeRF'
            prefix = 'bladeRF'
        else:
            raise Exception("file {} has wrong syntax!".format(tail))


        if tail.endswith('source.block.yml'):
            sourk = 'source'
            direction = 'out'
        elif tail.endswith('sink.block.yml'):
            sourk = 'sink'
            direction = 'in'
        else:
            raise Exception("is {} a source or sink?".format(file))

        params = ''.join([
            parse_tmpl(PARAMS_TMPL, n=n, sourk=sourk)
            for n in range(MAX_NUM_CHANNELS)
        ])

        open(file, 'w').write(
            parse_tmpl(
                MAIN_TMPL,
                max_nchan=MAX_NUM_CHANNELS,
                params=params,
                title=title,
                prefix=prefix,
                sourk=sourk,
                direction=direction,
            )
        )
