#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to introduce a user
#(Scavanged from mNewBook)
# para los mensajes por ventana
import wx
import Tools.interface as Iface

from Tools.regexe import *
from Tools.sqlite import DatabaseManager

import cfg
import Main

class NewUser(wx.Panel):
	def __init__(self, parent, size):
		wx.Panel.__init__(self, parent = parent, size = size)
		vbox = wx.BoxSizer(wx.VERTICAL)
		Entradas = 7

		self.DBmanager = DatabaseManager()

		fgs = wx.FlexGridSizer(9,2,7,15)
		#Cannons for mosquitoes? Totally. Need it for later
		ste       = wx.StaticText(self,label = "")
		self.stNm = wx.StaticText(self, label = "Nombre(s)  :")
		self.stAp = wx.StaticText(self, label = "Apellido(s):")
		self.stRu = wx.StaticText(self, label = "Rut        :")
		self.stEm = wx.StaticText(self, label = "Email      :")
		self.stDi = wx.StaticText(self, label = "Direccion  :")
		self.stTe = wx.StaticText(self, label = "Telefono   :")
		self.stCu = wx.StaticText(self, label = "Curso      :")
		self.stCm = wx.StaticText(self, label = "Comentarios:")
		self.tcNm = wx.TextCtrl(self)
		self.tcAp = wx.TextCtrl(self)
		self.tcRu = wx.TextCtrl(self)
		self.tcEm = wx.TextCtrl(self)
		self.tcDi = wx.TextCtrl(self)
		self.tcTe = wx.TextCtrl(self)
		self.tcCu = wx.TextCtrl(self)
		self.tcCm = wx.TextCtrl(self,style=wx.TE_MULTILINE)
		fgs.AddMany([(self.stNm),(self.tcNm, 1, wx.EXPAND),
		             (self.stAp),(self.tcAp, 1, wx.EXPAND),
		             (self.stRu),(self.tcRu, 1, wx.EXPAND),
		             (self.stEm),(self.tcEm, 1, wx.EXPAND),
		             (self.stDi),(self.tcDi, 1, wx.EXPAND),
		             (self.stTe),(self.tcTe, 1, wx.EXPAND),
		             (self.stCu),(self.tcCu, 1, wx.EXPAND),
		             (self.stCm),(self.tcCm, 2, wx.EXPAND)])
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben
	
		self.Clean() # limpia campos

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
		self.tcEm.SetValue("")
		self.tcDi.SetValue("")
		self.tcTe.SetValue("")
		self.tcCu.SetValue("")
		self.tcCm.SetValue("")

	def isValid(self):
		#fix from here on
		error = False
		error_str=''

		name = self.tcNm.GetValue()
		name = validate('name',name)
		if not name: 
			error = True
			error_str="Nombre No valido.\n"

		apellido = validate('name',self.tcAp.GetValue())
		if not apellido: 
			error = True
			error_str+="Apellido no valido.\n"
		rut = self.tcRu.GetValue()
		if cfg.reqRut and not rut:
			error_str+="Rut no valido \n"
			error = True
		email = validate('email',self.tcEm.GetValue())
		if not email:
			error_str+="Email no valido \n"
			error = True

		direccion   = str(self.tcDi.GetValue()).strip()
		telefono    = str(self.tcTe.GetValue()).strip()
		grade       = self.tcCu.GetValue()
		comentarios = self.tcCm.GetValue()


		if (error):
			Iface.showmessage(error_str,"Error!")
			return False
		return [name, apellido, rut,email,direccion,telefono,grade,comentarios]
		#Saving Actual User Data:



	def OnSave(self,e):
		newUserData = self.isValid()
		if newUserData:
			#try to save the user to the DB
			if self.DBmanager.save_new(newUserData,'user'):
				Iface.showmessage("Usuario ha sido registrado","Mensaje")
				#cleans just if the user was correctly added, de otra forma seria hincha-pelotas
				self.Clean()
			else:
				Iface.showmessage("Error Al intentar guardar Usuario","Error!")

if __name__ == '__main__':
	print "Aca se Agregan usuarios... suerte con eso..."
