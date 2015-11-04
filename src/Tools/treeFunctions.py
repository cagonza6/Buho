# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore


class TreeWiews():
	def __init__(self, parent=None):
		pass

	def addElement(self, model, columns):
		model.insertRow(0)
		for i in range(0, len(columns)):
			model.setData(model.index(0, i), columns[i])

	def setHeaders(self, model, headers):
		for i in range(0, len(headers)):
			model.setHeaderData(i, QtCore.Qt.Horizontal, headers[i])

	def setSourceModel(self, model):
		self.proxyModel.setSourceModel(model)

	def setColumnWidth(self, column, widths):
		for i in range(0, len(widths)):
			column.setColumnWidth(i, widths[i])

	def setTreeDecorations(self, tree, sorting):
		tree.sortByColumn(0, QtCore.Qt.AscendingOrder)
		tree.setRootIsDecorated(False)
		tree.setAlternatingRowColors(True)
		tree.setSortingEnabled(sorting)

	def createElementModel(self, data, cols):
		model = QtGui.QStandardItemModel(0, len(cols), self)
		if not data:
			return model
		for i in range(0, len(data)):
			values = []
			element = data[i]
			for j in range(0, len(cols)):
				values.append(element[cols[j]])
			self.addElement(model, values)
		return model
