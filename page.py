#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Pocsagtx
# Author: Jake Drahos
# Description: POCSAG TX Tweaked for SecDSM
# Generated: Fri Nov 17 02:03:54 2017
##################################################

### Set your callsign!!!
#call = 'W0XYZ'
raise Exception("Make sure you're legal!")

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from optparse import OptionParser
import math
import mixalot
import osmosdr

import sys


class pocsagtx(gr.top_block):

    def __init__(self, capcode, message):
        gr.top_block.__init__(self, "Pocsagtx")

        ##################################################
        # Variables
        ##################################################
        self.symrate = symrate = 38400
        self.samp_rate = samp_rate = 5000000
        ### Set the frequency!
        #self.pagerfreq = pagerfreq = 421000000
        raise Exception("Make sure you're legal!")

        ### Set to 2500.0 for narrowband
        self.max_deviation = max_deviation = 4500.0

        ##################################################
        # Blocks
        ##################################################
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  float(samp_rate)/float(symrate),
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        	
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1))
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(pagerfreq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.mixalot_pocencode_0 = mixalot.pocencode(1, 512, capcode, message, symrate)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.7, ))
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2.0 * math.pi * max_deviation / float(symrate))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_char_to_float_0, 0), (self.analog_frequency_modulator_fc_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))    
        self.connect((self.mixalot_pocencode_0, 0), (self.blocks_char_to_float_0, 0))    
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))    

    def get_symrate(self):
        return self.symrate

    def set_symrate(self, symrate):
        self.symrate = symrate
        self.analog_frequency_modulator_fc_0.set_sensitivity(2.0 * math.pi * self.max_deviation / float(self.symrate))
        self.pfb_arb_resampler_xxx_0.set_rate(float(self.samp_rate)/float(self.symrate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(float(self.samp_rate)/float(self.symrate))

    def get_pagerfreq(self):
        return self.pagerfreq

    def set_pagerfreq(self, pagerfreq):
        self.pagerfreq = pagerfreq
        self.osmosdr_sink_0.set_center_freq(self.pagerfreq, 0)

    def get_max_deviation(self):
        return self.max_deviation

    def set_max_deviation(self, max_deviation):
        self.max_deviation = max_deviation
        self.analog_frequency_modulator_fc_0.set_sensitivity(2.0 * math.pi * self.max_deviation / float(self.symrate))


def main(top_block_cls=pocsagtx, options=None):

    # Prepend callsign to identify
    message = call + "\n" + options["message"]
    tb = top_block_cls(options["capcode"], message)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: page.py <capcode> <message>")
        exit(-1)

    main(options={"capcode":int(sys.argv[1]), "message":sys.argv[2]})
