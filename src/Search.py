# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from Gui.mSearch import Ui_SearchItemWindow
from Tools.ItemTools import formatID
from Tools.Database import DBManager as DataBase
from Tools.regexe import cleanKeywords
from Tools.treeFunctions import TreeWiews
from Tools.timeFunctions import int2date, todaysDate

import config.GlobalConstants as Constants
from common import _translate, statusIcon
import session.Session as Session
from InfoWindows import ReaderInfo, ItemInfo


class QCustomDelegate(QtGui.QItemDelegate):
	def __init__(self, type_list, parent=None):
		super(QCustomDelegate, self).__init__()
		self.type_list = type_list

	def paint(self, painterQPainter, optionQStyleOptionViewItem, indexQModelIndex):
		column = indexQModelIndex.column()
		if column == 0:
			currentQAbstractItemModel = indexQModelIndex.model()
			iconQModelIndex = currentQAbstractItemModel.index(indexQModelIndex.row(), 0, indexQModelIndex.parent())
			status = currentQAbstractItemModel.data(iconQModelIndex, QtCore.Qt.EditRole)
			iconQPixmap = QtGui.QPixmap(statusIcon(status, self.type_list))

			if not iconQPixmap.isNull():
				painterQPainter.drawPixmap(
					optionQStyleOptionViewItem.rect.x(),
					optionQStyleOptionViewItem.rect.y(),
					iconQPixmap.scaled(16, 16, QtCore.Qt.KeepAspectRatio)
				)
		else:
			QtGui.QItemDelegate.paint(self, painterQPainter, optionQStyleOptionViewItem, indexQModelIndex)


class SortTree(QtGui.QSortFilterProxyModel):
	def __init__(self, parent=None):
		super(SortTree, self).__init__(parent)

	def filterAcceptsRow(self, sourceRow, sourceParent):
		index0 = self.sourceModel().index(sourceRow, 1, sourceParent)
		index1 = self.sourceModel().index(sourceRow, 2, sourceParent)
		index2 = self.sourceModel().index(sourceRow, 3, sourceParent)

		return (
			self.filterRegExp().indexIn(self.sourceModel().data(index0)) >= 0 or
			self.filterRegExp().indexIn(self.sourceModel().data(index1)) >= 0 or
			self.filterRegExp().indexIn(self.sourceModel().data(index2)) >= 0
		)

	def lessThan(self, left, right):
		leftData = self.sourceModel().data(left)
		rightData = self.sourceModel().data(right)

		return leftData < rightData


class SearchMaster(QtGui.QDialog, Ui_SearchItemWindow, TreeWiews):
	def __init__(self, parent=None):
		super(SearchMaster, self).__init__()

		self.setupUi(self)
		self.proxyModel = SortTree(self)
		self.proxyModel.setDynamicSortFilter(True)

		# Final value initialized as false
		self.ID = False

		# Search Type
		self.filterSyntaxComboBox.addItem("Fixed string", QtCore.QRegExp.FixedString)
		self.filterSyntaxComboBox.addItem("Regular expression", QtCore.QRegExp.RegExp)
		self.filterSyntaxComboBox.addItem("Wildcard", QtCore.QRegExp.Wildcard)

		# actions
		self.connect(self.proxyView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.filteredTreeClicked)

		self.filterPatternLineEdit.textChanged.connect(self.textFilterChanged)
		self.filterSyntaxComboBox.currentIndexChanged.connect(self.textFilterChanged)

		self.proxyView.setModel(self.proxyModel)
		self.setTreeDecorations(self.proxyView, True)
		self.proxyView.sortByColumn(1, QtCore.Qt.AscendingOrder)

	# Activated when the text of the filter changes.
	def textFilterChanged(self):
		syntax = QtCore.QRegExp.PatternSyntax(
			self.filterSyntaxComboBox.itemData(
				self.filterSyntaxComboBox.currentIndex()))

		caseSensitivity = False
		regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(), caseSensitivity, syntax)
		self.proxyModel.setFilterRegExp(regExp)

	def filteredTreeClicked(self):
		self.ID = str(self.proxyView.selectedIndexes()[1].data())
		if self.closable:
			self.accept()
			return
		if self.ID:
			self.openSearcher(self.ID)


class SearchItemWin(SearchMaster):
	def __init__(self, closable, status, parent=None):
		super(SearchItemWin, self).__init__()
		self.closable = closable
		self.ID = False

		self.proxyView.setItemDelegate(QCustomDelegate(Constants.TYPE_ITEM))

		# button actions
		self.connect(self.button_search, QtCore.SIGNAL("clicked()"), self.btnSearch)

		# set the status combo box
		statuses = [
			['Can be loaned', Constants.AVAILABLE_ITEMS],
			['Loaned Items', Constants.LOANED_ITEMS],
			['Dued Items', Constants.DUED_ITEMS],
			['All Items', Constants.ALL_ITEMS]
		]
		for i in range(0, len(statuses)):
			status_ = statuses[i]
			self.combo_status.addItem(*status_)  # text to show in the combobox
			if status_[1] == status:
				self.combo_status.setCurrentIndex(i)

		# Search Parameters
		search_fields = [['Titulo', 'title'], ['Autor', 'author'], ['Editorial', 'publisher'], ]
		for field in search_fields:
			self.combo_parameters.addItem(*field)  # text to show in the combobox

		self.combo_functions.addItem('All', False)
		for format_ in Session.FORMAT_TYPE_INFO:
			self.combo_functions.addItem(format_['formatNameShort'], format_['formatID'])
		# sets the default type to search

		self.headers = ['', "ID", "Title", "Author", "Publisher", "Year", "Language"]

		self.combo_functions.setCurrentIndex(1)
		self.combo_grades.addItem('All', False)
		self.combo_grades.hide()
		self.labelGrades.hide()

		self.retranslateUi_2()

	def btnSearch(self):
		column, keys, role, grade = self.getSearchParams()
		status = self.combo_status.itemData(self.combo_status.currentIndex())
		elements = DataBase.searchItems(status, column, keys, role)

		if not elements:
			elements = []
		self.setSourceModel(self.createElementModel(elements))
		self.setColumnWidth(self.proxyView, [16, 100, 200, 200, 200, 50, 50])

	def getSearchParams(self):
		column = str(self.combo_parameters.itemData(self.combo_parameters.currentIndex())).strip()
		keywords = str(self.field_keywords.text())
		role = self.combo_functions.itemData(self.combo_functions.currentIndex())
		grade = self.combo_grades.itemData(self.combo_grades.currentIndex())
		keys = cleanKeywords(keywords)

		return column, keys, role, grade

	def openSearcher(self, id_):
		if not id_:
			return
		showinfo = ItemInfo(id_, self)
		showinfo.exec_()

	def createElementModel(self, elements):
		model = QtGui.QStandardItemModel(0, len(self.headers), self)
		self.setHeaders(model, self.headers)

		for i in range(0, len(elements)):
			element = elements[i]

			if element['loaned']:
				statusicon = Constants.STATUS_WARNING
			if element['dueDate'] < todaysDate():  # dued item
				statusicon = Constants.STATUS_INVALID
			if not element['loaned']:
				statusicon = Constants.STATUS_VALID

			cols = [
				statusicon,
				formatID(element['format'], element['itemID']),
				element['title'],
				element['author'],
				element['publisher'],
				element['year'],
				element['language']
			]
			self.addElement(model, cols)
		return model

	def retranslateUi_2(self):
		self.label_functions.setText(_translate("SearchItemWindow", "Category", None))


class SearchUserWin(SearchMaster):
	def __init__(self, closable, status, parent=None):
		super(SearchUserWin, self).__init__()
		self.closable = closable

		self.proxyView.setItemDelegate(QCustomDelegate(Constants.TYPE_USER))

		# button actions
		self.connect(self.button_search, QtCore.SIGNAL("clicked()"), self.search)

		# set the status combo box
		statuses = [
			['Active', Constants.AVAILABLE_USERS],
			['Inactive', Constants.BLOCKED_USERS],
			['Baned', Constants.BANED_USER],
			['All', Constants.ALL_USERS], ]
		for i in range(0, len(statuses)):
			status_ = statuses[i]
			self.combo_status.addItem(*status_)  # text to show in the combobox
			if status_[1] == status:
				self.combo_status.setCurrentIndex(i)

		# Search Parameters
		search_fields = [['Name', 'name'], ['E-mail', 'email'], ]
		for field in search_fields:
			self.combo_parameters.addItem(*field)  # text to show in the combobox

		self.combo_functions.addItem('All', False)
		for rol in Session.ROLES_INFO:
			self.combo_functions.addItem(rol['roleName'], rol['roleID'])

		# sets the default for role
		self.combo_functions.setCurrentIndex(7)
		self.combo_grades.addItem('All', False)
		for grade in Session.GRADES_INFO:
			self.combo_grades.addItem(grade['gradeName'], grade['gradeID'])

		self.headers = ['', "ID", "Name", "Family Name", "Class"]
		self.retranslateUi_2()

	def search(self):
		column, keys, role, grade = self.getSearchParams()
		status = self.combo_status.itemData(self.combo_status.currentIndex())
		users = DataBase.search_users(status, column, keys, role, grade)
		if not users:
			users = []
		self.setSourceModel(self.createElementModel(users))

		self.setColumnWidth(self.proxyView, [16, 100, 200, 500, 50])

	def getSearchParams(self):
		column = str(self.combo_parameters.itemData(self.combo_parameters.currentIndex())).strip()
		keywords = str(self.field_keywords.text())
		role = self.combo_functions.itemData(self.combo_functions.currentIndex())
		grade = self.combo_grades.itemData(self.combo_grades.currentIndex())
		keys = cleanKeywords(keywords)

		return column, keys, role, grade

	def openSearcher(self, id_):
		if not id_:
			return
		showinfo = ReaderInfo(id_, self)
		showinfo.exec_()

	def createElementModel(self, elements):
		model = QtGui.QStandardItemModel(0, len(self.headers), self)
		self.setHeaders(model, self.headers)

		for i in range(0, len(elements)):
			element = elements[i]

			cols = [
				element['status'],
				formatID(element['role'], element['userID']),
				element['name'],
				element['familyname'],
				element['gradeName']
			]
			self.addElement(model, cols)
		return model

	def retranslateUi_2(self):
		self.label_title.setText(_translate("SearchItemWindow", "Search Readers", None))

class DuedItemWin(SearchMaster):
	def __init__(self, closable, status, parent=None):
		super(DuedItemWin, self).__init__()
		self.closable = closable
		self.ID = False

		self.proxyView.setItemDelegate(QCustomDelegate(Constants.TYPE_ITEM, Constants.TYPE_LOAN))

		# button actions
		self.connect(self.button_search, QtCore.SIGNAL("clicked()"), self.btnSearch)

		# set the status combo box
		statuses = [['Dued Items', Constants.DUED_ITEMS] ]
		for i in range(0, len(statuses)):
			status_ = statuses[i]
			self.combo_status.addItem(*status_)  # text to show in the combobox
			if status_[1] == status:
				self.combo_status.setCurrentIndex(i)

		# Search Parameters
		search_fields = [['Titulo', 'title'], ['Autor', 'author'], ['Editorial', 'publisher'], ]
		for field in search_fields:
			self.combo_parameters.addItem(*field)  # text to show in the combobox

		self.combo_functions.addItem('All', False)
		for format_ in Session.FORMAT_TYPE_INFO:
			self.combo_functions.addItem(format_['formatNameShort'], format_['formatID'])
		# sets the default type to search

		self.headers = [' ', 'Loan ID', 'Item ID', 'Title', 'Author', 'Reader ID', 'Reader', 'Grade', 'Loan Date', 'Due Date', 'Renewals']

		self.combo_functions.setCurrentIndex(1)
		self.combo_grades.addItem('All', False)
		self.combo_grades.hide()
		self.labelGrades.hide()

		self.retranslateUi_2()

	def btnSearch(self):
		column, keys, role, grade = self.getSearchParams()
		# status = self.combo_status.itemData(self.combo_status.currentIndex())
		elements = DataBase.duedItems()

		if not elements:
			elements = []
		self.setSourceModel(self.createElementModel(elements))
		self.setColumnWidth(self.proxyView, [16, 90, 90, 250, 200, 90, 250, 90, 100, 100, 90])

	def getSearchParams(self):
		column = str(self.combo_parameters.itemData(self.combo_parameters.currentIndex())).strip()
		keywords = str(self.field_keywords.text())
		role = self.combo_functions.itemData(self.combo_functions.currentIndex())
		grade = self.combo_grades.itemData(self.combo_grades.currentIndex())
		keys = cleanKeywords(keywords)

		return column, keys, role, grade

	def openSearcher(self, id_):
		pass

	def createElementModel(self, elements):
		model = QtGui.QStandardItemModel(0, len(self.headers), self)
		self.setHeaders(model, self.headers)

		for i in range(0, len(elements)):
			element = elements[i]
			cols = [
				Constants.STATUS_INVALID,
				formatID('LO', element['loanID']),
				formatID(element['format'], element['itemID']),
				element['title'],
				element['author'],
				formatID(element['role'], element['userID']),
				element['name'] + ' ' + element['familyname'],
				element['gradeName'],
				str(int2date(element['loanDate'])),
				str(int2date(element['dueDate'])),
				element['renewals']
			]
			self.addElement(model, cols)
		return model

	def retranslateUi_2(self):
		self.label_functions.setText(_translate("DuedItemWin", "Category", None))
		self.label_title.setText(_translate("DuedItemWin", "Reports: Dued Items", None))

if __name__ == "__main__":
	pass
