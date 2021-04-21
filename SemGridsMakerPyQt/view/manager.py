# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:23:54 2021

@author: gelias
"""

from maker import Maker
from json import JSONEncoder
import json

class Manager:
    def __init__(self):
        self.maker = Maker()
    
    def addSemGrid(self,name,seq,desc):
        for grid in self.maker.mesSemGrids:
            if (grid.name == name):
                print('SemGrid deja existente')
                return
        self.maker.addSemGrids(name,seq,desc)
    
    def deleteSemGrid(self,semGrid):
        for grid in self.mesSemGrids:
            if(grid == semGrid):
                index = self.mesSemGrids.index(grid)
        if index is None:
            print('SemGrid non trouve')
            return
        self.maker.deleteSemGrid(index)
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
    