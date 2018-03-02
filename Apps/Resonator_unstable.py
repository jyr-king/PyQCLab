# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 19:22:37 2016

@author: Xmon-SC05
"""

from PyQCLab.Instrument.NetworkAnalyser import *
from PyQCLab.Utils.Qextractor import *
from PyQCLab.Utils.DigiFilters import savitzky_golay
#from pylab import *
from array import array
import numpy as np
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
    
class Resonator():
    def __init__(self,Analyser=ZNB20(),Qextractor=Qextractor()):
        self.modes=np.array([])
        self.freq=np.array([])
        self.Sdata=np.array([])
        self.Qdata=np.array([])
        self.search_succeed=False
        self.powers=np.array([])
#        self.magS_db=0
#        self.SData=list()
#        self.Smatrix=0
#        self.powers=list()
#        self.Qparam=list()
#        self.attenuation=0
#        self.idx_3db=0
#        self.idx_broaden=0
#        self.mode=0
#        self.P=[1e5,1e5,1,f0]
#    def searchMode(self,)    
    def searchMode(self,pwr,IF0=1000,points=1001,span0=1e6,avg=1,MaxTimes=3,search_factor=5,sweep=True):
#        self.fcenter,self.fspan,self.power,self.IFbandwidth,self.points=self.f0,span0,pwr,IF0,points
        fstart,fstop=self.f0-span0/2,self.f0+span0/2
        self.setSweep([fstart,fstop,IF0,points,pwr,avg])
        sf=search_factor
#        self.q_succeed=False
#        self.search_succeed=False
        if self.search_succeed:
            print('A good search result has already gotten. Nothing will do.')
            return
        else:
            count=0
            while not self.search_succeed and count < MaxTimes:
                if sweep:
    #                self.sweepType='lin'
                    swp_time=self.points/self.IFbandwidth*self.average
                    self.sweep()   
                    time.sleep(swp_time)
                    self.fetchData()
#            else:
#                if not self.Smatrix:
#                    print('You must search by the Analyzer first. Nothing will be done.')
#                    break
                mode=getResonmode(self.magS_db,sf)
                self.mode=mode
                if len(mode)==0:
                    print('No resonance mode was found, we will try again.')
                    count+=1
                    if sweep:
                        self.fspan=2*self.fspan
                        self.points=2*self.points
                    else:
                        sf*=2
#                    swp_time=self.points/self.IFbandwidth*self.average
                        continue
                elif len(mode) > 1:
                    print('More than 1 mode were found, Please check manually.')
    #                self.success=True
                    break
                else:
                    fcenter=self.freq[mode[0]]
                    self.P[-1]=fcenter
                    self.update(self.P,'UCSB')                
    #                fcenter=self.Smatrix[mode[0],0]
    #                magS=self.Smatrix[:,3]
    #                magS_L,magS_R=magS[:mode[0]+1],magS[mode[0]:]
    #                d=magS.mean()-magS.std()
    #                idx_broaden=[abs(magS_L-d).argmin(),abs(magS_R-d).argmin()+mode[0]]
    #                idx_3db=[abs(magS_L-magS_L[-1]-3).argmin(),abs(magS_R-magS_R[0]-3).argmin()+mode[0]]
    ##                f_3db=self.Smatrix[[abs(magS_L-magS_L[-1]-3).argmin(),abs(magS_R-magS_R[0]-3).argmin()+mode[0]],0]
    #                span_broaden=self.Smatrix[idx_broaden,0].std()
    #                span_3db=self.Smatrix[idx_3db,0].std() 
                    if self.q_succeed:
                        print('One mode was found at {} GHz, with Qi={},Qc={}'.format(fcenter,self.Qi,self.Qc))
                        self.f0=fcenter
                        self.search_succeed=True
                        self.optimizeScan()
                    else:
                        count+=1
                        if sweep:
                            self.fspan=2*self.fspan
                            self.points=2*self.points
                        else:
                            sf*=2
#                        swp_time=1.1*self.points/IF0*self.average
    #                if input('Please confirm the result (y/n) :') in ['y','Y']:
    #                    self.f0=fcenter
    #                    self.span_3db=span_3db
    #                    self.span_broaden=span_broaden
    #                    self.idx_broaden=idx_broaden
    #                    self.idx_3db=idx_3db
    #                    self.success=True
    #                else:
    #                    print('Search continued.')
    #                    count+=1
    #                    self.fspan=2*self.fspan
    #                    self.points*=2
    #                    swp_time=1.1*self.points/IF0*self.average
                        
                if count > MaxTimes:
                    print('Maximum search times reached, search failed.')
                
    def optimizeScan(self,span_factor=10):
        self.span_3db=self.f0/self.Qi
        self.span_broaden=self.f0/self.Qi/self.Qc*(self.Qi+self.Qc)
        self.span_whole=self.span_broaden*span_factor
#        q=Qextractor()
#        self.span_whole=self.span_broaden*10
#        self.fineScan(power,IF,N)
#        q.freq=self.Smatrix[:,0]
#        q.sparam=dbphase2complex(self.Smatrix[:,3],self.Smatrix[:,4],deg=True)
#        q.update(self.P)
#        if q.succeed:
#            self.P=q.P
#            self.f0=q.f0
#            self.span_3db=q.f0/q.Qi
#            self.span_broaden=q.f0/q.Qi/q.Qc*(q.Qi+q.Qc)
#            self.span_whole=self.span_broaden*10
#        else:
#            print('Optimize failed for mode at {} Hz.'.format(self.f0))
#        self.clearData()
        
    def normalScan(self,scan_param):
#        fstart,fstop,IF,points,power,avg=scan_param
        self.setSweep(scan_param)
        self.sweepType('lin')
        wait=self.points/self.IFbandwidth*self.average
        self.sweep()
        time.sleep(wait)
        self.fetchData()
        
    def setScan(self,f0,span_3db,span_broaden,span_whole):
        self.f0,self.span_3db,self.span_broaden,self.span_whole=f0,span_3db,span_broaden,span_whole
        
            
    def fineScan(self,pwr,IF=200,N=101,weight=[20,40,40],avg=1):
        if not self.search_succeed:
            print('You cannot start fineScan befor get resonator information by searchMode.')
            return
        else:
#            self.optimizeScan()
            #create segments:
            N1=int(N*weight[0]/100/2)
            N2=int(N*weight[1]/100/2)
            N3=N-2*(N1+N2)
            #the average times will increase when the nominal power is lower than -60 dBm.
#            if pwr+self.attenuation < -60:
#                self.average=int(2**int((-60-pwr-self.attenuation+3)/3))
#            else:
#                self.average=1
            #create and add segments.
            self.average=avg
            self.clearSegments()
            segment=[(self.f0-self.span_whole,self.f0-self.span_broaden,IF,N1),\
                    (self.f0-self.span_broaden,self.f0-self.span_3db,IF/10,N2),\
                    (self.f0-self.span_3db,self.f0+self.span_3db,IF/100,N3),\
                    (self.f0+self.span_3db,self.f0+self.span_broaden,IF/10,N2),\
                    (self.f0+self.span_broaden,self.f0+self.span_whole,IF,N1)]
            self.addSegments(segment)
            self.power=pwr
    #        self.q_succeed=False
            wait=(2*(N1+N2)+100*N3)/IF*self.average
            self.sweep()
            time.sleep(wait)
            self.fetchData()
            self.update(self.P,'UCSB')
            if self.q_succeed:
                print('Succeed! Power={}dBm, Qi={}, Qc={}, f0={} Hz.'.format(self.power,self.Qi,self.Qc,self.f0))
                return True
            else:
                print('Failed to extract Q factors.')
                return False
#        self.SData.append(self.Smatrix[:,[0,3,4]])
#        self.powers.append(power+self.attenuation)
    
    def fetchData(self,meas='S21'):
        if meas in self.M_PARAM and meas in self.measurements.values():
            data=self.getData(snp=True)
            self.freq=data[:,0]
            if meas=='S11':
                self.sparam=dbphase2complex(data[:,1],data[:,2])
            elif meas=='S21':
                self.sparam=dbphase2complex(data[:,3],data[:,4])
            elif meas=='S12':
                self.sparam=dbphase2complex(data[:,5],data[:,6])
            elif meas=='S22':
                self.sparam=dbphase2complex(data[:,7],data[:,8])
            self.magS_db=rf.mag_2_db(abs(self.sparam))
            
        
#    def saveData(self,filename):
#        np.savez(filename,power=np.array(self.powers),SData=np.array(self.SData))
#        
#    def delData(self,dnum):
#        self.powers.pop(dnum)
#        self.SData.pop(dnum)
#        
#    def clearData(self):
#        self.powers=list()
#        self.SData=list()
#        
        
        
    
        
        
            
                    
            
            
        
        