# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:15:06 2018

@author: SC05
"""
from PyQCLab.Apps.Resonator_znb20 import *
from PyQCLab.Utils.Qextractor import *
import numpy as np
from pylab import *
import time
import matplotlib.pyplot as plt
import skrf as rf
#%%
fcenter=6e9
fspan=6e9
pwr=-0
IF=1000
N=10001
avg=1
R0=Resonator(fcenter)

time.sleep(1)
R0.average=avg
R0.searchMode(pwr,IF0=IF,points=N,span0=fspan,search_factor=10)
#R[i].fineScan2(powers[k],IF_fine,201,weight=[20,80],avg=avg)
#freq=R0.freq
#magS=rf.mag_2_db(abs(R0.sparam))
modes=list(R0.freq[R0.mode])
print(modes)
#figure(0),plt.plot(R0.freq,R0.magS_db,R0.freq[R0.mode],R0.magS_db[R0.mode],'*')
figure(0),plt.plot(R0.freq,R0.magS_db)
#%%
name='HKQOutsysports50ohaveCuboxhavetop'
rang1=str(int(fcenter-fspan/2)/1e9)+'-'+str(int(fcenter+fspan/2)/1e9)+'G'
plt.title('Room_T,'+name+rang1+str(pwr)+'db')
savefig('C:\\Users\\SC05\\Desktop\\20180227\\Room_T'+name+rang1+str(pwr)+'.png')
#np.savetxt('C:\\Users\\SC05\\Desktop\\20180227\\Room_T'+name,R0.freq)
np.savez('C:\\Users\\SC05\\Desktop\\20180227\\'+name+rang1+str(pwr),R0.freq,R0.magS_db)
#%%
diptitle='deng5bit'
plt.title(str(pwr)+':dbm_atten:-33db'+diptitle)
plt.xlabel(str(around(np.array(modes)/1e9,4)))
plt.ylabel('Qi'+str(around(np.array(R0.Qi)/1e4,4))+'w')
savefig('C:\\Users\\SC05\\Documents\\PyQCLab\\Data\\20180227add\\'+diptitle+str(pwr)+'.png')
#%%
addedModes=[6.2178e9]
for mode in addedModes:
    modes.append(mode)
modes.sort()
#modes=modes[:-1]
print(modes)
#%%
power0=-0
IF0=5000
N0=1001
span0=0.5e6
sf0=10   #找峰时的初始探索深度参数。
Max_searchTimes=2   #允许的最大探索失败次数。
#-----------设定精细测量时用的扫描参数：-----------------------------------------
IF_fine=5000
powers=np.linspace(0,-30,11)
#-----------其他外部参数：------------------------------------------------------
attenuation=-23     #外接衰减器衰减值，必须在测量前检查并准确输入！！！
path='C:\\Users\\SC05\\Documents\\PyQCLab\\Data\\20180204add\\'
#filename_prefix='YZG_WetEtch_Openloop_20161018_dip'
filename_prefix='5bit_dip'
filename_postfix='_HighPower'
#%%
R=list()
#P=list()
for i in range(len(modes)):
    R.append(Resonator(modes[i]))
#%%
for i in range(len(modes)):    
#    count=1
#    sf=sf0
#    span=span0
    R[i].searchMode(power0,IF0=500,points=1001,span0=2e6,search_factor=10)
    if not R[i].search_succeed:
    #如果第一次探索失败，则提高探索深度试图再进行搜索。
#        while not R[i].search_succeed and count < Max_searchTimes:
#            sf*=2
#            span*=2
        R[i].searchMode(power0,sweep=False)
#%%
for i in range(len(modes)):
#    R[i].optimizeScan()
    R[i].fineScan2(-0,IF=1000,N=501)
    
    figure()
    subplot(211),plot(R[i].freq,R[i].magS_db,'*')
    subplot(212),plot(R[i].invS_n.real,R[i].invS_n.imag,'o',R[i].invS_fit.real,R[i].invS_fit.imag,'r')
#%%
brd=[3e6,6e6,0.8e6,]
whl=[20e6,30e6,20e6]
for i in range(len(modes)):
    R[i].f0=R[i].freq[R[i].magS_db.argmin()]
    R[i].setScan(R[i].f0,0,brd[i],whl[i])
    R[i].fineScan2(0,IF=1000,N=401)
    
    figure(),plot(R[i].freq,R[i].magS_db,'o-')
#%%
#-----------以上的检查步骤全部通过之后，可以开始变功率扫描了：---------------------
IF_fine0=2000
#powers=linspace(-33,-60,10)
powers=linspace(-0,-57,20)
#-----------其他外部参数：------------------------------------------------------
attenuation=-33    #外接衰减器衰减值，必须在测量前检查并准确输入！！！
#path='.\\Data\\'
#filename_prefix='YZG_WetEtch_Openloop_20161018_dip'
#filename_prefix='SIRwQubit3_dip'
#filename_postfix='_5bitHighPower'
filename_postfix='_5bitPower'


class resonData():
    def __init__(self,powers,freq,SData,QData):
        self.powers=array(powers)
        self.freq=array(freq)
        self.SData=array(SData)
        self.QData=array(QData)
        
    def saveData(self,filename):
        savez(filename,power=self.powers,freq=self.freq,SData=self.SData,QData=self.QData)
        
allData=list()        
freq=list()
SData=list()
QData=list()

for i in range(len(modes)):
#for i in range(len(modes)):
#    i=4
    avg=1
    R[i].attenuation=attenuation
    R[i].average=avg
    IF_fine=IF_fine0
#    R[i].instrhandle.write('SENSe:AVERage:COUNt 1')
    for k in range(powers.size):
#        IF_fine=IF_fine/2**mod(k,2)
        IF_fine=IF_fine0/2**(k//2)
           
        if IF_fine < 20:
            IF_fine=20
            avg*=2   
#            avg=k*10 
#        avg=500
        tic=time.time()
        R[i].f0=R[i].freq[R[i].magS_db.argmin()]
#        R[i].setScan(R[i].f0,0,brd[i],whl[i])
        R[i].fineScan2(powers[k],IF_fine,201,weight=[20,80],avg=avg)
        print('{} sec escaped.'.format(time.time()-tic))
        print('IF',IF_fine)
        freq.append(R[i].freq)
        SData.append(R[i].sparam)
        QData.append([R[i].Qi,R[i].Qc,R[i].f0])
        
    d=resonData(powers+R[i].attenuation,freq,SData,QData)
    allData.append(d)
    freq=list()
    SData=list()
    QData=list()
    print('Dip{} finished.'.format(i+1))
    filename=path+filename_prefix+str(i)+filename_postfix
    d.saveData(filename)
#    R[i].saveData(filename)