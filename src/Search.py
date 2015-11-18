# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from Gui.mSearch import Ui_SearchItemWindow
from Dialogs import PdfExport
from Tools.ItemTools import formatID
from Tools.Database import DBManager as DataBase
from Tools.regexe import cleanKeywords
from Tools.treeFunctions import TreeWiews
from Tools.timeFunctions import int2date, todaysDate, daysbetween
from Tools.pdf import DefaultReport

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
		self.headers = []
		self.reportSubtitle = 'Report'
		self.orientation = Constants.PAPER_LANDSCAPE
		# Search Type
		self.filterSyntaxComboBox.addItem("Fixed string", QtCore.QRegExp.FixedString)
		self.filterSyntaxComboBox.addItem("Regular expression", QtCore.QRegExp.RegExp)
		self.filterSyntaxComboBox.addItem("Wildcard", QtCore.QRegExp.Wildcard)

		# actions
		self.connect(self.proxyView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.filteredTreeClicked)

		# button actions
		self.connect(self.button_search, QtCore.SIGNAL("clicked()"), self.btnSearch)
		self.connect(self.button_2PDF, QtCore.SIGNAL("clicked()"), self.btnToPdf)

		self.filterPatternLineEdit.textChanged.connect(self.textFilterChanged)
		self.filterSyntaxComboBox.currentIndexChanged.connect(self.textFilterChanged)

		self.proxyView.setModel(self.proxyModel)
		self.setTreeDecorations(self.proxyView, True)
		self.proxyView.sortByColumn(1, QtCore.Qt.AscendingOrder)

	def allowReports(self, closable):
		if closable:
			self.optionsBox.hide()

	def fillSearchStatus(self, statuses, status):
		for i in range(0, len(statuses)):
			status_ = statuses[i]
			self.combo_status.addItem(*status_)  # text to show in the combobox
			if status_[1] == status:
				self.combo_status.setCurrentIndex(i)

	def btnSearch(self):
		pass

	def positions2PDF(self, original, positions):
		headersPDF = []
		if not len(positions) == len(original):
			return headersPDF
		for i in range(0, len(positions)):
			if positions[i]:
				headersPDF.append(original[i])
		return headersPDF

	def getTreeData(self, positions):
		data2File = []
		headers = ['#'] + self.headers[1:]  # Avoids the column with the icon status: column 0
		headers = self.positions2PDF(headers, positions)
		data2File = [headers]

		cols, rows = self.proxyModel.columnCount(), self.proxyModel.rowCount()
		if cols != len(positions):
			return data2File
		if not rows or not cols:
			return data2File

		for i in range(0, rows):
			info = [i + 1]
			for j in range(1, cols):  # Avoids the column with the icon status: column 0
				modelIndex = self.proxyModel.index(i, j)
				value = modelIndex.data()
				info.append(unicode(value))
			info = self.positions2PDF(info, positions)
			data2File.append(info)

		return data2File

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

	def btnToPdf(self):
		PDFsaver = PdfExport(self.headers, self.reportPositions, self.reportSubtitle, orientation=self.orientation, parent=self)
		PDFsaver.exec_()
		reportPositions = PDFsaver.maping
		pathToFile = PDFsaver.pathToFile
		self.reportSubtitle = PDFsaver.subtitle
		colWidths = self.positions2PDF(self.colWidths, reportPositions)
		orientation = PDFsaver.orientation
		if PDFsaver.checkMaping(reportPositions):
			self.reportPositions = reportPositions

		if not reportPositions or not pathToFile:
			return

		data = self.getTreeData(reportPositions)
		DefaultReport(data, pathToFile, colWidths, title='Buho Library Manager', subtitle=self.reportSubtitle, orientation=orientation)

	def getSearchParams(self):
		column = int(self.combo_parameters.itemData(self.combo_parameters.currentIndex()))
		keywords = str(self.field_keywords.text())
		role = self.combo_functions.itemData(self.combo_functions.currentIndex())
		grade = self.combo_grades.itemData(self.combo_grades.currentIndex())
		keys = cleanKeywords(keywords, column)
		return column, keys, role, grade


class SearchItemWin(SearchMaster):
	def __init__(self, closable, status, parent=None):
		super(SearchItemWin, self).__init__()
		self.closable = closable
		self.ID = False

		self.proxyView.setItemDelegate(QCustomDelegate(Constants.TYPE_ITEM))

		# set the status combo box
		statuses = [
			['Can be loaned', Constants.AVAILABLE_ITEMS],
			['Loaned Items', Constants.LOANED_ITEMS],
			['Dued Items', Constants.DUED_ITEMS],
			['All Items', Constants.ALL_ITEMS]
		]

		self.fillSearchStatus(statuses, status)

		# Search Parameters
		search_fields = [['Titulo', Constants.TITLE], ['Autor', Constants.AUTHOR], ['Editorial', Constants.PUBLISHER], ['ID', Constants.IDS]]
		for field in search_fields:
			self.combo_parameters.addItem(*field)  # text to show in the combobox

		self.combo_functions.addItem('All', False)
		for format_ in Session.FORMAT_TYPE_INFO:
			self.combo_functions.addItem(format_['formatNameShort'], format_['formatID'])
		# sets the default type to search

		self.headers = [' ', "ID", "Title", "Author", "Publisher", "Year", "Language"]
		self.reportPositions = [1, 1, 1, 1, 1, 1, 1]
		self.colWidths = [
			Constants.WIDTH_NUM, Constants.WIDTH_ID, Constants.WIDTH_NAME, Constants.WIDTH_NAME,
			Constants.WIDTH_NAME, Constants.WIDTH_NUM, Constants.WIDTH_ID
		]
		self.reportSubtitle = 'Items'
		self.combo_functions.setCurrentIndex(1)
		self.combo_grades.addItem('All', False)
		self.combo_grades.hide()
		self.labelGrades.hide()
		self.retranslateUi_2()
		self.allowReports(closable)

	def btnSearch(self):
		column, keys, role, grade = self.getSearchParams()
		status = self.combo_status.itemData(self.combo_status.currentIndex())
		elements = DataBase.searchItems(status, column, keys, role)

		if not elements:
			elements = []
		self.setSourceModel(self.createElementModel(elements))
		self.setColumnWidth(self.proxyView, [16, 100, 200, 200, 200, 50, 50])

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

		# set the status combo box
		statuses = [
			['Active', Constants.AVAILABLE_USERS],
			['Inactive', Constants.BLOCKED_USERS],
			['Baned', Constants.BANED_USER],
			['All', Constants.ALL_USERS], ]

		self.fillSearchStatus(statuses, status)

		# Search Parameters
		search_fields = [['Name', Constants.NAME], ['E-mail', Constants.EMAIL], ['ID', Constants.IDS]]
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

		self.headers = [Constants.EMPTY, "ID", "Name", "Family Name", "Class"]
		self.reportPositions = [1, 1, 1, 1, 1]
		self.colWidths = [40, 70, 160, 160, 70]
		self.colWidths = [Constants.WIDTH_NUM, Constants.WIDTH_ID, Constants.WIDTH_NAME, Constants.WIDTH_NAME, Constants.WIDTH_GRADE]

		self.reportSubtitle = 'Readers'
		self.retranslateUi_2()

	def btnSearch(self):
		column, keys, role, grade = self.getSearchParams()
		status = self.combo_status.itemData(self.combo_status.currentIndex())
		users = DataBase.search_users(status, column, keys, role, grade)
		if not users:
			users = []
		self.setSourceModel(self.createElementModel(users))

		self.setColumnWidth(self.proxyView, [16, 100, 200, 200, 50])

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

		# set the status combo box
		statuses = [['Dued Items', Constants.DUED_ITEMS]]

		self.fillSearchStatus(statuses, status)

		# Search Parameters
		search_fields = [['Titulo', Constants.TITLE], ['Autor', Constants.AUTHOR], ['Editorial', Constants.PUBLISHER], ]
		for field in search_fields:
			self.combo_parameters.addItem(*field)  # text to show in the combobox

		self.combo_functions.addItem('All', False)
		for format_ in Session.FORMAT_TYPE_INFO:
			self.combo_functions.addItem(format_['formatNameShort'], format_['formatID'])
		# sets the default type to search

		self.headers = [
			' ', 'Loan ID', 'Item ID', 'Title', 'Author', 'Reader ID',
			'Reader', 'Grade', 'Loan Date', 'Due Date', 'Renewals', 'Delay / Days'
		]
		self.reportPositions = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
		self.colWidths = [40, 70, 70, 120, 120, 70, 120, 40, 70, 70, 60, 60]
		self.colWidths = [
			Constants.WIDTH_NUM, Constants.WIDTH_ID, Constants.WIDTH_ID,
			Constants.WIDTH_NAME, Constants.WIDTH_NAME, Constants.WIDTH_ID,
			Constants.WIDTH_NAME, Constants.WIDTH_GRADE, Constants.WIDTH_DATE,
			Constants.WIDTH_DATE, Constants.WIDTH_OTHER, Constants.WIDTH_OTHER
		]

		self.reportSubtitle = 'Dued Items'
		self.orientation = Constants.PAPER_LANDSCAPE

		self.combo_functions.setCurrentIndex(1)
		self.combo_grades.addItem('All', False)
		self.combo_grades.hide()
		self.labelGrades.hide()

		self.retranslateUi_2()
		self.optionsBox.show()
		self.allowReports(closable)

	def btnSearch(self):
		column, keys, role, grade = self.getSearchParams()
		status = self.combo_status.itemData(self.combo_status.currentIndex())
		elements = DataBase.duedItems(status, column, keys, role)

		if not elements:
			elements = []
		self.setSourceModel(self.createElementModel(elements))
		self.setColumnWidth(self.proxyView, [16, 90, 90, 250, 200, 90, 250, 90, 100, 100, 90, 90])

	def openSearcher(self, id_):
		pass

	def createElementModel(self, elements):
		model = QtGui.QStandardItemModel(0, len(self.headers), self)
		self.setHeaders(model, self.headers)

		for i in range(0, len(elements)):
			element = elements[i]
			delay = daysbetween(int2date(element['loanDate']), int2date(todaysDate()))
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
				element['renewals'],
				delay
			]
			self.addElement(model, cols)
		return model

	def retranslateUi_2(self):
		self.label_functions.setText(_translate("DuedItemWin", "Category", None))
		self.label_title.setText(_translate("DuedItemWin", "Reports: Dued Items", None))


if __name__ == "__main__":
	pass
