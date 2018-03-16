# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 15:42:49 2017

@author: A108QCLab
"""
from PyQCLab.Instrument.pyspcm import *

import sys
import numpy as np
import math
#import enum
spcm_rep_run_modes={
                'cont':SPC_REP_STD_CONTINUOUS,
                'single':SPC_REP_STD_SINGLE,
                'multi':SPC_REP_STD_MULTI,
                'gate':SPC_REP_STD_GATE,
                'sequence':SPC_REP_STD_SEQUENCE,
                'single_r':SPC_REP_STD_SINGLERESTART,
                'single_fifo':SPC_REP_FIFO_SINGLE,
                'multi_fifo':SPC_REP_FIFO_MULTI,
                'gate_fifo':SPC_REP_FIFO_GATE
                }
spcm_daq_run_modes={
                'std_single':SPC_REC_STD_SINGLE,
                'std_multi':SPC_REC_STD_MULTI,
                'std_gate':SPC_REC_STD_GATE,
                'std_aba':SPC_REC_STD_ABA,
                'std_segstats':SPC_REC_STD_SEGSTATS,
                'std_average':SPC_REC_STD_AVERAGE,
                'fifo_single':SPC_REC_FIFO_SINGLE,
                'fifo_multi':SPC_REC_FIFO_MULTI,
                'fifo_gate':SPC_REC_FIFO_GATE,
                'fifo_aba':SPC_REC_FIFO_ABA,
                'fifo_segstats':SPC_REC_FIFO_SEGSTATS,
                'fifo_average':SPC_REC_FIFO_AVERAGE
                }
spcm_clock_modes={
                'int':SPC_CM_INTPLL,
                'ext':SPC_CM_EXTREFCLOCK
                }
spcm_trig_sources={
            'sw':SPC_TMASK_SOFTWARE,
            'ext0':SPC_TMASK_EXT0,
            'ext1':SPC_TMASK_EXT1,
            'ext01':SPC_TMASK_EXT0 | SPC_TMASK_EXT1
            }
spcm_trig_masks={
            'or':SPC_TRIG_ORMASK,
            'and':SPC_TRIG_ANDMASK
            }
spcm_trig_modes={
            'pos':SPC_TM_POS,
            'neg':SPC_TM_NEG,
            'both':SPC_TM_BOTH,
            'winenter':SPC_TM_WINENTER,
            'winleave':SPC_TM_WINLEAVE,
            'inwin':SPC_TM_INWIN,
            'outwin':SPC_TM_OUTSIDEWIN
            }
class Spectrum_Card:

    def __init__(self,CardNo=0):
        handle_str='/dev/spcm'+str(CardNo)
        sbuff=create_string_buffer(handle_str.encode('ascii'))
        self.hCard = spcm_hOpen(sbuff)
        if self.hCard == None:
            print("no card found\n")
        self.resetCard()
        
        lCardType = int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_PCITYP, byref(lCardType))
        lSerialNumber = int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_PCISERIALNO, byref(lSerialNumber))
        lFncType = int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_FNCTYPE, byref(lFncType))
        lChCount=int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        lBytesPerSample = int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_MIINST_BYTESPERSAMPLE,  byref(lBytesPerSample))
        lMaxChs=int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_MIINST_CHPERMODULE, byref(lMaxChs))
        self.cardType=lCardType.value
        self.seriaNumber=lSerialNumber.value
        self.funcType=lFncType.value
        self.chCount = lChCount.value
        self.bytesPerSample=lBytesPerSample.value
        self.MAX_CHS=lMaxChs.value
#        self.amplitudes=np.ones(self.MAX_CHS)
        self.szTypeToName()
        
        if self.funcType in (SPCM_TYPE_AO,SPCM_TYPE_AI):
            print("Found: {0} sn {1:05d}\n".format(self.cardName,self.seriaNumber))
        else:
            print("Card: {0} sn {1:05d} not supported\n".format(self.cardName,self.seriaNumber))
    
    def szTypeToName (self):
#        sName = ''
        lCardType=self.cardType        
        lVersion = (lCardType & TYP_VERSIONMASK)
        if (lCardType & TYP_SERIESMASK) == TYP_M2ISERIES:
            sName = 'M2i.%04x'%lVersion
        elif (lCardType & TYP_SERIESMASK) == TYP_M2IEXPSERIES:
            sName = 'M2i.%04x-Exp'%lVersion
        elif (lCardType & TYP_SERIESMASK) == TYP_M3ISERIES:
            sName = 'M3i.%04x'%lVersion
        elif (lCardType & TYP_SERIESMASK) == TYP_M3IEXPSERIES:
            sName = 'M3i.%04x-Exp'%lVersion
        elif (lCardType & TYP_SERIESMASK) == TYP_M4IEXPSERIES:
            sName = 'M4i.%04x-x8'%lVersion
        elif (lCardType & TYP_SERIESMASK) == TYP_M4XEXPSERIES:
            sName = 'M4x.%04x-x4'%lVersion
        else:
            sName = 'unknown type'
        self.cardName=sName
        
    def _setSampleRate(self,samplerate):
        spcm_dwSetParam_i64(self.hCard, SPC_SAMPLERATE, samplerate)
        
    def _getSampleRate(self):
        samplerate=int64(0)
        spcm_dwGetParam_i64(self.hCard, SPC_SAMPLERATE, byref(samplerate))
        return samplerate.value
    sampleRate=property(fget=_getSampleRate,fset=_setSampleRate)
# Channel setups:    
    def chEnable(self,channels):
        chs=0
        for i in channels:
            chs=chs|2**i
        spcm_dwSetParam_i64(self.hCard, SPC_CHENABLE, chs)
        lChCount=int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        self.chCount=lChCount.value
        
    def chEnableAll(self):
        spcm_dwSetParam_i64(self.hCard, SPC_CHENABLE, 2**self.MAX_CHS-1)
        lChCount=int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        self.chCount=lChCount.value
#Clock settings:
    def setClockMode(self,mode='int'):
        spcm_dwSetParam_i32(self.hCard, SPC_CLOCKMODE, spcm_clock_modes[mode])
        if mode == 'ext':
            spcm_dwSetParam_i32(self.hCard, SPC_REFERENCECLOCK, 10000000)
#Trigger settings:            
    def setTriggerSource(self,trig_source='sw',mask='or'):        
        spcm_dwSetParam_i32(self.hCard, spcm_trig_masks[mask], spcm_trig_sources[trig_source])
        
    def setTriggerMode(self, trig='ext0',mode='pos'):
        trig_src=SPC_TRIG_EXT0_MODE if trig == 'ext0' else SPC_TRIG_EXT1_MODE
        spcm_dwSetParam_i32(self.hCard, trig_src, spcm_trig_modes[mode])
    
    def setTriggerLevel(self,level,trig='ext0'):
        spcm_dwSetParam_i32(self.hCard, SPC_TRIG_EXT0_LEVEL0, level)
    
    def setTriggerImpedance(self,impedance='50Ohm'):
        if impedance in ['50','50ohm','50Ohm','50OHM']:
            spcm_dwSetParam_i32(self.hCard, SPC_TRIG_TERM, 1)
        elif impedance in ['1M','1m','1MOhm','1MOHM','High','high','H']:
            spcm_dwSetParam_i32(self.hCard, SPC_TRIG_TERM, 0)
    
    def setTriggerInputCoupling(self,couple='DC'):
        if couple in ['dc','Dc','DC']:
            spcm_dwSetParam_i32(self.hCard, SPC_TRIG_EXT0_ACDC, 0)
        elif couple in ['ac','Ac','AC']:
            spcm_dwSetParam_i32(self.hCard, SPC_TRIG_EXT0_ACDC, 1)
#Card controll:    
    def start(self,loops=0):
        llLoops=int64(loops)
        
        spcm_dwSetParam_i64(self.hCard, SPC_LOOPS,llLoops)
        dwError = spcm_dwSetParam_i32(self.hCard, SPC_M2CMD, M2CMD_CARD_START | M2CMD_CARD_ENABLETRIGGER)
        return dwError
    
    def stop(self):
        spcm_dwSetParam_i32(self.hCard, SPC_M2CMD, M2CMD_CARD_STOP)
        
    def resetCard(self):
        spcm_dwSetParam_i32(self.hCard, SPC_M2CMD, M2CMD_CARD_RESET)
        
    def openCard(self,CardNo=0):
        self.__init__(CardNo)
        
    def closeCard(self):
        spcm_vClose(self.hCard)
        
class Spcm_DA(Spectrum_Card):
    def __init__(self,CardNo=0):
        super().__init__(CardNo)
        
    def setRange(self,level,ch=0):
        outRange=math.ceil(abs(level))
        if outRange > 2500:
            print('Warning: the setting level is two large, using the highest range of the board.')
            outRange=2500
        elif outRange < 80:
            outRange=80
        spcm_dwSetParam_i32(self.hCard, SPC_AMP0 + ch * (SPC_AMP1 - SPC_AMP0), int32(outRange))
    
    def setRangeAll(self,level):       
        for ch in range(self.chCount):
            self.setRange(level,ch)
            
    def setRunMode(self,mode):
        spcm_dwSetParam_i64(self.hCard, SPC_CARDMODE, spcm_rep_run_modes[mode])
        
    def chEnable(self,channels):
        chs=0
        for i in channels:
            chs=chs|2**i
        spcm_dwSetParam_i64(self.hCard, SPC_CHENABLE, chs)
        lChCount=int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        self.chCount=lChCount.value
        
    def chEnableAll(self):
        spcm_dwSetParam_i64(self.hCard, SPC_CHENABLE, 2**self.MAX_CHS-1)
        lChCount=int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        self.chCount=lChCount.value
        
    def setOutput(self,ch,state=1):
        chs={0:SPC_ENABLEOUT0,
            1:SPC_ENABLEOUT1,
            2:SPC_ENABLEOUT2,
            3:SPC_ENABLEOUT3,
            }
        if  state in ('On','on',1,True):
            spcm_dwSetParam_i64(self.hCard, chs[ch],  1)
        elif state in ('Off','off',0,False):
            spcm_dwSetParam_i64(self.hCard, chs[ch],  0)
        
    def setOutputAll(self,state=1):
        for i in range(self.chCount):
            self.setOutput(i,state)
        
    def writeWaveForm(self,wfdata):
        self.wfData=wfdata
        lMemsize=int64(int(len(wfdata)/self.chCount))
        spcm_dwSetParam_i64(self.hCard, SPC_MEMSIZE, lMemsize)
        qwBufferSize = uint64(wfdata.size*self.bytesPerSample)
        pvBuffer = create_string_buffer(qwBufferSize.value)
        pnBuffer = cast(pvBuffer, ptr16)
        for i in range(wfdata.size):
            pnBuffer[i] = wfdata[i]
        spcm_dwDefTransfer_i64 (self.hCard, SPCM_BUF_DATA, SPCM_DIR_PCTOCARD, int32(0), pvBuffer, uint64(0), qwBufferSize)
        spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_DATA_STARTDMA | M2CMD_DATA_WAITDMA)
        print("... data has been transferred to board memory\n")
        
    def readWaveForm(self):
        qwBufferSize = uint64(self.wfData.size*self.bytesPerSample)
        pvBuffer=(c_long*qwBufferSize.value)()
        spcm_dwDefTransfer_i64 (self.hCard, SPCM_BUF_DATA, SPCM_DIR_CARDTOPC, int32(0), pvBuffer, uint64(0), qwBufferSize)
        spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_DATA_STARTDMA | M2CMD_DATA_WAITDMA)
        data=np.zeros(self.wfData.size)
        for i in range(self.wfData.size):
            data[i]=pvBuffer[i]
        return data
    
class Spcm_AD(Spectrum_Card):
    def __init__(self,CardNo=0):
        super().__init__(CardNo)
        self.chEnableAll()
        self.setRangeAll('500mV')
        self.setInputAll()
        self.setMode('std_multi')
        
    def setRange(self,rang,ch=0):
        if rang in ['200mV','500mV','1000mV','2500mV']:
            outRange=int(rang[:-2])        
        spcm_dwSetParam_i32(self.hCard, SPC_AMP0 + ch * (SPC_AMP1 - SPC_AMP0), int32(outRange))
    
    def setRangeAll(self,rang):       
        for ch in range(self.chCount):
            self.setRange(rang,ch)
            
    def setIuput(self,ch,coupling='DC',filtering=0,offset=0):
        if coupling in ['ac','Ac','AC']:
            spcm_dwSetParam_i32(self.hCard, SPC_ACDC0 + ch * (SPC_ACDC1 - SPC_ACDC0), 1)
        else:
            spcm_dwSetParam_i32(self.hCard, SPC_ACDC0 + ch * (SPC_ACDC1 - SPC_ACDC0), 0)
        f= 0 if filtering == 0 else 1
        spcm_dwSetParam_i32(self.hCard, SPC_FILTER0, f)
        
        spcm_dwSetParam_i32(self.hCard, SPC_OFFS0, offset)
        
    def setInputAll(self,coupling='DC',filtering=0,offset=0):
        for ch in range(self.chCount):
            self.setIuput(ch)
        
    def setMode(self,mode):
        spcm_dwSetParam_i32 (self.hCard, SPC_CARDMODE, spcm_daq_run_modes[mode])
        self._mode=mode
        
    def setRecord(self,length,n_records=1,pretrig=0):
        rec_type, rec_mode=self._mode.split('_')
        n_records = 1 if rec_mode == 'single' else n_records
        if rec_type == 'std':           
            self.lMemsize = int32(length*self.chCount*n_records)
            spcm_dwSetParam_i32 (self.hCard, SPC_MEMSIZE, self.lMemsize.value)
            
        else:
            spcm_dwSetParam_i32 (self.hCard, SPC_LOOPS, n_records)

        spcm_dwSetParam_i32 (self.hCard, SPC_SEGMENTSIZE, length)    
        spcm_dwSetParam_i32 (self.hCard, SPC_POSTTRIGGER, length-pretrig)
        
    def start(self):
        self._pvData = create_string_buffer(self.lMemsize.value * 2)
        qwBufferSize = uint64 (self.lMemsize.value * 2)
        lNotifySize = int32 (0)
        spcm_dwDefTransfer_i64 (self.hCard, SPCM_BUF_DATA, SPCM_DIR_CARDTOPC, lNotifySize, self._pvData, uint64 (0), qwBufferSize)
#        spcm_dwDefTransfer_i64 (self.hCard, SPCM_BUF_DATA, SPCM_DIR_CARDTOPC , 0, self.pnData, 0, 2 * self.lMemsize.value)
#        self.pnData=cast(self._pvData,ptr16)
#        spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_CARD_START | M2CMD_CARD_ENABLETRIGGER | M2CMD_CARD_WAITREADY)
        dwError = spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_CARD_START | M2CMD_CARD_ENABLETRIGGER | M2CMD_DATA_STARTDMA)
        spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_CARD_WAITREADY)
        
#        spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_DATA_STARTDMA | M2CMD_DATA_WAITDMA)
        self.data=np.zeros(self.lMemsize.value)
        if self.bytesPerSample == 1:
            pnData = cast(self._pvData,ptr8)
            
#            self.data=np.frombuffer(pnData,dtype='int8',count=self.lMemsize.value)
        elif self.bytesPerSample == 2:
            pnData = cast(self._pvData,ptr16)
            
        for i in range(self.lMemsize.value):
            self.data[i] = pnData[i]
#            self.data=np.frombuffer(pnData,dtype='int16',count=self.lMemsize.value)
               
#%%        
if __name__ == '__main__':
    from PyQCLab.Utils.WaveForm_Gen import *
    from PyQCLab.Instrument.DG645 import *
    from time import sleep
    
    dg=DG645()
    dg.delayA=40e-8
    dg.delayAB=1e-6
    dg.trigSource('int')
    dg.trigRate(1e2)
    
    sp1=Spcm_DA(0)
    sp1.chEnableAll()
    sp1.setOutputAll()
    sp1.setRangeAll(1000)
    sp1.setRunMode('single')
    sp1.setClockMode('int')
    sp1.setTriggerSource('ext0')
    sp1.setTriggerMode(trig='ext0',mode='pos')
    sp1.setTriggerLevel(500)
    sp1.setTriggerInputCoupling('DC')
    sp1.setTriggerImpedance('1MOhm')
#    
##    sp1.runmode='cont'
##    sp1.setTriggerSource('sw')
##    sp1.setTriggerMode()
##    sp1.setClockMode('int')
##    #calculate the test waveform:
    NumofSamples=KILO_B(128)
    w1=WaveForm(NumofSamples,sp1.sampleRate)
    w1.base.inserts(KILO_B(1),[gaussian_r(KILO_B(1),0.5),rectangle(KILO_B(10)),gaussian_f(KILO_B(1),0.5)])
    c1=Carrier(NumofSamples,sp1.sampleRate,freq=1e7,phase=math.pi*0.5,offset=0.)
    c2=Carrier(NumofSamples,sp1.sampleRate,freq=0.5e7,phase=math.pi,offset=0.)
    c3=Carrier(NumofSamples,sp1.sampleRate,freq=1e6,phase=math.pi,offset=0.)
    w1.carrier.adds([c1,c2,c3])
    w1.carrier.update()
    w1.update('spcm4')
    figure(),plot(w1.waveform)
    
    w2=WaveForm(NumofSamples,sp1.sampleRate)
    w2.base.insert(KILO_B(1),rectangle(KILO_B(50)))
    w2.carrier.add(c1)
    w2.carrier.update()
    w2.update('spcm4')
    figure(),plot(w2.waveform)
    
    wfdata=np.concatenate((w2.waveform,w2.waveform))
    wfdata=wfdata.reshape(2,-1).transpose().flatten()
    sp1.writeWaveForm(wfdata)
#    wf_raw = np.zeros(NumofSamples)
#    wf_raw[100:1100]=np.sin(np.linspace(0,2*np.pi,1000))
#    wf_n=wf_raw/np.abs(wf_raw).max()
#    wf0=(wf_n*(2**15-1)).astype('int')
#    wf_raw[1500:2500]=np.ones(1000)
#    wf_n=wf_raw/np.abs(wf_raw).max()
#    wf1=(wf_n*(2**15-1)).astype('int')
#    wf2=np.concatenate((wf0,wf1))
#    wf2=wf2.reshape(2,-1).transpose().flatten()
#    sp1.writeWaveForm(wf2)
##    sp1.writeWaveForm(np.zeros(wf2.size).astype('int'))
#    sp1.outputAll()
    sp1.start()
#    sleep(10)
#    sp1.stop()    
#    sp1.closeCard()

#    sp2=Spcm_AD(2)
#    sp2.setRangeAll('2500mV')
#    sp2.setClockMode('int')
#    sp2.setTriggerSource('ext0')
#    sp2.setTriggerMode(trig='ext0',mode='pos')
#    sp2.setTriggerLevel(1000)
#    sp2.setTriggerInputCoupling('DC')
#    sp2.setTriggerImpedance('50Ohm')
#    sp2.setInputAll()
#    sp2.setRecord(1024,100,pretrig=32)
#    sp2.start()
##    sp2.stop()
#    data=sp2.data
#    data2=data.reshape([-1,2])
#    figure(),plot(data2[:,0]/128*2.5,'o-')
    from Instrument.M4i_2211 import M4i2211
    #from Instrument.M4i_Sync6631 import sync6631   
    da1=M4i2211()
    da1.setAnalogAllIn(3,2500)
    da1.setSampleRate_InterClock(5000)
    da1.setTrigger('ext',500)
    da1.setFIFOmode(3,1024,1,1)
    bufCh0,bufCh1=da1.getFIFOdata(3)
    figure()
    plot(bufCh0)
