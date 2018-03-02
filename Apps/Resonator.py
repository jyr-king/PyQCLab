# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 19:22:37 2016

@author: Xmon-SC05
"""

from PyQCLab.Instrument.NetworkAnalyser import *
from PyQCLab.Utils.Qextractor import *
from PyQCLab.Utils.DigiFilters import savitzky_golay
from pylab import *
import time
import skrf as rf
import numpy as np

def getResonmode(S,thr=3,search_factor=10,smooth=False,smooth_window=5):
    '''This function try to find the indices of the resonator modes.
        it looks back and forward for depth's points for 3dB points, if both get true, 
        we can consider that a resonator mode must exist between this search interval.
        S: network data.
        depth: search depth around each point.
        emax: maximium error value.'''
    if smooth:
        S=savitzky_golay(S,smooth_window,3)
    modes=list()
    depth=int(search_factor*np.ceil(thr/np.abs(S[1:]-S[:-1]).max()))
    for i in range(depth,len(S)-depth):
#        e=min(np.abs(S[i-depth+1:i+depth]-S[i-depth:i+depth-1]).max(),emax)
        e=min(np.abs(S[i-depth+1:i+depth]-S[i-depth:i+depth-1]).max()/2,thr)
        if np.abs(S[i-depth+1:i+1]-S[i]-thr).min() < e and np.abs(S[i:i+depth]-S[i]-thr).min() < e:
            idx=S[i-depth:i+depth+1].argmin()+i-depth
            if idx not in modes:
                modes.append(idx)
    return modes

def getIndex(x,values):
    idx=list()
    for v in values:
        idx.append(np.abs(x-v).argmin())
    return idx
    
class Resonator(ZNB20,Qextractor):
    def __init__(self,f0=6e9,attenuation=0,instr_name='PNA'):
        ZNB20.__init__(self)
        Qextractor.__init__(self)
        self.f0=f0                      #谐振腔中心频率。
#        self.search_succeed=False       #腔模探测成功标记。
        self.freq=np.array([])
        self.sparam=np.array([]).astype('complex')
        self.magS_db=np.array([])
        self.attenuation=attenuation
        self.P0=[1e5,1e5,1,f0]
        self.mode=[]
        
    def searchMode(self,scan_params,search_factor=10):
        self.setSweep(scan_params)

        self.sweepType='lin'
        swp_time=self.points/self.IFbandwidth*self.average
        self.sweep()
        time.sleep(swp_time)
        self.fetchData()
        self.mode=getResonmode(self.magS_db,search_factor)
        
        if len(self.mode) > 1:
            print('{} modes were found at {}'.format(len(self.mode),self.freq[self.mode]))
            self.search_succeed=True
        elif len(self.mode) == 1:
            print('One mode was found at {}'.format(self.freq[self.mode]))
            self.f0=self.freq[self.mode[0]]
            self.search_succeed=True
        else:
            print('No mode was found.')
                       
    def normalScan(self,scan_params):
        self.setSweep(scan_params)
        self.sweepType('lin')
        wait=self.points/self.IFbandwidth*self.average
        self.sweep()
        time.sleep(wait)
        self.fetchData()
        
    def setScan(self,spans):
        self.span_broaden, self.span_whole=spans
                   
    def fineScan(self,scan_params,weight=[20,80]):
        IF,N,self.power,self.average=scan_params
        N1=int(N*weight[0]/100/2)
        N2=N-2*N1
        
        self.clearSegments()
        segment=[(self.f0-self.span_whole,self.f0-self.span_broaden,IF,N1),\
                (self.f0-self.span_broaden,self.f0+self.span_broaden,IF/10,N2),\
                (self.f0+self.span_broaden,self.f0+self.span_whole,IF,N1)]
        self.addSegments(segment)
        wait=(2*N1+10*N2)/IF*self.average
        self.sweep()
        time.sleep(wait)
        self.fetchData()
        
        self.P0[-1]=self.f0
        self.update2(self.P0,'UCSB')
        if self.q_succeed:
            print('Succeed! Power={}dBm, Qi={}, Qc={}, f0={} Hz.'.format(self.power,self.Qi,self.Qc,self.f0))
            return True
        else:
            print('Failed to extract Q factors.')
            return False
    
    def fetchData(self,meas='S21'):
        self.freq,self.sparam=self.getData()
        self.magS_db=rf.mag_2_db(abs(self.sparam))
        
class resonData():
    def __init__(self):
        self.data=list()
    
    def append(self,d):
        self.data.append(d)
    def concatenate(self):
        if len(self.data):
            self.powers=np.zeros(len(self.data))
            self.freq=np.zeros((len(self.data),len(self.data[0][1])))
            self.Sdata=np.zeros((len(self.data),len(self.data[0][2]))).astype('complex')
            self.Qdata=np.zeros((len(self.data),len(self.data[0][3])))
            
            for i in range(len(self.data)):
                self.powers[i]=self.data[i][0]
                self.freq[i,:]=self.data[i][1]
                self.Sdata[i,:]=self.data[i][2]
                self.Qdata[i,:]=self.data[i][3]
    def saveData(self,filename):
        np.savez(filename,powers=self.powers,freq=self.freq,Sdata=self.Sdata,Qdata=self.Qdata)        
        
    
        
        
            
                    
            
            
        
        