# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 19:32:49 2017

@author: SC05
"""
import sys
import visa
#import numpy as np
from PyQt5.QtWidgets import QMessageBox

#Rm=visa.ResourceManager()
#Inst=Rm.open_resource('TCPIP0::10.204.4.244::inst0::INSTR')
#Inst.write(':SOUR:FUNC VOLT')
#Inst.write(':SOUR:RANG 1e0')
#Inst.write(':SOUR:LEV 0.2')
#Inst.write(':OUTP 0')
#
#
#Inst.close()
#%%
class GS_200(object):
    def __init__(self,name='TCPIP0::10.204.4.243::inst0::INSTR'):#DC6
        try:
            Rm=visa.ResourceManager()
            self.Inst=Rm.open_resource(name)
        except:
            QMessageBox.critical(None,"傻瓜", "找不到yokugawa了吧，哈哈")
#            sys.exit()
    def rst(self):
        self.Inst.write('*RST')
    def setCURRmode(self):
        self.Inst.write(':SOUR:FUNC CURR')
    def setVOLTmode(self):
        self.Inst.write(':SOUR:FUNC VOLT')#default
    def setLevel(self,level=0.0):
        self.Inst.write(':SOUR:LEV {}'.format(level))
    def setRange_Lev(self,rang=1):
        self.Inst.query(':SOUR:RANG {}'.format(rang))
    def Start_OutPut(self):
        self.Inst.write(':OUTP 1')
    def Stop_OutPut(self):
        self.Inst.write(':OUTP 0')
    def Close(self):
        self.Inst.close()