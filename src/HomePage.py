# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

from Gui.mMainPage import Ui_MainPage
from Tools.Database import DBManager as DataBase
from Tools.timeFunctions import todaysDate
from Tools.treeFunctions import TreeWiews
import config.GlobalConstants as Constants
from InfoWindows import LoanInfo
from Classes import Reader, Item, Loan


class Home(QtGui.QWidget, Ui_MainPage, TreeWiews):
	def __init__(self, parent=None):
		super(Home, self).__init__()
		self.setupUi(self)

		self.lastLoans = DataBase.lastNloans()
		self.dueToday = DataBase.duetoday(todaysDate())
		self.itemsInCats = DataBase.itemsInCategory()

		# defines the proxy
		self.proxyModelDue = QtGui.QSortFilterProxyModel(self)
		self.proxyModelLoans = QtGui.QSortFilterProxyModel(self)
		self.proxyModeCategories = QtGui.QSortFilterProxyModel(self)

		# Last Loans
		self.setTreeDecorations(self.tree_lastLoans, True)
		self.modelLastLoans = self.createElementModel(self.lastLoans, ['loanID', 'title', 'author'])
		self.setHeaders(self.modelLastLoans, ['ID', 'Title', 'Author'])
		self.proxyModelLoans.setSourceModel(self.modelLastLoans)
		self.tree_lastLoans.setModel(self.proxyModelLoans)
		self.setColumnWidth(self.tree_lastLoans, [100, 400, 400])

		# Due Today
		self.setTreeDecorations(self.tree_dueToday, True)
		self.modelDuetoday = self.createElementModel(self.dueToday, ['loanID', 'title', 'author'])
		self.setHeaders(self.modelDuetoday, ['ID', 'Title', 'Author'])
		self.proxyModelDue.setSourceModel(self.modelDuetoday)
		self.tree_dueToday.setModel(self.proxyModelDue)
		self.setColumnWidth(self.tree_dueToday, [100, 400, 400])

		# Tree categories
		self.setTreeDecorations(self.treeCategories, True)
		self.modelCats = self.createElementModel(self.itemsInCats, ['formatName', 'N'])
		self.setHeaders(self.modelCats, ['Category', 'Elements'])
		self.proxyModeCategories.setSourceModel(self.modelCats)
		self.treeCategories.setModel(self.proxyModeCategories)
		self.setColumnWidth(self.treeCategories, [100, 400, 400])

		# actions
		self.connect(self.tree_lastLoans, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.getLastLoansID)
		self.connect(self.tree_dueToday, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.getDueTodayID)
		self.fillStatistics()

	def getLastLoansID(self):
		loanID = str(self.tree_lastLoans.selectedIndexes()[0].data())
		self.showLoanInfo(loanID)

	def getDueTodayID(self):
		loanID = str(self.tree_dueToday.selectedIndexes()[0].data())
		self.showLoanInfo(loanID)

	def showLoanInfo(self, LoanID):
		loan = Loan(Constants.TYPE_LOAN, int(LoanID))
		reader = Reader(loan.userID())
		item = Item(loan.itemID())
		showinfo = LoanInfo(loan, reader, item, self)
		showinfo.exec_()

	def fillStatistics(self):
		self.value_itemsTotal.setText(str(DataBase.totalFromTable(Constants.TABLE_ITEMS)))
		self.value_readersTotal.setText(str(DataBase.totalFromTable(Constants.TABLE_USERS)))

		self.value_readersActive.setText(str(DataBase.countReaderByStatus(Constants.AVAILABLE_USERS)))
		self.value_readersInactive.setText(str(DataBase.countReaderByStatus(Constants.BLOCKED_USERS)))

		self.value_loansDone.setText(str(DataBase.totalFromTable(Constants.TABLE_HISTORY)))
		self.value_loansActive.setText(str(DataBase.totalFromTable(Constants.TABLE_LOANS)))
		delayed = DataBase.delayedbooks(todaysDate())

		if not delayed:
			delayed = 0

		self.valuel_loansDued.setText(str(delayed))

	def createElementModel(self, data, cols):
		model = QtGui.QStandardItemModel(0, len(cols), self)

		for i in range(0, len(data)):
			values = []
			element = data[i]
			for j in range(0, len(cols)):
				values.append(element[cols[j]])
			self.addElement(model, values)
		return model
