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

		self.defaultItemsSearch = Constants.LOANED_ITEMS
		self.defaultReaderSearch = Constants.AVAILABLE_USERS
		self.setupUi(self)
		self.btn_delete.hide()
		# Id edits
		self.connect(self.field_itemID, QtCore.SIGNAL("textChanged(QString)"), self.OnChangeItemID)
		self.connect(self.field_readerID, QtCore.SIGNAL("textChanged(QString)"), self.OnChangeReaderID)
		self.connect(self.calendarDueDay, QtCore.SIGNAL("clicked(QDate)"), self.getDueDate)

		# Buttons
		self.connect(self.buttonSearchReader, QtCore.SIGNAL("clicked()"), self.searchReader_)
		self.connect(self.button_loadReader, QtCore.SIGNAL("clicked()"), self.loadReaderSearch)
		'''
		Actions for load item and search item are loaded using self.itemOpensLoan(bool) in order to
		identify them with one or another function.
		when bool = true :  the function is to open a window to load a loan and then the items and reader
		when bool = false:  the function is to open a the required windows for items and nothing else
		'''
		self.connect(self.buttonAction, QtCore.SIGNAL("clicked()"), self.handleButton)

		# Proper dates for the calendars
		self.setCalendarToday()
		self.setCalendarDueDate()

		self.resetall()
		self.cheackall()
		self.item = self.reader = False

	def itemOpensLoan(self, openLoan):
		if openLoan:
			self.connect(self.buttonSearchBook, QtCore.SIGNAL("clicked()"), self.SearchMasterId)
			self.connect(self.button_loadItem, QtCore.SIGNAL("clicked()"), self.MasterIdLoad)
		else:
			self.connect(self.buttonSearchBook, QtCore.SIGNAL("clicked()"), self.searchItem_)
			self.connect(self.button_loadItem, QtCore.SIGNAL("clicked()"), self.loadItem)

	def searchItem_(self):
		'''
		Used to call the dafault time of item in each window
		that varies from window to window
		'''
		item = self.searchElement(Constants.TYPE_ITEM, self.defaultItemsSearch)
		self.validateAndShow(Constants.TYPE_ITEM, item)

	def validateAndShow(self, type_, entity):
		if not entity:
			return
		if type_ == Constants.TYPE_ITEM:
			self.field_itemID.setText(entity.id2str())
			self.showItemInfo(entity)
			self.checkItem(entity)
		elif Constants.TYPE_USER:
			self.field_readerID.setText(entity.id2str())
			self.showReaderInfo(entity)
			self.checkReader(entity)

	def searchReader_(self):
		'''
		Used to call the dafault time of user in each window
		that varies from window to window
		'''
		reader = self.searchElement(Constants.TYPE_USER, self.defaultReaderSearch)
		self.validateAndShow(Constants.TYPE_USER, reader)

	def hideReaderSearch(self):
		self.button_loadReader.hide()
		self.buttonSearchReader.hide()
		self.check_userID.hide()
		self.field_readerID.hide()
		self.label_readerID.hide()

	# Dates and Calendar Methods
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

	# Check Process
	def cheackall(self):
		self.checkID(Constants.TYPE_USER)
		self.checkID(Constants.TYPE_ITEM)

	# Reset and clean Data Methods
	def resetReader(self):
		self.reader = False
		self.cleanReader()
		self.checkID(Constants.TYPE_USER)

	def resetItem(self):
		self.item = False
		self.cleanItem()
		self.checkID(Constants.TYPE_ITEM)

	def resetLoan(self):
		self.loan = False

	def resetall(self):
		self.resetItem()
		self.resetReader()
		self.resetLoan()

	def cleanReader(self):
		self.label_field_name.setText(Constants.EMPTY)
		self.label_reader_role.setText(Constants.EMPTY)
		self.label_field_rederloans.setText(Constants.EMPTY)
		self.label_field_delays.setText(Constants.EMPTY)
		self.label_field_userStatus.setText(Constants.EMPTY)
		flag(self.check_loans, False)
		flag(self.check_delay, False)
		flag(self.check_userID, False)

	def cleanItem(self):
		self.label_field_isbn.setText(Constants.EMPTY)
		self.label_field_title.setText(Constants.EMPTY)
		self.label_field_author.setText(Constants.EMPTY)
		self.label_field_lang.setText(Constants.EMPTY)
		self.label_field_itemStatus.setText(Constants.EMPTY)
		self.field_renewals.setText('-')
		flag(self.check_itemID, False)

	def cleanall(self):
		self.field_itemID.setText(Constants.EMPTY)
		self.field_readerID.setText(Constants.EMPTY)
		self.cleanReader()
		self.cleanItem()

	# Item check process
	def loadItem(self):
		item = self.loadElement(Constants.TYPE_ITEM)
		self.validateAndShow(Constants.TYPE_ITEM, item)

	def loadReaderID(self, id_):
		if not id_:
			return False
		reader = Reader(id_)
		if not reader.Data:
			reader = False
		return reader

	def loadItemID(self, id_):
		if not id_:
			return False
		item = Item(id_)
		if not item.Data:
			item = False
		return item

	def loadReaderSearch(self):
		reader = self.loadElement(Constants.TYPE_USER)
		self.validateAndShow(Constants.TYPE_USER, reader)

	def loadLoan(self, type_, id_):
		if not id_ or not type_:
			return False
		loan = Loan(Constants.TYPE_ITEM, id_)
		if not loan.Data:
			loan = False
		self.loan = loan
		return loan

	def loadElement(self, type_):
		element = False
		if not type_:
			return
		id_, aux = self.checkID(type_)
		if not id_:
			return False
		if type_ == Constants.TYPE_ITEM:
			element = self.loadItemID(id_)
			if not element.formatID() == aux:
				return False
		elif type_ == Constants.TYPE_USER:
			element = self.loadReaderID(id_)
			if not element.role() == aux:
				return False
		return element

	# ID related methods
	def OnChangeReaderID(self):
		self.resetReader()
		self.checkID(Constants.TYPE_USER)

	def OnChangeItemID(self):
		self.resetItem()
		self.checkID(Constants.TYPE_ITEM)
		self.OnChangeItemID_hook()

	def OnChangeItemID_hook(self):
		pass

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

	# Hide Main button
	def showActionbutton(self, show):
		if show:
			self.buttonAction.show()
		else:
			self.buttonAction.hide()

	# Search Element
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
			else:
				self.cleanReader()
		elif type_ == Constants.TYPE_ITEM:
			if ID:
				self.field_itemID.setText(ID)
			else:
				self.cleanItem()

		return self.loadElement(type_)

	def MasterIdLoad(self, id_txt=False):
		if not id_txt:
			id_txt = unicode(self.field_itemID.text()).strip()
		id_, ident = validations.validate(Constants.IDS, id_txt, Session.FORMAT_TYPE_INFO)
		loan = self.loadLoan(Constants.TYPE_ITEM, id_)
		if not loan:
			QtGui.QMessageBox.critical(self, 'warning', 'Loan information not found. \nMake sure you selected a loaned item.', QtGui.QMessageBox.Ok)
			return

		# opens the related item
		item = self.loadItemID(loan.itemID())
		reader = self.loadReaderID(loan.userID())

		if not reader or not item:
			return

		self.item0 = item
		self.validateAndShow(Constants.TYPE_ITEM, item)

		# opens the related reader
		self.reader0 = reader
		self.validateAndShow(Constants.TYPE_USER, reader)

	def SearchMasterId(self):
		# Select the type of search window
		Searcher = SearchItemWin(True, Constants.LOANED_ITEMS, self)
		Searcher.exec_()
		# After closing the dialog search for the Id of the object to be shown
		id_txt = Searcher.ID
		if not id_txt:
			return
		self.field_itemID.setText(id_txt)
		self.MasterIdLoad(id_txt)


class LoanItem(LoanReturnMaster):
	def __init__(self, parent=None):
		super(LoanItem, self).__init__()

		self.defaultItemsSearch = Constants.AVAILABLE_ITEMS
		self.defaultReaderSearch = Constants.AVAILABLE_USERS
		self.itemOpensLoan(False)

	def checkReader(self, reader):
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
				QtGui.QMessageBox.critical(self, 'Error', 'Reader can not loan more than [%s] items.' % (str(Constants.ST_MAX_LOANS), ), QtGui.QMessageBox.Ok)
				flagStatus(self.check_loans, Constants.STATUS_WARNING)
				result = False

			if reader.delays():
				QtGui.QMessageBox.critical(self, 'Error', 'Reader has a delay in [%s] items.' % (str(reader.delays()), ), QtGui.QMessageBox.Ok)
				result = False
				flagStatus(self.check_delay, Constants.STATUS_WARNING)

		flag(self.check_user, result)
		if not result:
			self.label_field_userStatus.setText("Can not Loan")
		self.reader = result
		self.showActionbutton(result)

	def checkItem(self, item):
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
		self.showActionbutton(result)

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

	def loadLoan(self, type_, ID, upadteCalendar):
		pass


class ReturnItem(LoanReturnMaster):
	def __init__(self, id_, parent=None):
		super(ReturnItem, self).__init__()
		self.defaultItemsSearch = Constants.LOANED_ITEMS
		self.defaultReaderSearch = Constants.AVAILABLE_USERS
		self.itemOpensLoan(True)

		# Proper dates for the calendars
		self.setCalendarToday()

		# hide non required elements from the Window
		self.hideReaderSearch()
		self.retranslateUi2()
		if id_:
			self.MasterIdLoad(id_)

	# ID related methods
	def searchReader_(self):
		pass

	def OnChangeReaderID(self):
		pass

	def checkReader(self, reader):
		self.label_field_userStatus.setText("Can Return Items")
		flag(self.check_loans, reader)
		flag(self.check_delay, reader)
		flag(self.check_user, reader)

		if reader:
			if reader.loans() >= Constants.ST_MAX_LOANS:
				flagStatus(self.check_loans, Constants.STATUS_WARNING)
			if reader.delays():
				flagStatus(self.check_delay, Constants.STATUS_WARNING)
		self.showActionbutton(True)

	def checkItem(self, item):
		self.label_field_itemStatus.setText("Item Not Loaned")
		flag(self.check_item, item)
		if item:
			if not item.loaned():
				self.label_field_itemStatus.setText("Item not loaned.")
			else:
				self.label_field_itemStatus.setText("Nothing to do.")

		# the call to load user is done from loadLoan
		self.showActionbutton(True)

	def handleButton(self):
		if not self.loan:
			returnData = False
		else:
			returnData = self.loan.ID()

		if (not returnData):
			QtGui.QMessageBox.critical(self, 'Error', 'There is information Missing or wrong.', QtGui.QMessageBox.Ok)
		else:
			saved = DataBase.returnItem(returnData)
			if saved:
				QtGui.QMessageBox.information(self, 'Sucess', 'Item Returned.', QtGui.QMessageBox.Ok)
				self.resetall()
				self.cleanall()
				self.cheackall()
			else:
				QtGui.QMessageBox.critical(self, 'Error', 'Error while Returned.', QtGui.QMessageBox.Ok)

	def retranslateUi2(self):
		self.groupCalendarLoanDate.setTitle(_translate("LoanReturn", "Loan Date", None))
		self.buttonAction.setText(_translate("LoanReturn", "Return", None))
		self.title.setText(_translate("LoanReturn", "Return Item", None))


class RenewItem(LoanReturnMaster):
	def __init__(self, parent=None):
		super(RenewItem, self).__init__()
		self.itemOpensLoan(True)
		self.defaultItemsSearch = Constants.LOANED_ITEMS
		self.defaultReaderSearch = Constants.AVAILABLE_USERS

		# hide non required elements from the Window
		self.hideReaderSearch()
		self.retranslateUi2()

	# ID related methods
	def OnChangeItemID_hook(self):
		self.resetReader()
		self.checkID(Constants.TYPE_USER)

	def checkReader(self, reader):
		result = reader
		self.label_field_userStatus.setText("Can not renew")
		flag(self.check_loans, reader)
		flag(self.check_delay, reader)
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
				QtGui.QMessageBox.critical(self, 'Error', 'Reader has a delay in [%s] items.' % (str(reader.delays()), ), QtGui.QMessageBox.Ok)
				flagStatus(self.check_delay, Constants.STATUS_WARNING)
				result = False
		flag(self.check_user, result)
		self.reader = result
		if result:
			self.label_field_userStatus.setText("Can Renew")
		self.showActionbutton(result)

	def checkItem(self, item):
		result = item
		self.label_field_itemStatus.setText("Can be renewed.")
		if item:
			if not item.loaned():
				QtGui.QMessageBox.critical(self, 'warning', 'Item is not loaned.', QtGui.QMessageBox.Ok)
				result = False
			if item.renewals() >= Constants.RENEWAL_LIMIT:
				QtGui.QMessageBox.critical(self, 'warning', 'Limit of Renewals reached.', QtGui.QMessageBox.Ok)
				result = False
			if self.loan.dueDate() > self.getDueDate():
				QtGui.QMessageBox.critical(self, 'warning', 'Renewal Date must be after than the actual due date. To modify the Date use Edit loan.', QtGui.QMessageBox.Ok)
				result = False
		if not result:
			self.label_field_itemStatus.setText("Can not be renewed.")
		flag(self.check_item, result)
		self.item = result
		self.showActionbutton(result)

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
				QtGui.QMessageBox.critical(self, 'Error', 'Error while Returned.', QtGui.QMessageBox.Ok)

	def retranslateUi2(self):
		self.groupCalendarLoanDate.setTitle(_translate("LoanReturn", "Today", None))
		self.buttonAction.setText(_translate("LoanReturn", "Renew", None))
		self.title.setText(_translate("LoanReturn", "Renew Item", None))


class EditLoan(LoanReturnMaster):
	def __init__(self, id_, parent=None):
		super(EditLoan, self).__init__()
		self.item0 = self.rader0 = False
		self.defaultItemsSearch = Constants.LOANED_ITEMS
		self.itemOpensLoan(True)
		self.hideReaderSearch()
		self.groupLoad.show()
		self.retranslateUi2()

		if id_:
			self.MasterIdLoad(id_)

	def MasterIdLoad_hook(self, loan):
		self.groupLoad.show()

	def checkReader(self, reader):
		same = False
		result = reader

		if self.reader0.ID() == reader.ID():
			same = True

		self.label_field_userStatus.setText("Can be a replacement.")
		flag(self.check_loans, True)
		flag(self.check_delay, True)

		if reader:
			if reader.status() == Constants.STATUS_INVALID:
				QtGui.QMessageBox.critical(self, 'Error', 'Reader status is Inactive.', QtGui.QMessageBox.Ok)
				if not same:
					result = False
			if reader.status() == Constants.BANED_USER:
				QtGui.QMessageBox.critical(self, 'Error', 'Reader status is Banned.', QtGui.QMessageBox.Ok)
				if not same:
					result = False

			if reader.loans() >= Constants.ST_MAX_LOANS:
				QtGui.QMessageBox.critical(self, 'Error', 'Reader can not loan more than [%s] items.' % (str(Constants.ST_MAX_LOANS), ), QtGui.QMessageBox.Ok)
				flagStatus(self.check_loans, Constants.STATUS_WARNING)
				if not same:
					result = False

			if reader.delays():
				QtGui.QMessageBox.critical(self, 'Error', 'Reader has a delay in [%s] items.' % (str(reader.delays()), ), QtGui.QMessageBox.Ok)
				flagStatus(self.check_delay, Constants.STATUS_WARNING)
				if not same:
					result = False

		flag(self.check_user, result)
		if not result:
			self.label_field_userStatus.setText("Can not Loan")
		self.reader = result
		self.showActionbutton(result)

	def checkItem(self, item):
		same = False
		result = item

		if not item:
			return

		if self.item0.ID() == item.ID():
			same = True

		self.label_field_itemStatus.setText("Can be a replacement.")
		if item:
			if item.loaned():
				if not same:
					QtGui.QMessageBox.critical(self, 'warning', 'Item is loaned.', QtGui.QMessageBox.Ok)
					result = False

		if not result:
			self.label_field_itemStatus.setText("Can not be a replacement.")
		self.item = result
		flag(self.check_item, result)
		self.showActionbutton(result)

	def handleButton(self):
		pass

	def retranslateUi2(self):
		self.groupCalendarLoanDate.setTitle(_translate("EditLoan", "Loan Date", None))
		self.buttonAction.setText(_translate("EditLoan", "Edit", None))
		self.title.setText(_translate("EditLoan", "Edit Loan", None))
