#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
#!/usr/bin/env python
from  isbnlib import clean as isbnclean,is_isbn10,is_isbn13,canonical



def validate_comments(comments):
	comments = comments.strip()
	if comments == '' :
		return "Sin commentss"
	return False

def validate_author(author):
	author = author.strip()
	if author != '':
		return author.title()
	return False

def validate_title(title):
	title = title.strip()
	if title != '':
		return title.title()
	return False

def validate_isbn(isbnlike):

	isbnlike = isbnclean(isbnlike)
	if is_isbn10(isbnlike):
		isbnlike = to_isbn13(isbnlike)
	if is_isbn13(isbnlike):
		return canonical(isbnlike)
	return False

def validate_name(texto,regex):
	texto  = texto.strip()

	if texto == '':
		return False
	if 'name' in texto.lower():
		return False
	if 'apellido' in texto.lower():
		return False

	texto=texto.title()
	return texto


def validate_rut(rut,regex="^\d{6,}-[K|k|0-9]{1}$"):
	rut  = str(rut.strip())
	regex = re.compile(regex)

	if regex.match(rut):
		return rut

	return False

def validate_email(email,regex="^\d{6,}-[K|k|0-9]{1}$"):
	email  = str(email.strip())
	regex = re.compile(regex)

	if regex.match(email):
		return email
		print email
	return False


def validate(tipo,valor):
	tipo=tipo.strip()
	valor=valor.strip()
	if 'isbn' in tipo:
		return validate_isbn(valor)
	elif 'rut' in tipo:
		regex="^\d{6,}-[K|k|0-9]{1}$"
		return validate_rut(valor,regex)
	elif 'name' in tipo.lower():
		regex = "^([A-Z]{0,1}[a-zÑÁñáÉéÍíÓóÚú]+[\s]*)+$"
		return validate_name(valor,regex)
	elif 'title' in tipo.lower():
		return validate_title(valor)
	elif 'comments' in tipo.lower():
		return validate_comments(valor)
	elif 'author' in tipo.lower():
		return validate_author(valor)
	elif 'email' in tipo.lower():
		regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		return validate_email(valor,regex)

	return False

if __name__ == '__main__':

	print validate('name','ñaño')
	print validate('name','Pancho')
	print validate('name','Juan Psr ico')
	print validate('rut','111a1111-7')
	print validate('rut','7-7')
	print validate('rut','7999877-7')
	print "\n ISBN \n"
	print "1) real "
	print validate('isbn','978-1-4454-9331-2')
	print validate('isbn','9781445493312')
	print "2) missing last digit "
	print validate('isbn','978-1-4454-9331')
	print "3) flase last digit "
	print validate('isbn','978-1-4454-9331-1') # digito verificador cambiado
	print "4) no dash"
	print validate('isbn','9781445493312') # digito verificador cambiado
	print validate('email','lala@lala.com') # digito verificador cambiado
	print validate('email','lala@la@la.com') # digito verificador cambiado
	print validate('email','lala@l.a.l.a.c') # digito verificador cambiado
	print validate('email','l.a.l.a@lala.') # digito verificador cambiado
