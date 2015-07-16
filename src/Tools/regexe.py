#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

def validar(tipo,valor):
	valor=valor.strip()
	if 'rut' in tipo:
		patron="^\d{6,}-[K|k|0-9]{1}$"
	elif 'name' in tipo.lower():
		patron = "^([A-Z]{1}[a-zñáéíóú]+[\s]*)+$"
	else:
		return False

	if re.match(patron,valor):
		return True
	return False
