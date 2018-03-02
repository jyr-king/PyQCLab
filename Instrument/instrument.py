# -*- coding: utf-8 -*-
"""
Created on Sat Sep 05 01:18:49 2015

@author: jyr
"""
import pyvisa as visa
import numpy as np
import enum
from instr_config import VISA_RESOURCES

class instrument(object):

    def __init__(self, instr_name):
        super().__init__()
        self.__instr_name = instr_name
        self.__rm = visa.ResourceManager()
        self.__instr_handle = self.__rm.open_resource(VISA_RESOURCES[instr_name])

    def close(self):
        self.__instr_handle.close()
        
    def _getHandle(self):
        return self.__instr_handle
    def _getInstrname(self):
        return self.__instr_name
        
    instrhandle=property(fget=_getHandle)
    instrname=property(fget=_getInstrname)


if __name__ == '__main__':
    pass
#class RS_MWSource(instrument):
#    def __init__(self, instr_name):
#        instrument.__init__(self, instr_name)
#        self.__instr_handle=self.get_handle()
#        self.__instr_handle.write('*RST')
#        self.__freqency = self.get_freqency()
#        self.__level = self.get_level()
#        self.__phase = self.get_phase()
#        self.__state = self.get_state()
#
#    def set_freqency(self, freq, offset=0, multiplier=1):
#        try:
#            # 目前的理解，offset和multiplier不影响输出的频率，只是影响面板读数。测试方知。
#            # 为了便于控制，频率统一以Hz为单位，不接受KHz、MHz和GHz单位
#            freq = float(freq)
#            offset = float(offset)
#            multiplier = float(multiplier)
#        except:
#            print('Error:Wrong input format. Nothing will be done!')
#        fmax,fmin=int(2e10),int(1e9)    
#        if freq < fmin:
#            print('Warning:freqency set too low, min= 1GHz. min value will be used.')
#            freq=fmin
#            self.__instr_handle.write('FREQ:CW {}Hz'.format(freq))
#        elif freq > fmax:
#            print('Warning:freqency set too high, max= 20GHz. max value will be used.')
#            freq=fmax
#        self.__instr_handle.write('FREQ:CW {}Hz'.format(freq))        
#        self.__instr_handle.write('FREQ:OFFS {}Hz'.format(offset))
#        self.__instr_handle.write('FREQ:MULT {}'.format(multiplier))
#        self.__freqency = self.get_freqency()
#        
#        return self.__freqency
#
#    def set_level(self, level, offset=0):
#        try:
#            level = float(level)
#            offset = float(offset)
#        except:
#            print('Error:Wrong input format. Nothing will be done!')
#        lvl_max,lvl_min=18,-130
#        if level > lvl_max:
#            print('Warning:level set too high (max=18dB), max value will be used.')
#            level=lvl_max
#        elif level < lvl_min:
#            print('Warning:level set too low (min=-130dB), min value will be used.')
#            level=lvl_min
#        self.__instr_handle.write(':POW {}'.format(level))
#        self.__instr_handle.write(':POW:OFFS {}'.format(offset))
#        self.__level = self.get_level()
#        
#        return self.__level
#
#    def set_phase(self, phase,deg=True):
#        try:
#            phase = float(phase)
#        except:
#            print('phase given here may be wrong in format, float, int or all number string are accepted.')
#        phase_max,phase_min=720,-720
#        if not deg:
#            phase=np.rad2deg(phase)
#        if phase > phase_max:
#            print('Warning:phase set too high (max=720), max value will be used.')
#            phase=phase_max
#        elif phase < phase_min:
#            print('Warning:phase set too low (min=-720), min value will be used.')
#            phase=phase_min
#        
#        self.__instr_handle.write(':PHAS {}DEG'.format(phase))
#        self.__phase = self.get_phase()
#        
#        return self.__phase
#
#    def set_output(self, state):        
#        self.__instr_handle.write('OUTP:STAT {}'.format('ON' if state else 'OFF'))
#        self.__state = self.get_state()
#        return self.__state
#
#    def set_sweepfreq(self, start,stop,step,dwell=1e-2,spacing='LIN'):
#        self.__instr_handle.write('SOUR:FREQ:STAR {} GHz'.format(start/1e9))
#        self.__instr_handle.write('SOUR:FREQ:STOP {} GHz'.format(stop/1e9))
#        self.__instr_handle.write('SOUR:SWE:FREQ:SPAC {}'.format(spacing))
#        self.__instr_handle.write('SOUR:SWE:FREQ:STEP:LIN {}'.format(step))
#        self.__instr_handle.write('SOUR:SWE:FREQ:DWEL {} ms'.format(dwell*1000))
#        self.__instr_handle.write('TRIG:FSW:SOUR SING')
#        self.__instr_handle.write('SOURce:SWEep:FREQuency:MODE AUTO')
#        self.__instr_handle.write('SOURce:FREQuency:MODE SWEep')
#        
#    def start_sweep(self,mode='freq'):
#        if mode in ['freq','Freq','FREQ','f','F']:
#            self.__instr_handle.write('SOURce:SWEep:FREQuency:EXECute')
#        elif mode in ['power','Power','pow','p','POWER','POW','P']:
#            self.__instr_handle.write('SOURce:SWEep:POWer:EXECute')
#
#    def set_local(self):
#        self.__instr_handle.write('&GTR')
#
#    def get_freqency(self):
#        return float(self.__instr_handle.query('FREQ:CW?'))
#
#    def get_level(self):
#        return float(self.__instr_handle.query(':POW?'))
#
#    def get_phase(self):
#        return float(self.__instr_handle.query(':PHAS?'))
#
#    def get_state(self):
#        return self.__instr_handle.query('OUTP:STAT?')
#
#
#class AG33120A(instrument):
#    def __init__(self,instr_name):
#        instrument.__init__(self,instr_name)
#        self.__instr_handle=self.get_handle()
#        self.__instr_handle.write('*RST')
#        self.__level,self.__offset=self.get_level()
#        self.__freqency=self.get_freqency()
#        self.__function=self.get_function()
#        
#        
#    def apply(self,param):
#        '''apply命令比较简单直接。参数param设定为元组，格式为（‘波形函数名’，频率，幅度，偏置），暂不设置参数检查。
#            波形函数名包括：SINusoid, SQUare,TRIangle, RAMP, NOISe, DC, USER.'''
#        self.__instr_handle.write('APPLy:{} {},{},{}'.format(param[0],param[1],param[2],param[3]))
#
#    def set_level(self, level,offset=0):
#        '''方波/锯齿波（三角波）输出幅度有最小值限制：1.5V.
#            RAMP/NOISe波形最小幅度为0.3V。
#            
#            '''
#        #level must >0 and <=10:
#        if level > 10:
#            print('Level out or range, using max value 10Vpp.')
#            level=10
#        elif level < 0.1:
#            print('Level out or range, using min value 0.1Vpp.')
#            level=0.1
#            
#        offset=min(2*level,5-level/2,abs(offset))*(-1 if offset < 0 else 1)
#        
#        self.__instr_handle.write('VOLT:OFFS 0')    
#        self.__instr_handle.write('VOLTage {}'.format(level))
#        self.__instr_handle.write('VOLT:OFFS {}'.format(offset))
#        self.__level,self.__offset=self.get_level()
#        
#    def get_level(self):
#        return float(self.__instr_handle.query('VOLTage?')),float(self.__instr_handle.query('VOLTage:OFFSet?'))
#        
#    def set_freqency(self, freqency):
#        self.__instr_handle.write('FREQuency {}'.format(freqency))
#        self.__freqency=self.get_freqency()
#        
#    def get_freqency(self):
#        return float(self.__instr_handle.query('FREQuency?'))
#
#    def set_function(self, func_name):
#        '''func_name: SINusoid|SQUare|TRIangle|RAMP|NOISe|DC|USER'''
#        self.__instr_handle.write('FUNCtion:SHAPe {}'.format(func_name))
#        self.__function=self.get_function()
#        
#    def get_function(self):
#        return self.__instr_handle.query('FUNCtion:SHAPe?')
#        
#    def set_burstMode(self,cycles,rate,phase=0,bm_source='INT',state=True):
#        self.__instr_handle.write('BM:NCYCles {};BM:INTernal:RATE {};BM:PHASe {}'.format(cycles,rate,phase))
#        self.__instr_handle.write('BM:SOURce {}'.format(bm_source))        
#        self.__instr_handle.write('BM:STAT {}'.format('ON' if state else 'OFF'))
#        
#    def set_trigger(self,trig_source,trig_slop):
#        '''trig_source:IMMediate|EXTernal|BUS,
#            trig_slope:POSitive|NEGative'''
#        self.__instr_handle.write('TRIGger:SOURce {};TRIGger:SLOPe {}'.format(trig_source,trig_slop))
#        
#    def trigger(self):
#        self.__instr_handle.write('*TRG')
#        
#    def set_sweep(self,start,stop,step,dwell_time=0.01,state=True):
#        pass
#
#
#class yokogawa7651(instrument):
#    '''The command format is: Command + Parameter+ Terminator. 
#        "E" is the trigger command that execute the commands changing the output settings.
#        "CR LF, LF, EOI and ";", all can be accept as a terminator.'''
#    def __init__(self, instr_name):
#        instrument.__init__(self, instr_name)
#        self.__instr_handle=self.get_handle()
#        self.__instr_handle.write('RC')
#        
#    def set_range(self,dc_func,dc_range):
#        ranges={'10mV':'R2','100mV':'R3',
#                '1V':'R4','10V':'R5','30V':'R6',
#                '1mA':'R4','10mA':'R5','100mA':'R6'
#                }
#        if dc_func in ['dcV','dcv','v','V']:
#            self.__instr_handle.write('F1/{};E'.format(ranges[dc_range]))
#        elif dc_func in ['dcI','dci','i','I']:
#            self.__instr_handle.write('F5/{};E'.format(ranges[dc_range]))
#            
#    def set_level(self,level,autorange=False):
#        polarity='-' if level < 0 else '+'
#        lvl_str=str(level/10**(np.floor(np.log10(abs(level)))-1))
#        pwr_str=str(np.floor(np.log10(level)))
#        if len(lvl_str)>5:
#            lvl_str=lvl_str[:5]
#        if autorange:
#            self.__instr_handle.write('SA{}{}E{};E'.format(polarity,lvl_str,pwr_str))
#        else:
#            self.__instr_handle.write('S{}{}E{};E'.format(polarity,lvl_str,pwr_str))
#            
#    def set_stepup(self,digit):
#        self.__instr_handle.write('UP{};E'.format(digit))
#        
#    def set_stepdown(self,digit):
#        self.__instr_handle.write('DW{};E'.format(digit))    
#            
#    def set_output(self,state=True):
#        self.__instr_handle.write('O{};E'.format(1 if state else 0))
#            
#        
#
#
#class AWGenerator(instrument):
#    
#    def __init__(self, instr_name):
#        instrument.__init__(self, instr_name)
#        self.__instr_handle=self.get_handle()
#        self.__instr_handle.write('*RST')
#        self.__DAC_RESOLUTION=int(self.__instr_handle.query('SOURCE1:DAC:RESOLUTION?'))
#        self.__DIGITAL_DEEPTH = 2**self.__DAC_RESOLUTION
#        self.__NUM_OF_CHANNELS=int(self.__instr_handle.query('AWGControl:CONFigure:CNUMber?'))
#        self.__samplerate=self.get_samplerate()
#        self.__level=np.zeros(self.__NUM_OF_CHANNELS)
#        self.__offset=np.zeros(self.__NUM_OF_CHANNELS)
#        self.__markerHigh=np.zeros((self.__NUM_OF_CHANNELS,2))
#        self.__markerLow=np.zeros((self.__NUM_OF_CHANNELS,2))
#        self.__DirectOutput=np.zeros(self.__NUM_OF_CHANNELS).astype('bool')
#        for ch in range(1,self.__NUM_OF_CHANNELS+1):
#            self.__level[ch-1],self.__offset[ch-1]=self.get_level(ch)
#            self.__markerHigh[ch-1,0]=self.get_markerH(ch,1)
#            self.__markerHigh[ch-1,1]=self.get_markerH(ch,2)
#            self.__markerLow[ch-1,0]=self.get_markerL(ch,1)
#            self.__markerLow[ch-1,1]=self.get_markerL(ch,2)
#                    
#    def set_level(self,channel,level,offset=0):
#        #channel no. must be a integer in 1,2,3,4. level should be a float number.
#        self.__instr_handle.write('SOURCE{}:VOLTAGE:AMPLITUDE {}'.format(channel,level))
#        self.__instr_handle.write('SOURCE{}:VOLTAGE:OFFSet {}'.format(channel,offset))
#        self.__level[channel-1],self.__offset[channel-1]=self.get_level(channel)
#        
#    def get_level(self,channel):
#        return float(self.__instr_handle.query('SOURCE{}:VOLTAGE:AMPLITUDE?'.format(channel))),\
#                float(self.__instr_handle.query('SOURce{}:VOLTage:OFFSet?'.format(channel)))
#        
#    def set_samplerate(self,samplerate):
#        #this function sets the sampling rate of AWG, it should be between 10MHz to 1.2GHz.
#        samplerate=int(samplerate)
#        self.__instr_handle.write('SOURCE:FREQ:FIX {}'.format(samplerate))
#        self.__samplerate=self.get_samplerate()
#        
#    def get_samplerate(self):
#        return int(float(self.__instr_handle.query('SOURCE:FREQ:FIX?')))
#        
#    def set_runmode(self,mode):
#        '''AWG有4种运行模式，默认是CONTinuous，另外还有TRIGgered，GATed和SEQuence。'''
#        return self.__instr_handle.write('AWGC:RMOD {}'.format(mode))
#        
#    def set_trigsource(self,tgs,timer=0.01):
#        if tgs in (0,'int','internal','INT','INTERNAL'):
#            return self.__instr_handle.write('SOUR1:ROSC:SOUR INT') and\
#                self.__instr_handle.write('TRIG:TIM {}'.format(timer))
#        elif tgs in (1,'ext','external','EXT','EXTERNAL'):
#            return self.__instr_handle.write('SOUR1:ROSC:SOUR EXT') and \
#            self.__instr_handle.write('SOUR1:ROSC:SOUR FIX') and \
#            self.__instr_handle.write('SOUR1:ROSC:FREQ 10MHZ')
#    
#    def set_markerH(self,channel,marker,level):
#        return self.__instr_handle.write('SOURce{}:MARKer{}:VOLTage:HIGH {}'.format(channel,marker,level))
#        
#    def get_markerH(self,channel,marker):
#        return float(self.__instr_handle.query('SOURce{}:MARKer{}:VOLTage:HIGH?'.format(channel,marker)))
#    
#    def set_markerL(self,channel,marker,level):
#        return self.__instr_handle.write('SOURce{}:MARKer{}:VOLTage:LOW {}'.format(channel,marker,level))
#        
#    def get_markerL(self,channel,marker):
#        return float(self.__instr_handle.query('SOURce{}:MARKer{}:VOLTage:LOW?'.format(channel,marker)))
#        
#    def set_directoutput(self,channel,status=True):
#        return self.__instr_handle.write('AWGC:DOUT{} {}'.format(channel, 1 if status else 0))
#        
#    def set_directoutputAll(self,status=True):
#        for i in range(1,5):
#            self.set_directoutput(i,status)
#        
#    def writeWaveform(self, name, wfdata):
#        if self._isWaveformExists(name):
#            self._deleteWaveform(name)
#        self._createWaveform(name, len(wfdata))
#        self._writeWaveformData(name, wfdata)
#
#    def writeSequence(self, name, sequenceItems):
#        if self._isSequenceExists(name):
#            self._deleteSequence(name)
#        self._createSequence(name, len(sequenceItems), 1)
#        for i in range(len(sequenceItems)):
#            self._setSequenceItem(name, i, sequenceItems[i])
#
#    def assignOutput(self, channel, waveform):
#        self._assignWaveform(channel, waveform)
#
#    def assignOutputs(self, waveforms):
#        for channel in range(1,len(waveforms)+1):
#            self.assignOutput(channel,waveforms[channel-1])
#
#    def start(self,channels=[1,2,3,4]):
#        for ch in channels:
#            print('channel {} started successfully.'.format(ch))
#            self._setOutput(ch, True)
#        self._start()
#
#    def stop(self,channels=[1,2,3,4]):
#        for ch in channels:
#            print('channel {} stopped successfully.'.format(ch))
#            self._setOutput(ch, False)
#        self._stop()
#        
#    def trigger(self,channels):
#        for ch in channels:
#            print('channel {} started successfully.'.format(ch))
#            self._setOutput(ch, True)   
#        self.__instr_handle.write('*TRIG')
#
#    class SequenceItem():
#        def __init__(self, waveformName, repeat=1, waitMode='OFF', goto='NEXT', jumpMode='OFF', jumpTarget='NEXT'):
#            self.waveformName = waveformName
#            self.repeat = repeat
#            self.waitMode = waitMode
#            self.goto = goto
#            self.jumpMode = jumpMode
#            self.jumpTarget = jumpTarget
#
#        class TrigegrMode(enum.Enum):
#            OFF = 'OFF'
#            TriggerA = 'ATR'
#            TrigegrB = 'BTR'
#            Integer = 'ITR'
#
#        class Target(enum.Enum):
#            NEXT = 'NEXT'
#            FIRST = 'FIRST'
#            LAST = 'LAST'
#            END = 'END'
#
#    def _identity(self):
#        return self.__instr_handle.query('*IDN?')[:-1]
#
#    def _getVersion(self):
#        return self.__instr_handle.query('SYSTem:VERSion?')[:-1]
#
#    def _createWaveform(self, name, length):
#        self.__instr_handle.write('WLISt:WAVeform:NEW "{}",{},{}'.format(name, length, 'INTEGER'))
#
#    def _getWaveformListSize(self):
#        return int(self.__instr_handle.query('WLISt:SIZE?'))
#
#    def _getWaveformLength(self, name):
#        return int(self.__instr_handle.query('WLISt:WAVeform:LENGth? "{}"'.format(name)))
#
#    def _getWaveformName(self, index):
#        return self.__instr_handle.query('WLISt:NAME? {}'.format(index))[1:-2]
#
#    def _listWaveforms(self):
#        size = self._getWaveformListSize()
#        return [self._getWaveformName(i) for i in range(size)]
#
#    def _isWaveformExists(self, name):
#        return self._listWaveforms().__contains__(name)
#
#    def _deleteWaveform(self, name):
#        self.__instr_handle.write('WLISt:WAVeform:DELete "{}"'.format(name))
#
#    def _deleteAllWaveforms(self):
#        self.__instr_handle.write('WLISt:WAVeform:DELete ALL')
#
#    def _getWaveformType(self, name):
#        return self.__instr_handle.query('WLISt:WAVeform:TYPE? "{}"'.format(name))[:-1]
#
#    def _writeWaveformData(self, name, data, start=0):
##        self.__instr_handle.values_format.use_binary('h',False,np.array)
##        self.__instr_handle.write_binary_values('WLISt:WAVeform:DATA {},{},{}'.format(name, start, len(data)), data)
#        self.__instr_handle.write_binary_values('WLISt:WAVeform:DATA "{}",{},{},'.format(name, start, len(data)), data,
#                                              datatype='h', is_big_endian=False)
#    def _setOutput(self, channel, status):
#        self.__instr_handle.write('OUTPUT{} {}'.format(channel, 1 if status else 0))
#
#    def _start(self):
#        self.__instr_handle.write('AWGControl:RUN')
#
#    def _stop(self):
#        self.__instr_handle.write('AWGControl:STOP')
#
#    def _getSequenceName(self, index):
#        return self.__instr_handle.query('SLISt:NAME? {}'.format(index))[1:-2]
#
#    def _deleteSequence(self, name):
#        self.__instr_handle.write('SLISt:SEQuence:DELete "{}"'.format(name))
#
#    def _deleteAllSequence(self):
#        self.__instr_handle.write('SLISt:SEQuence:DELete ALL')
#
#    def _createSequence(self, name, step, track):
#        self.__instr_handle.write('SLISt:SEQuence:NEW "{}",{},{}'.format(name, step, track))
#
#    def _getSequenceListSize(self):
#        return int(self.__instr_handle.query('SLISt:SIZE?'))
#
#    def _listSequences(self):
#        size = self._getSequenceListSize()
#        return [self._getSequenceName(i) for i in range(size)]
#
#    def _isSequenceExists(self, name):
#        return self._listSequences().__contains__(name)
#
#    def _setSequenceItemWaitMode(self, name, step, mode):
#        # mode can be OFF|ATRIGGER|BTRIGGER|ITRIGGER
#        self.__instr_handle.write('SLISt:SEQuence:STEP{}:WINPut "{}", {}'.format(step, name, mode))
#
#    def _setSequenceItemJumpMode(self, name, step, mode):
#        # mode can be OFF|ATRIGGER|BTRIGGER|ITRIGGER
#        self.__instr_handle.write('SLISt:SEQuence:STEP{}:EJINput "{}", {}'.format(step, name, mode))
#
#    def _setSequenceItemJumpTarget(self, name, step, target):
#        # target can be NEXT|FIRST|LAST|END or a index
#        self.__instr_handle.write('SLISt:SEQuence:STEP{}:EJUMp "{}", {}'.format(step, name, target))
#
#    def _setSequenceItemGoto(self, name, step, target):
#        # target can be NEXT|FIRST|LAST|END or a index
#        self.__instr_handle.write('SLISt:SEQuence:STEP{}:GOTO "{}", {}'.format(step, name, target))
#
#    def _setSequenceItemRepeat(self, name, step, count):
#        # count can be INFINITE or a number
#        self.__instr_handle.write('SLISt:SEQuence:STEP{}:RCOunt "{}", {}'.format(step, name, count))
#
#    def _setSequenceItemWaveform(self, name, step, track, waveformName):
#        self.__instr_handle.write(
#            'SLISt:SEQuence:STEP{}:TASSet{}:WAVeform "{}", "{}"'.format(step, track, name, waveformName))
#
#    def _setSequenceItem(self, name, step, sequenceItem):
#        self._setSequenceItemWaveform(name, step, 1, sequenceItem.waveformName)
#
#        def modeParse(mode, clazz):
#            return mode.value if isinstance(mode, clazz) else mode
#
#        self._setSequenceItemRepeat(name, step, sequenceItem.repeat)
#        self._setSequenceItemWaitMode(name, step, modeParse(sequenceItem.waitMode, AWGenerator.SequenceItem.TrigegrMode))
#        self._setSequenceItemGoto(name, step, modeParse(sequenceItem.goto, AWGenerator.SequenceItem.Target))
#        self._setSequenceItemJumpMode(name, step, modeParse(sequenceItem.jumpMode, AWGenerator.SequenceItem.TrigegrMode))
#        self._setSequenceItemJumpTarget(name, step, modeParse(sequenceItem.jumpTarget, AWGenerator.SequenceItem.Target))
#
#    def _assignWaveform(self, channel, waveformName):
#        self.__instr_handle.write('SOURCE{}:WAVeform "{}"'.format(channel, waveformName))
#
#    def _assignSequence(self, channel, sequenceName):
#        self.__instr_handle.write('SOURCE{}:CASSet:SEQuence "{}",1'.format(channel, sequenceName))
#
#
#class NetworkAnalyser(instrument):
#    def __init__(self, instr_name):
#        instrument.__init__(self, instr_name)
##        self.__instr_handle.write('CALC1:PAR:DEL:ALL')
##        self.__instr_handle.write('CALC1:PAR:DEF "ch1_S21",S21')
##        self.__instr_handle.write('DISP:WIND1:TRAC1:FEED "ch1_S21"')
##        self.__instr_handle.write('MMEM:STOR:TRAC:FORM:SNP DB')
##        self.__instr_handle.write('TRIG:CONT:OFF')
#        self.__instr_handle.write('*RST')
#        self.__instr_handle.write('INIT:CONT OFF')
#
#    def set_sweep(self, start, stop, IF, N, avg=1):
##        self.__instr_handle.write('SENS1:SWE:TYPE SEGM')
#        #set frequency range:
#        if isinstance(start, (float,int)) and isinstance(stop, (float,int)):
#            self.__instr_handle.write('SENS:FREQ:STAR '+str(start))
#            self.__instr_handle.write('SENS:FREQ:STOP '+str(stop))
#        else :
#            print('The type of "start" or "stop" is error, please retype, this function will not start.')
#            return 0
#        #set IFbandwidth:
#        if isinstance(IF,int):
#            self.__instr_handle.write('SENS:BAND:RES '+str(IF))
#        else:
#            print('IF bandwidth setting should be integer >1,please retype. this function will not start.')
#            return 0
#        #set sweep number of points:
#        if isinstance(N,int):
#            self.__instr_handle.write('SENS:SWE:POIN '+str(N))
#        else:
#            print('sweep number of points should be integer,please retype. this function will not start.')
#            return 0
#        #set average times:
#        if avg > 1 and isinstance(avg,int):        
#            self.__instr_handle.write('SENS:AVER:STAT ON')
#            self.__instr_handle.write('SENS:AVER:CLE')
#            self.__instr_handle.write('SENS:AVER:COUN ' + str(avg))
#            self.__instr_handle.write('SENS:AVER:MODE AUTO')
#        else :
#            self.__instr_handle.write('SENS:AVER:STATE OFF')
#
##        for i in range(len(IF)):
##            idx = str(i + 1)
##            self.__instr_handle.write('SENS1:SEGM' + idx + ':ADD')
##            self.__instr_handle.write('SENS1:SEGM' + idx + ':STATE ON')
##            self.__instr_handle.write('SENS1:SEGM' + idx + ':BWID:RES ' + str(IF[i]) + 'Hz')
##            self.__instr_handle.write('SENS1:SEGM' + idx + ':FREQ:START ' + str(freq[i]))
##            self.__instr_handle.write('SENS1:SEGM' + idx + ':FREQ:STOP ' + str(freq[i + 1]))
##            self.__instr_handle.write('SENS1:SEGM' + idx + ':SWE:POIN ' + str(N[i]))
##            self.__instr_handle.write('SENS1:SEGM' + idx + ':X:SPAC OBAS')
##
##        self.__instr_handle.write('OUTP ON')
##        self.__instr_handle.write('SENS1:SWE:GRO:COUN ' + str(avg))
##        self.__instr_handle.write('SENS1:SWE:MODE GRO')
#
#    def set_level(self, level):
#        try:
#            level = float(level)
#        except:
#            print('level given here may be illegal, float, int or all number string are accepted.')
#        if 12 > level > -60:
#            self.__instr_handle.write('SOUR:POW ' + str(level))
#            self.level = float(self.__instr_handle.query('SOUR:POW?'))
#        else:
#            raise ValueError('The given level value is out of range (-27 to 5dBm).')
#        return self.level
#        
#    def set_format(self,Fmt):
#        if Fmt in ['MLIN','MLOG','PHAS','UPH','POL','SMIT','ISM','GDEL','REAL','IMAG','SWR']:
#            self.__instr_handle.write('CALC:FORM '+Fmt)
#        else:
#            print('Wrong format was given, nothing been done.')
#            
#    def get_data(self):
#        data=self.__instr_handle.query('CALC:DATA? SDAT')
#        f=self.__instr_handle.query('CALC:DATA:STIM?')
#        data=data.split(',')
#        f=f.split(',')
#        for i in range(len(data)):
#            data[i]=float(data[i])
#            if i < len(data)/2:
#                f[i]=float(f[i])
#        f=np.array(f)
#        data=np.array(data).reshape(len(data)/2,2)
#        data=data[:,0]+data[:,1]*1j
#        return f,data
#        
#    def start_sweep(self):
#        self.__instr_handle.write('INIT:IMM; *WAI')
#
#    def abort_sweep(self):
#        self.__instr_handle.write('abort')
        
    
