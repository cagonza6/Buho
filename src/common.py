# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

import config.GlobalConstants as Constants

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


def statusIcon(status):
	img = _fromUtf8(Constants.ICON_INVALID)
	if status == Constants.STATUS_INVALID:
		img = _fromUtf8(Constants.ICON_INVALID)
	elif status == Constants.STATUS_VALID:
		img = _fromUtf8(Constants.ICON_VALID)
	elif status == Constants.STATUS_WARNING:
		img = _fromUtf8(Constants.ICON_WARNING)
	return img


def flag(element, flag_):
	if flag_:
		element.setPixmap(QtGui.QPixmap(_fromUtf8(Constants.ICON_VALID)))
	else:
		element.setPixmap(QtGui.QPixmap(_fromUtf8(Constants.ICON_INVALID)))


def flagStatus(element, flag):
	element.setPixmap(QtGui.QPixmap(statusIcon(flag)))
