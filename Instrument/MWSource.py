# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:20:29 2016
微波源的类。目前包括R&S SMF100A，SMB100A
@author: Xmon-SC05:Jin Yirong
"""
import numpy as np
from .instrument import instrument

class RS_MWSource(instrument):
    FREQ_MAX=20e9
    FREQ_MIN=1e9
    LVL_MAX=18
    LVL_MIN=-90
    
    def __init__(self, instr_name):
        instrument.__init__(self, instr_name)
        self.instrhandle.write('*RST')
        
#频率的设置和获取方法：        
    def _setFreqency(self, freq):
        freq=float(freq)
        if freq < self.FREQ_MIN:
            print('Warning:freqency set too low, min= 1GHz. min value will be used.')
            freq=self.FREQ_MIN
            self.instrhandle.write('FREQ:CW {}Hz'.format(freq))
        elif freq > self.FREQ_MAX:
            print('Warning:freqency set too high, max= 20GHz. max value will be used.')
            freq=self.FREQ_MAX
        self.instrhandle.write('FREQ:CW {}Hz'.format(freq)) 
    def _getFreqency(self):
        return float(self.instrhandle.query('FREQ:CW?'))
#幅度的设置和获取方法：        
    def _setLevel(self,level):
        self.instrhandle.write(':POW {}'.format(level))
    def _getLevel(self):
        return float(self.instrhandle.query(':POW?'))
#相位的设置和获取方法：
    def _setPhase(self,phase):
        pass
    def _getPhase(self):
        pass
    
    freqency=property(fget=_getFreqency,fset=_setFreqency)
    level=property(fget=_getLevel,fset=_setLevel)
    phase=property(fget=_getPhase,fset=_setPhase)
    
    def set_freqency(self, freq, offset=0, multiplier=1):
        try:
            # 目前的理解，offset和multiplier不影响输出的频率，只是影响面板读数。测试方知。
            # 为了便于控制，频率统一以Hz为单位，不接受KHz、MHz和GHz单位
            freq = float(freq)
            offset = float(offset)
            multiplier = float(multiplier)
        except:
            print('Error:Wrong input format. Nothing will be done!')
        fmax,fmin=int(2e10),int(1e9)    
        if freq < fmin:
            print('Warning:freqency set too low, min= 1GHz. min value will be used.')
            freq=fmin
            self.__instr_handle.write('FREQ:CW {}Hz'.format(freq))
        elif freq > fmax:
            print('Warning:freqency set too high, max= 20GHz. max value will be used.')
            freq=fmax
        self.__instr_handle.write('FREQ:CW {}Hz'.format(freq))        
        self.__instr_handle.write('FREQ:OFFS {}Hz'.format(offset))
        self.__instr_handle.write('FREQ:MULT {}'.format(multiplier))
        self.__freqency = self.get_freqency()
        
        return self.__freqency

    def set_level(self, level, offset=0):
        try:
            level = float(level)
            offset = float(offset)
        except:
            print('Error:Wrong input format. Nothing will be done!')
        lvl_max,lvl_min=18,-130
        if level > lvl_max:
            print('Warning:level set too high (max=18dB), max value will be used.')
            level=lvl_max
        elif level < lvl_min:
            print('Warning:level set too low (min=-130dB), min value will be used.')
            level=lvl_min
        self.__instr_handle.write(':POW {}'.format(level))
        self.__instr_handle.write(':POW:OFFS {}'.format(offset))
        self.__level = self.get_level()
        
        return self.__level

    def set_phase(self, phase,deg=True):
        try:
            phase = float(phase)
        except:
            print('phase given here may be wrong in format, float, int or all number string are accepted.')
        phase_max,phase_min=720,-720
        if not deg:
            phase=np.rad2deg(phase)
        if phase > phase_max:
            print('Warning:phase set too high (max=720), max value will be used.')
            phase=phase_max
        elif phase < phase_min:
            print('Warning:phase set too low (min=-720), min value will be used.')
            phase=phase_min
        
        self.instrhandle.write(':PHAS {}DEG'.format(phase))
        self.__phase = self.get_phase()
        
        return self.__phase

    def set_output(self, state):        
        self.instrhandle.write('OUTP:STAT {}'.format('ON' if state else 'OFF'))
        self.__state = self.get_state()
        return self.__state

    def set_sweepfreq(self, start,stop,step,dwell=1e-2,spacing='LIN'):
        self.__instr_handle.write('SOUR:FREQ:STAR {} GHz'.format(start/1e9))
        self.__instr_handle.write('SOUR:FREQ:STOP {} GHz'.format(stop/1e9))
        self.__instr_handle.write('SOUR:SWE:FREQ:SPAC {}'.format(spacing))
        self.__instr_handle.write('SOUR:SWE:FREQ:STEP:LIN {}'.format(step))
        self.__instr_handle.write('SOUR:SWE:FREQ:DWEL {} ms'.format(dwell*1000))
        self.__instr_handle.write('TRIG:FSW:SOUR SING')
        self.__instr_handle.write('SOURce:SWEep:FREQuency:MODE AUTO')
        self.__instr_handle.write('SOURce:FREQuency:MODE SWEep')
        
    def start_sweep(self,mode='freq'):
        if mode in ['freq','Freq','FREQ','f','F']:
            self.__instr_handle.write('SOURce:SWEep:FREQuency:EXECute')
        elif mode in ['power','Power','pow','p','POWER','POW','P']:
            self.__instr_handle.write('SOURce:SWEep:POWer:EXECute')

    def set_local(self):
        self.__instr_handle.write('&GTR')

    def get_freqency(self):
        return float(self.__instr_handle.query('FREQ:CW?'))

    def get_level(self):
        return float(self.__instr_handle.query(':POW?'))

    def get_phase(self):
        return float(self.__instr_handle.query(':PHAS?'))

    def get_state(self):
        return self.instrhandle.query('OUTP:STAT?')
