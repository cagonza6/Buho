# -*- coding: utf-8 -*-
import os.path

from PyQt4 import QtCore, QtGui
from Gui.dialogs.mExportPDF import Ui_PdfExport
from Gui.dialogs.mSelectTargetFile import Ui_SelectTargetFile
from Tools.timeFunctions import todaysDate

import config.GlobalConstants as Constants


class PathMethods(QtGui.QDialog):
	def __init__(self, parent=None):
		super(PathMethods, self).__init__()
		self.setupUi(self)
		self.connect(self.btn_searchFile, QtCore.SIGNAL("clicked()"), self.searchFile)
		self.connect(self.btnExport, QtCore.SIGNAL("clicked()"), self.getExportInfo)
		self.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), self.closeWin)

	def searchFile(self):
		path = str(QtGui.QFileDialog.getSaveFileName(self, "Select Directory", '%s.pdf' % (self.baseName + '-' + str(todaysDate()), ), '*.pdf'))
		path = os.path.normcase(path)
		self.field_path.setText(path)

	def checkPath(self, path):
		checkPath = os.access(os.path.dirname(path), os.W_OK)
		if not checkPath:
			QtGui.QMessageBox.critical(self, 'Error', 'Invalid path to file.', QtGui.QMessageBox.Ok)
			return False
		return True

	def closeEvent(self, event):
		self.closeWin()

	def closeWin(self):
		self.accept()


class GetPath(Ui_SelectTargetFile, PathMethods):
	def __init__(self, baseName='Card', parent=None):
		super(GetPath, self).__init__()
		self.baseName = baseName
		self.pathToFile = ''

	def getExportInfo(self):
		self.pathToFile = path = str(self.field_path.text()).strip()
		if not self.checkPath(path):
			return
		self.accept()

	def closeWin(self):
		self.pathToFile = False
		self.accept()


class PdfExport(Ui_PdfExport, PathMethods):
	def __init__(self, headers, maping, subtitle, baseName='Report', orientation=Constants.PAPER_PORTAIL, parent=None):
		super(PdfExport, self).__init__()

		if orientation == Constants.PAPER_LANDSCAPE:
			self.radio_landscape.setChecked(True)
		else:
			self.radio_portail.setChecked(True)

		self.headers = headers
		headers[0] = '#'
		self.maping = maping
		self.pathToFile = False
		self.subtitle = subtitle
		self.baseName = baseName

		self.cheks = [
			self.checkBox_01, self.checkBox_02, self.checkBox_03, self.checkBox_04,
			self.checkBox_05, self.checkBox_06, self.checkBox_07, self.checkBox_08,
			self.checkBox_09, self.checkBox_10, self.checkBox_11, self.checkBox_12
		]

		self.field_title.setText(subtitle)

		for i in range(0, len(self.cheks)):
			self.cheks[i].hide()
		for i in range(0, len(self.headers)):
			self.cheks[i].show()
			self.cheks[i].setText(headers[i])
			if self.maping[i]:
				self.cheks[i].setCheckState(QtCore.Qt.Checked)

	def getExportInfo(self):
		self.maping = self.remaping()
		self.pathToFile = path = str(self.field_path.text()).strip()
		self.subtitle = unicode(self.field_title.text())
		self.orientation = self.checkOrientation()
		if not self.checkPath(path) or not self.checkFields():
			return
		self.accept()

	def checkOrientation(self):
		if self.radio_portail.isChecked():
			return Constants.PAPER_PORTAIL
		return Constants.PAPER_LANDSCAPE

	def checkFields(self):
		if not self.checkMaping(self.maping):
			QtGui.QMessageBox.critical(self, 'Error', 'At least two [2] fields required.', QtGui.QMessageBox.Ok)
			return False
		return True

	def closeWin(self):
		self.maping = self.maping * 0
		self.pathToFile = False
		self.accept()

	def checkMaping(self, maping):
		cnt = 0
		for var in maping:
			if var:
				cnt += 1
			if cnt > 1:
				return True
		return False

	def remaping(self):
		maping = []
		for i in range(0, len(self.headers)):
			if self.cheks[i].isChecked():
				maping.append(1)
			else:
				maping.append(0)
		return maping
