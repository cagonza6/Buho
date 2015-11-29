# -*- coding: utf-8 -*-
import os.path

from PyQt4 import QtCore, QtGui
from common import flag
from Gui.dialogs.mSelectTargetFile import Ui_SelectTargetFile
from Gui.mAbout import Ui_About
from Tools.timeFunctions import todaysDate


class PathMethods(QtGui.QDialog):
	def __init__(self, parent=None):
		super(PathMethods, self).__init__()
		self.setupUi(self)
		self.connect(self.btn_searchFile, QtCore.SIGNAL("clicked()"), self.searchFile)
		self.connect(self.field_path, QtCore.SIGNAL("textChanged(QString)"), self.checkPath)
		self.connect(self.btnExport, QtCore.SIGNAL("clicked()"), self.getExportInfo)
		self.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), self.closeWin)

	def searchFile(self):
		path = str(QtGui.QFileDialog.getSaveFileName(self, "Select Directory", '%s.pdf' % (self.baseName + '-' + str(todaysDate()), ), '*.pdf'))
		path = os.path.normcase(path)
		self.field_path.setText(path)

	def checkPath(self):
		path = str(self.field_path.text())
		isValid = os.access(os.path.dirname(path), os.W_OK)
		if not isValid:
			path = False
		flag(self.pathCheck, path)
		return path

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
		if not self.checkPath():
			return
		self.accept()

	def closeWin(self):
		self.pathToFile = False
		self.accept()


class AboutApplication(QtGui.QDialog, Ui_About):
	def __init__(self, parent=None):
		super(AboutApplication, self).__init__()
		self.setupUi(self)

		self.setWindowTitle("About %s" % QtCore.QCoreApplication.applicationName())
		self.title.setText(QtCore.QCoreApplication.applicationName())
		self.version.setText("Version %s" % QtCore.QCoreApplication.applicationVersion())

		title_font = QtGui.QFont()
		title_font.setBold(True)
		title_font.setPointSize(title_font.pointSize() + 4)
		self.title.setFont(title_font)

		authors = [
			("Maite Barros", "maite.barros@gmail.com"),
			(unicode("Cristian González", 'utf-8'), "cagonza6@gmail.com")
		]
		web = 'http://www.google.com'
		thanksto = False
		self.content.setHtml(self.aboutText(authors, web, thanksto))

	def MakeHtml(self, name, email=False):
		line = name
		if not email:
			return line
		else:
			line = "%s &lt;<a href=\"mailto:%s\">%s</a>&gt;" % (name, email, email)
		return line

	def aboutText(self, authors, kUrl, thanksTo):
		ret = ''
		if kUrl:
			ret += "<p><a href=\"%s\">%s</a></p><p><b>%s:</b>" % (kUrl, kUrl, "Authors")

		for author in authors:
			ret += "<br />" + self.MakeHtml(*author)

		if thanksTo:
			ret += "</p><p><b>%s:</b>" % ("Thanks to", )
			for person in thanksTo:
				ret += "<br />" + self.MakeHtml(person)

		return ret
