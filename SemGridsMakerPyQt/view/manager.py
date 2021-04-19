# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:23:54 2021

@author: gelias
"""

from maker import Maker

class Manager:
    def __init__(self):
        self.maker = Maker()
    
    def addSemGrid(self,name,lien,desc):
        for grid in self.mesSemGrids:
            if (grid.name == name):
                print('SemGrid deja existente')
                return
        self.maker.addSemGrids(name,lien,desc)
    
    def deleteSemGrid(self,semGrid):
        for grid in self.mesSemGrids:
            if(grid == semGrid):
                index = self.mesSemGrids.index(grid)
        if index is None:
            print('SemGrid non trouve')
            return
        self.maker.deleteSemGrid(index)
        
    