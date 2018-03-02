# -*- coding: utf-8 -*-
"""
Created on Fri May 12 18:47:40 2017

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
da1=spectrumDA(0)
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
da1.setClockMode('int')
#da2=spectrumDA(0)
#da2.level0=1000
#da2.level1=1000
#da2.level2=1000
#da2.chEnableAll()
#da2.outputAll()
#da2.runmode='single_r'
#da2.setTriggerSource('ext0')
#da2.setTriggerMode()
#da2.setClockMode('ext')
#%%
#-------------创建DG645并设置脉冲延时-------------------------------------------#
dg1=DG645()
dg1.delayA=1e-6
dg1.delayAB=2e-6
dg1.trigSource('int')
dg1.trigRate(1e3)
#%%
#-------------设置时序及波形参数-------------------------------------------#
#t_stim=10e-6    #qubit激发时间间隔
t_r=20e-9      #激发波形上升和下降边沿宽度
beta=8          #采用kaiser窗作为上升和下降沿，beta是Kaiser窗的参数。
t_meas=4e-6     #读出腔激发时间间隔
f_b=10.3e6      #读出调制基带频率

tao=0      #qubit激发后到开始测量的延时

#N_stim=int(t_stim*da2.sampleRate)
N_rise=int(t_r*da1.sampleRate)
N_hold=int(t_meas*da1.sampleRate)

N_shift=int(tao*da1.sampleRate)

l1=KILO_B(32)    #波形长度,对应输出时间约6.5微秒(l1/da1.sampleRate).
l2=KILO_B(16)    #波形长度，da2的采样率为da1的一半，所以波形长度相应减半。

#%%
fq=6.483e9
fr=6.7187e9
level_q=-10
level_r=13
mw1.freqency=fq
mw2.freqency=fr
mw1.level=level_q
mw2.level=level_r
mw1.set_output(True)
mw2.set_output(True)
#%%
t_stim=np.linspace(0e-6,1e-6,501)
#tao=-5e-7
#N_hold=int(t_meas*da2.sampleRate)
#N_rise=int(t_r*da2.sampleRate)
#N_shift=int(tao*da2.sampleRate)

avg=4

#l1=KILO_B(32)    #波形长度
#l2=KILO_B(16)
Imod=WaveForm(length=l1,AWGType='spcm4')
Qmod=WaveForm(length=l1,AWGType='spcm4')
Ioff=WaveForm(length=l2,AWGType='spcm4')
Ireson=WaveForm(length=l2,AWGType='spcm4')
Qreson=WaveForm(length=l2,AWGType='spcm4')
Z=WaveForm(length=l2,AWGType='spcm4')

Ireson.createBase(func='cos',period=f_b*l2/da2.sampleRate)    #读出腔脉冲基带波形，I
Qreson.createBase(func='sin',period=f_b*l2/da2.sampleRate,phase=np.pi)  #读出腔脉冲基带波形，Q，相移pi，为了保证合成波形为cos[(omega_LO+omega_IF)*t].

Rabidata=np.zeros(t_stim.size).astype('complex')
r_area=np.zeros(t_stim.size)
for i in range(t_stim.size):
    N_stim=int(t_stim[i]*da2.sampleRate)
    Imod.createWindow((('kaiser_r',0,N_rise*2,beta),\
                   ('rectangle',N_rise*2,N_rise*2+N_stim*2),\
                   ('kaiser_f',N_rise*2+N_stim*2,N_rise*4+N_stim*2,beta)\
                   ))
    Qmod.createWindow((\
                   ('rectangle',0,0),\
                   
                   ))
    Ioff.createWindow((('rectangle',0,N_rise*2+N_stim),\
                   ))
    Ireson.createWindow((\
                     ('rectangle',N_rise*2+N_stim,N_rise*2+N_stim+N_hold),\
                     ))
    Qreson.createWindow((\
                     ('rectangle',N_rise*2+N_stim,N_rise*2+N_stim+N_hold),\
                     ))
    Imod.createWaveform()
    Qmod.createWaveform()
    Ioff.createWaveform()
    Ireson.createWaveform()
    Qreson.createWaveform()
    
    da1.stop()
    da2.stop()
    wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
    wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
    da1.writeWaveForm(wfdata1)
    da2.writeWaveForm(wfdata2)
    da1.start()
    da2.start()
    
    dg1.delayAB=t_r*2+t_stim[i]+tao+0.42e-6
    
    r_area[i]=integrate.simps(Imod.rawWaveform,dx=1/da1.sampleRate)
    for k in range(avg):
        ad1.start()
        D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
        Dfft=np.fft.fft(D,axis=1).mean(axis=0)[idx]                 #对采样数据做fft，取平均，然后取出信号频率点的值。
        Rabidata[i]=(Rabidata[i]*k+Dfft)/(k+1)
#    for k in range(avg):
#        ad1.start()
#        I,Q=ad1.data
#        I2,Q2=I.reshape(ad1.records,-1).mean(axis=0),Q.reshape(ad1.records,-1).mean(axis=0)
#        Ifft2,Qfft2=np.abs(np.fft.rfft(I2)),np.abs(np.fft.rfft(Q2))
#        Rabidata[i]=(Rabidata[i]*k+Ifft2[8]+1j*Qfft2[8])/(k+1)
    np.savez('c5q5_Rabi_bias0.2mA-5',Rabidata=Rabidata,t_stim=t_stim,r_area=r_area,fr=fr,fq=fq,levelq=level_q,levelr=level_r,avg=avg)
    print(i)
figure(),plot(r_area,np.abs(Rabidata))
#%%
#fq=6.482e9
#fr=6.733e9
#level_q=-10
#level_r=13
#mw1.freqency=fq
#mw2.freqency=fr
#mw1.level=level_q
#mw2.level=level_r
#mw1.set_output(True)
#mw2.set_output(True)
#
#t_meas=2e-6
#t_r=np.linspace(10,100,21)*1e-9
#t_stim=np.linspace(0e-6,1e-6,401)
#tao=-5e-7
#N_hold=int(t_meas*da2.sampleRate)
#N_rise=int(t_r[0]*da2.sampleRate)
#N_shift=int(tao*da2.sampleRate)
#
#avg=4
#
#l1=KILO_B(32)    #波形长度
#l2=KILO_B(16)
#Imod=WaveForm(length=l1,AWGType='spcm4')
#Qmod=WaveForm(length=l1,AWGType='spcm4')
#Ioff=WaveForm(length=l2,AWGType='spcm4')
#Ireson=WaveForm(length=l2,AWGType='spcm4')
#Qreson=WaveForm(length=l2,AWGType='spcm4')
#Z=WaveForm(length=l2,AWGType='spcm4')
#
#Ireson.createBase(func='cos',period=200)
#Qreson.createBase(func='sin',period=200)
# 
#Rabidata=np.zeros(t_r.size).astype('complex')
#r_area=np.zeros(t_r.size)
#for i in range(t_r.size):
#    N_rise=int(t_r[i]*da2.sampleRate)
#    Imod.createWindow((('kaiser',0,N_rise*4,8),\
#                       
#                       
#                       ))
#    Qmod.createWindow((('kaiser',0,N_rise*4,8),\
#                       
#                       
#                       ))
#    Ioff.createWindow(( \
#                       ('rectangle',0,N_rise*2),\
#                       ))
#    Ireson.createWindow((\
#                     ('rectangle',N_rise*2,N_rise*2+N_hold),\
#                     ))
#    Qreson.createWindow((\
#                     ('rectangle',N_rise*2,N_rise*2+N_hold),\
#                     ))
#    Imod.createWaveform()
#    Qmod.createWaveform()
#    Ioff.createWaveform()
#    Ireson.createWaveform()
#    Qreson.createWaveform()
#
#    da1.stop()
#    da2.stop()
#    wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
#    wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
#    da1.writeWaveForm(wfdata1)
#    da2.writeWaveForm(wfdata2)
#    da1.start()
#    da2.start()
#    
#    dg1.delayAB=t_r*2
#    
#    r_area[i]=integrate.simps(Imod.rawWaveform,dx=1/da1.sampleRate)
#    for k in range(avg):
#        ad1.start()
#        I,Q=ad1.data
#        I2,Q2=I.reshape(ad1.records,-1).mean(axis=0),Q.reshape(ad1.records,-1).mean(axis=0)
#        Ifft2,Qfft2=np.abs(np.fft.rfft(I2)),np.abs(np.fft.rfft(Q2))
#        Rabidata[i]=(Rabidata[i]*k+Ifft2[8]+1j*Qfft2[8])/(k+1)
#        
#    print(i)
#    np.savez('Rabi_bias0.2mA-6',Rabidata=Rabidata,t_r=t_r,r_area=r_area,fr=fr,fq=fq,levelq=level_q,levelr=level_r,avg=avg)
#figure(),plot(r_area,np.abs(Rabidata))
##%%
#fq=6.482e9
#fr=6.733e9
#level_q=-10
#level_r=13
#mw1.freqency=fq
#mw2.freqency=fr
#mw1.level=level_q
#mw2.level=level_r
#mw1.set_output(True)
#mw2.set_output(True)
#
#t_meas=2e-6
#t_r=np.linspace(10,100,21)*1e-9
#t_stim=np.linspace(0e-6,1e-6,401)
#tao=-5e-7
#N_hold=int(t_meas*da2.sampleRate)
#N_rise=int(t_r[0]*da2.sampleRate)
#N_shift=int(tao*da2.sampleRate)
#
#avg=4
#
#l1=KILO_B(32)    #波形长度
#l2=KILO_B(16)
#Imod=WaveForm(length=l1,AWGType='spcm4')
#Qmod=WaveForm(length=l1,AWGType='spcm4')
#Ioff=WaveForm(length=l2,AWGType='spcm4')
#Ireson=WaveForm(length=l2,AWGType='spcm4')
#Qreson=WaveForm(length=l2,AWGType='spcm4')
#Z=WaveForm(length=l2,AWGType='spcm4')
#
#Ireson.createBase(func='cos',period=200)
#Qreson.createBase(func='sin',period=200)
# 
#Rabidata=np.zeros(t_r.size).astype('complex')
#r_area=np.zeros(t_r.size)
#for i in range(t_r.size):
#    N_rise=int(t_r[i]*da2.sampleRate)
#    Imod.createWindow((('kaiser',0,N_rise*4,8),\
#                       
#                       
#                       ))
#    Qmod.createWindow((('kaiser',0,N_rise*4,8),\
#                       
#                       
#                       ))
#    Ioff.createWindow(( \
#                       ('rectangle',0,N_rise*2),\
#                       ))
#    Ireson.createWindow((\
#                     ('rectangle',N_rise*2,N_rise*2+N_hold),\
#                     ))
#    Qreson.createWindow((\
#                     ('rectangle',N_rise*2,N_rise*2+N_hold),\
#                     ))
#    Imod.createWaveform()
#    Qmod.createWaveform()
#    Ioff.createWaveform()
#    Ireson.createWaveform()
#    Qreson.createWaveform()
#
#    da1.stop()
#    da2.stop()
#    wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
#    wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
#    da1.writeWaveForm(wfdata1)
#    da2.writeWaveForm(wfdata2)
#    da1.start()
#    da2.start()
#    
#    dg1.delayAB=t_r*2
#    
#    r_area[i]=integrate.simps(Imod.rawWaveform,dx=1/da1.sampleRate)
#    for k in range(avg):
#        ad1.start()
#        data=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)
#        Dfft=np.fft.fft(data,axis=1).mean(axis=0)[8]
#        
##        I2,Q2=I.reshape(ad1.records,-1).mean(axis=0),Q.reshape(ad1.records,-1).mean(axis=0)
##        Ifft2,Qfft2=np.abs(np.fft.rfft(I2)),np.abs(np.fft.rfft(Q2))
#        Rabidata[i]=(Rabidata[i]*k+Dfft)/(k+1)
#        
#    print(i)
#    np.savez('Rabi_bias0.2mA-6',Rabidata=Rabidata,t_r=t_r,r_area=r_area,fr=fr,fq=fq,levelq=level_q,levelr=level_r,avg=avg)
#figure(),plot(r_area,np.abs(Rabidata))
##%%
#fq=6.482e9
#fr=6.733e9
#level_q=-10
#level_r=13
#mw1.freqency=fq
#mw2.freqency=fr
#mw1.level=level_q
#mw2.level=level_r
#mw1.set_output(True)
#mw2.set_output(True)
#
#t_meas=2e-6
#t_r=36*1e-9
#t_stim=np.linspace(0e-6,1e-6,401)
#tao=-5e-7
#N_hold=int(t_meas*da2.sampleRate)
#N_rise=int(t_r*da2.sampleRate)
#N_shift=int(tao*da2.sampleRate)
#
#l1=KILO_B(8)    #波形长度
#l2=KILO_B(4)
#Imod=WaveForm(length=l1,AWGType='spcm4')
#Qmod=WaveForm(length=l1,AWGType='spcm4')
#Ioff=WaveForm(length=l2,AWGType='spcm4')
#Ireson=WaveForm(length=l2,AWGType='spcm4')
#Qreson=WaveForm(length=l2,AWGType='spcm4')
#Z=WaveForm(length=l2,AWGType='spcm4')
#
#Ireson.createBase(func='cos',period=200)
#Qreson.createBase(func='sin',period=200)
#
#Ireson.createWindow((\
#                     ('rectangle',N_rise*2,N_rise*2+N_hold),\
#                     ))
#Qreson.createWindow((\
#                     ('rectangle',N_rise*2,N_rise*2+N_hold),\
#                     ))
#
#Ireson.createWaveform()
#Qreson.createWaveform()
#
#da1.stop()
#da2.stop()
#wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
#wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
#da1.writeWaveForm(wfdata1)
#da2.writeWaveForm(wfdata2)
#da1.start()
#da2.start()
#
#dg1.delayAB=t_r*2
#
#ad1.start()
#I,Q=ad1.data
#I1,Q1=I.reshape(ad1.records,-1),Q.reshape(ad1.records,-1)
#I2,Q2=np.zeros(ad1.records).astype('complex'),np.zeros(ad1.records).astype('complex')
#for i in range(ad1.records):
#    I2[i],Q2[i]=np.fft.rfft(I1[i,:])[8],np.fft.rfft(Q1[i,:])[8]
