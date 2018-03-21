# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:00:26 2018

@author: SC05
"""
from PyQCLab.Instrument.MWSource import RS_MWSource
from PyQCLab.Instrument.Spcm_Cards import Spcm_AD
from PyQCLab.Instrument.DG645 import DG645
from matplotlib.pyplot import figure,plot
import numpy as np

spad=Spcm_AD(2)
spad.setRangeAll('200mV')
spad.setClockMode('int')
spad.setTrigger(trig_source='ext0',mode='neg',level=1000,coupling='DC',impedance='50Ohm')
spad.setInputAll()
spad.setMode('std_single')
spad.setRecord(1024*10,1,pretrig=32)

mw1=RS_MWSource('SMB100A_0')
mw2=RS_MWSource('SMB100A_1')
mw1.freqency=6e9
mw2.freqency=mw1.freqency+1e6

mw1.level=0
mw2.level=13
mw1.set_output(1)
mw2.set_output(1)
dg=DG645()
dg.delayA=40e-8
dg.delayAB=0.8e-6
dg.trigSource('int')
dg.trigRate(5e3)
#dg.start()

spad.start()
Q,I=spad.getData(0),spad.getData(1)
figure(),plot(I,Q,'o-')

np.savez('IQ_balance_cal_data1',I=I,Q=Q,samplerate=spad.sampleRate)                                                                                                                                                                                                 


