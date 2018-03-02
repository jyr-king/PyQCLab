# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 01:45:00 2016

@author: Win7
"""

import sys
from PyQt4 import QtCore, QtGui, uic
#import instrument_unstable2 as ins
sys.path.append('..\\Instrument\\')
import NetworkAnalyser
import time

#qtCreatorFile = "E:\\Python Scripts\\PyQCLab\\UIs\\Reson_meas_uiDlg.ui" # Enter file here.
qtCreatorFile = "..\\UIs\\Reson_meas_uiDlg.ui" # Enter file here.
 
Ui_Dlg, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class resonMeas(QtGui.QDialog, Ui_Dlg):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_Dlg.__init__(self)
        self.setupUi(self)
        #-------------------------连接信号。-----------------------------
        self.btn_singleSweep.clicked.connect(self.singleSweep)
        self.btn_addSeg.clicked.connect(self.addSegment)
        self.lst_Segments.itemDoubleClicked.connect(self.delSegment)
        self.lst_Segments.itemChanged.connect(self.stopEditSeg)
        self.edt_Freq_start.editingFinished.connect(self.update_freqencySS)
        self.edt_Freq_stop.editingFinished.connect(self.update_freqencySS)
        self.edt_Freq_center.editingFinished.connect(self.update_freqencyCS)
        self.edt_Freq_span.editingFinished.connect(self.update_freqencyCS)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.elapsed=0
        self.totalTime=0
        self.t_start=0
        
        #-----------------------创建并初始化设备，显示初始参数。------------
#        self.analyser=NetworkAnalyser('PNA')
#        self.edt_Freq_start.setText(str(self.analyser.fstart/1e9))
#        self.edt_Freq_stop.setText(str(self.analyser.fstop/1e9))
#        self.edt_Freq_center.setText(str(self.analyser.fcenter/1e9))
#        self.edt_Freq_span.setText(str(self.analyser.fspan/1e6))
#        self.edt_Power.setText(str(self.analyser.power))
#        self.cbBox_swpMode.setCurrentIndex(self.analyser.SWP_MODES[self.analyser.sweepMode])
#        self.cbBox_swpType.setCurrentIndex(self.analyser.SWP_TYPES[self.analyser.sweepType])
#        self.edt_swpPoints.setText(str(self.analyser.points))
#        self.edt_IF.setText(str(self.analyser.IFbandwidth))
#        self.spinBox_Avg.setValue(str(self.analyser.average))
        
    def singleSweep(self):
        self.progressBar.setValue(0)
        self.timer.start(1000)
        f_start=float(self.edt_Freq_start.text())
        f_stop=float(self.edt_Freq_stop.text())
        bandwidth=float(self.edt_IF.text())
        N=float(self.edt_swpPoints.text())
        avg=self.spinBox_Avg.value()
        p=float(self.edt_Power.text())
        self.t_start=time.time()
        self.totalTime=N/bandwidth
        print(self.totalTime)
#        time.sleep(10)
#        t_stop=time.time()
#        self.timer.stop()
#        self.analyser.setSweep(f_start,f_stop,bandwidth,N,p,avg)
#        self.analyser.sweepMode=self.cbBox_swpMode.currentText()
#        self.analyser.sweepType=self.cbBox_swpType.currentText()
#        self.analyser.sweep()
#        print(self.cbBox_swpMode.currentText())
        
        self.mplCanvas.startPlot([1,2,3,4],[4,5,3,1])
    def addSegment(self):
        item=QtGui.QListWidgetItem(self.edt_Segment.text())
        self.lst_Segments.addItem(item)
    def delSegment(self):
        item=self.lst_Segments.currentItem()
        self.lst_Segments.openPersistentEditor(item)
    def stopEditSeg(self):
        item=self.lst_Segments.currentItem()
        self.lst_Segments.closePersistentEditor(item)
        print(item.text())
    def update_freqencySS(self):
        f_start=float(self.edt_Freq_start.text())*1e9
        f_stop=float(self.edt_Freq_stop.text())*1e9
        if f_stop < f_start:
            f_stop=f_start
#        f_center=float(self.edt_Freq_center.text())*1e9
#        f_span=float(self.edt_Freq_span.text())*1e6
        f_center=(f_start+f_stop)/2
        f_span=f_stop-f_start
        self.edt_Freq_center.setText(str(f_center/1e9))
        self.edt_Freq_span.setText(str(f_span/1e6))
            
    def update_freqencyCS(self):
        f_center=float(self.edt_Freq_center.text())*1e9
        f_span=float(self.edt_Freq_span.text())*1e6
        if f_span < 0:
            f_span = 0
        f_start=f_center-f_span/2
        f_stop=f_center+f_span/2
        self.edt_Freq_start.setText(str(f_start/1e9))
        self.edt_Freq_stop.setText(str(f_stop/1e9))        
#    def get_linevalue(self):
#        self.plainTextEdit.setPlainText(self.edt_Freq_start.text())
#        value=float(self.edt_Freq_start.text())
#        print(value*10)
    def update_progress(self):
        self.elapsed=time.time()-self.t_start
        self.progressBar.setValue(self.elapsed/self.totalTime*100)
        if self.elapsed > self.totalTime:
            self.timer.stop()
        print(self.progressBar.value())
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = resonMeas()
    window.show()
    sys.exit(app.exec_())
