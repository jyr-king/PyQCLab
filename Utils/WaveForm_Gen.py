
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:21:11 2016

@author: Xmon-SC05
"""
import numpy as np
from matplotlib.pyplot import figure,plot
from PyQCLab.etc.awg_config import *
#from PyQCLab.Instrument.pyspcm import KILO
import math

def gaussian_r(length,std):
    return gaussian(length*2,std)[:length]
def gaussian_f(length,std):
    return gaussian(length*2,std)[length:]
def kaiser_r(length,beta):
    return mKaiser(length*2,beta)[:length]
def kaiser_f(length,beta):
    return mKaiser(length*2,beta)[length:]
def bartlett_r(length,*args):
    return np.bartlett(length*2)[:length]
def bartlett_f(length,*args):
    return np.bartlett(length*2)[length:]
   
def gaussian(length,std):
    x=np.arange(length)
    std *= length
    cut=np.exp(-(length-1)**2/8/std**2)
    return (np.exp(-(x-(length-1)/2)**2/2/std**2)-cut)/(1-cut)

def tangential(length,sigma=1):
    x=np.arange(length)
    sigma*=length
    A=1/(2*math.tanh((length-1)/2/sigma)-math.tanh(0)-math.tanh((length-1)/sigma))
    B=A*(math.tanh(0)+math.tanh((length-1)/sigma))
    return A*(np.tanh(x/sigma)+np.tanh((length-1-x)/sigma))-B

def mKaiser(length,beta=4):
    x=np.kaiser(length,beta)
    return (x-x[0])/(x[length//2]-x[0])

def rectangle(length):
    return np.ones(length)

def cosin(length):
    x=np.arange(length)
    return np.cos((x-(length-1)/2)*math.pi/(length-1))

def expand(x,length):
    y=np.zeros(len(x)+length)
    idx=len(x)//2
    y[:idx]=x[:idx]
    y[idx:idx+length]=np.ones(length)
    y[idx+length:]=x[idx:]
    return y  

class BaseBand:
    def __init__(self,length):   
        self.length=int(length)
        self.reset()
        
    def reset(self):
        self.value=np.zeros(self.length)
        
    def insert(self,start,x):
        '''insert a segment "x" into the wavefrom(baseband) at start point "start".'''
        length=len(x)
        self.value[start:start+length]=x
    
    def inserts(self,start,segments):
        for i in range(len(segments)):
            if i > 0:
                start+=len(segments[i-1])
            self.insert(start,segments[i])
            
    def gain(self,factor=1):
        self.value *= factor
        if self.value.max() > 1 or self.value.min() < -1:
            self.normalize() 
    
    def normalize(self):
        Max=np.abs(self.value).max()
        self.value /= Max
        
    def step(self,d):
        self.value += d
        if self.value.max() > 1 or self.value.min() < -1:
            self.normalize()
            
    def shift(self,points):
        L,R=self.value[:-points].copy(),self.value[-points:].copy()
        self.value[:points]=R
        self.value[points:]=L
        
    def offset(self,offset):
        if self.value.max()+offset < 1 and self.value.min()+offset > -1:
            self.value += offset

class Carrier:
    def __init__(self,length,samplerate,func=np.cos,freq=0,phase=0,offset=0):
        self.length=length
        self.samplerate=samplerate
        self._frequency=freq
        self._func=func
        self._phase=phase
        self._offset=offset
        self.update()
 
    def normalize(self):
        Max=np.abs(self.value).max()
        if Max > 1e-16:
            self.value /= Max       

        
    def _setFrequency(self,freq):
        self._frequency=freq
        self.update()
    
    def _getFrequency(self):
        return self._frequency
    
    def _setPhase(self,phase):
        self._phase=phase
        self.update()
    
    def _getPhase(self):
        return self._phase
    
    def _setOffset(self,offset):
        self._offset=offset
        self.update()
    
    def _getOffset(self):
        return self._offset
    
    def _setFunc(self,func):
        self._func=func
        self.update()
        
    def _getFunc(self):
        return self._func

    frequency=property(fget=_getFrequency,fset=_setFrequency)
    phase=property(fget=_getPhase,fset=_setPhase)
    offset=property(fget=_getOffset,fset=_setOffset)
    func=property(fget=_getFunc,fset=_setFunc)
    
    def gain(self,factor=1):
        self.value *= factor
        if self.value.max() > 1 or self.value.min() < -1:
            self.normalize() 
            
    def update(self):
        x=np.arange(self.length)
        self.value=self.func(2*np.pi*self.frequency/self.samplerate*x+self.phase)+self.offset
        self.normalize()
                
    def __add__(self,another_carrier):
        c=Carrier(self.length,self.samplerate)
        c.value=self.value+another_carrier.value
        c.normalize()
        return c

class Carriers(Carrier):
    def __init__(self,length,samplerate):
        self.carrier_list=[]
        super().__init__(length,samplerate)
        
        
    def add(self,carr):
        if carr.length == self.length and carr.samplerate == self.samplerate:
            self.carrier_list.append(carr)
    
    def adds(self,carrs):
        for carr in carrs:
            self.add(carr)
            
    def update(self):
        self.value=np.zeros(self.length)
        for carr in self.carrier_list:
            self.value+=carr.value
        self.value += self._offset
        self.normalize()
              
        
    
        
class WaveForm:
    digit_depth={'awg5000':14,'spcm4':16}
    markers={'awg5000':2,'spcm4':0}
    dataFormats={'awg5000':'uint16','spcm4':'int16'}
    
    def __init__(self,length,samplerate):
        self.length=int(length)
        self.samplerate=samplerate
#        self.AWGType=AWGType
        self.base=BaseBand(self.length)
        self.carrier=Carriers(self.length,self.samplerate)
        self.marker1=BaseBand(self.length)
        self.marker2=BaseBand(self.length)
#        self.update(awg_type)
        
    def update(self,awg_type):
        self.raw_waveform=self.base.value*self.carrier.value
        depth=digit_depth[awg_type]
        d_type=dataFormats[awg_type]
        if d_type == 'uint16':
            self.waveform=(self.raw_waveform*2**(depth-1)+2**(depth-1)-self.raw_waveform).astype('uint16')
        elif d_type == 'int16':
            self.waveform=(self.raw_waveform*2**(depth-1)-self.raw_waveform).astype('int16')
            
        if awg_type in ['awg5000']:
            self.waveform+=self.marker1.value.astype('uint16')*2**depth+self.marker2.value.astype('uint16')*2**(depth+1)
     
    def func_generator(self,freq,phase=0,offset=0,func=np.cos):
        self.length=int(self.samplerate/freq)
        freq_actual=self.samplerate/self.length
        self.base=BaseBand(self.length)
        self.base.insert(0,rectangle(self.length))
        self.carrier=Carrier(self.length,samplerate=self.samplerate,freq=freq_actual,phase=phase,offset=offset,func=func)
        
        
        
if __name__ == '__main__':
    L=10*1024
    samplerate=1250000000
    w=WaveForm(L,samplerate)
    w.func_generator(22e6,func=np.sin,phase=0.5*np.pi)
#    w.base.insert(1000,gaussian(2000,0.5))
#    
#    c1=Carrier(L,samplerate,freq=1e7,phase=math.pi*0.5,offset=0.)
#    c2=Carrier(L,samplerate,freq=0.5e7,phase=math.pi,offset=0.)
#    c3=Carrier(L,samplerate,freq=1e6,phase=math.pi,offset=0.)
#    w.carrier.adds([c1,c2,c3])
#    w.carrier.update()
#    w.carrier.offset=0.3
    w.update('spcm4')
    
    figure()
    plot(w.waveform)
    