# -*- coding: utf-8 -*
from PyQt4 import QtCore


class IdMaster():
	def __init__(self):
		pass

	def connections(self):
		# Actions
		self.connect(self.fieldMasterId, QtCore.SIGNAL("textChanged(QString)"), self.MasterIdChanged)
		# Buttons
		self.connect(self.buttonLoadMasterId, QtCore.SIGNAL("clicked()"), self.MasterIdLoad)
		self.connect(self.buttonSearchMasterId, QtCore.SIGNAL("clicked()"), self.SearchMasterId)

	def MasterIdChanged(self):
		pass

	def MasterIdLoad(self):
		pass

	def SearchMasterId(self):
		pass
