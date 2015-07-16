#!/usr/bin/python
# -*- coding: utf-8 -*

import time

def today():
	dt = [0,2]
	dt[0] = time.strftime('%d', time.localtime())
	dt[1] = time.strftime('%m', time.localtime())
	return dt

def printa():
	td = today()
	print td


printa()
