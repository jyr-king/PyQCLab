# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 02:42:32 2016

@author: Xmon-SC05
"""
from PyQCLab.Instrument.instrument import instrument
import numpy as np

class AG33120_DC(instrument):
    def __init__(self,no):
        '''input: no the labeled number on the physical instrument. note: no must be a positive integer.'''
        instr_name='AG33120A'+str(no)
        super().__init__(instr_name)
        self.instrhandle.write('*RST')
        self.instrhandle.write('FUNCtion:SHAPe DC')
        
    def _setLevel(self,level):
        pass
    
    def _getLevel(self,level):
        pass
    
    def _setRang(self,rang):
        pass
    
    def _getRang(self,rang):
        pass
    
    def _setMode(self,mode):
        pass
    
    def _getMode(self):
        pass
    
    def _setOutput(self,state):
        pass
    
    def _getOutput(self):
        pass
    
    level=property(fget=_getLevel,fset=_setLevel)
    rang=property(fget=_getRang,fset=_setRang)
    mode=property(fget=_getMode,fset=_setMode)
    output=property(fget=_getOutput,fset=_setOutput)
        
class AG33120A(instrument):
    def __init__(self,instr_name='AG33120Aa'):
        instrument.__init__(self,instr_name)

        self.instrhandle.write('*RST')
        self.__level,self.__offset=self.get_level()
        self.__freqency=self.get_freqency()
        self.__function=self.get_function()
        
        
    def apply(self,param):
        '''apply命令比较简单直接。参数param设定为元组，格式为（‘波形函数名’，频率，幅度，偏置），暂不设置参数检查。
            波形函数名包括：SINusoid, SQUare,TRIangle, RAMP, NOISe, DC, USER.'''
        self.instrhandle.write('APPLy:{} {},{},{}'.format(param[0],param[1],param[2],param[3]))

    def set_level(self, level,offset=0):
        '''方波/锯齿波（三角波）输出幅度有最小值限制：1.5V.
            RAMP/NOISe波形最小幅度为0.3V。
            
        '''
        #level must >0 and <=10:
        if level > 10:
            print('Level out or range, using max value 10Vpp.')
            level=10
        elif level < 0.1:
            print('Level out or range, using min value 0.1Vpp.')
            level=0.1
            
        offset=min(2*level,5-level/2,abs(offset))*(-1 if offset < 0 else 1)
        
        self.instrhandle.write('VOLT:OFFS 0')    
        self.instrhandle.write('VOLTage {}'.format(level))
        self.instrhandle.write('VOLT:OFFS {}'.format(offset))
        self.__level,self.__offset=self.get_level()
        
    def get_level(self):
        return float(self.instrhandle.query('VOLTage?')),float(self.instrhandle.query('VOLTage:OFFSet?'))
        
    def set_freqency(self, freqency):
        self.instrhandle.write('FREQuency {}'.format(freqency))
        self.__freqency=self.get_freqency()
        
    def get_freqency(self):
        return float(self.instrhandle.query('FREQuency?'))

    def set_function(self, func_name):
        '''func_name: SINusoid|SQUare|TRIangle|RAMP|NOISe|DC|USER'''
        self.instrhandle.write('FUNCtion:SHAPe {}'.format(func_name))
        self.__function=self.get_function()
        
    def get_function(self):
        return self.instrhandle.query('FUNCtion:SHAPe?')
        
    def set_burstMode(self,cycles,rate,phase=0,bm_source='INT',state=True):
        self.instrhandle.write('BM:NCYCles {};BM:INTernal:RATE {};BM:PHASe {}'.format(cycles,rate,phase))
        self.instrhandle.write('BM:SOURce {}'.format(bm_source))        
        self.instrhandle.write('BM:STAT {}'.format('ON' if state else 'OFF'))
        
    def set_trigger(self,trig_source,trig_slop):
        '''trig_source:IMMediate|EXTernal|BUS,
            trig_slope:POSitive|NEGative'''
        self.instrhandle.write('TRIGger:SOURce {};TRIGger:SLOPe {}'.format(trig_source,trig_slop))
        
    def trigger(self):
        self.instrhandle.write('*TRG')
        
    def set_sweep(self,start,stop,step,dwell_time=0.01,state=True):
        pass


class yokogawa7651(instrument):
    '''The command format is: Command + Parameter+ Terminator. 
        "E" is the trigger command that execute the commands changing the output settings.
        "CR LF, LF, EOI and ";", all can be accept as a terminator.'''
    def __init__(self, instr_name='YOKOGAWA7651'):
        instrument.__init__(self, instr_name)
#        self.instrhandle=self.get_handle()
        self.instrhandle.write('RC')
    def setFunc(self,func):
        if func in ['dcV','dcv','v','V']:
            self.instrhandle.write('F1;E')
        elif func in ['dcI','dci','i','I']:
            self.instrhandle.write('F5;E')
        
    def set_range(self,dc_func,dc_range):
        ranges={'10mV':'R2','100mV':'R3',
                '1V':'R4','10V':'R5','30V':'R6',
                '1mA':'R4','10mA':'R5','100mA':'R6'
                }
        if dc_func in ['dcV','dcv','v','V']:
            self.instrhandle.write('{};E'.format(ranges[dc_range]))
        elif dc_func in ['dcI','dci','i','I']:
            self.instrhandle.write('{};E'.format(ranges[dc_range]))
            
    def set_level(self,level,autorange=False):
        polarity='-' if level < 0 else'+'
        level=abs(level)
        if level == 0:
            lvl_str='0.0'
            pwr_str='0'
        else:
            lvl_str=str(level/10**(np.floor(np.log10(abs(level)))-1))
            pwr_str=str(np.floor(np.log10(level))-1).split('.')[0]
        if len(lvl_str)>5:
            lvl_str=lvl_str[:5]
        if autorange:
            self.instrhandle.write('SA{}{}E{};E'.format(polarity,lvl_str,pwr_str))
        else:
            self.instrhandle.write('S{}{}E{};E'.format(polarity,lvl_str,pwr_str))
            
    def set_stepup(self,digit):
        self.instrhandle.write('UP{};E'.format(digit))
        
    def set_stepdown(self,digit):
        self.instrhandle.write('DW{};E'.format(digit))    
            
    def set_output(self,state=True):
        self.instrhandle.write('O{};E'.format(1 if state else 0))
        
class GS200(instrument):
    levels_I= {
                'MIN':'1E-3',
                '1mA':'1E-3',
                '10mA':'10e-3',
                '100mA':'100e-3',
                '200mA':'200e-3',
                'MAX':'200e-3',
                }
    levels_V= {
                'MIN':'10e-3',
                '10mV':'10e-3',
                '100mV':'100e-3',
                '1V':'1E+0',
                '10V':'10E+0',
                '30V':'30E+0',
                'MAX':'30E+0',
                }
    def __init__(self,instr_name='DC6'):
        instrument.__init__(self,instr_name)
        self.instrhandle.write('*RST')
        self.mode='V'
        self.rang='1V'
        self.level=0
        self.output=0
        
        
    def _setMode(self,mode='dcV'):
        if mode in ('V','dcV','v','dcv','volt','voltage'):
            self.instrhandle.write(':SOUR:FUNC VOLT')
            self._mode='V'
        elif mode in ('I','i','dcI','dci','curr','current'):
            self.instrhandle.write(':SOUR:FUNC CURR')
            self._mode='I'
        else:
            return
        
    def _getMode(self):
        return self._mode
    
    mode=property(fget=_getMode,fset=_setMode)
    
    def _setLevel(self,level):
        if abs(level) > self.rang:
            print('Warning: level out of range. using MAXimum value instead.')
            level = -self.rang if level < 0 else self.rang
        self.instrhandle.write(':SOUR:LEV {}'.format(level))
        self._level=level
        
    def _getLevel(self):
        return self._level
    
    level=property(fget=_getLevel,fset=_setLevel)
    
    def _setRange(self,rang_kwd):
        if self.mode == 'I' and rang_kwd in self.levels_I.keys():
            rang=self.levels_I[rang_kwd]
        elif self.mode == 'V' and rang_kwd in self.levels_V.keys():
            rang=self.levels_V[rang_kwd]
        else:
            print('No such range, using MAXimum range instead.')
            rang=self.levels_I['MAX']
        self.instrhandle.write(':SOUR:RANG {}'.format(rang))
        self._rang=float(rang)
        
    def _getRange(self):
        return self._rang
        
    rang=property(fget=_getRange,fset=_setRange)
    
    def _setOutput(self,state):
        if state in ('on','ON','On',True,1):
            self.instrhandle.write(':OUTP 1')
            self._output=1
        elif state in ('off','Off','OFF',False,0):
            self.instrhandle.write(':OUTP 0')
            self._output=0
            
    def _getOutput(self):
        return self._output
    
    output=property(fget=_getOutput,fset=_setOutput)
        
