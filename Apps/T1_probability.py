# -*- coding: utf-8 -*-
"""
Created on Wed May 10 17:48:46 2017

@author: A108QCLab
"""
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

tao=9e-6      #qubit激发后到开始测量的延时

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

Imod.createWindow((('kaiser_r',N_t1*2-N_shift*2-N_rise*4-N_stim*2,N_t1*2-N_shift*2-N_rise*2-N_stim*2,beta),\
                   ('rectangle',N_t1*2-N_shift*2-N_rise*2-N_stim*2,N_t1*2-N_shift*2-N_rise*2),\
                   ('kaiser_f',N_t1*2-N_shift*2-N_rise*2,N_t1*2-N_shift*2,beta)\
                   ))
Qmod.createWindow((\
                   ('rectangle',0,0),\
                   
                   ))
Ioff.createWindow((('rectangle',N_t1-N_shift-N_stim-N_rise*2,N_t1-N_shift),\
                   ))

Ireson.createBase(func='cos',period=f_b*l2/da2.sampleRate)    #读出腔脉冲基带波形，I
Qreson.createBase(func='sin',period=f_b*l2/da2.sampleRate,phase=np.pi)  #读出腔脉冲基带波形，Q，相移pi，为了保证合成波形为cos[(omega_LO+omega_IF)*t].

Ireson.createWindow((\
                     ('rectangle',N_t1,N_t1+N_hold),\
                     ))
Qreson.createWindow((\
                     ('rectangle',N_t1,N_t1+N_hold),\
                     ))

Imod.createWaveform()
Qmod.createWaveform()
Ioff.createWaveform()
Ireson.createWaveform()
Qreson.createWaveform()
dg1.delayAB=t1+0.42e-6
#dg1.delayAB=1e-6
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
ad1.set_triggeroperation(trigsourcej='TRIG_EXT',triglevelj=135,trigslopej='NEG')
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

#%%
#path='./'
#filename='c5q5_state_decider.npz'
#decider=np.load(path+filename)

tao=np.linspace(0,10e-6,101)
T1data=np.zeros(tao.size)
T1data2=np.zeros(tao.size).astype('complex')
#t_meas=3e-6
#t_r=10e-9
#N_hold=int(t_meas*da2.sampleRate)
#N_rise=int(t_r*da2.sampleRate)
N=50
idx=np.abs(np.fft.fftfreq(ad1.recordlength,d=1/ad1.samplerate)+f_b).argmin()
figure()
for i in range(tao.size):
    N_shift=int(tao[i]*da2.sampleRate)
    Imod.createWindow((('kaiser_r',N_t1*2-N_shift*2-N_rise*4-N_stim*2,N_t1*2-N_shift*2-N_rise*2-N_stim*2,beta),\
                   ('rectangle',N_t1*2-N_shift*2-N_rise*2-N_stim*2,N_t1*2-N_shift*2-N_rise*2),\
                   ('kaiser_f',N_t1*2-N_shift*2-N_rise*2,N_t1*2-N_shift*2,beta)\
                   ))
    Ioff.createWindow((('rectangle',N_t1-N_shift-N_stim-N_rise*2,N_t1-N_shift),\
                   ))
    
    Imod.createWaveform()
    Ioff.createWaveform()
    
    da1.stop()
    da2.stop()
    wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
    wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
    da1.writeWaveForm(wfdata1)
    da2.writeWaveForm(wfdata2)
    da1.start()
    da2.start()
#    wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
    
#    dg1.delayAB=t_r*2+t_stim+tao[i]+0.42e-6
#    da2.stop()
#    da2.writeWaveForm(wfdata2)
#    da2.start()
    
    S=np.zeros(N)
    for k in range(N):
        ad1.start()
        D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
#        Dfft=np.fft.fft(D,axis=1).mean(axis=0)[idx]                 #对采样数据做fft，取平均，然后取出信号频率点的值。
#        Dfft_n=(Dfft-center)*np.exp(-1j*angle)
#        S[k]=Dfft_n.real > 0
        Dfft=np.fft.fft(D,axis=1)[:,idx]
        Dfft_n=(Dfft-center)*np.exp(-1j*angle)
        S[k]=(Dfft_n.real > 0).sum()
        T1data2[i]=(T1data2[i]*k+Dfft.mean())/(k+1)
#    S=S*np.exp(1j*2*np.pi*f_b*tao[i])
#    plot(S.real,S.imag)
    T1data[i]=S.sum()
#        ad1.start()
#        I,Q=ad1.data
#        I2,Q2=I.reshape(ad1.records,-1).mean(axis=0),Q.reshape(ad1.records,-1).mean(axis=0)
#        Ifft2,Qfft2=np.abs(np.fft.rfft(I2)),np.abs(np.fft.rfft(Q2))
#        T1data[i]=(T1data[i]*k+Ifft2[8]+1j*Qfft2[8])/(k+1)
    np.savez('c5q5_T1_probability1',T1data=T1data,T1data2=T1data2,tao=tao,fr=fr,fq=fq) 
    print(i,T1data[i])
plot(tao,T1data)
#%%
fq=6.482e9
fr=6.733e9
mw1.freqency=fq
mw2.freqency=fr

t_meas=2e-6
t_r=20e-9
t_stim=10e-6
tao=-1e-6
N_hold=int(t_meas*da2.sampleRate)
N_rise=int(t_r*da2.sampleRate)
N_stim=int(t_stim*da2.sampleRate)
N_shift=int(tao*da2.sampleRate)

avg=4

l1=KILO_B(32)    #波形长度
l2=KILO_B(16)
Imod=WaveForm(length=l1,AWGType='spcm4')
Qmod=WaveForm(length=l1,AWGType='spcm4')
Ioff=WaveForm(length=l2,AWGType='spcm4')
Ireson=WaveForm(length=l2,AWGType='spcm4')
Qreson=WaveForm(length=l2,AWGType='spcm4')
Z=WaveForm(length=l2,AWGType='spcm4')
Imod.createWindow((('rectangle',0,N_stim*2),))
Qmod.createWindow((('rectangle',0,N_stim*2),))
Ioff.createWindow((('rectangle',0,N_stim),))
Ireson.createBase(func='cos',period=200)
Qreson.createBase(func='sin',period=200)
Ireson.createWindow((('kaiser_r',N_stim+N_shift,N_rise+N_stim+N_shift,12),\
                     ('rectangle',N_rise+N_stim+N_shift,N_rise+N_stim+N_shift+N_hold),\
                     ('kaiser_f',N_rise+N_stim+N_shift+N_hold,N_rise*2+N_stim+N_shift+N_hold,12)\
                     ))
Qreson.createWindow((('kaiser_r',N_stim+N_shift,N_rise+N_stim+N_shift,12),\
                     ('rectangle',N_rise+N_stim+N_shift,N_rise+N_stim+N_shift+N_hold),\
                     ('kaiser_f',N_rise+N_stim+N_shift+N_hold,N_rise*2+N_stim+N_shift+N_hold,12)\
                     ))

Imod.createWaveform()
Qmod.createWaveform()
Ioff.createWaveform()
Ireson.createWaveform()
Qreson.createWaveform()
dg1.delayAB=t_r*4+t_stim+tao    

da1.stop()
da2.stop()
wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
da1.writeWaveForm(wfdata1)
da2.writeWaveForm(wfdata2)
da1.start()
da2.start()

tao=np.linspace(-1e-6,1e-6,101)
T1data=np.zeros(tao.size).astype('complex')
for i in range(tao.size):
    N_shift=int(tao[i]*da2.sampleRate)
    Ireson.createWindow((('kaiser_r',N_stim+N_shift,N_rise+N_stim+N_shift,12),\
                     ('rectangle',N_rise+N_stim+N_shift,N_rise+N_stim+N_shift+N_hold),\
                     ('kaiser_f',N_rise+N_stim+N_shift+N_hold,N_rise*2+N_stim+N_shift+N_hold,12)\
                     ))
    Qreson.createWindow((('kaiser_r',N_stim+N_shift,N_rise+N_stim+N_shift,12),\
                     ('rectangle',N_rise+N_stim+N_shift,N_rise+N_stim+N_shift+N_hold),\
                     ('kaiser_f',N_rise+N_stim+N_shift+N_hold,N_rise*2+N_stim+N_shift+N_hold,12)\
                     ))
    Ireson.createWaveform()
    Qreson.createWaveform()
    wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
    
    dg1.delayAB=t_r*4+t_stim+tao[i]
    da2.stop()
    da2.writeWaveForm(wfdata2)
    da2.start()
    
    for k in range(avg):
        ad1.start()
        I,Q=ad1.data
        I2,Q2=I.reshape(ad1.records,-1).mean(axis=0),Q.reshape(ad1.records,-1).mean(axis=0)
        Ifft2,Qfft2=np.abs(np.fft.rfft(I2)),np.abs(np.fft.rfft(Q2))
        T1data[i]=(T1data[i]*k+Ifft2[8]+1j*Qfft2[8])/(k+1)
    
figure(),plot(tao,np.abs(T1data))
np.savez('T1_bias0.2mA',T1data=T1data,tao=tao,fr=fr,fq=fq)
#%%
#-------------关闭DA卡。其它设备暂时看来无需关闭。-------------------------------------------#
da1.stop()
da2.stop()
da1.closeCard()
da2.closeCard()