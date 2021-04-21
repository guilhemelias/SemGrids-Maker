# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: gelias
"""
import sys
import os
import serial
import time
import json
import pickle
from json import dump
from io import StringIO
from PyQt5 import Qt
from arduino import Arduino
from manager import Manager
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtGui
from semGrid import SemGrid



from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QLabel,QListWidgetItem, QListWidget, QAction
testlist = ["RegularStep", "Linac3", "Custom"]






class MainWindows(QMainWindow):
    def __init__(self,mgr):
        super(MainWindows,self).__init__()     
        loadUi("viewUi/main_windows.ui",self)      
        self.setWindowTitle("Ma fenetre")
        self.manager = mgr
        self.editCom.setPlaceholderText(self.manager.maker.get_portCom())
        # self.regularStepButton.clicked.connect(self.regularStepButtonClicked)
        # self.linacButton.clicked.connect(self.linac3ButtonClicked)
        # self.customButton.clicked.connect(self.customButtonClicked)
        self.listProgramme.itemSelectionChanged.connect(self.progammeSelec)
        for test in testlist:
            obj = QListWidgetItem(self.listProgramme)
            obj.setText(test)
            
        
    # def regularStepButtonClicked(self):
    #     self.manager.maker.set_portCom(self.editCom.toPlainText())
    #     rsd=RegularStepDialog(self.manager)
    #     widget.addWidget(rsd)
    #     widget.setCurrentIndex(widget.currentIndex()+1)
    
    # def linac3ButtonClicked(self):
    #     self.manager.maker.set_portCom(self.editCom.toPlainText())
    #     linac=Linac3Dialog(self.manager)
    #     widget.addWidget(linac)
    #     widget.setCurrentIndex(widget.currentIndex()+1)
    
    # def customButtonClicked(self):
    #     self.manager.maker.set_portCom(self.editCom.toPlainText())
    #     custom=CustomDialog(self.manager)
    #     widget.addWidget(custom)
    #     widget.setCurrentIndex(widget.currentIndex()+1)
    
        
    def progammeSelec(self):
        if(self.listProgramme.currentItem().text()=='RegularStep'):
            self.manager.maker.set_portCom(self.editCom.toPlainText())
            rsd=RegularStepDialog(self.manager)
            widget.addWidget(rsd)
            widget.setCurrentIndex(widget.currentIndex()+1)
            
        elif(self.listProgramme.currentItem().text()=='Linac3'):
            self.manager.maker.set_portCom(self.editCom.toPlainText())
            linac=Linac3Dialog(self.manager)
            widget.addWidget(linac)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.manager.maker.set_portCom(self.editCom.toPlainText())
            custom=CustomDialog(self.manager)
            widget.addWidget(custom)
            widget.setCurrentIndex(widget.currentIndex()+1)
        
        
class ItemPropertyCustom(QWidget):
    def __init__(self,parent=None):
        super(ItemPropertyCustom,self).__init__(parent)
        loadUi("viewUi/propertiy_list_item.ui",self)
    def getText(self):
        return self.label.text()
        
       
        
        

class RegularStepDialog(QDialog):
    def __init__(self,mgr):
        self.manager=mgr
        #print(self.manager.maker.get_portCom())
        super(RegularStepDialog,self).__init__()
        loadUi("viewUi/regular_step.ui",self)
       # self.label.setText(self.manager.maker.get_portCom())
        self.menuButton.clicked.connect(self.menuButtonClicked)
        self.runRegularStepButton.clicked.connect(self.runRegularStepButtonButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def runRegularStepButtonButtonClicked(self):
        ar = Arduino()
        ar.initUART(self.manager.maker.get_portCom())




class Linac3Dialog(QDialog):
    def __init__(self,mgr):
        self.manager=mgr
        super(Linac3Dialog,self).__init__()
        loadUi("viewUi/linac_3.ui",self)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
 
        
class CustomDialog(QDialog):
    def __init__(self,mgr):
        self.manager=mgr
        super(CustomDialog,self).__init__()
        loadUi("viewUi/custom.ui",self)
        myItemPropertyCustom = ItemPropertyCustom()
        # Create QListWidgetItem
        myQListWidgetItem  = QListWidgetItem(self.listProperties)
        # Set size hint
        self.listProperties.addItem(myQListWidgetItem)
        myQListWidgetItem.setSizeHint(myItemPropertyCustom.minimumSizeHint())
        # Add QListWidgetItem into QListWidget
        
        self.listProperties.setItemWidget(myQListWidgetItem, myItemPropertyCustom)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.runCustomButton.clicked.connect(self.runCustomButtonClicked)

        
    def menuButtonClicked(self):
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addButtonClicked(self):
        myItemPropertyCustom = ItemPropertyCustom()
        # Create QListWidgetItem
        myQListWidgetItem  = QListWidgetItem(self.listProperties)
        # Set size hint
        self.listProperties.addItem(myQListWidgetItem)
        myQListWidgetItem.setSizeHint(myItemPropertyCustom.minimumSizeHint())
        # Add QListWidgetItem into QListWidget      
        self.listProperties.setItemWidget(myQListWidgetItem, myItemPropertyCustom)
    
    def runCustomButtonClicked(self):
        nbFolder = self.listProperties.count()
        sequence = []
        if nbFolder > 0:
             i=0
        while i < nbFolder:
            #self.editCom.toPlainText()
            dirname = self.listProperties.itemWidget(self.listProperties.item(i))            
            sequence.append([int(dirname.stepslabel.toPlainText()),int(dirname.lapsLabel.toPlainText())])
            i=i+1
        print(sequence)    
        self.manager.addSemGrid('test',sequence,'test desc')
        self.manager.addSemGrid('test2',sequence,'test desc')



class MainWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super(MainWidget,self).__init__()           
        #self.manager = Manager()
        self.toJson()
        mw=MainWindows(self.manager)
        self.addWidget(mw)
        self.setFixedHeight(400)
        self.setFixedWidth(800)
        self.setWindowTitle("SEMGrids Maker")
        
        
        quit = QAction(self)
        quit.triggered.connect(self.closeEvent)
        self.addAction(quit)

    def closeEvent(self, event):
        #print(self.manager)
        # jsoned=pickle.dumps(self.manager,pickle.HIGHEST_PROTOCOL)
        # print(jsoned)
        # dejsoned=pickle.loads(jsoned)
        # dejsoned.maker.get_portCom()
        with open('bin/data.bin','wb') as fh:
            pickle.dump(self.manager,fh,pickle.HIGHEST_PROTOCOL)
        event.accept()
        
    def toJson(self):
        with open('bin/data.bin', 'rb') as fh:
            data = pickle.load(fh)
        print(data)
        self.manager = data
        # with open('json/data.json') as fh:
        #     data = json.load(fh)            
        # print(data['maker']['mesSemGrids']) 
        # for grid in data['maker']['mesSemGrids']:
        #     seq = []
        #     print(grid) #une grid
        #     desc=grid['descritpion']
        #     #print(grid['descritpion'])
        #     name=grid['name']
        #     #print(grid['name'])
        #     for att in grid['sequence']:
        #         seq.append(att)
        #         print(seq)
        #     self.manager.addSemGrid(name,seq,desc)
        # print(data['maker']['portCom'])
        # self.manager.maker.set_portCom(data['maker']['portCom'])        

# app = QApplication.instance() 
# if not app:
#     app = QApplication(sys.argv)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    # mw=MainWindows()
    # widget=QtWidgets.QStackedWidget()
    # widget.addWidget(mw)
    # widget.setFixedHeight(400)
    # widget.setFixedWidth(800)
    # widget.setWindowTitle("SEMGrids Maker")
    widget.show()
    sys.exit(app.exec_())