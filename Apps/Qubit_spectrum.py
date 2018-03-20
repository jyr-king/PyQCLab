# -*- coding: utf-8 -*-
"""
Created on Sun May  7 13:57:50 2017
通过扫谱获取qubit的大致能量信息，包括能级位置、非谐性等。
所需设备：1微波源，1网分，1 2通道AWG卡，1 2通道高速采集卡，1 触发源，2 IQmixer，2 定向耦合器。
@author: A108QCLab
"""
import time
import skrf as rf
import numpy as np

from PyQCLab.Instrument.NetworkAnalyser import *
from PyQCLab.Instrument.MWSource import *
from PyQCLab.Instrument.DCSources import *
from PyQCLab.Utils.WaveForm_Gen import *
#from PyQCLab.Instrument.Spcm_Cards import *
from PyQCLab.Examples.VNA_setup_guidata import *

from pylab import *

#%%
class Vna_Sweep_2D(Vna_Parameters):
    grp_swp_pwr = gdt.BeginGroup('Sweep Power:')
    swp_power_start = gdi.FloatItem('From (dBm):',default=0,min=-60,max=10)
    swp_power_stop = gdi.FloatItem('To (dBm):',default=-60,min=-60,max=10)
    swp_power_step = gdi.FloatItem('Step (dBm):',default=-3,min=-60,max=10)
    _grp_swp_pwr = gdt.EndGroup('Sweep Power:')
#%%
class Qubit_Spectrum_1D(gdt.DataSet):
    grp_swp_fq = gdt.BeginGroup('Sweep qubit excitations:')
    swp_fq_start = gdi.FloatItem('From (GHz):',default=6,min=0,max=20)
    swp_fq_stop = gdi.FloatItem('To (GHz):',default=6,min=0,max=20)
    swp_fq_step = gdi.FloatItem('Step (MHz):',default=1,min=-10000,max=10000)
    _grp_swp_fq = gdt.EndGroup('Sweep qubit excitations:')
    
    grp_pulses = gdt.BeginGroup('Pulses Definition:')
    iq_carrier_freq = gdi.FloatItem('Carrier Frequency (MHz):', default=10.039, min=-200, max=200)
    stim_pulse_len = gdi.FloatItem('Stimulation Pulse Length (us):', default=10, min=0, max=200)
    readout_pulse_len = gdi.FloatItem('Readout Pulse Length (us):',default=2, min=0, max=200)  
    _grp_pulses = gdt.EndGroup('Pulses Definition:')
    
    grp_timing = gdt.BeginGroup('Timing Definition:')
    trig_rate = gdi.IntItem('Trigger Rate:',default=10000,min=1,max=1000000,unit='Hz')
    delay_stim_to_read = gdi.FloatItem('Delay: stim off to readout on', default=0, unit='ns')
    record_len = gdi.FloatItem('Record Length per run', default=1, unit='us')
    record_times = gdi.IntItem('Record(Average) Times',default=1,min=1,max=1000000)
    _grp_timing = gdt.EndGroup('Timing Definition:')
#%%    
na1=ZNB20()
mw1=RS_MWSource('SMB100A_1')
dc1=GS200('DC3')
#%%
mw1.set_output(False)
#设置网分扫描范围：
fcenter=6.75e9
fspan=300e6
N=5001
IF0=10000
pwr=-20
na1.fcenter,na1.fspan,na1.points,na1.IFbandwidth=fcenter,fspan,N,IF0
na1.power=pwr
na1.average=1
na1.sweepType='lin'
waitime=na1.average*na1.points/na1.IFbandwidth
na1.sweep()
time.sleep(waitime)
f,Sdata=na1.getData()
magS=rf.mag_2_db(np.abs(Sdata))
modes=getResonmode(magS)
figure(),plot(f,magS)
#%%
powers=np.linspace(-20,-60,21)
Sdata=np.zeros((powers.size,N)).astype('complex')

for i in range(len(powers)):
    na1.power=powers[i]
    na1.IFbandwidth=IF0/2**(i//2)
    waitime=na1.average*na1.points/na1.IFbandwidth
    na1.sweep()
    time.sleep(waitime)
    f,Sdata[i,:]=na1.getData()
    
X,Y=np.meshgrid(powers,f)
figure(),pcolor(Y,X,rf.mag_2_db(np.abs(Sdata)).T)
#%%

#dc1=GS200('DC3')
dc1.mode='V'
dc1.range='1V'
dc1.level=0
dc1.output=1

bias=np.linspace(-0.5,0.5,21)
data=np.zeros((bias.size,N)).astype('complex')
for i in range(bias.size):
    dc1.level=bias[i]
    na1.sweep()
    time.sleep(waitime)
    f,Sdata=na1.getData()
    data[i,:]=Sdata
        
dc1.output=0   
X,Y=np.meshgrid(bias,f)
figure(),pcolor(X,Y,(rf.mag_2_db(np.abs(data))).T)
#%%
dc1.rang='1V'
dc1.level=-1
dc1.output=0
time.sleep(1)
fq=np.linspace(5.2,6.2,1001)*1e9
fr=6.8377e9





data1=np.zeros(fq.size).astype('complex')
mw1.set_output(True)
mw1.level=-30
#na1.sweepType='lin'
na1.fstart,na1.fstop=fr,fr
na1.points=1
na1.average=1
na1.IFbandwidth=10
na1.power=-50
waitime=na1.average*na1.points/na1.IFbandwidth

for i in range(fq.size):
    mw1.freqency=fq[i]
    na1.sweep()
    time.sleep(waitime)
    f,Sdata=na1.getData()
    data1[i]=Sdata[0]
mw1.set_output(False)   
dc1.output=0 
figure()
subplot(211),plot(fq,rf.mag_2_db(np.abs(data1)))
subplot(212),plot(fq,np.unwrap(np.angle(data1)))
#%%

fq=5.631e9
mw1.freqency=fq
dc1.level=-0.8
dc1.output=0
#fr=np.linspace(6.6,6.7,201)*1e9
#data1=np.zeros(fr.size).astype('complex')
mw1.set_output(False)
mw1.level=-20
na1.fstart,na1.fstop=6.68e9,6.685e9
na1.points=401
na1.average=1
na1.IFbandwidth=10
na1.power=-60
waitime=na1.average*na1.points/na1.IFbandwidth
na1.sweep()
time.sleep(waitime)
fr,Sdata=na1.getData()

mw1.set_output(False)  
dc1.output=0  
figure()
subplot(211),plot(fr,rf.mag_2_db(np.abs(Sdata)))
subplot(212),plot(fr,np.unwrap(np.angle(Sdata)))
#%%

dc1.output=0
dc1.rang='1V'
bias=np.linspace(-1,1,101)
fq=np.linspace(5.2,6.2,1001)*1e9
fr=6.7948e9
data2=np.zeros((bias.size,fq.size)).astype('complex')   
mw1.set_output(True)
mw1.level=-25
na1.fstart,na1.fstop=fr,fr
na1.points=1
na1.average=1
na1.IFbandwidth=10
na1.power=-50
waitime=na1.average*na1.points/na1.IFbandwidth
dc1.output=1
time.sleep(1)
for i in range(bias.size):
    dc1.level=bias[i]
    for j in range(fq.size):
        mw1.freqency=fq[j]
        na1.sweep()
        time.sleep(waitime)
        f,Sdata=na1.getData()
        data2[i,j]=Sdata[0]
    print('{:.0f}% completed.'.format((i+1)/bias.size*100))
mw1.set_output(False)
dc1.output=0
X,Y=np.meshgrid(bias,fq)
figure(),pcolor(X,Y,(rf.mag_2_db(np.abs(data2))).T)
figure(),pcolor(X,Y,np.angle(data2).T)

path='F:\\实验室据\\20180210LHK-5bits\\'
filename='LHK-5bit-spectrum_Q4'
np.savez(path+filename,data=data2)
#%%
dc1=yokogawa7651()
dc1.setFunc('dcI')
dc1.set_range('dcI','1mA')
dc1.set_level(1e-9)
dc1.set_output()

bias=np.linspace(0,0.5,51)*1e-3
fq=np.linspace(5.6,6.8,1201)*1e9
fr=6.7222e9
data2=np.zeros((bias.size,fq.size)).astype('complex')   
mw1.set_output(True)
mw1.level=-15
na1.fstart,na1.fstop=fr,fr
na1.points=1
na1.average=1
na1.IFbandwidth=1
na1.power=-40
waitime=na1.average*na1.points/na1.IFbandwidth
for i in range(bias.size):
    if abs(bias[i]) < 0.2001e-3:
        k=np.abs(fq-6.3e9).argmin()
        l=np.abs(fq-6.8e9).argmin()
    elif abs(bias[i]) < 0.4001e-3:
        k=np.abs(fq-5.9e9).argmin()
        l=np.abs(fq-6.5e9).argmin()
    else:
        k=np.abs(fq-5.6e9).argmin()
        l=np.abs(fq-6.1e9).argmin()
    dc1.set_level(bias[i])
    for j in range(k,l):
        mw1.freqency=fq[j]
        na1.sweep()
        time.sleep(waitime)
        f,Sdata=na1.getData()
        data2[i,j]=Sdata[0]
    np.savez('temp',data=data2)
mw1.set_output(False)
X,Y=np.meshgrid(bias,fq)
figure(),pcolor(X,Y,(rf.mag_2_db(np.abs(data2))).T)
figure(),pcolor(X,Y,np.unwrap(np.angle(data2)).T)
np.savez('c5q5_spectrum2',data=data2)

#%%
if __name__ == '__main__':
    import guidata
    _app = guidata.qapplication()
    v1=Vna_Sweep_2D(title='hello!')
    v1.edit()
    
    v2=Qubit_Spectrum_1D()
    v2.edit()
