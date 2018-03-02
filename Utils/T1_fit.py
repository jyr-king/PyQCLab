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
filename='c5q5_T1_3.npz'
data=np.load(path+filename)
T1data=data['T1data']
tao=data['tao']
#t_r=data['t_r']
#figure(),plot(r_area, np.abs(Rabidata))
#%%
def T1(p,x):
    a,b,c=p
    return a+b*np.exp(-x/c)

def error_T1(p,x,y):
    return T1(p,x)-y

#%%
p0=[6.484e9,-30e6,1e-6]
P=leastsq(error_T1,p0,args=(tao1,peaks1))
figure(),plot(tao, np.abs(T1data),tao,T1(P[0],tao))
