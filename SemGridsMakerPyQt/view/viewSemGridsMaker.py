# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: gelias
"""
import sys
import os
import serial
import time

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow


class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows,self).__init__()     
        loadUi("viewUi/main_windows.ui",self)      
        self.setWindowTitle("Ma fenetre")
        self.regularStepButton.clicked.connect(self.regularStepButtonClicked)
        self.linacButton.clicked.connect(self.linac3ButtonClicked)
        self.customButton.clicked.connect(self.customButtonClicked)
        
    def regularStepButtonClicked(self):
        rsd=RegularStepDialog()
        widget.addWidget(rsd)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def linac3ButtonClicked(self):
        linac=Linac3Dialog()
        widget.addWidget(linac)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def customButtonClicked(self):
        custom=CustomDialog()
        widget.addWidget(custom)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
        
        
        

class RegularStepDialog(QDialog):
    def __init__(self):
        super(RegularStepDialog,self).__init__()
        loadUi("viewUi/regular_step.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        self.runRegularStepButton.clicked.connect(self.runRegularStepButtonButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def runRegularStepButtonButtonClicked(self):
        ar = Arduino()
        ar.initUART()


class Linac3Dialog(QDialog):
    def __init__(self):
        super(Linac3Dialog,self).__init__()
        loadUi("viewUi/linac_3.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
 
        
class CustomDialog(QDialog):
    def __init__(self):
        super(CustomDialog,self).__init__()
        loadUi("viewUi/custom.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)





class Arduino:
    def __init__(self):
        self.initUART('COM3')  # En windows de COM4 a COM 30
   
    def initUART(self,port):
    		baudrate = 9600	
    		try: 	
    			self.ser = serial.Serial(
    				port,
    				baudrate,
    				timeout=1,
    				# parity=serial.PARITY_NONE,
    				# stopbits=serial.STOPBITS_ONE,
    				# bytesize=serial.EIGHTBITS
    			)
    		except serial.SerialException as e:
    			print("port inconnu" % port)
    			self.ser.close()
    			sys.exit(-1)






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