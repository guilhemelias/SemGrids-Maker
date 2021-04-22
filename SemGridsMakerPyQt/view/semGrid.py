# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:13:54 2021

@author: gelias
"""


class SemGrid:
    def __init__(self,name,seq,desc):
        self.name = name
        self.sequence = seq
        self.descritpion = desc

    def __eq__(self, other):
        return (self.name  == other.name)
    # def __str__(self):
    #     return f'{self.name}   |   {self.descritpion}'
   
