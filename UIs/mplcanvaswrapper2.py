# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 01:14:16 2016

@author: Win7
"""

#from PyQt4 import  QtGui
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import  FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

#from array import array

import time

#import random
#
#import threading
#
#from datetime import datetime

#from matplotlib.dates import  date2num, MinuteLocator, SecondLocator, DateFormatter

#X_MINUTES = 1
#
#Y_MAX = 100
#
#Y_MIN = 1
#
#INTERVAL = 1
#
#MAXCOUNTER = int(X_MINUTES * 60/ INTERVAL)

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

#        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass
    
class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self,x,y):
#        t = np.arange(0.0, 3.0, 0.01)
#        s = np.sin(2*np.pi*t)
        self.axes.plot(x,y,'o-')
        self.axes.set_autoscale_on(True)
        self.draw()


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
#        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()
#class MplCanvas(FigureCanvas):
#
#    def __init__(self):
#    
#        self.fig = Figure()
#        
#        self.ax = self.fig.add_subplot(111)
#        
#        FigureCanvas.__init__(self, self.fig)
#        
#        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
#        
#        FigureCanvas.updateGeometry(self)
#        
#        self.ax.set_xlabel("time of data generator")
#        
#        self.ax.set_ylabel('random data value')
#        
#        self.ax.legend()
#        
#        self.ax.set_ylim(Y_MIN,Y_MAX)
#        
#        self.ax.xaxis.set_major_locator(MinuteLocator())  # every minute is a major locator
#        
#        self.ax.xaxis.set_minor_locator(SecondLocator([10,20,30,40,50])) # every 10 second is a minor locator
#        
#        self.ax.xaxis.set_major_formatter( DateFormatter('%H:%M:%S') ) #tick label formatter
#        
#        self.curveObj = None # draw object
#
#    def plot(self, datax, datay):
#    
#        if self.curveObj is None:
#        
#        #create draw object once
#        
#            self.curveObj, = self.ax.plot_date(np.array(datax), np.array(datay),'bo-')
#        
#        else:
#        
#        #update data of draw object
#        
#            self.curveObj.set_data(np.array(datax), np.array(datay))
#        
#        #update limit of X axis,to make sure it can move
#        
#        self.ax.set_xlim(datax[0],datax[-1])
#        
#        ticklabels = self.ax.xaxis.get_ticklabels()
#    
#        for tick in ticklabels:
#        
#            tick.set_rotation(25)
#        
#        self.draw()

class  MplCanvasWrapper(QtGui.QWidget):

    def __init__(self , parent =None):    
        QtGui.QWidget.__init__(self, parent)        
        self.canvas = MyStaticMplCanvas()        
        self.vbl = QtGui.QVBoxLayout()        
        self.ntb = NavigationToolbar(self.canvas, parent)        
        self.vbl.addWidget(self.ntb)       
        self.vbl.addWidget(self.canvas)       
        self.setLayout(self.vbl)       
        self.dataX= np.linspace(0,2*np.pi,101)      
        self.dataY= np.sin(self.dataX)**2        
#        self.initDataGenerator()

    def startPlot(self):
        self.canvas.compute_initial_figure(self.dataX,self.dataY)
    
#        self.__generating = True
#    
#    def pausePlot(self):
#    
#        self.__generating = False
#    
#    def initDataGenerator(self):
#    
#        self.__generating=False
#        
#        self.__exit = False
#        
#        self.tData = threading.Thread(name = "dataGenerator",target = self.generateData)
#        
#        self.tData.start()
#        
#    def releasePlot(self):
#    
#        self.__exit  = True
#        
#        self.tData.join()
#    
#    def generateData(self):
#    
#        counter=0
#    
#        while(True):
#    
#            if self.__exit:
#    
#                break
#    
#            if self.__generating:
#    
#                newData = random.randint(Y_MIN, Y_MAX)
#
#                newTime= date2num(datetime.now())
#
#                self.dataX.append(newTime)
#
#                self.dataY.append(newData)
#
#                self.canvas.plot(self.dataX, self.dataY)
#
#            if counter >= MAXCOUNTER:
#
#                self.dataX.pop()
#
#                self.dataY.pop()
#
#
#            else:
#
#                counter+=1
#
#            time.sleep(INTERVAL)