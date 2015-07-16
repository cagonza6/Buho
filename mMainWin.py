#!/usr/bin/python
# -*- coding: utf-8 -*-

#This is my main window.

import wx
import cfg
import Main
import mNewBook
import mSelecBook
import mNewUser
import mSelecUser
import mDispBook
import mDispUser
import mLoanBook
import mRetBook

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
		mBln = wx.MenuItem(bM, wx.ID_FORWARD, '&Prestar Libro\tCtrl+P')
		mBrt = wx.MenuItem(bM, wx.ID_BACKWARD, '&Devolver Libro\tCtrl+D')
		mBnw = wx.MenuItem(bM, wx.ID_NEW, '&Nuevo Libro\tCtrl+N')
		mBse = wx.MenuItem(bM, wx.ID_FIND, '&Buscar Libro\tCtrl+B')
		
		bM.AppendItem(mBln)
		bM.AppendItem(mBrt)
		bM.AppendItem(mBnw)
		bM.AppendItem(mBse)
		
		#Usuarios
		uM = wx.Menu()
		mUnw = wx.MenuItem(bM, wx.ID_ADD, 'Nuevo &Usuario\tCtrl+U')
		mUse = wx.MenuItem(bM, wx.ID_FILE, 'Bu&scar Usuario\tCtrl+S')
		uM.AppendItem(mUnw)
		uM.AppendItem(mUse)

		self.Bind(wx.EVT_MENU, self.OnLoanBook, mBln)
		self.Bind(wx.EVT_MENU, self.OnRetBook, mBrt)
		self.Bind(wx.EVT_MENU, self.OnNewBook, mBnw)
		self.Bind(wx.EVT_MENU, self.OnSearchBook, mBse)
		self.Bind(wx.EVT_MENU, self.OnNewUser, mUnw)
		self.Bind(wx.EVT_MENU, self.OnSearchUser, mUse)
		self.Bind(wx.EVT_MENU, self.OnTry, mitry)
		self.Bind(wx.EVT_MENU, self.OnQuit, mFqt)

		mb.Append(fM, '&Acciones')
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
		
	def OnLoanBook(self, e):
		self.ChangePanel(mLoanBook.LoanBook(self,self.GetSize()))
		
	def OnNewBook(self, e):
		self.ChangePanel(mNewBook.NewBook(self,self.GetSize()))
        
	def ChangePanel(self, Panel):
		if cfg.lockwin:
			if cfg.cnt(u"La información no guardada se perderá. "):
				cfg.lockwin = False			#If user wants to continue, act as if there's no lock

		if not(cfg.lockwin):								#Windows empty or user has said xe doesn't care
			self.panel.Destroy()
			self.panel = Panel
			self.panel.Show()
			cfg.lockwin = True

	def OnSearchBook(self, e):
		self.panel.Hide()
		mSelecBook.SelecBook(self)
	      
	def OnNewUser(self, e):
		self.ChangePanel(mNewUser.NewUser(self,self.GetSize()))
		
	def OnSearchUser(self,e):
		self.panel.Hide()

		mSelecUser.SelecUser(self)
		
	def RecieveIdn(self, idn, what):
		if what == 0: mDispBook.DispBook(self, idn)
		if what == 1: mDispUser.DispUser(self, idn)
		
	def OnQuit(self, e):
		Main.end_save()
		self.Close(True)
        
	def to_do(self,what):
		wx.MessageBox(what+' no está implementado', 'Falla Temporal', wx.OK)
      
if __name__ == '__main__':
  
	app = wx.App()
	MainWin(None)
	app.MainLoop()
        
#Achicar para display?
