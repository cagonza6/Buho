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

def cnt(msg):
	dial = wx.MessageDialog(None, msg+"¿Desea continuar?".decode('utf-8'), 'Advertencia', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
	ret = dial.ShowModal()
	if ret == wx.ID_YES: return True
	else: return False
