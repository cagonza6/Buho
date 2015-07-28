#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Here are located all the interface methods we need to use...
'''

import wx

'''
@text : mensaje a mostrar
@type_: 
'''
def showmessage(text,tittle):
	wx.MessageBox(text, tittle, wx.OK)
	return

def cnt(msg, question= u'\n¿Desea continuar?', title=u'Advertencia'):
	dial = wx.MessageDialog(None, msg+'\n'+question, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
	ret = dial.ShowModal()
	if ret == wx.ID_YES: return True
	else: return False
