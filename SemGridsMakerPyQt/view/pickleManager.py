# -*- coding: utf-8 -*-
"""
Created on Tue May 18 09:19:33 2021

@author: gelias
"""

import pickle


class PickleManager():

    def savePickle(self,manager):
        with open('bin/data.bin','wb') as fh:
            pickle.dump(manager,fh,pickle.HIGHEST_PROTOCOL)
        pass
    def loadPickle(self):
        with open('bin/data.bin', 'rb') as fh:
             data = pickle.load(fh)
        return data
        
    
    
    
    
    
    
    
    
    
    
    
    
# with open('json/data.json') as json_file:
        #     data = json.load(json_file)
        # print(data)
        # for grid in data['maker']['mesSemGrids']:
        #     seq = []
        #     print(grid) #une grid
        #     desc=grid['descritpion']
        #     #print(grid['descritpion'])
        #     name=grid['name']
        #     #print(grid['name'])
        #     for att in grid['sequence']:
        #         seq.append(att)
        #         print(seq)
        # self.manager.addSemGrid(name,seq,desc)
        # print(data['maker']['portCom'])
        # self.manager.maker.set_portCom(data['maker']['portCom'])