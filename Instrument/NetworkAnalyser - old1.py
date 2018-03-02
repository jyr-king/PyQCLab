# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:20:29 2016
网络分析仪子类。目前包括R&S的ZNB系列和Agilent的PNA系列。
@author: Xmon-SC05:Jin Yirong
"""
import sys
import numpy as np
from enum import Enum
sys.path.append('.')
#from instrument import instrument
from instrument import *
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
#        self.__instr_handle.write('CALC1:PAR:DEF "ch1_S21",S21')
#        self.__instr_handle.write('DISP:WIND1:TRAC1:FEED "ch1_S21"')
#        self.__instr_handle.write('MMEM:STOR:TRAC:FORM:SNP DB')
#        self.__instr_handle.write('TRIG:CONT:OFF')
        self.instrhandle.write('*RST')
        self.instrhandle.write('INIT:CONT OFF')
        self.channel=1
        self.measDict={}
        self.getMeas()
        self.clearMeas()
        self.__measCount=0
                
#        self.clearTrace()
##        测量计数：
##
##        默认添加S21：
        self.addMeas('S21')
#   
#    def addMeas(self,meas,name=None):
#        if meas not in self.measDict.keys():
#            self.__measCount+=1
#            
#            if not name:
#                name='Meas_'+meas
#            self.instrhandle.write(
#                "CALCulate:PARameter:DEFine:EXT '{}',{}".format(name,meas))
##            self.instrhandle.write(
##                'DISPlay:WINDow:STATE ON'.format(self.__measCount))
#            self.instrhandle.write(
#                "DISPlay:WINDow:TRACe{}:FEED '{}'".format(self.__measCount,name))
#            
#            self.measDict[meas]=(name,self.__measCount)
#        else:
#            return
    def getMeas(self):
        mlist=(self.instrhandle.query('CALC:PAR:CAT:EXT?')).split(',')
        self.__measDict=dict()
        M=int(len(mlist)/2)
        if M > 0:
            for i in range(M):
                if mlist[i] not in self.__measDict.keys():
                    self.__measDict[mlist[i]]=mlist[i+1]
#                
    def addMeas(self,meas,name=None,trace=1):
        if not name:
            name='CH{}_{}_{}'.format(self.channel,meas,trace)
        if meas in self.M_PARAM and name not in self.__measDict.keys():
            self.instrhandle.write(
                "CALCulate:PARameter:DEFine:EXT '{}',{}".format(name,meas))
            self.__measDict[name]=meas
                
    def delMeas(self,name):
        if name in self.__measDict.keys():
            self.instrhandle.write(
                "CALCulate:PARameter:DELete '{}'".format(self.measDict[name]))
            self.measDict.pop(name)
#            
#    def modMeas(self,name,meas):
#        if name in self.__measDict.keys():
#            self.instrhandle.write(
#                "CALCulate:PARameter:SELect '{}'".format(name))
#            self.instrhandle.write(
#                "CALCulate:PARameter:MODify:EXTended '{}'".format(meas))
#            self.__measDict[name]=meas
    def clearMeas(self):
        for name in self.measDict.keys():
            self.delMeas(name)
#    
    def addTrace(self,meas):
        pass
    
    def delTrace(self,trace):
        pass
        
        
    def sweep(self):
        self.instrhandle.write('INIT:IMM; *WAI')
        
    def addSegment(self,seg):
        pass
        
    def getData(self,name=None,fmt=False):
        if name:
            self.instrhandle.write('CALCulate:PARameter:SELect "{}"'.format(name))            
        if fmt:
            data=np.array(self.instrhandle.query('CALC:DATA? FDAT').split(',')).astype('float')
        else:
            data=np.array(self.instrhandle.query('CALC:DATA? SDAT').split(',')).astype('float').reshape(len(data)/2,2)
            data=data[:,0]+data[:,1]*1j
        f=np.array(self.instrhandle.query('CALC:DATA:STIM?').split(',')).astype('float')
        return f,data
        
    def setSweep(self,start, stop, IF, N, p, avg=1):
        self.fstart=start
        self.fstop=stop
        self.IFbandwidth=IF
        self.points=N
        self.average=avg
        self.power=p
    

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
        
        