# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:59:47 2018

@author: SC05
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:15:06 2018

@author: SC05

"""
from PyQCLab.Apps.Resonator_znb20 import *
from PyQCLab.Utils.Qextractor import *
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import time
import skrf as rf
from GS200 import GS_200
#%%
gsV=GS_200('TCPIP0::10.204.4.242::inst0::INSTR')
gsV.setLevel(0.015)
gsV.Start_OutPut()
gsV.Stop_OutPut()
#%%
Sdata=list()
Fredata=list()
Vspace=np.linspace(-0.2,-0.1,80)
for i in range(len(Vspace)):
    gsV.setLevel(Vspace[i])
    fcenter=6.6471e9
    fspan=5e6
    pwr=-40
    IF=50
    N=501
    avg=1
    R0=Resonator(fcenter)
    time.sleep(1)
    R0.average=avg
    R0.searchMode(pwr,IF0=IF,points=N,span0=fspan,search_factor=10)
    modes=list(R0.freq[R0.mode])
    print(modes)
    Sdata.append(R0.magS_db)
    
    Fredata.append(R0.freq)
    print(i)
#    figure(0),plt.plot(R0.freq,R0.magS_db,R0.freq[R0.mode],R0.magS_db[R0.mode],'*')
#    plt.xlabel(str(around(np.array(modes)/1e9,4)))
#%%
plt.imshow(np.transpose(Sdata))
#%%单独手动扫某个腔
#for i in range(8):
fcenter=6.217821945e9
fspan=0.15e6
brd=20e3
pwr=-56
IF=2
N=201
avg=20
R0=Resonator(fcenter)

time.sleep(1)
R0.average=avg
R0.search_succeed=True
#R0.searchMode(pwr,IF0=IF,points=N,span0=fspan,search_factor=10)
#R0.f0=R0.freq[R0.magS_db.argmin()]
R0.setScan(fcenter,0,brd,fspan)
R0.fineScan2(pwr,IF,N,weight=[20,80],avg=avg)
#freq=R0.freq
#magS=rf.mag_2_db(abs(R0.sparam))
figure(),plt.plot(R0.freq,R0.magS_db,R0.freq[R0.mode],R0.magS_db[R0.mode],'*')
#%%
diptitle='5bit'
plt.title(str(pwr)+':dbm_atten:-33db'+diptitle)
plt.xlabel(str(around(np.array(modes)/1e9,4)))
plt.ylabel('Qi'+str(around(np.array(R0.Qi)/1e4,4))+'w')
savefig('C:\\Users\\SC05\\Documents\\PyQCLab\\Data\\20180204add\\'+diptitle+str(pwr)+'.png')

pathw='C:\\Users\\SC05\\Documents\\PyQCLab\\Data\\20180125\\'
filenamen6=pathw+'25zuihouNb6dip1'+str(pwr)+'DB'+str(IF)+'IF'+str(avg)+'NQI_'+str(int(round(R0.Qi,-4)/10000))
plt.savefig(filenamen6+'w.png')
d=resonData(pwr-53,R0.freq,R0.sparam,[R0.Qi,R0.Qc,R0.f0])
d.saveData(filenamen6)
#modes=list(R0.freq[R0.mode])
#print(modes)
#%%
