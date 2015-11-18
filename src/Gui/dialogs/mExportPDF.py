# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/Gui/dialogs/mExportPDF.ui'
#
# Created: Wed Nov 18 11:12:53 2015
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_PdfExport(object):
    def setupUi(self, PdfExport):
        PdfExport.setObjectName(_fromUtf8("PdfExport"))
        PdfExport.resize(529, 352)
        self.verticalLayout = QtGui.QVBoxLayout(PdfExport)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(PdfExport)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox_title = QtGui.QGroupBox(PdfExport)
        self.groupBox_title.setObjectName(_fromUtf8("groupBox_title"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_title)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.field_title = QtGui.QLineEdit(self.groupBox_title)
        self.field_title.setObjectName(_fromUtf8("field_title"))
        self.horizontalLayout_4.addWidget(self.field_title)
        self.horizontalLayout_2.addWidget(self.groupBox_title)
        self.groupBox_2 = QtGui.QGroupBox(PdfExport)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radio_portail = QtGui.QRadioButton(self.groupBox_2)
        self.radio_portail.setChecked(True)
        self.radio_portail.setObjectName(_fromUtf8("radio_portail"))
        self.verticalLayout_2.addWidget(self.radio_portail)
        self.radio_landscape = QtGui.QRadioButton(self.groupBox_2)
        self.radio_landscape.setChecked(False)
        self.radio_landscape.setObjectName(_fromUtf8("radio_landscape"))
        self.verticalLayout_2.addWidget(self.radio_landscape)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.checkBox = QtGui.QGroupBox(PdfExport)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout = QtGui.QGridLayout(self.checkBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox_03 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_03.setObjectName(_fromUtf8("checkBox_03"))
        self.gridLayout.addWidget(self.checkBox_03, 0, 2, 1, 1)
        self.checkBox_07 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_07.setObjectName(_fromUtf8("checkBox_07"))
        self.gridLayout.addWidget(self.checkBox_07, 2, 0, 1, 1)
        self.checkBox_09 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_09.setObjectName(_fromUtf8("checkBox_09"))
        self.gridLayout.addWidget(self.checkBox_09, 2, 2, 1, 1)
        self.checkBox_01 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_01.setObjectName(_fromUtf8("checkBox_01"))
        self.gridLayout.addWidget(self.checkBox_01, 0, 0, 1, 1)
        self.checkBox_10 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_10.setObjectName(_fromUtf8("checkBox_10"))
        self.gridLayout.addWidget(self.checkBox_10, 3, 0, 1, 1)
        self.checkBox_06 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_06.setObjectName(_fromUtf8("checkBox_06"))
        self.gridLayout.addWidget(self.checkBox_06, 1, 2, 1, 1)
        self.checkBox_02 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_02.setObjectName(_fromUtf8("checkBox_02"))
        self.gridLayout.addWidget(self.checkBox_02, 0, 1, 1, 1)
        self.checkBox_11 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_11.setObjectName(_fromUtf8("checkBox_11"))
        self.gridLayout.addWidget(self.checkBox_11, 3, 1, 1, 1)
        self.checkBox_05 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_05.setObjectName(_fromUtf8("checkBox_05"))
        self.gridLayout.addWidget(self.checkBox_05, 1, 1, 1, 1)
        self.checkBox_08 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_08.setObjectName(_fromUtf8("checkBox_08"))
        self.gridLayout.addWidget(self.checkBox_08, 2, 1, 1, 1)
        self.checkBox_04 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_04.setObjectName(_fromUtf8("checkBox_04"))
        self.gridLayout.addWidget(self.checkBox_04, 1, 0, 1, 1)
        self.checkBox_12 = QtGui.QCheckBox(self.checkBox)
        self.checkBox_12.setObjectName(_fromUtf8("checkBox_12"))
        self.gridLayout.addWidget(self.checkBox_12, 3, 2, 1, 1)
        self.verticalLayout.addWidget(self.checkBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btnCancel = QtGui.QPushButton(PdfExport)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.btnExport = QtGui.QPushButton(PdfExport)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout_3.addWidget(self.btnExport)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(PdfExport)
        QtCore.QMetaObject.connectSlotsByName(PdfExport)

    def retranslateUi(self, PdfExport):
        PdfExport.setWindowTitle(_translate("PdfExport", "Save File", None))
        self.groupBox.setTitle(_translate("PdfExport", "Destination File", None))
        self.btn_searchFile.setText(_translate("PdfExport", "...", None))
        self.groupBox_title.setTitle(_translate("PdfExport", "Report title", None))
        self.groupBox_2.setTitle(_translate("PdfExport", "Orientation", None))
        self.radio_portail.setText(_translate("PdfExport", "Portail", None))
        self.radio_landscape.setText(_translate("PdfExport", "Landscape", None))
        self.checkBox.setTitle(_translate("PdfExport", "Columns to export", None))
        self.checkBox_03.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_07.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_09.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_01.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_10.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_06.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_02.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_11.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_05.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_08.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_04.setText(_translate("PdfExport", "CheckBox", None))
        self.checkBox_12.setText(_translate("PdfExport", "CheckBox", None))
        self.btnCancel.setText(_translate("PdfExport", "Cancel", None))
        self.btnExport.setText(_translate("PdfExport", "Save", None))

