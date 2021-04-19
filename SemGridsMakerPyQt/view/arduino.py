# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 08:39:07 2021

@author: gelias
"""
import sys
import os
import serial
import time

class Arduino:
    def __init__(self,com):
        self.portCom = com
        self.initUART(self.portCom)  # En windows de COM4 a COM 30
   
    def initUART(self,port):
    		baudrate = 9600	
    		try: 	
    			self.ser = serial.Serial(
    				port,
    				baudrate,
    				timeout=1,
    				# parity=serial.PARITY_NONE,
    				# stopbits=serial.STOPBITS_ONE,
    				# bytesize=serial.EIGHTBITS
    			)
    		except serial.SerialException as e:
    			print("port inconnu" % port)
    			self.ser.close()
    			sys.exit(-1)