# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 10:41:43 2018

Configuration file for instruments.

@author: jyr_king
"""

VISA_RESOURCES={
                  'SMB100A_0': 'TCPIP0::10.204.4.249::INSTR',
                  'SMB100A_1': 'TCPIP0::10.204.4.247::INSTR', 
                  'SMF100A': 'TCPIP0::10.204.4.250::inst0::INSTR',
                  'ADCMT6166': '',
                  'AG33120A_0': 'GPIB0::10::INSTR',
                  'AG33120A_1': '',
                  'PNA': 'TCPIP0::10.204.4.252::inst0::INSTR',
                  'ZNB20':'TCPIP0::ZNB20-62-101800::inst0::INSTR',
                  'YOKOGAWA7651': 'GPIB0::14::INSTR',
                  'AWG5014C': 'TCPIP0::AWG-3289382193::inst0::INSTR',
                  'SR620': '',
                  'DG645':'TCPIP0::10.204.4.200::inst0::INSTR',
                  'DC6':'TCPIP0::10.204.4.243::inst0::INSTR',
                  'DC3':'TCPIP0::10.204.4.242::inst0::INSTR',
                  }

#instrument specified constanses
PNA_CONSTS={
        'FREQMAX':20e9,
        'FREQMIN':10e6,
        'POWMAX':5,
        'POWMIN':-27,
        'POINTMIN':1,
        'POINTMAX':100001,
        'IFMIN':1,
        'IFMAX':15000000
        }

ZNB20_CONSTS={
        'FREQMAX':20e9,
        'FREQMIN':10e6,
        'POWMAX':10,
        'POWMIN':-60,
        'POINTMIN':1,
        'POINTMAX':100001,
        'IFMIN':1,
        'IFMAX':15000000
        }