# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 21:56:33 2017

@author: A108QCLab
"""

import numpy as np
from pylab import *
from time import sleep
#from PyQCLab.Instrument.AlazarDefs import *
from PyQCLab.Instrument.digitizer_v2 import *
#from PyQCLab.Instrument.DataAcquisition import *
#%%
ad1=digitizer()
#ad1.set_captureclock(timebase='EXT_10MHz_REF')
ad1.set_inputcontrol()
ad1.set_triggeroperation(trigsourcej='TRIG_EXT',triglevelj=135,trigslopej='NEG')
ad1.set_externaltrigger(coupling='AC')
ad1.set_triggermisc()
ad1.mode='NPT'
#%%
ad1.samplerate=1.8e9
ad1.set_captureclock(timebase='EXT_10MHz_REF')
ad1.recordlength=100000
#ad1.acqlength=10240
ad1.records=12
ad1.start()
sleep(1)
data=ad1.data
#plot(data[0])
plot(1/ad1.samplerate*np.arange(len(data[0])),data[0])

