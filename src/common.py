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


def statusIcon(status, type_):
	if type_ == Constants.TYPE_FLAG:
		if status == Constants.STATUS_INVALID:
			return _fromUtf8(Constants.ICON_UNAVAILABLE)
		elif status == Constants.STATUS_VALID:
			return _fromUtf8(Constants.ICON_VALID)
		elif status == Constants.BANED_USER:
			return _fromUtf8(Constants.ICON_WARNING)

	elif type_ == Constants.TYPE_USER:
		if status == Constants.BLOCKED_USERS:
			return _fromUtf8(Constants.ICON_UNAVAILABLE)
		elif status == Constants.AVAILABLE_USERS:
			return _fromUtf8(Constants.ICON_VALID)
		elif status == Constants.BANED_USER:
			return _fromUtf8(Constants.ICON_INVALID)

	elif type_ == Constants.TYPE_ITEM or type_ == Constants.TYPE_LOAN:
		if status == Constants.STATUS_INVALID:
			return _fromUtf8(Constants.ICON_INVALID)
		elif status == Constants.STATUS_VALID:
			return _fromUtf8(Constants.ICON_VALID)
		elif status == Constants.STATUS_WARNING:
			return _fromUtf8(Constants.ICON_WARNING)

		return _fromUtf8(Constants.ICON_INVALID)


def flag(element, flag_):
	if flag_:
		element.setPixmap(QtGui.QPixmap(_fromUtf8(Constants.ICON_VALID)))
	else:
		element.setPixmap(QtGui.QPixmap(_fromUtf8(Constants.ICON_INVALID)))


def flagStatus(element, status):
	element.setPixmap(QtGui.QPixmap(statusIcon(status, Constants.TYPE_FLAG)))


def itemStatusIcon(element, status):
	element.setPixmap(QtGui.QPixmap(statusIcon(status, Constants.TYPE_ITEM)))


def userStatusIcon(element, status):
	element.setPixmap(QtGui.QPixmap(statusIcon(status, Constants.TYPE_USER)))


def loanStatusIcon(element, status):
	element.setPixmap(QtGui.QPixmap(statusIcon(status, Constants.TYPE_ITEM)))
