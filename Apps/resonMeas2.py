# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 01:23:04 2016

@author: Xmon-SC05
"""
from PyQCLab.Apps.Resonator import *
from PyQCLab.Utils.Qextractor import *
import numpy as np
#from pylab import *
import time
import skrf as rf
#%%
#给定需要测量的腔模大致的中心频率，精确到M即可。
f0=6.2e9
span=1e9
N=12000
IF=5000
power0=0
avg_times=1
fstart,fstop=f0-span/2,f0+span/2
#%%
R0=Resonator(f0)
R0.searchMode((fstart,fstop,IF,N,power0,avg_times),5)
freq=R0.freq
magS=rf.mag_2_db(abs(R0.sparam))
figure(),plot(freq,magS,freq[R0.mode],magS[R0.mode],'*')
#%%
figure(),plot(magS)
#%%
#如果有遗漏的腔模，则手动补上。
missed_modes=[]
for items in missed_modes:
    R0.mode.append(items)
#如果有找错了的腔模，则剔除。
wrongModes_idx=[]
for i in wrongModes_idx:
    R0.mode.pop(i)
    
R0.mode.sort()
#获取腔模对应的中心频率。
modes=freq[array(R0.mode)]
print(modes)
#modes=array([5.278,5.412,5.541,6.013,6.133,6.855,6.927])*1e9
#%%
#-----------设定找峰参数时用的扫描参数：-----------------------------------------
span0=10e6
IF0=5000
N0=5001
power0=0
avg_times=1
#-----------设定精细测量时用的扫描参数：-----------------------------------------
IF_fine=5000
powers=linspace(0,-30,7)
#-----------其他外部参数：------------------------------------------------------
attenuation=-20     #外接衰减器衰减值，必须在测量前检查并准确输入！！！
path='.\\Data\\'
filename_prefix='GH_6_20170830_dip'
filename_postfix='_HighPower'
#%%
#-----------创建所有腔模的实例：------------------------------------------------
R=list()
#P=list()
for i in range(modes.size):
    R.append(Resonator(modes[i],attenuation=attenuation))
#    P.append([1e5,1e5,1,mode[i]])
#q=Qextractor()
#R=Resonator(modes[0])
#%%
#-----------对每个腔模搜索参数：------------------------------------------------
for i in range(modes.size):   
    R[i].f0=modes[i]
    fstart,fstop=R[i].f0-span0/2,R[i].f0+span0/2
    R[i].searchMode((fstart,fstop,IF0,N0,power0,avg_times),5)
#%%
#-----------画出扫描结果并手动确定细扫参数。-----------------------------------------   
for i in range(modes.size):
    figure(),plot(R[i].freq,R[i].magS_db)
    grid()
    title('mode {}'.format(i))
#%%
fine_params=[(60e3,3e6),\
             (200e3,5e6),\
             (400e3,5e6),\
             (450e3,5e6),\
             (500e3,5e6),\
             (1e6,6e6)\
            ]
for i in range(modes.size):
    R[i].setScan(fine_params[i])
#%%
#-----------对搜索成功的腔模进行精细测量，在改变功率测量之前再提供一次检查机会：----
IF_fine=5000
N_fine=201

fineScan_params=(IF_fine,N_fine,power0,1)         
for i in range(modes.size):
    
    tic=time.time()
    if R[i].fineScan(fineScan_params,[20,80]):
        figure()
        plot(R[i].freq,rf.mag_2_db(abs(R[i].sparam)),'o-')
        title('mode {}'.format(i))
        figure(),plot(R[i].S_n.real,R[i].S_n.imag,'o',R[i].S_fit.real,R[i].S_fit.imag,'r-')
        title('mode {} smith'.format(i))
    else:
        figure()
        plot(R[i].freq,rf.mag_2_db(abs(R[i].sparam)),'o-')
        title('mode {}'.format(i))
    print('{} sec escaped.'.format(time.time()-tic))
#%%
for i in range(modes.size):
    m=getResonmode(R[i].magS_db)
    if len(m)==1:
        print('One mode was found at {}.'.format(R[i].freq[m]))
        R[i].f0=R[i].freq[m[0]]
#%%
R[0].P0=[5e5,5e4,0,R[0].f0]
R[1].P0=[1e5,1e4,0,R[1].f0]
R[2].P0=[3e4,2e4,0,R[2].f0]
R[3].P0=[1e5,4e3,0,R[3].f0]
R[4].P0=[1e5,3e3,0,R[4].f0]
R[5].P0=[1e4,3e3,0,R[5].f0]


for i in range(modes.size):
    R[i].update(R[i].P0,'UCSB')
    figure()
    subplot(211),plot(R[i].invS_n.real,R[i].invS_n.imag,'o',R[i].invS_fit.real,R[i].invS_fit.imag,'r-')
    subplot(212),plot(R[i].freq,rf.mag_2_db(np.abs(R[i].S_n)),'o',R[i].freq,rf.mag_2_db(np.abs(R[i].S_fit)),'r-')
    title('mode {} smith'.format(i))
#%% 
for i in range(modes.size):
    R[i].P0=R[i].P
#%%
#-----------以上的检查步骤全部通过之后，可以开始变功率扫描了：---------------------
class resonData():
    def __init__(self):
        self.data=list()
    
    def append(self,d):
        self.data.append(d)
    def concatenate(self):
        if len(self.data):
            self.powers=np.zeros(len(self.data))
            self.freq=np.zeros((len(self.data),len(self.data[0][1])))
            self.Sdata=np.zeros((len(self.data),len(self.data[0][2]))).astype('complex')
            self.Qdata=np.zeros((len(self.data),len(self.data[0][3])))
            
            for i in range(len(self.data)):
                self.powers[i]=self.data[i][0]
                self.freq[i,:]=self.data[i][1]
                self.Sdata[i,:]=self.data[i][2]
                self.Qdata[i,:]=self.data[i][3]
    def saveData(self,filename):
        np.savez(filename,powers=self.powers,freq=self.freq,Sdata=self.Sdata,Qdata=self.Qdata)
#%%  
powers=linspace(0,-60,13) 
IF_fine=5000
avg_times=1
filename_postfix='_AllPower'    
allData=list()        

for i in range(modes.size):
    
    allData.append(resonData())
    avg_times=1
    for k in range(powers.size):
        IF=IF_fine/2**k
        if IF < 10:
            avg_times=2*np.floor(10/IF)
            IF=10
        print('IF={}, avg_times={}.'.format(IF,avg_times))
        tic=time.time()
        R[i].fineScan((IF,N_fine,powers[k],avg_times))
        toc=time.time()
        print('{} sec escaped.'.format(toc-tic))
        allData[i].append((R[i].power+R[i].attenuation,R[i].freq,R[i].sparam,np.array([R[i].Qi,R[i].Qc,R[i].f0])))
    allData[i].concatenate()
    filename=path+filename_prefix+str(i)+filename_postfix
    allData[i].saveData(filename)
    print('Dip{} finished.'.format(i+1))
#    filename=path+filename_prefix+str(i)+filename_postfix+'-2'
#    R[i].saveData(filename)
#%%
for i in range(modes.size):
    filename=path+filename_prefix+str(i)+filename_postfix
    np.savez(filename,powers=allData[i].power,freq=allData[i].freq,SData=allData[i].SData,QData=allData[i].QData)    
