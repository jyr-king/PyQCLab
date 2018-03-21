# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 14:22:06 2018

@author: jyr_king
"""

import numpy as np
from numpy.fft import rfft,rfftfreq
from math import pi,sqrt,atan
from matplotlib.pyplot import figure,plot
from scipy.optimize import leastsq
#G_I=1
#G_Q=1
#G_leakI=0.
#G_leakQ=0.
#theta=1
#
#N=10001
#samplerate=1e9
#
#f_LO= 20*1e6
#
#t=np.arange(N)/samplerate
#
#s_LO=np.cos(2*pi*f_LO*t)+1j*np.sin(2*pi*f_LO*t-theta)
#
#f_IF=1e6
#
#s_IF=G_I*np.cos(2*pi*f_IF*t)-1j*G_Q*np.sin(2*pi*f_IF*t-theta)
#
#s_RF=s_LO.real*s_IF.real+s_LO.imag*s_IF.imag+G_leakI*np.cos(2*pi*f_LO*t)+G_leakQ*np.sin(2*pi*f_LO*t-theta)
#
#s_RF_r=s_RF.real+s_RF.imag
#spectr_RF=rfft(s_RF)
#freq=rfftfreq(N,1/samplerate)
#
#figure(),plot(freq,np.abs(spectr_RF))
#figure(),plot(t,s_RF)

def fit_I(p,x,y):
    I_dc,m1,m2,n1,n2=p
    return I_dc+m1*np.cos(x)+n1*np.sin(x)+m2*np.cos(2*x)+n2*np.sin(2*x)-y

def fit_IQ(p,x,y):
    a0,a1,a2,b0,b1,b2=p
    S=a0+a1*x.real+a2*x.imag+1j*(b0+b1*x.real+b2*x.imag)
    return np.abs(S-y)

def cal_IQ(a0,I_d,I,Q,mu=1e-6):
    u=np.array([np.ones(I.size),I,Q])
    e=np.zeros(I.size)
    a=a0

    for k in range(1,I.size):
        e[k]=I_d[k]-(a*u[:,k]).sum()
        a=a+mu*u[:,k]*e[k]
    return a,e
        


if __name__ == '__main__':
    data=np.load('C:/Users/jyr_king/Documents/GitHub\PyQCLab/Utils/IQ_balance_cal_data1.npz')
    I,Q=data['I'],data['Q']
    samplerate=data['samplerate']
    #RF和LO的频率差：f_iq=f_rf-f_lo,下次记得存数据的时候就保存下来
    f_if = 1e6
    t=np.arange(I.size)/samplerate
    t_n=2*np.pi*f_if*t
    p0=[0,0,0,0,0]
    #将I按照傅里叶序列拟合，拟合到2阶：
    p,ier=leastsq(fit_I,p0,args=(t_n,I))
    #计算希望得到的校准后的I和Q：
    I_d=p[1]*np.cos(t_n)+p[3]*np.sin(t_n)+p[2]*np.cos(2*t_n)+p[4]*np.sin(2*t_n)
    Q_d=p[1]*np.cos(t_n-pi/2)+p[3]*np.sin(t_n-pi/2)+p[2]*np.cos(2*t_n-pi/2)+p[4]*np.sin(2*t_n-pi/2)
    #假设I_d和Q_d都是I和Q的线性组合，拟合出组合系数来：
    p2,ier2=leastsq(fit_IQ,[0,0,0,0,0,0],args=(I+1j*Q,I_d+1j*Q_d))    
    #反之，I，Q是I_d,Q_d的线性组合，拟合出组合系数：
    p3,ier3=leastsq(fit_IQ,[0,0,0,0,0,0],args=(I_d+1j*Q_d,I+1j*Q))
    #根据p3中得到的系数，还可以进一步得到修正的幅度和相位：
    G=sqrt(p3[-1]**2+p3[-2]**2)
    theta=atan(p3[-2]/p3[-1])
    
    