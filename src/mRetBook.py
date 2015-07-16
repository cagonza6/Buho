#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book
#Cannibalized from mLoanBook

import wx
import cfg
import mSelecBook
import mSelecUser

class RetBook(wx.Panel):
	def __init__(self, parent, size):
		wx.Panel.__init__(self, parent = parent, size = size)	
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.bk_id = -1
		self.us_id = -1
		
		fgs = wx.FlexGridSizer(2,2,7,15)
		btBk = wx.Button(self, label = "Buscar Libro")
		self.tcBk = wx.TextCtrl(self)
		stUs = wx.StaticText(self, label = "Devuelve:")
		self.stUs = wx.StaticText(self)
		fgs.AddGrowableCol(1)
		fgs.AddMany([(btBk, 0),(self.tcBk, 1, wx.EXPAND),(stUs, 0),(self.stUs, 1, wx.EXPAND)])
		btRt = wx.Button(self, label = "Devolver")
		
		btBk.Bind(wx.EVT_BUTTON, self.OnSelecBook)
		btRt.Bind(wx.EVT_BUTTON, self.OnRet)
			
		vbox.Add(fgs, 0, wx.EXPAND)
		vbox.Add(btRt, 0 , wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
		self.SetSizer(vbox)
		self.Hide()

	def OnSelecBook(self, e):
		mSelecBook.SelecBook(self)
		
	def RecieveIdn(self, idn, what):
		#print idn, what
		if what == 0:
			self.bk_id = idn
			self.tcBk.SetValue(cfg.bks[idn].GetTitle())
			self.us_id = cfg.bks[idn].GetOwner()
			self.stUs.SetLabel(cfg.uss[self.us_id].GetName())
			
	def OnRet(self, e):
		if (self.bk_id != -1) and (self.us_id != -1):
			if cfg.bks[self.bk_id].IsLoaned():
				aux = cfg.uss[self.us_id].ReturnBook(self.bk_id)
				if aux == 1: 
					print "Devuelto"
					self.Clean()
				else: print "Libro no estaba prestado a este usuario."
			else:
				print "Libro no está prestado."
		
	def Clean(self):
		self.tcBk.SetValue("")
		self.stUs.SetLabel("")
              

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
