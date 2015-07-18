#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the Frame to display a book

import wx
import cfg

class DispBook(wx.Frame):
	def __init__(self, parent, book):
		wx.Frame.__init__(self, parent = parent, style = wx.RESIZE_BORDER | wx.CLOSE_BOX)

		self.book = book
		self.SetTitle('Datos del Libro')

		self.PanelUI()
		self.Centre()
		self.Show()
		
	def PanelUI(self):
		print self.book
		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self, -1)
		fgs   = wx.FlexGridSizer(4,2,7,15)
		ste   = wx.StaticText(panel, label = "")
		stTi  = wx.StaticText(panel, label = "Título: ")
		stAu  = wx.StaticText(panel, label = "Autor: ")
		stPt  = wx.StaticText(panel, label = "Prestado: ")
		stCm  = wx.StaticText(panel, label = "Comentario: ")
		stTio = wx.StaticText(panel, label = self.book['titulo'])
		stAuo = wx.StaticText(panel, label = self.book['autor'])
		if self.book['estado']:
			stPto = wx.StaticText(panel, label = "No")
		else:
			stPto = wx.StaticText(panel, label = "Si")
		stCmo = wx.StaticText(panel, label = self.book['comentarios'])
		fgs.AddMany([(stTi),(stTio, 1, wx.EXPAND),(stAu),(stAuo, 1, wx.EXPAND),(stPt),(stPto, 2, wx.EXPAND), (stCm),(stCmo, 2, wx.EXPAND)])
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben

		vbox.Add(fgs, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 15)
		panel.SetSizerAndFit(vbox)
		self.Hide()


if __name__ == '__main__':
	#dummy dictionary to test the method
	ddic={'titulo':'Titulo','autor': 'Autor','isbn':'123456789','comentarios': 'no hay comentarios','estado':1}
	ex = wx.App()
	DispBook(None, ddic)
	ex.MainLoop()
