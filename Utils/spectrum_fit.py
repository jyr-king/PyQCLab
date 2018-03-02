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
filename='c5q5_sweep_fq.npz'
data=np.load(path+filename)
data1=data['data']
fq=data['fq']
#t_r=data['t_r']
#figure(),plot(r_area, np.abs(Rabidata))
#%%
def spectrum1(p,x):
    a,b,c,d=p
    return a*np.exp(-(x-b)**2/c)+d

def spectrum2(p,x):
    a,b,c,d=p
    return a+b/(1+(x-c)**2/d)

def error_spec1(p,x,y):
    return spectrum1(p,x)-y
def error_spec2(p,x,y):
    return spectrum2(p,x)-y

#%%
def Rabi_osc(p,x):
    a,b,omega,phi=p
    return a+b*cos(omega*x+phi)

def error_rabi(p,x,y):
    return Rabi_osc(p,x)-y
#%%
#---------------高斯线型拟合-----------------------------
p0=[1.4,6.4822e9,1e12,2.4]
P=leastsq(error_spec,p0,args=(fq,np.abs(data1)))
plot(fq,np.abs(data1),fq, spectrum(P[0],fq))
#%%
#---------------洛伦兹线型拟合-----------------------------
p0=[2.4,1.4,6.4822e9,1e12]
P=leastsq(error_spec2,p0,args=(fq,np.abs(data1)))
figure(),plot(fq,np.abs(data1),fq, spectrum2(P[0],fq))
