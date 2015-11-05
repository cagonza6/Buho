# -*- coding: utf-8 -*-
import datetime

from PyQt4 import QtGui, QtCore

from Gui.mLoanReturnBook import Ui_LoanReturn
from common import flag, flagStatus
from Search import SearchItemWin, SearchUserWin
from Tools import validations
from Tools.Database import DBManager as DataBase
from Tools.timeFunctions import date2int, int2date, addDays, searchNoWeekend, todaysDate
import config.GlobalConstants as Constants
import session.Session as Session
from Classes import Reader, Item, Loan
from InfoWindows import ShowInfo
from common import _translate


class LoanReturnMaster(QtGui.QWidget, Ui_LoanReturn, ShowInfo):
	def __init__(self, parent=None):
		super(LoanReturnMaster, self).__init__()

		self.setupUi(self)

		# Actions
		self.connect(self.field_itemID, QtCore.SIGNAL("textChanged(QString)"), self.OnChangeItemID)
		self.connect(self.field_readerID, QtCore.SIGNAL("textChanged(QString)"), self.OnChangeReaderID)
		self.connect(self.calendarDueDay, QtCore.SIGNAL("clicked(QDate)"), self.getDueDate)

		# Buttons
		self.connect(self.buttonSearchBook, QtCore.SIGNAL("clicked()"), self.searchItem_)
		self.connect(self.buttonSearchReader, QtCore.SIGNAL("clicked()"), self.searchReader_)
		self.connect(self.button_loadItem, QtCore.SIGNAL("clicked()"), self.loadItem)
		self.connect(self.button_loadReader, QtCore.SIGNAL("clicked()"), self.loadReader)
		self.connect(self.buttonAction, QtCore.SIGNAL("clicked()"), self.handleButton)

		# Proper dates for the calendars
		self.setCalendarToday()
		self.setCalendarDueDate()

		self.resetall()
		self.cheackall()

	#
	# Dates and Calendar Methods
	#
	def setCalendarDueDate(self, duedate=False):
		today = datetime.datetime.now()
		self.calendarDueDay.setMinimumDate(QtCore.QDate(today.year, today.month, today.day))
		if duedate:
			dueDate = int2date(duedate)
		else:
			dueDate = self.generateMaxDueDate()
			# duedate is limited by the maximum of span days acoording to the acoount
			# TO-DO: set by account type
			self.calendarDueDay.setMaximumDate(QtCore.QDate(dueDate.year, dueDate.month, dueDate.day))
		self.calendarDueDay.setSelectedDate(QtCore.QDate(dueDate.year, dueDate.month, dueDate.day))

	def setCalendarToday(self):
		today = datetime.datetime.now()
		# todays calendar is limited to the date of today
		self.calendarToday.setSelectedDate(QtCore.QDate(today.year, today.month, today.day))

	def getDueDate(self):
		duedate = self.calendarDueDay.selectedDate().toPyDate()
		duedate = searchNoWeekend(duedate)
		self.calendarDueDay.setSelectedDate(QtCore.QDate(duedate.year, duedate.month, duedate.day))
		dueDate = date2int(duedate)
		return dueDate

	def generateMaxDueDate(self):
		today = datetime.date.today()
		duedate = today + addDays(Constants.LOAN_SPAN)
		duedate = searchNoWeekend(duedate)
		return duedate

	#
	# Check Process
	#
	def cheackall(self):
		self.checkID(Constants.TYPE_USER)
		self.checkID(Constants.TYPE_ITEM)

	#
	# Reset and clean Data Methods
	#
	def resetReader(self):
		self.reader = False
		self.cleanReader()

	def resetItem(self):
		self.item = False
		self.cleanItem()

	def resetLoan(self):
		self.loan = False

	def resetall(self):
		self.resetItem()
		self.resetReader()
		self.resetLoan()

	def cleanReader(self):
		self.label_field_name.setText('')
		self.label_reader_role.setText('')
		self.label_field_rederloans.setText('')
		self.label_field_delays.setText('')
		self.label_field_userStatus.setText('')
		flag(self.check_loans, False)
		flag(self.check_delay, False)
		flag(self.check_userID, False)

	def cleanItem(self):
		self.label_field_isbn.setText('')
		self.label_field_title.setText('')
		self.label_field_author.setText('')
		self.label_field_lang.setText('')
		self.label_field_itemStatus.setText('')
		flag(self.check_itemID, False)

	def cleanall(self):
		self.field_itemID.setText('')
		self.field_readerID.setText('')
		self.cleanReader()
		self.cleanItem()

	#
	# Item check process
	#
	def loadItem(self):
		self.loadElement(Constants.TYPE_ITEM)

	def loadReader(self):
		self.loadElement(Constants.TYPE_USER)

	def loadElement(self, type_=False):
		id_, aux = self.checkID(type_)
		if not id_:
			return False
		if type_ == Constants.TYPE_ITEM:
			item = Item(id_)
			if not item.formatID() == aux:
				return False
			self.showItemInfo(item)
			self.checkItem(item)
		elif type_ == Constants.TYPE_USER:
			reader = Reader(id_)
			if not reader.role() == aux:
				return False
			self.showReaderInfo(reader)
			self.checkReader(reader)

	#
	# ID related methods
	#
	def OnChangeReaderID(self):
		self.resetReader()
		self.checkID(Constants.TYPE_USER)


	def OnChangeItemID(self):
		self.resetItem()
		self.checkID(Constants.TYPE_ITEM)

	def checkID(self, type_):
		id_, ident = False, False
		if type_ == Constants.TYPE_ITEM:
			aux = unicode(self.field_itemID.text()).strip()
			id_, ident = validations.validate(Constants.IDS, aux, Session.FORMAT_TYPE_INFO)
			flag(self.check_itemID, id_)
		elif type_ == Constants.TYPE_USER:
			aux = unicode(self.field_readerID.text()).strip()
			id_, ident = validations.validate(Constants.IDS, aux, Session.ROLES_INFO)
			flag(self.check_userID, id_)
		return id_, ident

	#
	# Hide Main button
	#
	def showbutton(self, show):
		if show:
			self.buttonAction.show()
		else:
			self.buttonAction.hide()

	#
	# Load Loan
	#
	def loadLoan(self, upadteCalendar, type_, id_):
		if not id_ or not type_:
			return False
		if type_ == Constants.TYPE_ITEM:
			self.loan = Loan(Constants.TYPE_ITEM, id_)
		elif type_ == Constants.TYPE_LOAN:
			self.loan = Loan(Constants.TYPE_LOAN, id_)
		if upadteCalendar:
			self.setCalendarDueDate(self.loan.dueDate())
		self.loadReader(self.loan.userID())

	#
	# Search Element
	#
	def searchElement(self, type_, status):
		# Select the type of search window
		if type_ == Constants.TYPE_USER:
			Searcher = SearchUserWin(True, status, self)
		elif type_ == Constants.TYPE_ITEM:
			Searcher = SearchItemWin(True, status, self)
		Searcher.exec_()
		# After closing the dialog search for the Id of the object to be shown
		ID = Searcher.ID
		if type_ == Constants.TYPE_USER:
			if ID:
				self.field_readerID.setText(ID)
				self.loadElement(Constants.TYPE_USER)
			else:
				self.cleanReader()
		elif type_ == Constants.TYPE_ITEM:
			if ID:
				self.field_itemID.setText(ID)
				self.loadElement(Constants.TYPE_ITEM)
			else:
				self.cleanItem()


class LoanItem(LoanReturnMaster):
	def __init__(self, parent=None):
		super(LoanItem, self).__init__()

	def searchItem_(self):
		self.searchElement(Constants.TYPE_ITEM, Constants.AVAILABLE_ITEMS)

	def searchReader_(self):
		self.searchElement(Constants.TYPE_USER, Constants.AVAILABLE_USERS)

	def checkReader(self, reader=False):
		result = reader
		self.label_field_userStatus.setText("Can Loan")
		flag(self.check_loans, True)
		flag(self.check_delay, True)

		if reader:
			if reader.status() == Constants.STATUS_INVALID:
				QtGui.QMessageBox.critical(self, 'Error', 'Reader status is Blocked.', QtGui.QMessageBox.Ok)
				result = False
			if reader.status() == Constants.BANED_USER:
				QtGui.QMessageBox.critical(self, 'Error', 'Reader status is Banned.', QtGui.QMessageBox.Ok)
				result = False

			if reader.loans() >= Constants.ST_MAX_LOANS:
				QtGui.QMessageBox.critical(self, 'Error', 'Reader can not loan more than ' + str(Constants.ST_MAX_LOANS) + ' items.', QtGui.QMessageBox.Ok)
				flagStatus(self.check_loans, Constants.STATUS_WARNING)
				result = False

			if reader.delays():
				QtGui.QMessageBox.critical(self, 'Error', 'Reader has a delay in [' + str(reader.delays()) + '] items.', QtGui.QMessageBox.Ok)
				result = False
				flagStatus(self.check_delay, Constants.STATUS_WARNING)

		flag(self.check_user, result)
		if not result:
			self.label_field_userStatus.setText("Can not Loan")
		self.reader = result
		self.showbutton(result)

	def checkItem(self, item=False):
		result = item
		self.label_field_itemStatus.setText("Can not be Loaned")
		if item:
			if item.loaned():
				QtGui.QMessageBox.critical(self, 'Error', 'Item is loaned.', QtGui.QMessageBox.Ok)
				self.label_field_itemStatus.setText("Is Loaned")
				result = False
			else:
				self.label_field_itemStatus.setText("Can be Loaned")
		flag(self.check_item, result)
		self.item = result
		self.showbutton(result)

	def handleButton(self):
		if not self.item or not self.reader:
			loanData = [False, False, False, False]
		else:
			loanData = [
				self.item.ID(),
				self.reader.ID(),
				todaysDate(),  # loan date is always "today", when the item is given
				self.getDueDate()
			]

		if (False in loanData):
			QtGui.QMessageBox.critical(self, 'Error', 'There is information Missing or wrong.', QtGui.QMessageBox.Ok)
		else:
			saved = DataBase.loanItem(*loanData)
			if saved:
				QtGui.QMessageBox.information(self, 'Sucess', 'Item Loaned.', QtGui.QMessageBox.Ok)
				self.resetall()
				self.cleanall()
				self.cheackall()
			else:
				QtGui.QMessageBox.critical(self, 'Error', 'Error while Loaning.', QtGui.QMessageBox.Ok)

	def loadLoan(self, upadteCalendar, type_, ID):
		pass


class ReturnItem(LoanReturnMaster):
	def __init__(self, parent=None):
		super(ReturnItem, self).__init__()

		# Proper dates for the calendars
		self.setCalendarToday()

		# hide non required elements from the Window
		self.hideElements()
		self.retranslateUi2()

	#
	# ID related methods
	#
	def OnChangeItemID(self):
		self.checkID(Constants.TYPE_ITEM)
		self.resetItem()
		self.resetReader()

	def searchReader_():
		pass

	def OnChangeReaderID():
		pass

	def loadReader(self, id_):
		if not id_:
			return
		reader = Reader(id_)
		self.showReaderInfo(reader)
		self.checkReader(reader)

	def searchItem_(self):
		self.searchElement(Constants.TYPE_ITEM, Constants.LOANED_ITEMS)

	def hideElements(self):
		self.button_loadReader.hide()
		self.buttonSearchReader.hide()
		self.check_userID.hide()
		self.field_readerID.hide()
		self.label_readerID.hide()

	def checkReader(self, reader=False):
		result = reader
		self.label_field_userStatus.setText("Can Loan")
		flag(self.check_loans, result)
		flag(self.check_delay, result)

		if reader:
			if reader.loans() >= Constants.ST_MAX_LOANS:
				result = False
				flagStatus(self.check_loans, Constants.STATUS_WARNING)

			if reader.delays():
				QtGui.QMessageBox.warning(self, 'Error', 'Reader has a delay in [' + str(reader.delays()) + '] items.', QtGui.QMessageBox.Ok)
				flagStatus(self.check_delay, Constants.STATUS_WARNING)
				result = False

		if not result:
			self.label_field_userStatus.setText("Can not Loan")

		flag(self.check_user, result)
		self.reader = result
		self.showReaderInfo(result)
		self.showbutton(result)

	def checkItem(self, item):
		result = item
		self.label_field_itemStatus.setText("Not Loaned")
		if item:
			if not item.loaned():
				QtGui.QMessageBox.critical(self, 'warning', 'Item is not loaned.', QtGui.QMessageBox.Ok)
				self.label_field_itemStatus.setText("Can not be retrieved")
				result = False
			else:
				self.label_field_itemStatus.setText("Can be retrieved")
		flag(self.check_item, result)

		self.item = result
		if result:
			self.loadLoan(True, Constants.TYPE_ITEM, item.ID())
		# the call to load user is done from loadLoan
		self.showbutton(result)

	def handleButton(self):
		if not self.loan:
			returnData = [False, False]
		else:
			returnData = [
				todaysDate(),
				self.loan.ID()
			]

		if (False in returnData):
			QtGui.QMessageBox.critical(self, 'Error', 'There is information Missing or wrong.', QtGui.QMessageBox.Ok)
		else:
			saved = DataBase.returnItem(*returnData)
			if saved:
				QtGui.QMessageBox.information(self, 'Sucess', 'Item retrieved.', QtGui.QMessageBox.Ok)
				self.resetall()
				self.cleanall()
				self.cheackall()
			else:
				QtGui.QMessageBox.critical(self, 'Error', 'Error while retrieving.', QtGui.QMessageBox.Ok)

	def retranslateUi2(self):
		self.groupCalendarLoanDate.setTitle(_translate("LoanReturn", "Loan Date", None))
		self.buttonAction.setText(_translate("LoanReturn", "Return", None))
		self.label_MainTitle.setText(_translate("LoanReturn", "Return Item", None))


class RenewItem(LoanReturnMaster):
	def __init__(self, parent=None):
		super(RenewItem, self).__init__()

		# hide non required elements from the Window
		self.hideElements()
		self.retranslateUi2()

	#
	# ID related methods
	#
	def OnChangeItemID(self):
		self.checkID(Constants.TYPE_ITEM)
		self.resetItem()
		self.resetReader()

	def searchReader_():
		pass

	def OnChangeReaderID():
		pass

	def loadItem(self):
		self.loadElement()

	def searchItem_(self):
		self.searchElement(Constants.TYPE_ITEM, Constants.LOANED_ITEMS)

	def hideElements(self):
		self.button_loadReader.hide()
		self.buttonSearchReader.hide()
		self.check_userID.hide()
		self.field_readerID.hide()
		self.label_readerID.hide()

	def checkReader(self, reader):
		result = reader
		self.label_field_userStatus.setText("Can not renew")
		if reader:

			if reader.status() == Constants.STATUS_INVALID:
				QtGui.QMessageBox.critical(self, 'Error', 'Reader status is Blocked.', QtGui.QMessageBox.Ok)
				result = False
			if reader.status() == Constants.BANED_USER:
				QtGui.QMessageBox.critical(self, 'Error', 'Reader status is Banned.', QtGui.QMessageBox.Ok)
				result = False

			if reader.loans() >= Constants.ST_MAX_LOANS:
				flagStatus(self.check_loans, Constants.STATUS_WARNING)
			if reader.delays():
				QtGui.QMessageBox.warning(self, 'Error', 'Reader has a delay in [' + str(reader.delays()) + '] items.', QtGui.QMessageBox.Ok)
				result = False
				flagStatus(self.check_delay, Constants.STATUS_WARNING)
		flag(self.check_user, result)
		self.reader = result
		if result:
			self.label_field_userStatus.setText("Can Renew")
		self.showbutton(result)

	def loadReader(self, id_):
		if not id_:
			return
		reader = Reader(id_)
		self.showReaderInfo(reader)
		self.checkReader(reader)

	def checkItem(self, item=False):
		result = item
		self.label_field_itemStatus.setText("Can be renewed.")
		self.label_field_itemStatus.setText('')
		if item:
			if not item.loaned():
				QtGui.QMessageBox.critical(self, 'warning', 'Item is not loaned.', QtGui.QMessageBox.Ok)
				result = False
			else:
				self.label_field_itemStatus.setText("Can be retrieved")
			if item.renewals() >= Constants.RENEWAL_LIMIT:
				QtGui.QMessageBox.critical(self, 'warning', 'Limit of Renewals reached.', QtGui.QMessageBox.Ok)
				result = False

			self.loadLoan(False, Constants.TYPE_ITEM, item.ID())
			# the call to load user is done from loadLoan

			if self.loan.dueDate() > self.getDueDate():
				QtGui.QMessageBox.critical(self, 'warning', 'Renewal Date must be after than the actual due date. To modify the Date use Edit loan.', QtGui.QMessageBox.Ok)
				result = False
		if not result:
			self.label_field_itemStatus.setText("Can not be renewed.")
		flag(self.check_item, result)
		self.item = result
		self.showbutton(result)

	def handleButton(self):
		if not self.item or not self.reader:
			returnData = [False, False]
		else:
			returnData = [
				self.getDueDate(),
				self.loan.ID()
			]
		if (False in returnData):
			QtGui.QMessageBox.critical(self, 'Error', 'There is information Missing or wrong.', QtGui.QMessageBox.Ok)
		else:
			saved = DataBase.renewItem(*returnData)
			if saved:
				QtGui.QMessageBox.information(self, 'Sucess', 'Item Renewed.', QtGui.QMessageBox.Ok)
				self.resetall()
				self.cleanall()
				self.cheackall()
			else:
				QtGui.QMessageBox.critical(self, 'Error', 'Error while retrieving.', QtGui.QMessageBox.Ok)

	def retranslateUi2(self):
		self.groupCalendarLoanDate.setTitle(_translate("LoanReturn", "Today", None))
		self.buttonAction.setText(_translate("LoanReturn", "Renew", None))
		self.label_MainTitle.setText(_translate("LoanReturn", "Renew Item", None))
