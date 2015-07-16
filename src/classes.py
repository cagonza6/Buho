#!/usr/bin/python
# -*- coding: utf-8 -*

'''
Clase Usuario
@idn   : Id unica de usuario, se obtiene al registrarlo en la base de datos
@status: ?
@name  : nombre del usuario en cuestion
'''
class User:
	def __init__(self, idn, status, name):
		self.idn = idn
		self.name = name
		self.books = []					#Libros que tiene prestados, incluyendo fecha de entrega
		self.status = status				#0 = eliminado, 1 = old, 2 = new,3 = modificado

	def GetIdn(self):    return self.idn
	def GetStatus(self): return self.status
	def GetName(self):   return self.name
	def GetBooks(self):  return self.books

	def SetIdn(self, aux):    self.idn   = aux
	def SetStatus(self, aux): self.nobor = aux
	def SetName(self, aux):   self.name  = aux
	def SetBooks(self, aux):  self.books = aux
	
	def BorrowBook(self, bk_id, returndate):
		self.books.append([bk_id, returndate])

	def ReturnBook(self, bk_id):
		i = 0
		while (i<len(self.books)):		#No creo que se de tener la media lista...
			if bk_id == self.books[i][0]:
				print bk_id, self.books[i][0]
				self.books.pop(i)
				bks[bk_id].Return()
				i = i - 1 				#has to do with the check condition at the end
				break
			i = i +1 
		if (i != len(self.books)):
			return 1			#todo bien (remember, I popped sth out, so new length 
		else:
			return -1								#El libro no era de este usuario
		#Maybe there should be some check para marcar si lo devolvió fuera de plazo?

	def LateBook(self):
		aux = ""
		for bk in self.books:
			if is_late(bk[1]):
				aux = aux + "\n " + bks[bk[0]].GetTitle()
		return aux

'''
Clase Libro
@idn    : Id unica de libro, se obtiene al registrarlo. Libros de mismo titulo tendran diferente ID
@status : ?
@titulo : Titulo del libro
@author : Autor
@owner  : quien pose el libro de momento. (arrendador)
@cmnt   : Comentarios del libro.
'''
class Book:
	def __init__(self, idn, status, isbn, title, author, owner, cmnt):
		self.idn    = idn
		self.isbn   = isbn				#texto. Debe ser texto, hay una X como la K del rut
		self.title  = title
		self.author = author			#au string name, for now
		self.cmnt   = cmnt				#could have carriage return
		self.owner  = owner				#idn_own #it's for whoever has it at the time. Biblioteca will be the main owner
		self.status = status			#0 = eliminado, 1 = old, 2 = new,3 = modificado

	def GetIdn(self):    return self.idn
	def GetIsbn(self):   return self.isbn
	def GetStatus(self): return self.status
	def GetTitle(self):  return self.title
	def GetAuthor(self): return self.author
	def GetCmnt(self):   return self.cmnt
	def GetOwner(self):  return self.owner
	
	def SetIdn(self, aux):    self.idn    = aux
	def SetIsbn(self, aux):   self.isbn   = aux
	def SetStatus(self, aux): self.status = aux
	def SetAuthor(self, aux): self.author = aux
	def SetTitle(self, aux):  self.title  = aux
	def SetCmnt(self, aux):   self.cmnt   = aux
	def SetOwner(self, aux):  self.owner  = aux
	
	def IsLoaned(self):
		if self.GetOwner() == 1: return False			#1 es Biblioteca
		else: return True
		
	def Return(self):
		self.SetOwner(1)
		#I'm quite sure this will change in time, so it goes here. So I only have to change one place

if __name__ == '__main__':
	print "Classes OK!"
