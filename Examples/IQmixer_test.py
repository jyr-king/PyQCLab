# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:21:15 2017

@author: A108QCLab
"""
import numpy as np
from pylab import *
#from time import sleep
from PyQCLab.Utils.WaveForm_v2 import *
from PyQCLab.Instrument.spcmDA import *
from PyQCLab.Instrument.pyspcm import *
from PyQCLab.Instrument.digitizer_v2 import *
from PyQCLab.Instrument.MWSource import *
from PyQCLab.Instrument.DG645 import *
from time import sleep
#%%
#-------------创建所需的微波源。-------------------------------------------#
mw1=RS_MWSource('SMB100A_1')        #Qubit microwave drive
mw2=RS_MWSource('SMB100A_0')        #Readout resonator drive
#%%
#-------------创建AWG并初始化。-------------------------------------------#
da1=spectrumDA(1)
da1.level0=1000
#da1.level0
da1.level1=1000
#da1.level1
#da1.chEnable((1,))
#da1.output(1)
da1.chEnableAll()
da1.outputAll()
da1.runmode='single_r'
da1.setTriggerSource('ext0')
da1.setTriggerMode()
da1.setClockMode('ext')
da2=spectrumDA(0)
da2.level0=1000
da2.chEnable((0,))
da2.output(0)
da2.runmode='single_r'
da2.setTriggerSource('ext0')
da2.setTriggerMode()
da2.setClockMode('int')
#%%
#-------------创建DG645并设置脉冲延时-------------------------------------------#
dg1=DG645()
dg1.delayA=1e-6
dg1.delayAB=1e-6
dg1.trigSource('int')
dg1.trigRate(1e3)
#%%
#-------------创建IQ调制波形-------------------------------------------#
l=KILO_B(64)
Imod=WaveForm(length=l,AWGType='spcm4')
Qmod=WaveForm(length=l,AWGType='spcm4')
Ioff=WaveForm(length=l/2,AWGType='spcm4')
Imod.createWindow((('kaiser_r',0,1000,12),('rectangle',1000,5000),('kaiser_f',5000,6000,12)))
Qmod.createWindow((('kaiser_r',0,1000,12),('rectangle',1000,5000),('kaiser_f',5000,6000,12)))
Ioff.createWindow((('kaiser_r',0,500,12),('rectangle',500,2500),('kaiser_f',2500,3000,12)))
Imod.createWaveform()
Qmod.createWaveform()
Ioff.createWaveform()
#%%
#-------------波形写入DA卡，打开微波，触发DG645-------------------------------------------#
wfdata=np.array([Imod.waveform,Qmod.waveform]).flatten('F')
da1.writeWaveForm(wfdata)
da2.writeWaveForm(Ioff.waveform)
mw1.freqency=10e6
mw1.level=0
mw1.set_output(True)

da1.start()
da2.start()
dg1.start()
#%%

