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
import math
from scipy import integrate
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

tao=0      #qubit激发后到开始测量的延时

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

Imod.createWindow((('kaiser_r',N_t1*2-N_shift*2-N_rise*4-N_stim*2,N_t1*2-N_shift*2-N_rise*2-N_stim*2,beta,1),\
                   ('rectangle',N_t1*2-N_shift*2-N_rise*2-N_stim*2,N_t1*2-N_shift*2-N_rise*2,0,1),\
                   ('kaiser_f',N_t1*2-N_shift*2-N_rise*2,N_t1*2-N_shift*2,beta,1)\
                   ))
Qmod.createWindow((\
                   ('rectangle',0,0,0,0),\
                   
                   ))
Ioff.createWindow((('rectangle',N_t1-N_shift-N_stim-N_rise*2,N_t1-N_shift,0,1),\
                   ))

Ireson.createBase(func='cos',period=f_b*l2/da2.sampleRate)    #读出腔脉冲基带波形，I
Qreson.createBase(func='sin',period=f_b*l2/da2.sampleRate,phase=np.pi)  #读出腔脉冲基带波形，Q，相移pi，为了保证合成波形为cos[(omega_LO+omega_IF)*t].

Ireson.createWindow((\
                     ('rectangle',N_t1,N_t1+N_hold,0,1),\
                     ))
Qreson.createWindow((\
                     ('rectangle',N_t1,N_t1+N_hold,0,1),\
                     ))

Imod.createWaveform()
Qmod.createWaveform()
Ioff.createWaveform()
Ireson.createWaveform()
Qreson.createWaveform()
dg1.delayAB=t1+0.51e-6
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
fq=6.48405e9
fr=6.7187e9
mw1.level=-10       #qubit激发强度
mw2.level=13        #读出腔激发强度，13是给到IQ mixer LO端用于解调信号的，给到读出腔的实际经过了定向耦合器的20dB衰减+20dB衰减器+IQ mixer衰减+线上衰减。
mw2.freqency=fr
mw1.freqency=fq
mw1.set_output(True)
mw2.set_output(True)
#%%
#-------------加X方向微波的Ramsey。-------------------------------------------#
N_window=51
fq=6.488e9
mw1.freqency=fq
tao=np.linspace(0,1e-6,51)
SEdataX=np.zeros(tao.size)
SEdataX2=np.zeros(tao.size).astype('complex')

N=10
idx=np.abs(np.fft.fftfreq(ad1.recordlength,d=1/ad1.samplerate)+f_b).argmin()
figure()

for i in range(tao.size):
    N_tao=int(tao[i]*da2.sampleRate)
    Imod.createWindow((('kaiser',N_t1*2-N_window,N_t1*2,12,1),\
                       ('kaiser',N_t1*2-N_window*3-N_tao*2,N_t1*2-N_window-N_tao*2,12,1),\
                       ('kaiser',N_t1*2-N_window*4-N_tao*4,N_t1*2-N_window*3-N_tao*4,12,1)\
                   ))
    Ioff.createWindow((('rectangle',N_t1-math.ceil(N_window/2),N_t1,0,1),\
                       ('rectangle',N_t1-math.ceil(3*N_window/2)-N_tao,N_t1-math.floor(N_window/2)-N_tao,0,1),\
                       ('rectangle',N_t1-N_window*2-N_tao*2,N_t1-math.floor(3*N_window/2)-N_tao*2,0,1)\
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
    
    S=np.zeros(N)
    for k in range(N):
        ad1.start()
        D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
#        Dfft=np.fft.fft(D,axis=1).mean(axis=0)[idx]                 #对采样数据做fft，取平均，然后取出信号频率点的值。
#        Dfft_n=(Dfft-center)*np.exp(-1j*angle)
#        S[k]=Dfft_n.real > 0
        Dfft=np.fft.fft(D,axis=1)[:,idx]
#        Dfft_n=(Dfft-center)*np.exp(-1j*angle)
#        S[k]=(Dfft_n.real > 0).sum()
        SEdataX2[i]=(SEdataX2[i]*k+Dfft.mean())/(k+1)
#    S=S*np.exp(1j*2*np.pi*f_b*tao[i])
#    plot(S.real,S.imag)
#    SEdataX[i]=S.sum()
    np.savez('c5q5_SpinEchoX-7',SEdataX=SEdataX,SEdataX2=SEdataX2,tao=tao,fr=fr,fq=fq) 
    print(i)
plot(tao,np.abs(SEdataX2))
#%%
N_window=51
T=500e-9
W=500e-9
N_T=int(T*da2.sampleRate)
N_W=int(W*da2.sampleRate)
fq=np.linspace(0,100e6,51)+6.43e9
tao=np.linspace(-0.1,1,56)*1e-6
PNdata=np.zeros([fq.size,tao.size]).astype('complex')

Ireson.createWindow((('rectangle',N_t1-N_T-N_W,N_t1-N_T),\
                     ('rectangle',N_t1,N_t1+N_hold),\
                     ))
Qreson.createWindow((('rectangle',N_t1-N_T-N_W,N_t1-N_T),\
                     ('rectangle',N_t1,N_t1+N_hold),\
                     ))
Ireson.createWaveform()
Qreson.createWaveform()

N=4
idx=np.abs(np.fft.fftfreq(ad1.recordlength,d=1/ad1.samplerate)+f_b).argmin()
figure()

for l in range(tao.size):
    N_tao=int(tao[l]*da2.sampleRate)
 
    #Ireson.createWindow((\
    #                     ('rectangle',N_t1,N_t1+N_hold),\
    #                     ))
    #Qreson.createWindow((\
    #                     ('rectangle',N_t1,N_t1+N_hold),\
    #                     ))
    Imod.createWindow((\
                       ('kaiser',N_t1*2-N_window*2-N_T*2-N_W*2+N_tao*2,N_t1*2-N_T*2-N_W*2+N_tao*2,12),\
                       ))
    Ioff.createWindow((\
                       ('rectangle',N_t1-N_window-N_T-N_W+N_tao,N_t1-N_T-N_W+N_tao),\
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
   
    for i in range(fq.size):
        mw1.freqency=fq[i]
#        S=np.zeros(N)
        for k in range(N):
            ad1.start()
            D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
    #        Dfft=np.fft.fft(D,axis=1).mean(axis=0)[idx]                 #对采样数据做fft，取平均，然后取出信号频率点的值。
    #        Dfft_n=(Dfft-center)*np.exp(-1j*angle)
    #        S[k]=Dfft_n.real > 0
            Dfft=np.fft.fft(D,axis=1)[:,idx]
#            Dfft_n=(Dfft-center)*np.exp(-1j*angle)
#            S[k]=(Dfft_n.real > 0).sum()
            PNdata[i,l]=(PNdata[i,l]*k+Dfft.mean())/(k+1)
#    S=S*np.exp(1j*2*np.pi*f_b*tao[i])
#    plot(S.real,S.imag)
#    SEdataX[i]=S.sum()
    print(l,fq[np.abs(PNdata[:,l]).argmax()]/1e9)
    np.savez('c5q5_PhotonNumber-spectrum-6',PNdata=PNdata,T=T,W=W,tao=tao,fr=fr,fq=fq)
#plot(fq,np.abs(PNdata))
pcolor(np.abs(PNdata))
#%%
N_window=85
T=500e-9
W=500e-9
t_r=100e-9
t_f=50e-9
N_rise=int(t_r*da2.sampleRate)
N_fall=int(t_f*da2.sampleRate)
N_T=int(T*da2.sampleRate)
N_W=int(W*da2.sampleRate)
fq=np.linspace(0,200e6,51)+6.3e9
tao=np.linspace(0,1,51)*1e-6
PNdata=np.zeros([fq.size,tao.size]).astype('complex')

Ireson.createWindow((('kaiser_f',N_t1-N_T-N_fall,N_t1-N_T,8,0.5),\
                     ('kaiser',N_t1-N_T-N_fall-N_W-N_rise,N_t1-N_T-N_fall-N_W+N_rise,8,1),\
                     ('rectangle',N_t1-N_T-N_fall-N_W+int(N_rise/2),N_t1-N_T-N_fall,0,0.5),\
                     ('kaiser_f',N_t1+N_W+int(N_rise/2),N_t1+N_W+int(N_rise/2)+N_fall,8,0.5),\
                     ('kaiser',N_t1,N_t1+N_rise*2,8,1),\
                     ('rectangle',N_t1+int(3*N_rise/2),N_t1+N_W+int(N_rise/2),0,0.5),\
                     ))
Qreson.createWindow((('kaiser_f',N_t1-N_T-N_fall,N_t1-N_T,8,0.5),\
                     ('kaiser',N_t1-N_T-N_fall-N_W-N_rise,N_t1-N_T-N_fall-N_W+N_rise,8,1),\
                     ('rectangle',N_t1-N_T-N_fall-N_W+int(N_rise/2),N_t1-N_T-N_fall,0,0.5),\
                     ('kaiser_f',N_t1+N_W+int(N_rise/2),N_t1+N_W+int(N_rise/2)+N_fall,8,0.5),\
                     ('kaiser',N_t1,N_t1+N_rise*2,8,1),\
                     ('rectangle',N_t1+int(3*N_rise/2),N_t1+N_W+int(N_rise/2),0,0.5),\
                     ))
Ireson.createWaveform()
Qreson.createWaveform()

N=1
idx=np.abs(np.fft.fftfreq(ad1.recordlength,d=1/ad1.samplerate)+f_b).argmin()
figure()

for l in range(tao.size):
    N_tao=int(tao[l]*da2.sampleRate)
 
    #Ireson.createWindow((\
    #                     ('rectangle',N_t1,N_t1+N_hold),\
    #                     ))
    #Qreson.createWindow((\
    #                     ('rectangle',N_t1,N_t1+N_hold),\
    #                     ))
    Imod.createWindow((\
                       ('kaiser',N_t1*2-N_window*2-N_T*2-N_W*2+N_tao*2,N_t1*2-N_T*2-N_W*2+N_tao*2,12,1),\
                       ))
    Ioff.createWindow((\
                       ('rectangle',N_t1-N_window-N_T-N_W+N_tao,N_t1-N_T-N_W+N_tao,0,1),\
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
   
    for i in range(fq.size):
        mw1.freqency=fq[i]
#        S=np.zeros(N)
        for k in range(N):
            ad1.start()
            D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
    #        Dfft=np.fft.fft(D,axis=1).mean(axis=0)[idx]                 #对采样数据做fft，取平均，然后取出信号频率点的值。
    #        Dfft_n=(Dfft-center)*np.exp(-1j*angle)
    #        S[k]=Dfft_n.real > 0
            Dfft=np.fft.fft(D,axis=1)[:,idx]
#            Dfft_n=(Dfft-center)*np.exp(-1j*angle)
#            S[k]=(Dfft_n.real > 0).sum()
            PNdata[i,l]=(PNdata[i,l]*k+Dfft.mean())/(k+1)
#    S=S*np.exp(1j*2*np.pi*f_b*tao[i])
#    plot(S.real,S.imag)
#    SEdataX[i]=S.sum()
    print(l,fq[np.abs(PNdata[:,l]).argmin()]/1e9)
    np.savez('c5q5_PhotonNumber-spectrum-10',PNdata=PNdata,T=T,W=W,tao=tao,fr=fr,fq=fq)
#plot(fq,np.abs(PNdata))
pcolor(np.abs(PNdata))
#%%
N_window=91
T=500e-9
W=500e-9
t_r=100e-9
t_f=50e-9
N_rise=int(t_r*da2.sampleRate)
N_fall=int(t_f*da2.sampleRate)
N_T=int(T*da2.sampleRate)
N_W=int(W*da2.sampleRate)
fq=6.484e9
mw1.freqency=fq
fr=np.linspace(-10e6,10e6,101)+6.7187e9
tao=0
Sdata1=np.zeros(fr.size).astype('complex')

Ireson.createWindow((\
                     ('kaiser_f',N_t1+N_W+int(N_rise/2),N_t1+N_W+int(N_rise/2)+N_fall,8,0.5),\
                     ('kaiser',N_t1,N_t1+N_rise*2,8,1),\
                     ('rectangle',N_t1+int(3*N_rise/2),N_t1+N_W+int(N_rise/2),0,0.5),\
                     ))
Qreson.createWindow((\
                     ('kaiser_f',N_t1+N_W+int(N_rise/2),N_t1+N_W+int(N_rise/2)+N_fall,8,0.5),\
                     ('kaiser',N_t1,N_t1+N_rise*2,8,1),\
                     ('rectangle',N_t1+int(3*N_rise/2),N_t1+N_W+int(N_rise/2),0,0.5),\
                     ))
Ireson.createWaveform()
Qreson.createWaveform()

N=2
idx=np.abs(np.fft.fftfreq(ad1.recordlength,d=1/ad1.samplerate)+f_b).argmin()
#figure()


N_tao=int(tao*da2.sampleRate)
 
#Ireson.createWindow((\
#                     ('rectangle',N_t1,N_t1+N_hold),\
#                     ))
#Qreson.createWindow((\
#                     ('rectangle',N_t1,N_t1+N_hold),\
#                     ))
Imod.createWindow((\
                   ('kaiser',N_t1*2-N_window*2+N_tao*2,N_t1*2+N_tao*2,12,1),\
                   ))
Ioff.createWindow((\
                   ('rectangle',N_t1-N_window+N_tao,N_t1+N_tao,0,1),\
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
   
for i in range(fr.size):
    mw2.freqency=fr[i]
#        S=np.zeros(N)
    for k in range(N):
        ad1.start()
        D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
#        Dfft=np.fft.fft(D,axis=1).mean(axis=0)[idx]                 #对采样数据做fft，取平均，然后取出信号频率点的值。
#        Dfft_n=(Dfft-center)*np.exp(-1j*angle)
#        S[k]=Dfft_n.real > 0
        Dfft=np.fft.fft(D,axis=1)[:,idx]
#            Dfft_n=(Dfft-center)*np.exp(-1j*angle)
#            S[k]=(Dfft_n.real > 0).sum()
        Sdata1[i]=(Sdata1[i]*k+Dfft.mean())/(k+1)
#    S=S*np.exp(1j*2*np.pi*f_b*tao[i])
#    plot(S.real,S.imag)
#    SEdataX[i]=S.sum()
    print(i,np.abs(Sdata1[i]))
    
#plot(fq,np.abs(PNdata))
np.savez('c5q5_resonator_S21_e-8',Sdata1=Sdata1,T=T,W=W,tao=tao,fr=fr,fq=fq)
angS=np.unwrap(np.angle(Sdata1))
angSn=angS-angS[0]-(angS[-1]-angS[0])/(fr[-1]-fr[0])*(fr-fr[0])
subplot(211),plot(fr,np.abs(Sdata1))
subplot(212),plot(fr,angSn)
#%%
#%%
N_window=np.linspace(10,1000,199).astype('int')
P_area=np.zeros(N_window.size)
T=500e-9
W=500e-9
t_r=100e-9
t_f=50e-9
N_rise=int(t_r*da2.sampleRate)
N_fall=int(t_f*da2.sampleRate)
N_T=int(T*da2.sampleRate)
N_W=int(W*da2.sampleRate)
fq=6.484e9
mw1.freqency=fq
fr=np.linspace(-10e6,10e6,201)+6.715e9
tao=0
Sdata=np.zeros([N_window.size,fr.size]).astype('complex')

Ireson.createWindow((\
                     ('kaiser_f',N_t1+N_W+int(N_rise/2),N_t1+N_W+int(N_rise/2)+N_fall,8,0.5),\
                     ('kaiser',N_t1,N_t1+N_rise*2,8,1),\
                     ('rectangle',N_t1+int(3*N_rise/2),N_t1+N_W+int(N_rise/2),0,0.5),\
                     ))
Qreson.createWindow((\
                     ('kaiser_f',N_t1+N_W+int(N_rise/2),N_t1+N_W+int(N_rise/2)+N_fall,8,0.5),\
                     ('kaiser',N_t1,N_t1+N_rise*2,8,1),\
                     ('rectangle',N_t1+int(3*N_rise/2),N_t1+N_W+int(N_rise/2),0,0.5),\
                     ))
Ireson.createWaveform()
Qreson.createWaveform()

N=1
idx=np.abs(np.fft.fftfreq(ad1.recordlength,d=1/ad1.samplerate)+f_b).argmin()
figure()


N_tao=int(tao*da2.sampleRate)
 
#Ireson.createWindow((\
#                     ('rectangle',N_t1,N_t1+N_hold),\
#                     ))
#Qreson.createWindow((\
#                     ('rectangle',N_t1,N_t1+N_hold),\
#                     ))
for l in range(N_window.size):
    Imod.createWindow((\
                       ('kaiser',N_t1*2-N_window[l]*2+N_tao*2,N_t1*2+N_tao*2,12,1),\
                       ))
    Ioff.createWindow((\
                       ('rectangle',N_t1-N_window[l]+N_tao,N_t1+N_tao,0,1),\
                       ))
    
    Imod.createWaveform()
    Ioff.createWaveform()
    P_area[l]=integrate.simps(Imod.window)/da1.sampleRate
          
    da1.stop()
    da2.stop()
    wfdata1=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
    wfdata2=np.array([Ioff.waveform,Ireson.waveform,Qreson.waveform,Z.waveform]).flatten('F')
    da1.writeWaveForm(wfdata1)
    da2.writeWaveForm(wfdata2)
    da1.start()
    da2.start()
   
    for i in range(fr.size):
        mw2.freqency=fr[i]
    #        S=np.zeros(N)
        for k in range(N):
            ad1.start()
            D=(ad1.data[0]+1j*ad1.data[1]).reshape(ad1.records,-1)      #将采集信号合成为复信号，并根据记录次数分段。
    #        Dfft=np.fft.fft(D,axis=1).mean(axis=0)[idx]                 #对采样数据做fft，取平均，然后取出信号频率点的值。
    #        Dfft_n=(Dfft-center)*np.exp(-1j*angle)
    #        S[k]=Dfft_n.real > 0
            Dfft=np.fft.fft(D,axis=1)[:,idx]
    #            Dfft_n=(Dfft-center)*np.exp(-1j*angle)
    #            S[k]=(Dfft_n.real > 0).sum()
            Sdata[l,i]=(Sdata[l,i]*k+Dfft.mean())/(k+1)
#    S=S*np.exp(1j*2*np.pi*f_b*tao[i])
#    plot(S.real,S.imag)
#    SEdataX[i]=S.sum()
    np.savez('c5q5_rabi_2D-2',Sdata=Sdata,N_window=N_window,P_area=P_area,fr=fr,fq=fq)
    print(l)
    
#plot(fq,np.abs(PNdata))

#angS=np.unwrap(np.angle(Sdata))
#angSn=angS-angS[0]-(angS[-1]-angS[0])/(fr[-1]-fr[0])*(fr-fr[0])
#subplot(211),plot(fr,np.abs(Sdata1))
#subplot(212),plot(fr,angSn)