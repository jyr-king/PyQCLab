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

class spectrumDA:

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
        
        if self.funcType == SPCM_TYPE_AO:
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
           
    def _setLevel0(self,level):
        outRange=math.ceil(abs(level))
        ch=0
        if outRange > 2500:
            print('Warning: the setting level is two large, using the highest range of the board.')
            outRange=2500
        elif outRange < 80:
            outRange=80
        spcm_dwSetParam_i32(self.hCard, SPC_AMP0 + ch * (SPC_AMP1 - SPC_AMP0), int32(outRange))
#        self.amplitudes[ch]=min(1,level/outRange)

    def _getLevel0(self):
        ch=0
        level = int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_AMP0 + ch * (SPC_AMP1 - SPC_AMP0), byref(level))
        return level.value
    
    def _setLevel1(self,level):
        outRange=math.ceil(abs(level))
        ch=0
        if outRange > 2500:
            print('Warning: the setting level is two large, using the highest range of the board.')
            outRange=2500
        elif outRange < 80:
            outRange=80
        spcm_dwSetParam_i32(self.hCard, SPC_AMP1 + ch * (SPC_AMP1 - SPC_AMP0), int32(outRange))
#        self.amplitudes[ch]=min(1,level/outRange)

    def _getLevel1(self):
        ch=0
        level = int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_AMP1 + ch * (SPC_AMP1 - SPC_AMP0), byref(level))
        return level.value    
    
    def _setLevel2(self,level):
        outRange=math.ceil(abs(level))
        ch=0
        if outRange > 2500:
            print('Warning: the setting level is two large, using the highest range of the board.')
            outRange=2500
        elif outRange < 80:
            outRange=80
        spcm_dwSetParam_i32(self.hCard, SPC_AMP2 + ch * (SPC_AMP1 - SPC_AMP0), int32(outRange))
#        self.amplitudes[ch]=min(1,level/outRange)

    def _getLevel2(self):
        ch=0
        level = int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_AMP2 + ch * (SPC_AMP1 - SPC_AMP0), byref(level))
        return level.value    
    
    def _setLevel3(self,level):
        outRange=math.ceil(abs(level))
        ch=0
        if outRange > 2500:
            print('Warning: the setting level is two large, using the highest range of the board.')
            outRange=2500
        elif outRange < 80:
            outRange=80
        spcm_dwSetParam_i32(self.hCard, SPC_AMP3 + ch * (SPC_AMP1 - SPC_AMP0), int32(outRange))
#        self.amplitudes[ch]=min(1,level/outRange)

    def _getLevel3(self):
        ch=0
        level = int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_AMP3 + ch * (SPC_AMP1 - SPC_AMP0), byref(level))
        return level.value    
    level0=property(fget=_getLevel0,fset=_setLevel0)
    level1=property(fget=_getLevel1,fset=_setLevel1)
    level2=property(fget=_getLevel2,fset=_setLevel2)
    level3=property(fget=_getLevel3,fset=_setLevel3)
#    def setLevel(self):
        
    def output(self,channel,state='On'):
        chs={0:SPC_ENABLEOUT0,
            1:SPC_ENABLEOUT1,
            2:SPC_ENABLEOUT2,
            3:SPC_ENABLEOUT3,
            }
        if  state in ('On','on',1,True):
            spcm_dwSetParam_i64(self.hCard, chs[channel],  1)
        elif state in ('Off','off',0,False):
            spcm_dwSetParam_i64(self.hCard, chs[channel],  0)
        
    def outputAll(self,state='On'):
        for i in range(self.chCount):
            self.output(i,state)
    
    def _setRunMode(self,mode):
        modes={'cont':SPC_REP_STD_CONTINUOUS,
        'single':SPC_REP_STD_SINGLE,
        'multi':SPC_REP_STD_MULTI,
        'gate':SPC_REP_STD_GATE,
        'sequence':SPC_REP_STD_SEQUENCE,
        'single_r':SPC_REP_STD_SINGLERESTART,
        'single_fifo':SPC_REP_FIFO_SINGLE,
        'multi_fifo':SPC_REP_FIFO_MULTI,
        'gate_fifo':SPC_REP_FIFO_GATE
        }
        spcm_dwSetParam_i64(self.hCard, SPC_CARDMODE, modes[mode])
    def _getRunMode(self):
        modes={SPC_REP_STD_CONTINUOUS:'cont',
        SPC_REP_STD_SINGLE:'single',
        SPC_REP_STD_MULTI:'multi',
        SPC_REP_STD_GATE:'gate',
        SPC_REP_STD_SEQUENCE:'sequence',
        SPC_REP_STD_SINGLERESTART:'single_r',
        SPC_REP_FIFO_SINGLE:'single_fifo',
        SPC_REP_FIFO_MULTI:'multi_fifo',
        SPC_REP_FIFO_GATE:'gate_fifo'
        }
        mode=int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CARDMODE, byref(mode))
        return modes[mode.value]
    runmode=property(fget=_getRunMode,fset=_setRunMode)
    
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
    
    def setTriggerSource(self,trig_source='sw',mask='or'):
        trig_sources={
                'sw':SPC_TMASK_SOFTWARE,
                'ext0':SPC_TMASK_EXT0,
                'ext1':SPC_TMASK_EXT1,
                'ext01':SPC_TMASK_EXT0 | SPC_TMASK_EXT1
                }
        trig_masks={
                'or':SPC_TRIG_ORMASK,
                'and':SPC_TRIG_ANDMASK
                }
        spcm_dwSetParam_i32(self.hCard, trig_masks[mask], trig_sources[trig_source])
        
    def setTriggerMode(self, trig='ext0',mode='pos'):
        trig_modes={
                'pos':SPC_TM_POS,
                'neg':SPC_TM_NEG,
                'both':SPC_TM_BOTH,
                'winenter':SPC_TM_WINENTER,
                'winleave':SPC_TM_WINLEAVE,
                'inwin':SPC_TM_INWIN,
                'outwin':SPC_TM_OUTSIDEWIN
                }
        trig_src=SPC_TRIG_EXT0_MODE if trig == 'ext0' else SPC_TRIG_EXT1_MODE
        spcm_dwSetParam_i32(self.hCard, trig_src, trig_modes[mode])
    
    def setTriggerLevel(self,level,trig='ext0'):
        pass
        
    def setClockMode(self,mode='int'):
        modes={
                'int':SPC_CM_INTPLL,
                'ext':SPC_CM_EXTREFCLOCK
                }
        spcm_dwSetParam_i32(self.hCard, SPC_CLOCKMODE, modes[mode])
        if mode == 'ext':
            spcm_dwSetParam_i32(self.hCard, SPC_REFERENCECLOCK, 10000000)
    
    def writeWaveForm(self,wfdata):
        self.wfData=wfdata
        lMemsize=int64(int(len(wfdata)/self.chCount))
        spcm_dwSetParam_i64(self.hCard, SPC_MEMSIZE, lMemsize)
        qwBufferSize = uint64(wfdata.size*self.bytesPerSample)
#        pvBuffer=(c_long*qwBufferSize.value)()
#        for i in range(wfdata.size):
#            pvBuffer[i] = wfdata[i]
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
#%%        
if __name__ == '__main__':
    pass
    sp1=spectrumDA(1)
    sp1.chEnable((0,1))
    sp1.runmode='cont'
    sp1.setTriggerSource('sw')
    sp1.setTriggerMode()
    sp1.setClockMode('int')
    #calculate the test waveform:
    NumofSamples=KILO_B(128)
    wf_raw = np.zeros(NumofSamples)
    wf_raw[100:1100]=np.sin(np.linspace(0,2*np.pi,1000))
    wf_n=wf_raw/np.abs(wf_raw).max()
    wf0=(wf_n*(2**15-1)).astype('int')
    wf_raw[1500:2500]=np.ones(1000)
    wf_n=wf_raw/np.abs(wf_raw).max()
    wf1=(wf_n*(2**15-1)).astype('int')
    wf2=np.concatenate((wf0,wf1))
    wf2=wf2.reshape(2,-1).transpose().flatten()
    sp1.writeWaveForm(wf2)
#    sp1.writeWaveForm(np.zeros(wf2.size).astype('int'))
    sp1.outputAll()
    sp1.start()
    sp1.stop()    
