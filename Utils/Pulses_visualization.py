# -*- coding: utf-8 -*-
"""
Created on Thu May 18 19:43:45 2017

@author: A108QCLab
"""
import numpy as np
from pylab import *
from PyQCLab.Utils.WaveForm_v2 import *
import math
#%%
Imod=WaveForm(length=10000,AWGType='spcm4')
Imod.createBase('sin',period=50)
Imod.createWindow((('kaiser_r',0,1000,12),\
                     ('rectangle',1000,9000),\
                     ('kaiser_f',9000,10000,12)\
                     ))
Imod.createWaveform()
figure(),plot(Imod.rawWaveform)
