#!/usr/bin/python
# -*- coding: utf-8 -*

#mSelecUser.py: Shows all users, selects one, will send it to DispUser
#

import wx
import cfg
import mDisplayinfo
import wx.lib.mixins.listctrl as listmix
#import sys

#All Glory for this goes to the people at http://code.activestate.com/recipes/426407-columnsortermixin-with-a-virtual-wxlistctrl/
class SortedVirtualAutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style = wx.LC_REPORT | wx.LC_HRULES| wx.LC_VIRTUAL)
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		listmix.ColumnSorterMixin.__init__(self, 1)			#Cantidad de columnas
		self.InsertColumn(0, "Nombre", width = 100)
		#self.InsertColumn(1, u"Autor")
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

	def OnItemActivated(self, event):
		#Maybe there's a simple way to get the index. I don't know it, and don't know how to search for it.
		item = event.m_itemIndex
		index = self.itemIndexMap[item]
		self.GetGrandParent().SendIdn(index)
		
	def OnGetItemText(self, item, col):
		index = self.itemIndexMap[item]
		if col == 0: return cfg.uss[index].GetName()
		#if col == 1: return cfg.bks[index].GetAuthor()

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
	#Might need it later
	#~ def GetSortImages(self):
		#~ return (self.sm_dn, self.sm_up)

class SelecUser(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent = parent,style = wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.CAPTION | wx.MINIMIZE_BOX| wx.CLOSE_BOX)
		self.PanelUI()
		self.SetSize((1000, 600))
		self.SetTitle(u'Búsqueda de Usuario')
		self.Centre()
		self.Show()
		#self.Maximize()

	def PanelUI(self):
		self.limlist = cfg.uss
		self.idn = ""
		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self, -1)

		fgs = wx.FlexGridSizer(2, 1, 2, 2)		#row, col, margin, margin
		self.ckbNm = wx.CheckBox(panel, label = u"El nombre del usuario contiene:")
		self.tcNm = wx.TextCtrl(panel)
		fgs.AddMany([(self.ckbNm), (self.tcNm, 1, wx.EXPAND)])
		#self.ckbSn = wx.CheckBox(panel, label = "El apellido contiene:")
		#self.tcSn = wx.TextCtrl(panel)
		#fgs.AddMany([(self.ckbAu), (self.tcAu, 1, wx.EXPAND)])
		fgs.AddGrowableCol(1)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckText)				#All events go to OnCheck, regardless of list
		self.Bind(wx.EVT_TEXT,self.OnCheckText)

		self.stinst = wx.StaticText(panel,label = u"Haga doble click para seleccionar el usuario:")
		auxlst = {}
		self.lst = SortedVirtualAutoWidthListCtrl(panel)
			
		vbox.AddMany([(fgs, 0, wx.EXPAND),(self.stinst, 0, wx.ALIGN_CENTER_HORIZONTAL)])
		vbox.Add(self.lst, 1, wx.EXPAND)
		panel.SetSizer(vbox)

		#Initialization/Default values	
		self.ckbNm.SetValue(True) #Asumo que la búsqueda por nombre es el default.
		#self.ckbfv.SetValue(True)
		#self.Limit("")	#For filling.
		self.ReDoList()

	def ReDoList(self):
		self.lst.DeleteAllItems()
		auxlst = {}
		for key, item in self.limlist.iteritems(): 
			if cfg.IsNotBor(item):
				auxlst[key] = item.GetName()				#it allows for the sorting
		self.lst.itemDataMap = auxlst
		self.lst.itemIndexMap = self.limlist.keys()
		self.lst.SetItemCount(len(self.limlist))
		#~ items = self.limlist.items()
		#~ for key,se in items:
			#~ index = self.lst.InsertStringItem(sys.maxint, se.GetPal())
			#~ self.lst.SetItemData(index, key)

	def OnCheckText(self, e):
		#stSn = ""
		stNm = ""
		#if self.ckbSn.GetValue(): stSn = self.tcSn.GetValue()
		if self.ckbNm.GetValue(): stNm = self.tcNm.GetValue()
		#stSn = stSn.strip()
		stNm = stNm.strip()
		self.Limit(stNm)

	def Limit(self, stNm):
		new_list = {}
		items = cfg.uss.items()
		for key, us in items:
			if (stNm in us.GetName()):
			#if (stau in bk.GetAuthor()) and (stti in bk.GetTitle()):
				new_list[key] = us
		self.limlist = new_list
		self.ReDoList()

	def SendIdn(self, idn):
		self.GetParent().RecieveIdn(idn, 1)
		self.Close()
		#print idn

