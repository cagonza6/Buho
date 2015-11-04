# -*- coding: utf-8 -*-

def formatID(category, id_number):
	idStr = str(id_number)
	pref = ''
	for i in range(len(idStr), 5):
		pref += str('0')
	return category + pref + idStr
