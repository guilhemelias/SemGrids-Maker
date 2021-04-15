# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow


class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows,self).__init__()     
        loadUi("main_windows.ui",self)      
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
        loadUi("regular_step.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Linac3Dialog(QDialog):
    def __init__(self):
        super(Linac3Dialog,self).__init__()
        loadUi("linac_3.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
 
        
class CustomDialog(QDialog):
    def __init__(self):
        super(CustomDialog,self).__init__()
        loadUi("custom.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows()
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)



app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)

widget=QtWidgets.QStackedWidget()
mw=MainWindows()

widget.addWidget(mw)
widget.setFixedHeight(400)
widget.setFixedWidth(800)
widget.setWindowTitle("SEMGrids Maker")
widget.show()


    
# widget=QtWidgets.QStackedWidget()
# mw=MainWindows()
# widget.addWigdet(mw)
# widget.show()

app.exec_()

