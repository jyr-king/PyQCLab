# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:04:48 2017

@author: A108QCLab
"""
#%%
import numpy as np
from pylab import *
#from time import sleep
from PyQCLab.Utils.WaveForm_v2 import *
from PyQCLab.Instrument.spcmDA import *
from PyQCLab.Instrument.pyspcm import *
from PyQCLab.Instrument.digitizer_v2 import *
from PyQCLab.Instrument.MWSource import *
from PyQCLab.Instrument.DG645 import *
from time import sleep
from scipy import integrate
import skrf as rf
#%%
#-------------创建所需的微波源。-------------------------------------------#
mw1=RS_MWSource('SMB100A_1')        #Qubit microwave drive
mw2=RS_MWSource('SMB100A_0')        #Readout resonator drive
#%%
#-------------创建AWG并初始化。-------------------------------------------#
da1=spectrumDA(1)
da1.level0=1000
#da1.level0
da1.level1=1000
#da1.level1
#da1.chEnable((1,))
#da1.output(1)
da1.chEnableAll()
da1.outputAll()
da1.runmode='single_r'
da1.setTriggerSource('ext0')
da1.setTriggerMode()
da1.setClockMode('ext')
da2=spectrumDA(0)
da2.level0=1000
da2.level1=1000
da2.level2=1000
da2.chEnableAll()
da2.outputAll()
da2.runmode='single_r'
da2.setTriggerSource('ext0')
da2.setTriggerMode()
da2.setClockMode('ext')
#%%
#-------------创建DG645并设置脉冲延时-------------------------------------------#
dg1=DG645()
dg1.delayA=1e-8
dg1.trigSource('int')
dg1.trigRate(2e4)
#%%
#-------------设置时序及波形参数-------------------------------------------#
t1=20e-6
t_stim=56e-9    #qubit激发时间间隔
t_r=20e-9      #激发波形上升和下降边沿宽度
beta=8          #采用kaiser窗作为上升和下降沿，beta是Kaiser窗的参数。
t_meas=4e-6     #读出腔激发时间间隔
f_b=10.3e6      #读出调制基带频率
state=0
tao=0     #qubit激发后到开始测量的延时

N_t1=int(t1*da2.sampleRate)
N_stim=int(t_stim*da2.sampleRate)
N_rise=int(t_r*da2.sampleRate)
N_hold=int(t_meas*da2.sampleRate)

N_shift=int(tao*da2.sampleRate)

l1=KILO_B(32)    #波形长度,对应输出时间约6.5微秒(l1/da1.sampleRate).
l2=KILO_B(16)    #波形长度，da2的采样率为da1的一半，所以波形长度相应减半。
#%%
#-------------创建波形-------------------------------------------#
Imod=WaveForm(length=l1,AWGType='spcm4')    #qubit激发波形I
Qmod=WaveForm(length=l1,AWGType='spcm4')    #qubit激发波形Q
Ioff=WaveForm(length=l2,AWGType='spcm4')    #qubit激发波形关断脉冲，采用一个额外的mixer作为关断。
Ireson=WaveForm(length=l2,AWGType='spcm4')  #读出腔激发脉冲波形I
Qreson=WaveForm(length=l2,AWGType='spcm4')  #读出腔激发脉冲波形I
Z=WaveForm(length=l2,AWGType='spcm4')       #qubitZ控制脉冲，目前为空。

if state:
    Imod.createWindow((('kaiser_r',N_t1*2-N_shift*2-N_rise*4-N_stim*2,N_t1*2-N_shift*2-N_rise*2-N_stim*2,beta),\
                   ('rectangle',N_t1*2-N_shift*2-N_rise*2-N_stim*2,N_t1*2-N_shift*2-N_rise*2),\
                   ('kaiser_f',N_t1*2-N_shift*2-N_rise*2,N_t1*2-N_shift*2,beta)\
                   ))
else:
    Imod.createWindow((\
                   ('rectangle',0,0),\
                   
                   ))
Qmod.createWindow((\
                   ('rectangle',0,0),\
                   
                   ))
Ioff.createWindow((('rectangle',N_t1-N_shift-N_stim-N_rise*2,N_t1-N_shift),\
                   ))
Ireson.createWindow((\
                     ('rectangle',N_t1,N_t1+N_hold),\
                     ))
Qreson.createWindow((\
                     ('rectangle',N_t1,N_t1+N_hold),\
                     ))

Ireson.createBase(func='cos',period=f_b*l2/da2.sampleRate)    #读出腔脉冲基带波形，I
Qreson.createBase(func='sin',period=f_b*l2/da2.sampleRate,phase=np.pi)  #读出腔脉冲基带波形，Q，相移pi，为了保证合成波形为cos[(omega_LO+omega_IF)*t].

Imod.createWaveform()
Qmod.createWaveform()
Ioff.createWaveform()
Ireson.createWaveform()
Qreson.createWaveform()
dg1.delayAB=t1+0.41e-6
#%%
#-------------波形写入DA卡-------------------------------------------#
da1.stop()
da2.stop()
wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
da1.writeWaveForm(wfdata1)
da2.writeWaveForm(wfdata2)
da1.start()
da2.start()
#%%
#-------------初始化采集卡并设置采集参数。-------------------------------------------#
sample_rate=1.8e9   #采样率。注意采用外部时钟采样时，采样率需在300M-1.8G之间，以1M为最小间隔。
t_rec=0.5e-6          #单个采样记录的时长。
N_rec=1000         #重复采样次数。

ad1=digitizer()
ad1.set_inputcontrol()
ad1.set_triggeroperation(trigsourcej='TRIG_EXT',triglevelj=180,trigslopej='NEG')
ad1.set_externaltrigger(coupling='DC')
ad1.set_triggermisc()
ad1.mode='NPT'
#ad1.mode='CS'
ad1.samplerate=sample_rate
ad1.set_captureclock(timebase='EXT_10MHz_REF')
ad1.recordlength=int(t_rec*ad1.samplerate)
#ad1.acqlength=int(12e-6*ad1.samplerate)
ad1.records=N_rec
#%%
#-------------设置微波源参数。-------------------------------------------#
fq=6.483e9
fr=6.7187e9
mw1.level=-10       #qubit激发强度
mw2.level=13        #读出腔激发强度，13是给到IQ mixer LO端用于解调信号的，给到读出腔的实际经过了定向耦合器的20dB衰减+20dB衰减器+IQ mixer衰减+线上衰减。
mw2.freqency=fr
mw1.freqency=fq
mw1.set_output(True)
mw2.set_output(True)
#mw1.set_output(False)
#mw2.set_output(False)
#%%
#-------------设置微波源参数。-------------------------------------------#
ad1.start()
D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
Dfft=np.fft.fft(D,axis=1)[:,idx]
print(abs(Dfft.mean()))
figure(),hist(Dfft.real,bins=100)
#%%
state=0
Count=1000     #用100次测量值作为一个点。
idx=np.abs(np.fft.fftfreq(ad1.recordlength,d=1/ad1.samplerate)+f_b).argmin()
Imod.createWindow((\
                   ('rectangle',0,0),\
                   
                   ))
Imod.createWaveform()

da1.stop()
wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
da1.writeWaveForm(wfdata1)
da1.start()
Dfft0=np.zeros(Count).astype('complex')
for i in range(Count):
    ad1.start()
    D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
    Dfft0[i]=np.fft.fft(D,axis=1).mean(axis=0)[idx]
mean_0=Dfft0.mean()

state=1
Imod.createWindow((('kaiser_r',N_t1*2-N_shift*2-N_rise*4-N_stim*2,N_t1*2-N_shift*2-N_rise*2-N_stim*2,beta),\
                   ('rectangle',N_t1*2-N_shift*2-N_rise*2-N_stim*2,N_t1*2-N_shift*2-N_rise*2),\
                   ('kaiser_f',N_t1*2-N_shift*2-N_rise*2,N_t1*2-N_shift*2,beta)\
                   ))

Imod.createWaveform()

da1.stop()
wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
da1.writeWaveForm(wfdata1)
da1.start()

Dfft1=np.zeros(Count).astype('complex')
for i in range(Count):
    ad1.start()
    D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
    Dfft1[i]=np.fft.fft(D,axis=1).mean(axis=0)[idx]
mean_1=Dfft1.mean()

center=(mean_0+mean_1)/2
angle=np.angle(mean_1-mean_0)

Dfft0_s=Dfft0-center
Dfft1_s=Dfft1-center
Dfft0_r=Dfft0_s*np.exp(-1j*angle)
Dfft1_r=Dfft1_s*np.exp(-1j*angle)
figure(),plot(Dfft0_r.real,Dfft0_r.imag,Dfft1_r.real,Dfft1_r.imag)
#np.savez('c5q5_state_distribution-5',Dfft0=Dfft0,Dfft1=Dfft1,Dfft0_r=Dfft0_r,Dfft1_r=Dfft1_r,Count=Count,N_rec=N_rec)
#np.savez('c5q5_state_decider',center=center,angle=angle,N_rec=N_rec,t_rec=t_rec)
#%%
N=100
S=np.zeros(N)
S1=np.zeros(N).astype('complex')
for i in range(N):
    ad1.start()
    D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)
    Dfft=np.fft.fft(D,axis=1).mean(axis=0)[idx]
    Dfft_n=(Dfft-center)*np.exp(-1j*angle)
    S[i]=Dfft_n.real > 0
    S1[i]=Dfft_n
print(S.sum()/S.size)
#plot(S1.real,S1.imag)
#%%
N=100
S=np.zeros(N)
S1=np.zeros(N).astype('complex')
for i in range(N):
    ad1.start()
    D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)
    Dfft=np.fft.fft(D,axis=1)[:,idx]
    Dfft_n=(Dfft-center)*np.exp(-1j*angle)
    S[i]=(Dfft_n.real > 0).sum()
#    S1[i]=Dfft_n
print(S.sum())