#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to loan a book

import wx
import cfg
import mSearchWindows
import wx.calendar as cal
from Tools.sqlite import DatabaseManager                                # Database functions
from Tools.calendar import date2int, isweekend, int2date, daysbetween   # Calendar tools
from Tools.calendar import oneDay, date2DMY                             # Calendar tools
import Tools.interface as Iface                                         # Screen Dialogs


MIN_LOAN_SPAN     = 0
LOAN_SPAN         = 14
MAX_LOAN_SPAN     = 28
LOANS_ALERT       = 2
MAX_LOANS_ALLOWED = 4

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
		but_Loan = wx.Button(self, label       = "Prestar")

		self.inputField_bookId = wx.TextCtrl(self)
		self.inputField_userId = wx.TextCtrl(self)
		fgs.AddMany([(but_searchbook, 0),
                     (self.inputField_bookId, 1, wx.EXPAND),
                     (but_searchuser, 0),
                     (self.inputField_userId, 1, wx.EXPAND)])
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
		label_ISBN    = wx.StaticText(self.bookPanel,     label = "ISBN ")
		txtValueTitle = wx.StaticText(self.bookPanel,     label = "Título ")
		label_Author  = wx.StaticText(self.bookPanel,     label = "Autor ")
		label_BookStatus  = wx.StaticText(self.bookPanel, label = "Prestado ")
				# Fields
		self.txtValueISBN = wx.StaticText(self.bookPanel, label ='')
		self.txtValueTitle = wx.StaticText(self.bookPanel)
		self.txtValueAuthor = wx.StaticText(self.bookPanel)
		self.label_BookStatuso = wx.StaticText(self.bookPanel)
		bookDataSizer.AddMany([(label_ISBN      , 0),(self.txtValueISBN      , 0),
		               (txtValueTitle     , 0),(self.txtValueTitle     , 0),
		               (label_Author    , 0),(self.txtValueAuthor    , 0),
		               (label_BookStatus, 0),(self.label_BookStatuso, 0)])
		self.bookPanel.SetSizer(bookDataSizer)
		self.bookPanel.Hide()

		bookDataZiser.AddMany([(self.bookPanel, 1), 
                               (wx.StaticLine(self, -1, style=wx.LI_VERTICAL),1,wx.ALIGN_CENTER_HORIZONTAL ), # separator
                               (self.userPanel, 1)])

		calendarsSizer = wx.FlexGridSizer(3,2,10,20)

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

		self.dueDateReset()

		calendarsSizer.AddMany([(label_LoanDate, 1, wx.ALIGN_CENTER_HORIZONTAL), (label_DueDate, 1, wx.ALIGN_CENTER_HORIZONTAL, 0),
		               (self.calendar_LoanDay, 1, wx.ALIGN_CENTER_HORIZONTAL), (self.calendar_DueDate, 1, wx.ALIGN_CENTER_HORIZONTAL)])
		calendarsSizer.AddGrowableCol(0)
		calendarsSizer.AddGrowableCol(1)
		calendarsSizer.AddGrowableRow(1)

		# Button Events
		but_searchbook.Bind(wx.EVT_BUTTON, self.OnSelecBook)
		but_searchuser.Bind(wx.EVT_BUTTON, self.OnSelecUser)
		but_Loan.Bind(wx.EVT_BUTTON, self.OnLoan)

		# calendar: Loan Day - Events
		self.calendar_LoanDay.Bind(cal.EVT_CALENDAR, self.OnLoandayCalendarChange)                # locks every date modification: fix calendar
		self.calendar_LoanDay.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnLoandayCalendarChange)
		self.calendar_LoanDay.Bind(cal.EVT_CALENDAR_DAY, self.OnLoandayCalendarChange)
		# calendar: Due Day - Events
		self.calendar_DueDate.Bind(cal.EVT_CALENDAR, self.OnDueCalendarChange)
		self.calendar_DueDate.Bind(cal.EVT_CALENDAR_SEL_CHANGED, self.OnDueCalendarChange)
		self.calendar_DueDate.Bind(cal.EVT_CALENDAR_DAY, self.OnDueCalendarChange)
		
		verticalBox.Add(fgs, 0, wx.EXPAND)
		verticalBox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		verticalBox.Add(bookDataZiser, 0, wx.EXPAND)
		verticalBox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		verticalBox.Add(calendarsSizer, 0, wx.EXPAND)
		verticalBox.Add(wx.StaticLine(self, size = (1000,10), style = wx.LI_HORIZONTAL), 0, wx.ALL, 10)
		verticalBox.Add(but_Loan, 0 , wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
		self.SetSizer(verticalBox)
		self.Hide()

	# sets the calendar to the LOAN_SPAN from "today"
	def dueDateReset(self):
		today               = wx.DateTime_Now()
		default_loan_span   = wx.DateSpan.Days(LOAN_SPAN)
		self.default_return_date = today.AddDS(default_loan_span)            # doday + Loan periode
		self.calendar_DueDate.SetDate(self.default_return_date)              # updates Loan date to the calculated day

	def OnSelecBook(self, e):
		self.books     = self.DBmanager.load_table('libros')
		mSearchWindows.SearchBook(self, 2,self.books)	#2: Sow just available items

	def OnSelecUser(self, e):
		self.users     = self.DBmanager.load_table('usuarios')
		mSearchWindows.SearchUser(self, 1,self.users)	#1: Show just active users

	def RecieveIdn(self, data, tipo):

		if tipo == 'book':
			self.book = self.isBookValid(data)
			if self.book:
				self.inputField_bookId.SetValue(str(self.book['id_libro']))
				self.fillBookData()

		elif tipo == 'user':
			self.user = self.isUserValid(data)
			if self.user:
				self.inputField_userId.SetValue(str(self.user['id_usuario']))
				self.alertLoanNumber(data)
				self.fillUserData()


	def fillBookData(self):

		self.txtValueISBN.SetLabel(self.book['isbn'])
		self.txtValueTitle.SetLabel(self.book['titulo'])
		self.txtValueAuthor.SetLabel(self.book['autor'])
		if self.book['estado']:
			self.label_BookStatuso.SetLabel(label = "Si")
		else: self.label_BookStatuso.SetLabel("No")
		self.bookPanel.Layout()
		self.bookPanel.Show()
		self.Layout()
		
	def	fillUserData(self):
		self.txtValueUserName.SetLabel(self.user['nombres'])
		self.txtValueUserFamilyName.SetLabel(self.user['apellidos'])
		if self.user['estado']:
			self.txtValueUserStatus.SetLabel("Activo")
		else:
			self.txtValueUserStatus.SetLabel("Inactivo")
		self.userPanel.Layout()
		self.userPanel.Show()
		self.Layout()

	def OnLoandayCalendarChange(self, e):
		# Every date changes are blocked, the calendar returns to the date of "today"
		self.calendar_LoanDay.SetDate(wx.DateTime_Now())

	def OnDueCalendarChange(self, e):
		today    = wx.DateTime_Now()
		minSpan   = wx.DateSpan.Days(MIN_LOAN_SPAN)
		tomorrow = today.AddDS(minSpan)		#modifica today

		#If the due date is set before the date of loan, it bring the next possible day
		# or same day if due day is the loan day (min loan span =0)
		if ( self.calendar_DueDate.GetDate().IsEarlierThan(tomorrow) ):
			self.calendar_DueDate.SetDate(tomorrow)

	def alertLoanNumber(self, user):
		if LOANS_ALERT and user['number_loans']>=LOANS_ALERT:
			Iface.showmessage('El Lector seleccionado ya posee ['+str(user['number_loans'])+u'] libros\n de un máximo de ['+str(MAX_LOANS_ALLOWED)+'] permitidos.',u"Atención")

	def isdelayed(self,user):
		date    = date2int(self.calendar_LoanDay.PyGetDate())
		user_id = user['id_usuario']
		count = len(self.DBmanager.userDelayedBooks(user_id,date))
		return count

	def isUserValid(self, user):
		if user:
			if not ( 'estado' in user.keys()) or not user['estado']:
				Iface.showmessage('El usuario seleccionado no puede recibir libros ya que se encuentra bloqueado.',"Bloqueado")
				return False

			if user['number_loans']>=MAX_LOANS_ALLOWED:
				Iface.showmessage(u'Máximo número de prestmaos alcanzado ['+str(MAX_LOANS_ALLOWED)+']. \n Prestamo cancelado.',"Bloqueado")
				return False

			retrasos = self.isdelayed(user)
			if retrasos:
				Iface.showmessage(u'Usuario presenta retraso en ['+str(retrasos)+'] prestamos. \n Prestamo Cancelado',"Retrasos")
				return False
			return user

		Iface.showmessage('Usuario no valido.',"Error")
		return False

	def isBookValid(self, book):
		if book:
			if not ('estado' in book.keys()) or book['estado']:
				Iface.showmessage('El Libro que seleccionado ya se encuentra prestado.',"Prestado")
				return False
			return book
		Iface.showmessage('Libro no valido.',"Error")
		return False

	def isLoanValid(self):

		if not self.validateDueDate():
			return False
		if not self.user:
			Iface.showmessage('Usuario Invalido.',"Error")
			return False
		if not self.book:
			Iface.showmessage('Libro Invalido.',"Error")
			return False

		return [self.book['id_libro'],self.user['id_usuario'],date2int(self.LoanDate),date2int(self.dueDate)]


	# This method is ment to skipe the Weekends (and holidays, not yet implemented)
	# it starts from the already defined LOAN_SPAN days
	def searchDueDate(self):
		date0  = int2date(date2int(self.calendar_DueDate.PyGetDate()))
		while isweekend(date0):
			date0 +=oneDay()
		dmy = date2DMY(date0)
		wxdate=wx.DateTimeFromDMY(*dmy)

		return wxdate

	# This method cares about the validity of the day: not weekend
	# also alidates how long the Loan gets
	def validateDueDate(self):
		self.LoanDate = self.calendar_LoanDay.PyGetDate()
		self.dueDate  = self.calendar_DueDate.PyGetDate()

		if isweekend(self.dueDate):
			if not  Iface.cnt(u'El dia de retorno no puede ser Fin de semana', u'¿Desea cambiarlo al dia hábil siguiente?','Advertencia'):
				return False
		self.calendar_DueDate.SetDate(self.searchDueDate())
		self.dueDate  = self.calendar_DueDate.PyGetDate()

		diff = daysbetween(self.LoanDate,self.dueDate)
		if MAX_LOAN_SPAN and diff > MAX_LOAN_SPAN :
			Iface.showmessage(u'Prestamo de ['+str(diff)+'] dias.\n Prestamo no puede superar ['+str(MAX_LOAN_SPAN)+'] Dias.','Período Invalido')
			return False
		if diff > LOAN_SPAN :
			if not Iface.cnt('Prestamo de ['+str(diff)+'] dias.\n Superior a los estandar ['+str(LOAN_SPAN)+'] Dias.'):
				return False

		if self.LoanDate>self.dueDate:
			Iface.showmessage('El dia de retorno debe ser posterior al dia de prestamo.','Período Invalido')
			return False

		return True

	def OnLoan(self, e):
		# second validation of the parameters: user and book
		# Obtains the parameters to generate the loan
		self.data_loan = self.isLoanValid()

		if not self.data_loan:
			return

		self.saving = self.DBmanager.loanbook(*self.data_loan)
		if not self.saving:
			Iface.showmessage('Error al registrar el préstamo.',"Database")
		if self.saving:
			# Update the values of book and labels in order to clean the data and not loan the books twice
			self.book=False
			self.user=False
			self.dueDateReset()
			self.Clean()
			Iface.showmessage('Prestamo realizado con éxito.','Préstamos')
			return

	def Clean(self):
		self.inputField_bookId.SetValue('')
		self.inputField_userId.SetValue('')
		self.txtValueUserName.SetLabel('')
		self.txtValueUserFamilyName.SetLabel('')
		self.txtValueUserStatus.SetLabel('')
		self.txtValueISBN.SetLabel('')
		self.txtValueTitle.SetLabel('')
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
