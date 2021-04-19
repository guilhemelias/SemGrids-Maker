# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:23:54 2021

@author: gelias
"""

from maker import Maker

class Manager:
    def __init__(self):
        self.maker = Maker()
    
    def addSemGrids(self,name,sequence,lien,desc):
        for grid in self.mesSemGrids:
            if (grid.name == name):
                print('SemGrid deja existente')
                return
        self.maker.addSemGrids(name,sequence,lien,desc)
    
    def deleteSemGrid(self,SemGrid):
        for grid in self.mesSemGrids:
            if(grid == SemGrid):
                index = self.mesSemGrids.index(grid)
        if index is None:
            print('SemGrid non trouve')
            return
        self.maker.deleteSemGrid(index)
        
    