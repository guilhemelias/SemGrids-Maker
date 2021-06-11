# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: gelias
"""
import sys
import serial
import pickle
import re 
import time
import json

from arduino import Arduino
from manager import Manager
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets



from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QLabel,QListWidgetItem, QListWidget, QAction



class MainWindows(QMainWindow):
    def __init__(self,mgr):
        super(MainWindows,self).__init__()     
        loadUi("viewUi/main_windows.ui",self)      
        self.setWindowTitle("Ma fenetre")
        self.manager = mgr
        
        self.editCom.setText(self.manager.maker.get_portCom())
        self.customButton.clicked.connect(self.customButtonClicked)
        self.listProgramme.itemSelectionChanged.connect(self.progammeSelec)
        for grid in self.manager.maker.mesSemGrids:
            self.listProgramme.addItem(grid.name)
        

    def customButtonClicked(self):
        if(self.editCom.toPlainText()==""):
             self.labelErrorCom.setText("ENTER A PORT COM")
             return
        else:
            self.manager.maker.set_portCom(self.editCom.toPlainText())
        custom=CustomDialog(self.manager)
        widget.addWidget(custom)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
        
    def progammeSelec(self):
        if(self.editCom.toPlainText()==""):
            self.labelErrorCom.setText("ENTER A PORT COM")
            return
        else:
            self.manager.maker.set_portCom(self.editCom.toPlainText())
        prgrmName = self.listProgramme.currentItem().text()
        grid=self.manager.searchSemGrids(prgrmName)
        self.manager.setCurrentGrid(grid)
        custom=CommonProgrammDialog(self.manager,grid)
        widget.addWidget(custom)
        widget.setCurrentIndex(widget.currentIndex()+1)





class ItemPropertyCustom(QWidget):
    def __init__(self,parent=None):
        super(ItemPropertyCustom,self).__init__(parent)
        loadUi("viewUi/propertiy_list_item.ui",self)
    def getText(self):
        return self.label.text()
        
       
class ItemPropertyDisplayCustom(QWidget):
    def __init__(self,seq,parent=None):
        super(ItemPropertyDisplayCustom,self).__init__(parent)
        self.seq=seq
        loadUi("viewUi/property_list_display_item.ui",self)
        self.labelDispalySteps.setText(str(seq[0]))
        self.labelDispalyLaps.setText(str(seq[1]))





class CommonProgrammDialog(QDialog):
    
    def __init__(self,mgr,grid):
        self.manager=mgr
        #self.manager.setCurrentGrid(grid)
        super(CommonProgrammDialog,self).__init__()
        loadUi("viewUi/common_programm_dialog.ui",self)
        self.labelDisplayProgrammName.setText(self.manager.getMyCurrentGrid().name)
        propertyGrid=self.manager.getMyCurrentGrid().sequence
        # self.manager.getStepFromGrid(self.manager.getMyCurrentGrid())
        # self.manager.getLapFromGrid(self.manager.getMyCurrentGrid())
        for seq in propertyGrid:
            myQListWidgetItem  = QListWidgetItem(self.listPropertiesLoaded)
            self.listPropertiesLoaded.addItem(myQListWidgetItem)
            myItemPropertyDisplayCustom = ItemPropertyDisplayCustom(seq)             
            myQListWidgetItem.setSizeHint(myItemPropertyDisplayCustom.minimumSizeHint())
            self.listPropertiesLoaded.setItemWidget(myQListWidgetItem, myItemPropertyDisplayCustom)
            
        self.editGap.setText(str(self.manager.maker.get_gap()))
        self.menuButton.clicked.connect(self.menuButtonClicked)
        self.deleteGridButton.clicked.connect(self.deleteGridButtonClicked)
        self.runCommonButton.clicked.connect(self.runCommonButtonClicked)
    
    def setList(self):
        pass
        
    def menuButtonClicked(self):
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def deleteGridButtonClicked(self):
        self.manager.deleteSemGrid(self.manager.getMyCurrentGrid().name)
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def runCommonButtonClicked(self):
        regex = re.search("^[1-9]\d*$", self.editGap.toPlainText())       
        if (regex):
          self.manager.maker.set_gap(self.editGap.toPlainText())
        else:
            self.editGap.clear()
            self.LabelErrorGap.setText('YOU MUST ENTER A NUMERIC VALUE')
            return
        tabSteps = self.manager.getStepFromGrid(self.manager.getMyCurrentGrid())
        tabLaps =self.manager.getLapFromGrid(self.manager.getMyCurrentGrid())
        
        self.manager.connectArduino()
        time.sleep(2)

        self.manager.sendDataArduino(self.manager.maker.get_gap(),len(tabSteps),tabSteps,tabLaps)
        time.sleep(5)

        # print(self.manager.arduino.ser.readline().decode('ISO-8859-1'))

        self.manager.closeArduino()
        
       
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)

 
        
class CustomDialog(QDialog):
    def __init__(self,mgr):
        self.manager=mgr
        super(CustomDialog,self).__init__()
        loadUi("viewUi/custom.ui",self)
        
        myItemPropertyCustom = ItemPropertyCustom()
        myQListWidgetItem  = QListWidgetItem(self.listProperties)
        self.listProperties.addItem(myQListWidgetItem)
        myQListWidgetItem.setSizeHint(myItemPropertyCustom.minimumSizeHint())
        
        self.editGap.setText(self.manager.maker.get_gap())
        
        self.listProperties.setItemWidget(myQListWidgetItem, myItemPropertyCustom)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.runCustomButton.clicked.connect(self.runCustomButtonClicked)
        
    def menuButtonClicked(self):
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addButtonClicked(self):
        myItemPropertyCustom = ItemPropertyCustom()
        myQListWidgetItem  = QListWidgetItem(self.listProperties)
        self.listProperties.addItem(myQListWidgetItem)
        myQListWidgetItem.setSizeHint(myItemPropertyCustom.minimumSizeHint())
        self.listProperties.setItemWidget(myQListWidgetItem, myItemPropertyCustom)
        
    def deleteButtonClicked(self):
        items=self.listProperties.selectedItems()
        for item in items:
              widget = self.listProperties.itemWidget(item)
              self.listProperties.removeItemWidget(item)
              self.listProperties.takeItem(self.listProperties.row(item))
              widget.deleteLater()     

    def runCustomButtonClicked(self):
        regex = re.search("^[1-9]\d*$", self.editGap.toPlainText())       
        if (regex):
          self.manager.maker.set_gap(self.editGap.toPlainText())
        else:
            self.editGap.clear()
            self.LabelErrorGap.setText('YOU MUST ENTER A NUMERIC VALUE')
            return
        nbRow = self.listProperties.count()
        sequence = []
        if nbRow <= 0:
            print('REMPLIR CASES')
        i=0
        while i < nbRow:
            dirname = self.listProperties.itemWidget(self.listProperties.item(i))  
            regexStep = re.search("^[1-9]\d*$", dirname.lapsLabel.toPlainText())
            regexLabel = re.search("^[1-9]\d*$", dirname.stepslabel.toPlainText())
            if( not regexStep or  not regexLabel):
                self.labelError.setText('YOU MUST ENTER FLOAT STEPS AND NUMERIC LAPS')
                return
            self.labelError.clear()
            sequence.append([float(dirname.stepslabel.toPlainText()),int(dirname.lapsLabel.toPlainText())])
            i=i+1
        
        custom=GridCreateDialog(self.manager,sequence)
        custom.exec_()
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)



class GridCreateDialog(QDialog):
    def __init__(self,mgr,sequence):
        self.manager=mgr
        super(GridCreateDialog,self).__init__()
        loadUi("viewUi/grid_create_dialog.ui",self)
        self.sequence=sequence
        self.registerAndRunButton.clicked.connect(self.registerAndRunButtonClicked)
        self.passAndRunButton.clicked.connect(self.passAndRunButtonClicked)
    
    def registerAndRunButtonClicked(self):
        name=self.editName.toPlainText()
        description=self.editDesc.toPlainText()
        self.manager.addSemGrid(name,self.sequence,description)
        self.close()
        
    def passAndRunButtonClicked(self):
        self.close()


class MainWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super(MainWidget,self).__init__()           
        self.manager = Manager()
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
        with open('bin/data.bin','wb') as fh:
            pickle.dump(self.manager,fh,pickle.HIGHEST_PROTOCOL)
        event.accept()
        
    def toJson(self):
        with open('bin/data.bin', 'rb') as fh:
            data = pickle.load(fh)
        self.manager = data
        # with open('json/data.json') as json_file:
        #     data = json.load(json_file)
        # print(data)
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
        # self.manager.addSemGrid(name,seq,desc)
        # print(data['maker']['portCom'])
        # self.manager.maker.set_portCom(data['maker']['portCom'])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())