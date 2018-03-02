# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 01:23:04 2016

@author: Xmon-SC05
"""
from PyQCLab.Apps.Resonator_znb20 import *
from PyQCLab.Utils.Qextractor import *
from pylab import *
import time
import skrf as rf

#%%  
fcenter=6e9
fspan=1e9
pwr=-20
IF=1000
N=20001
avg=1
R0=Resonator(fcenter)
R0.average=avg
R0.searchMode(pwr,IF0=IF,points=N,span0=fspan,search_factor=10)
#freq=R0.freq
#magS=rf.mag_2_db(abs(R0.sparam))
figure(),plot(R0.freq,R0.magS_db,R0.freq[R0.mode],R0.magS_db[R0.mode],'*')
modes=list(R0.freq[R0.mode])
print(modes)
#%%
#如果自动搜索腔模有问题，在这一段做修正。


#%%
#粗扫
R0.fspan,R0.IFbandwidth,R0.points,R0.average=0.5e6,10,5001,1
waitime=R0.points/R0.IFbandwidth*R0.average
#%%
#R0.IFbandwidth=100
#waitime=R0.points/R0.IFbandwidth*R0.average
R0.power=-60
#R0.fspan=1e6
R0.fcenter=modes[0]
R0.sweep()
time.sleep(waitime)
R0.fetchData()
R0.f0=R0.freq[R0.magS_db.argmin()]
P0=[1e6,1e5,0,R0.f0]
R0.update2(P0)
print('Mode {} at {}, Qi={},Qc={}'.format(0,R0.fcenter,R0.Qi,R0.Qc))

figure()
subplot(211),plot(R0.freq,rf.mag_2_db(np.abs(R0.S_n)),'*',R0.freq,rf.mag_2_db(np.abs(R0.S_fit)))
subplot(212),plot(R0.invS_n.real,R0.invS_n.imag,'*',R0.invS_fit.real,R0.invS_fit.imag,'r-')
    
#%%
    