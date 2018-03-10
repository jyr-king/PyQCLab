# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 09:56:03 2018
State decider: processing the readout signal and decide which state the qubits are on.
@author: jyr_king
"""
import numpy as np
from matplotlib.pyplot import figure,plot
from PyQCLab.Utils.WaveForm_Gen import *

#parameter for kaiser window.
BETA=8

class State_Decider:
    def __init__(self,data,samplerate):
        if len(data.shape) == 1:
            data=data.reshape([-1,1])
        self.data=data
        self.n_samples,self.repeats=data.shape
        self.samplerate=samplerate
        
        self.detect_freqs=[]
        self.signals=[]
        self.update()
        
    def update(self,window=None):
        if window == 'kaiser':
            window=np.kaiser(self.n_samples,BETA)
            correction=self.n_samples/np.trapz(window)
            data=self.data*(window.reshape([-1,1])*np.ones(self.repeats))
        else:
            data=self.data
            correction=1
        self.spectrum = np.fft.fft(data,axis=0)*correction
        self.freq = np.fft.fftfreq(self.n_samples,1/self.samplerate)
        self.signals=[]
        for f in self.detect_freqs:
            idx=np.abs(self.freq-f).argmin()
            self.signals.append(2*self.spectrum[idx][0]/self.n_samples)
        
    def add_detection(self,freq):
        self.detect_freqs.append(freq)
        
    def add_detections(self,freqs):
        for freq in freqs:
            self.add_detection(freq)
        
    
if __name__ == '__main__':
    L=1001
    samplerate=1000e6

    w=WaveForm(L,samplerate)
    w.base.insert(100,gaussian(100,0.5))
#Add three carrier frequencies to the waveform:
    c1=Carrier(L,samplerate,freq=10e6,phase=math.pi*0.7,offset=0.)
    c2=Carrier(L,samplerate,freq=5e6,phase=math.pi*0.3,offset=0.)
    c3=Carrier(L,samplerate,freq=20e6,phase=math.pi*0.5,offset=0.)
    w.carrier.adds([c1,c2,c3])
    w.carrier.update()
#Set an offset:
    w.carrier.offset=0.
#update the waveform data:
    w.update('spcm4')
    
    sd1=State_Decider(w.carrier.value,samplerate)
    sd1.add_detections([c1.frequency,c2.frequency,c3.frequency])
    sd1.update()
#    sd1.update(window='kaiser')
    
    figure(),plot(sd1.freq,2*np.abs(sd1.spectrum)/sd1.n_samples)
    
    for (f,sig) in zip(sd1.detect_freqs,sd1.signals):
        print('detection at {}: amp={:.2f}, phase={:.2f}pi'.format(f,np.abs(sig),np.angle(sig)/np.pi))