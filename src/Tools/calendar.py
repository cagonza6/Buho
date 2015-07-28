#!/usr/bin/python
# -*- coding: utf-8 -*-

# Time and date Functions
import datetime

def date2int(date):
	return int(str(date).replace('-',''))

def isweekend(date):
	if date.isoweekday() in range(1, 6):
		return False
	return True

def int2date(intdate):
	strdate = str(intdate)
	return datetime.datetime.strptime(strdate,'%Y%m%d').date()

def daysbetween(from_,to_):
	diff = to_-from_
	return diff.days

def date2DMY(date):
	date_s = str(date).split('-')
	dmy=[int(date_s[2]),int(date_s[1])-1,int(date_s[0])]
	return dmy

def oneDay():
	return datetime.timedelta(1)

if __name__ == '__main__':
	date='2015-12-31'
	print date2string(date)+1
