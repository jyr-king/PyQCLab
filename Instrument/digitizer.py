# -*- coding: utf-8 -*-
"""
Created on Wed May 18 00:41:38 2016

@author: Xmon-SC05
"""
from ctypes import *
from AlazarDefs import *
import numpy as np

class digitizer:
    """
        This class provide configuration and capture data function to ATS9360 board.
    """
    MAX_SAMPLERATE=1.8e9
    MIN_SAMPLERATE=1e3
    MIN_RECORD_LEN=256
    
    def __init__(self,systemID=1,boardID=1):
        self.__alazarapi=cdll.LoadLibrary('ATSApi.dll')
        self.__boardhandle=self.__alazarapi.AlazarGetBoardBySystemID(systemID,boardID)
        self.__voltA=np.array([])
        self.__voltB=np.array([])
        self.__recordlength=1024
        self.__samplerate='100msps'
        self.__SamplesPerSec=int(100e6)
        self.__CHANNELS_PER_BOARD=2
        #计算板卡的最大内存占用和每个采样点的bit数
        self.__MIN_RECORD_LEN=256     #设置一个记录的最小长度为256.
        self.__MEMORY_SIZE=c_uint32()
        self.__BITS_PER_SAMPLE=c_uint8()
        self.__alazarapi.AlazarGetChannelInfo(self.__boardhandle,
                                byref(self.__MEMORY_SIZE),
                                byref(self.__BITS_PER_SAMPLE)
                                )
        self.__MEMORY_SIZE=self.__MEMORY_SIZE.value
        self.__BITS_PER_SAMPLE=self.__BITS_PER_SAMPLE.value
        self.__BYTES_PER_SAMPLE=int((self.__BITS_PER_SAMPLE + 7)/8) 
    
    def _getApi(self):
        return self.__alazarapi
    def _setApi(self,lib):
        self.__alazarapi=cdll.LoadLibrary(lib)
    alazarapi=property(fget=_getApi,fset=_setApi)
    
    def getChannelInfo(self):
                                            
    def set_samplerate(self,samplerate):
        if samplerate < self.MIN_SAMPLERATE:
            print('Warning:samplerate too low, using the lowest value 1Ksps.')
            self.__samplerate='1ksps'
            self.__SamplesPerSec=self.MIN_SAMPLERATE
        elif samplerate > self.MAX_SAMPLERATE:
            print('Warning:samplerate too high, using the highest value 1.8Gsps.')
            self.__samplerate='1800msps'
            self.__SamplesPerSec=self.MAX_SAMPLERATE
        else:
            count=0
            hit=False
            while not hit:
                if samplerate_table[count]<samplerate:
                    count+=1
                else:
                    self.__SamplesPerSec=int(samplerate_table[count])
                    if self.__SamplesPerSec < int(1e6):
                        self.__samplerate=str(self.__SamplesPerSec/1e3).split('.')[0]+'ksps'
                    else:
                        self.__samplerate=str(self.__SamplesPerSec/1e6).split('.')[0]+'msps'
                    hit=True
        return self.__SamplesPerSec
        
    def get_samplerate(self):
#        print(self.__samplerate)
        return self.__SamplesPerSec
        
    def samplerateToString(self,samplerate):
        idx=np.abs(samplerate_table-samplerate).argmin()
        samplerate=int(samplerate_table[idx])
        if samplerate < 1e6:
            return samplerate,str(samplerate/1e3).split('.')[0]+'ksps'
        else:
            return samplerate,str(samplerate/1e6).split('.')[0]+'ksps'
            
    def _getSampleRate(self):
        return self.__SamplesPerSec
    def _setSampleRate(self,samplerate):
        if isinstance(samplerate,(float,int)):
            if samplerate < self.MIN_SAMPLERATE:
                samplerate=self.MIN_SAMPLERATE
            elif samplerate > self.MAX_SAMPLERATE:
                samplerate=self.MAX_SAMPLERATE
            self.__SamplesPerSec,self.__samplerate=self.samplerateToString(samplerate)
    samplerate=property(fget=_getSampleRate,fset=_setSampleRate)
        
    def set_recordlength(self,length):
        length=int(length)
        if length < self.__MIN_RECORD_LEN:
            self.__recordlength = self.__MIN_RECORD_LEN
        else:
            self.__recordlength = 256+int((length-128)/128)*128
        #计算板卡的最大内存占用和每个采样点的bit数
                                         
        #如果采样点设置太多，超出最大内存值，则报溢出警告。
        if (self.__MEMORY_SIZE > 0) and (length > self.__MEMORY_SIZE):
            print('Warning:Too many samples per record!')
            self.__recordlength = self.__MEMORY_SIZE
        return self.__recordlength
            
    def get_recordlength(self):
        return self.__recordlength
        
    def _setRecordLength(self,length):
        length=int(length)
        if length < self.MIN_RECORD_LEN:
            self.__recordlength = self.MIN_RECORD_LEN
        else:
            self.__recordlength = 256+int((length-128)/128)*128
        if (self.__MEMORY_SIZE > 0) and (length > self.__MEMORY_SIZE):
            print('Warning:Too many samples per record!')
            self.__recordlength = self.__MEMORY_SIZE
    
    def set_captureclock(self,timebase='INT',edge='RISING',decimation=0):      
        return self.__alazarapi.AlazarSetCaptureClock(self.__boardhandle,
                                            dict_clocksource[timebase],dict_samplerate[self.__samplerate],
                                            dict_clkedge[edge],decimation
                                            )
                                            
    def set_inputcontrol(self,channel='CH_ALL',coupling='DC',inputrange='400mV',impedance='50_OHM'):
        self.__alazarapi.AlazarInputControl(self.__boardhandle,
                                        dict_channels['CHA'],dict_coupling[coupling],
                                        dict_inputrange[inputrange],dict_impedance[impedance]
                                        )
        return self.__alazarapi.AlazarInputControl(self.__boardhandle,
                                        dict_channels['CHB'],dict_coupling[coupling],
                                        dict_inputrange[inputrange],dict_impedance[impedance]
                                        )
                                        
    def set_triggeroperation(self,trigengop='J',trigsourcej='TRIG_CHA',trigsourcek='TRIG_DISABLE',
                                  trigslopej='POS',trigslopek='POS',triglevelj=128,triglevelk=128):
        return self.__alazarapi.AlazarSetTriggerOperation(self.__boardhandle,dict_trigengop[trigengop],
                            TRIG_ENGINE_J,dict_trigsource[trigsourcej],dict_trigslope[trigslopej],triglevelj,
                            TRIG_ENGINE_K,dict_trigsource[trigsourcek],dict_trigslope[trigslopek],triglevelk
                            )
                            
                            
    def set_externaltrigger(self,coupling='DC',couplerange='5V'):
        return self.__alazarapi.AlazarSetExternalTrigger(self.__boardhandle,dict_coupling['DC'],dict_couplerange['5V'])
        
    def set_triggermisc(self,delay=0,timeout=0):        
        return (self.__alazarapi.AlazarSetTriggerDelay(self.__boardhandle,delay),\
                self.__alazarapi.AlazarSetTriggerTimeOut(self.__boardhandle,timeout))
                
    def configaux(self,auxmode='OUT_TRIGGER',param=0):
        return self.__alazarapi.AlazarConfigureAuxIO(self.__boardhandle,dict_auxmode[auxmode],param)
        
    def get_data(self,channel='CH_ALL'):
        if channel=='CH_ALL':
            return self.__voltA,self.__voltB
        elif channel=='CHA':
            return self.__voltA
        elif channel=='CHB':
            return self.__voltB
            
    def get_timestamp(self):
        return self.__t
    def sleepdevice(self,state='POWER_OFF'):
        return self.__alazarapi.AlazarSleepDevice(self.__boardhandle,dict_devicestate[state])
        
    def AcqData(self,acquisitionLength_sec=0.1,channel='CH_ALL',mode='CS'):
        #设置采样点数，等于采样时间乘以采样率        
        samplesPerChannel = self.get_recordlength()
        if acquisitionLength_sec > 0: 
            samplesPerAcquisition = int(np.floor((self.__SamplesPerSec * acquisitionLength_sec + 0.5)))
            buffersPerAcquisition = int(np.floor((samplesPerAcquisition + samplesPerChannel - 1) / samplesPerChannel))
            if buffersPerAcquisition > 32:
                self.set_recordlength(samplesPerAcquisition/32)
                samplesPerChannel = self.get_recordlength()
                buffersPerAcquisition = int(np.floor((samplesPerAcquisition + samplesPerChannel - 1) / samplesPerChannel))
        else :
            buffersPerAcquisition = hex2dec('7FFFFFFF') # acquire until aborted
        
        
        #连续模式下只用一个record，record的长度根据NPT模式下的测试结果，设定为256+128*N.
        
        #设置缓存timeout        
        bufferTimeout_ms = 5000
        #设置channelmask，每次采样之前重置channelcount。板卡有两个通道
        if channel == 'CH_ALL':
            channelMask = dict_channels['CHA'] + dict_channels['CHB']
        else:
            channelMask = dict_channels[channel] 
        channelCount = 0
        channelsPerBoard = self.__CHANNELS_PER_BOARD
        #根据channelmask计算采样通道数
        for channel in range(channelsPerBoard):
            channelId = 2**channel
            if channelId&channelMask:
                channelCount += 1
        #判断channelmask设置是否有问题
        if (channelCount < 1) or (channelCount > channelsPerBoard):
            print('Invalid channel mask {}\n'.format(channelMask))
            return
 
        samplesPerBuffer = samplesPerChannel * channelCount
        bytesPerBuffer = self.__BYTES_PER_SAMPLE * samplesPerBuffer

        

        bufferCount = 16
###AlazarAllocBufferU16调用要返回一个指向分配的buffer空间块的地址指针，但是ctypes默认返回值是整数，
###    因此用restype方法重新指定返回值类型。
        self.__alazarapi.AlazarAllocBufferU16.restype=POINTER(c_uint16)
        buffers=list()
        for j in range(bufferCount):
            pbuffer=self.__alazarapi.AlazarAllocBufferU16(self.__boardhandle,samplesPerBuffer)
            if pbuffer == 0:
                print('Error:Buffer allocation failed.')
                raise ValueError
            buffers.append(pbuffer)
            
        #每次采样之前清除上次的残留数据：
        self.__voltA=np.array([])
        self.__voltB=np.array([])
        rawdata=np.array([])
        #选择采样模式：连续模式或触发连续模式
        if mode == 'CS':
            admaFlags = ADMA_EXTERNAL_STARTCAPTURE + ADMA_CONTINUOUS_MODE + ADMA_FIFO_ONLY_STREAMING
        elif mode == 'TS':
            admaFlags = ADMA_EXTERNAL_STARTCAPTURE + ADMA_TRIGGERED_STREAMING + ADMA_FIFO_ONLY_STREAMING
        self.__alazarapi.AlazarBeforeAsyncRead(self.__boardhandle, 
                                              channelMask, 0, samplesPerChannel, 1, 
                                              buffersPerAcquisition, admaFlags
                                              )
        #加载buffer                                      
        for bufferIndex in range(bufferCount):
            pbuffer = buffers[bufferIndex]
            retCode = self.__alazarapi.AlazarPostAsyncBuffer(self.__boardhandle, pbuffer, bytesPerBuffer)
            if retCode != 512:
                print('Error:post buffer failed. errorcode={}'.format(retCode))
                raise ValueError
        #让板卡开始采样
        retCode = self.__alazarapi.AlazarStartCapture(self.__boardhandle)
        if retCode != 512:
            print('Error:start capture failed. errorcode={}'.format(retCode))
            raise ValueError
    
        buffersCompleted = 0
        captureDone = False
        success = False

        while not(captureDone):

            bufferIndex = np.mod(buffersCompleted, bufferCount)
            pbuffer = buffers[bufferIndex]

   # % Wait for the first available buffer to be filled by the board
            self.__alazarapi.AlazarWaitAsyncBufferComplete(self.__boardhandle, pbuffer, bufferTimeout_ms)
            if retCode == 512: 
       # % This buffer is full
                bufferFull = True
                captureDone = False
            elif retCode == dict_errorcode['ApiWaitTimeout']:
        #% The wait timeout expired before this buffer was filled.
        #% The board may not be triggering, or the timeout period may be too short.
                print('Error: AlazarWaitAsyncBufferComplete timeout')
                bufferFull = False
                captureDone = True
            else:
        #% The acquisition failed
#                raise ValueError, 'Error: AlazarWaitAsyncBufferComplete failed -- Errorcode %s\n' %(retCode)
                bufferFull = False
                captureDone = True

            if bufferFull:
                rawdata = np.append(rawdata,pbuffer[0:samplesPerBuffer])
    
            retCode = self.__alazarapi.AlazarPostAsyncBuffer(self.__boardhandle, pbuffer, bytesPerBuffer)
#            if retCode != 512:
#                raise ValueError
        
#% Update progress
            buffersCompleted = buffersCompleted + 1
            if buffersCompleted >= buffersPerAcquisition:
                captureDone = True
                success = True

        retCode = self.__alazarapi.AlazarAbortAsyncRead(self.__boardhandle)
        if retCode != 512:
            raise ValueError
        
        for pbuffer in buffers:
            retCode = self.__alazarapi.AlazarFreeBufferU16(self.__boardhandle,pbuffer)
            if retCode != 512:
                raise ValueError
    
#        dataA=rawdata[::2]
#        dataB=rawdata[1::2]      
        self.__voltA=0.4*(rawdata[::2]/16-2048)/2048  
        self.__voltB=0.4*(rawdata[1::2]/16-2048)/2048
        self.__t=np.arange(self.__voltA.size)/self.__SamplesPerSec
        return success
        
    def AcqData_NPT(self,SamplesperTrig,RecordsperAcq,channel='CH_ALL',mode='NPT'):
        preTriggerSamples = 0
        postTriggerSamples = int(SamplesperTrig)
        recordsPerBuffer = 100
        buffersPerAcquisition = int(np.ceil(RecordsperAcq/recordsPerBuffer))
        bufferTimeout_ms = 5000
        
        if channel == 'CH_ALL':
            channelMask = dict_channels['CHA'] + dict_channels['CHB']
        else:
            channelMask = dict_channels[channel] 
        channelCount = 0
        channelsPerBoard = self.__CHANNELS_PER_BOARD
        #根据channelmask计算采样通道数
        for channel in range(channelsPerBoard):
            channelId = 2**channel
            if channelId&channelMask:
                channelCount += 1
        #判断channelmask设置是否有问题
        if (channelCount < 1) or (channelCount > channelsPerBoard):
            print('Invalid channel mask {}\n'.format(channelMask))
            return
        #计算每个记录的长度    
#        samplesPerRecord = preTriggerSamples + postTriggerSamples
        samplesPerRecord = self.set_recordlength(preTriggerSamples + postTriggerSamples)
            
        samplesPerBuffer = samplesPerRecord * recordsPerBuffer * channelCount
        bytesPerBuffer = self.__BYTES_PER_SAMPLE * samplesPerBuffer         

        #分配采样内存
        bufferCount = 16
        self.__alazarapi.AlazarAllocBufferU16.restype=POINTER(c_uint16)
        buffers=list()
        for j in range(bufferCount):
            pbuffer=self.__alazarapi.AlazarAllocBufferU16(self.__boardhandle,samplesPerBuffer)
            if pbuffer == 0:
                print('Error: AlazarAllocBufferU16 {} samples failed'.format(samplesPerBuffer))
                return
            buffers.append(pbuffer)
            
        #每次采样之前清除上次的残留数据：
        self.voltA=np.array([])
        self.voltB=np.array([])    
        rawdata=np.array([])
        #下面这一行有点存疑。
        self.__alazarapi.AlazarSetRecordSize(self.__boardhandle,preTriggerSamples, samplesPerRecord-preTriggerSamples)
        if mode == 'NPT':
            admaFlags = ADMA_EXTERNAL_STARTCAPTURE + ADMA_NPT + ADMA_FIFO_ONLY_STREAMING
        elif mode == 'TR':
            admaFlags = ADMA_EXTERNAL_STARTCAPTURE + ADMA_TRADITIONAL_MODE + ADMA_FIFO_ONLY_STREAMING
        recordsPerAcquisition = recordsPerBuffer * buffersPerAcquisition
        self.__alazarapi.AlazarBeforeAsyncRead(self.__boardhandle, 
                                              channelMask, -int(preTriggerSamples), samplesPerRecord, recordsPerBuffer, 
                                              recordsPerAcquisition, admaFlags
                                              )
        for bufferIndex in range(bufferCount):
            pbuffer = buffers[bufferIndex]
            retCode = self.__alazarapi.AlazarPostAsyncBuffer(self.__boardhandle, pbuffer, bytesPerBuffer)
            if retCode != 512:
                raise ValueError                                      
       # Update status
#        if buffersPerAcquisition == hex2dec('7FFFFFFF'):
#            print('Capturing buffers until aborted...')
#        else:
#            print('Capturing {} buffers ...'.format(buffersPerAcquisition))

# Arm the board system to wait for triggers
        retCode = self.__alazarapi.AlazarStartCapture(self.__boardhandle)
        
# Wait for sufficient data to arrive to fill a buffer, process the buffer,
# and repeat until the acquisition is complete  
        buffersCompleted = 0
        captureDone = False
        success = False

        while not(captureDone):

            bufferIndex = np.mod(buffersCompleted, bufferCount)
            pbuffer = buffers[bufferIndex]
            self.__alazarapi.AlazarWaitAsyncBufferComplete(self.__boardhandle, pbuffer, bufferTimeout_ms)
            if retCode == 512: 
       # % This buffer is full
                bufferFull = True
                captureDone = False
            elif retCode == dict_errorcode['ApiWaitTimeout']:
        #% The wait timeout expired before this buffer was filled.
        #% The board may not be triggering, or the timeout period may be too short.
                print('Error: AlazarWaitAsyncBufferComplete timeout')
                bufferFull = False
                captureDone = True
            else:
        #% The acquisition failed
                print('Error: AlazarWaitAsyncBufferComplete failed, errorCode={}'.format(retCode))
                bufferFull = False
                captureDone = True

            if bufferFull:
                rawdata = np.append(rawdata,pbuffer[0:samplesPerBuffer])
    
            retCode = self.__alazarapi.AlazarPostAsyncBuffer(self.__boardhandle, pbuffer, bytesPerBuffer)
#            if retCode != 512:
#                raise ValueError
        
#% Update progress
            buffersCompleted = buffersCompleted + 1
            if buffersCompleted >= buffersPerAcquisition:
                captureDone = True
                success = True

        retCode = self.__alazarapi.AlazarAbortAsyncRead(self.__boardhandle)
        if retCode != 512:
            raise ValueError
        
        for pbuffer in buffers:
            retCode = self.__alazarapi.AlazarFreeBufferU16(self.__boardhandle,pbuffer)
            if retCode != 512:
                raise ValueError   
#        dataA=rawdata[::2]
#        dataB=rawdata[1::2]
        rawdata=rawdata.reshape((recordsPerAcquisition,rawdata.size/recordsPerAcquisition))
#        dataA=self.rawdata[:,::2]
#        dataB=self.rawdata[:,1::2]
        self.__voltA=0.4*(rawdata[:,::2]/16-2048)/2048  
        self.__voltB=0.4*(rawdata[:,1::2]/16-2048)/2048
        self.__t=np.arange(self.__voltA.size)/self.__SamplesPerSec
#        del buffers,rawdata 
        return success                              