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

# da igual donde se ejecute, the main folder will always be automatically detected
# and dinamically asigned, I hope It works on wintendo...
homeDir = os.getcwd()
DataDir = '/Data/'

dataDir = homeDir + DataDir
topidfn = "topid.dat"

class Book:
	def __init__(self, idn, status, isbn, title, author, owner, cmnt):
		self.idn = idn
		self.isbn = isbn				#texto. Debe ser texto, hay una X como la K del rut
		self.title = title
		self.author = author			#au string name, for now
		self.cmnt = cmnt				#could have carriage return
		self.owner = owner				#idn_own #it's for whoever has it at the time. Biblioteca will be the main owner
		self.status = status			#0 = eliminado, 1 = old, 2 = new,3 = modificado
    
	def GetIdn(self): return self.idn
	def GetIsbn(self): return self.isbn
	def GetStatus(self): return self.status
	def GetTitle(self): return self.title
	def GetAuthor(self): return self.author
	def GetCmnt(self): return self.cmnt
	def GetOwner(self): return self.owner
	
	def SetIdn(self, aux): self.idn = aux
	def SetIsbn(self, aux): self.isbn = aux
	def SetStatus(self, aux): self.status = aux
	def SetAuthor(self, aux): self.author = aux
	def SetTitle(self, aux): self.title = aux
	def SetCmnt(self, aux): self.cmnt = aux
	def SetOwner(self, aux): self.owner = aux
	
	def IsLoaned(self):
		if self.GetOwner() == 1: return False			#1 es Biblioteca
		else: return True
		
	def Return(self):
		self.SetOwner(1)
		#I'm quite sure this will change in time, so it goes here. So I only have to change one place
		

     
def ept_bk():return Book(0,0,"SinISBN","SinTitulo","SinAutor",0,"SinComentario")  
def ex_bk():return Book(2,1,"Título","Autor",1,"Muy bueno.")  

#begin usuario
class User:
	def __init__(self, idn, status, name):
		self.idn = idn
		self.name = name
		self.books = []					#Libros que tiene prestados, incluyendo fecha de entrega
		self.status = status				#0 = eliminado, 1 = old, 2 = new,3 = modificado
			
	def GetIdn(self): return self.idn
	def GetStatus(self): return self.status
	def GetName(self): return self.name
	def GetBooks(self): return self.books
		
	def SetIdn(self, aux): self.idn = aux
	def SetStatus(self, aux): self.nobor = aux
	def SetName(self, aux): self.name = aux
	def SetBooks(self, aux): self.books = aux
	
	def BorrowBook(self, bk_id, returndate):
		self.books.append([bk_id, returndate])
		
	def ReturnBook(self, bk_id):
		i = 0
		while (i<len(self.books)):		#No creo que se de tener la media lista...
			if bk_id == self.books[i][0]:
				print bk_id, self.books[i][0]
				self.books.pop(i)
				bks[bk_id].Return()
				i = i - 1 				#has to do with the check condition at the end
				break
			i = i +1 
		if i != len(self.books): return 1			#todo bien (remember, I popped sth out, so new length 
		else: return -1								#El libro no era de este usuario
		#Maybe there should be some check para marcar si lo devolvió fuera de plazo?
	
	def LateBook(self):
		aux = ""
		for bk in self.books:
			if is_late(bk[1]):
				aux = aux + "\n " + bks[bk[0]].GetTitle()
		return aux
 
def ept_us():return User(0,0,"SinNombre")  
def ex_us():return User(2,1,"Nombre")  

def IsNotBor(whatever):
	if (whatever.GetStatus()==0): return False
	else: return True

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


def chk(msg,idn):
	if idn == 1: msge = "Error"
	if idn == 2: msge = "Check"
	wx.MessageBox(msg, msge, wx.OK)
	
def cnt(msg):
	dial = wx.MessageDialog(None, msg+"¿Desea continuar?".decode('utf-8'), 'Advertencia', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
	ret = dial.ShowModal()
	if ret == wx.ID_YES: return True
	else: return False

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
