# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 01:23:04 2016

@author: Xmon-SC05
"""
from PyQCLab.Apps.Resonator_znb20 import *
from PyQCLab.Utils.Qextractor import *
import numpy as np
from pylab import *
import time
import skrf as rf
#%%
#给定需要测量的腔模大致的中心频率，精确到M即可。
def multiModeSearch(fstart=4e9,fstop=8e9,pwr=0,IF=1001,N=20001,avg=1):
    fcenter=(fstart+fstop)/2
    fspan=fstop-fstart
    R0=Resonator(fcenter)
    R0.searchMode(pwr,IF0=IF,points=N,span0=fspan,search_factor=10)
    figure(),plot(R0.freq,R0.magS_db,R0.freq[R0.mode],R0.magS_db[R0.mode],'*')
    print('Modes were found at {}'.format(R0.mode))
    return R0.mode

#def scanPower(R,powers,IF0=1000,N0=addAttenuator=True): 
#%%  
fcenter=7.0e9
fspan=300e6
pwr=-10
IF=1000
N=10001
avg=1
R0=Resonator(fcenter)

time.sleep(1)
R0.average=avg
R0.searchMode(pwr,IF0=IF,points=N,span0=fspan,search_factor=10)
#freq=R0.freq
#magS=rf.mag_2_db(abs(R0.sparam))
figure(),plot(R0.freq,R0.magS_db,R0.freq[R0.mode],R0.magS_db[R0.mode],'*')
modes=list(R0.freq[R0.mode])
print(modes)
#%%
#mask=[1,2,3,4,5,6,7,8]
#modes=freq[array(R0.mode)[mask]]
#modes=[5.9768e9,6.1135e9,6.1219e9,6.3118e9,6.3312e9,6.4304e9,6.5413e9,6.6508e9,6.7486e9]
addedModes=[7.004e9,7.033e9,7.0598e9]
for mode in addedModes:
    modes.append(mode)
modes.sort()
#modes=modes[:-1]
print(modes)

#modes=array([5.278,5.412,5.541,6.013,6.133,6.855,6.927])*1e9
#%%
#-----------设定找峰参数时用的扫描参数：-----------------------------------------
power0=-10
IF0=5000
N0=1001
span0=0.5e6
sf0=10   #找峰时的初始探索深度参数。
Max_searchTimes=3   #允许的最大探索失败次数。
#-----------设定精细测量时用的扫描参数：-----------------------------------------
IF_fine=5000
powers=np.linspace(0,-30,11)
#-----------其他外部参数：------------------------------------------------------
attenuation=-0     #外接衰减器衰减值，必须在测量前检查并准确输入！！！
path='C:\\Users\\SC05\\Documents\\PyQCLab\\Data\\20180203\\'
#filename_prefix='YZG_WetEtch_Openloop_20161018_dip'
filename_prefix='Jinkou_20db_dip'
filename_postfix='_HighPower'
#%%
#-----------创建所有腔模的实例：------------------------------------------------
R=list()
#P=list()
for i in range(len(modes)):
    R.append(Resonator(modes[i]))
#    P.append([1e5,1e5,1,mode[i]])
#q=Qextractor()
#R=Resonator(modes[0])
#%%
#-----------对每个腔模搜索参数：------------------------------------------------
#power0=-15
for i in range(len(modes)):    
#    count=1
#    sf=sf0
#    span=span0
    R[i].searchMode(power0,IF0=500,points=201,span0=1e6,search_factor=10)
    if not R[i].search_succeed:
    #如果第一次探索失败，则提高探索深度试图再进行搜索。
#        while not R[i].search_succeed and count < Max_searchTimes:
#            sf*=2
#            span*=2
        R[i].searchMode(power0,sweep=False)
#            count+=1
#%%
for i in range(len(modes)):
    R[i].search_succeed=True
    figure()
    plot(R[i].freq,R[i].magS_db,'o-')
    
#%%
brd=[200e3,100e3,30e3,400e3,200e3,100e3]
whl=[2e6,1e6,1.2e6,3e6,3e6,3e6]
for i in range(len(modes)):
    R[i].f0=R[i].freq[R[i].magS_db.argmin()]
    R[i].setScan(R[i].f0,0,brd[i],whl[i])
    R[i].fineScan2(0,IF=1000,N=401)
    
    figure(),plot(R[i].freq,R[i].magS_db,'o-')
#%%
path='.\\Data\\'
filename='SIRwQubit3_Alldips--40dBm'
postfix='.npz'
data=load(path+filename+postfix)
#freq=data['freq']
#Sdata=data['SData']
Qdata=data['QData']
for i in range(len(modes)):
    R[i].Qi,R[i].Qc,R[i].f0=Qdata[i,:]
    R[i].optimizeScan()
#-----------对搜索失败的腔模做补救搜索：-----------------------------------------
#for i in range(modes.size):
#    count=1
#    while not R[i].success and count < Max_searchTimes:
#            sf*=2
#            R[i].searchMode(power0,search_factor=sf,sweep=False)
#            count+=1
#    if not R[i].success:
#         print('We can not find the parameters of this {} mode, please check and input manually.'.format(i))
#         print('Measurement of this mode will be skipped this time, please measure it after check.')
#%%
#-----------对搜索成功的腔模进行精细测量，在改变功率测量之前再提供一次检查机会：---- 
#path='.\\Data\\'
#filename_prefix='JYR_SIR2_1#_Alldips_'
IF_fine=100
pwr=-30
freq=list()
SData=list()
QData=list()
avgs=np.ones(len(modes))*30
for i in range(len(modes)-4):
#    R[i].attenuation=attenuation
#    R[i].average=200
    if R[i].fineScan(pwr,IF_fine,201,avg=avgs[i]):
        figure(),plot(R[i].freq,rf.mag_2_db(abs(R[i].sparam)),'o-')
#        figure(),plot(R[i].S_n.real,R[i].S_n.imag,'o',R[i].S_fit.real,R[i].S_fit.imag,'r-')
        figure(),plot(R[i].invS_n.real,R[i].invS_n.imag,'o',R[i].invS_fit.real,R[i].invS_fit.imag,'r-')
    else:
        print('faild to get a fine result.')
    freq.append(R[i].freq)
    SData.append(R[i].sparam)
    QData.append([R[i].Qi,R[i].Qc,R[i].f0])    
    print('Dip{} finished at {}'.format(i+1,time.ctime()))
d=resonData(pwr,freq,SData,QData)
filename=path+filename_prefix+str(pwr)
d.saveData(filename)
#    if R[i].search_succeed:
#        tic=time.time()
##        R[i].optimizeScan()        
#        R[i].fineScan(power0,IF_fine)
#        print('{} sec escaped.'.format(time.time()-tic))
#        figure()
##        freq=R[i].SData[0][:,0]
##        magS=R[i].SData[0][:,1]
##        angS=R[i].SData[0][:,2]
##        s21=dbphase2complex(magS,angS,deg=True)
##        q.freq,q.sparam=freq,s21
##        q.update(R[i].P)
##        if q.succeed:
##            print('Qi={}, Qc={}, f0={} Hz.'.format(q.Qi,q.Qc,q.f0))
##        else:
##            print('fitting failed for mode {} GHz.'.format(R[i].f0))
##        R[i].span_3db=q.f0/q.Qi/2
##        R[i].span_broaden=q.f0/q.Qi/q.Qc*(q.Qi+q.Qc)/2
##        R[i].optimizeScan()
##        R[i].fineScan(power0,IF_fine)
##        freq=R[i].SData[0][:,0]
##        magS=R[i].SData[0][:,1]
##        angS=R[i].SData[0][:,2]
##        s21=dbphase2complex(magS,angS,deg=True)
##        q.freq,q.sparam=freq,s21
##        q.update([1e5,1e5,1,modes[i]])
##        idx_3db=[abs(freq-q.f0+R[i].span_3db).argmin(),abs(freq-q.f0-R[i].span_3db).argmin()]
##        idx_broaden=[abs(freq-q.f0+R[i].span_broaden).argmin(),abs(freq-q.f0-R[i].span_broaden).argmin()]
##        plot(freq,magS,'o-',freq[idx_3db],magS[idx_3db],'D',freq[idx_broaden],magS[idx_broaden],'D')
#        plot(R[i].freq,rf.mag_2_db(abs(R[i].sparam)),'o-')
#        figure(),plot(R[i].S_n.real,R[i].S_n.imag,'o',R[i].S_fit.real,R[i].S_fit.imag,'r-')
#        figure(),plot(q.invS_n.real,q.invS_n.imag,'o',q.invS_fit.real,q.invS_fit.imag,'r-')
#        R[i].clearData()
#%%
for i in range(len(modes)):
#    R[i].optimizeScan()
    R[i].fineScan2(-15,IF=1000,N=501)
    
    figure()
    subplot(211),plot(R[i].freq,R[i].magS_db,'*')
    subplot(212),plot(R[i].invS_n.real,R[i].invS_n.imag,'o',R[i].invS_fit.real,R[i].invS_fit.imag,'r')

#%%
for i in range(3,6):
    R[i].setScan(R[i].f0,R[i].span_3db,R[i].span_broaden/5,R[i].span_whole)
#%%   
#-----------以上的检查步骤全部通过之后，可以开始变功率扫描了：---------------------
IF_fine0=1000
powers=linspace(-10,-50,9)
#-----------其他外部参数：------------------------------------------------------
attenuation=-20    #外接衰减器衰减值，必须在测量前检查并准确输入！！！
#path='.\\Data\\'
#filename_prefix='YZG_WetEtch_Openloop_20161018_dip'
#filename_prefix='SIRwQubit3_dip'
filename_postfix='_HighPower'
#filename_postfix='_LowPower'
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
    avg=1
    R[i].attenuation=attenuation
    R[i].average=avg
    IF_fine=IF_fine0
#    R[i].instrhandle.write('SENSe:AVERage:COUNt 1')
    for k in range(powers.size):
        IF_fine=IF_fine/2**mod(k,2)
        if IF_fine < 10:
#            IF_fine=100
            avg*=2    
        tic=time.time()
        R[i].f0=R[i].freq[R[i].magS_db.argmin()]
#        R[i].setScan(R[i].f0,0,brd[i],whl[i])
        R[i].fineScan2(powers[k],IF_fine,201,weight=[20,80],avg=avg)
        print('{} sec escaped.'.format(time.time()-tic))
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
    
