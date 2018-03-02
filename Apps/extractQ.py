# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 22:32:01 2016

@author: Xmon-SC05
"""
from PyQCLab.Utils.Qextractor import *
from pylab import *
import skrf as rf

def dbphase2complex(mag_db,phase,deg=True):
    if deg:
        phase=deg2rad(phase)
        return rf.db_2_mag(mag_db)*exp(1j*phase)
        
path='..\\Data\\'
filename='YZG_WetEtch_Openloop_20161018_dip'
postfix1='_HowPower'
postfix2='.npz'
postfix3='Qfactor'

modes=[5.3026e9,5.4271e9,5.5531e9,6.0409e9,6.1512e9,6.3264e9,6.865e9,6.9378e9]
q=Qextractor()

for i in range(len(modes)):
    data=load(path+filename+str(i)+postfix1+postfix2)
    power=data['power']
    SData=data['SData']
    M,N,O=SData.shape
    Qparam=zeros((M,4))
    
    f0=modes[i]
    p0=[1e5,1e5,1,f0]
    figure()
    for k in range(M):
        freq=SData[k,:,0]
        sparam=dbphase2complex(SData[k,:,1],SData[k,:,2])
        q.freq,q.sparam=freq,sparam
        q.update(p0)
        subplot(6,2,k+1),plot(q.S_n.real,q.S_n.imag,'o',q.S_fit.real,q.S_fit.imag,'r-')
#    figure(),plot(q.S_n.real,q.S_n.imag,'o',q.S_fit.real,q.S_fit.imag,'r-')
        Qparam[k,:]=power[k],q.Qi,q.Qc,q.f0
        print('Power={}dBm, Qi={}, Qc={}, f0={} Hz.'.format(power[k],q.Qi,q.Qc,q.f0))
#    savez(path+filename+str(i)+postfix1+postfix3+'1',Qparam=Qparam)
    
