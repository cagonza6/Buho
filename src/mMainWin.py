#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is my main window.

import wx
import cfg
import Main
import mNewBook
import mSearchWindows
import mNewUser
import mDisplayinfo
import mLoanBook
import mRetBook
import Tools.interface as Iface # mensajes por pantall
import wx.lib.mixins.listctrl as listmix
from Tools.sqlite import load_table

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
		mitry = wx.MenuItem(fM, wx.ID_RETRY, '&TryTest\tCtrl+T')
		mFqt = wx.MenuItem(fM, wx.ID_EXIT, 'Salir (&Q) \tCtrl+Q')
		
		fM.AppendItem(mitry)
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
		self.Bind(wx.EVT_MENU, self.OnTry, mitry)
		self.Bind(wx.EVT_MENU, self.OnQuit, mFqt)

		mb.Append(fM, '&Acciones')
		mb.Append(pM, '&Préstamos')
		mb.Append(bM, '&Libro')
		mb.Append(uM, '&Usuario')
		self.SetMenuBar(mb)

		self.SetSize((750, 500))
		self.SetTitle('Biblioteca')

	def OnTry(self, e):
		pass
		#aux = mLoanBook.LoanBook(self,self.GetSize())
		#self.ChangePanel(aux)
		#mDispUser.DispUser(self, 1)

	def OnRetBook(self, e):
		self.ChangePanel(mRetBook.RetBook(self,self.GetSize()))
	
	def OnEditLoan(self, e):
		print "No está hecho"
		pass
		
	def OnLoanBook(self, e):
		self.ChangePanel(mLoanBook.LoanBook(self,self.GetSize()) )

	def OnNewBook(self, e):
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
		mSearchWindows.SearchBook(self)

	def OnNewUser(self, e):
		self.ChangePanel(mNewUser.NewUser(self,self.GetSize()))
		
	def OnSearchUser(self,e):
		self.panel.Hide()
		mSearchWindows.SearchUser(self)

	def RecieveIdn(self, data, tipo):
		if tipo == 'book':
			mDisplayinfo.DispBook(self, data)
		if tipo == 'user':
			mDisplayinfo.DispUser(self, data)

	def OnQuit(self, e):
		Main.end_save()
		self.Close(True)

	def to_do(self,what):
		wx.MessageBox(what+' no está implementado', 'Falla Temporal', wx.OK)

	def getBook(self,book_id):
		if book_id > len (self.BooksDB):
			return False
		return self.BooksDB[book_id]

	def getUser(self,user_id):
		if user_id > len (self.UsersDB):
			return False
		return self.UsersDB[user_id]

if __name__ == '__main__':
  
	app = wx.App()
	MainWin(None)
	app.MainLoop()
        
#Achicar para display?
