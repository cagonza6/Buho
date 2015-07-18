#!/usr/bin/python
# -*- coding: utf-8 -*

import wx
import cfg
import mDisplayinfo
import wx.lib.mixins.listctrl as listmix
from Tools.sqlite import load_table
#import sys

#
# Carga la Base de datos
#

def loadUsers():
	##################cargar libros... toodos#######################
	error_str=''
	error = False
	UsersDB = load_table('usuarios')
	if not UsersDB:
		error_str +="Error al cargar Base de datos de usuarios"
		error      = True
	else: 
		print "Usuarios cargados correctamente"
	if error:
		Iface.showmessage(error_str,"Error!")
		return False
	return UsersDB
		####### fin carga libros #######################################

def loadbooks():
	##################cargar libros... toodos#######################
	error_str=''
	error = False
	BooksDB = load_table('libros')
	if not BooksDB:
		error_str +="Error al cargar Base de datos de libros"
		error      = True
	else: 
		print "libros cargados correctamente"
	if error:
		Iface.showmessage(error_str,"Error!")
		return False
	return BooksDB
	####### fin carga libros #######################################

#All Glory for this goes to the people at http://code.activestate.com/recipes/426407-columnsortermixin-with-a-virtual-wxlistctrl/
class TempSortedListPanelUser(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__( self, parent, -1, style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VIRTUAL)

		#definitions for colors
		self.attr0 = wx.ListItemAttr()
		self.attr0.SetBackgroundColour("red")
		self.attr1 = wx.ListItemAttr()
		self.attr1.SetBackgroundColour("green")

		#Status icons
		self.il = wx.ImageList(16, 16)
		a={"sm_ok":"TICK_MARK","sm_no":"CROSS_MARK"}
		for k,v in a.items():
			s="self.%s= self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_%s,wx.ART_TOOLBAR,(16,16)))" % (k,v)
			exec(s)
		self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

		#mixins
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		listmix.ColumnSorterMixin.__init__(self, 1)			#Cantidad de columnas

		#building the columns
		self.InsertColumn(0,  "ID"       , width = 50)
		self.InsertColumn(1,  "Nombre"   , width = 250)
		self.InsertColumn(2, u"Apellido" , width = 250)


		#events
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

	# Se activa con el doble click al elemento de la lista
	#Maybe there's a simple way to get the index. I don't know it, and don't know how to search for it.
	def OnItemActivated(self, event):
		#Maybe there's a simple way to get the index. I don't know it, and don't know how to search for it.
		item = event.m_itemIndex
		index = self.itemIndexMap[item]
		self.GetGrandParent().SendIdn(self.users[index])



    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...
	#este es el bicho que se encarga de llenar las columnas
	def OnGetItemText(self, item, col):
		index = self.itemIndexMap[item]
		self.tuser_ = self.users[index]

		if col == 0: return '' #self.tuser_['id_usuario']
		if col == 1: return self.tuser_['nombres']
		if col == 2: return self.tuser_['apellidos']
		return ''



	def SortItems(self,sorter=cmp):
		items = list(self.itemDataMap.keys())
		items.sort(sorter)
		self.itemIndexMap = items
		# redraw the list
		self.Refresh()

	# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
	def GetListCtrl(self):
		return self

	#
	# Methods that nobody needs but their names expalin more than the method that they call
	#
	
	def cleanpanel(self):
		self.DeleteAllItems() # existing method to clean the panel

	def SetLists(self,users):
		self.users=users


	def OnGetItemImage(self, item):
		index=self.itemIndexMap[item]
		self.estado=self.itemDataMap[index]['estado']
		if not self.estado:
			return self.sm_no
		elif self.estado==1:
			return self.sm_ok
		else:
			return -1

#es la ventana que aparece al hacer click en el boton de buscar en el programa principal
class SearchUser(wx.Frame):
	def __init__(self, parent,users=False):
		wx.Frame.__init__(self, parent = parent,style = wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.CAPTION | wx.MINIMIZE_BOX| wx.CLOSE_BOX)
		if not users:
			self.users = loadUsers()
		self.SetSize((1000, 300))
		self.SetTitle(u'Buscar Usuario')
		self.Centre()
		self.Show()
		#self.Maximize()
		self.PanelUI()

	def PanelUI(self):
		self.idn = 0 # el indice de los usuarios en el arreglo principal
		self.limlist = self.users #este coso define los usuarios
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self, -1)

		fgs = wx.FlexGridSizer(2, 2, 2, 2)		#row, col, margin, margin
		#campos buscador
		#ckeckbox para ajustar que parametro se busca
		self.ckechboxNombre = wx.CheckBox(panel, label = u"El Nombre contiene:")
		self.ckechboxApellido = wx.CheckBox(panel, label = "El Apellido contiene:")
		#campos asociados a las checkbox
		self.tcTi          = wx.TextCtrl(panel)
		self.tcAu          = wx.TextCtrl(panel)

		#campos barra intermedia
		self.stinst = wx.StaticText(panel,label = u"Haga doble click para seleccionar el usuario.")

		fgs.AddMany([(self.ckechboxNombre), (self.tcTi, 1, wx.EXPAND)])
		fgs.AddMany([(self.ckechboxApellido), (self.tcAu, 1, wx.EXPAND)])

		fgs.AddGrowableCol(1)

		#ventos
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckText)				#All events go to OnCheck, regardless of list
		self.Bind(wx.EVT_TEXT,self.OnCheckText)

		#Panel de busquedas
		self.DinamicPanel = TempSortedListPanelUser(panel)
		vbox.AddMany([(fgs, 0, wx.EXPAND),(self.stinst, 0, wx.ALIGN_CENTER_HORIZONTAL)])
		vbox.Add(self.DinamicPanel, 1, wx.EXPAND)
		panel.SetSizer(vbox)

		#Initialization/Default values, debe ser la lista completa
		#inicializa la checkbox de titulo en true como basico
		self.ckechboxNombre.SetValue(True)
		#arma la primera lista de libtos
		self.ReDoList(self.users)

	def ReDoList(self,users):
		self.DinamicPanel.cleanpanel()
		auxlst       = {}
		self.auxKeys = []

		# Aqui es donde agrego todos los metodos q vienen en el problema
		# Se puede transformat un arreglo en diccionarios a mostrar de forma simple
		# Este es el lugar
		for i in range(0,len(users)):
			auxlst[i] = users[i]
			self.auxKeys.append(i)

		self.DinamicPanel.SetLists(auxlst)
		self.DinamicPanel.itemDataMap  = auxlst
		self.DinamicPanel.itemIndexMap = self.auxKeys
		self.DinamicPanel.SetItemCount(len(users)) #este bichodefine cuantas iteraciones se hacen, debe ser la cantidad de usuarios q se dan
		#~ items = self.limlist.items()
		#~ for key,se in items:
			#~ index = self.DinamicPanel.InsertStringItem(sys.maxint, se.GetPal())
			#~ self.DinamicPanel.SetItemData(index, key)

	def OnCheckText(self, e):
		partial_autor = False
		partial_title = False

		if self.ckechboxApellido.GetValue():
			partial_autor = str(self.tcAu.GetValue())
			partial_autor = partial_autor.strip()
			if partial_autor=='':
				partial_autor=False
		if self.ckechboxNombre.GetValue():
			partial_title = self.tcTi.GetValue()
			partial_title = partial_title.strip()
			if partial_title=='':
				partial_title = False
		self.ListaFiltrada(partial_autor, partial_title)

	def ListaFiltrada(self,partial_autor,partial_title):
		#si no hay filtros regresa la lista completa
		if(not partial_autor and not partial_title):
			self.ReDoList(self.users)
			return
		new_list = []
		for i in range(0,len(self.users)):
			self.usuario_ = self.users[i]
			if (partial_autor and partial_autor.lower() in self.usuario_['apellidos'].lower()):
				new_list.append(self.users[i])
			if (partial_title and partial_title.lower() in self.usuario_['nombres'].lower()):
				new_list.append(self.users[i])

		self.ReDoList(new_list)

	def SendIdn(self, user):
		self.GetParent().RecieveIdn(user, 'user')
		self.Close()


#All Glory for this goes to the people at http://code.activestate.com/recipes/426407-columnsortermixin-with-a-virtual-wxlistctrl/
class TempSortedListPanelBook(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__( self, parent, -1, style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VIRTUAL)

		#definitions for colors
		self.attr0 = wx.ListItemAttr()
		self.attr0.SetBackgroundColour("red")
		self.attr1 = wx.ListItemAttr()
		self.attr1.SetBackgroundColour("green")

		#Status icons
		self.il = wx.ImageList(16, 16)
		a={"sm_ok":"TICK_MARK","sm_no":"CROSS_MARK"}
		for k,v in a.items():
			s="self.%s= self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_%s,wx.ART_TOOLBAR,(16,16)))" % (k,v)
			exec(s)
		self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

		#mixins
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		listmix.ColumnSorterMixin.__init__(self, 1)			#Cantidad de columnas

		#building the columns
		self.InsertColumn(0,  "ID"     , width = 50)
		self.InsertColumn(1,  "ISBN"   , width = 150)
		self.InsertColumn(2, u"Título" , width = 350)
		self.InsertColumn(3,  "Autor"  , width = 350)

		#events
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

	# Se activa con el doble click al elemento de la lista
	#Maybe there's a simple way to get the index. I don't know it, and don't know how to search for it.
	def OnItemActivated(self, event):
		#Maybe there's a simple way to get the index. I don't know it, and don't know how to search for it.
		item = event.m_itemIndex
		index = self.itemIndexMap[item]
		self.GetGrandParent().SendIdn(self.books[index])



    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...
	#este es el bicho que se encarga de llenar las columnas
	def OnGetItemText(self, item, col):
		index = self.itemIndexMap[item]
		self.tbook_ = self.books[index]

		if col == 0: return ''
		if col == 1: return self.tbook_['isbn']
		if col == 2: return self.tbook_['titulo']
		if col == 3: return self.tbook_['autor']
		return ''



	def SortItems(self,sorter=cmp):
		items = list(self.itemDataMap.keys())
		items.sort(sorter)
		self.itemIndexMap = items
		# redraw the list
		self.Refresh()

	# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
	def GetListCtrl(self):
		return self

	#
	# Methods that nobody needs but their names expalin more than the method that they call
	#
	
	def cleanpanel(self):
		self.DeleteAllItems() # existing method to clean the panel

	def SetLists(self,books):
		self.books=books

	def OnGetItemImage(self, item):
		index=self.itemIndexMap[item]
		self.estado=self.itemDataMap[index]['estado']
		if not self.estado:
			return self.sm_no
		elif self.estado==1:
			return self.sm_ok
		else:
			return -1

#es la ventana que aparece al hacer click en el boton de buscar en el programa principal
class SearchBook(wx.Frame):
	def __init__(self, parent,books=False):
		wx.Frame.__init__(self, parent = parent,style = wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.CAPTION | wx.MINIMIZE_BOX| wx.CLOSE_BOX)
		self.books = loadbooks()
		self.SetSize((1000, 300))
		self.SetTitle(u'Buscar Libro')
		self.Centre()
		self.Show()
		#self.Maximize()
		self.PanelUI()

	def PanelUI(self):
		self.idn = 0 # el indice de los libros en el arreglo principal
		self.limlist = self.books #este coso define los libros
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self, -1)

		fgs = wx.FlexGridSizer(2, 2, 2, 2)		#row, col, margin, margin
		#campos buscador
		#ckeckbox para ajustar que parametro se busca
		self.ckechboxTitle = wx.CheckBox(panel, label = u"El título contiene:")
		self.ckechboxAutor = wx.CheckBox(panel, label = "El autor contiene:")
		#campos asociados a las checkbox
		self.tcTi          = wx.TextCtrl(panel)
		self.tcAu          = wx.TextCtrl(panel)

		#campos barra intermedia
		self.stinst = wx.StaticText(panel,label = u"Haga doble click para seleccionar el libro.")

		fgs.AddMany([(self.ckechboxTitle), (self.tcTi, 1, wx.EXPAND)])
		fgs.AddMany([(self.ckechboxAutor), (self.tcAu, 1, wx.EXPAND)])

		fgs.AddGrowableCol(1)

		#ventos
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckText)				#All events go to OnCheck, regardless of list
		self.Bind(wx.EVT_TEXT,self.OnCheckText)

		#Panel de busquedas
		self.DinamicPanel = TempSortedListPanelBook(panel)
		vbox.AddMany([(fgs, 0, wx.EXPAND),(self.stinst, 0, wx.ALIGN_CENTER_HORIZONTAL)])
		vbox.Add(self.DinamicPanel, 1, wx.EXPAND)
		panel.SetSizer(vbox)

		#Initialization/Default values, debe ser la lista completa
		#inicializa la checkbox de titulo en true como basico
		self.ckechboxTitle.SetValue(True)
		#arma la primera lista de libtos
		self.ReDoList(self.books)

	def ReDoList(self,books):
		self.DinamicPanel.cleanpanel()
		auxlst       = {}
		self.auxKeys = []

		# Aqui es donde agrego todos los metodos q vienen en el problema
		# Se puede transformat un arreglo en diccionarios a mostrar de forma simple
		# Este es el lugar
		for i in range(0,len(books)):
			auxlst[i] = books[i]
			self.auxKeys.append(i)

		self.DinamicPanel.SetLists(auxlst)
		self.DinamicPanel.itemDataMap  = auxlst
		self.DinamicPanel.itemIndexMap = self.auxKeys
		self.DinamicPanel.SetItemCount(len(books)) #este bichodefine cuantas iteraciones se hacen, debe ser la cantidad de libros q se dan
		#~ items = self.limlist.items()
		#~ for key,se in items:
			#~ index = self.DinamicPanel.InsertStringItem(sys.maxint, se.GetPal())
			#~ self.DinamicPanel.SetItemData(index, key)

	def OnCheckText(self, e):
		partial_autor = False
		partial_title = False

		if self.ckechboxAutor.GetValue():
			partial_autor = str(self.tcAu.GetValue())
			partial_autor = partial_autor.strip()
			if partial_autor=='':
				partial_autor=False
		if self.ckechboxTitle.GetValue():
			partial_title = self.tcTi.GetValue()
			partial_title = partial_title.strip()
			if partial_title=='':
				partial_title = False
		self.ListaFiltrada(partial_autor, partial_title)

	def ListaFiltrada(self,partial_autor,partial_title):
		#si no hay filtros regresa la lista completa
		if(not partial_autor and not partial_title):
			self.ReDoList(self.books)
			return
		new_list = []
		for i in range(0,len(self.books)):
			self.libro_ = self.books[i]
			if (partial_autor and partial_autor.lower() in self.libro_['autor'].lower()):
				new_list.append(self.books[i])
			if (partial_title and partial_title.lower() in self.libro_['titulo'].lower()):
				new_list.append(self.books[i])

		self.ReDoList(new_list)

	def SendIdn(self, book):
		self.GetParent().RecieveIdn(book, 'book')
		self.Close()


if __name__ == '__main__':
	#dummy dictionary to test the method
	ddic1={'id_libro':1,'titulo':'Titulo animal','autor': 'Autor Auto 1','isbn':'123456789','comentarios': 'no hay 1','estado':0}
	ddic2={'id_libro':2,'titulo':'Titulo mueble','autor': 'Autor Casa 2','isbn':'223456789','comentarios': 'no hay 2','estado':1}
	ddic3={'id_libro':3,'titulo':'Titulo pelota','autor': 'Autor mono 2','isbn':'323456789','comentarios': 'no hay 3','estado':1}
	books=[ddic1,ddic2,ddic3]
	ex = wx.App()
	SearchBook(None,books)
	ex.MainLoop()

	#dummy dictionary to test the method
	ddic1={'id_usuario':1,'nombres':'Nombre 1','apellidos': 'Apellido1 ','rut':'123456789','comentarios': 'no hay 1','direccion':'Direccion 1','estado':1, 'telefono':'111-corriente'}
	ddic2={'id_usuario':2,'nombres':'Nombre 2','apellidos': 'Apellido2 ','rut':'223456789','comentarios': 'no hay 2','direccion':'Direccion 2','estado':0, 'telefono':'222-corriente'}
	ddic3={'id_usuario':3,'nombres':'Nombre 3','apellidos': 'Apellido3 ','rut':'323456789','comentarios': 'no hay 3','direccion':'Direccion 3','estado':1, 'telefono':'333-corriente'}
	users=[ddic1,ddic2,ddic3]
	ex = wx.App()
	SearchUser(None,users)
	ex.MainLoop()
