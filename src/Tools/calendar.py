#!/usr/bin/python
# -*- coding: utf-8 -*-

def date2int(date):
	return int(str(date).replace('-',''))

def ishollyday(date):
	return False
if __name__ == '__main__':
	date='2015-12-31'
	print date2string(date)+1
