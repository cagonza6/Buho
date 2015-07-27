#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book

import wx
import cfg
import mSearchWindows
import wx.calendar as cal
from Tools.sqlite import DatabaseManager
from Tools.calendar import date2int,isweekend
import Tools.interface as Iface # mensajes por pantall

class LoanBook(wx.Panel):
	def __init__(self, parent, size):
		wx.Panel.__init__(self, parent = parent, size = size)
		verticalBox = wx.BoxSizer(wx.VERTICAL)                          # Main box of the App
		fgs = wx.FlexGridSizer(2,2,7,15)

		self.DBmanager = DatabaseManager()
		self.user      = False
		self.book      = False
		#########
		#Buttons#
		#########
		but_searchbook = wx.Button(self, label = "Buscar Libro")
		but_searchuser = wx.Button(self, label = "Buscar Usuario")

		self.txtfield_bookId = wx.TextCtrl(self)
		self.txtfield_userId = wx.TextCtrl(self)
		fgs.AddMany([(but_searchbook, 0),
                     (self.txtfield_bookId, 1, wx.EXPAND),
                     (but_searchuser, 0),
                     (self.txtfield_userId, 1, wx.EXPAND)])
		fgs.AddGrowableCol(1)

		#############
		#Data Panels#
		#############
		bookDataZiser = wx.BoxSizer(wx.HORIZONTAL)
			# User Panel
		self.userPanel = wx.Panel(self, -1)
		userDataSizer   = wx.FlexGridSizer(3,2,7,15)
				# Labels
		label_userName = wx.StaticText(self.userPanel,       label = "Nombre(s)")
		label_userFamilyName = wx.StaticText(self.userPanel, label = "Apellido(s)")
		label_userState = wx.StaticText(self.userPanel,      label = "Estado")
				# Fields
		self.txtValueUserName = wx.StaticText(self.userPanel)
		self.txtValueUserFamilyName = wx.StaticText(self.userPanel)
		self.txtValueUserStatus = wx.StaticText(self.userPanel)

		userDataSizer.AddMany([(label_userName),(self.txtValueUserName, 0),
		               (label_userFamilyName),(self.txtValueUserFamilyName , 0),
		               (label_userState),(self.txtValueUserStatus , 0),
		            ]
		)
		
			#Book Panel
		self.userPanel.SetSizer(userDataSizer, 0)
		self.userPanel.Hide()
		
				#Book Data
		self.bookPanel = wx.Panel(self, -1)
		bookDataSizer = wx.FlexGridSizer(4,2,7,15)
				# Labels
		label_ISBN  = wx.StaticText(self.bookPanel, label = "ISBN ")
		txtValueTitle  = wx.StaticText(self.bookPanel, label = "Título ")
		label_Author  = wx.StaticText(self.bookPanel, label = "Autor ")
		label_BookStatus  = wx.StaticText(self.bookPanel, label = "Prestado ")
				# Fields
		self.txtValueISBN = wx.StaticText(self.bookPanel, label ='')
		self.txtValueTitleo = wx.StaticText(self.bookPanel)
		self.txtValueAuthor = wx.StaticText(self.bookPanel)
		self.label_BookStatuso = wx.StaticText(self.bookPanel)
		bookDataSizer.AddMany([(label_ISBN      , 0),(self.txtValueISBN      , 0),
		               (txtValueTitle     , 0),(self.txtValueTitleo     , 0),
		               (label_Author    , 0),(self.txtValueAuthor    , 0),
		               (label_BookStatus, 0),(self.label_BookStatuso, 0)])
		self.bookPanel.SetSizer(bookDataSizer)
		self.bookPanel.Hide()

		bookDataZiser.AddMany([(self.bookPanel, 1), (wx.StaticLine(self, -1, style=wx.LI_VERTICAL),1,wx.ALIGN_CENTER_HORIZONTAL ),(self.userPanel, 1)])

		btPt = wx.Button(self, label = "Prestar")

		fgsCal = wx.FlexGridSizer(3,2,10,20)

		label_LoanDate = wx.StaticText(self, label = "Fecha de Préstamo")
		font = label_LoanDate.GetFont()
		font.SetWeight(wx.BOLD)
		label_LoanDate.SetFont(font)
		self.calendar_LoanDay = cal.CalendarCtrl(self, -1, wx.DateTime.Today())
		self.calendar_LoanDay.EnableMonthChange(False)
		self.calendar_LoanDay.EnableHolidayDisplay()

		label_DueDate = wx.StaticText(self, label = "Fecha de Entrega")
		label_DueDate.SetFont(font)
		self.calendar_DueDate = cal.CalendarCtrl(self, -1, wx.DateTime_Now(), style = cal.CAL_NO_YEAR_CHANGE)
		self.calendar_DueDate.EnableMonthChange(True)
		self.calendar_DueDate.EnableHolidayDisplay()

		default_loan_span = wx.DateSpan.Days(14)
		today = wx.DateTime_Now()
		default_return_date = today.AddDS(default_loan_span)		#modifica today
		self.calendar_DueDate.SetDate(default_return_date)

		fgsCal.AddMany([(label_LoanDate, 1, wx.ALIGN_CENTER_HORIZONTAL), (label_DueDate, 1, wx.ALIGN_CENTER_HORIZONTAL, 0),
		               (self.calendar_LoanDay, 1, wx.ALIGN_CENTER_HORIZONTAL), (self.calendar_DueDate, 1, wx.ALIGN_CENTER_HORIZONTAL)])
		fgsCal.AddGrowableCol(0)
		fgsCal.AddGrowableCol(1)
		fgsCal.AddGrowableRow(1)

		but_searchbook.Bind(wx.EVT_BUTTON, self.OnSelecBook)
		but_searchuser.Bind(wx.EVT_BUTTON, self.OnSelecUser)
		btPt.Bind(wx.EVT_BUTTON, self.OnLoan)
		#calendario dia actual: dia del prestamo
		self.calendar_LoanDay.Bind(cal.EVT_CALENDAR, self.OnHoyMove)						#Locking all possible movement of today's date.
		self.calendar_LoanDay.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnHoyMove)
		self.calendar_LoanDay.Bind(cal.EVT_CALENDAR_DAY, self.OnHoyMove)
		#caledario dia retorno
		self.calendar_DueDate.Bind(cal.EVT_CALENDAR, self.OnFutMove)						#Locking all possible movement of today's date.
		self.calendar_DueDate.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnFutMove)
		self.calendar_DueDate.Bind(cal.EVT_CALENDAR_DAY, self.OnFutMove)
		
		verticalBox.Add(fgs, 0, wx.EXPAND)
		verticalBox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		verticalBox.Add(bookDataZiser, 0, wx.EXPAND)
		verticalBox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		verticalBox.Add(fgsCal, 0, wx.EXPAND)
		verticalBox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		verticalBox.Add(btPt, 0 , wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
		self.SetSizer(verticalBox)
		self.Hide()

	def OnSelecBook(self, e):
		self.books     = self.DBmanager.load_table('libros')
		mSearchWindows.SearchBook(self, 2,self.books)	#2: Mostrar solo libros disponibles

	def OnSelecUser(self, e):
		self.users     = self.DBmanager.load_table('usuarios')
		mSearchWindows.SearchUser(self, 1,self.users)	#1: Mostrar solo usuarios activos.

	def RecieveIdn(self, data, tipo):

		if tipo == 'book':
			self.book = self.validarLibro(data)
			if self.book:
				self.txtfield_bookId.SetValue(str(self.book['id_libro']))
				self.llenarDatosLibro()

		elif tipo == 'user':
			self.user = self.validarUser(data)
			if self.user:
				self.txtfield_userId.SetValue(str(self.user['id_usuario']))
				self.llenarDatosUsuario()

	def llenarDatosLibro(self):

		self.txtValueISBN.SetLabel(self.book['isbn'])
		self.txtValueTitleo.SetLabel(self.book['titulo'])
		self.txtValueAuthor.SetLabel(self.book['autor'])
		if self.book['estado']:
			self.label_BookStatuso.SetLabel(label = "Si")
		else: self.label_BookStatuso.SetLabel("No")
		self.bookPanel.Layout()
		self.bookPanel.Show()
		self.Layout()
		
	def	llenarDatosUsuario(self):
		self.txtValueUserName.SetLabel(self.user['nombres'])
		self.txtValueUserFamilyName.SetLabel(self.user['apellidos'])
		if self.user['estado']:
			self.txtValueUserStatus.SetLabel("Activo")
		else:
			self.txtValueUserStatus.SetLabel("Inactivo")
		self.userPanel.Layout()
		self.userPanel.Show()
		self.Layout()

	def OnHoyMove(self, e):
		#Todos los posibles cambios de fecha en calendar_LoanDay están bloqueados.
		self.calendar_LoanDay.SetDate(wx.DateTime_Now())
		
	def OnFutMove(self, e):
		un_dia = wx.DateSpan.Days(1)
		today = wx.DateTime_Now()
		manana = today.AddDS(un_dia)		#modifica today
		
		if (self.calendar_DueDate.GetDate().IsEarlierThan(manana)):		#Si la fecha es anterior a mañana, automáticamente se corre a mañana. 
			self.calendar_DueDate.SetDate(manana)

	def validarUser(self, user):
		if user:
			if not ( 'estado' in user.keys()) or not user['estado']:
				Iface.showmessage('El usuario seleccionado no puede recibir libros ya que se encuentra bloqueado.',"Bloqueado")
				return False
			return user
		Iface.showmessage('Usuario no valido.',"Error")
		return False

	def validarLibro(self, libro):
		if libro:
			if not ('estado' in libro.keys()) or libro['estado']:
				Iface.showmessage('El Libro que seleccionado ya se encuentra prestado.',"Prestado")
				return False
			return libro
		Iface.showmessage('Libro no valido.',"Error")
		return False

	def validateLoan(self):

		if not self.validarUser(self.user):
			return False
		if not self.validarLibro(self.book):
			return False
		if not self.checkdate(self.calendar_LoanDay.PyGetDate(),self.calendar_DueDate.PyGetDate()):
			return False

		return [self.book['id_libro'],self.user['id_usuario'],self.desde,self.hasta]

	def checkdate(self,desde,hasta):
		self.desde = date2int(desde)
		self.hasta = date2int(hasta)

		if isweekend(hasta):
			Iface.showmessage('El dia de retorno no puede ser Fin de semana','Período Invalido')
			return False

		if self.desde>self.hasta:
			Iface.showmessage('El dia de retorno debe ser posterior al dia de prestamo.','Período Invalido')
			return False

		return True

	def OnLoan(self, e):
		#segunda validacion de los parametros de usuario y libro,
		#tambien obtiene los parametros para prestar
		self.data_loan = self.validateLoan()

		if not self.data_loan:
			Iface.showmessage('Se encontró un problema al prestar libros.\nPrestamo cancelado.',"Prestamo")
			return

		self.saving = self.DBmanager.loanbook(*self.data_loan)
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
		self.txtfield_bookId.SetValue('')
		self.txtfield_userId.SetValue('')
		self.txtValueUserName.SetLabel('')
		self.txtValueUserFamilyName.SetLabel('')
		self.txtValueUserStatus.SetLabel('')
		self.txtValueISBN.SetLabel('')
		self.txtValueTitleo.SetLabel('')
		self.txtValueAuthor.SetLabel('')

class DummyFrame(wx.Frame):
	def __init__(self,parent):
		super(DummyFrame, self).__init__(parent = parent, size=(700, 500)) 
		verticalBox = wx.BoxSizer(wx.VERTICAL)
		panel = LoanBook(self, self.GetSize())
		verticalBox.Add(panel, 2, wx.EXPAND)
		panel.Show()
		self.SetSizer(verticalBox)
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
