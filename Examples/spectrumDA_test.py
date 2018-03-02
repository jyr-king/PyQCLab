# -*- coding: utf-8 -*-
"""
Created on Mon May  8 17:26:26 2017
example and test scripts for Spectrum's M4ixx series DA cards.
@author: A108QCLab
"""
#%%
import numpy as np
from pylab import *
#from time import sleep
from PyQCLab.Utils.WaveForm_v2 import *
from PyQCLab.Instrument.spcmDA import *
from PyQCLab.Instrument.pyspcm import *
#%%
da1=spectrumDA(0)
da1.level0=200
da1.level0
da1.level1=888
da1.level1
#da1.chEnable((1,))
#da1.output(1)
da1.chEnable((0,1))
da1.output(0)
da1.output(1)
da1.runmode='single_r'
da1.setTriggerSource('ext0')
da1.setTriggerMode()
da1.setClockMode('int')

#%%
length=KILO_B(64)
w1=WaveForm(length,AWGType='spcm4')
w2=WaveForm(length,AWGType='spcm4')
w1.createBase('sin')
#w1.createWindow((('kaiser',10,100,14),))
w2.createWindow((('gaussian_half',10,110,20),('rectangle',110,5100)))
w1.createWaveform()
w2.createWaveform()
data=np.array([w1.waveform,w2.waveform]).flatten('F')
#%%
da1.writeWaveForm(data)
#%%
da1.start()
da1.stop()
da1.closeCard()
da1.setTriggerSource('sw')
