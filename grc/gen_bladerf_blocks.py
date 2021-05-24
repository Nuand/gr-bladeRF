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
  
- id: args
  label: 'Device Arguments'
  dtype: string
  default: '""'
  hide: ${'$'}{ 'none' if args else 'part'}
  
- id: sync
  label: Sync
  dtype: enum
  options: [sync, pc_clock, none]
  option_labels: [Unknown PPS, PC Clock, Don't Sync]
  hide: ${'$'}{ 'none' if sync else 'part'}
  
- id: num_mboards
  label: 'Number MBoards'
  dtype: int
  default: 1
  options: [ ${", ".join([str(n) for n in range(1, max_mboards+1)])} ]
  hide: part
% for m in range(max_mboards):
- id: clock_source${m}
  label: 'MB${m}: Clock Source'
  dtype: string
  options: ['', internal, external, external_1pps, mimo, gpsdo]
  option_labels: [Default, Internal, External, External 1PPS, MIMO Cable, O/B GPSDO]
  hide: ${'$'}{ 'all' if not (num_mboards > ${m}) else ( 'none' if clock_source${m} else 'part' )}
- id: time_source${m}
  label: 'MB${m}: Time Source'
  dtype: string
  options: ['', external, mimo, gpsdo]
  option_labels: [Default, External, MIMO Cable, O/B GPSDO]
  hide: ${'$'}{ 'all' if not (num_mboards > ${m}) else ( 'none' if time_source${m} else 'part' )}  
% endfor

- id: nchan
  label: 'Number Channels'
  dtype: int
  default: 1
  options: [ ${", ".join([str(n) for n in range(1, max_nchan+1)])} ]
  
- id: sample_rate
  label: 'Sample Rate (sps)'
  dtype: real
  default: samp_rate
  
- id: fpga_image
  label: 'FPGA image'
  dtype: string
  
- id: bias_tee
  label: 'Bias tee'
  dtype: bool
  default: False
  
- id: xb_200
  label: 'XB-200'
  dtype: enum
  default: auto
  options: ['auto', 'auto3db', '50M', '144M', '222M', 'custom']
  option_labels: [auto, auto3db, 50M, 144M, 222M, custom]
  
- id: power_monitoring
  label: 'Enable power monitoring'
  dtype: bool
  default: False
 
- id: ref_clk
  label: 'Reference clock'
  dtype: real
  
- id: in_clk
  label: 'Input clock'
  dtype: enum
  default: auto
  options: ['ONBOARD', 'EXTERNAL']
  option_labels: ['ONBOARD', 'EXTERNAL']
  
- id: out_clk
  label: 'Output clock'
  dtype: bool
  default: False


${params}

inputs:
- domain: message
  id: command
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

templates:
  imports: |-
     import bladerf
     import time
  make: |
    bladerf.${sourk}(
        args="numchan=" + str(${'$'}{nchan}) + " " + ${'$'}{args}
    )
    % for m in range(max_mboards):
    ${'%'} if context.get('num_mboards')() > ${m}:
    ${'%'} if context.get('clock_source${m}')():
    self.${'$'}{id}.set_clock_source(${'$'}{${'clock_source' + str(m)}}, ${m})
    ${'%'} endif
    ${'%'} if context.get('time_source${m}')():
    self.${'$'}{id}.set_time_source(${'$'}{${'time_source' + str(m)}}, ${m})
    ${'%'} endif
    ${'%'} endif
    % endfor
    ${'%'} if sync == 'sync':
    self.${'$'}{id}.set_time_unknown_pps(osmosdr.time_spec_t())
    ${'%'} elif sync == 'pc_clock':
    self.${'$'}{id}.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
    ${'%'} endif
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
    self.${'$'}{id}.set_antenna(${'$'}{${'ant' + str(n)}}, ${n})
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
    - set_antenna(${'$'}{${'ant' + str(n)}}, ${n})
    - set_bandwidth(${'$'}{${'bw' + str(n)}}, ${n})
    % endfor

documentation: |-
  The bladeRF ${sourk} block:


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

  This functionality depends on http://cgit.osmocom.org/cgit/gr-iqbal/

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

  Antenna:
  For devices with only one antenna, this may be left blank.
  Otherwise, the user should specify one of the possible antenna choices.

  Bandwidth:
  Set the bandpass filter on the radio frontend. To use the default (automatic) bandwidth filter setting, this should be zero.
  
file_format: 1
"""

# MAIN_TMPL = """\
# <block>
#   <check>$max_nchan >= \$nchan</check>
#   <check>\$nchan > 0</check>
#   <check>$max_mboards >= \$num_mboards</check>
#   <check>\$num_mboards > 0</check>
#   <check>\$nchan >= \$num_mboards</check>
# </block>
# """

PARAMS_TMPL = """
- id: freq${n}
  label: 'Ch${n}: Frequency (Hz)'
  dtype: real
  default: 100e6
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
- id: corr${n}
  label: 'Ch${n}: Frequency Correction (ppm)'
  dtype: real
  default: 0
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
% if sourk == 'source':
- id: dc_offset_mode${n}
  label: 'Ch${n}: DC Offset Mode'
  dtype: int
  default: 0
  options: [0, 1, 2]
  option_labels: [Off, Manual, Automatic]
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
- id: iq_balance_mode${n}
  label: 'Ch${n}: IQ Balance Mode'
  dtype: int
  default: 0
  options: [0, 1, 2]
  option_labels: [Off, Manual, Automatic]
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
- id: gain_mode${n}
  label: 'Ch${n}: Gain Mode'
  dtype: bool
  default: False
  options: [False, True]
  option_labels: [Manual, Automatic]
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
% endif
- id: gain${n}
  label: 'Ch${n}: RF Gain (dB)'
  dtype: real
  default: 10
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
- id: if_gain${n}
  label: 'Ch${n}: IF Gain (dB)'
  dtype: real
  default: 20
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
- id: bb_gain${n}
  label: 'Ch${n}: BB Gain (dB)'
  dtype: real
  default: 20
  hide: ${'$'}{'none' if (nchan > ${n}) else 'all'}
- id: ant${n}
  label: 'Ch${n}: Antenna'
  dtype: string
  default: ""
  hide: ${'$'}{'all' if not (nchan > ${n}) else ('none' if eval('ant' + str(${n})) else 'part')}
- id: bw${n}
  label: 'Ch${n}: Bandwidth (Hz)'
  dtype: real
  default: 0
  hide: ${'$'}{'all' if not (nchan > ${n}) else ('none' if eval('bw' + str(${n})) else 'part')}
"""


def parse_tmpl(_tmpl, **kwargs):
    from mako.template import Template
    from mako import exceptions

    try:
        block_template = Template(_tmpl)
        return str(block_template.render(**kwargs))
    except:
        print(exceptions.text_error_template().render())

MAX_NUM_MBOARDS = 8
MAX_NUM_CHANNELS = MAX_NUM_MBOARDS * 4

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
                max_mboards=MAX_NUM_MBOARDS,
                params=params,
                title=title,
                prefix=prefix,
                sourk=sourk,
                direction=direction,
            )
        )
