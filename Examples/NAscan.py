# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:20:14 2017
网络分析仪扫描的示例代码。以罗德的ZNB20网分为例。
@author: A108QCLab
"""
#%%
#导入所需的模块
import numpy as np
from PyQCLab.Instrument.NetworkAnalyser import *
from PyQCLab.Utils.Qextractor import *
from PyQCLab.Utils.DigiFilters import savitzky_golay
from pylab import *
import time
import skrf as rf
#%%
#创建网分设备并初始化
na=ZNB20()

