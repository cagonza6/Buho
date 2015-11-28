# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from isbnlib import meta as isbnmetadata

from Gui.mNewItem import Ui_NewItem
from Tools import validations
from Tools import ISBN
from Tools.Database import DBManager as DataBase
from Search import SearchItemWin
import config.GlobalConstants as Constants
from common import flag, _translate
from Classes import Item
import session.Session as Session


class ItemMaster(QtGui.QWidget, Ui_NewItem):
	def __init__(self, parent=None):
		super(ItemMaster, self).__init__()
		self.setupUi(self)
		self.needsISBN = False
		self.frameEditItem.hide()
		self.newItem = True  # to identify the module
		# The idea is to validate the format of each field. Then, when a
		# field is modified it trigers the corresponding check of field
		self.connect(self.field_format, QtCore.SIGNAL("currentIndexChanged(int)"), self.getFormat)
		self.connect(self.field_title, QtCore.SIGNAL("textChanged(QString)"), self.getTitile)
		self.connect(self.field_ISBN, QtCore.SIGNAL("textChanged(QString)"), self.isbnChanged)
		self.connect(self.field_author, QtCore.SIGNAL("textChanged(QString)"), self.getAuthor)
		self.connect(self.field_publisher, QtCore.SIGNAL("textChanged(QString)"), self.getPublisher)
		self.connect(self.field_year, QtCore.SIGNAL("valueChanged(int)"), self.getYear)
		self.connect(self.field_language, QtCore.SIGNAL("currentIndexChanged(int)"), self.getLanguage)
		self.connect(self.field_location, QtCore.SIGNAL("textChanged(QString)"), self.getLocation)
		self.connect(self.field_comments, QtCore.SIGNAL("textChanged()"), self.getComments)

		# initial values for the form: if any of these are false, it will not possible to save anything
		self.reset()
		# Button action
		self.connect(self.button_add, QtCore.SIGNAL("clicked()"), self.handleButton)
		self.connect(self.buttonIsbnSearch, QtCore.SIGNAL("clicked()"), self.searchISBN)
		# ISBN check, some book could not have one
		self.check_needIsbn.toggled.connect(self.getFormat)

		# Fill parameters for formats and language
		self.fillFormats()
		self.fillLanguages()
		self.cheackall()
		self.defaults()

	def showISBNfield(self, show):
		if self.check_needIsbn.isChecked():
			show = False
		if show:
			self.field_ISBN.show()
			self.buttonIsbnSearch.show()
			self.label_ISBN_check.show()
		else:
			self.field_ISBN.hide()
			self.buttonIsbnSearch.hide()
			self.label_ISBN_check.hide()

	def fillFormats(self):
		if Session.FORMAT_TYPE_INFO:
			for i in range(0, len(Session.FORMAT_TYPE_INFO)):
				format_ = Session.FORMAT_TYPE_INFO[i]
				self.field_format.addItem(format_['formatName'], format_['formatID'])

	def fillLanguages(self):
		if Session.LANGUAGES_INFO:
			for i in range(0, len(Session.LANGUAGES_INFO)):
				lang = Session.LANGUAGES_INFO[i]
				self.field_language.addItem(lang['Ref_Name'], lang['langIsoID'])  # text to show in the combobox

	def isbnChanged(self):
		self.getISBN()

	def getlangtype(self, langIso):
		language = False
		for i in range(0, len(Session.LANGUAGES_INFO)):
			lang = Session.LANGUAGES_INFO[i]
			if langIso not in lang.values():
				continue
			if langIso in lang.values():
				language = lang['langIsoID']
		return language

	def setlang(self, langIso):
		langIso = self.getlangtype(langIso)
		self.field_language.setCurrentIndex(self.listIndex(self.field_language, langIso))

	def searchISBN(self):
		fromDb = metaData = False
		itemFromDb = item = False
		copies = 0
		cleanISBN = ISBN.clean(self.getISBN())
		if self.getISBN():
			itemFromDb = DataBase.searchByCodeBar(cleanISBN)
			self.field_ISBN.setText(ISBN.formated(cleanISBN))
		if itemFromDb:
			item = Item(itemFromDb['itemID'])
			copies = int(itemFromDb['copies'])
			reply = QtGui.QMessageBox.question(self, 'Question', 'There are [%s] copies of this item in the actual Datadase. Do you want to use the data of them?' % copies, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.No:
				itemFromDb = False

		if itemFromDb:
			self.fillItemFields(item)
			fromDb = True
		elif ISBN.isISBN(cleanISBN):
			metaData = self.searchBookInet(cleanISBN)

		if self.newItem:
			self.field_copy.setValue(copies + 1)

		if fromDb or metaData:
			QtGui.QMessageBox.information(self, 'Search', 'Book Found.', QtGui.QMessageBox.Ok)
		else:
			QtGui.QMessageBox.information(self, 'Search', 'Book not Found.', QtGui.QMessageBox.Ok)

	def searchBookInet(self, bookIsbn):
		metaData = isbnmetadata(bookIsbn, service='default', cache='default')
		if metaData:
			if 'Publisher' in metaData.keys():
				self.field_publisher.setText(metaData['Publisher'])
			if 'Title' in metaData.keys():
				self.field_title.setText(metaData['Title'])
			if 'Authors' in metaData.keys():
				aux = ', '.join(metaData['Authors'])
				self.field_author.setText(aux)
			if 'Year' in metaData.keys():
				self.field_year.setValue(int(metaData['Year']))
			if 'Language' in metaData.keys():
				langIso = unicode(metaData['Language'])
				self.setlang(langIso)
		return metaData
	'''
	Methods to clean data
	'''

	def reset(self):
		self.field_ISBN.setText(Constants.EMPTY)
		self.needsISBN = False
		self.cleanall()
		# self.field_format.setCurrentIndex(0)
		self.field_year.setValue(1400)
		self.field_copy.setValue(1)

	def cleanall(self):
		self.field_title.setText(' ')
		self.field_ISBN.setText(' ')
		self.field_author.setText(' ')
		self.field_publisher.setText(' ')
		self.field_location.setText(' ')
		self.field_comments.setPlainText(' ')

	def defaults(self):
		self.field_title.setText('untitled')
		self.field_ISBN.setText(Constants.EMPTY)
		self.field_author.setText('unknown')
		self.field_publisher.setText('unknown')
		self.field_location.setText(Constants.EMPTY)
		self.field_comments.setPlainText(Constants.EMPTY)

	'''
	Methods to check and valid data
	'''

	def cheackall(self):
		self.getTitile()
		self.getISBN()
		self.showISBNfield(self.getFormat())
		self.getAuthor()
		self.getPublisher()
		self.getYear()
		self.getLocation()
		self.getComments()

	def fillItemFields(self, item):
		self.field_format.setCurrentIndex(self.listIndex(self.field_format, item.formatID()))
		self.field_language.setCurrentIndex(self.listIndex(self.field_language, item.langIsoID()))
		self.field_ISBN.setText(ISBN.formated(item.ISBN()))
		self.field_title.setText(item.title())
		self.field_author.setText(item.author())
		self.field_publisher.setText(item.publisher())
		self.field_year.setValue(int(item.year()))
		self.field_location.setText(item.location())
		self.field_comments.setPlainText(item.comments())
		self.field_copy.setValue(int(item.copy()))

	def getData2sql(self):
		itemData = [
			self.getFormat(),
			ISBN.clean(self.getISBN()),
			ISBN.isbn10(self.getISBN()),
			ISBN.isbn13(self.getISBN()),
			self.getTitile(),
			self.getAuthor(),
			self.getPublisher(),
			self.getYear(),
			self.getLanguage(),
			self.getLocation(),
			self.getComments(),
			self.getCopy()
		]
		return itemData

	def handleButton(self):
		pass

	'''
	check/get the data from the different fields
	'''

	def getFormat(self):
		format_ = self.field_format.itemData(self.field_format.currentIndex())
		flag(self.label_category_check, self.field_format.currentIndex())
		self.needsISBN = False
		if self.field_format.currentIndex():
			if format_ == Constants.ITEM_BOOK:
				self.needsISBN = True
			self.showISBNfield(self.needsISBN)
			return str(format_)
		self.showISBNfield(self.needsISBN)
		return False

	def getISBN(self):
		if not self.needsISBN:
			return None
		text = str(self.field_ISBN.text())
		bookIsbn = validations.validate(Constants.ISBN, text)
		flag(self.label_ISBN_check, bookIsbn)
		return bookIsbn

	def getTitile(self):
		text = unicode(self.field_title.text())
		title = validations.validate(Constants.TITLE, text)
		flag(self.label_title_check, title)
		return title

	def getAuthor(self):
		text = unicode(self.field_author.text())
		author = validations.validate(Constants.AUTHOR, text)
		flag(self.label_author_check, author)
		return author

	def getPublisher(self):
		text = unicode(self.field_publisher.text())
		publisher = validations.validate(Constants.PUBLISHER, text)
		flag(self.label_publisher_check, publisher)
		return publisher

	def getYear(self):
		inputyear = int(self.field_year.value())
		year = validations.validate(Constants.YEAR, inputyear)
		return year

	def getCopy(self):
		copy = int(self.field_copy.value())
		if copy:
			return copy
		return False

	def getLanguage(self):
		# Just used when called from searchISBN for automatic search
		lang = self.field_language.itemData(self.field_language.currentIndex())
		flag(self.label_language_check, self.field_language.currentIndex())

		if lang is not None:
			return str(lang).strip()
		return None

	def getLocation(self):
		location = unicode(self.field_location.text())
		return location

	def getComments(self):
		comments = str(self.field_comments.toPlainText())
		return comments.strip()

	def listIndex(self, Cbox, value):
		index = Cbox.findData(value)
		if index < 0:
			index = 0
		return index


class NewItem(ItemMaster):
	def __init__(self, parent=None):
		super(NewItem, self).__init__()

	def handleButton(self):

		self.cheackall()
		itemData = self.getData2sql()

		if (False in itemData):
			QtGui.QMessageBox.critical(self, 'Error', 'There is information Missing or wrong.', QtGui.QMessageBox.Ok)
		else:
			saved = DataBase.save_new(Constants.TYPE_ITEM, itemData)
			if saved:
				QtGui.QMessageBox.information(self, 'Sucess', 'Item Saved.', QtGui.QMessageBox.Ok)
				self.reset()
				self.cleanall()
				self.cheackall()
			else:
				QtGui.QMessageBox.critical(self, 'Error', 'Error while saving.', QtGui.QMessageBox.Ok)


class EditItem(ItemMaster, QtGui.QDialog):
	def __init__(self, id_, parent=None):
		super(EditItem, self).__init__()
		self.newItem = False  # to identify the module
		if not id_:
			self.frameEditItem.show()
		else:
			ID, ident = validations.validate(Constants.IDS, id_, Session.FORMAT_TYPE_INFO)

		self.retranslateUi2()
		# actions
		self.connect(self.buttonLoadID, QtCore.SIGNAL("clicked()"), self.loadElement)
		self.connect(self.buttonSearch, QtCore.SIGNAL("clicked()"), self.searchItem)
		self.connect(self.field_itemID, QtCore.SIGNAL("textChanged(QString)"), self.changeID)

	def changeID(self):
		self.checkID()
		self.cleanall()

	def searchItem(self):
		self.searchElement(Constants.TYPE_ITEM, Constants.ALL_ITEMS)

	def searchElement(self, type_, status):
		# Select the type of search window
		if type_ == Constants.TYPE_ITEM:
			Searcher = SearchItemWin(True, status, self)
		else:
			return 0
		Searcher.exec_()
		# After closing the dialog search for the Id of the object to be shown
		ID = Searcher.ID
		if type_ == Constants.TYPE_USER:
			if ID:
				self.field_readerID.setText(ID)
				self.loadElement()
			else:
				self.cleanReader()
		elif type_ == Constants.TYPE_ITEM:
			if ID:
				self.field_itemID.setText(ID)
				self.loadElement()
			else:
				self.cleanall()

	def checkID(self):
		aux = unicode(self.field_itemID.text()).strip()
		id_, ident = validations.validate(Constants.IDS, aux, Session.FORMAT_TYPE_INFO)
		flag(self.check_itemID, id_)
		return id_, ident

	def loadElement(self):
		id_, ident = self.checkID()
		if not id_:
			return False
		item = Item(id_)
		if item:
			if not item.formatID() == ident:
				return False
			self.showItemData(item)
		return id_, ident

	def showItemData(self, item):
		isbn = item.ISBN()
		if isbn:
			self.needsISBN = True
		self.fillItemFields(item)

	def handleButton(self):
		itemData = self.getData2sql()
		itemData.append(self.checkID()[0])  # gets the ID, but not the aux variable used to test the type of item

		if (False in itemData):
			QtGui.QMessageBox.critical(self, 'Error', 'There is information Missing or wrong.', QtGui.QMessageBox.Ok)
		else:
			edited = DataBase.edit_itemUser(Constants.TYPE_ITEM, itemData)
			if edited:
				QtGui.QMessageBox.information(self, 'Sucess', 'Item Saved.', QtGui.QMessageBox.Ok)
				self.reset()
				self.cleanall()
				self.field_itemID.setText(Constants.EMPTY)
			else:
				QtGui.QMessageBox.critical(self, 'Error', 'Error while saving.', QtGui.QMessageBox.Ok)

	def retranslateUi2(self):
		self.retranslateUi(self)
		self.setWindowTitle(_translate("NewItem", "Edit Item", None))
		self.title.setText(_translate("NewItem", "Edit Item", None))
		self.button_add.setText(_translate("NewItem", "Edit", None))
