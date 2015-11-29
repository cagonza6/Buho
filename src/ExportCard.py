# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from Tools import validations
from Tools.Database import DBManager as DataBase
from Tools.pdf import CreateIDCard
from Classes import Reader
from common import flagStatus, flag
from Search import SearchUserWin
from Dialogs import PathMethods
from Gui.dialogs.mPrintCards import Ui_SaveCards
import session.Session as Session
import config.GlobalConstants as Constants


class ExportCards(Ui_SaveCards, PathMethods):
	def __init__(self, parent=None):
		super(ExportCards, self).__init__()
		self.baseName = 'IDCards'
		self.pathToFile = ''
		self.connect(self.buttonSearchReader, QtCore.SIGNAL("clicked()"), self.searchReader_)
		self.connect(self.field_readerID, QtCore.SIGNAL("textChanged(QString)"), self.OnChangeReaderID)
		self.connect(self.radio_reader, QtCore.SIGNAL("clicked()"), self.OnChangeReaderID)
		self.connect(self.combo_grades, QtCore.SIGNAL("currentIndexChanged(int)"), self.OnGradeChanged)
		self.connect(self.radio_grade, QtCore.SIGNAL("clicked()"), self.OnGradeChanged)

		self.combo_grades.addItem('Select', False)
		for grade in Session.GRADES_INFO:
			self.combo_grades.addItem(grade['gradeName'], grade['gradeID'])

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

	def searchReader_(self):
		Searcher = SearchUserWin(True, Constants.AVAILABLE_USERS, self)
		Searcher.exec_()
		Id_ = Searcher.ID
		if Id_:
			self.field_readerID.setText(Id_)

	def OnChangeReaderID(self):
		flagStatus(self.checkGrade, Constants.BLOCKED_USERS)
		self.checkID(Constants.TYPE_USER)

	def OnGradeChanged(self):
		self.combo_grades.itemData(self.combo_grades.currentIndex())
		flagStatus(self.check_userID, Constants.BLOCKED_USERS)
		self.checkGrade_()

	def checkGrade_(self):
		grade = self.combo_grades.itemData(self.combo_grades.currentIndex())
		flag(self.checkGrade, grade)
		return int(grade)

	def getExportInfo(self):
		# first check if the radio buton is toggled
		readersCards = []
		if not self.checkPath():
			QtGui.QMessageBox.critical(self, 'Error', 'Invalid path to file.', QtGui.QMessageBox.Ok)
			return
		if self.radio_grade.isChecked():
			# then, check if a grade is checked
			grade = self.checkGrade_()
			if not grade:
				QtGui.QMessageBox.critical(self, 'Error', 'Invalid grade.', QtGui.QMessageBox.Ok)
				return
			# Get all users from that grade that are not banned.
			# i.e. that can loan books
			readers = DataBase.search_users(Constants.AVAILABLE_USERS, False, False, False, grade)
			for reader in readers:
				if reader:
					readersCards.append(Reader(reader['userID']))

		elif self.radio_reader.isChecked():
			id_, aux = self.checkID(Constants.TYPE_USER)
			if not id_:
				return
			readersCards.append(Reader(id_))

		if readersCards:
			self.generateCard(readersCards)


	def generateCard(self, readers):
		pathToFile = str(self.field_path.text()).strip()
		pathToCard = self.checkPath()
		if not pathToCard:
			return

		CreateIDCard(pathToFile, readers)
		QtGui.QMessageBox.information (self, 'PDF', 'File created.', QtGui.QMessageBox.Ok)
		self.cleanall()

	def cleanall(self):
		self.field_path.setText(Constants.EMPTY)
		self.field_readerID.setText(Constants.EMPTY)
		self.combo_grades.setCurrentIndex(0)
