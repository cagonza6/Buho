#!/usr/bin/python
# -*- coding: utf-8 -*-
#defines Book and User. 
#will have ept for each.
#has the main arrays: bks, uss

#has the practicalities:
#	op system vars
#	?IsNotBor
#	

import sys # detect SO
from os import system
import os.path

#import Main
import time
#import calendar
import wx
import codecs
#list of global vars. Can't alter here.
topidb = 0
topidu = 2			#User Bilbioteca
lockwin = False
ext = 0

bks = {}
uss = {}

# Da igual donde se ejecute, the main folder will always be automatically detected
# and dinamically asigned, I hope It works on wintendo...

                #########
                # Paths #
                #########

homeDir = os.getcwd()                  # Automatically generated acoording where the script is running from
DataDir = '/Data/'                     # Name of the folder where the data is located
                                       # txt only
dataDir  = homeDir + DataDir           # folder with the txt information

sqdbPath = homeDir+'/database/Main.db' #path to the database SQlite
#???
topidfn  = "topid.dat"                 # 

                ###########
                # Configs #
                ###########
reqRut = False                         #if True, RUT es necesario para registrar un usuario

                ###########
                # Methods #
                ###########
# in future versions they will be moved to other files to left here just configurations

def ept_bk(): return Book(0,0,"SinISBN","SinTitulo","SinAutor",0,"SinComentario")  
def ex_bk():  return Book(2,1,"Título","Autor",1,"Muy bueno.")  

def ept_us(): return User(0,0,"SinNombre")  
def ex_us():  return User(2,1,"Nombre")  

def IsNotBor(whatever):
	if (whatever.GetStatus()==0): return False
	return True

def today():
	dt = [0,2]
	dt[0] = int(time.strftime('%d', time.localtime()))
	dt[1] = int(time.strftime('%m', time.localtime()))
	#print dt
	return dt

def is_late(rtrn_dt):	#return boolean
	td = today()
	return_date = rtrn_dt.split("/")
	print return_date
	print td
	if int(return_date[1]) < td[1]: return True
	elif int(return_date[1]) > td[1]: return False
	if int(return_date[1]) == td[1]:
		if int(return_date[0]) > td[0]: return False
		else: return True

def calc_return_date(): 
	td = today()
	rt_day = td[0] + 14
	if rt_day > day_month(td[1]):	#si el día es mayor q el maximo de mes:
		rt_day = day_month(td[1]) - rt_day
		mt_day = td[1] +1
	else: mt_day = td[1]
	return str(rt_day)+"/"+str(mt_day)

def day_month(month):
	m31 = [1,3,5,7,8,10,12]
	m30 = [4,6,9,11]
	#year = time.strftime('%Y', time.localtime())
	if (month in m31):
		return 31
	if (month in m30):
		return 30
	#if (month == 2):
	#	if (calendar.isleap(year)): return 29
	#	else: return 28
#There shouldn't be any loans in Feb.


def stop(msg):
	print msg
	#op=raw_input()

#~ Might need sth similar for loans. There will have to be a check against holidays and stuff, but that is further refinement.
#~ def calc_age(age, dt): 
	#~ yd = (int)(dt[2]) - (int)(age[2]) 		#year difference
	#~ if ((int)(age[1]) >= (int)(dt[1])):	
		#~ if ((int)(age[0]) >= (int)(dt[0])):
			#~ yd = 1 + yd
	#~ return  yd


