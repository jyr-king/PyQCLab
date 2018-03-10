# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:47:45 2018

@author: jyr_king
"""

import numpy as np
from matplotlib.pyplot import figure,plot
from PyQCLab.Utils.WaveForm_Gen import *
#from PyQCLab.Instrument.pyspcm import KILO
import math

L=1001
samplerate=1e6
w=WaveForm(L,samplerate)
w.base.insert(100,gaussian(100,0.5))
#Add three carrier frequencies to the waveform:
c1=Carrier(L,samplerate,freq=1e5,phase=math.pi*0.5,offset=0.)
c2=Carrier(L,samplerate,freq=0.5e5,phase=math.pi,offset=0.)
c3=Carrier(L,samplerate,freq=1e4,phase=math.pi,offset=0.)
w.carrier.adds([c1,c2,c3])
w.carrier.update()
#Set an offset:
w.carrier.offset=0.3
#update the waveform data:
w.update('spcm4')

figure()
plot(w.waveform)

w2=WaveForm(L,samplerate)
w2.base.inserts(100,(gaussian_r(50,0.5),0.5*gaussian_f(50,0.5)+0.5,0.5*rectangle(200),0.5*gaussian_f(50,0.5)))
w2.base.shift(120)
c4=Carrier(L,samplerate)
c4.frequency=1e5
w2.carrier.add(c4)
w2.carrier.update()
w2.marker1.insert(150,rectangle(30))
w2.marker2.insert(30,rectangle(10))
w2.update('awg5000')

figure()
plot(w2.waveform)
