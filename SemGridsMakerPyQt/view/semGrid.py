# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 09:13:54 2021

@author: gelias
"""
from json import JSONEncoder

import json

class SemGrid:
    def __init__(self,name,seq,desc):
        self.name = name
        self.sequence = seq
        self.descritpion = desc

    def __eq__(self, other):
        return (self.name  == other.name)
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
   
