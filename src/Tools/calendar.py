#!/usr/bin/python
# -*- coding: utf-8 -*-

#funciones de tiempo
import datetime


def date2int(date):
	return int(str(date).replace('-',''))

def isweekend(date):
	if date.isoweekday() in range(1, 6):
		return False
	return True

if __name__ == '__main__':
	date='2015-12-31'
	print date2string(date)+1
