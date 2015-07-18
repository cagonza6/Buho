#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book
#Cannibalized from mNewBook

import wx
import cfg
import mSearchWindows
from Tools.sqlite import loanbook

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

	def validarUser(self, user):
		if not user['estado']:
			return False
		return True

	def validarLibro(self, libro):
		if not libro['estado']:
			return False
		return True

	def validateLoan(self):
		if not self.validarUser (self.user):
			return False
			print "Usuario no puede recibir libros"

		if not self.validarLibro(self.book):
			return False
			print "Libro ya se encuentra prestado"
		self.desde=20160105
		self.hasta=20160106
		return [self.book['id_libro'],self.user['id_usuario'],self.desde,self.hasta]

	def OnLoan(self, e):
		self.data_loan = self.validateLoan()

		if not self.data_loan:
			print "Problem while validating loan!"
			return

		self.saving = loanbook(self.data_loan)
		if self.saving:
			return

	def Clean(self):

		self.tcBk.SetValue("")
		self.tcUs.SetValue("")

if __name__ == '__main__':
	ex = wx.App()
	LoanBook(None)
	ex.MainLoop()    
