# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:23:54 2021

@author: gelias
"""

from maker import Maker
from arduino import Arduino

class Manager():
    """
    Manager of the model. It is called by the view. It makes the link between the model and the view 
    """
    def __init__(self):
        """
        The cinstructor zhich instanciate the maker and the arduino part

        """
        self.maker = Maker()
        self.arduino =Arduino()
        self.myCurrentGrid=None
    
    def addSemGrid(self,name,seq,desc):
        """
        A fonction to add a Grid to the model
        """
        for grid in self.maker.mesSemGrids:
            if (grid.name == name):
                return False
        self.maker.addSemGrids(name,seq,desc)
    
    def deleteSemGrid(self,name):
        """
        A fonction to delete a Grid to the model
        """
        grid=self.searchSemGrids(name)
        index = self.maker.mesSemGrids.index(grid)
        self.maker.deleteSemGrid(index)
        
    
    def searchSemGrids(self,name):
        """
        A fonction to search a Grid to the list of saved grid
        """
        for grid in self.maker.mesSemGrids:
            if (grid.name == name):
                return grid
        return False
    
    def getStepFromGrid(self,grid):
        """
        A fonction to get the steps from a grid
        """
        tabStep = []
        for step in grid.sequence:
            tabStep.append(step[0])
        return tabStep
    
    def getLapFromGrid(self,grid):
        """
        A fonction to get the laps from a grid
        """
        tabLaps = []
        for step in grid.sequence:
            tabLaps.append(step[1])
        return tabLaps

    def setCurrentGrid(self,grid):
        """
        A fonction to set the current grid
        """
        self.myCurrentGrid=grid
        
    def getMyCurrentGrid(self):
        """
        A fonction to get the current grid, to get his informations
        """
        return self.myCurrentGrid
    
    
    def connectArduino(self):
        """
        A fonction to connect to arduino using the port COM

        """
        
        portCom=self.maker.get_portCom()
        
        self.arduino.connect(portCom)
        
    def sendDataPatternArduino(self,gap,index,tab1,tab2):
        """
        A fonction to send data to arduino for running programm

        """
        chain = "pattern"
        chain = chain+'/'+str(index)
        chain = chain+'/'+str(gap)
        for elem in tab1:
            chain = chain+'/'+str(elem)
        for elem in tab2:
            chain = chain+'/'+str(elem)
        self.arduino.sendValue(chain) 
        
        
    def sendDataCCWArduino(self,gap,direction):
        """
        A fonction to send data to arduino for running programm

        """
        chain = "cw"
        chain = chain+'/'+direction
        chain = chain+'/'+str(gap)
        self.arduino.sendValue(chain) 
            
    def receiveValueArduino(self):
        """
        A fonction to recive data from arduino

        """
        self.arduino.receivevalue()
    
    def closeArduino(self):
        """
        A fonction to discconnect from arduino 

        """
        self.arduino.close()
        
    
    
    
    
    
    