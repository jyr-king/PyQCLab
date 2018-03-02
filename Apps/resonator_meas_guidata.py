# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:02:43 2016

@author: Win7
"""
from guidata.qt.QtGui import QMainWindow, QSplitter, QDialog, QHBoxLayout, QVBoxLayout, QButtonGroup, QPushButton

from guidata.dataset.datatypes import (DataSet, BeginGroup, EndGroup,
                                       BeginTabGroup, EndTabGroup)
from guidata.dataset.dataitems import (ChoiceItem, FloatItem, IntItem, StringItem,
                                       DirectoryItem, FileOpenItem, MultipleChoiceItem)
from guidata.dataset.qtwidgets import DataSetShowGroupBox, DataSetEditGroupBox
from guidata.configtools import get_icon
from guidata.qthelpers import create_action, add_actions, get_std_icon

from guiqwt.builder import make
from guiqwt.plot import CurveWidget, QToolBar, CurveWidgetMixin
# Local test import:
from guidata.tests.activable_dataset import ExampleDataSet

class freqSetup(DataSet):
    fstart=FloatItem('Start (GHz)',default=4)
    fstop=FloatItem('Stop (GHz)',default=8)
    fcenter=FloatItem('Center (GHz)',default=0)
    fspan=FloatItem('Span (MHz)',default=0)
    mc=MultipleChoiceItem('mc1',['choice1','choice2','choice3']).vertical()
    
class powerSetup(DataSet):
    power=FloatItem('Power (dBm)',default=-20)
    
class sweepSetup(DataSet):
    swpMode=ChoiceItem('Sweep Mode:',('SINGle','HOLD','CONTinous','GROups'),default=0)
    swpType=ChoiceItem('Sweep Type:',('LINear','LOGarithmic','POWer','CW','SEGMent','PHASe'),default=0)
    swpPoints=IntItem('Sweep Points:',default=201,min=1,max=100001)
    IFbandWidth=IntItem('IF Bandwidth (Hz):',default=1000,min=1,max=15000000)
    avgTimes=IntItem('Average Times:',default=1,min=1,max=10000)
    
    
class resonMeasDlg(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowIcon(get_icon('python.png'))
        self.setWindowTitle("Application example")
        self.groupbox1 = DataSetEditGroupBox("Freqency Setup",
                                             freqSetup, comment='')
#        self.groupbox1.SIG_APPLY_BUTTON_CLICKED.connect(self.update_window)
        self.groupbox2 = DataSetEditGroupBox("Power Setup",
                                             powerSetup, comment='')
        self.groupbox3 = DataSetEditGroupBox("Power Setup",
                                             sweepSetup, comment='')                                     
        self.btnStartSwp=QPushButton('Start Sweep')
        self.btnCancel=QPushButton('Cancel')  
        self.curvewidget=CurveWidget()
        toolbar=QToolBar('tools')
#        toolbar.show()
        self.curvewidget.add_toolbar(toolbar)
        self.curvewidget.register_all_curve_tools()
#        self.curvewidget.activate_default_tool()
#        self.set                                  
#        buttonbox=QButtonGroup(QW)
#        buttonbox.addButton(self.btnStartSwp)
#        buttonbox.addButton(self.btnCancel)
        btnLayout=QVBoxLayout()
        btnLayout.addStretch()
        btnLayout.addWidget(self.btnStartSwp)
        btnLayout.addWidget(self.btnCancel)
        self.update_groupboxes()
        
        splitter = QHBoxLayout()
        splitter.addWidget(self.groupbox1)
        splitter.addWidget(self.groupbox2)
        splitter.addWidget(self.groupbox3)
        splitter.addLayout(btnLayout)
        
        Flayout=QVBoxLayout()
        Flayout.addLayout(splitter)
        Flayout.addWidget(toolbar)
        Flayout.addWidget(self.curvewidget)
        self.setLayout(Flayout)
        self.setContentsMargins(10, 5, 10, 5)
        
        self.btnCancel.clicked.connect(self.close)
        self.btnStartSwp.clicked.connect(self.sweep)        
#        self.connect(self.btnCancel,SIGNAL('clicked()'),self,SLOT('close()'))
        
    def update_window(self):
        dataset = self.groupbox1.dataset
        
        self.setWindowTitle(dataset.title)
        self.setWindowIcon(get_icon(dataset.icon))
        self.setWindowOpacity(dataset.opacity)
        
    def update_groupboxes(self):
        self.groupbox1.get()
        
    def sweep(self):
        plot=self.curvewidget.plot
        from numpy import linspace, sin, trapz
        x = linspace(-10, 10, 1000)
        y = sin(sin(sin(x)))
        curve = make.curve(x, y, "ab", "b")
        range1 = make.range(-2, 2)
        plot.add_item(curve)
        plot.add_item(range1)
        dataset=self.groupbox1.dataset
        print(dataset.mc)

        
if __name__ == '__main__':
    from guidata.qt.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = resonMeasDlg()
    window.show()
    sys.exit(app.exec_())