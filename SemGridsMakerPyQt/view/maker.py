# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:00:27 2021

@author: gelias
"""

from semGrid import SemGrid

class Maker:
    def __init__(self):
        self.mesSemGrids = []

    # getter method
    def get_portCom(self):
        return self.portCom
      
    # setter method
    def set_portCom(self, com):
        self.portCom = com
        
    def addSemGrids(self,name,lien,desc):
        self.mesSemGrids.append(SemGrid(name,lien,desc))
    
    def deleteSemGrid(self,index):
        self.mesSemGrids.pop(index)
        
    def showListGrids(self):
        for grid in self.mesSemGrids:
            print( grid.name, grid.sequence,grid.lienImage, grid.descritpion, sep =' ' )
        