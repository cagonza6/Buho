#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
#!/usr/bin/env python
from  isbnlib import clean as isbnclean,is_isbn10,is_isbn13,canonical



def validar_comentario(comentario):
	comentario = comentario.strip()
	if comentario == '' :
		return "Sin comentarios"
	return False

def validar_autor(autor):
	autor = autor.strip()
	if autor != '':
		return autor.title()
	return False

def validar_titulo(titulo):
	titulo = titulo.strip()
	if titulo != '':
		return titulo.title()
	return False

def validar_isbn(isbnlike):

	isbn = isbnclean(isbnlike)
	if is_isbn10(isbnlike):
		isbn = to_isbn13(isbnlike)
	elif is_isbn13(isbnlike):
		return canonical(isbnlike)
	return False

def validar_nombre(texto,patron="^([A-Z]{0,1}[a-zñáéíóú]+[\s]*)+$"):
	patron = re.compile(patron)
	texto  = texto.strip()
	#texto=texto.title()
	if texto == '':
		return False
	if 'nombre' in texto.lower():
		return False
	if 'apellido' in texto.lower():
		return False

	if patron.match(texto):
		return texto
	return False

def validar_rut(rut,patron="^\d{6,}-[K|k|0-9]{1}$"):
	rut  = str(rut.strip())
	patron = re.compile(patron)

	if patron.match(rut):
		return rut

	return False

def validar(tipo,valor):
	tipo=tipo.strip()
	valor=valor.strip()
	if 'isbn' in tipo:
		return validar_isbn(valor)
	elif 'rut' in tipo:
		patron="^\d{6,}-[K|k|0-9]{1}$"
		return validar_rut(valor,patron)
	elif 'name' in tipo.lower():
		patron = "^([A-Z]{0,1}[a-zñáéíóú]+[\s]*)+$"
		return validar_nombre(valor,patron)
	elif 'titulo' in tipo.lower():
		return validar_titulo(valor)
	elif 'comentario' in tipo.lower():
		return validar_comentario(valor)
	elif 'autor' in tipo.lower():
		return validar_autor(valor)

	return False

if __name__ == '__main__':

	print validar('name','Naño')
	print validar('name','Pancho')
	print validar('name','Juan Psr ico')
	print validar('rut','111a1111-7')
	print validar('rut','7-7')
	print validar('rut','7999877-7')
	print "\n ISBN \n"
	print "1) real "
	print validar('isbn','978-1-4454-9331-2')
	print validar('isbn','9781445493312')
	print "2) missing last digit "
	print validar('isbn','978-1-4454-9331')
	print "3) flase last digit "
	print validar('isbn','978-1-4454-9331-1') # digito verificador cambiado
	print "4) no dash"
	print validar('isbn','9781445493312') # digito verificador cambiado

