#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to display a User

import wx
import cfg
import sys

class DispUser(wx.Frame):
	def __init__(self, parent, idn):
		wx.Frame.__init__(self, parent = parent, style = wx.RESIZE_BORDER | wx.CLOSE_BOX)
		#self.SetSize((1000, 600))
		self.us = cfg.uss[idn]
		self.SetTitle(self.us.GetName())
		self.PanelUI()
		self.Centre()
		self.Show()
		
	def PanelUI(self):

		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self, -1)
		fgs = wx.FlexGridSizer(1,2,7,15)
		#Cannons for mosquitoes? Totally. Need it for later
		#ste = wx.StaticText(panel,label = "")
		stNm = wx.StaticText(panel, label = "Nombre")
		stNmo = wx.StaticText(panel, label = self.us.GetName())
		fgs.AddMany([(stNm),(stNmo, 1, wx.EXPAND)])
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben
		
		lcBks = wx.ListCtrl(panel,  -1, style = wx.LC_REPORT)
		lcBks.InsertColumn(0, u'Título', width = 140)
		lcBks.InsertColumn(1, u'Fecha de Devolución', width = 130)

		for item in self.us.GetBooks():
			index = lcBks.InsertStringItem(sys.maxint, cfg.bks[item[0]].GetTitle())
			lcBks.SetStringItem(index, 1, item[1])
			#Add color if the date hasn't been set
			
		
		#~ btsv = wx.Button(self, label = 'Guardar')#, pos=(30, 160))
		#~ btsv.Bind(wx.EVT_BUTTON, self.OnSave)
		#~ fgs.AddMany([(ste),(btsv)])
		
		vbox.Add(fgs, 1, wx.EXPAND)
		vbox.Add(lcBks, 1, wx.EXPAND)
		panel.SetSizerAndFit(vbox)
		panel.Show()
        

#if __name__ == '__main__':
	#ex = wx.App()
	#DispUser(None, 0)
	#ex.MainLoop()    
