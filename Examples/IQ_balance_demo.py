# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 14:22:06 2018

@author: jyr_king
"""

import numpy as np
from numpy.fft import rfft,rfftfreq
from math import pi
from matplotlib.pyplot import figure,plot
G_I=1
G_Q=1
G_leakI=0.
G_leakQ=0.
theta=1

N=10001
samplerate=1e9

f_LO= 20*1e6

t=np.arange(N)/samplerate

s_LO=np.cos(2*pi*f_LO*t)+1j*np.sin(2*pi*f_LO*t-theta)

f_IF=1e6

s_IF=G_I*np.cos(2*pi*f_IF*t)-1j*G_Q*np.sin(2*pi*f_IF*t-theta)

s_RF=s_LO.real*s_IF.real+s_LO.imag*s_IF.imag+G_leakI*np.cos(2*pi*f_LO*t)+G_leakQ*np.sin(2*pi*f_LO*t-theta)

s_RF_r=s_RF.real+s_RF.imag
spectr_RF=rfft(s_RF)
freq=rfftfreq(N,1/samplerate)

figure(),plot(freq,np.abs(spectr_RF))
figure(),plot(t,s_RF)