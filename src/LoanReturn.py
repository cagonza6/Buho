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
from IdMaster import IdMaster


class LoanReturnMaster(QtGui.QWidget, Ui_LoanReturn, ShowInfo):
	def __init__(self, parent=None):
		super(LoanReturnMaster, self).__init__()

		self.defaultItemsSearch = Constants.LOANED_ITEMS
		self.defaultReaderSearch = Constants.AVAILABLE_USERS
		self.setupUi(self)
		self.frameMasterID.hide()
		self.btn_delete.hide()
		# Actions
		self.connect(self.field_itemID, QtCore.SIGNAL("textChanged(QString)"), self.OnChangeItemID)
		self.connect(self.field_readerID, QtCore.SIGNAL("textChanged(QString)"), self.OnChangeReaderID)
		self.connect(self.calendarDueDay, QtCore.SIGNAL("clicked(QDate)"), self.getDueDate)

		# Buttons
		self.connect(self.buttonSearchBook, QtCore.SIGNAL("clicked()"), self.searchItem_)
		self.connect(self.buttonSearchReader, QtCore.SIGNAL("clicked()"), self.searchReader_)
		self.connect(self.button_loadItem, QtCore.SIGNAL("clicked()"), self.loadItem)
		self.connect(self.button_loadReader, QtCore.SIGNAL("clicked()"), self.loadReaderSearch)
		self.connect(self.buttonAction, QtCore.SIGNAL("clicked()"), self.handleButton)

		# Proper dates for the calendars
		self.setCalendarToday()
		self.setCalendarDueDate()

		self.resetall()
		self.cheackall()

	def searchItem_(self):
		'''
		Used to call the dafault time of item in each window
		that varies from window to window
		'''
		self.searchElement(Constants.TYPE_ITEM, self.defaultItemsSearch)

	def searchReader_(self):
		'''
		Used to call the dafault time of user in each window
		that varies from window to window
		'''
		self.searchElement(Constants.TYPE_USER, self.defaultReaderSearch)

	def hideElements(self):
		self.groupLoad.hide()

	def hideReaderSearch(self):
		self.button_loadReader.hide()
		self.buttonSearchReader.hide()
		self.check_userID.hide()
		self.field_readerID.hide()
		self.label_readerID.hide()

	def showReaderSearch(self):
		self.button_loadReader.show()
		self.buttonSearchReader.show()
		self.check_userID.show()
		self.field_readerID.show()
		self.label_readerID.show()

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
		self.loadElement(Constants.TYPE_ITEM)
		self.loadItem_hook(False)

		'''
		The idea of the hook methods is to call them after the original
		method in order perform further processes o calls to other methods
		I guess it is cool and I got it from Drupal, I have no idea how
		it would be programed by a real programer
		'''
	def loadItem_hook(self, item):
		pass

	def loadReaderID(self, id_):
		if not id_:
			return
		reader = Reader(id_)
		self.loadReader_hook(reader)

	def loadReaderSearch(self):
		self.loadElement(Constants.TYPE_USER)
		self.loadReader_hook(False)

	def loadReader_hook(self, reader):
		pass

	def loadLoan(self, type_, id_):
		if not id_ or not type_:
			return False
		self.loan = Loan(Constants.TYPE_ITEM, id_)
		self.loadLoan_hook(self.loan)
		return self.loan

	def loadLoan_hook(self, loan):
		pass

	def loadElement(self, type_):
		if not type_:
			return
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

	# ID related methods
	def OnChangeReaderID(self):
		self.resetReader()
		self.checkID(Constants.TYPE_USER)
		self.OnChangeReaderID_hook(False)

	def OnChangeReaderID_hook(self, reader):
		pass

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

		self.loadElement(type_)


class LoanItem(LoanReturnMaster):
	def __init__(self, parent=None):
		super(LoanItem, self).__init__()

		self.defaultItemsSearch = Constants.AVAILABLE_ITEMS
		self.defaultReaderSearch = Constants.AVAILABLE_USERS

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

		# Proper dates for the calendars
		self.setCalendarToday()

		# hide non required elements from the Window
		self.hideReaderSearch()
		self.retranslateUi2()

		if id_:
			# id comes with the format as in the barcode of the book,
			# like would be written by the user
			self.field_itemID.setText(id_)
			self.loadItem()
			self.groupLoad.hide()

	# ID related methods
	def OnChangeItemID_hook(self):
		self.resetReader()
		self.checkID(Constants.TYPE_USER)

	def searchReader_(self):
		pass

	def OnChangeReaderID(self):
		pass

	def loadReader_hook(self, reader):
		self.showReaderInfo(reader)
		self.checkReader(reader)

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
				QtGui.QMessageBox.warning(self, 'Error', 'Reader has a delay in [%s] items.' % (str(reader.delays()), ), QtGui.QMessageBox.Ok)
				flagStatus(self.check_delay, Constants.STATUS_WARNING)
				result = False

		if not result:
			self.label_field_userStatus.setText("Can not Loan")

		flag(self.check_user, result)
		self.reader = result
		self.showReaderInfo(result)
		self.showActionbutton(result)

	def checkItem(self, item):
		result = item
		self.label_field_itemStatus.setText("Not Loaned")
		if item:
			if not item.loaned():
				QtGui.QMessageBox.critical(self, 'warning', 'Item is not loaned.', QtGui.QMessageBox.Ok)
				self.label_field_itemStatus.setText("Can not be Returned")
				result = False
			else:
				self.label_field_itemStatus.setText("Can be Returned")
		flag(self.check_item, result)

		self.item = result
		if result:
			self.loadLoan(Constants.TYPE_ITEM, item.ID())
			self.setCalendarDueDate(self.loan.dueDate())
			self.loadReaderID(self.loan.userID())
		# the call to load user is done from loadLoan
		self.showActionbutton(result)

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
				result = False
				flagStatus(self.check_delay, Constants.STATUS_WARNING)
		flag(self.check_user, result)
		self.reader = result
		if result:
			self.label_field_userStatus.setText("Can Renew")
		self.showActionbutton(result)

	def loadReader_hook(self, reader):
		self.showReaderInfo(reader)
		self.checkReader(reader)

	def checkItem(self, item):
		result = item
		self.label_field_itemStatus.setText("Can be renewed.")
		if item:
			if not item.loaned():
				QtGui.QMessageBox.critical(self, 'warning', 'Item is not loaned.', QtGui.QMessageBox.Ok)
				result = False
			else:
				self.label_field_itemStatus.setText("Can be Returned")
			if item.renewals() >= Constants.RENEWAL_LIMIT:
				QtGui.QMessageBox.critical(self, 'warning', 'Limit of Renewals reached.', QtGui.QMessageBox.Ok)
				result = False

			self.loadLoan(Constants.TYPE_ITEM, item.ID())
			self.loadReaderID(self.loan.userID())

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


class EditLoan(LoanReturnMaster, IdMaster):
	def __init__(self, id_, parent=None):
		super(EditLoan, self).__init__()

		self.defaultItemsSearch = Constants.LOANED_ITEMS
		self.retranslateUi2()
		self.connections()
		if id_:
			self.connections()
			self.fieldMasterId.setText(id_)
			self.loadMasterID()
		else:
			self.frameMasterID.show()
			self.btn_delete.show()

		self.hideElements()
		self.item = self.rader = False

	def MasterIdChanged(self):
		self.resetall()

	def MasterIdLoad(self):
		self.frameMasterID.hide()

	def SearchMasterId(self):
		# Select the type of search window
		Searcher = SearchItemWin(True, self.defaultItemsSearch, self)
		Searcher.exec_()
		# After closing the dialog search for the Id of the object to be shown
		id_ = Searcher.ID
		id_, ident = validations.validate(Constants.IDS, id_, Session.FORMAT_TYPE_INFO)
		if not id_:
			return
		loan = Loan(Constants.TYPE_ITEM, id_)
		if not loan.Data:
			QtGui.QMessageBox.critical(self, 'warning', 'Loan information not found. \n Make sure you selected a loaned item.', QtGui.QMessageBox.Ok)
			return
		# this part must be on another side... I guess
		# shows sesarch parameters for reader and item
		self.fieldMasterId.setText(loan.id2str())
		self.groupLoad.show()

		# opens the related item
		item = Item(loan.itemID())
		self.item0 = item
		self.field_itemID.setText(item.id2str())
		self.showItemInfo(item)
		self.checkItem(item)

		# opens the related reader
		reader = Reader(loan.userID())
		self.reader0 = reader
		self.field_readerID.setText(reader.id2str())
		self.showReaderInfo(reader)
		self.checkReader(reader)

		self.MasterIdLoad()

	def loadReader_hook(self, reader):
		if not reader:
			return
		self.field_readerID.setText(reader.id2str())
		self.showReaderInfo(reader)
		self.checkReader(reader)

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
				QtGui.QMessageBox.critical(self, 'Error', 'Reader status is Blocked.', QtGui.QMessageBox.Ok)
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
				if not same:
					result = False
					flagStatus(self.check_delay, Constants.STATUS_WARNING)

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
