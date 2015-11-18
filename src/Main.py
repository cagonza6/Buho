# -*- coding: utf-8 -*-
import sip

import config.GlobalConstants as GlobalConstants
import session.Session as Session

sip.setapi('QVariant', 2)

from PyQt4 import QtGui
from Gui.Main_window import Ui_MainWindow
from Dialogs import AboutApplication
from Items import NewItem, EditItem
from HomePage import Home
from Readers import NewReader, EditReader
from LoanReturn import ReturnItem, LoanItem, RenewItem
from Search import SearchItemWin, SearchUserWin, DuedItemWin
from Tools.Database import DBManager as DataBase


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.showMaximized()

		self.NeedsAccept = False
		#
		# General Actions
		#
		self.actionHome.triggered.connect(self.MainPage)

		#
		# About Actions
		#
		self.actionAbout_Qt.triggered.connect(self.aboutQt)
		self.actionAbout_Buho.triggered.connect(self.aboutApp)

		#
		# Users Actions
		#
		self.actionNewReader.triggered.connect(self.addNewReader)
		self.actionSearchReader.triggered.connect(self.SearchReaders)
		self.actionEditReader.triggered.connect(self.editReader)

		#
		# Item Actions
		#
		self.actionNewItem.triggered.connect(self.addNewItem)
		self.actionEditItem.triggered.connect(self.editItem)
		self.actionSearchItems.triggered.connect(self.SearchItems)
		self.actionRenew_Loan.triggered.connect(self.RenewItem)
		self.actionEditItem.triggered.connect(self.editItem)

		#
		# Item Trafic
		#
		self.actionLoan_Item.triggered.connect(self.LoanItem)
		self.actionReturn_Item.triggered.connect(self.ReturnItem)
		self.actionLoanedItems.triggered.connect(self.LoanedItems)
		# self.actionEdit_Loan.triggered.connect(self.editLoan)

		#
		# Reports
		#
		self.actionDuedItems.triggered.connect(self.DuedItems)

		#
		# contructor requirements
		#
		self.loadSessionInfo()
		self.MainPage()

	def changePanel(self, Newpanel):
		self.setCentralWidget(Newpanel)

	#
	# Calls to different methods to manage items and users
	#

	def MainPage(self):
		self.changePanel(Home(self))

	def addNewItem(self):
		self.changePanel(NewItem(self))

	def editItem(self):
		self.changePanel(EditItem(False, self))

	def addNewReader(self):
		self.changePanel(NewReader(self))

	def editReader(self):
		self.changePanel(EditReader(False, self))

	def LoanItem(self):
		self.changePanel(LoanItem(self))

	def ReturnItem(self, id_=False):
		self.changePanel(ReturnItem(id_, self))

	def RenewItem(self):
		self.changePanel(RenewItem(self))

	def LoanedItems(self):
		self.changePanel(SearchItemWin(False, GlobalConstants.LOANED_ITEMS, self))

	def SearchReaders(self):
		self.changePanel(SearchUserWin(False, GlobalConstants.ALL_USERS, self))

	def SearchItems(self):
		self.changePanel(SearchItemWin(False, GlobalConstants.ALL_ITEMS, self))

	def DuedItems(self):
		self.changePanel(DuedItemWin(False, GlobalConstants.ALL_ITEMS, self))

	def aboutQt(self):
		QtGui.QMessageBox.aboutQt(self, 'About Qt')

	def aboutApp(self):
		ab = AboutApplication(self)
		ab.exec_()
	'''
	def closeEvent(self, event):
		result = QtGui.QMessageBox.question(self,
					"Confirm Exit...",
					"Are you sure you want to exit ?",
					QtGui.QMessageBox.Yes| QtGui.QMessageBox.Ok)
		event.ignore()
		self.MainPage()
		event.accept()
	'''

	def closeEvent(self, event):
		self.MainPage()
		event.accept()

	def loadSessionInfo(self):
		rolesIDs = DataBase.load_roles()

		if rolesIDs:
			Session.ROLES_INFO = rolesIDs
		formats = DataBase.load_categories()
		if formats:
			Session.FORMAT_TYPE_INFO = formats
		languages = DataBase.load_languages()
		if languages:
			Session.LANGUAGES_INFO = languages
		grades = DataBase.load_grades()
		if grades:
			Session.GRADES_INFO = grades


if __name__ == '__main__':
	import sys

	app = QtGui.QApplication(sys.argv)
	app.setApplicationName('Buho')
	app.setApplicationVersion('Alpha - 0.1')
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
