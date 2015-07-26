#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is my main window.

import wx
import cfg
import mNewBook
import mSearchWindows
import mNewUser
import mDisplayinfo
import mLoanBook
import mRetBook
import Tools.interface as Iface # mensajes por pantalla
import wx.lib.mixins.listctrl as listmix


class MainWin(wx.Frame):
	
	def __init__(self, parent):
		super(MainWin, self).__init__(parent = parent ,style = wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.CAPTION | wx.MINIMIZE_BOX| wx.CLOSE_BOX)
		self.InitUI()
		self.Centre()
		self.Show(True)

	def InitUI(self):
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.panel = wx.Panel(self,-1)

		mb = wx.MenuBar()

		#Acciones
		fM = wx.Menu()
		mFqt = wx.MenuItem(fM, wx.ID_EXIT, 'Salir (&Q) \tCtrl+Q')
		fM.AppendItem(mFqt)

		#Libros
		bM = wx.Menu()
		mBnw = wx.MenuItem(bM, wx.ID_NEW, '&Nuevo Libro\tCtrl+N')
		mBse = wx.MenuItem(bM, wx.ID_FIND, '&Buscar Libro\tCtrl+B')

		bM.AppendItem(mBnw)
		bM.AppendItem(mBse)

		#Prestamos
		pM = wx.Menu()
		mPln = wx.MenuItem(pM, wx.ID_FORWARD, '&Prestar Libro\tCtrl+P')
		mPed = wx.MenuItem(pM, wx.ID_EDIT, '&Editar Préstamo \tCtrl+E')
		mPrt = wx.MenuItem(pM, wx.ID_BACKWARD, '&Devolver Libro\tCtrl+D')

		pM.AppendItem(mPln)
		pM.AppendItem(mPed)
		pM.AppendItem(mPrt)

		#Usuarios
		uM = wx.Menu()
		mUnw = wx.MenuItem(bM, wx.ID_ADD, 'Nuevo &Usuario\tCtrl+U')
		mUse = wx.MenuItem(bM, wx.ID_FILE, 'Bu&scar Usuario\tCtrl+S')
		uM.AppendItem(mUnw)
		uM.AppendItem(mUse)

		self.Bind(wx.EVT_MENU, self.OnLoanBook, mPln)
		self.Bind(wx.EVT_MENU, self.OnEditLoan, mPed)
		self.Bind(wx.EVT_MENU, self.OnRetBook, mPrt)
		self.Bind(wx.EVT_MENU, self.OnNewBook, mBnw)
		self.Bind(wx.EVT_MENU, self.OnSearchBook, mBse)
		self.Bind(wx.EVT_MENU, self.OnNewUser, mUnw)
		self.Bind(wx.EVT_MENU, self.OnSearchUser, mUse)
		self.Bind(wx.EVT_MENU, self.OnQuit, mFqt)

		mb.Append(fM, '&Acciones')
		mb.Append(pM, '&Préstamos')
		mb.Append(bM, '&Libro')
		mb.Append(uM, '&Usuario')
		self.SetMenuBar(mb)

		self.SetSize((750, 500))
		self.SetTitle('Biblioteca')

	def OnRetBook(self, event):
		self.ChangePanel(mRetBook.RetBook(self,self.GetSize()))

	def OnEditLoan(self, event):
		print "No está hecho"
		pass

	def OnLoanBook(self, event):
		self.ChangePanel(mLoanBook.LoanBook(self,self.GetSize()) )

	def OnNewBook(self, event):
		self.ChangePanel(mNewBook.NewBook(self,self.GetSize()))

	def ChangePanel(self, Panel):
		if cfg.lockwin:
			if Iface.cnt(u'La información no guardada se perderá. '):
				cfg.lockwin = False			#If user wants to continue, act as if there's no lock

		if not(cfg.lockwin):								#Windows empty or user has said xe doesn't care
			self.panel.Destroy()
			self.panel = Panel
			self.panel.Show()
			cfg.lockwin = True

	def OnSearchBook(self, e ):
		self.panel.Hide()
		mSearchWindows.SearchBook(self, 0)			#Mostrar todo

	def OnNewUser(self, e):
		self.ChangePanel(mNewUser.NewUser(self,self.GetSize()))
		
	def OnSearchUser(self,e):
		self.panel.Hide()
		mSearchWindows.SearchUser(self, 0)			#0: Mostrar Todo

	def RecieveIdn(self, data, tipo):
		if tipo == 'book':
			mDisplayinfo.DispBook(self, data)
		if tipo == 'user':
			mDisplayinfo.DispUser(self, data)

	def OnQuit(self, e):
		self.Close(True)

	def to_do(self,what):
		wx.MessageBox(what+' no está implementado', 'TO-DO', wx.OK)
