# -*- coding: utf-8 -*-
import datetime


def todaysDate():
	today = datetime.date.today().isoformat()
	todaysDate = date2int(today)
	return todaysDate


def date2int(date):
	return int(str(date).replace('-', ''))


def isweekend(date):
	if date.isoweekday() in range(1, 6):
		return False
	return True


def int2date(intdate):
	strdate = str(intdate)
	if len(strdate)<8:
		return 0
	return datetime.datetime.strptime(strdate, '%Y%m%d').date()


def daysbetween(from_, to_):
	diff = to_ - from_
	return diff.days


def date2DMY(date):
	date_s = str(date).split('-')
	dmy = [int(date_s[2]), int(date_s[1]) - 1, int(date_s[0])]
	return dmy


def addDays(days=1):
	return datetime.timedelta(days)


def searchNoWeekend(duedate):
	while isweekend(duedate):
		duedate += addDays(1)
	return duedate


if __name__ == '__main__':
	pass
