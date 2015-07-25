#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book

import wx
import cfg
import mSearchWindows
import wx.calendar as cal
from Tools.sqlite import DatabaseManager
from Tools.calendar import int2date,date2int
import Tools.interface as Iface # mensajes por pantalla


class RetBook(wx.Panel):
	def __init__(self, parent, size,books=False):
		wx.Panel.__init__(self, parent = parent, size = size)
		vbox = wx.BoxSizer(wx.VERTICAL)

		self.user     = False
		self.book     = False
		self.prestamo = False

		self.DBmanager = DatabaseManager()
		if not books:
			self.books     = self.DBmanager.load_table('libros')
		else:
			self.books     = books


		#Búsqueda libro
		bsBus = wx.BoxSizer(wx.HORIZONTAL)
		btBk = wx.Button(self, label = "Buscar Libro")
		self.tcBk = wx.TextCtrl(self)
		bsBus.AddMany([(btBk, 0),(self.tcBk, 1, wx.EXPAND)])

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

		self.pnlUs.SetSizerAndFit(fgsUs, 0)
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
		self.stIso = wx.StaticText(self.pnlBk)
		self.stTio = wx.StaticText(self.pnlBk)
		self.stAuo = wx.StaticText(self.pnlBk)
		self.stPto = wx.StaticText(self.pnlBk)
		fgsBk.AddMany([(stIs, 0),(self.stIso, 0),
		             (stTi, 0),(self.stTio, 0),
		             (stAu, 0),(self.stAuo, 0),
		             (stPt, 0),(self.stPto, 0)])
		self.pnlBk.SetSizerAndFit(fgsBk)
		self.pnlBk.Hide()

		bsDt.AddMany([(self.pnlBk, 1), (wx.StaticLine(self, -1, style=wx.LI_VERTICAL),1,wx.ALIGN_CENTER_HORIZONTAL ),(self.pnlUs, 1)])

		fgsCal = wx.FlexGridSizer(3,2,10,20)

		stTitHoy = wx.StaticText(self, label = "Fecha de Hoy")
		font = stTitHoy.GetFont()
		font.SetWeight(wx.BOLD)
		stTitHoy.SetFont(font)
		self.cal_hoy = cal.CalendarCtrl(self, -1, wx.DateTime.Today())
		self.cal_hoy.EnableMonthChange(False)
		self.cal_hoy.EnableHolidayDisplay(False)

		stTitEnt = wx.StaticText(self, label = "Fecha debida de Entrega")
		stTitEnt.SetFont(font)
		self.cal_ent = cal.CalendarCtrl(self, -1, style = cal.CAL_NO_YEAR_CHANGE)
		self.cal_ent.EnableMonthChange(False)
		self.cal_ent.EnableHolidayDisplay(False)

		fgsCal.AddMany([(stTitHoy, 1, wx.ALIGN_CENTER_HORIZONTAL), (stTitEnt, 1, wx.ALIGN_CENTER_HORIZONTAL, 0),
		               (self.cal_hoy, 1, wx.ALIGN_CENTER_HORIZONTAL), (self.cal_ent, 1, wx.ALIGN_CENTER_HORIZONTAL)])
		fgsCal.AddGrowableCol(0)
		fgsCal.AddGrowableCol(1)
		fgsCal.AddGrowableRow(1)


		btRt = wx.Button(self, label = "Devolver")

		btBk.Bind(wx.EVT_BUTTON, self.OnSelecBook)
		btRt.Bind(wx.EVT_BUTTON, self.OnRet)

		#calendario dia actual: 
		self.cal_hoy.Bind(cal.EVT_CALENDAR, self.OnHoyMove)						#Locking all possible movement of today's date.
		self.cal_hoy.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnHoyMove)
		self.cal_hoy.Bind(cal.EVT_CALENDAR_DAY, self.OnHoyMove)
		#calendario dia debido retorno
		self.cal_ent.Bind(cal.EVT_CALENDAR, self.OnEntMove)						#Locking all possible movement of date to keep it in range
		self.cal_ent.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnEntMove)
		self.cal_ent.Bind(cal.EVT_CALENDAR_DAY, self.OnEntMove)


		vbox.Add(bsBus, 0, wx.EXPAND)
		vbox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		vbox.Add(bsDt, 0, wx.EXPAND)
		vbox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		vbox.Add(fgsCal, 0, wx.EXPAND)
		vbox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		vbox.Add(btRt, 0 , wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
		self.SetSizer(vbox)
		self.Hide()

	def OnSelecBook(self, e):
		self.books     = self.DBmanager.load_table('libros')
		mSearchWindows.SearchBook(self, 1,self.books)	#2: Mostrar solo libros disponibles

	def RecieveIdn(self, data, tipo):

		if tipo == 'book':
			self.tcBk.SetValue('')
			self.book = self.validarLibro(data)
			if self.book:
				self.tcBk.SetValue(self.book['titulo'])
				self.prestamo = self.DBmanager.load_loan_data(self.book['id_prestamo'])
				self.user     = self.DBmanager.load_user(self.prestamo['id_usuario'])
			if self.user:
				self.llenarDatos()

	def llenarDatos(self):
		#Libro
		self.cal_ent.EnableMonthChange(True)
		self.stIso.SetLabel(self.book['isbn'])
		self.stTio.SetLabel(self.book['titulo'])
		self.stAuo.SetLabel(self.book['autor'])
		if self.book['estado']:
			self.stPto.SetLabel(label = "Si")
		else:
			self.stPto.SetLabel("No")

		#Usuario
		self.laNm.SetLabel(self.user['nombres'])
		self.laAp.SetLabel(self.user['apellidos'])

		if self.user['estado']:
			self.laSt.SetLabel("Activo")
		else:
			self.laSt.SetLabel("Inactivo")
		self.cal_ent.PySetDate(int2date(self.prestamo['hasta'])) 	#Mostrar fecha en calendario

		self.pnlUs.Layout()
		self.pnlBk.Layout()
		self.pnlUs.Show()
		self.pnlBk.Show()
		#self.cal_ent.EnableMonthChange(False)					#Bloqueo el cambio de mes
		self.Layout()

	def OnHoyMove(self, e):
		#Bloquea movimientos de fecha
		self.cal_hoy.SetDate(wx.DateTime_Now())

	def OnEntMove(self, e):
		self.cal_hoy.SetDate(wx.DateTime_Now())
		if self.user:
			self.cal_ent.PySetDate(int2date(self.prestamo['hasta']))

	def validarLibro(self, libro):

		if not ('estado' in libro.keys()) or not libro['estado']:
			Iface.showmessage('El Libro que seleccionado no se encuentra prestado.',"No Prestado")
			return False
		return libro

	def isdelayed(self):
		self.delay=self.prestamo['hasta'] - self.retorno;
		if self.delay<0:
			Iface.showmessage(u'El libro se está entregando con ['+str(self.delay)+'] Dias de atraso.',"Atraso")
			return self.delay
		return 0

	def validateReturn(self):
		if not self.validarLibro(self.book):
			return False
		self.retorno = date2int(self.cal_hoy.PyGetDate())
		return [self.book['id_prestamo'],self.retorno]


	def OnRet(self, e):
		#segunda validacion de los parametros de usuario y libro,
		#tambien obtiene los parametro
		self.data_return = self.validateReturn()

		if not self.data_return:
			Iface.showmessage('Se encontro un problema al prestar libros.\nPrestamo cancelado.',"Prestamo")
			return

		self.saving = self.DBmanager.returnbook(*self.data_return)
		if not self.saving:
			Iface.showmessage('Error al registrar el retorno.',"Database")
		if self.saving:
			self.isdelayed()
			#self.multar()
			self.book     = False
			self.user     = False
			self.prestamo = False
			Iface.showmessage(u'Devolución realizado con exito.','Prestamos')
			self.Clean()
			return

	def Clean(self):
		self.tcBk.SetValue("")


class DummyFrame(wx.Frame):
	def __init__(self,parent):
		super(DummyFrame, self).__init__(parent = parent, size=(700, 500)) 
		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = RetBook(self, self.GetSize())
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
