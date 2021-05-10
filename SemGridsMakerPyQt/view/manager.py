# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:23:54 2021

@author: gelias
"""

from maker import Maker
from arduino import Arduino

class Manager():
    def __init__(self):
        self.maker = Maker()
        self.arduino =Arduino()
        self.myCurrentGrid=None
    
    def addSemGrid(self,name,seq,desc):
        for grid in self.maker.mesSemGrids:
            if (grid.name == name):
                print('SemGrid deja existente')
                return
        self.maker.addSemGrids(name,seq,desc)
    
    def deleteSemGrid(self,name):
        grid=self.searchSemGrids(name)
        # if(grid==False):
        #     print('SemGrid non trouve')
        #     return
        index = self.maker.mesSemGrids.index(grid)
        self.maker.deleteSemGrid(index)
        
    def showSemGrids(self):
        self.maker.showListGrids()
    
    def searchSemGrids(self,name):
        for grid in self.maker.mesSemGrids:
            if (grid.name == name):
                return grid
        return False
    
    def getStepFromGrid(self,grid):
        tabStep = []
        for step in grid.sequence:
            tabStep.append(step[0])
        return tabStep
    
    def getLapFromGrid(self,grid):
        tabLaps = []
        for step in grid.sequence:
            tabLaps.append(step[1])
        return tabLaps

    def setCurrentGrid(self,grid):
        self.myCurrentGrid=grid
        
    def getMyCurrentGrid(self):
        return self.myCurrentGrid
    
    def connectArduino(self):
        portCom=self.maker.get_portCom()
        
        self.arduino.connect(portCom)
        
    def sendDataArduino(self,gap,index,tab1,tab2):
        chain = str(index)
        chain = chain+'/'+str(gap)
        for elem in tab1:
            chain = chain+'/'+str(elem)
        for elem in tab2:
            chain = chain+'/'+str(elem)
        self.arduino.sendValue(chain) 
            
    def receiveValueArduino(self):
        self.arduino.receivevalue()
    
    def closeArduino(self):
        self.arduino.close()
        
    
    
    
    
    
    