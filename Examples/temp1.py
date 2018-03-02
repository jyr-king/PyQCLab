# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 11:43:39 2018

@author: SC05
"""

from PyQCLab.Instrument.NetworkAnalyser import *
from PyQCLab.Instrument.DCSources import GS200
from PyQCLab.Instrument.MWSource import RS_MWSource
from time import sleep
import numpy as np
from pylab import *

from scipy.optimize import leastsq,curve_fit
import skrf as rf

def fit_linearPhase(x,a,b):
    return a*x+b

na=ZNB20()
dc=GS200()

na.set_sweep(4e9,7e9,1000,5001,1)
na.average=1
swp_time=na.points/na.IFbandwidth*na.average
na.power=-12

dc.mode='V'
dc.range=1
dc.level=0
dc.output=0

na.sweep()
sleep(swp_time)
freq,Sdata=na.getData()
angS=np.unwrap(np.angle(Sdata))
popt,pcov=curve_fit(fit_linearPhase,freq[:1000],angS[:1000])

bias=np.linspace(-0.9,0.9,21)
angS_n=np.zeros((bias.size,freq.size))

#powers=np.linspace(0,15,5)
#%%
dc.level=0
dc.output=1
for i in range(bias.size):
    dc.level=bias[i]
    na.sweep()
    sleep(swp_time)
    freq,Sdata=na.getData()
    angS=np.unwrap(np.angle(Sdata))
    angS_n[i,:]=angS-(popt[0]*freq+popt[1])
dc.output=0
figure() 
X,Y=np.meshgrid(bias,freq)   
pcolor(X,Y,angS_n.T)

#%%
na.set_sweep(4e9,7e9,1000,2001,1)
na.average=1
swp_time=na.points/na.IFbandwidth*na.average

dc.output=0

na.sweep()
sleep(swp_time)
freq,Sdata=na.getData()
angS=np.unwrap(np.angle(Sdata))
popt,pcov=curve_fit(fit_linearPhase,freq[:200],angS[:200])

powers=np.linspace(-10,10,41)
angS_n=np.zeros((powers.size,freq.size))

for i in range(powers.size):
    na.power=powers[i]
    na.sweep()
    sleep(swp_time)
    freq,Sdata=na.getData()
    angS=np.unwrap(np.angle(Sdata))
    angS_n[i,:]=angS-(popt[0]*freq+popt[1])
    
X,Y=np.meshgrid(freq,powers)

figure()
pcolor(X,Y,angS_n)
xlabel('frequency (Hz)')
ylabel('power (dBm)')

#%%
#后端pump粗扫增益
mw=RS_MWSource('SMF100A')
mw.freqency=8.8e9

na.set_sweep(4e9,5e9,100,1001,1)
na.power=-40
na.average=1
swp_time=na.points/na.IFbandwidth*na.average

pumps=np.linspace(-30,-15,51)

mw.set_output(False)
na.sweep()
sleep(swp_time)
freq,Sdata0=na.getData()
angS=np.unwrap(np.angle(Sdata0))
popt,pcov=curve_fit(fit_linearPhase,freq[:100],angS[:100])

Sdata=np.zeros((pumps.size,freq.size)).astype('complex')

mw.level=pumps[0]
mw.set_output(True)

for i in range(pumps.size):
    mw.level=pumps[i]
    sleep(1e-3)
    na.sweep()
    sleep(swp_time)
    freq,Sdata[i,:]=na.getData()
    
X,Y=np.meshgrid(freq,pumps)

magS0=rf.mag_2_db(np.abs(Sdata0))
magS=rf.mag_2_db(np.abs(Sdata))
Gain=magS-magS0

figure()
pcolor(X,Y,Gain)
xlabel('frequency (Hz)')
ylabel('pump power (dBm)')

path='F:\\实验室据\\20180106-JPA\\'
filename='JPA-chuanshu1-Gain-pump-8.8G'
np.savez(path+filename,freq=freq,pumps=pumps,Sdata=Sdata,Sdata0=Sdata0)
