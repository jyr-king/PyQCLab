# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Network_Analyser_UI_simple.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from embedding_in_qt5 import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1280, 768)
        self.groupBox_scanParams = QtWidgets.QGroupBox(Dialog)
        self.groupBox_scanParams.setGeometry(QtCore.QRect(940, 10, 331, 231))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.groupBox_scanParams.setFont(font)
        self.groupBox_scanParams.setObjectName("groupBox_scanParams")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_scanParams)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 311, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.cbBox_swpType = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cbBox_swpType.setObjectName("cbBox_swpType")
        self.cbBox_swpType.addItem("")
        self.cbBox_swpType.addItem("")
        self.cbBox_swpType.addItem("")
        self.cbBox_swpType.addItem("")
        self.cbBox_swpType.addItem("")
        self.cbBox_swpType.addItem("")
        self.gridLayout.addWidget(self.cbBox_swpType, 1, 1, 1, 1)
        self.label_swpMode = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_swpMode.setObjectName("label_swpMode")
        self.gridLayout.addWidget(self.label_swpMode, 0, 0, 1, 1)
        self.cbBox_swpMode = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cbBox_swpMode.setObjectName("cbBox_swpMode")
        self.cbBox_swpMode.addItem("")
        self.cbBox_swpMode.addItem("")
        self.cbBox_swpMode.addItem("")
        self.cbBox_swpMode.addItem("")
        self.gridLayout.addWidget(self.cbBox_swpMode, 0, 1, 1, 1)
        self.spinBox_Avg = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_Avg.setMinimum(1)
        self.spinBox_Avg.setObjectName("spinBox_Avg")
        self.gridLayout.addWidget(self.spinBox_Avg, 4, 1, 1, 1)
        self.edt_IF = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edt_IF.setObjectName("edt_IF")
        self.gridLayout.addWidget(self.edt_IF, 3, 1, 1, 1)
        self.label_SwpType = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_SwpType.setObjectName("label_SwpType")
        self.gridLayout.addWidget(self.label_SwpType, 1, 0, 1, 1)
        self.label_AvgTime = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_AvgTime.setObjectName("label_AvgTime")
        self.gridLayout.addWidget(self.label_AvgTime, 4, 0, 1, 1)
        self.label_IF = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_IF.setObjectName("label_IF")
        self.gridLayout.addWidget(self.label_IF, 3, 0, 1, 1)
        self.label_swpPoints = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_swpPoints.setObjectName("label_swpPoints")
        self.gridLayout.addWidget(self.label_swpPoints, 2, 0, 1, 1)
        self.edt_swpPoints = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edt_swpPoints.setObjectName("edt_swpPoints")
        self.gridLayout.addWidget(self.edt_swpPoints, 2, 1, 1, 1)
        self.groupBox_freq = QtWidgets.QGroupBox(Dialog)
        self.groupBox_freq.setGeometry(QtCore.QRect(940, 240, 331, 201))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.groupBox_freq.setFont(font)
        self.groupBox_freq.setObjectName("groupBox_freq")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_freq)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 30, 311, 161))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_fstart = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_fstart.setObjectName("label_fstart")
        self.verticalLayout_3.addWidget(self.label_fstart)
        self.label_fstop = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_fstop.setObjectName("label_fstop")
        self.verticalLayout_3.addWidget(self.label_fstop)
        self.label_fcenter = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_fcenter.setObjectName("label_fcenter")
        self.verticalLayout_3.addWidget(self.label_fcenter)
        self.label_fspan = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_fspan.setObjectName("label_fspan")
        self.verticalLayout_3.addWidget(self.label_fspan)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.edt_fstart = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.edt_fstart.setObjectName("edt_fstart")
        self.verticalLayout_4.addWidget(self.edt_fstart)
        self.edt_fstop = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.edt_fstop.setObjectName("edt_fstop")
        self.verticalLayout_4.addWidget(self.edt_fstop)
        self.edt_fcenter = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.edt_fcenter.setObjectName("edt_fcenter")
        self.verticalLayout_4.addWidget(self.edt_fcenter)
        self.edt_fspan = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.edt_fspan.setObjectName("edt_fspan")
        self.verticalLayout_4.addWidget(self.edt_fspan)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.groupBox_pwr = QtWidgets.QGroupBox(Dialog)
        self.groupBox_pwr.setGeometry(QtCore.QRect(940, 440, 331, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.groupBox_pwr.setFont(font)
        self.groupBox_pwr.setObjectName("groupBox_pwr")
        self.layoutWidget_3 = QtWidgets.QWidget(self.groupBox_pwr)
        self.layoutWidget_3.setGeometry(QtCore.QRect(10, 30, 311, 41))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_power = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_power.setObjectName("label_power")
        self.horizontalLayout_4.addWidget(self.label_power)
        spacerItem1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.edt_Power = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.edt_Power.setObjectName("edt_Power")
        self.horizontalLayout_4.addWidget(self.edt_Power)
        self.groupBox_segments = QtWidgets.QGroupBox(Dialog)
        self.groupBox_segments.setGeometry(QtCore.QRect(940, 520, 331, 241))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.groupBox_segments.setFont(font)
        self.groupBox_segments.setObjectName("groupBox_segments")
        self.layoutWidget_4 = QtWidgets.QWidget(self.groupBox_segments)
        self.layoutWidget_4.setGeometry(QtCore.QRect(10, 40, 311, 191))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edt_Segment = QtWidgets.QLineEdit(self.layoutWidget_4)
        self.edt_Segment.setObjectName("edt_Segment")
        self.horizontalLayout.addWidget(self.edt_Segment)
        self.btn_addSeg = QtWidgets.QPushButton(self.layoutWidget_4)
        self.btn_addSeg.setObjectName("btn_addSeg")
        self.horizontalLayout.addWidget(self.btn_addSeg)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.table_segments = QtWidgets.QTableWidget(self.layoutWidget_4)
        self.table_segments.setObjectName("table_segments")
        self.table_segments.setColumnCount(0)
        self.table_segments.setRowCount(0)
        self.horizontalLayout_5.addWidget(self.table_segments)
        self.btn_delSeg = QtWidgets.QPushButton(self.layoutWidget_4)
        self.btn_delSeg.setObjectName("btn_delSeg")
        self.horizontalLayout_5.addWidget(self.btn_delSeg)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 610, 701, 141))
        self.widget.setObjectName("widget")
        self.gridLayout_file = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_file.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_file.setObjectName("gridLayout_file")
        self.lineEdit_path = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_path.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_path.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lineEdit_path.setFont(font)
        self.lineEdit_path.setObjectName("lineEdit_path")
        self.gridLayout_file.addWidget(self.lineEdit_path, 0, 0, 1, 1)
        self.pushButton_path = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_path.setFont(font)
        self.pushButton_path.setObjectName("pushButton_path")
        self.gridLayout_file.addWidget(self.pushButton_path, 0, 1, 1, 1)
        self.lineEdit_filename = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lineEdit_filename.setFont(font)
        self.lineEdit_filename.setObjectName("lineEdit_filename")
        self.gridLayout_file.addWidget(self.lineEdit_filename, 1, 0, 1, 1)
        self.pushButton_save = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_save.setFont(font)
        self.pushButton_save.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_save.setObjectName("pushButton_save")
        self.gridLayout_file.addWidget(self.pushButton_save, 1, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(10, 10, 921, 591))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_canvas = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_canvas.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_canvas.setObjectName("verticalLayout_canvas")
        self.graphicsView = QtWidgets.QGraphicsView(self.widget1)
        self.graphicsView = MyStaticMplCanvas(self.widget1)
        self.graphicsView.setObjectName("graphicsView")
        self.ntb=NavigationToolbar(self.graphicsView,self.widget1) 
        
        self.verticalLayout_canvas.addWidget(self.graphicsView)
        self.progressBar = QtWidgets.QProgressBar(self.widget1)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setProperty("value", 1)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_canvas.addWidget(self.progressBar)
        self.widget2 = QtWidgets.QWidget(Dialog)
        self.widget2.setGeometry(QtCore.QRect(720, 610, 211, 141))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_startstop = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_startstop.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_startstop.setObjectName("verticalLayout_startstop")
        self.pushButton_start = QtWidgets.QPushButton(self.widget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout_startstop.addWidget(self.pushButton_start)
        self.pushButton_quit = QtWidgets.QPushButton(self.widget2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.pushButton_quit.setFont(font)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.verticalLayout_startstop.addWidget(self.pushButton_quit)
#        self.label_fstart.setBuddy(Dialog.edt_Freq_start)

        self.retranslateUi(Dialog)
        self.pushButton_quit.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Vector Network Analyzer-Scanner"))
        self.groupBox_scanParams.setTitle(_translate("Dialog", "扫描设置"))
        self.cbBox_swpType.setItemText(0, _translate("Dialog", "LINear"))
        self.cbBox_swpType.setItemText(1, _translate("Dialog", "LOGarithmic"))
        self.cbBox_swpType.setItemText(2, _translate("Dialog", "POWer"))
        self.cbBox_swpType.setItemText(3, _translate("Dialog", "CW"))
        self.cbBox_swpType.setItemText(4, _translate("Dialog", "SEGMent"))
        self.cbBox_swpType.setItemText(5, _translate("Dialog", "PHASe"))
        self.label_swpMode.setText(_translate("Dialog", "Sweep Mode:"))
        self.cbBox_swpMode.setItemText(0, _translate("Dialog", "SINGle"))
        self.cbBox_swpMode.setItemText(1, _translate("Dialog", "HOLD "))
        self.cbBox_swpMode.setItemText(2, _translate("Dialog", "CONTinuous"))
        self.cbBox_swpMode.setItemText(3, _translate("Dialog", "GROups"))
        self.edt_IF.setText(_translate("Dialog", "1000"))
        self.label_SwpType.setText(_translate("Dialog", "Sweep Type:"))
        self.label_AvgTime.setText(_translate("Dialog", "Average times:"))
        self.label_IF.setText(_translate("Dialog", "IF bandwidth (Hz):"))
        self.label_swpPoints.setText(_translate("Dialog", "Sweep Points:"))
        self.edt_swpPoints.setText(_translate("Dialog", "1001"))
        self.groupBox_freq.setTitle(_translate("Dialog", "扫频设置"))
        self.label_fstart.setText(_translate("Dialog", "Start (GHz):"))
        self.label_fstop.setText(_translate("Dialog", "Stop (GHz):"))
        self.label_fcenter.setText(_translate("Dialog", "Center (GHz):"))
        self.label_fspan.setText(_translate("Dialog", "Span (MHz):"))
        self.edt_fstart.setText(_translate("Dialog", "4"))
        self.edt_fstop.setText(_translate("Dialog", "8"))
        self.edt_fcenter.setText(_translate("Dialog", "6"))
        self.edt_fspan.setText(_translate("Dialog", "4000"))
        self.groupBox_pwr.setTitle(_translate("Dialog", "功率"))
        self.label_power.setText(_translate("Dialog", "Power (dBm):"))
        self.edt_Power.setText(_translate("Dialog", "-10"))
        self.groupBox_segments.setTitle(_translate("Dialog", "分段(start,stop,IF,N,avg):"))
        self.btn_addSeg.setText(_translate("Dialog", "Add Seg."))
        self.btn_delSeg.setText(_translate("Dialog", "Del Seg."))
        self.pushButton_path.setText(_translate("Dialog", "路径..."))
        self.pushButton_save.setText(_translate("Dialog", "保存"))
        self.pushButton_start.setText(_translate("Dialog", "开始"))
        self.pushButton_quit.setText(_translate("Dialog", "退出"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
