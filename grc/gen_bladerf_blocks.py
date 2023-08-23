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

- id: fpga_reload
  label: 'FPGA reload'
  dtype: enum
  default: auto
  options: ['False', 'True']
  hide: part
  
- id: fpga_image
  label: 'FPGA image'
  dtype: string
  hide: ${'$'}{ 'none' if fpga_reload == 'True' else 'part'}  
  
- id: nchan
  label: 'Num Channels'
  dtype: int
  default: 1
  options: [ ${", ".join([str(n) for n in range(1, max_nchan+1)])} ]
  
- id: verbosity
  label: 'Verbosity'
  dtype: enum
  default: verbose
  options: ['verbose', 'debug', 'info', 'warning', 'error', 'critical', 'silent']
  option_labels: [verbose, debug, info, warning, error, critical, silent]

- id: feature
  label: 'Feature'
  dtype: enum
  default: default
  options: ['default', 'oversample']
  option_labels: [Default, Oversample]

- id: sample_format
  label: 'Sample Format'
  dtype: enum
  default: 16bit
  options: ['16bit', '8bit']
  option_labels: [16bit, 8bit]
  
- id: sample_rate
  label: 'Sample Rate (sps)'
  dtype: real
  default: samp_rate
  
- id: freq
  label: 'Frequency (Hz)'
  dtype: real
  default: 1e8
  
- id: bw
  label: 'Bandwidth (Hz)'
  dtype: real
  default: 200000
   
- id: use_ref_clk
  label: 'Use reference clock'
  dtype: enum
  default: False
  options: ['False', 'True']
  hide: part

- id: ref_clk
  label: 'Reference clock'
  dtype: real
  default: 10e6
  hide: ${'$'}{ 'none' if use_ref_clk == 'True' else 'part'}
  
- id: buflen
  label: 'Buffer Size'
  dtype: real
  default: 4096
  hide: ${'$'}{ 'none' if use_ref_clk == 'True' else 'part'}

- id: buffers
  label: 'Number of Buffers'
  dtype: real
  default: 512
  hide: ${'$'}{ 'none' if use_ref_clk == 'True' else 'part'}

- id: in_clk
  label: 'Input clock'
  dtype: enum
  default: auto
  options: ['ONBOARD', 'EXTERNAL']
  option_labels: ['Onboard', 'External']
  
- id: out_clk
  label: 'Output clock'
  dtype: enum
  default: False
  options: [False, True]
  option_labels: ['Disable', 'Enable']
  
- id: use_dac
  label: 'Use VCXTO DAC'
  dtype: enum
  default: False
  options: ['False', 'True']
  hide: part
  
- id: dac
  label: 'VCXTO DAC'
  dtype: real
  default: 10000
  hide: ${'$'}{ 'none' if use_dac == 'True' else 'part'} 
  
- id: show_pmic
  label: 'Show PMIC controls'
  dtype: enum
  default: False
  options: ['False', 'True']
  hide: part  
  

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
  label: 'Sampling'
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
  default: 38.4e6
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
  id: pmic_in
  optional: true
  hide: ${'$'}{show_pmic == 'False'}
  
% if sourk == 'source':
outputs:

% endif
- domain: stream
  dtype: ${'$'}{type.type}
  multiplicity: ${'$'}{nchan}
% if sourk == 'sink':
outputs:
% endif

- domain: message
  id: pmic_out
  optional: true
  hide: ${'$'}{show_pmic == 'False'}
  
templates:
  imports: |-
     import bladeRF
     import time
  make: |      
    bladeRF.${sourk}(
        args="numchan=" + str(${'$'}{nchan})
             + ",metadata=" + '${'$'}{metadata}'
             + ",bladerf=" +  str(${'$'}{device_id})
             + ",verbosity=" + '${'$'}{verbosity}'
             + ",feature=" + '${'$'}{feature}'
             + ",sample_format=" + '${'$'}{sample_format}'
             + ",fpga=" + str(${'$'}{fpga_image})
             + ",fpga-reload=" + '${'$'}{fpga_reload}'
             + ",use_ref_clk=" + '${'$'}{use_ref_clk}'
             + ",ref_clk=" + str(int(${'$'}{ref_clk}))
             + ",buflen=" + str(int(${'$'}{buflen}))
             + ",buffers=" + str(int(${'$'}{buffers}))
             + ",in_clk=" + '${'$'}{in_clk}'
             + ",out_clk=" + str(${'$'}{out_clk})
             + ",use_dac=" + '${'$'}{use_dac}'
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
    self.${'$'}{id}.set_center_freq(${'$'}{freq},0)
    self.${'$'}{id}.set_bandwidth(${'$'}{bw},0)
    % for n in range(max_nchan):
    ${'%'} if context.get('nchan')() > ${n}:    
    % if sourk == 'source':
    self.${'$'}{id}.set_dc_offset_mode(${'$'}{${'dc_offset_mode' + str(n)}}, ${n})
    self.${'$'}{id}.set_iq_balance_mode(${'$'}{${'iq_balance_mode' + str(n)}}, ${n})
    self.${'$'}{id}.set_gain_mode(${'$'}{${'gain_mode' + str(n)}}, ${n})    
    % endif
    self.${'$'}{id}.set_gain(${'$'}{${'gain' + str(n)}}, ${n})
    self.${'$'}{id}.set_if_gain(${'$'}{${'if_gain' + str(n)}}, ${n})    
    ${'%'} endif
    % endfor
  callbacks:
    - set_sample_rate(${'$'}{sample_rate})
    - set_center_freq(${'$'}{freq}, 0)
    - set_bandwidth(${'$'}{bw}, 0)
    % for n in range(max_nchan):    
    % if sourk == 'source':
    - set_dc_offset_mode(${'$'}{${'dc_offset_mode' + str(n)}}, ${n})
    - set_iq_balance_mode(${'$'}{${'iq_balance_mode' + str(n)}}, ${n})
    - set_gain_mode(${'$'}{${'gain_mode' + str(n)}} == True, ${n})
    % endif
    - set_gain(${'$'}{${'gain' + str(n)}}, ${n})
    - set_if_gain(${'$'}{${'if_gain' + str(n)}}, ${n})
    % endfor

documentation: |-
  The bladeRF ${sourk} block:
  
  Device: 
  Device serial id. If 'device' are not specified, the first available device is used.
  
  Metadata:
  Provide metadata with samples
  
  FPGA reload:
  Reload reload FPGA image by 'FPGA image' path.
  
  FPGA image:  
  Load the FPGA bitstream from the specified file. This is required only once after powering the bladeRF on. If the FPGA is already loaded, this argument is ignored, unless FPGA reload is True.
  
  Num Channels:
  Selects the total number of channels in this multi-device configuration. Required when specifying multiple device arguments.

  Verbosity:
  Sets the filter level for displayed log messages.

  Feature:
  Sets an availble bladeRF device feature.

  Sample Format:
  Sets the sample format to either 16bit or 8bit.
  8bit mode allows for a faster sampling rate.
  
  Sample Rate:
  The sample rate is the number of samples per second output by this block on each channel.
  
  Reference clock:
  Value of reference clock
  
  Input clock:
  Onboard/external clock.
  
  Output clock:
  Enable/disable clock output.
  
  VCXTO DAC:
  Value to VCTCXO trim DAC  
  
  x40/x115 Specific:
    XB-200:
    Select XB-200 filterbank.
    
    Tamer:
    Select tamer mode.
    
    Sampling:
    Configure the sampling of the LMS6002D to be either internal or external.
    Internal sampling will read from the RXVGA2 driver internal to the chip. External sampling will connect the ADC inputs to the external inputs for direct sampling.
    
    LPF mode:
    Set the LMS LPF mode to bypass or disable it.
    
    SMB frequency:
    Set the SMB connector output frequency in Hz. This function inherently configures the SMB clock port as an output. 
    
    DC calibration:
    Perform DC calibration.
    
  
  For each channel:
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

  AGC:
  Chooses between the manual (False) and automatic (True) gain mode where appropriate.
  To allow manual control of RF/IF gain stages, manual gain mode must be configured.

  % endif
  RF Gain:
  Overall RF gain of the device.

  IF Gain:
  Overall intermediate frequency gain of the device.
  This setting is available for RTL-SDR and OsmoSDR devices with E4000 tuners and HackRF in receive and transmit mode. Observations lead to a reasonable gain range from 15 to 30dB.

  Bandwidth:
  Set the bandpass filter on the radio frontend. To use the default (automatic) bandwidth filter setting, this should be zero.
  
  Use trigger:
  Enable trigger functionality
  
  Trigger role:
  Set trigger role (master/slave) for channel
  
  Trigger signal:
  This selects pin or signal used for the trigger.
  
file_format: 1
"""

# MAIN_TMPL = """\
# <block>
#   <check>$max_nchan >= \$nchan</check>
#   <check>\$nchan > 0</check>
# </block>
# """

PARAMS_TMPL = """
- id: bias_tee${n}
  category: 'Channel ${n}'
  label: 'Bias tee'
  dtype: enum
  default: 'False'
  options: ['False', 'True']
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
  label: 'AGC'
  dtype: enum
  default: 'False'
  options: ['False', 'True']
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
