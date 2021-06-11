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
    def __init__(self):
        pass
    def connect(self,port):
        baudrate = 2000000	
        
        try: 	
            self.ser = serial.Serial(
    				port,
    				baudrate
    				# parity=serial.PARITY_NONE,
    				# stopbits=serial.STOPBITS_ONE,
    				# bytesize=serial.EIGHTBITS
    			)
                
        except serial.SerialException as e:
            print("port inconnu" % port)
            self.ser.close()
            sys.exit(-1)
                
    def sendValue(self,val):        
        print(val)
        print(self.ser.write(val.encode()))
        
        
        
    def receivevalue(self):
        
        line = self.ser.readline().decode()
        print(line)
        
        
    def close(self):
        print("closing")
        self.ser.close()