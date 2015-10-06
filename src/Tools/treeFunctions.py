
from PyQt4 import QtGui, QtCore

class TreeWiews():
	def __init__(self, parent=None):
		pass

	def addElement(self, model, columns):
		model.insertRow(0)
		for i in range(0, len(columns)):
			model.setData(model.index(0, i), columns[i])

	def createElementModel(self, data, cols, headers):
		model = QtGui.QStandardItemModel(0, len(cols), self)
		for i in range(0, len(headers)):
			model.setHeaderData(i, QtCore.Qt.Horizontal, headers[i])
		for i in range(0, len(data)):
			values=[]
			element = data[i]
			for j in range(0, len(cols)):
				values.append(element[cols[j]])
			self.addElement(model, values)
		return model
