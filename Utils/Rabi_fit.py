# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:01:50 2017

@author: A108QCLab
"""
#%%
import numpy as np
from scipy.optimize import leastsq
from pylab import *
#%%
#-------------导入数据---------------------------------
path='C:/Users/A108QCLab/Documents/Python Scripts/PyQCLab/'
filename='c5q5_SpinEchoX-3.npz'
data=np.load(path+filename)
Rabidata=data['SEdataX2']
#areaY=data['areaX']
tao=data['tao']
#t_r=data['t_r']
figure(),plot(tao, np.abs(Rabidata))
#%%
def Rabi_osc(p,x):
    a,b,tr,omega,phi=p
    return a+b*np.exp(-t_stim/tr)*cos(omega*t_stim+phi)

def error_rabi(p,x,y):
    return Rabi_osc(p,x)-y
#%%
def Rabi_osc(p,x):
    a,b,tr,omega,phi=p
    return a+b*np.exp(-x/tr)*cos(omega*x+phi)

def error_rabi(p,x,y):
    return Rabi_osc(p,x)-y
#%%
p0=[1,2,3e-6,60e6,3]
P=leastsq(error_rabi,p0,args=(tao,np.abs(Rabidata)))
P=leastsq(error_rabi,P[0],args=(areaY,np.abs(Rabidata)))
P=leastsq(error_rabi,P[0],args=(areaY,np.abs(Rabidata)))
plot(tao, Rabi_osc(P[0],tao))
xlabel('norminal pulse length (s)',fontsize=24)
ylabel('Amplitude (a.u)',fontsize=24)
#text(1e-6,3.1,'$T_{2rabi}=3.36\mu s$',fontsize=24)
