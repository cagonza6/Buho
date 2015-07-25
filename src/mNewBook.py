#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to introduce a book

import cfg
import wx
import Tools.interface as Iface
from classes import *
from Tools.regexe import *
from Tools.sqlite import DatabaseManager

class NewBook(wx.Panel):
	def __init__(self, parent, size):

		self.DBmanager = DatabaseManager()

		wx.Panel.__init__(self, parent = parent, size = size)
		vbox = wx.BoxSizer(wx.VERTICAL)
		fgs = wx.FlexGridSizer(5,2,7,15)
		ste = wx.StaticText(self,label = "")
		self.stIs = wx.StaticText(self, label= "ISBN")
		self.stTi = wx.StaticText(self, label = "Título")
		self.stAu = wx.StaticText(self, label = "Autor")
		self.stCm = wx.StaticText(self, label = "Comentario")
		self.tcIs = wx.TextCtrl(self)
		self.tcTi = wx.TextCtrl(self)
		self.tcAu = wx.TextCtrl(self)
		self.tcCm = wx.TextCtrl(self,style=wx.TE_MULTILINE)
		fgs.AddMany([(self.stIs),(self.tcIs, 1, wx.EXPAND),
		             (self.stTi),(self.tcTi, 1, wx.EXPAND),
		             (self.stAu),(self.tcAu, 1, wx.EXPAND),
		             (self.stCm),(self.tcCm, 2, wx.EXPAND)])
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben
	
		##Fake Addition
		self.Clean() # limpia campos

		btsv = wx.Button(self, label = 'Guardar')#, pos=(30, 160))
		btsv.Bind(wx.EVT_BUTTON, self.OnSave)
		fgs.AddMany([(ste),(btsv)])

		vbox.Add(fgs, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 15)
		self.SetSizer(vbox)
		self.Hide()


	def Clean(self):
		self.tcIs.SetValue("")
		self.tcTi.SetValue("")
		self.tcAu.SetValue("")
		self.tcCm.SetValue("")

	def isValid(self):
		#fix from here on
		error = False
		error_str=''

		isbn = validar('isbn',self.tcIs.GetValue())
		if not isbn:
			error      = True
			error_str += "ISBN no valido\n"

		ti = validar('titulo',self.tcTi.GetValue())
		if not ti:
			error      = True
			error_str += "Titulo no valido.\n"

		au = validar('autor',self.tcAu.GetValue())
		if not au:
			if Iface.cnt(u'El campo Autor está en blanco, desea llenarlo con: "Anonimo"'):
				au = "Anonimo"
				self.tcAu.SetValue(au)

		comentarios = self.tcCm.GetValue()

		if (error):
			Iface.showmessage(error_str,"Error!")
			return False
		return [isbn,ti,au,comentarios]
	def OnSave(self,e):
		newBookData = self.isValid()
		if newBookData:
			if self.DBmanager.save_new(newBookData,'book'):
				Iface.showmessage('Libro registrado con exito.', 'Información')
				self.Clean()
			else:
				Iface.showmessage("Error Al intentar guardar Libro","Error!")
			return
