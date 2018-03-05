# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 12:55:43 2018

@author: jyr_king
"""

from PyQt5 import QtCore,QtWidgets,QtGui
from PyQCLab.UIs.Network_Analyser_UI_simple import Ui_Dialog
from PyQCLab.Instrument.NetworkAnalyser import ZNB20
import sys

class NetworkAnalyzer_Dialog(object):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.Dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        
#        self.vna=ZNB20()
        self.ui.edt_fstart.editingFinished.connect(lambda:self.update_freq_params('ss'))
        self.ui.edt_fstop.editingFinished.connect(lambda:self.update_freq_params('ss'))
        self.ui.edt_fcenter.editingFinished.connect(lambda:self.update_freq_params('cs'))
        self.ui.edt_fspan.editingFinished.connect(lambda:self.update_freq_params('cs'))
        
        self.ui.pushButton_path.pressed.connect(self.set_save_path)
        self.Dialog.show()
        sys.exit(app.exec_())
    

    def update_freq_params(self,method='ss'):
        params=list(self.get_freq_params())
        if method == 'ss':
            params[0]/=1e9
            params[1]/=1e9
            params[2]=(params[0]+params[1])/2
            params[3]=(params[1]-params[0])*1e3
        elif method == 'cs':
            params[0]=params[2]/1e9-params[3]/2/1e9
            params[1]=params[2]/1e9+params[3]/2/1e9
            params[2]/=1e9
            params[3]/=1e6
            
#        print(params)
        self.set_freq_params(params)
        
    def get_freq_params(self):
        return \
            float(self.ui.edt_fstart.text())*1e9,\
            float(self.ui.edt_fstop.text())*1e9,\
            float(self.ui.edt_fcenter.text())*1e9,\
            float(self.ui.edt_fspan.text())*1e6
            
    def set_freq_params(self,params):
        fstart,fstop,fcenter,fspan=params
        self.ui.edt_fstart.setText(str(fstart))
        self.ui.edt_fstop.setText(str(fstop))
        self.ui.edt_fcenter.setText(str(fcenter))
        self.ui.edt_fspan.setText(str(fspan))
        
        
    def get_power(self):
        return float(self.ui.edt_Power.text())
    
    def get_sweep_mode(self):
        return self.ui.cbBox_swpMode.currentText()
    
    def get_sweep_type(self):
        return self.ui.cbBox_swpType.currentText()
        
    def set_sweep_mode(self,mode):
        self.ui.cbBox_swpMode.setCurrentText(mode)
        
    def set_sweep_type(self,typ):
        self.ui.cbBox_swpType.setCurrentText(typ)
        
    def get_sweep_points(self):
        return int(self.ui.edt_swpPoints.text())
    
    def get_IFbandwidth(self):
        return int(self.ui.edt_IF.text())
    
    def get_avg_times(self):
        return self.ui.spinBox_Avg.value()
    
    def set_save_path(self):
        dir_path=QtWidgets.QFileDialog.getExistingDirectory(self.Dialog,'save file','./')
        self.ui.lineEdit_path.setText(dir_path)
        
    def get_save_path(self):
        return self.ui.lineEdit_path.text()
    
    def get_save_filename(self):
        return self.ui.lineEdit_filename.text()
    
    def start_sweep(self):
        pass
#        self.vna.sweepMode=self.get_sweep_mode()
#        self.vna.sweepType=self.get_sweep_type()
#        
#        fstart,fstop,fcenter,fspan=self.get_freq_params()
#        pwr=self.get_power()
#        points=self.get_sweep_points()
#        IF=self.get_IFbandwidth()
#        avg_times=self.get_avg_times()
#        
#        self.vna.setSweep((fstart,fstop,IF,points,pwr,avg_times))
#        self.vna.sweep()
    
        
    
if __name__ == "__main__":
    NetworkAnalyzer_Dialog()