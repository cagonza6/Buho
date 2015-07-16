#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to introduce a book

import wx
import cfg

class NewBook(wx.Panel):
	def __init__(self, parent, size):
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
		fgs.AddMany([(self.stIs),(self.tcIs, 1, wx.EXPAND),(self.stTi),(self.tcTi, 1, wx.EXPAND),(self.stAu),(self.tcAu, 1, wx.EXPAND),(self.stCm),(self.tcCm, 2, wx.EXPAND)])
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben
	
		##Fake Addition
		self.tcIs.SetValue("0")
		self.tcTi.SetValue("Tríbes")
		self.tcAu.SetValue("M. Sandrïne")
	
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
              
	def OnSave(self,e):
		if True:
			error = 0
			#taking data
			isbn = self.tcIs.GetValue()
			if isbn == "":
				error = 1
				cfg.chk("Debe poner un ISBN", 2)
			ti = self.tcTi.GetValue()
			au = self.tcAu.GetValue()
			cm = self.tcCm.GetValue()	
			if cm == "": cm = "Sin Comentarios"
			#need to check a bunch of things here
			
			#Saving Actual Book Data:
			if (error == 0):
				nbk = cfg.Book(cfg.topidb, isbn, 2, ti, au, 1, cm)		#0=eliminado, 1=old, 2=new,3=modificado
				cfg.bks[cfg.topidb] = nbk
				cfg.topidb = cfg.topidb + 1
				cfg.chk("Libro ha sido registrado", 1)
				self.Clean()
			else:
				cfg.chk("Hubo al menos un error en el proceso. Libro no ha sido registrado", 2)
	  
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
