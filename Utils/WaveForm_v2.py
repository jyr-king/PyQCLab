
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:21:11 2016

@author: Xmon-SC05
"""
import numpy as np

#用于生成高斯型边沿。
def gaussian_r(length,std):
    x=np.arange(0,length)
    return np.exp(-(x-length)**2/std**2)
def gaussian_f(length,std):
    x=np.arange(0,length)
    return 1-np.exp(-(x-length)**2/std**2)
def kaiser_r(length,beta):
    return np.kaiser(length*2,beta)[:length]
def kaiser_f(length,beta):
    return np.kaiser(length*2,beta)[length:]
def linear_edge(length,*args):
    return np.linspace(0,1,length,endpoint=False)
#用于生成高斯型窗函数    
def gaussian(length,std):
    x=np.arange(0,length)
    return np.exp(-(x-length/2)**2/std**2)
#平直函数，等价于ones，但参数可以和sin,cos等函数相同
def flat1(x):
    return np.ones(x.shape)

def kaiser_half(length,beta):
    pass            
class WaveForm:
    digit_depth={'awg5000':14,'spcm4':16}
    markers={'awg5000':2,'spcm4':0}
    dataFormats={'awg5000':'uint16','spcm4':'int16'}
    def __init__(self,length=1000,AWGType='awg5000'):
        self.length=int(length)
        self.AWGType=AWGType
        self.createBase()
        self.createWindow((('rectangle',0,0,0,0),))
        self.createMarker1(((0,0),))
        self.createMarker2(((0,0),))
        self.createWaveform()
#        self.baseband('ones')
#        self.window=np.zeros(length)
#        self.rawData=np.zeros(length)
#        self.WFData=np.zeros(length).astype('int16')
#        self.Marker1=np.zeros(length).astype('int')
#        self.Marker2=np.zeros(length).astype('int')
        
    def _setLength(self, length):
        self.__WFlength=int(length)
    def _getLength(self):
        return self.__WFlength
    length=property(fget=_getLength,fset=_setLength)
    
    def _setAWGType(self,awgtype):
        self.__AWGType=awgtype
    def _getAWGType(self):
        return self.__AWGType
    AWGType=property(fget=_getAWGType,fset=_setAWGType)
    
    def createBase(self,func='flat1',period=1,phase=0,offset=0):
#        period=period
#        offset=offset
        funcs={'flat1':flat1,'sin':np.sin,'cos':np.cos}
        if func in funcs.keys():
            self.baseBand=funcs[func](np.linspace(phase,phase+2*np.pi*period,self.length))+offset
    
    def createWindow(self,windows):
        '''windows are parameter sets in the form (function, start, stop, arg, amplitude).'''
        winfuncs1={'rectangle':np.ones,
                   'hanning':np.hanning,
                   'hamming':np.hamming
                   }
        winfuncs2={'gaussian':gaussian,
                   'gaussian_r':gaussian_r,
                   'gaussian_f':gaussian_f,
                   'kaiser':np.kaiser,
                   'kaiser_r':kaiser_r,
                   'kaiser_f':kaiser_f
                   }
        self.window=np.zeros(self.length)
        for win in windows:
            if win[0] in winfuncs1.keys():
                self.window[win[1]:win[2]]=winfuncs1[win[0]](win[2]-win[1])*win[4]
            elif win[0] in winfuncs2.keys():
                self.window[win[1]:win[2]]=winfuncs2[win[0]](win[2]-win[1],win[3])*win[4]
    
    def createWaveform(self):
        self.rawWaveform=self.baseBand*self.window
        depth=self.digit_depth[self.AWGType]
        if self.dataFormats[self.AWGType] == 'uint16':
            self.waveform=(self.rawWaveform*2**(depth-1)+2**(depth-1)-self.rawWaveform).astype('uint16')
        elif self.dataFormats[self.AWGType] == 'int16':
            self.waveform=(self.rawWaveform*2**(depth-1)-self.rawWaveform).astype('int16')
        if self.AWGType in ['awg5000']:
            self.waveform+=self.marker1*2**depth+self.marker2*2**(depth+1)
#            np.floor((self.rawWaveform+1)*2**(self.__DIGITAL_DEPTH-1)-Data_n)+\
#                                self.__Marker1*2**self.__DIGITAL_DEPTH+\
#                                self.__Marker2*2**(self.__DIGITAL_DEPTH+1)            
#    def get_waveform(self,format=True):
#        if format:
#            return self.__WFData
#        else:
#            return self.__rawData
            
#    def window(self):
#        return self.__Window
        
#    def createBackGround(self,bg_func,period=1,offset=0):
#        #这里本来打算将bg_func作为函数参数的，但调用格式很难统一，所以暂时将bg_func作为关键字，暂定支持全1，cos和sin三种函数。
#        #offset:允许对波形做左右微调，offset为正表示向左移，为负表示向右移。offset的值为移动的点数。
#        period=int(period)
#        offset=int(offset)
#        backgrounds={'flat':flat1,'sin':np.sin,'cos':np.cos}
#        if bg_func in backgrounds.keys():
#            self.__rawData=backgrounds[bg_func](np.arange(offset,self.__length+offset)*period*2*np.pi/self.__length)
#        elif bg_func in ['Sin','Sine','sin','sine']:
##            self.__rawData=np.sin(np.linspace(0,period*2*np.pi,self.__length,endpoint=False))
#            self.__rawData=np.sin(np.arange(offset,self.__length+offset)*period*2*np.pi/self.__length)
#        elif bg_func in ['Cos','Cosin','cos','cosin']:
#            self.__rawData=np.cos(np.arange(offset,self.__length+offset)*period*2*np.pi/self.__length)
            
#    def createWindow(self,segments,start=0):
#        w_length=int(start)
#        #如果createWindow方法已经被调用过，说明已经存在Window了，重新调用则需要将原有的window清零。
#        if self.__hasWindow:
#            self.__Window*=0
#        else:
#            #首次调用，将haswindow置为真。
#            self.__hasWindow=True
#                            
#        for i in range(len(segments)):
#            #segments是一个元组，格式为(高度，长度，边沿，边沿长度)。
#            #generate the edge:
#            if segments[i][2] in ['lin','Lin','L','l', 'linear','Linear']:
#                self.__Window[w_length:w_length+segments[i][3]]=\
#                (segments[i][0]-self.__Window[w_length])*np.arange(1,segments[i][3]+1)
#            elif segments[i][2] in ['g','G','Gauss', 'gauss']:
#                self.__Window[w_length:w_length+segments[i][3]]=\
#                (segments[i][0]-self.__Window[w_length])*gaussian_half(segments[i][3],max(np.floor(segments[i][3]/2),1))+\
#                self.__Window[w_length]
#            #generate the platform:
#            if segments[i][1]>segments[i][3]:
#                self.__Window[w_length+segments[i][3]:w_length+segments[i][1]+1]=segments[i][0]
#            w_length+=segments[i][1]
#                        
#        if w_length > self.__length:
#            print ('window length out of range! Generated window may be incorrect!')
#            return
    
#    def createWindow(self,win_func,length,offset=0,**kwds):
#        w_length=int(offset)
#        length=int(length)
#        windows1={'rectangle':np.ones,'bartlett':np.bartlett,'blackman':np.blackman,'hamming':np.hamming,'hanning':np.hanning}
#        windows2={'gaussian':gaussian,'kaiser':np.kaiser}
#        edges={'linear':linear_edge,'gaussian':gaussian_half}
##        print('kwds:{}'.format(kwds.keys()))
#        #如果长度与起点相加大于总长度，则报错，并将length截断到可以的最大长度。
#        if w_length+length > self.__length:
#            print('the length is out of range!')
#            length=self.__length-w_length
#        #如果createWindow方法已经被调用过，说明已经存在Window了，重新调用则需要将原有的window清零。
#        if self.__hasWindow:
#            self.__Window*=0
#        else:
#            #首次调用，将haswindow置为真。
#            self.__hasWindow=True
#        if win_func == 'userdefine':
#            segments=kwds['segments']
#            for i in range(len(segments)):
#            #segments是一个元组，格式为(高度，长度，边沿函数，边沿长度)。
#            #generate the edge:
#                self.__Window[w_length:w_length+segments[i][3]]=\
#                    (segments[i][0]-self.__Window[w_length])*edges[segments[i][2]](segments[i][3],max(np.floor(segments[i][3]/3),1))+\
#                    self.__Window[w_length]
##                if segments[i][2] in ['lin','Lin','L','l', 'linear','Linear']:
##                    self.__Window[w_length:w_length+segments[i][3]]=\
##                    (segments[i][0]-self.__Window[w_length])*np.arange(1,segments[i][3]+1)
##                elif segments[i][2] in ['g','G','Gauss', 'gauss']:
##                    self.__Window[w_length:w_length+segments[i][3]]=\
##                    (segments[i][0]-self.__Window[w_length])*gaussian_half(segments[i][3],max(np.floor(segments[i][3]/2),1))+\
##                    self.__Window[w_length]
#            #generate the platform:
#                if segments[i][1]>=segments[i][3]:
#                    self.__Window[w_length+segments[i][3]:w_length+segments[i][1]+1]=segments[i][0]
#                w_length+=segments[i][1]    
#        if win_func in windows1.keys():
#            self.__Window[w_length:w_length+length]=windows1[win_func](length)
#        elif win_func in windows2.keys():
#            self.__Window[w_length:w_length+length]=windows2[win_func](length,kwds['beta'])
                        
    def createMarker1(self,segments):
        '''Marker的点数与waveform相等，但值只能是0或1.'''
        #因为没有中间值，marker的segments格式只包含（高度，长度），边沿信息将被忽略。
        self.marker1=np.zeros(self.length).astype('uint16')
        for seg in segments:
            self.marker1[seg[0]:seg[1]]=1
    def createMarker2(self,segments):
        '''Marker的点数与waveform相等，但值只能是0或1.'''
        #因为没有中间值，marker的segments格式只包含（高度，长度），边沿信息将被忽略。
        self.marker2=np.zeros(self.length).astype('uint16')
        for seg in segments:
            self.marker2[seg[0]:seg[1]]=1
                   
#    def createWaveForm(self):
#        if self.__hasWindow:
#            self.__rawData=self.__rawData*self.__Window
#        else:
#            print('No window function was defined.')
#        #首先将数组归一化。
#        Data_n=self.__rawData/np.abs(self.__rawData).max()
##        self.__WFData=np.floor((2**13-1)*(self.__rawData/np.abs(self.__rawData).max())+2**13)+self.__Marker1*2**14+self.__Marker2*2**15
#        self.__WFData=np.floor((Data_n+1)*2**(self.__DIGITAL_DEPTH-1)-Data_n)+\
#                                self.__Marker1*2**self.__DIGITAL_DEPTH+\
#                                self.__Marker2*2**(self.__DIGITAL_DEPTH+1)
#        self.__WFData=self.__WFData.astype('uint16')
        
    
    