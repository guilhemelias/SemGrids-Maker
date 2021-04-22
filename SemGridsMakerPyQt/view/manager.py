# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:23:54 2021

@author: gelias
"""

from maker import Maker
from json import JSONEncoder
from semGrid import SemGrid
import json

class Manager():
    def __init__(self):
        self.maker = Maker()
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
    def setCurrentGrid(self,grid):
        self.myCurrentGrid=grid
        
    def getMyCurrentGrid(self):
        return self.myCurrentGrid
    
    
    
    
    
    
    