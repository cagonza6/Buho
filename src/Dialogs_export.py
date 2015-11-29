# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from Dialogs import PathMethods
from Gui.dialogs.mExportPDF import Ui_PdfExport
from Gui.dialogs.mPrintCards import Ui_SaveCards
import session.Session as Session
import config.GlobalConstants as Constants


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
		if not self.checkPath() or not self.checkFields():
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
