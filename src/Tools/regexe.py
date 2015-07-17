#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

def validar_nombre(texto,patron="^([A-Z]{0,1}[a-zñáéíóú]+[\s]*)+$"):
	patron = re.compile(patron)
	texto  = texto.strip()
	#texto=texto.title()
	if texto == '':
		print "\t X"
		return False
	if 'nombre' in texto.lower():
		print "\t X"
		return False
	if 'apellido' in texto.lower():
		print "\t X"
		return False

	if patron.match(texto):
		return texto
	return False

def validar_rut(texto,patron="^\d{6,}-[K|k|0-9]{1}$"):
	patron = re.compile(patron)
	texto  = texto.strip()

	if patron.match(texto):
		return True

	return False

def validar(tipo,valor):
	tipo=tipo.strip()
	valor=valor.strip()
	if 'rut' in tipo:
		patron="^\d{6,}-[K|k|0-9]{1}$"
		return validar_rut(valor,patron)
	elif 'name' in tipo.lower():
		patron = "^([A-Z]{0,1}[a-zñáéíóú]+[\s]*)+$"
		return validar_nombre(valor,patron)

	return False


if __name__ == '__main__':

	validar('name','Naño')
	validar('name','Nano')
	validar('name','Pancho')
	validar('name','Juan Psr ico')
	print validar('rut','111a1111-7')
	print validar('rut','7-7')
	print validar('rut','7999877-7')

