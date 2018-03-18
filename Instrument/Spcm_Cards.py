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

class Spectrum_Card:

    def __init__(self,CardNo=0):
        handle_str='/dev/spcm'+str(CardNo)
        sbuff=create_string_buffer(handle_str.encode('ascii'))
        self.hCard = spcm_hOpen(sbuff)
        if self.hCard == None:
            print("no card found\n")
        self.resetCard()
        #gethor card information:
        lCardType = c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_PCITYP, byref(lCardType))
        lSerialNumber = c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_PCISERIALNO, byref(lSerialNumber))
        lFncType = c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_FNCTYPE, byref(lFncType))
        lChCount=c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        lBytesPerSample = c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_MIINST_BYTESPERSAMPLE,  byref(lBytesPerSample))
        lBitsPerSample = c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_MIINST_BITSPERSAMPLE,  byref(lBitsPerSample))
        lMaxChs=c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_MIINST_CHPERMODULE, byref(lMaxChs))
        self.cardType=lCardType.value
        self.seriaNumber=lSerialNumber.value
        self.funcType=lFncType.value
        self.chCount = lChCount.value
        self.bytesPerSample=lBytesPerSample.value
        self.bitsPerSample=lBitsPerSample.value
        self.MAX_CHS=lMaxChs.value
#        self.amplitudes=np.ones(self.MAX_CHS)
        self.szTypeToName()
        
        if self.funcType in (SPCM_TYPE_AO,SPCM_TYPE_AI):
            print("Found: {0} sn {1:05d}\n".format(self.cardName,self.seriaNumber))
        else:
            print("Card: {0} sn {1:05d} not supported\n".format(self.cardName,self.seriaNumber))
            
        #Some default settings:
        self.enabled_chs=[]
        self.range_chs=[]
        self.chEnableAll()
        self.setClockMode('int')
        self.setTrigger(trig_source='ext0',mode='pos',level=1000,couple='DC',impedance='50Ohm')
    
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
        
    def getErrorInfo(self):
        szErrorTextBuffer = create_string_buffer (ERRORTEXTLEN)
        sys.stdout.write("{0}\n".format(szErrorTextBuffer.value))
    
    # Samplerate:        
    def _setSampleRate(self,samplerate):
        spcm_dwSetParam_i64(self.hCard, SPC_SAMPLERATE, samplerate)
        
    def _getSampleRate(self):
        samplerate=c_int64(0)
        spcm_dwGetParam_i64(self.hCard, SPC_SAMPLERATE, byref(samplerate))
        return samplerate.value
    sampleRate=property(fget=_getSampleRate,fset=_setSampleRate)
    # Channel setups:    
    def chEnable(self,channels):
        chs=0
        for i in channels:
            chs=chs|2**i
        spcm_dwSetParam_i64(self.hCard, SPC_CHENABLE, chs)
        lChCount=c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        self.chCount=lChCount.value
        for ch in channels:
            if ch not in self.enabled_chs:
                self.enabled_chs.append(ch)
        
    def chEnableAll(self):
        spcm_dwSetParam_i64(self.hCard, SPC_CHENABLE, 2**self.MAX_CHS-1)
        lChCount=c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        self.chCount=lChCount.value
        for ch in range(self.MAX_CHS):
            if ch not in self.enabled_chs:
                self.enabled_chs.append(ch)
    #Clock settings, int or ext?:
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
            
    def setTrigger(self,**kwargs):
        if 'trig_source' in kwargs.keys():
            if kwargs['trig_source'] == 'sw':
                self.setTriggerSource()
            elif kwargs['trig_source'] == 'ext0':
                self.setTriggerSource('ext0')
                if 'mode' in kwargs.keys():
                    self.setTriggerMode(mode=kwargs['mode'])
                elif 'level' in kwargs.keys():
                    self.setTriggerLevel(kwargs['level'])
                elif 'coupling' in kwargs.keys():
                    self.setTriggerInputCoupling(kwargs['coupling'])
                elif 'impedance' in kwargs.keys():
                    self.setTriggerImpedance(kwargs['impedance'])
                
#Card controll:    
    def start(self,loops=0):
        llLoops=c_int64(loops)        
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
        
        self.setOutputAll(1)
        self.setRangeAll(1000)
        self.setRunMode('single_r')
        self.wfData=np.empty(0)
        
    def setRange(self,rang,ch=0):
        try:
            outRange=math.ceil(abs(rang))
            ch=int(ch)
        except:
            sys.stdout.write('Error: "rang" and "ch" must be numbers.')
        else:
            if outRange > 2500:
                outRange = 2500
            elif outRange < 80:
                outRange = 80
            else:
                if ch in range(self.MAX_CHS):
                    spcm_dwSetParam_i32(self.hCard, SPC_AMP0 + ch * (SPC_AMP1 - SPC_AMP0), c_int32(outRange))
                    self.range_chs[ch]=outRange
                else:
                    sys.stdout.write('ValueError: "ch" must be a integer between 0 and MAX_CHS. Nothing will do.')
    
    def setRangeAll(self,rang):       
        for ch in range(self.chCount):
            self.setRange(rang,ch)
            
    def setRunMode(self,mode):
        spcm_dwSetParam_i64(self.hCard, SPC_CARDMODE, spcm_rep_run_modes[mode])
        
    def chEnable(self,channels):
        chs=0
        for i in channels:
            chs=chs|2**i
        spcm_dwSetParam_i64(self.hCard, SPC_CHENABLE, chs)
        lChCount=c_int32(0)
        spcm_dwGetParam_i32(self.hCard, SPC_CHCOUNT, byref(lChCount))
        self.chCount=lChCount.value
        
    def chEnableAll(self):
        spcm_dwSetParam_i64(self.hCard, SPC_CHENABLE, 2**self.MAX_CHS-1)
        lChCount=c_int32(0)
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
        lMemsize=c_int64(int(len(wfdata)/self.chCount))
        spcm_dwSetParam_i64(self.hCard, SPC_MEMSIZE, lMemsize)
        qwBufferSize = c_uint64(wfdata.size*self.bytesPerSample)
        pvBuffer = create_string_buffer(qwBufferSize.value)
        pnBuffer = cast(pvBuffer, ptr16)
        for i in range(wfdata.size):
            pnBuffer[i] = wfdata[i]
        spcm_dwDefTransfer_i64 (self.hCard, SPCM_BUF_DATA, SPCM_DIR_PCTOCARD, c_int32(0), pvBuffer, c_uint64(0), qwBufferSize)
        dwError = spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_DATA_STARTDMA | M2CMD_DATA_WAITDMA)
        if not dwError:
            self.getErrorInfo()
        else:
            sys.stdout.write("... data has been transferred to board memory\n")
        
    def readWaveForm(self):
        if self.wfData.size:
            qwBufferSize = c_uint64(self.wfData.size*self.bytesPerSample)
            pvBuffer=(c_long*qwBufferSize.value)()
            spcm_dwDefTransfer_i64 (self.hCard, SPCM_BUF_DATA, SPCM_DIR_CARDTOPC, c_int32(0), pvBuffer, c_uint64(0), qwBufferSize)
            spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_DATA_STARTDMA | M2CMD_DATA_WAITDMA)
        for i in range(self.wfData.size):
            self.wfData[i]=pvBuffer[i]
    
class Spcm_AD(Spectrum_Card):
    def __init__(self,CardNo=0):
        super().__init__(CardNo)
        
        self.setRangeAll('500mV')
        self.setInputAll()
        self.setMode('std_multi')
        
    def setRange(self,rang,ch=0):
        if rang in ['200mV','500mV','1000mV','2500mV']:
            outRange=int(rang[:-2])        
        try:
            ch=int(ch)
        except:
            sys.stdout.write('Error: "ch" must be a integer between 0 and MAX_CHS.')
        else:
            spcm_dwSetParam_i32(self.hCard, SPC_AMP0 + ch * (SPC_AMP1 - SPC_AMP0), c_int32(outRange))
            self.range_chs[ch] = outRange
    
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
        
    def setRecord(self,length,n_records=1,pretrig=32):
        rec_type, rec_mode=self._mode.split('_')
        SPC_LEN_RECORD_MIN=64
        SPC_LEN_RECORD_STEP=32
        SPC_LEN_PRETRIG_MIN=32
        SPC_LEN_POSTTRIG_MIN=32
        SPC_LEN_PRETRIG_STEP=32
        #record length and pretrig must follow some restricts:
        if length < SPC_LEN_RECORD_MIN:
            length = SPC_LEN_RECORD_MIN
        else:
            length = math.ceil((length-SPC_LEN_RECORD_MIN)/SPC_LEN_RECORD_STEP)*SPC_LEN_RECORD_STEP+SPC_LEN_RECORD_MIN
        
        if pretrig < SPC_LEN_PRETRIG_MIN:
            pretrig = SPC_LEN_PRETRIG_MIN
        elif pretrig > (length - SPC_LEN_POSTTRIG_MIN):
            pretrig = length - SPC_LEN_POSTTRIG_MIN
        else:
            pretrig = math.ceil((pretrig-SPC_LEN_PRETRIG_MIN)/SPC_LEN_PRETRIG_STEP)*SPC_LEN_PRETRIG_STEP+SPC_LEN_PRETRIG_MIN
            
        n_records = 1 if rec_mode == 'single' else int(n_records)
        #计算所需的内存空间（以采样点为单位，实际分配空间的时候需要乘以BytesPerSample），单个记录长度*通道数*记录数
        self.lMemsize = c_int32(length*self.chCount*n_records)
        if rec_type == 'std':
            #设置notify size=0，即一直到采集结束才触发中断事件。                     
            self.lNotifySize = c_int32(0)
            spcm_dwSetParam_i32 (self.hCard, SPC_MEMSIZE, self.lMemsize.value)
            
        else:
            spcm_dwSetParam_i32 (self.hCard, SPC_LOOPS, n_records)
            #FIFO模式下，我们尝试分配足够大的buffer（能够容得下所有的采样点），因此可以与std模式一样的运行。
            self.lNotifySize = c_int32(0)
#            self.lNotifySize = c_int32(self.bytesPerSample*self.lMemsize.value)
            
        spcm_dwSetParam_i32 (self.hCard, SPC_SEGMENTSIZE, length)    
        spcm_dwSetParam_i32 (self.hCard, SPC_POSTTRIGGER, length-pretrig)
        
    def start(self):
        #计算所需缓存大小，为了简化操作，只使用一个刚好能装下所有采样点的buffer。
        qwBufferSize = c_uint64 (self.lMemsize.value * self.bytesPerSample)
        #分配缓存：
        self._pvData = create_string_buffer(qwBufferSize.value)       
        #Define the transfer:
        spcm_dwDefTransfer_i64 (self.hCard, SPCM_BUF_DATA, SPCM_DIR_CARDTOPC, self.lNotifySize, self._pvData, c_uint64 (0), qwBufferSize)
#        spcm_dwDefTransfer_i64 (self.hCard, SPCM_BUF_DATA, SPCM_DIR_CARDTOPC , 0, self.pnData, 0, 2 * self.lMemsize.value)
#        self.pnData=cast(self._pvData,ptr16)
#        spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_CARD_START | M2CMD_CARD_ENABLETRIGGER | M2CMD_CARD_WAITREADY)
        #启动采集卡，等待触发，开始DMA数据传输
        dwError = spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_CARD_START | M2CMD_CARD_ENABLETRIGGER | M2CMD_DATA_STARTDMA)
        spcm_dwSetParam_i32 (self.hCard, SPC_M2CMD, M2CMD_CARD_WAITREADY)
        #取出数据：
        self.data=np.zeros(self.lMemsize.value)
        if self.bytesPerSample == 1:
            pnData = cast(self._pvData,ptr8)
        elif self.bytesPerSample == 2:
            pnData = cast(self._pvData,ptr16)
        
        self.raw_data = pnData[:self.lMemsize.value]
        
#        for i in range(self.lMemsize.value):
#            self.data[i] = pnData[i]
#            self.data=np.frombuffer(pnData,dtype='int16',count=self.lMemsize.value)
    def getData(self,ch):
        return self.raw_data.reshape([-1,self.chCount])[:,ch]/2**(self.bitsPerSample-1)*self.range_chs[ch]              
#%%        
if __name__ == '__main__':
    from PyQCLab.Utils.WaveForm_Gen import *
    from PyQCLab.Instrument.DG645 import *
    from time import sleep
    #设置外部触发
    dg=DG645()
    dg.delayA=40e-8
    dg.delayAB=1e-6
    dg.trigSource('int')
    dg.trigRate(1e4)
    #设置波形回放卡：
    sp1=Spcm_DA(0)
    sp1.chEnableAll()
    sp1.setOutputAll()
    sp1.setRangeAll(1000)
    sp1.setRunMode('single_r')
    sp1.setClockMode('int')
#    sp1.setTriggerSource('ext0')
#    sp1.setTriggerMode(trig='ext0',mode='pos')
#    sp1.setTriggerLevel(500)
#    sp1.setTriggerInputCoupling('DC')
#    sp1.setTriggerImpedance('1MOhm')
    sp1.setTrigger(trig_source='ext0',mode='pos',level=1000,coupling='DC',impedance='50Ohm')
    da_samplerate=sp1.sampleRate
#    
##    sp1.runmode='cont'
##    sp1.setTriggerSource('sw')
##    sp1.setTriggerMode()
##    sp1.setClockMode('int')
##    #calculate the test waveform:
    #写入波形：
    #波形长度128K：
    NumofSamples=KILO_B(128)
    #对应的周期为T_da:
    T_da=NumofSamples/da_samplerate
    w1=WaveForm(NumofSamples,da_samplerate)
    w1.base.inserts(KILO_B(1),[gaussian_r(KILO_B(1),0.5),rectangle(KILO_B(10)),gaussian_f(KILO_B(1),0.5)])
    #给w1添加三种不同频率的载波：
    c1=Carrier(NumofSamples,sp1.sampleRate,freq=1e7,phase=math.pi*0.5,offset=0.)
    c2=Carrier(NumofSamples,sp1.sampleRate,freq=0.5e7,phase=math.pi,offset=0.)
    c3=Carrier(NumofSamples,sp1.sampleRate,freq=1e6,phase=math.pi,offset=0.)
    w1.carrier.adds([c1,c2,c3])
    w1.carrier.update()
    w1.update('spcm4')
    figure(),plot(w1.waveform)
    #w1只有一种载波频率：
    w2=WaveForm(NumofSamples,da_samplerate)
    w2.base.insert(KILO_B(1),rectangle(KILO_B(50)))
    w2.carrier.add(c1)
    w2.carrier.update()
    w2.update('spcm4')
    figure(),plot(w2.waveform)
    
    wfdata=np.array([w1.waveform,w2.waveform]).T.flatten() 
#    wfdata=wfdata.reshape(2,-1).transpose().flatten()
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

    sp2=Spcm_AD(2)
    sp2.setRangeAll('1000mV')
    sp2.setClockMode('int')
    sp1.setTrigger(trig_source='ext0',mode='pos',level=1000,coupling='DC',impedance='50Ohm')
#    sp2.setTriggerSource('ext0')
#    sp2.setTriggerMode(trig='ext0',mode='pos')
#    sp2.setTriggerLevel(1000)
#    sp2.setTriggerInputCoupling('DC')
#    sp2.setTriggerImpedance('50Ohm')
    sp2.setInputAll()
    sp2.setRecord(1024,100,pretrig=32)
    sp2.start()
#    sp2.stop()
    data_ch0,data_ch1=sp2.getData(0),sp2.getData(1)
    figure(),plot(data_ch0,'o-')
#    from Instrument.M4i_2211 import M4i2211
#    #from Instrument.M4i_Sync6631 import sync6631   
#    da1=M4i2211()
#    da1.setAnalogAllIn(3,2500)
#    da1.setSampleRate_InterClock(5000)
#    da1.setTrigger('ext',500)
#    da1.setFIFOmode(3,1024,1,1)
#    bufCh0,bufCh1=da1.getFIFOdata(3)
#    figure()
#    plot(bufCh0)
