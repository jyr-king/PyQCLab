# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 22:44:26 2018

@author: jyr_king
"""
from PyQCLab.Instrument.instrument import instrument
import numpy as np

class Awg5014C(instrument):
    def __init__(self,instr_name='AWG5014C'):
        super().__init__(instr_name)
        self.instrhandle.write('*RST')
        self.getInstr_Information()
        
    def getInstr_Information(self):
        pass
    
    def _setSampleRate(self,samplerate):
        pass
    
    def _getSampleRate(self):
        pass
    
    samplerate=property(fget=_getSampleRate,fset=_setSampleRate)
    
    def setRange(self,rang,ch):
        pass
    
    def setRangeAll(self,rang):
        pass
    
    def setRunMode(self,mode):
        pass
    
    def setTriggerSource(self,trig_source):
        pass
    
    def setTriggerMode(self,mode):
        pass
    
    def setTriggerCoupling(self,coupling):
        pass
    
    def setTriggerImpedance(self,impedance):
        pass
    
    def setTrigger(self,**kwargs):
        pass
    
    def setMarkerH(self,ch,marker,level):
        pass
    
    def getMarkerH(self,ch,marker):
        pass
    
    def setMarkerL(self,ch,marker,level):
        pass
    
    def getMarkerL(self,ch,marker):
        pass
    
    def setDirect_Output(self,ch):
        pass
    
    def setDirect_OutputAll(self):
        pass
    
    def chEnable(self,ch):
        pass
    
    def chEnableAll(self):
        pass
    
    def setOutput(self,ch):
        pass
    
    def setOutputAll(self):
        pass
    
    def writeWaveForm(self,wfdata):
        pass
    
    def readWaveForm(self):
        pass
    
    def assignWaveForm(self,wf_name,ch):
        pass
    
    def start(self):
        pass
    
    def stop(self):
        pass

