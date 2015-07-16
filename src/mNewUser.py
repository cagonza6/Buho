#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to introduce a user
#(Scavanged from mNewBook)
# para los mensajes por ventana
import wx
import Tools.interface as Iface

from Tools.regexe import *
from Tools.sqlite import saveuser

import cfg
import Main

class NewUser(wx.Panel):
	def __init__(self, parent, size):
		wx.Panel.__init__(self, parent = parent, size = size)
		vbox = wx.BoxSizer(wx.VERTICAL)
		Entradas = 7

		fgs = wx.FlexGridSizer(7,2,7,15)
		#Cannons for mosquitoes? Totally. Need it for later
		ste       = wx.StaticText(self,label = "")
		self.stNm = wx.StaticText(self, label = "Nombre(s)  :")
		self.stAp = wx.StaticText(self, label = "Apellido(s):")
		self.stRu = wx.StaticText(self, label = "Rut        :")
		self.stDi = wx.StaticText(self, label = "Direccion  :")
		self.stTe = wx.StaticText(self, label = "Telefono   :")
		self.stCm = wx.StaticText(self, label = "Comentarios:")
		self.tcNm = wx.TextCtrl(self)
		self.tcAp = wx.TextCtrl(self)
		self.tcRu = wx.TextCtrl(self)
		self.tcDi = wx.TextCtrl(self)
		self.tcTe = wx.TextCtrl(self)
		self.tcCm = wx.TextCtrl(self,style=wx.TE_MULTILINE)
		fgs.AddMany([(self.stNm),(self.tcNm, 1, wx.EXPAND),
		             (self.stAp),(self.tcAp, 1, wx.EXPAND),
		             (self.stRu),(self.tcRu, 1, wx.EXPAND),
		             (self.stDi),(self.tcDi, 1, wx.EXPAND),
		             (self.stTe),(self.tcTe, 1, wx.EXPAND),
		             (self.stCm),(self.tcCm, 2, wx.EXPAND)])
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben
	
		self.Clean()

		btsv = wx.Button(self, label = 'Guardar')#, pos=(30, 160))
		btsv.Bind(wx.EVT_BUTTON, self.OnSave)
		fgs.AddMany([(ste),(btsv)])

		vbox.Add(fgs, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 15)
		self.SetSizer(vbox)
		self.Hide()

	def Clean(self):
		self.tcNm.SetValue("")
		self.tcAp.SetValue("")
		self.tcRu.SetValue("")
		self.tcDi.SetValue("")
		self.tcTe.SetValue("")
		self.tcCm.SetValue("")

	def isValid(self):
		#fix from here on
		error = 0
		error_str=''
		#taking data
		name = unicode(self.tcNm.GetValue())
		name = unicode(name.strip().title())
		if not validar('name',name): 
			error += 1
			error_str="Nombre No valido: ["+name+"] \n"
		apellido = unicode(self.tcAp.GetValue())
		apellido = unicode(apellido.strip().title())
		if not validar('name',apellido): 
			error += 1
			error_str+="Apellido no valido: ["+apellido+"] \n"

		rut = str(self.tcRu.GetValue()).strip()
		if cfg.reqRut and not validar('rut',rut):
			error_str+="Rut no valido: ["+rut+"] \n"
			error += 1

		direccion   = str(self.tcDi.GetValue()).strip()
		telefono    = str(self.tcTe.GetValue()).strip()
		comentarios = str(self.tcCm.GetValue()).strip()

		if (error):
			Iface.showmessage(error_str,"Error!")
			return False
		return [name, apellido, rut,direccion,telefono,comentarios]
		#Saving Actual User Data:

	def OnSave(self,e):
		newUserData = self.isValid()
		if newUserData:
			'''
			nm = self.tcNm.GetValue()
			nus = cfg.User(cfg.topidu, 2, nm)		#0=eliminado, 1=old, 2=new,3=modificado
			cfg.uss[cfg.topidu] = nus
			cfg.topidu = cfg.topidu + 1
			'''

			if saveuser(newUserData,cfg.sqdbPath):
				Iface.showmessage("Usuario ha sido registrado","Mensaje")
			else:
				Iface.showmessage("Error Al intentar guardar Usuario","Error!")
			self.Clean()

