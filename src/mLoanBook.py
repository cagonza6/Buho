#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book
#Cannibalized from mNewBook

import wx
import cfg
import mSearchWindows

class LoanBook(wx.Panel):
	def __init__(self, parent, size, books, users):
		self.books=books
		self.users=users
		wx.Panel.__init__(self, parent = parent, size = size)
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.bk_id = -1
		self.us_id = -1
		fgs = wx.FlexGridSizer(2,2,7,15)
		ste = wx.StaticText(self,label = "")

		#Botones
		btBk = wx.Button(self, label = "Buscar Libro")
		btUs = wx.Button(self, label = "Buscar Usuario")

		self.tcBk = wx.TextCtrl(self)
		self.tcUs = wx.TextCtrl(self)
		fgs.AddGrowableCol(1)
		fgs.AddMany([(btBk, 0),(self.tcBk, 1, wx.EXPAND),(btUs, 0),(self.tcUs, 1, wx.EXPAND)])
		#fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben

		self.stDt = wx.StaticText(self, label = "Libro será prestado hasta el " + cfg.calc_return_date())
		btPt = wx.Button(self, label = "Prestar")
		
		btBk.Bind(wx.EVT_BUTTON, self.OnSelecBook)
		btUs.Bind(wx.EVT_BUTTON, self.OnSelecUser)
		btPt.Bind(wx.EVT_BUTTON, self.OnLoan)
			
		vbox.Add(fgs, 0, wx.EXPAND)
		vbox.Add(self.stDt, 0)
		vbox.Add(btPt, 0 , wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
		self.SetSizer(vbox)
		self.Hide()

	def OnSelecBook(self, e):
		mSearchWindows.SearchBook(self,self.books)

	def OnSelecUser(self, e):
		mSearchWindows.SearchUser(self,self.users)

	def RecieveIdn(self, data, tipo):
		#print idn, what
		if tipo == 'book':
			self.book = data
			self.tcBk.SetValue(self.book['titulo'])
		if tipo == 'user':
			self.user = data
			self.tcUs.SetValue(self.user['nombres']+" "+self.user['apellidos'])

	def OnLoan(self, e):
		print "Prestando"
		if (self.bk_id != -1) and (self.us_id != -1):
			bk = cfg.bks[self.bk_id]
			us = cfg.uss[self.us_id]
			if not(bk.IsLoaned()):
				aux = us.LateBook()
				if aux == "":
					bk.SetOwner(self.us_id)
					us.BorrowBook(self.bk_id, cfg.calc_return_date() )
					print "Loaned"
				else: 
					cfg.chk("Usuario debe:" + aux, 2)
			else:
				print "Libro está prestado."

	def Clean(self):
		self.tcBk.SetValue("")
		self.tcUs.SetValue("")

if __name__ == '__main__':
	ex = wx.App()
	LoanBook(None)
	ex.MainLoop()    
