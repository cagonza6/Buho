#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book
#Cannibalized from mNewBook

import wx
import cfg
import mSearchWindows
from Tools.sqlite import loanbook
import Tools.interface as Iface # mensajes por pantall

class LoanBook(wx.Panel):
	def __init__(self, parent, size):

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
		mSearchWindows.SearchBook(self)

	def OnSelecUser(self, e):
		mSearchWindows.SearchUser(self)

	def RecieveIdn(self, data, tipo):
		#print idn, what
		if tipo == 'book':
			self.tcBk.SetValue('')
			self.book = self.validarLibro(data)
			if self.book:
				self.tcBk.SetValue(self.book['titulo'])

		elif tipo == 'user':
			self.tcUs.SetValue('')
			self.user = self.validarUser(data)
			if self.user:
				self.tcUs.SetValue(self.user['nombres']+" "+self.user['apellidos'])

	def validarUser(self, user):
		if not ('estado' in user.keys()) or not user['estado']:
			Iface.showmessage('El usuario seleccionado no puede recibir libros ya que se encuentra bloqueado.',"Bloqueado")
			return False
		return user

	def validarLibro(self, libro):
		if not libro['estado']:
			Iface.showmessage('El Libro que seleccionado ya se encuentra prestado.',"Prestado")
			return False
		return libro

	def validateLoan(self):

		if not self.user:
			self.validarUser(self.user)
			return False
		if self.validarLibro(self.book)
			return False
		'''
		Aqui hai q incluir los metodo para validar las fechas desde un calendario
		'''
		self.desde=20160105
		self.hasta=20160106
		return [self.book['id_libro'],self.user['id_usuario'],self.desde,self.hasta]

	def OnLoan(self, e):
		#segunda validacion de los parametros de usuario y libro,
		#tambien obtiene los parametros para prestar
		self.data_loan = self.validateLoan()

		if not self.data_loan:
			Iface.showmessage('Se encontro un problema al prestar libros.\nPrestamo cancelado.',"Prestamo")
			return

		self.saving = loanbook(self.data_loan)
		if self.saving:
			#actualiza los valores despues de prestar un libro para no prestarlo otra vez
			self.book=False
			self.user=False
			self.Clean()
			return

	def Clean(self):
		self.tcBk.SetValue("")
		self.tcUs.SetValue("")

if __name__ == '__main__':
	ex = wx.App()
	LoanBook(None)
	ex.MainLoop()    
