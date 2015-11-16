# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/Gui/dialogs/mSelectTargetFile.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SelectTargetFile(object):
    def setupUi(self, SelectTargetFile):
        SelectTargetFile.setObjectName(_fromUtf8("SelectTargetFile"))
        SelectTargetFile.resize(529, 116)
        self.verticalLayout = QtGui.QVBoxLayout(SelectTargetFile)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(SelectTargetFile)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.field_path = QtGui.QLineEdit(self.groupBox)
        self.field_path.setObjectName(_fromUtf8("field_path"))
        self.horizontalLayout.addWidget(self.field_path)
        self.btn_searchFile = QtGui.QPushButton(self.groupBox)
        self.btn_searchFile.setObjectName(_fromUtf8("btn_searchFile"))
        self.horizontalLayout.addWidget(self.btn_searchFile)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btnCancel = QtGui.QPushButton(SelectTargetFile)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.btnExport = QtGui.QPushButton(SelectTargetFile)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout_3.addWidget(self.btnExport)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(SelectTargetFile)
        QtCore.QMetaObject.connectSlotsByName(SelectTargetFile)

    def retranslateUi(self, SelectTargetFile):
        SelectTargetFile.setWindowTitle(_translate("SelectTargetFile", "Save File", None))
        self.groupBox.setTitle(_translate("SelectTargetFile", "Destination File", None))
        self.btn_searchFile.setText(_translate("SelectTargetFile", "...", None))
        self.btnCancel.setText(_translate("SelectTargetFile", "Cancel", None))
        self.btnExport.setText(_translate("SelectTargetFile", "Export", None))

