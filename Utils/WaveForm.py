# -*- coding: utf-8 -*-
"""
Created on Tue May 17 16:21:11 2016

@author: Xmon-SC05
"""
import numpy as np

#用于生成高斯型边沿。
def gaussian_half(length,std):
    x=np.arange(0,length)
    return np.exp(-(x-length)**2/std**2)
def linear_edge(length,*args):
    return np.linspace(0,1,length,endpoint=False)
#用于生成高斯型窗函数    
def gaussian(length,std):
    x=np.arange(0,length)
    return np.exp(-(x-length/2)**2/std**2)
#平直函数，等价于ones，但参数可以和sin,cos等函数相同
def flat1(x):
    return np.ones(x.shape)
            
class WaveForm:
    def __init__(self,name,length=1000,digit_depth=14):
        self.__name=name
        self.__length=int(length)
        self.__DIGITAL_DEPTH = int(digit_depth)
        self.__Window=np.zeros(length)
        self.__rawData=np.zeros(length)
        self.__WFData=np.zeros(length).astype('uint16')
        self.__Marker1=np.zeros(length).astype('int')
        self.__Marker2=np.zeros(length).astype('int')
        self.__hasWindow = False
        
    def name(self):
        return self.__name
    
    def length(self):
        return self.__length
        
    def get_waveform(self,format=True):
        if format:
            return self.__WFData
        else:
            return self.__rawData
            
    def window(self):
        return self.__Window
        
    def createBackGround(self,bg_func,period=1,offset=0):
        #这里本来打算将bg_func作为函数参数的，但调用格式很难统一，所以暂时将bg_func作为关键字，暂定支持全1，cos和sin三种函数。
        #offset:允许对波形做左右微调，offset为正表示向左移，为负表示向右移。offset的值为移动的点数。
        period=int(period)
        offset=int(offset)
        backgrounds={'flat':flat1,'sin':np.sin,'cos':np.cos}
        if bg_func in backgrounds.keys():
            self.__rawData=backgrounds[bg_func](np.arange(offset,self.__length+offset)*period*2*np.pi/self.__length)
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
    
    def createWindow(self,win_func,length,offset=0,**kwds):
        w_length=int(offset)
        length=int(length)
        windows1={'rectangle':np.ones,'bartlett':np.bartlett,'blackman':np.blackman,'hamming':np.hamming,'hanning':np.hanning}
        windows2={'gaussian':gaussian,'kaiser':np.kaiser}
        edges={'linear':linear_edge,'gaussian':gaussian_half}
#        print('kwds:{}'.format(kwds.keys()))
        #如果长度与起点相加大于总长度，则报错，并将length截断到可以的最大长度。
        if w_length+length > self.__length:
            print('the length is out of range!')
            length=self.__length-w_length
        #如果createWindow方法已经被调用过，说明已经存在Window了，重新调用则需要将原有的window清零。
        if self.__hasWindow:
            self.__Window*=0
        else:
            #首次调用，将haswindow置为真。
            self.__hasWindow=True
        if win_func == 'userdefine':
            segments=kwds['segments']
            for i in range(len(segments)):
            #segments是一个元组，格式为(高度，长度，边沿函数，边沿长度)。
            #generate the edge:
                self.__Window[w_length:w_length+segments[i][3]]=\
                    (segments[i][0]-self.__Window[w_length])*edges[segments[i][2]](segments[i][3],max(np.floor(segments[i][3]/3),1))+\
                    self.__Window[w_length]
#                if segments[i][2] in ['lin','Lin','L','l', 'linear','Linear']:
#                    self.__Window[w_length:w_length+segments[i][3]]=\
#                    (segments[i][0]-self.__Window[w_length])*np.arange(1,segments[i][3]+1)
#                elif segments[i][2] in ['g','G','Gauss', 'gauss']:
#                    self.__Window[w_length:w_length+segments[i][3]]=\
#                    (segments[i][0]-self.__Window[w_length])*gaussian_half(segments[i][3],max(np.floor(segments[i][3]/2),1))+\
#                    self.__Window[w_length]
            #generate the platform:
                if segments[i][1]>=segments[i][3]:
                    self.__Window[w_length+segments[i][3]:w_length+segments[i][1]+1]=segments[i][0]
                w_length+=segments[i][1]    
        if win_func in windows1.keys():
            self.__Window[w_length:w_length+length]=windows1[win_func](length)
        elif win_func in windows2.keys():
            self.__Window[w_length:w_length+length]=windows2[win_func](length,kwds['beta'])
                        
    def createMarker(self,segments,M=1,offset=0):
        '''Marker的点数与waveform相等，但值只能是0或1.'''
        #因为没有中间值，marker的segments格式只包含（高度，长度），边沿信息将被忽略。
        w_length=int(offset)
        M=int(M)
        Marker=np.zeros(self.__length).astype('int')
        for i in range(len(segments)):
            Marker[w_length:w_length+segments[i][1]]=segments[i][0]
            w_length+=segments[i][1]
        if M == 1:
            self.__Marker1=Marker
        elif M == 2:
            self.__Marker2=Marker
            
        if w_length > self.__length:
            print ('marker length out of range! Generated window may be incorrect!')
            return
                
    def createWaveForm(self):
        if self.__hasWindow:
            self.__rawData=self.__rawData*self.__Window
        else:
            print('No window function was defined.')
        #首先将数组归一化。
        Data_n=self.__rawData/np.abs(self.__rawData).max()
#        self.__WFData=np.floor((2**13-1)*(self.__rawData/np.abs(self.__rawData).max())+2**13)+self.__Marker1*2**14+self.__Marker2*2**15
        self.__WFData=np.floor((Data_n+1)*2**(self.__DIGITAL_DEPTH-1)-Data_n)+\
                                self.__Marker1*2**self.__DIGITAL_DEPTH+\
                                self.__Marker2*2**(self.__DIGITAL_DEPTH+1)
        self.__WFData=self.__WFData.astype('uint16')
        
    
    