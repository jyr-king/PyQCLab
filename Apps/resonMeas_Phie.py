# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 01:23:04 2016

@author: Xmon-SC05
"""
from PyQCLab.Apps.Resonator import *
from PyQCLab.Utils.Qextractor import *
from PyQCLab.Instrument.DCSources import yokogawa7651
from pylab import *
import time
import skrf as rf
#%%
class resonData():
    def __init__(self,powers,freq,SData,QData):
        self.powers=array(powers)
        self.freq=array(freq)
        self.SData=array(SData)
        self.QData=array(QData)
        
    def saveData(self,filename):
        self.filename=filename
        savez(filename,power=self.powers,freq=self.freq,SData=self.SData,QData=self.QData)
    def loadData(self):
        data=load(self.filename+'.npz')
        self.powers=data['power']
        self.freq=data['freq']
        self.SData=data['SData']
        self.QData=data['QData']
#%%
#mask=[1,2,3,4,5,6,7,8]
#modes=freq[array(R0.mode)[mask]]
modes=[5.3026e9,5.4271e9,5.5531e9,6.0409e9,6.1512e9,6.3264e9,6.865e9,6.9378e9]
#addedModes=[6.0409e9]
#for mode in addedModes:
#    modes.append(mode)
#modes.sort()
#
#print(modes)
#modes=array([5.278,5.412,5.541,6.013,6.133,6.855,6.927])*1e9
#%%
#-----------设定找峰参数时用的扫描参数：-----------------------------------------
power0=0
IF0=5000
N0=1001
span0=1e6
sf0=10   #找峰时的初始探索深度参数。
Max_searchTimes=3   #允许的最大探索失败次数。
#-----------设定精细测量时用的扫描参数：-----------------------------------------
IF_fine=5000
powers=linspace(3,-27,11)
#-----------其他外部参数：------------------------------------------------------
attenuation=-20     #外接衰减器衰减值，必须在测量前检查并准确输入！！！
path='..\\Data\\'
#filename_prefix='YZG_WetEtch_Openloop_20161018_dip'
filename_prefix='test'
filename_postfix='_LowPower'
#%%
#-----------创建所有腔模的实例：------------------------------------------------
#source1=AG33120A('AG33120A_0')
source2=yokogawa7651('YOKOGAWA7651')
source2.instrhandle.write('F5;E')
source2.instrhandle.write('SA0.001E;E')
source2.set_output()
#output=['DC',1,0.05,0]
#source1.apply(output)
allData=list()
R=list()
#P=list()
for i in range(len(modes)):
    R.append(Resonator(modes[i]))
#    P.append([1e5,1e5,1,mode[i]])
#q=Qextractor()
#R=Resonator(modes[0])
#%%
    
#-----------对每个腔模搜索参数：------------------------------------------------
power0=-12
IF0=1000
N0=1001
IF_fine=100
attenuation=-20
avg=1
path='..\\Data\\'
filename_prefix='YZG_WetEtch_Openloop_20161018_dcI'

dcI=concatenate((arange(64.5,-100,-0.5)/1000,arange(-100,0,0.5)/1000))

# 
allData=list()       
freq=list()
SData=list()
QData=list()

source2.instrhandle.write('F5;E')
source2.instrhandle.write('SA0.001E;E')
source2.set_output()

for k in range(dcI.size):
#    output=['DC',1,0.05,dcV[k]]
#    source1.apply(output)
    source2.instrhandle.write('SA{}E;E'.format(dcI[k]))
    for i in range(len(modes)):    
    #    count=1
    #    sf=sf0
    #    span=span0
#        R[i].average=avg
        R[i].attenuation=attenuation
        R[i].search_succeed=False
        tic=time.time()
        R[i].searchMode(power0,IF0=IF0,points=N0,span0=2e6,search_factor=10)
        if not R[i].search_succeed:
        #如果第一次探索失败，则提高探索深度试图再进行搜索。
    #    while not R[i].search_succeed and count < Max_searchTimes:
    #        sf*=2
    #        span*=2
            R[i].searchMode(power0,sweep=False)
#        R[i].average=avg
#        R[i].fineScan(power0,IF_fine)
        print('{} sec escaped.'.format(time.time()-tic))
        freq.append(R[i].freq)
        SData.append(R[i].sparam)
        QData.append([R[i].Qi,R[i].Qc,R[i].f0])
    d=resonData([power0,dcI[k]],freq,SData,QData)
    if k==0:
        filename=path+filename_prefix+str(dcI[k])+'-'+str(power0+attenuation)+'dBm_Up-2'
    elif dcI[k]-dcI[k-1]>0:
        filename=path+filename_prefix+str(dcI[k])+'-'+str(power0+attenuation)+'dBm_Up-2'
    else:
        filename=path+filename_prefix+str(dcI[k])+'-'+str(power0+attenuation)+'dBm_Dwn-2'
    d.saveData(filename)
    allData.append(d)
    freq=list()
    SData=list()
    QData=list()
    print('dcI {} mA finished.'.format(dcI[k]*1000))
#source1.apply(['DC',1,0.05,0])
#source2.instrhandle.write('SA.0001E;E')
#source2.set_output(False)

#        count+=1
#%% 
power0=-22
IF0=100
N0=2001
IF_fine=100
attenuation=-53
avg=2
path='..\\Data\\'
filename_prefix='YZG_WetEtch_Openloop_20161031_lowPower'

dcI=0.02
wait=10
N=1
# 
allData=list()       
freq=list()
SData=list()
QData=list()

#source2.instrhandle.write('F5;E')
#source2.instrhandle.write('SA{}E;E'.format(dcI))
#source2.set_output()

for k in range(N):
#    output=['DC',1,0.05,dcV[k]]
#    source1.apply(output)
#    source2.instrhandle.write('SA{}E;E'.format(dcI[k]))
    for i in range(4,5):    
    #    count=1
    #    sf=sf0
    #    span=span0
#        R[i].average=avg
        R[i].attenuation=attenuation
#        R[i].search_succeed=False
        tic=time.time()
        R[i].searchMode(power0,IF0=IF0,points=N0,span0=2e6,search_factor=10)
        if not R[i].search_succeed:
        #如果第一次探索失败，则提高探索深度试图再进行搜索。
    #    while not R[i].search_succeed and count < Max_searchTimes:
    #        sf*=2
    #        span*=2
            R[i].searchMode(power0,sweep=False)
#        R[i].average=avg
        R[i].fineScan(power0,IF_fine)
        print('{} sec escaped.'.format(time.time()-tic))
        freq.append(R[i].freq)
        SData.append(R[i].sparam)
        QData.append([R[i].Qi,R[i].Qc,R[i].f0])
#    time.sleep(wait)
    d=resonData([power0,N],freq,SData,QData)
#    if k < dcI.size/2:
#        filename=path+filename_prefix+str(dcI[k])+'-'+str(power0+attenuation)+'dBm_Up'
#    else:
#        filename=path+filename_prefix+str(dcI[k])+'-'+str(power0+attenuation)+'dBm_Dwn'
    filename=path+filename_prefix+'-'+str(power0+attenuation)+'dBm-3'
    d.saveData(filename)
    allData.append(d)
    freq=list()
    SData=list()
    QData=list()
    print('The {}nd scan finished.'.format(k))
#source1.apply(['DC',1,0.05,0])
#source2.instrhandle.write('SA.0001E;E')
#source2.set_output(False)  
#-----------以上的检查步骤全部通过之后，可以开始变功率扫描了：---------------------
#IF_fine=100
#powers=linspace(3,-27,11)
##-----------其他外部参数：------------------------------------------------------
#attenuation=-53    #外接衰减器衰减值，必须在测量前检查并准确输入！！！
#path='..\\Data\\'
##filename_prefix='YZG_WetEtch_Openloop_20161018_dip'
#filename_prefix='test_dip'
#filename_postfix='_LowPower'
#
#
#        
#allData=list()        
#freq=list()
#SData=list()
#QData=list()
#
#for i in range(4,len(modes)):
#    R[i].attenuation=attenuation
#    R[i].average=2
##    R[i].instrhandle.write('SENSe:AVERage:COUNt 1')
#    for k in range(powers.size):
#        tic=time.time()
#        R[i].fineScan(powers[k],IF_fine)
#        print('{} sec escaped.'.format(time.time()-tic))
#        freq.append(R[i].freq)
#        SData.append(R[i].sparam)
#        QData.append([R[i].Qi,R[i].Qc,R[i].f0])
#    d=resonData(powers+R[i].attenuation,freq,SData,QData)
#    allData.append(d)
#    freq=list()
#    SData=list()
#    QData=list()
#    print('Dip{} finished.'.format(i+1))
#    filename=path+filename_prefix+str(i)+filename_postfix
#    d.saveData(filename)
#    R[i].saveData(filename)
    
