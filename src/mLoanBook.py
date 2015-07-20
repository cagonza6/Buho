#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book

import wx
import cfg
import mSearchWindows
import wx.calendar as cal
from Tools.sqlite import loanbook
import Tools.interface as Iface # mensajes por pantall

class LoanBook(wx.Panel):
	def __init__(self, parent, size):
		wx.Panel.__init__(self, parent = parent, size = size)
		vbox = wx.BoxSizer(wx.VERTICAL)
		fgs = wx.FlexGridSizer(2,2,7,15)

		#Botones
		btBk = wx.Button(self, label = "Buscar Libro")
		btUs = wx.Button(self, label = "Buscar Usuario")

		self.tcBk = wx.TextCtrl(self)
		self.tcUs = wx.TextCtrl(self)
		fgs.AddMany([(btBk, 0), (self.tcBk, 1, wx.EXPAND),(btUs, 0), (self.tcUs, 1, wx.EXPAND)])
		fgs.AddGrowableCol(1)

		#Paneles datos
		bsDt = wx.BoxSizer(wx.HORIZONTAL)
		
		#Panel datos Usuario
		self.pnlUs = wx.Panel(self, -1)
		fgsUs   = wx.FlexGridSizer(3,2,7,15)
		# Identificadores
		stNm = wx.StaticText(self.pnlUs, label = "Nombre(s)")
		stAp = wx.StaticText(self.pnlUs, label = "Apellido(s)")
		stSt = wx.StaticText(self.pnlUs, label = "Estado")
		# Campos
		self.laNm = wx.StaticText(self.pnlUs)
		self.laAp = wx.StaticText(self.pnlUs)
		self.laSt = wx.StaticText(self.pnlUs)

		fgsUs.AddMany([(stNm),(self.laNm, 0),
		            (stAp),(self.laAp , 0),
		            (stSt),(self.laSt , 0),
		            ]
		)
		
		self.pnlUs.SetSizer(fgsUs, 0)
		self.pnlUs.Hide()
		
		#Datos Libro
		self.pnlBk = wx.Panel(self, -1)
		fgsBk = wx.FlexGridSizer(4,2,7,15)
		# Identificadores
		stIs  = wx.StaticText(self.pnlBk, label = "ISBN: ")
		stTi  = wx.StaticText(self.pnlBk, label = "Título: ")
		stAu  = wx.StaticText(self.pnlBk, label = "Autor: ")
		stPt  = wx.StaticText(self.pnlBk, label = "Prestado: ")
		# Campos
		self.stIso = wx.StaticText(self.pnlBk, label =".")
		self.stTio = wx.StaticText(self.pnlBk)
		self.stAuo = wx.StaticText(self.pnlBk)
		self.stPto = wx.StaticText(self.pnlBk)
		fgsBk.AddMany([(stIs, 0),(self.stIso, 0),
		             (stTi, 0),(self.stTio, 0),
		             (stAu, 0),(self.stAuo, 0),
		             (stPt, 0),(self.stPto, 0)])
		self.pnlBk.SetSizer(fgsBk)
		self.pnlBk.Hide()
		
		bsDt.AddMany([(self.pnlBk, 1), (wx.StaticLine(self, -1, style=wx.LI_VERTICAL),1,wx.ALIGN_CENTER_HORIZONTAL ),(self.pnlUs, 1)])

		btPt = wx.Button(self, label = "Prestar")
		
		fgsCal = wx.FlexGridSizer(3,2,10,20)
		
		stTitHoy = wx.StaticText(self, label = "Fecha de Préstamo")
		font = stTitHoy.GetFont()
		font.SetWeight(wx.BOLD)
		stTitHoy.SetFont(font)
		self.cal_hoy = cal.CalendarCtrl(self, -1, wx.DateTime.Today())
		self.cal_hoy.EnableMonthChange(False)
		self.cal_hoy.EnableHolidayDisplay()
		
		stTitFut = wx.StaticText(self, label = "Fecha de Entrega")
		stTitFut.SetFont(font)
		self.cal_fut = cal.CalendarCtrl(self, -1, wx.DateTime_Now(), style = cal.CAL_NO_YEAR_CHANGE)
		self.cal_fut.EnableMonthChange(True)
		self.cal_fut.EnableHolidayDisplay()
		default_loan_span = wx.DateSpan.Days(14)
		today = wx.DateTime_Now()
		default_return_date = today.AddDS(default_loan_span)		#modifica today
		self.cal_fut.SetDate(default_return_date)

		fgsCal.AddMany([(stTitHoy, 1, wx.ALIGN_CENTER_HORIZONTAL), (stTitFut, 1, wx.ALIGN_CENTER_HORIZONTAL, 0),
		               (self.cal_hoy, 1, wx.ALIGN_CENTER_HORIZONTAL), (self.cal_fut, 1, wx.ALIGN_CENTER_HORIZONTAL)])
		fgsCal.AddGrowableCol(0)
		fgsCal.AddGrowableCol(1)
		fgsCal.AddGrowableRow(1)

		btBk.Bind(wx.EVT_BUTTON, self.OnSelecBook)
		btUs.Bind(wx.EVT_BUTTON, self.OnSelecUser)
		btPt.Bind(wx.EVT_BUTTON, self.OnLoan)
		self.cal_hoy.Bind(cal.EVT_CALENDAR, self.OnHoyMove)						#Locking all possible movement of today's date.
		self.cal_hoy.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnHoyMove)
		self.cal_hoy.Bind(cal.EVT_CALENDAR_DAY, self.OnHoyMove)
		self.cal_fut.Bind(cal.EVT_CALENDAR, self.OnFutMove)						#Locking all possible movement of today's date.
		self.cal_fut.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnFutMove)
		self.cal_fut.Bind(cal.EVT_CALENDAR_DAY, self.OnFutMove)
		
		vbox.Add(fgs, 0, wx.EXPAND)
		vbox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		vbox.Add(bsDt, 0, wx.EXPAND)
		vbox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		vbox.Add(fgsCal, 0, wx.EXPAND)
		vbox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
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
				self.llenarDatosLibro()

		elif tipo == 'user':
			self.tcUs.SetValue('')
			self.user = self.validarUser(data)
			if self.user:
				self.tcUs.SetValue(self.user['nombres']+" "+self.user['apellidos'])
				self.llenarDatosUsuario()

	def llenarDatosLibro(self):
		
		self.stIso.SetLabel(self.book['isbn'])
		self.stTio.SetLabel(self.book['titulo'])
		self.stAuo.SetLabel(self.book['autor'])
		if self.book['estado']: self.stPto.SetLabel(label = "Si")
		else: self.stPto.SetLabel("No")
		self.pnlBk.Layout()
		self.pnlBk.Show()
		self.Layout()
		
	def	llenarDatosUsuario(self):
		self.laNm.SetLabel(self.user['nombres'])
		self.laAp.SetLabel(self.user['apellidos'])
		if self.user['estado']: self.laSt.SetLabel("Activo")
		else: self.laSt.SetLabel("Inactivo")
		self.pnlUs.Layout()
		self.pnlUs.Show()
		self.Layout()

	def OnHoyMove(self, e):
		#Todos los posibles cambios de fecha en cal_hoy están bloqueados.
		self.cal_hoy.SetDate(wx.DateTime_Now())
		
	def OnFutMove(self, e):
		un_dia = wx.DateSpan.Days(1)
		today = wx.DateTime_Now()
		manana = today.AddDS(un_dia)		#modifica today
		
		if (self.cal_fut.GetDate().IsEarlierThan(manana)):		#Si la fecha es anterior a mañana, automáticamente se corre a mañana. 
			self.cal_fut.SetDate(manana)
		
	def validarUser(self, user):
		if not ('estado' in user.keys()) or not user['estado']:
			Iface.showmessage('El usuario seleccionado no puede recibir libros ya que se encuentra bloqueado.',"Bloqueado")
			return False
		return user

	def validarLibro(self, libro):
		if not ('estado' in libro.keys()) or libro['estado']:
			Iface.showmessage('El Libro que seleccionado ya se encuentra prestado.',"Prestado")
			return False
		return libro

	def validateLoan(self):

		if not self.validarUser(self.user):
			return False
		if not self.validarLibro(self.book):
			return False
		#Las fechas se leen del calendario, ya está bloqueado elegir fechas de devolución anteriores a fecha de préstamo.
		self.desde = self.cal_hoy.PyGetDate()
		self.hasta = self.cal_fut.PyGetDate()
		return [self.book['id_libro'],self.user['id_usuario'],self.desde,self.hasta]

	def OnLoan(self, e):
		#segunda validacion de los parametros de usuario y libro,
		#tambien obtiene los parametros para prestar
		self.data_loan = self.validateLoan()

		if not self.data_loan:
			Iface.showmessage('Se encontró un problema al prestar libros.\nPrestamo cancelado.',"Prestamo")
			return

		self.saving = loanbook(*self.data_loan)
		if not self.saving:
			Iface.showmessage('Error al registrar el préstamo.',"Database")
		if self.saving:
			#actualiza los valores despues de prestar un libro para no prestarlo otra vez
			self.book=False
			self.user=False
			self.Clean()
			Iface.showmessage('Prestamo realizado con éxito.','Préstamos')
			return

	def Clean(self):
		self.tcBk.SetValue("")
		self.tcUs.SetValue("")

class DummyFrame(wx.Frame):
	def __init__(self,parent):
		super(DummyFrame, self).__init__(parent = parent, size=(700, 500)) 
		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = LoanBook(self, self.GetSize())
		vbox.Add(panel, 2, wx.EXPAND)
		panel.Show()
		self.SetSizer(vbox)
		self.Centre()
		self.Show()


if __name__ == '__main__':
	ddic1={'id_libro':1,'titulo':'Titulo animal','autor': 'Autor Auto 1','isbn':'123456789','comentarios': 'no hay 1','estado':0}
	ddic2={'id_libro':2,'titulo':'Titulo mueble','autor': 'Autor Casa 2','isbn':'223456789','comentarios': 'no hay 2','estado':1}
	ddic3={'id_libro':3,'titulo':'Titulo pelota','autor': 'Autor mono 2','isbn':'323456789','comentarios': 'no hay 3','estado':1}
	books=[ddic1,ddic2,ddic3]

	ex = wx.App()
	DummyFrame(None)
	ex.MainLoop()    
