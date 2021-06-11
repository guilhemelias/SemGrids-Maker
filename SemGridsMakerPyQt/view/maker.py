# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:00:27 2021

@author: gelias
"""

from semGrid import SemGrid

class Maker():
    """
    A class with the list of grids, the port Com and the gap
    """
    
    def __init__(self):
        """
        The Maker constructor with the list of grids, the portCom to communicate with arduino,
        and the gap, which is the distance of the sring position at the beginning of the program

        """
        self.mesSemGrids = []
        self.portCom=None
        self.gap=None



    def get_portCom(self):
        """
        The port COM getter
        """
        return self.portCom
      
    def set_portCom(self, com):
        """
        The port COM setter
        """
        self.portCom = com
        
    def get_gap(self):
        """
        The gap getter
        """
        return self.gap
      
    def set_gap(self, gap):
        """
        The gap setter
        """
        self.gap = gap  
        
    
        
        
        
    def addSemGrids(self,name,lien,desc):
        """
        A fonction called by the manager, adding a new SemGrid to the list
        """
        self.mesSemGrids.append(SemGrid(name,lien,desc))
    
    def deleteSemGrid(self,index):
        """
        A fonction called by the manager, zhich delete an existing SemGrid of the list
        """
        self.mesSemGrids.pop(index)
    