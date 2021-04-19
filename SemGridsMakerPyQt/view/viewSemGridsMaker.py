# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: gelias
"""
import sys
import os
import serial
import time

from arduino import Arduino
from manager import Manager
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QLabel


class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows,self).__init__()     
        loadUi("viewUi/main_windows.ui",self)      
        self.setWindowTitle("Ma fenetre")
        self.manager = Manager()
        self.regularStepButton.clicked.connect(self.regularStepButtonClicked)
        self.linacButton.clicked.connect(self.linac3ButtonClicked)
        self.customButton.clicked.connect(self.customButtonClicked)
        
    def regularStepButtonClicked(self):
        self.manager.maker.set_portCom(self.editCom.toPlainText())
        rsd=RegularStepDialog(self.manager)
        widget.addWidget(rsd)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def linac3ButtonClicked(self):
        self.manager.maker.set_portCom(self.editCom.toPlainText())
        linac=Linac3Dialog(self.manager)
        widget.addWidget(linac)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def customButtonClicked(self):
        self.manager.maker.set_portCom(self.editCom.toPlainText())
        custom=CustomDialog(self.manager)
        widget.addWidget(custom)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
        
        
        

class RegularStepDialog(QDialog):
    def __init__(self,mgr):
        self.manager=mgr
        print(self.manager.maker.get_portCom())
        super(RegularStepDialog,self).__init__()
        loadUi("viewUi/regular_step.ui",self)
        self.label.setText(self.manager.maker.get_portCom())
        self.menuButton.clicked.connect(self.menuButtonClicked)
        self.runRegularStepButton.clicked.connect(self.runRegularStepButtonButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def runRegularStepButtonButtonClicked(self):
        ar = Arduino(self.manager.maker.get_portCom())
        ar.initUART()




class Linac3Dialog(QDialog):
    def __init__(self,mgr):
        self.manager=mgr
        super(Linac3Dialog,self).__init__()
        loadUi("viewUi/linac_3.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
 
        
class CustomDialog(QDialog):
    def __init__(self,mgr):
        self.manager=mgr
        super(CustomDialog,self).__init__()
        loadUi("viewUi/custom.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)












# app = QApplication.instance() 
# if not app:
#     app = QApplication(sys.argv)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw=MainWindows()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mw)
    widget.setFixedHeight(400)
    widget.setFixedWidth(800)
    widget.setWindowTitle("SEMGrids Maker")
    widget.show()
    sys.exit(app.exec_())