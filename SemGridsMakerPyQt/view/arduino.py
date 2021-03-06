# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 08:39:07 2021

@author: gelias
"""
import sys
import os
import serial
import time

class Arduino():
    def connect(self,port):
        baudrate = 2000000	
        
        try: 	
            self.ser = serial.Serial(
    				port,
    				baudrate
    			)
                
        except serial.SerialException as e:
            print("port inconnu" % port)
            self.ser.close()
            sys.exit(-1)
                
    def sendValue(self,val):        
        print(self.ser.write(val.encode()))
        
        
        
    def receivevalue(self):
        
        line = self.ser.readline().decode()
        print(line)
        
        
    def close(self):
        print("closing")
        self.ser.close()