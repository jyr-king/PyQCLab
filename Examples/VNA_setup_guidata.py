# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 22:50:13 2018

@author: jyr_king
"""

import numpy as np
from pylab import *
import skrf as rf
from PyQCLab.Instrument.NetworkAnalyser import *
from PyQCLab.etc.instr_config import *
import guidata.qt.QtCore as QtCore
import guidata.qt.QtGui as QtGui

import guidata.dataset.datatypes as gdt
import guidata.dataset.dataitems as gdi
import guidata.dataset.qtwidgets as gdq
import guidata.configtools as configtools

#import guiqwt.plot as gqp
#import guiqwt.curve as gqc
#import guiqwt.image as gqi
#import guiqwt.tools as gqt
import time

class Vna_Parameters(gdt.DataSet):
    g1 = gdt.BeginGroup('Sweep setups:')
    swp_mode=gdi.ChoiceItem('Sweep Mode:',[('hold','Hold'),('cont','Continuous'),('gro','Groups'),('sing','Single')])
    swp_type=gdi.ChoiceItem('Sweep Type:',[('lin','Linear'),('log','Logarithmic'),('pow','Power'),('cw','CW'),\
                                           ('segm','Segment'),('phas','Phase')])
    swp_points=gdi.IntItem('Sweep Points:',min=ZNB20_CONSTS['POINTMIN'],max=ZNB20_CONSTS['POINTMAX'],default=10001)
    swp_IFbandwidth=gdi.IntItem('IF_Bandwidth:',min=ZNB20_CONSTS['IFMIN'],max=ZNB20_CONSTS['IFMAX'],default=1000)
    swp_average=gdi.IntItem('Average:',min=1,default=1)
    _g1=gdt.EndGroup('Sweep setups:')
    
    _prop = gdt.GetAttrProp("choice")
    g2 = gdt.BeginGroup('Frequency Setup:')
    choice = gdi.ChoiceItem('',[('SS','Start Stop'),('CS','Center Span')],radio=False)\
                            .set_prop('display',store=_prop)
    fstart = gdi.FloatItem('Start (GHz):',min=ZNB20_CONSTS['FREQMIN']/1e9,\
                           max=ZNB20_CONSTS['FREQMAX']/1e9,default=4)\
                           .set_prop('display',active=gdt.FuncProp(_prop, lambda x: x=='SS'))
    fstop = gdi.FloatItem('Stop (GHz):',min=ZNB20_CONSTS['FREQMIN']/1e9,\
                          max=ZNB20_CONSTS['FREQMAX']/1e9,default=8)\
                          .set_prop('display',active=gdt.FuncProp(_prop, lambda x: x=='SS'))
    fcenter = gdi.FloatItem('Center (GHz):',min=ZNB20_CONSTS['FREQMIN']/1e9,\
                            max=ZNB20_CONSTS['FREQMAX']/1e9,default=8)\
                            .set_prop('display',active=gdt.FuncProp(_prop, lambda x: x=='CS'))
    fspan = gdi.FloatItem('Span (GHz):',min=ZNB20_CONSTS['FREQMIN']/1e9,\
                          max=ZNB20_CONSTS['FREQMAX']/1e9,default=8)\
                          .set_prop('display',active=gdt.FuncProp(_prop, lambda x: x=='CS'))
    _g2 = gdt.EndGroup('Frequency Setup:')
    
    g3 = gdt.BeginGroup('Power Setup:')
    pwr = gdi.FloatItem('Power (dBm):',min=ZNB20_CONSTS['POWMIN'],max=ZNB20_CONSTS['POWMAX'],default=-12)
    _g3 = gdt.EndGroup('Power Setup:')
    
    g4 = gdt.BeginGroup('Save:')
    save_enable = gdi.BoolItem("Enable Data Save",
                      help="If disabled, the following parameters will be ignored",
                      default=False)
    path = gdi.DirectoryItem('Directory:','C:/Users/SC05/Documents/')
    filename = gdi.StringItem('File Name:',time.strftime("%Y-%m-%d", time.localtime())+'_VNA_sweep')
    _g4 = gdt.EndGroup('Save:')
    
#Vna_Parameters.active_setup()    
    
if __name__ == "__main__":
    # -- Create QApplication
    import guidata
    _app = guidata.qapplication()
    
    vna_params = Vna_Parameters()
    if vna_params.edit():
        vna = ZNB20()
#        vna.sweepMode=vna_params.swp_mode
#        vna.sweepType=vna_params.swp_type
        if vna_params.choice == 'CS':
            fstart,fstop=vna_params.fcenter-vna_params.fspan/2*1e9,vna_params.fcenter+vna_params.fspan/2*1e9
        else:
            fstart,fstop=vna_params.fstart*1e9,vna_params.fstop*1e9
        
        vna.setSweep([fstart,fstop,vna_params.swp_IFbandwidth,vna_params.swp_points,vna_params.pwr,vna_params.swp_average])
        vna.sweep2()
        freq,Sdata=vna.getData()
        if vna_params:
            np.savez(vna_params.path+vna_params.filename,freq=freq,Sdata=Sdata)
        figure(),plot(freq,rf.mag_2_db(np.abs(Sdata)))
        
#    stamp_gbox = gdq.DataSetEditGroupBox("Dots", Vna_Parameters)
#    stamp_gbox.show()
    x=vna_params.swp_IFbandwidth
    print(vna_params.choice,x)
