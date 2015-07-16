#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the Frame to display a book

import wx
import cfg

class DispBook(wx.Frame):
	def __init__(self, parent, idn):
		wx.Frame.__init__(self, parent = parent, style = wx.RESIZE_BORDER | wx.CLOSE_BOX)
		#self.SetSize((1000, 600))
		self.bk = cfg.bks[idn]
		self.SetTitle(self.bk.GetTitle())
		self.PanelUI()
		self.Centre()
		self.Show()
		
	def PanelUI(self):

		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self, -1)
		fgs = wx.FlexGridSizer(4,2,7,15)
		ste = wx.StaticText(panel, label = "")
		stTi = wx.StaticText(panel, label = "Título: ")
		stAu = wx.StaticText(panel, label = "Autor: ")
		stPt = wx.StaticText(panel, label = "Prestado: ")
		stCm = wx.StaticText(panel, label = "Comentario: ")
		stTio = wx.StaticText(panel, label = self.bk.GetTitle())
		stAuo = wx.StaticText(panel, label = self.bk.GetAuthor())
		if self.bk.GetOwner() == 1: stPto = wx.StaticText(panel, label = "No")
		else: stPto = wx.StaticText(panel, label = "Si")
		stCmo = wx.StaticText(panel, label = self.bk.GetCmnt())
		fgs.AddMany([(stTi),(stTio, 1, wx.EXPAND),(stAu),(stAuo, 1, wx.EXPAND),(stPt),(stPto, 2, wx.EXPAND), (stCm),(stCmo, 2, wx.EXPAND)])
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben
	
		##Fake Addition
		#tcTi.SetValue("Tríbes")
		#tcAu.SetValue("M. Sandrïne")
	
		#btsv = wx.Button(self, label = 'Guardar')#, pos=(30, 160))
		#btsv.Bind(wx.EVT_BUTTON, self.OnSave)
		#fgs.AddMany([(ste),(btsv)])
		
		vbox.Add(fgs, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 15)
		panel.SetSizerAndFit(vbox)
		self.Hide()
        

#if __name__ == '__main__':
	#ex = wx.App()
	#DispBook(None, 0)
	#ex.MainLoop()    
