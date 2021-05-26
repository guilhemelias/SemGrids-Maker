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
from pickleManager import PickleManager
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets



from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QLabel,QListWidgetItem, QListWidget, QAction




class MainWidget(QtWidgets.QStackedWidget):
    """
     The main widget of the software. It instanciate the model, the mainWindow with different properties and 
     it call the pickleManager to save and load the model
     
    """
    def __init__(self):
        super(MainWidget,self).__init__()           
        self.manager = Manager()
        self.pickleManager= PickleManager()
        #loading model
        self.toPickle()
        
        mw=MainWindows(self.manager)
        self.addWidget(mw)
        self.setFixedHeight(400)
        self.setFixedWidth(600)
        self.setWindowTitle("SEMGrids Maker")
        
        #closing app event to call the model saver.        
        quit = QAction(self)
        quit.triggered.connect(self.closeEvent)
        self.addAction(quit)

    def closeEvent(self, event):
        """        
        save model
        
        """
        self.pickleManager.savePickle(self.manager)
        event.accept()
        
    def toPickle(self):
        """
        load model

        """
        
        self.manager = self.pickleManager.loadPickle()

        
        
        

class MainWindows(QMainWindow):
    """
    The main window, it instanciate the view, and use the model to use/delete/create semgrids
    
    """
    def __init__(self,mgr):
        super(MainWindows,self).__init__()     
        loadUi("viewUi/main_windows.ui",self)      
        self.setWindowTitle("Ma fenetre")
        self.manager = mgr
        
        self.editCom.setText(self.manager.maker.get_portCom())
        self.customButton.clicked.connect(self.customButtonClicked)
        self.listProgramme.itemSelectionChanged.connect(self.progammeSelec)
        self.slideButton.clicked.connect(self.slideButtonClicked)
        
        #adding semGrids to the listView
        for grid in self.manager.maker.mesSemGrids:
            self.listProgramme.addItem(grid.name)
        

    def customButtonClicked(self):
        """
        A fonction to run a non existing semGrid
        """

        if(self.editCom.toPlainText()==""):
             self.labelErrorCom.setText("ENTER A PORT COM")
             return
        else:
            self.manager.maker.set_portCom(self.editCom.toPlainText())
        custom=CustomDialog(self.manager)
        widget.addWidget(custom)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
        
    def progammeSelec(self):
        """
        A fonction to call an existing semGrid, when clicking it in the list view

        """

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

    def slideButtonClicked(self):
        """
        A fonction to run a slide movement program
        """
        slideDialog=SlideMovementDialog(self.manager)
        slideDialog.exec_()





class CommonProgrammDialog(QDialog):
    """
    The  Dialog Window to run an existing semGrid. The grid can be delete.
    
    When arriving on this dialog, the user can look at the properties of the grid. 
    Properties are made by group of two: Step and laps. 
    There cant be a step without lap and vice versa. 
    
    """
    def __init__(self,mgr,grid):
        self.manager=mgr
        super(CommonProgrammDialog,self).__init__()
        loadUi("viewUi/common_programm_dialog.ui",self)
        self.labelDisplayProgrammName.setText(self.manager.getMyCurrentGrid().name)
        
        #properties part loading
        propertyGrid=self.manager.getMyCurrentGrid().sequence
        for seq in propertyGrid:
            myQListWidgetItem  = QListWidgetItem(self.listPropertiesLoaded)
            self.listPropertiesLoaded.addItem(myQListWidgetItem)
            myItemPropertyDisplayCustom = ItemPropertyDisplayCustom(seq)             
            myQListWidgetItem.setSizeHint(myItemPropertyDisplayCustom.minimumSizeHint())
            self.listPropertiesLoaded.setItemWidget(myQListWidgetItem, myItemPropertyDisplayCustom)
            
        self.editGap.setText(str(self.manager.maker.get_gap()))
        
        try:
            desc = self.manager.getMyCurrentGrid().description
        except:
            desc="No description"
        
        self.labelDesc.setText(desc)
        self.menuButton.clicked.connect(self.menuButtonClicked)
        self.deleteGridButton.clicked.connect(self.deleteGridButtonClicked)
        self.runCommonButton.clicked.connect(self.runCommonButtonClicked)
    

        
    def menuButtonClicked(self):
        """
        A fonction to go back to the menu (the MainWindow)

        """
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def deleteGridButtonClicked(self):
        """
        A fonction to delete the semGrids qnd go back to the menu 

        """
        
        self.manager.deleteSemGrid(self.manager.getMyCurrentGrid().name)
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def runCommonButtonClicked(self):
        """
        A fonction to run the program on the winding machine. Before that, it will check 
        that the gap is a numeric value. Afetr, it will connect toi the arduino and send data 
        to run the wished programm.

        """
        regex = re.search("^[0-9]\d*$", self.editGap.toPlainText())       
        if (regex):
          self.manager.maker.set_gap(self.editGap.toPlainText())
        else:
            self.editGap.clear()
            self.LabelErrorGap.setText('YOU MUST ENTER A NUMERIC VALUE')
            return
        tabSteps = self.manager.getStepFromGrid(self.manager.getMyCurrentGrid())
        tabLaps =self.manager.getLapFromGrid(self.manager.getMyCurrentGrid())
        
        dist=  self.manager.maker.get_initialReturn() 
        for step,lap in zip(tabSteps,tabLaps):
            dist+=step*lap
        dist+=float(self.manager.maker.get_gap())
        print(dist)
        self.manager.maker.set_initialReturn(dist) 
        
        self.manager.connectArduino()
        time.sleep(2)
        # print(self.manager.arduino.ser.readline().decode('ISO-8859-1'))
        
        self.manager.sendDataPatternArduino(self.manager.maker.get_gap(),len(tabSteps),tabSteps,tabLaps)
        time.sleep(5)

        # self.manager.receiveValueArduino()
        
        self.manager.closeArduino()
             
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)

 
        
class CustomDialog(QDialog):
    """
    The  Dialog Window to run a non existing semGrid. The grid can be saved to the model.    
    When arriving on this dialog, the user can add and delete the properties of the grid. 
    Properties are made by group of two: Step and laps. 
    There cant be a step without lap and vice versa. 
    """
    def __init__(self,mgr):
        self.manager=mgr
        super(CustomDialog,self).__init__()
        loadUi("viewUi/custom.ui",self)
        
        
        #customing properties part loading using a ListView with custom items 
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
        """
        A fonction to go back to the menu (the MainWindow)

        """
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addButtonClicked(self):
        """
        A fonction to add an item custom off the listView

        """
        myItemPropertyCustom = ItemPropertyCustom()
        myQListWidgetItem  = QListWidgetItem(self.listProperties)
        self.listProperties.addItem(myQListWidgetItem)
        myQListWidgetItem.setSizeHint(myItemPropertyCustom.minimumSizeHint())
        self.listProperties.setItemWidget(myQListWidgetItem, myItemPropertyCustom)
        
    def deleteButtonClicked(self):
        """
        A fonction to delete a selected item custom off the listView

        """
        items=self.listProperties.selectedItems()
        for item in items:
              widget = self.listProperties.itemWidget(item)
              self.listProperties.removeItemWidget(item)
              self.listProperties.takeItem(self.listProperties.row(item))
              widget.deleteLater()     

    def runCustomButtonClicked(self):
        """
        A fonction to run the program on the winding machine. Before that, it will check 
        that the gap is a numeric value. It will propose you with a new window to save it or not.
        After, it will connect toi the arduino and send data 
        to run the wished programm.

        """
        regex = re.search("^[0-9]\d*$", self.editGap.toPlainText())       
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
            regexLabel = re.search("^[0-9]\d*$", dirname.stepslabel.toPlainText())
            if( not regexStep or  not regexLabel):
                self.labelError.setText('YOU MUST ENTER FLOAT STEPS AND NUMERIC LAPS')
                return
            self.labelError.clear()
            # tabSteps=float(dirname.stepslabel.toPlainText())
            # tabLaps=int(dirname.lapsLabel.toPlainText())
            sequence.append([float(dirname.stepslabel.toPlainText()),int(dirname.lapsLabel.toPlainText())])
            i=i+1
        
        custom=GridCreateDialog(self.manager,sequence)
        custom.exec_()
        mw=MainWindows(self.manager)
        widget.addWidget(mw)
        widget.setCurrentIndex(widget.currentIndex()+1)






class GridCreateDialog(QDialog):
    """
 The Dialog to decide if the user save or not a custom grid before running it
    """
    def __init__(self,mgr,sequence):
        self.manager=mgr
        super(GridCreateDialog,self).__init__()
        loadUi("viewUi/grid_create_dialog.ui",self)
        self.sequence=sequence
        self.registerAndRunButton.clicked.connect(self.registerAndRunButtonClicked)
    

    def registerAndRunButtonClicked(self):
        """
        User decide to save it

        """
        name=self.editName.toPlainText()
        description=self.editDesc.toPlainText()
        res = self.manager.addSemGrid(name,self.sequence,description)
        if(res==False):
            self.labelError.setText('SEMGRID DEJA EXISTANTE')
            return
        self.close()
        
    
        

class SlideMovementDialog(QDialog):
    """
 The Dialog to decide if the user save or not a custom grid before running it
    """
    def __init__(self,mgr):
        self.manager=mgr
        super(SlideMovementDialog,self).__init__()
        loadUi("viewUi/ccw_dialog.ui",self)
        self.exitButton.clicked.connect(self.exitButtonClicked)
        self.slideRightButton.clicked.connect(self.slideRightButtonClicked)
        self.slideLeftButton.clicked.connect(self.slideLeftButtonClicked)

    def exitButtonClicked(self):
        """
        User decide to exit

        """
        self.close()
        
    def slideRightButtonClicked(self):
        regex = re.search("^[1-9]\d*$", self.editSlideMovement.toPlainText())       
        if (regex):
          self.manager.connectArduino()
          time.sleep(2)
          self.manager.sendDataCCWArduino(self.editSlideMovement.toPlainText(),'R')          
          time.sleep(5)
          self.manager.closeArduino()
          self.close()
          
        else:
            self.editSlideMovement.clear()
            self.LabelErrorSlideMovement.setText('YOU MUST ENTER A POSITIVE NUMERIC VALUE')
        
        
        
        
        
    
    def slideLeftButtonClicked(self):
        regex = re.search("^[1-9]\d*$", self.editSlideMovement.toPlainText())       
        if (regex):
          self.manager.connectArduino()
          time.sleep(2)
          self.manager.sendDataCCWArduino(self.editSlideMovement.toPlainText(),'L')          
          time.sleep(5)
          self.manager.closeArduino()
          self.close()
        else:
            self.editSlideMovement.clear()
            self.LabelErrorSlideMovement.setText('YOU MUST ENTER A POSITIVE NUMERIC VALUE')





class ItemPropertyCustom(QWidget):
    """
    The custom item to add properties to the custom programm
    """
    def __init__(self,parent=None):

        super(ItemPropertyCustom,self).__init__(parent)
        loadUi("viewUi/propertiy_list_item.ui",self)
    def getText(self):
        return self.label.text()
        
       
class ItemPropertyDisplayCustom(QWidget):
    """
    The custom item to display properties of a saved programm
    """
    def __init__(self,seq,parent=None):
        super(ItemPropertyDisplayCustom,self).__init__(parent)
        self.seq=seq
        loadUi("viewUi/property_list_display_item.ui",self)
        self.labelDispalySteps.setText(str(seq[0]))
        self.labelDispalyLaps.setText(str(seq[1]))






if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())