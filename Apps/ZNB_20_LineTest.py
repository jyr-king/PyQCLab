# -*- coding: utf-8 -*-
"""
Cable test
This is a temporary script file.
"""
"""
中文注释
"""
from PyQCLab.Instrument.NetworkAnalyser import *
from PyQCLab.Instrument.MWSource import *
from pylab import *
import time
import skrf as rf
import numpy as np
#%%
DataPath='C:\\Users\\A108QCLab\\Documents\\Python Scripts\\PyQCLab\Data\\'
fstart=100e3
fstop=20e9
powr=0
N=10001
IF=1000

na=ZNB20()
na.fstart,na.fstop,na.power,na.points,na.IFbandwidth=fstart,fstop,powr,N,IF
na.average=1
waitime=na.average*na.points/na.IFbandwidth
#%%
filename='HKQ5bit_TL_RT'
na.fstop=20e9
na.sweep()
time.sleep(waitime)
f,Sdata=na.getData()
np.savez(DataPath+filename,f=f,Sdata=Sdata)
figure(),plot(f,rf.mag_2_db(np.abs(Sdata)))



#%% plot figure; 
data=np.load('C:/Users/A108QCLab/Documents/Python Scripts/PyQCLab/Data/40C4-6.npz')
f,Sdata=data['f'],data['Sdata']
plt.figure('figC4')
plot(f,rf.mag_2_db(np.abs(Sdata)))
title('C4_All')
# coding=utf-8 中文注释
#%%
modes=np.array([6.545,6.548,6.566,6.604,6.639,6.676,6.708,6.743])*1e9
path='C:\\Users\\A108QCLab\\Documents\\Python Scripts\\PyQCLab\\Data\\'
filename_prefix='HKQ_5bits_Allmodes_'               
na=ZNB20()
N=1601
IF0=1e5
fstart=6.53e9
fstop=6.75e9
powers=np.linspace(10,-30,31)
data=list()

na.fstart,na.fstop,na.points,na.IFbandwidth=fstart,fstop,N,IF0
avg=1

figure()
for i in range(powers.size):
    na.power=powers[i]
    IF=IF0/10**((powers[0]-na.power)/10)
    if IF < 1:
        avg=int(1/IF)
        IF=1    
    na.IFbandwidth=int(IF)
    print(na.IFbandwidth)
    na.average=avg
    print(na.average)
    waitime=na.average*na.points/na.IFbandwidth
    na.sweep()
    time.sleep(waitime)
    f,Sdata=na.getData()
    data.append((na.power,f,Sdata))
    filename=path+filename_prefix+str(na.power)+'dBm'
#    np.savez(filename,power=na.power,f=f,Sdata=Sdata)
    plot(f,rf.mag_2_db(np.abs(Sdata)))

#%%
path='C:\\Users\\A108QCLab\\Documents\\Python Scripts\\PyQCLab\\Data\\'
filename_prefix='HKQ_5bits_JPAMode_'               
na=ZNB20()
N=1601
IF0=1e5
fstart=6e9
fstop=8e9
powers=np.linspace(10,-30,31)
data=list()

na.fstart,na.fstop,na.points,na.IFbandwidth=fstart,fstop,N,IF0
avg=1
figure()
for i in range(powers.size):
    na.power=powers[i]
    IF=IF0/3**((powers[0]-na.power)/10)
    if IF < 1:
        avg=int(1/IF)
        IF=1    
    na.IFbandwidth=int(IF)
    print(na.IFbandwidth)
    na.average=avg
    print(na.average)
    waitime=na.average*na.points/na.IFbandwidth
    na.sweep()
    time.sleep(waitime)
    f,Sdata=na.getData()
    data.append((na.power,f,Sdata))
    filename=path+filename_prefix+str(na.power)+'dBm'
#    np.savez(filename,power=na.power,f=f,Sdata=Sdata)
    subplot(211)
    plot(f,rf.mag_2_db(np.abs(Sdata)))
    Phase=np.unwrap(np.angle(Sdata))
    Phase_n=Phase-(Phase[-1]-Phase[0])/(f[-1]-f[0])*(f-f[0])
    subplot(212)
    plot(f,Phase_n)
na.close()
#%%
from PyQCLab.Instrument.DCSources import *

dc0=yokogawa7651()
dc0.set_range('dcI','1mA')
dc0.set_level(0.1)
#%%
mws=RS_MWSource('SMB100A_1')
mws.instrhandle.write('OUTP:STAT {}'.format('ON'))
mws.level=-30
na=ZNB20()
na.fcenter=6.6763e9
na.fspan=10e6
na.points=101
na.IFbandwidth=20


na.power=-30
#na.IFbandwidth=1
na.average=1
#na.points=1
waitime=na.average*na.points/na.IFbandwidth
fq=np.linspace(6.4,6.6,201)*1e9
#pwr_q=0
#mws.level=pwr_q

data=np.zeros((fq.size,na.points)).astype('complex')
for i in range(fq.size):
    mws.freqency=fq[i]
    time.sleep(0.001)
    na.sweep()
    time.sleep(waitime)
    f,Sdata=na.getData()
    data[i,:]=Sdata
figure()
X,Y=np.meshgrid(f,fq)
pcolor(X,Y,rf.mag_2_db(np.abs(data)))

#%%
na=ZNB20()
N=1601
IF0=10
fstart=6.53e9
fstop=6.75e9
pwr=-50
na.fstart,na.fstop,na.points,na.IFbandwidth=fstart,fstop,N,IF0
na.power=pwr
na.average=1
na.sweep()
#%%
mws.instrhandle.write('OUTP:STAT {}'.format('OFF'))
na.fcenter=6.60384e9
na.fspan=10e6
na.points=201
na.IFbandwidth=2

waitime=na.average*na.points/na.IFbandwidth
na.sweep()
time.sleep(waitime)
f,Sdata=na.getData()
figure(),plot(f,rf.mag_2_db(np.abs(Sdata)))
Sdata0=Sdata.copy()

mws.freqency=6.04207e9
mws.instrhandle.write('OUTP:STAT {}'.format('ON'))
na.sweep()
time.sleep(waitime)
f,Sdata=na.getData()
plot(f,rf.mag_2_db(np.abs(Sdata)))
Sdata1=Sdata.copy()
#%%
mws=RS_MWSource('SMB100A_1')
mws.instrhandle.write('OUTP:STAT {}'.format('ON'))
na=ZNB20()
na.fstart=6.70819e9
na.fstop=6.70819e9
na.points=1
na.IFbandwidth=2

na.power=-50
#na.IFbandwidth=1
na.average=1
#na.points=1
waitime=na.average*na.points/na.IFbandwidth
fq=np.linspace(5.6,5.8,301)*1e9
pwr_q=0
mws.level=pwr_q

data=np.zeros(fq.size).astype('complex')
for i in range(fq.size):
    mws.freqency=fq[i]
    time.sleep(0.001)
    
    waitime=na.average*na.points/na.IFbandwidth
    na.sweep()
    time.sleep(waitime)
    f,Sdata=na.getData()
    data[i]=Sdata[0]
#figure()
plot(fq,rf.mag_2_db(np.abs(data)))

#%%
mws=RS_MWSource('SMB100A_1')
mws.level=0
mws.instrhandle.write('OUTP:STAT {}'.format('ON'))
na=ZNB20()

segments=[(6.56562e9,6.56562e9,2,1),(6.60384e9,6.60384e9,2,1),(6.6763e9,6.6763e9,2,1),(6.7082e9,6.7082e9,2,1),(6.74258e9,6.74258e9,2,1)]
na.addSegments(segments)
na.power=-50
na.average=1

waitime=2.5
fq=np.linspace(6,6.1,101)*1e9
data=np.zeros((fq.size,5)).astype('complex')
for i in range(fq.size):
    mws.freqency=fq[i]
    time.sleep(0.001)
    
#    waitime=na.average*na.points/na.IFbandwidth
    na.sweep()
    time.sleep(waitime)
    f,Sdata=na.getData()
    data[i,:]=Sdata
        
figure()
for i in range(5):
    plot(fq,rf.mag_2_db(np.abs(data[:,i])))