# -*- coding: utf-8 -*-
"""
Created on Fri May  5 17:37:32 2017
JPA扫描测试脚本。
@author: A108QCLab
"""
from PyQCLab.Instrument.NetworkAnalyser import *
from PyQCLab.Instrument.MWSource import *
from pylab import *
import time
import skrf as rf
import numpy as np
#%%
#创建并初始化设备：
na1=ZNB20()
mw1=RS_MWSource('SMF100A')
#%%
#Pump off情况下扫描低功率下的腔响应。
mw1.set_output(False)
#设置网分扫描范围：
fcenter=6.65e9
fspan=200e6
N=401
IF0=20
pwr=-50
na1.fcenter,na1.fspan,na1.points,na1.IFbandwidth=fcenter,fspan,N,IF0
na1.power=pwr
na1.average=1
na1.sweepType='lin'
waitime=na1.average*na1.points/na1.IFbandwidth
na1.sweep()
time.sleep(waitime)
f,Sdata=na1.getData()
plot(f,rf.mag_2_db(np.abs(Sdata)))
#%%
#Pump on情况下扫描低功率下的腔响应。
dc1=yokogawa7651()
dc1.setFunc('dcI')
dc1.set_range('dcI','1mA')
dc1.set_output(True)
dc1.set_level(3e-4)
#%%
mw1.freqency=14e9
mw1.level=8
mw1.set_output(True)
fcenter=mw1.freqency/2
fspan=2e9
N=401
IF0=100
na1.fcenter,na1.fspan,na1.points,na1.IFbandwidth=fcenter,fspan,N,IF0
na1.power=-50
waitime=na1.average*na1.points/na1.IFbandwidth
na1.sweep()
time.sleep(waitime)
f,Sdata=na1.getData()
mw1.set_output(False)
plot(f,rf.mag_2_db(np.abs(Sdata)))
#%%
#测JPA前端响应随功率变化
fstart=7e9
fstop=8e9
N=1601
IF0=1000
pwr=-10
na1.fstart,na1.fstop,na1.points,na1.IFbandwidth=fstart,fstop,N,IF0
na1.power=pwr
na1.average=1
na1.sweepType='lin'
waitime=na1.average*na1.points/na1.IFbandwidth
na1.sweep()
time.sleep(waitime)
f,Sdata=na1.getData()
angS=np.unwrap(np.angle(Sdata))
f0,angS0=f.copy(),angS.copy()
angS_n=angS-angS0[0]-(angS0[-1]-angS0[0])/(f0[-1]-f0[0])*(f0-f0[0])
figure()
plot(f,angS_n)
#%%
na1.power+=3
na1.sweep()
time.sleep(waitime)
f,Sdata=na1.getData()
angS=np.unwrap(np.angle(Sdata))
angS_n=angS-angS0[0]-(angS0[-1]-angS0[0])/(f0[-1]-f0[0])*(f0-f0[0])
plot(f,angS_n)
#%%
from PyQCLab.Instrument.DCSources import *
dc1=yokogawa7651()
dc1.setFunc('dcI')
dc1.set_range('dcI','1mA')
dc1.set_output(False)
fstart=6e9
fstop=8e9
N=1601
IF0=1000
pwr=-10
na1.fstart,na1.fstop,na1.points,na1.IFbandwidth=fstart,fstop,N,IF0
na1.power=pwr
na1.average=1
na1.sweepType='lin'
waitime=na1.average*na1.points/na1.IFbandwidth
na1.sweep()
time.sleep(waitime)
f,Sdata=na1.getData()
angS=np.unwrap(np.angle(Sdata))
f0,angS0=f.copy(),angS.copy()
#angS_n=angS-angS0[0]-(angS0[-1]-angS0[0])/(f0[-1]-f0[0])*(f0-f0[0])
#figure()
#plot(f,angS_n)
I=np.linspace(-0.5,0.5,50)*1e-3
data=np.zeros((I.size,N))
dc1.set_output()
for i in range(I.size):
    dc1.set_level(I[i])
    na1.sweep()
    time.sleep(waitime)
    f,Sdata=na1.getData()
    data[i,:]=np.unwrap(np.angle(Sdata))-angS0[0]-(angS0[-1]-angS0[0])/(f0[-1]-f0[0])*(f0-f0[0])

X,Y=np.meshgrid(I,f0)    
figure(),pcolor(X,Y,data.T)
    
#%%
mw1.freqency=14.25e9
pumps=np.linspace(9.7,9.9,21)
#mw1.level=10.21
mw1.set_output(False)
fcenter=mw1.freqency/2
fspan=1e8
N=401
IF0=20
na1.fcenter,na1.fspan,na1.points,na1.IFbandwidth=fcenter,fspan,N,IF0
na1.power=-50
waitime=na1.average*na1.points/na1.IFbandwidth
na1.sweep()
time.sleep(waitime)
f0,Sdata0=na1.getData()
mw1.set_output(False)

data=np.zeros((pumps.size,N)).astype('complex')
for i in range(pumps.size):
    mw1.level=pumps[i]
    mw1.set_output(True)
    time.sleep(1e-1)
    na1.sweep()
    time.sleep(waitime)
    f,data[i,:]=na1.getData()
    mw1.set_output(False)
    
X,Y=np.meshgrid(pumps,f0)
figure(),pcolor(X,Y,(rf.mag_2_db(np.abs(data))).T - rf.mag_2_db(np.abs(np.ones((pumps.size,1))*Sdata0)).T)
