# -*- coding: utf-8 -*-
"""
Created on Wed May 10 09:23:23 2017
此模块提供SRS DG645的基本控制。
@author: A108QCLab
"""
import numpy as np
from PyQCLab.Instrument.instrument import *

class DG645(instrument):
    def __init__(self,instr_name='DG645'):
        instrument.__init__(self,instr_name)
        self.instrhandle.write('*RST')

    def _setDelayA(self,delay):
        self.instrhandle.write('DLAY 2,0,{}'.format(delay))
    def _getDelayA(self):
        delay_str=(self.instrhandle.query('DLAY?2')).split(',')
        return float(delay_str[1])
    delayA=property(fget=_getDelayA,fset=_setDelayA)

    def _setDelayB(self,delay):
        self.instrhandle.write('DLAY 3,0,{}'.format(delay))
    def _getDelayB(self):
        delay_str=(self.instrhandle.query('DLAY?3')).split(',')
        if delay_str[0] == '2':
            return float(delay_str[1])+self.delayA
        if delay_str[0] == '0':
            return float(delay_str[1])
    delayB=property(fget=_getDelayB,fset=_setDelayB)    

    def _setDelayC(self,delay):
        self.instrhandle.write('DLAY 4,0,{}'.format(delay))
    def _getDelayC(self):
        delay_str=(self.instrhandle.query('DLAY?4')).split(',')
        return float(delay_str[1])
    delayC=property(fget=_getDelayC,fset=_setDelayC)

    def _setDelayD(self,delay):
        self.instrhandle.write('DLAY 5,0,{}'.format(delay))
    def _getDelayD(self):
        delay_str=(self.instrhandle.query('DLAY?5')).split(',')
        if delay_str[0] == '4':
            return float(delay_str[1])+self.delayC
        if delay_str[0] == '0':
            return float(delay_str[1])
    delayD=property(fget=_getDelayD,fset=_setDelayD)

    def _setDelayE(self,delay):
        self.instrhandle.write('DLAY 6,0,{}'.format(delay))
    def _getDelayE(self):
        delay_str=self.instrhandle.query('DLAY?6')
        return float(delay_str.split(',')[1])
    delayE=property(fget=_getDelayE,fset=_setDelayE) 

    def _setDelayF(self,delay):
        self.instrhandle.write('DLAY 7,0,{}'.format(delay))
    def _getDelayF(self):
        delay_str=(self.instrhandle.query('DLAY?7')).split(',')
        if delay_str[0] == '6':
            return float(delay_str[1])+self.delayE
        if delay_str[0] == '0':
            return float(delay_str[1])
    delayF=property(fget=_getDelayF,fset=_setDelayF)
    
    def _setDelayG(self,delay):
        self.instrhandle.write('DLAY 8,0,{}'.format(delay))
    def _getDelayG(self):
        delay_str=self.instrhandle.query('DLAY?8')
        return float(delay_str.split(',')[1])
    delayG=property(fget=_getDelayG,fset=_setDelayG)

    def _setDelayH(self,delay):
        self.instrhandle.write('DLAY 9,0,{}'.format(delay))
    def _getDelayH(self):
        delay_str=(self.instrhandle.query('DLAY?9')).split(',')
        if delay_str[0] == '8':
            return float(delay_str[1])+self.delayG
        if delay_str[0] == '0':
            return float(delay_str[1])
    delayH=property(fget=_getDelayH,fset=_setDelayH) 

    def _setDelayAB(self,delay):
        self.instrhandle.write('DLAY 3,2,{}'.format(delay))
    def _getDelayAB(self):
        delay_str=(self.instrhandle.query('DLAY?3')).split(',')
        if delay_str[0] == '2':
            return float(delay_str[1])
        if delay_str[0] == '0':
            return float(delay_str[1])-self.delayA
    delayAB=property(fget=_getDelayAB,fset=_setDelayAB)

    def _setDelayCD(self,delay):
        self.instrhandle.write('DLAY 5,4,{}'.format(delay))
    def _getDelayCD(self):
        delay_str=(self.instrhandle.query('DLAY?5')).split(',')
        if delay_str[0] == '4':
            return float(delay_str[1])
        if delay_str[0] == '0':
            return float(delay_str[1])-self.delayC
    delayCD=property(fget=_getDelayCD,fset=_setDelayCD)

    def _setDelayEF(self,delay):
        self.instrhandle.write('DLAY 7,6,{}'.format(delay))
    def _getDelayEF(self):
        delay_str=(self.instrhandle.query('DLAY?7')).split(',')
        if delay_str[0] == '6':
            return float(delay_str[1])
        if delay_str[0] == '0':
            return float(delay_str[1])-self.delayE
    delayEF=property(fget=_getDelayEF,fset=_setDelayEF)

    def _setDelayGH(self,delay):
        self.instrhandle.write('DLAY 9,8,{}'.format(delay))
    def _getDelayGH(self):
        delay_str=(self.instrhandle.query('DLAY?9')).split(',')
        if delay_str[0] == '8':
            return float(delay_str[1])
        if delay_str[0] == '0':
            return float(delay_str[1])-self.delayG
    delayGH=property(fget=_getDelayGH,fset=_setDelayGH) 
    
    def trigSource(self,src='int'):
        trig_sources={'int':0,
                      'ext_r':1,
                      'ext_f':2,
                      'single_ext_r':3,
                      'single_ext_f':4,
                      'single':5,
                      'line':6
                      }
        self.instrhandle.write('TSRC {}'.format(trig_sources[src]))
    
    def trigRate(self,rate):
        rate=int(rate)
        self.instrhandle.write('TRAT {}'.format(rate))
        
    def burstOn(self,count,period):
        self.instrhandle.write('BURM 1')
        self.instrhandle.write('BURC {}'.format(count))
        self.instrhandle.write('BURP {}'.format(period))
    def burstOff(self):
        self.instrhandle.write('BURM 0')
        
    def start(self):
        self.instrhandle.write('*TRG')