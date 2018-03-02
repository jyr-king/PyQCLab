# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:20:29 2016
网络分析仪子类。目前包括R&S的ZNB系列和Agilent的PNA系列。
@author: Xmon-SC05:Jin Yirong
"""
#import sys
import numpy as np
from enum import Enum
#sys.path.append('.')
from PyQCLab.Instrument.instrument import *
from PyQCLab.Instrument.instr_config import *
from time import sleep

class NetworkAnalyser(instrument):
    FREQMAX=20e9
    FREQMIN=10e6
    POWMAX=5
    POWMIN=-27
    POINTMIN=1
    POINTMAX=100001
    IFMIN=1
    IFMAX=15000000
    
#    SWP_MODES={'hold':0,'cont':1,'gro':2,'sing':3}
    SWP_MODES=Enum('swpMode','hold cont gro sing')
#    SWP_TYPES={'lin':0,'log':1,'pow':2,'cw':3,'segm':4,'phas':5}
    SWP_TYPES=Enum('swpType','lin log pow cw segm phas')
    M_PARAM=['S11','S21','S12','S22']
    def __init__(self, instr_name):
        instrument.__init__(self, instr_name)      
        self.instrhandle.write('*RST')
        self.instrhandle.write('INIT:CONT OFF')
        self.measurements={}        
        self.clearMeas()

        #默认添加S21：
        self.addMeas('S21')
   
    def getMeas(self):
        mlist=(self.instrhandle.query('CALC:PAR:CAT:EXT?')).split(',')
        M=int(len(mlist)/2)
        if M > 0:
            for i in range(M):
                if mlist[i] not in self.measurements.keys():
                    self.measurements[mlist[i]]=mlist[i+1]
                
    def addMeas(self,meas,name=None,trace=1):
        if meas in self.M_PARAM and meas not in self.measurements.values():
            if not name:
                name='CH1_{}'.format(meas)
            self.instrhandle.write(
            "CALCulate:PARameter:DEFine:EXT '{}',{}".format(name,meas))
#            trace=self.instrhandle.query('CALC:PAR:TNUM?')
            self.instrhandle.write('DISP:WIND:TRAC{}:FEED "{}"'.format(trace,name))
            self.measurements[name]=meas
        else:
            print('A wrong measurement was assigned, or already existed. Nothing will do.')
            
                
    def delMeas(self,name):
        if name in self.measurements.keys():
            self.instrhandle.write(
                "CALCulate:PARameter:DELete '{}'".format(name))
            self.measurements.pop(name)
        else:
            print('Wrong name assigned, nothing will do.')
            
    def modMeas(self,name,meas):
        if meas in self.M_PARAM and name in self.measurements.keys():
            if self.measurements[name]==meas:
                print('Identical measurement was assigned, nothing will do.')
            else:
                self.instrhandle.write(
                    "CALCulate:PARameter:SELect '{}'".format(name))
                self.instrhandle.write(
                    "CALCulate:PARameter:MODify:EXTended '{}'".format(meas))
                self.measurements[name]=meas
            
    def clearMeas(self):
        self.instrhandle.write('CALCulate:PARameter:DELete:ALL')
        self.measurements.clear()
    
    def sweep(self):
        for i in range(self.average):
            self.instrhandle.write('INIT:IMM; *WAI')
        
    def addSegment(self,seg):
        '''Add a single segment. In the form: (fstart,fstop,IFbandwidth,points).'''
        if not self.sweepType=='segm':
            self.sweepType='segm'
            self.instrhandle.write('SENS:SEGM:BWID:CONT ON')    # enable independently set of IFbandwidth.
        #unpack the segment parameters:
        fstart,fstop,IF,points=seg
        #get how many segments are set now:
        N=int(self.instrhandle.query('SENS:SEGM:COUNt?'))
        self.instrhandle.write('SENS:SEGM{}:ADD'.format(N+1))  # Add a new segment.
        self.instrhandle.write('SENS:SEGM{}:STATE ON'.format(N+1)) #Activate this segment.        
        self.instrhandle.write('SENS:SEGM{}:BWID:RES {}Hz'.format(N+1,IF)) 
        self.instrhandle.write('SENS:SEGM{}:FREQ:START {}'.format(N+1,fstart))
        self.instrhandle.write('SENS:SEGM{}:FREQ:STOP {}'.format(N+1,fstop))
        self.instrhandle.write('SENS:SEGM{}:SWE:POIN {}'.format(N+1,points))
    
    def addSegments(self,segs):
        '''batch add multiple segments. 'segs' must be a list,tuple or array of seg.'''
        for seg in segs:
            self.addSegment(seg)
            
    def delSegment(self,snum):
        self.instrhandle.write('SENS:SEGM{}:DEL'.format(snum))
        
    def clearSegments(self):
        self.instrhandle.write('SENS:SEGM:DEL:ALL')
        
    def getData(self,name=None,snp=False):
        if name and name in self.measurements.keys():
            self.instrhandle.write('CALCulate:PARameter:SELect "{}"'.format(name))
#        else:
#            name=self.instrhandle.query('CALCulate:PARameter:SELect?')[1:-2]
#            self.instrhandle.write('CALCulate:PARameter:SELect "{}"'.format(name))
        if snp:
            return np.array(self.instrhandle.query('CALC:DATA:SNP:PORTs? "1,2"').split(',')).astype('float').reshape(9,-1).T            
#        if fmt:
#            data=np.array(self.instrhandle.query('CALC:DATA? FDAT').split(',')).astype('float')
        else:
            data=np.array(self.instrhandle.query('CALC:DATA? SDATA').split(',')).astype('float').reshape(-1,2)
            return data[:,0]+data[:,1]*1j
#        f=np.array(self.instrhandle.query('CALC:DATA:STIM?').split(',')).astype('float')
#        return f,data
        
    def setSweep(self,swp_param):
        '''swp_param: in the form: [fstart,fstop,IFbandwidth,swp_points,power,avg_times].'''
        if not self.sweepType=='lin':
            self.sweepType='lin'
        #unpack parameters:
        self.fstart,self.fstop,self.IFbandwidth,self.points,self.power,self.average=swp_param#,self.fminf
            
    def _getFreqStart(self):
        return float(self.instrhandle.query('SENSe:FREQuency:STARt?'))
    def _setFreqStart(self,freq):
        if freq > self.FREQMAX:
            freq=self.FREQMAX
        elif freq < self.FREQMIN:
            freq=self.FREQMIN
        self.instrhandle.write('SENSe:FREQuency:STARt {}'.format(freq))
    def _getFreqStop(self):
        return float(self.instrhandle.query('SENSe:FREQuency:STOP?'))
    def _setFreqStop(self,freq):
        if freq > self.FREQMAX:
            freq=self.FREQMAX
        elif freq < self.FREQMIN:
            freq=self.FREQMIN
        elif freq < self.fstart:
            freq=self.fstart
        self.instrhandle.write('SENSe:FREQuency:STOP {}'.format(freq))
    def _getFreqCenter(self):
        return float(self.instrhandle.query('SENSe:FREQuency:CENTer?'))
    def _setFreqCenter(self,freq):
        if freq > self.FREQMAX:
            freq=self.FREQMAX
        elif freq < self.FREQMIN:
            freq=self.FREQMIN
        self.instrhandle.write('SENSe:FREQuency:CENTer {}'.format(freq))
    def _getFreqSpan(self):
        return float(self.instrhandle.query('SENSe:FREQuency:SPAN?'))
    def _setFreqSpan(self,freq):
        if freq/2+self.fcenter > self.FREQMAX:
            freq=2*(self.FREQMAX-self.fcenter)
        elif self.fcenter-freq/2 < self.FREQMIN:
            freq=2*(self.fcenter-self.FREQMIN)
        self.instrhandle.write('SENSe:FREQuency:SPAN {}'.format(freq))
    def _getPoints(self):
        return float(self.instrhandle.query('SENSe:SWEep:POINts?'))
    def _setPoints(self,p):
        p=int(p)
        if p < self.POINTMIN:
            p = self.POINTMIN
        elif p > self.POINTMAX:
            p = self.POINTMAX
        self.instrhandle.write('SENSe:SWEep:POINts {}'.format(p))
    def _getIFBandwidth(self):
        return float(self.instrhandle.query('Sense:Bandwidth?'))
    def _setIFBandwidth(self,IF):
        if IF > self.IFMAX:
            IF=self.IFMAX
        elif IF < self.IFMIN:
            IF=self.IFMIN
        self.instrhandle.write('Sense:Bandwidth {}'.format(IF))
    def _getPower(self):
        return float(self.instrhandle.query('SOURce:POWer?'))
    def _setPower(self,p):
        if p > self.POWMAX:
            p=self.POWMAX
        elif p < self.POWMIN:
            p=self.POWMIN
        self.instrhandle.write('SOURce:POWer {}'.format(p))
    def _getAverage(self):
        return int(self.instrhandle.query('SENSe:AVERage:COUNt?'))
    def _setAverage(self,N):
        N=int(N)
        if N > 1:
            self.instrhandle.write('SENS:AVER ON')
            self.instrhandle.write('SENS:AVER:CLE')
            self.instrhandle.write('SENS:AVER:MODE AUTO')
            self.instrhandle.write('SENSe:AVERage:COUNt {}'.format(N))
        else:
            self.instrhandle.write('SENS:AVER OFF')
            self.instrhandle.write('SENSe:AVERage:COUNt 1')
    def _getSweepMode(self):
        return self.instrhandle.query('SENSe:SWEep:MODE?')[:-1].lower()
    def _setSweepMode(self,mode):
        self.instrhandle.write('SENSe:SWEep:MODE {}'.format(mode))
    def _getSweepType(self):
        return self.instrhandle.query('SENSe:SWEep:TYPE?')[:-1].lower()
    def _setSweepType(self,t):
        self.instrhandle.write('SENSe:SWEep:TYPE {}'.format(t))
   

        
    fstart=property(fget=_getFreqStart,fset=_setFreqStart)
    fstop=property(fget=_getFreqStop,fset=_setFreqStop)
    fcenter=property(fget=_getFreqCenter,fset=_setFreqCenter)
    fspan=property(fget=_getFreqSpan,fset=_setFreqSpan)
    points=property(fget=_getPoints,fset=_setPoints)
    power=property(fget=_getPower,fset=_setPower)
    IFbandwidth=property(fget=_getIFBandwidth,fset=_setIFBandwidth)
    average=property(fget=_getAverage,fset=_setAverage)
    sweepMode=property(fget=_getSweepMode,fset=_setSweepMode)
    sweepType=property(fget=_getSweepType,fset=_setSweepType)
 
        
    def set_sweep(self, start, stop, IF, N, avg=1):
#        self.__instr_handle.write('SENS1:SWE:TYPE SEGM')
        #set frequency range:
        if isinstance(start, (float,int)) and isinstance(stop, (float,int)):
            self.instrhandle.write('SENS:FREQ:STAR '+str(start))
            self.instrhandle.write('SENS:FREQ:STOP '+str(stop))
        else :
            print('The type of "start" or "stop" is error, please retype, this function will not start.')
            return 0
        #set IFbandwidth:
        if isinstance(IF,int):
            self.instrhandle.write('SENS:BAND:RES '+str(IF))
        else:
            print('IF bandwidth setting should be integer >1,please retype. this function will not start.')
            return 0
        #set sweep number of points:
        if isinstance(N,int):
            self.instrhandle.write('SENS:SWE:POIN '+str(N))
        else:
            print('sweep number of points should be integer,please retype. this function will not start.')
            return 0
        #set average times:
        if avg > 1 and isinstance(avg,int):        
            self.instrhandle.write('SENS:AVER:STAT ON')
            self.instrhandle.write('SENS:AVER:CLE')
            self.instrhandle.write('SENS:AVER:COUN ' + str(avg))
            self.instrhandle.write('SENS:AVER:MODE AUTO')
        else :
            self.instrhandle.write('SENS:AVER:COUN 1')
            self.instrhandle.write('SENS:AVER:STATE OFF')

#        for i in range(len(IF)):
#            idx = str(i + 1)
#            self.__instr_handle.write('SENS1:SEGM' + idx + ':ADD')
#            self.__instr_handle.write('SENS1:SEGM' + idx + ':STATE ON')
#            self.__instr_handle.write('SENS1:SEGM' + idx + ':BWID:RES ' + str(IF[i]) + 'Hz')
#            self.__instr_handle.write('SENS1:SEGM' + idx + ':FREQ:START ' + str(freq[i]))
#            self.__instr_handle.write('SENS1:SEGM' + idx + ':FREQ:STOP ' + str(freq[i + 1]))
#            self.__instr_handle.write('SENS1:SEGM' + idx + ':SWE:POIN ' + str(N[i]))
#            self.__instr_handle.write('SENS1:SEGM' + idx + ':X:SPAC OBAS')
#
#        self.__instr_handle.write('OUTP ON')
#        self.__instr_handle.write('SENS1:SWE:GRO:COUN ' + str(avg))
#        self.__instr_handle.write('SENS1:SWE:MODE GRO')

    def set_level(self, level):
        try:
            level = float(level)
        except:
            print('level given here may be illegal, float, int or all number string are accepted.')
        if 12 > level > -60:
            self.__instr_handle.write('SOUR:POW ' + str(level))
            self.level = float(self.__instr_handle.query('SOUR:POW?'))
        else:
            raise ValueError('The given level value is out of range (-27 to 5dBm).')
        return self.level
        
    def set_format(self,Fmt):
        if Fmt in ['MLIN','MLOG','PHAS','UPH','POL','SMIT','ISM','GDEL','REAL','IMAG','SWR']:
            self.__instr_handle.write('CALC:FORM '+Fmt)
        else:
            print('Wrong format was given, nothing been done.')
            
    def get_data(self):
        data=self.__instr_handle.query('CALC:DATA? SDAT')
        f=self.__instr_handle.query('CALC:DATA:STIM?')
        data=data.split(',')
        f=f.split(',')
        for i in range(len(data)):
            data[i]=float(data[i])
            if i < len(data)/2:
                f[i]=float(f[i])
        f=np.array(f)
        data=np.array(data).reshape(len(data)/2,2)
        data=data[:,0]+data[:,1]*1j
        return f,data
        
    def start_sweep(self):
        self.__instr_handle.write('INIT:IMM; *WAI')

    def abort_sweep(self):
        self.__instr_handle.write('abort')
        
class ZNB20(NetworkAnalyser):
    FREQMAX=20e9
    FREQMIN=100e3
    POWMAX=10
    POWMIN=-80
    POINTMIN=1
    POINTMAX=100001
    IFMIN=1
    IFMAX=15000000
    
    def __init__(self,instr_name='ZNB20'):
        instrument.__init__(self,instr_name)
        self.instrhandle.write('*RST')
        self.instrhandle.write('INIT:CONT OFF')
        self.measurements={}
        
    def sweep(self):
#        swptime=float(self.instrhandle.query('SENSe:SWEep:TIME?'))
#        wait=np.ceil(self.average*swptime)
        self.instrhandle.write('SENSe:SWEep:COUNt {}'.format(self.average))
        self.instrhandle.write('INIT:IMM; *WAI')
#        sleep(wait)
        
    def addSegment(self,seg):
        fstart,fstop,IF,points=seg
        N=int(self.instrhandle.query('SENS:SEGM:COUNt?'))
        self.instrhandle.write('SENS:SEGM{}:ADD'.format(N+1))  # Add a new segment.
        self.instrhandle.write('SENS:SEGM{}:STATE ON'.format(N+1)) #Activate this segment.        
        self.instrhandle.write('SENS:SEGM{}:BWID:RES {}Hz'.format(N+1,IF)) 
        self.instrhandle.write('SENS:SEGM{}:FREQ:START {}'.format(N+1,fstart))
        self.instrhandle.write('SENS:SEGM{}:FREQ:STOP {}'.format(N+1,fstop))
        self.instrhandle.write('SENS:SEGM{}:SWE:POIN {}'.format(N+1,points))
        if not self.sweepType=='segm':
            self.sweepType='segm'
            self.instrhandle.write('SENS:SEGM:BWID:CONT ON')
            
    def getData(self):
        data=np.array(self.instrhandle.query('CALC:DATA? SDAT').split(',')).astype('float').reshape(-1,2)
        f=np.array(self.instrhandle.query('CALC:DATA:STIM?').split(',')).astype('float')
        return f,data[:,0]+data[:,1]*1j
        
        
    
        
    