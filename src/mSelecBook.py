#!/usr/bin/python
# -*- coding: utf-8 -*

#mSelecBook.py: Shows all books, selects one, sends it to Display
#

import wx
import cfg
import mDispBook
import wx.lib.mixins.listctrl as listmix
from Tools.sqlite import load_table

#import sys

#All Glory for this goes to the people at http://code.activestate.com/recipes/426407-columnsortermixin-with-a-virtual-wxlistctrl/
class SortedVirtualAutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__( self, parent, -1, style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VIRTUAL)

		#definitions for colors
		self.attr0 = wx.ListItemAttr()
		self.attr0.SetBackgroundColour("red")
		self.attr1 = wx.ListItemAttr()
		self.attr1.SetBackgroundColour("green")

		#mixins
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		listmix.ColumnSorterMixin.__init__(self, 4)			#Cantidad de columnas

		#building the columns
		self.InsertColumn(0,  "ID"     , width = 50)
		self.InsertColumn(1,  "ISBN"   , width = 150)
		self.InsertColumn(2, u"Título" , width = 350)
		self.InsertColumn(3,  "Autor"  , width = 250)

		#events
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

	# Se activa con el doble click al elemento de la lista
	#Maybe there's a simple way to get the index. I don't know it, and don't know how to search for it.
	def OnItemActivated(self, event):
		#Maybe there's a simple way to get the index. I don't know it, and don't know how to search for it.
		item = event.m_itemIndex
		index = self.itemIndexMap[item]
		self.GetGrandParent().SendIdn(index)

	def OnGetItemText(self, item, col):
		index = self.itemIndexMap[item]
		self.libro_t = self.LibrosDB[index]
		if col == 0: return cfg.bks[index].GetTitle()
		if col == 1: return cfg.bks[index].GetAuthor()
		'''
		if col == 0: return self.libro_t['id_libro']
		if col == 1: return self.libro_t['isbn']
		if col == 2: return self.libro_t['titulo']
		if col == 3: return self.libro_t['autor']
		'''

	def SortItems(self,sorter=cmp):
		items = list(self.itemDataMap.keys())
		items.sort(sorter)
		self.itemIndexMap = items
		# redraw the list
		self.Refresh()

	# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
	def GetListCtrl(self):
		return self

	#~ # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
	#Will need it later
	#~ def GetSortImages(self):
		#~ return (self.sm_dn, self.sm_up)

#es la ventana que aparece al hacer click en el boton de buscar en el programa principal
class SelecBook(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent = parent,style = wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.CAPTION | wx.MINIMIZE_BOX| wx.CLOSE_BOX)

		self.SetSize((1000, 600))
		self.SetTitle(u'Buscar Libro')
		self.Centre()
		self.Show()
		#self.Maximize()
		self.PanelUI()

	def PanelUI(self):
		self.limlist = cfg.bks
		self.idn = ""
		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self, -1)
			
		fgs = wx.FlexGridSizer(2, 2, 2, 2)		#row, col, margin, margin
		self.ckbTi = wx.CheckBox(panel, label = u"El título contiene:")
		self.tcTi = wx.TextCtrl(panel)
		fgs.AddMany([(self.ckbTi), (self.tcTi, 1, wx.EXPAND)])
		self.ckbAu = wx.CheckBox(panel, label = "El autor contiene:")
		self.tcAu = wx.TextCtrl(panel)
		fgs.AddMany([(self.ckbAu), (self.tcAu, 1, wx.EXPAND)])
		fgs.AddGrowableCol(1)
		
		#ventos
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckText)				#All events go to OnCheck, regardless of list
		self.Bind(wx.EVT_TEXT,self.OnCheckText)

		self.stinst = wx.StaticText(panel,label = u"Haga doble click para seleccionar el libro:")
		auxlst = {}
		#for key, item in self.limlist.iteritems(): auxlst[key] = item.GetTitle()				#it allows for the sorting
		#self.lst = SortedVirtualAutoWidthListCtrl(panel, auxlst)
		self.lst = SortedVirtualAutoWidthListCtrl(panel)

		vbox.AddMany([(fgs, 0, wx.EXPAND),(self.stinst, 0, wx.ALIGN_CENTER_HORIZONTAL)])
		vbox.Add(self.lst, 1, wx.EXPAND)
		panel.SetSizer(vbox)

		#Initialization/Default values	
		self.ckbTi.SetValue(True) #Asumo que la búsqueda por título es el default.
		#self.ckbfv.SetValue(True)
		#self.Limit("")	#For filling.
		self.ReDoList()

	def ReDoList(self):
		self.lst.DeleteAllItems()
		auxlst = {}
		for key, item in self.limlist.iteritems(): 
			if cfg.IsNotBor(item):
				auxlst[key] = item.GetTitle()				#it allows for the sorting
		self.lst.itemDataMap = auxlst
		self.lst.itemIndexMap = self.limlist.keys()
		self.lst.SetItemCount(len(self.limlist))
		#~ items = self.limlist.items()
		#~ for key,se in items:
			#~ index = self.lst.InsertStringItem(sys.maxint, se.GetPal())
			#~ self.lst.SetItemData(index, key)

	def OnCheckText(self, e):
		stau = ""
		stti = ""
		if self.ckbAu.GetValue(): stau = self.tcAu.GetValue()
		if self.ckbTi.GetValue(): stti = self.tcTi.GetValue()
		stau = stau.strip()
		stti = stti.strip()
		self.Limit(stau, stti)

	def Limit(self,stau,stti):
		new_list = {}
		items = cfg.bks.items()
		for key, bk in items:
			if (stau in bk.GetAuthor()) and (stti in bk.GetTitle()):
				new_list[key] = bk
		self.limlist = new_list
		self.ReDoList()

	def SendIdn(self, idn):
		self.GetParent().RecieveIdn(idn, 'book')
		self.Close()

