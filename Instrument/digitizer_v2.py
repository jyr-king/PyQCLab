# -*- coding: utf-8 -*-
"""
Created on Wed May 18 00:41:38 2016

@author: Xmon-SC05
"""
from ctypes import *
from PyQCLab.Instrument.AlazarDefs import *
#from AlazarDefs import samplerate_table
import numpy as np


class digitizer:
    """
        This class provide configuration and capture data function to ATS9360 board.
    """
    MAX_SAMPLERATE=int(1.8e9)
    MIN_SAMPLERATE=int(1e3)
    MIN_RECORD_LEN=256
    CHANNELS_PER_BOARD=2
    def __init__(self,systemID=1,boardID=1,lib='ATSApi.dll',samplerate=1e8,recordlength=1024,acqlength=1024,records=1,mode='CS'):
        self.alazarapi=lib
        self.boardhandle=((systemID,boardID))
        self.getChannelInfo()
        self.recordlength=recordlength
        self.samplerate=samplerate
        self.acqlength=acqlength
        self.records=records
        
        self.mode=mode
        self.data=np.array([])
        
#        self.set_captureclock()
# ?       self.set_externaltrigger()
#        self.set_inputcontrol()
#        self.set_triggermisc()
#        self.set_triggeroperation()
        
    def _getApi(self):
        return self.__alazarapi
    def _setApi(self,lib):
        self.__alazarapi=cdll.LoadLibrary(lib)
    alazarapi=property(fget=_getApi,fset=_setApi)
    
    def _getBoardhandle(self):
        return self.__boardhandle
    def _setBoardhandle(self,ID):
        systemID,boardID=ID
        self.__boardhandle=self.alazarapi.AlazarGetBoardBySystemID(systemID,boardID)
    boardhandle=property(_getBoardhandle,_setBoardhandle)
    
    def getChannelInfo(self):
        memorySize=c_uint32()
        bitsPerSample=c_uint8()
        self.alazarapi.AlazarGetChannelInfo(self.boardhandle,
                                byref(memorySize),
                                byref(bitsPerSample)
                                )
        self.__MEMORY_SIZE=memorySize.value
        self.__BITS_PER_SAMPLE=bitsPerSample.value
        self.__BYTES_PER_SAMPLE=int((self.__BITS_PER_SAMPLE + 7)/8)
    def channelInfo(self):
        return 'Memory_size={},Bits per sample={},Bytes per sample={}'.format(self.__MEMORY_SIZE,self.__BITS_PER_SAMPLE,self.__BYTES_PER_SAMPLE)
        
    def samplerateToString(self,samplerate):
        samplerate_table=[1e3,2e3,5e3,1e4,2e4,5e4,1e5,2e5,5e5,1e6,2e6,5e6,10e6,20e6,25e6,50e6,100e6,\
                    125e6,160e6,180e6,200e6,250e6,400e6,500e6,800e6,1e9,1.2e9,1.5e9,1.6e9,1.8e9,2e9]
        idx=np.abs(np.array(samplerate_table)-samplerate).argmin()
#        idx=np.abs(np.array(samplerate_table)-samplerate).argmin()
        samplerate=int(samplerate_table[idx])
        if samplerate < 1e6:
            return samplerate,str(samplerate/1e3).split('.')[0]+'ksps'
        else:
            return samplerate,str(samplerate/1e6).split('.')[0]+'msps'
            
    def _getSampleRate(self):
        return self.__SamplesPerSec
    def _setSampleRate(self,samplerate):
        if isinstance(samplerate,(float,int)):
#            if samplerate < self.MIN_SAMPLERATE:
#                samplerate=self.MIN_SAMPLERATE
#            elif samplerate > self.MAX_SAMPLERATE:
#                samplerate=self.MAX_SAMPLERATE
            self.__SamplesPerSec,self.__samplerate=self.samplerateToString(samplerate)
    samplerate=property(_getSampleRate,_setSampleRate)
        
    def _getRecordLength(self):
        return self.__recordlength
    def _setRecordLength(self,length):
        if length < self.MIN_RECORD_LEN:
            length = self.MIN_RECORD_LEN
        else:
            length = 256+int((length-128)/128)*128
        if (self.__MEMORY_SIZE > 0) and (length > self.__MEMORY_SIZE):
            length = self.__MEMORY_SIZE
        self.__recordlength=length
    recordlength=property(_getRecordLength,_setRecordLength)
    
    def set_captureclock(self,timebase='INT',edge='RISING',decimation=0):
        if timebase in ['int','INT']:
            return self.alazarapi.AlazarSetCaptureClock(self.boardhandle,
                                            dict_clocksource[timebase],dict_samplerate[self.__samplerate],
                                            dict_clkedge[edge],decimation
                                            )
        if timebase in ['ext_10m','EXT_10MHz_REF']:
            return self.alazarapi.AlazarSetCaptureClock(self.boardhandle,
                                            dict_clocksource[timebase],self.__SamplesPerSec,
                                            dict_clkedge[edge],1
                                            )
                                            
    def set_inputcontrol(self,channel='CH_ALL',coupling='DC',inputrange='400mV',impedance='50_OHM'):
        self.alazarapi.AlazarInputControl(self.boardhandle,
                                        dict_channels['CHA'],dict_coupling[coupling],
                                        dict_inputrange[inputrange],dict_impedance[impedance]
                                        )
        return self.alazarapi.AlazarInputControl(self.boardhandle,
                                        dict_channels['CHB'],dict_coupling[coupling],
                                        dict_inputrange[inputrange],dict_impedance[impedance]
                                        )
                                        
    def set_triggeroperation(self,trigengop='J',trigsourcej='TRIG_CHA',trigsourcek='TRIG_DISABLE',
                                  trigslopej='POS',trigslopek='POS',triglevelj=128,triglevelk=128):
        return self.alazarapi.AlazarSetTriggerOperation(self.boardhandle,dict_trigengop[trigengop],
                            TRIG_ENGINE_J,dict_trigsource[trigsourcej],dict_trigslope[trigslopej],triglevelj,
                            TRIG_ENGINE_K,dict_trigsource[trigsourcek],dict_trigslope[trigslopek],triglevelk
                            )
                            
                            
    def set_externaltrigger(self,coupling='DC',couplerange='5V'):
        return self.alazarapi.AlazarSetExternalTrigger(self.boardhandle,dict_coupling[coupling],dict_couplerange[couplerange])
        
    def set_triggermisc(self,delay=0,timeout=0):        
        return (self.alazarapi.AlazarSetTriggerDelay(self.boardhandle,delay),\
                self.alazarapi.AlazarSetTriggerTimeOut(self.boardhandle,timeout))
                
    def configaux(self,auxmode='OUT_TRIGGER',param=0):
        return self.alazarapi.AlazarConfigureAuxIO(self.boardhandle,dict_auxmode[auxmode],param)
        
    def sleep(self,state='POWER_OFF'):
        return self.alazarapi.AlazarSleepDevice(self.boardhandle,dict_devicestate[state])
        
    def start(self):
        bufferTimeout_ms = 5000
        bufferCount = 16
        """在连续流采样模式下，采样点数samplesPerAcquisition是通过采样时间计算而来的。
        （在这里我们将这个换算放在其他的模块中去，也就是说digitizer类只接受采样点数作为参数）
        单个记录的长度samplesPerChannel可以小于总的采样点数，这样就要计算需要多少个buffer（buffersPerAcquisition）来完成一次采样。
        如果所需buffer的数量超过32，则认为单个记录长度设置得太短了，需要重新设置。"""
        if self.mode in ['CS','TS']:
            samplesPerRecord=self.recordlength
            samplesPerAcquisition=self.acqlength
            recordsPerBuffer = 1
            if samplesPerAcquisition > 0:
                buffersPerAcquisition=int(np.floor((samplesPerAcquisition + samplesPerRecord - 1) / samplesPerRecord))
                if buffersPerAcquisition > 32:
                    self.recordlength=samplesPerAcquisition/32
                    samplesPerRecord = self.recordlength
                    buffersPerAcquisition = int(np.floor((samplesPerAcquisition + samplesPerRecord - 1) / samplesPerRecord))
            else:
                buffersPerAcquisition = hex2dec('7FFFFFFF') # acquire until aborted
#            recordsPerAcquisition = recordsPerBuffer * buffersPerAcquisition
        elif self.mode in ['NPT','TR']:
#            preTriggerSamples = 0
#            postTriggerSamples = self.recordlength
            samplesPerRecord=self.recordlength
            samplesPerAcquisition=samplesPerRecord*self.records
            self.acqlength=samplesPerAcquisition
            recordsPerBuffer = 100
            buffersPerAcquisition = int(np.ceil(self.records/recordsPerBuffer))
        recordsPerAcquisition = recordsPerBuffer * buffersPerAcquisition
        self.records=recordsPerAcquisition
        samplesPerChannel=samplesPerRecord*recordsPerBuffer

        #——————————以下设置channelMask.——————————————————————————————————————#
        channel='CH_ALL' #就目前的采数要求而言，同时采两路总是可行的，暂不开放单路采样的设置。
        if channel == 'CH_ALL':
            channelMask = dict_channels['CHA'] + dict_channels['CHB']
        else:
            channelMask = dict_channels[channel] 
        channelCount = 0
        channelsPerBoard = self.CHANNELS_PER_BOARD
        #根据channelmask计算采样通道数
        for channel in range(channelsPerBoard):
            channelId = 2**channel
            if channelId&channelMask:
                channelCount += 1
        #判断channelmask设置是否有问题
        if (channelCount < 1) or (channelCount > channelsPerBoard):
            print('Invalid channel mask {}\n'.format(channelMask))
            return
                
        #——————————以下分配buffer内存。——————————————————————————————————————#    
        samplesPerBuffer = samplesPerChannel * channelCount
        bytesPerBuffer = self.__BYTES_PER_SAMPLE * samplesPerBuffer
        
        self.alazarapi.AlazarAllocBufferU16.restype=POINTER(c_uint16)
        buffers=list()
        for j in range(bufferCount):
            pbuffer=self.alazarapi.AlazarAllocBufferU16(self.boardhandle,samplesPerBuffer)
            if pbuffer == 0:
                print('Error:Buffer allocation failed.')
                raise ValueError
            buffers.append(pbuffer)
            
        rawdata=np.zeros(samplesPerBuffer*buffersPerAcquisition)
        if self.mode in ['NPT','TR']:
            self.alazarapi.AlazarSetRecordSize(self.boardhandle,0,samplesPerRecord)
        #——————————选择采样模式：设置DAMFlags。——————————————————————————————#
        if self.mode == 'CS':
            admaFlags = ADMA_EXTERNAL_STARTCAPTURE + ADMA_CONTINUOUS_MODE + ADMA_FIFO_ONLY_STREAMING
        elif self.mode == 'TS':
            admaFlags = ADMA_EXTERNAL_STARTCAPTURE + ADMA_TRIGGERED_STREAMING + ADMA_FIFO_ONLY_STREAMING
        elif self.mode == 'NPT':
            admaFlags = ADMA_EXTERNAL_STARTCAPTURE + ADMA_NPT + ADMA_FIFO_ONLY_STREAMING
        elif self.mode == 'TR':
            admaFlags = ADMA_EXTERNAL_STARTCAPTURE + ADMA_TRADITIONAL_MODE + ADMA_FIFO_ONLY_STREAMING    
        self.alazarapi.AlazarBeforeAsyncRead(self.boardhandle, 
                                              channelMask, 0, samplesPerRecord, recordsPerBuffer, 
                                              recordsPerAcquisition, admaFlags
                                              )
        #——————————加载buffer。——————————————————————————————#                                      
        for i in range(bufferCount):
            pbuffer = buffers[i]
            retCode = self.alazarapi.AlazarPostAsyncBuffer(self.boardhandle, pbuffer, bytesPerBuffer)
            if retCode != 512:
                print('Error:post buffer failed. errorcode={}'.format(retCode))
                raise ValueError
        #——————————开始采样。——————————————————————————————#        
        retCode = self.alazarapi.AlazarStartCapture(self.boardhandle)
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
            self.alazarapi.AlazarWaitAsyncBufferComplete(self.boardhandle, pbuffer, bufferTimeout_ms)
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
            #————————当一个buffer采满了之后，取出其中的数据。——————————————————#
            if bufferFull:
                i0=buffersCompleted*samplesPerBuffer
                rawdata[i0:i0+samplesPerBuffer] = pbuffer[0:samplesPerBuffer]
            #——————————将已经取出数据的buffer重新放到buffer队列的尾部。————————#
            retCode = self.alazarapi.AlazarPostAsyncBuffer(self.boardhandle, pbuffer, bytesPerBuffer)
#            if retCode != 512:
#                raise ValueError
        
#% Update progress
            buffersCompleted += 1
            if buffersCompleted >= buffersPerAcquisition:
                captureDone = True
                success = True
        #————————————退出采样。————————————————————————————————————————#
        retCode = self.alazarapi.AlazarAbortAsyncRead(self.boardhandle)
        if retCode != 512:
            raise ValueError
        #————————————释放内存。————————————————————————————————————————#
        for pbuffer in buffers:
            retCode = self.alazarapi.AlazarFreeBufferU16(self.boardhandle,pbuffer)
            if retCode != 512:
                raise ValueError
    
#        dataA=rawdata[::2]
#        dataB=rawdata[1::2]      
#        self.__voltA=0.4*(rawdata[::2]/16-2048)/2048  
#        self.__voltB=0.4*(rawdata[1::2]/16-2048)/2048
#        self.__t=np.arange(self.__voltA.size)/self.__SamplesPerSec
        self.__rawdata=rawdata.reshape((buffersPerAcquisition,recordsPerBuffer,-1))
        return success
  
    def _getData(self):
        try:
#            if self.mode in ['CS','TS']:
#                data=(0.4*(self.__rawdata/16-2048)/2048).reshape((-1,2))
#            elif self.mode in ['NPT','TR']:
#                rawdata=self.__rawdata.reshape((-1,rawdata.size/self.records))                
#                data=0.4*(self.__rawdata[:,:,::2]/16-2048)/2048
#                
#            self.__data= data[:self.acqlength,:]
            dataA=(0.4*(self.__rawdata[:,:,::2]/16-2048)/2048).flatten()
            dataB=(0.4*(self.__rawdata[:,:,1::2]/16-2048)/2048).flatten()
            self.__data=(dataA,dataB)
            return self.__data
#            self.__voltA=0.4*(self.__rawdata[::2]/16-2048)/2048  
#            self.__voltB=0.4*(self.__rawdata[1::2]/16-2048)/2048
        except:
            return self.__data
    def _setData(self,data):
        self.__data=data
    data=property(_getData,_setData)                         