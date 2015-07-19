#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book
#Cannibalized from mLoanBook

import wx
import cfg
import mSearchWindows
from Tools.sqlite import returnbook
import Tools.interface as Iface # mensajes por pantall

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
		mSearchWindows.SearchBook(self)

	def RecieveIdn(self, data, tipo):

		if tipo == 'book':
			self.tcBk.SetValue('')
			self.book = self.validarLibro(data)
			if self.book:
				self.tcBk.SetValue(self.book['titulo'])

	def validarLibro(self, libro):
		if not ('estado' in libro.keys()) or not libro['estado']:
			Iface.showmessage('El Libro que seleccionado no se encuentra prestado.',"No Prestado")
			return False
		return libro

	def validateReturn(self):
		if not self.validarLibro(self.book):
			return False
		'''
		Aqui hai q incluir los metodo para validar las fechas desde un calendario
		'''
		self.retorno=20160105
		return [self.book['id_libro'],self.retorno]

	def OnRet(self, e):
		#segunda validacion de los parametros de usuario y libro,
		#tambien obtiene los parametro
		self.data_return = self.validateReturn()

		if not self.data_return:
			Iface.showmessage('Se encontro un problema al prestar libros.\nPrestamo cancelado.',"Prestamo")
			return

		self.saving = returnbook(*self.data_return)
		if not self.saving:
			Iface.showmessage('Error al registrar el retorno.',"Database")
		if self.saving:
			self.book = False
			self.Clean()
			Iface.showmessage(u'Devolución realizado con exito.','Prestamos')
			return

	def Clean(self):
		self.tcBk.SetValue("")
		self.stUs.SetLabel("")

if __name__ == '__main__':
	ddic1={'id_libro':1,'titulo':'Titulo animal','autor': 'Autor Auto 1','isbn':'123456789','comentarios': 'no hay 1','estado':0}
	ddic2={'id_libro':2,'titulo':'Titulo mueble','autor': 'Autor Casa 2','isbn':'223456789','comentarios': 'no hay 2','estado':1}
	ddic3={'id_libro':3,'titulo':'Titulo pelota','autor': 'Autor mono 2','isbn':'323456789','comentarios': 'no hay 3','estado':1}
	books=[ddic1,ddic2,ddic3]

	ex = wx.App()
	RetBook(None)
	ex.MainLoop()    
