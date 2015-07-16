#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to introduce a user
#(Scavanged from mNewBook)

import wx
import cfg
import Main

class NewUser(wx.Panel):
	def __init__(self, parent, size):
		wx.Panel.__init__(self, parent = parent, size = size)	
		vbox = wx.BoxSizer(wx.VERTICAL)
		fgs = wx.FlexGridSizer(2,2,7,15)
		#Cannons for mosquitoes? Totally. Need it for later
		ste = wx.StaticText(self,label = "")
		self.stNm = wx.StaticText(self, label = "Nombre")
		self.tcNm = wx.TextCtrl(self)
		fgs.AddMany([(self.stNm),(self.tcNm, 1, wx.EXPAND)])
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben
	
		##Fake Addition
		btsv = wx.Button(self, label = 'Guardar')#, pos=(30, 160))
		btsv.Bind(wx.EVT_BUTTON, self.OnSave)
		fgs.AddMany([(ste),(btsv)])
        
		vbox.Add(fgs, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 15)
		self.SetSizer(vbox)
		self.Hide()
        
	def Clean(self):
		self.tcNm.SetValue("")
              
	def OnSave(self,e):
		if True:
			#fix from here on
			error = 0
			#taking data
			nm = self.tcNm.GetValue()
			if nm == "": 
				error = 1
				#cfg.chk("No ha ingresado nombre de usuario",1)
			#Saving Actual User Data:
			if (error == 0):
				nus = cfg.User(cfg.topidu, 2, nm)		#0=eliminado, 1=old, 2=new,3=modificado
				cfg.uss[cfg.topidu] = nus
				cfg.topidu = cfg.topidu + 1
				cfg.chk("Usuario ha sido registrado",2)
				self.Clean()
			else:
				cfg.chk("Hubo al menos un error en el proceso. Usuario no ha sido registrado", 2)
	  
#class Example(wx.Frame):
	#def __init__(self,parent):
		#super(Example, self).__init__(parent=parent, size=(700, 250)) 
		#vbox = wx.BoxSizer(wx.VERTICAL)
		#self.panel = NewBook(self)
		#vbox.Add(self.panel,2,wx.EXPAND)
		#self.SetSizer(vbox)
		#self.Centre()
		#self.Show()

#if __name__ == '__main__':
	#ex = wx.App()
	#Example(None)
	#ex.MainLoop()    
