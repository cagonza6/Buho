# -*- coding: utf-8 -*-

class GuiSearchUserMethdos():
	def __init__(self, parent=None):
		pass

	def connections():
		self.connect(self.field_readerID, QtCore.SIGNAL("textChanged(QString)"), self.OnChangeReaderID)
		self.connect(self.buttonSearchReader, QtCore.SIGNAL("clicked()"), self.searchReader_)

	def openSearchWindow(self, type_):
		searcher = False
		if type_ == Constants.TYPE_USER:
			Searcher = SearchUserWin(True, status, self)
		elif type_ == Constants.TYPE_ITEM:
			Searcher = SearchItemWin(True, status, self)
		return Searcher
