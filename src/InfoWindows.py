# -*- coding: utf-8 -*-
import textwrap

from PyQt4 import QtGui

from Gui.mReaderInfo import Ui_ReaderInfo
from Gui.mItemInfo import Ui_ItemInfo
from Gui.mLoanInfo import Ui_LoanInfo
from Classes import Reader, Item
from Tools import validations
import config.GlobalConstants as Constants
import session.Session as Session
from Tools.ItemTools import formatID
from Tools.treeFunctions import TreeWiews
from common import flagStatus, flag, userStatusIcon
from Tools.timeFunctions import int2date, todaysDate


class ShowInfo():
	def __init__(self):
		pass

	def showReaderInfo(self, reader):
		if not reader:
			return
		self.label_field_name.setText(textwrap.fill(reader.name(), width=36))
		self.label_reader_role.setText(reader.roleName())
		self.label_field_rederloans.setText('%s/%s' % (str(reader.loans()), str(Constants.ST_MAX_LOANS)))
		self.label_field_delays.setText(str(reader.delays()))

	def showItemInfo(self, item):
		if not item:
			return
		self.label_field_isbn.setText(item.ISBN())
		self.label_field_title.setText(textwrap.fill(item.title(), width=36))
		self.label_field_author.setText(textwrap.fill(item.author(), width=36))
		self.label_field_lang.setText(item.language())


class ReaderInfo(Ui_ReaderInfo, QtGui.QDialog, TreeWiews):
	def __init__(self, id_, parent=None):
		super(ReaderInfo, self).__init__()
		self.setupUi(self)
		id_, aux = validations.validate(Constants.IDS, id_, Session.ROLES_INFO)

		if id_:
			reader = Reader(id_)
			self.field_ID.setText(reader.id2str())
			self.field_name.setText(textwrap.fill(reader.fullName(), width=36))
			self.field_role.setText(reader.roleName())
			self.field_email.setText(reader.email())
			self.field_address.setText(reader.address())
			self.field_cellphone.setText(reader.cellphone())
			self.field_IDN.setText(reader.IDN())
			self.field_grade.setText(reader.gradeName())
			self.field_phone.setText(reader.phone())
			self.field_comments.setText(textwrap.fill(reader.comments(), width=36))

			userStatusIcon(self.check_status, reader.status())

			# Data tables
			# TODO
			self.proxyLoans = QtGui.QSortFilterProxyModel(self)
			self.proxyDueItems = QtGui.QSortFilterProxyModel(self)
			self.proxyHistory = QtGui.QSortFilterProxyModel(self)

			self.modelActiveloans = self.createElementModel(reader.activeLoans, ['itemIdStr', 'title', 'author', 'publisher', 'year'])
			self.setHeaders(self.modelActiveloans, ['ID', 'Title', 'Author', 'Publisher', 'year'])
			self.proxyLoans.setSourceModel(self.modelActiveloans)
			self.treeLoans.setModel(self.proxyLoans)
			self.setColumnWidth(self.treeLoans, [90, 150, 150, 150, 50])

			self.modelActiveloans = self.createElementModel(reader.duedItems, ['itemIdStr', 'title', 'author', 'publisher', 'year'])
			self.setHeaders(self.modelActiveloans, ['ID', 'Title', 'Author', 'Publisher', 'year'])
			self.proxyDueItems.setSourceModel(self.modelActiveloans)
			self.treeDued.setModel(self.proxyDueItems)
			self.setColumnWidth(self.treeDued, [90, 150, 150, 150, 50])

			self.headersH = ['ID', 'Title', 'Author', 'Publisher', 'year', 'Due Date', 'Returned', 'Renewed']
			self.modelHistory = self.createElementModelH(reader.history)
			self.setHeaders(self.modelHistory, self.headersH)
			self.proxyHistory.setSourceModel(self.modelHistory)
			self.treeHistory.setModel(self.proxyHistory)
			self.setColumnWidth(self.treeHistory, [90, 220, 220, 180, 50, 120, 120, 50])

	def createElementModelH(self, elements):
		model = QtGui.QStandardItemModel(0, len(self.headersH), self)
		self.setHeaders(model, self.headersH)
		if not elements:
			return model

		for i in range(0, len(elements)):
			element = elements[i]

			cols = [
				element['itemIdStr'],
				element['title'],
				element['author'],
				element['publisher'],
				str(element['year']),
				str(int2date(element['dueDate'])),
				str(int2date(element['returnDate'])),
				element['renewals']
			]

			self.addElement(model, cols)
		return model


class ItemInfo(Ui_ItemInfo, QtGui.QDialog, TreeWiews):
	def __init__(self, id_, parent=None):
		super(ItemInfo, self).__init__()
		self.setupUi(self)
		id_, aux = validations.validate(Constants.IDS, id_, Session.FORMAT_TYPE_INFO)

		if not id_:
			self.close()

		item = Item(id_)

		self.field_ID.setText(item.id2str())
		self.field_format.setText(item.formatName())
		self.field_title.setText(textwrap.fill(item.title(), width=36))
		self.field_publisher.setText(item.publisher())
		self.field_location.setText(item.location())
		self.field_comments.setText(item.comments())

		self.field_ISBN.setText(item.ISBN())
		self.field_author.setText(textwrap.fill(item.author(), width=36))
		self.field_language.setText(item.language())
		self.field_status.setText('')
		self.field_year.setText(str(item.year()))
		flagStatus(self.check_status, item.status())

		# treeHistory
		self.headers = ['ID', 'Reader', 'Grade', 'Loan Date', 'Due Date', 'Returned', 'Renewals']
		self.proxyHistory = QtGui.QSortFilterProxyModel(self)
		self.modelHistory = self.createElementModel(item.getHistory())
		self.setHeaders(self.modelHistory, self.headers)
		self.proxyHistory.setSourceModel(self.modelHistory)
		self.treeHistory.setModel(self.proxyHistory)
		self.setColumnWidth(self.treeHistory, [90, 300, 50, 100, 100, 100, 100])

	def createElementModel(self, elements):
		model = QtGui.QStandardItemModel(0, len(self.headers), self)
		self.setHeaders(model, self.headers)
		if not elements:
			return model

		for i in range(0, len(elements)):
			element = elements[i]

			cols = [
				# element['dueDate'] < element['returnDate'] # Here should be a identifier for the indication of a delay in the return
				formatID(element['role'], element['userID']),
				element['name'] + ' ' + element['familyname'],
				element['gradeName'],
				str(int2date(element['loanDate'])),
				str(int2date(element['dueDate'])),
				str(int2date(element['returnDate'])),
				str(element['renewals'])
			]
			self.addElement(model, cols)
		return model


class LoanInfo(QtGui.QDialog, Ui_LoanInfo, ShowInfo):
	def __init__(self, loan, reader, item, parent=None):
		super(LoanInfo, self).__init__()
		self.setupUi(self)

		self.showReaderInfo(reader)

		flag(self.check_delay, not reader.delays())
		flag(self.check_dued, loan.dueDate() >= todaysDate())

		self.label_loanDate.setText(str(int2date(loan.loanDate())))
		self.label_dueDate.setText(str(int2date(loan.dueDate())))

		self.showItemInfo(item)
