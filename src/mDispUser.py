#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is the panel to display a User

import wx
import cfg

class DispUser(wx.Frame):
	def __init__(self, parent, user):
		wx.Frame.__init__(self, parent = parent, style = wx.RESIZE_BORDER | wx.CLOSE_BOX)

		self.user = user
		self.SetTitle('Datos de usuario')

		self.PanelUI()
		self.Centre()
		self.Show()

	def PanelUI(self):
		print self.user
		vbox  = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self, -1)
		fgs   = wx.FlexGridSizer(5,2,7,15)
		# Identificadores
		stNm = wx.StaticText(panel, label = "Nombre(s)")
		stAp = wx.StaticText(panel, label = "Apellido(s)")
		stDi = wx.StaticText(panel, label = "Direccion")
		stTe = wx.StaticText(panel, label = "Telefono")
		stSt = wx.StaticText(panel, label = "Estado")
		# Campos
		laNm = wx.StaticText(panel, label = self.user['nombres'])
		laAp = wx.StaticText(panel, label = self.user['apellidos'])
		laDi = wx.StaticText(panel, label = self.user['direccion'])
		laTe = wx.StaticText(panel, label = self.user['telefono'])

		if self.user['estado']:
			laSt = wx.StaticText(panel, label = "Activo")
		else:
			laSt = wx.StaticText(panel, label = "Inactivo")

		fgs.AddMany([(stNm),(laNm, 1, wx.EXPAND),
		            (stAp),(laAp , 1, wx.EXPAND),
		            (stDi),(laDi , 2, wx.EXPAND),
		            (stTe),(laTe , 2, wx.EXPAND),
		            (stSt),(laSt , 2, wx.EXPAND),
		            ]
		            

		)
		fgs.AddGrowableCol(1, 0)	#me asegura que crezcan como deben

		lcBks = wx.ListCtrl(panel,  -1, style = wx.LC_REPORT)
		lcBks.InsertColumn(0, u'Título', width = 140)
		lcBks.InsertColumn(1, u'Fecha de Devolución', width = 130)
		'''
		for item in self.user.GetBooks():
			index = lcBks.InsertStringItem(sys.maxint, cfg.bks[item[0]].GetTitle())
			lcBks.SetStringItem(index, 1, item[1])
			#Add color if the date hasn't been set
		'''

		#~ btsv = wx.Button(self, label = 'Guardar')#, pos=(30, 160))
		#~ btsv.Bind(wx.EVT_BUTTON, self.OnSave)
		#~ fgs.AddMany([(ste),(btsv)])

		vbox.Add(fgs, 1, wx.EXPAND)
		vbox.Add(lcBks, 1, wx.EXPAND)
		panel.SetSizerAndFit(vbox)
		panel.Show()

if __name__ == '__main__':
	ddic={'telefono':'555-corriente','nombres':'Juan Carlos','apellidos': 'Perez Perez','rut':'12345678-9','comentarios': 'no hay comentarios','estado':1, 'direccion':'Su casa'}
	ex = wx.App()
	DispUser(None, ddic)
	ex.MainLoop()    
