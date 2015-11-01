# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Gui.mNewReader import Ui_NewReader

from Tools import validations
from Tools.Database import DBManager as DataBase
from common import flag
import config.GlobalConstants as Constants

from Classes import Reader
import session.Session as Session

from Search import SearchUserWin


class NewReader(QtGui.QWidget, Ui_NewReader):
	def __init__(self, parent=None):
		super(NewReader, self).__init__()
		self.setupUi(self)
		self.frameEditReader.hide()
		# The idea is to validate the format of each field. Then, when a
		# field is modified it trigers the corresponding check of field
		self.connect(self.field_name, QtCore.SIGNAL("textChanged(QString)"), self.getName)
		self.connect(self.field_familyname, QtCore.SIGNAL("textChanged(QString)"), self.getFamilyName)
		self.connect(self.list_roles, QtCore.SIGNAL("currentIndexChanged(int)"), self.getRole)
		self.connect(self.list_grades, QtCore.SIGNAL("currentIndexChanged(int)"), self.getGrade)
		self.connect(self.field_IDN, QtCore.SIGNAL("textChanged(QString)"), self.getIDN)
		self.connect(self.field_email, QtCore.SIGNAL("textChanged(QString)"), self.getEmail)
		self.connect(self.field_address, QtCore.SIGNAL("textChanged(QString)"), self.getAddress)
		self.connect(self.field_telephone, QtCore.SIGNAL("textChanged(QString)"), self.getPhone)
		self.connect(self.field_cellphone, QtCore.SIGNAL("textChanged(QString)"), self.getCell)
		self.connect(self.field_comments, QtCore.SIGNAL("textChanged()"), self.checkComments)
		# Button action
		self.connect(self.button_add, QtCore.SIGNAL("clicked()"), self.handleButton)

		self.fillRoles()
		self.fillGrades()

		self.reset()
		self.cheackall()

	def fillGrades(self):
		if Session.GRADES_INFO:
			for i in range(0, len(Session.GRADES_INFO)):
				aux = Session.GRADES_INFO[i]
				self.list_grades.addItem(aux['gradeName'], aux['gradeID'])

	def fillRoles(self):
		if Session.ROLES_INFO:
			for i in range(0, len(Session.ROLES_INFO)):
				aux = Session.ROLES_INFO[i]
				self.list_roles.addItem(aux['roleName'], aux['roleID'])

	def handleButton(self):
		readerData = [
			self.getRole(),
			self.getName(),
			self.getFamilyName(),
			self.getIDN(),
			self.getEmail(),
			self.getAddress(),
			self.getPhone(),
			self.getCell(),
			self.getGrade(),
			self.checkComments()
		]
		if (False in readerData):
			QtGui.QMessageBox.critical(self, 'Error', 'There is information Missing or wrong.', QtGui.QMessageBox.No)
		else:
			saved = DataBase.save_new(Constants.TYPE_USER, readerData)
			if saved:
				QtGui.QMessageBox.information(self, 'Sucess', 'Reader Saved.', QtGui.QMessageBox.No)
				self.reset()
			else:
				QtGui.QMessageBox.critical(self, 'Error', 'Error while saving.', QtGui.QMessageBox.No)

	def cleanall(self):
		self.field_name.setText('')
		self.field_familyname.setText('')
		self.list_grades.setCurrentIndex(0)
		self.list_roles.setCurrentIndex(0)
		self.list_grades.setCurrentIndex(0)
		self.field_IDN.setText('')
		self.field_email.setText('')
		self.field_address.setText('')
		self.field_telephone.setText('')
		self.field_cellphone.setText('')
		self.field_comments.setPlainText('')

	def reset(self):
		pass

	def cheackall(self):
		self.getName()
		self.getFamilyName()
		self.getRole()
		self.getGrade()
		self.getIDN()
		self.getEmail()
		self.getAddress()
		self.getPhone()
		self.getCell()

	def getName(self):
		aux = unicode(self.field_name.text())
		Name = validations.validate(Constants.NAME, aux)
		flag(self.label_name_check, Name)
		return Name

	def getFamilyName(self):
		aux = unicode(self.field_familyname.text())
		FamilyName = validations.validate(Constants.NAME, aux)
		flag(self.label_familyName_check, FamilyName)
		return FamilyName

	def getRole(self):
		role_ = self.list_roles.itemData(self.list_roles.currentIndex())
		if role_:
			role_ = str(role_)
		flag(self.label_role_check, role_)
		self.showGradeField(role_)
		return role_

	def showGradeField(self, role_):
		if Session.roleNeedsGrade(role_):
			self.list_grades.show()
			self.label_grade.show()
			self.label_grade_check.show()
		else:
			self.list_grades.hide()
			self.label_grade.hide()
			self.label_grade_check.hide()

	def getGrade(self):
		if not Session.roleNeedsGrade(self.getRole()):
			return -1
		grade = self.list_grades.itemData(self.list_grades.currentIndex())
		flag(self.label_grade_check, self.list_grades.currentIndex())
		if grade == -1:
			return False
		return grade

	def getIDN(self):
		aux = str(self.field_IDN.text())
		IDN_ = validations.validate(Constants.IDN, aux)
		flag(self.check_idn, IDN_)
		return IDN_

	def getEmail(self):
		aux = str(self.field_email.text())
		email = validations.validate(Constants.EMAIL, aux)
		flag(self.check_email, email)
		return email

	def getAddress(self):
		address = str(self.field_address.text()).strip()
		flag(self.check_address, address)
		return address

	def getPhone(self):
		aux = str(self.field_telephone.text()).strip()
		phone = validations.validate(Constants.PHONE, aux)
		flag(self.check_telephone, phone)
		return phone

	def getCell(self):
		aux = str(self.field_cellphone.text()).strip()
		cellphone = validations.validate(Constants.CELPHONE, aux)
		flag(self.check_cellphone, cellphone)
		return cellphone

	def checkComments(self):
		comments = str(self.field_comments.toPlainText()).strip()
		return comments

	def listIndex(self, Cbox, value):
		index = Cbox.findData(value)
		if index < 0:
			index = 0
		return index


class EditReader(NewReader, QtGui.QDialog):
	def __init__(self, id_, parent=None):
		super(EditReader, self).__init__()

		if not id_:
			self.frameEditReader.show()
		else:
			ID, ident = validations.validate(Constants.IDS, id_, Session.FORMAT_TYPE_INFO)

		self.connect(self.buttonLoadID, QtCore.SIGNAL("clicked()"), self.loadElement)
		self.connect(self.buttonSearch, QtCore.SIGNAL("clicked()"), self.searchReader)
		self.connect(self.field_readerID, QtCore.SIGNAL("textChanged(QString)"), self.changeID)

	def changeID(self):
		self.cleanall()

	def searchReader(self):
		self.searchElement(Constants.TYPE_USER, Constants.ALL_USERS)

	def searchElement(self, type_, status):
		# Select the type of search window
		if type_ == Constants.TYPE_USER:
			Searcher = SearchUserWin(True, status, self)
		else:
			return
		Searcher.exec_()
		# After closing the dialog search for the Id of the object to be shown
		ID = Searcher.ID
		if type_ == Constants.TYPE_USER:
			if ID:
				self.field_readerID.setText(ID)
				self.loadElement(Constants.TYPE_USER)
			else:
				self.cleanall()
		elif type_ == Constants.TYPE_ITEM:
			if ID:
				self.field_itemID.setText(ID)
				self.loadElement(Constants.TYPE_ITEM)
			else:
				self.cleanItem()

	def checkID(self):
		aux = unicode(self.field_readerID.text()).strip()
		id_, ident = validations.validate(Constants.IDS, aux, Session.ROLES_INFO)
		flag(self.check_readerID, id_)
		return id_, ident

	def loadElement(self, dummy=False):
		id_, ident = self.checkID()
		if not id_:
			return False
		reader = Reader(id_)
		if reader:
			if not reader.role() == ident:
				return False
			self.showReaderData(reader)
		return id_, ident

	def showReaderData(self, reader):
		self.field_name.setText(reader.name())
		self.field_familyname.setText(reader.familyname())
		self.list_roles.setCurrentIndex(self.listIndex(self.list_roles, reader.role()))
		self.list_grades.setCurrentIndex(self.listIndex(self.list_grades, reader.grade()))
		self.field_IDN.setText(reader.IDN())
		self.field_email.setText(reader.email())
		self.field_address.setText(reader.address())
		self.field_telephone.setText(reader.phone())
		self.field_cellphone.setText(reader.cellphone())
		self.field_comments.setPlainText(reader.comments())

	def handleButton(self):
		readerData = [
			self.getRole(),
			self.getName(),
			self.getFamilyName(),
			self.getIDN(),
			self.getEmail(),
			self.getAddress(),
			self.getPhone(),
			self.getCell(),
			self.getGrade(),
			self.checkComments(),
			self.checkID()[0]  # gets the ID, but not the aux variable used to test the type of user
		]
		if (False in readerData):
			QtGui.QMessageBox.critical(self, 'Error', 'There is information Missing or wrong.', QtGui.QMessageBox.No)
		else:
			edited = DataBase.edit_itemUser(Constants.TYPE_USER, readerData)
			if edited:
				QtGui.QMessageBox.information(self, 'Sucess', 'Reader Modified.', QtGui.QMessageBox.No)
				self.reset()
				self.cleanall()
			else:
				QtGui.QMessageBox.critical(self, 'Error', 'Error while saving.', QtGui.QMessageBox.No)
