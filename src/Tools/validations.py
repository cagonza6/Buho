# -*- coding: utf-8 -*-
import re
from datetime import date

from isbnlib import clean as isbnclean, is_isbn10, is_isbn13, to_isbn13, canonical, mask

import config.GlobalConstants as Constants


# Removes breacklines and empty spaces at the end and begining of the string
def validate_title(title):
	title = unicode(title.strip())
	if title != '':
		return title.title()
	return False


def validate_author(author):
	author = author.strip()
	if author != '':
		return author.title()
	return False


def validate_comments(comments):
	comments = comments.strip()
	return comments


def validate_isbn(isbnlike):
	isbnlike = isbnclean(isbnlike)
	if is_isbn10(isbnlike):
		return mask(canonical(isbnlike), separator='-')
	if is_isbn13(isbnlike):
		return mask(canonical(isbnlike), separator='-')
	return False


def validate_year(year):
	if int(year) <= int(date.today().year):
		return year
	return False


def validate_IDs(idstr, regex, IDlist=False):

	if not IDlist or not re.match(regex, idstr):
		return False, False

	aux = re.findall(regex, idstr)[0]

	if len(aux) > 1:
		role = str(aux[0])
		id_ = int(aux[1])
		if role in str(IDlist) and id_:
			return id_, role

	return False, False


def validate_name(name, regex):
	name = name.strip()

	if name == '':
		return False
	if 'nombre' in name.lower() or 'name' in name.lower():
		return False
	if 'apellido' in name.lower() or 'familyname' in name.lower():
		return False

	name = name.title()
	return name


def validate_idn(idn, regex):
	idn = str(idn).strip()
	regex = re.compile(regex)
	if regex.match(idn):
		return idn
	return False


def validate_cellphone(phone, regex):
	phone = str(phone).strip()
	regex = re.compile(regex)
	if regex.match(phone):
		return phone
	return False


def validate_email(email, regex):
	email = str(email.strip())
	regex = re.compile(regex)

	if regex.match(email):
		return email
	return False


def validate(field, value, var1=False):
	if Constants.ISBN == field:
		return validate_isbn(value)
	elif Constants.IDN == field:
		regex = "^\d{6,}-[K|k|0-9]{1}$"
		return validate_idn(value, regex)
	elif Constants.NAME == field:
		regex = "^([A-Z]{0,1}[a-zÑÁñáÉéÍíÓóÚú]+[\s]*)+$"
		return validate_name(value, regex)
	elif Constants.TITLE == field:
		return validate_title(value)
	elif Constants.COMMENTS == field:
		return validate_comments(value)
	elif Constants.AUTHOR == field or Constants.PUBLISHER == field:
		return validate_author(value)
	elif Constants.EMAIL == field:
		regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		return validate_email(value, regex)
	elif Constants.YEAR == field:
		return validate_year(value)
	elif Constants.CELPHONE == field:
		regex = "^0{0,1}[6|7|8|9][0-9]{7}$"
		return validate_cellphone(value, regex)
	elif Constants.PHONE == field:
		regex = "^([0-9]{5,8})$"
		return validate_cellphone(value, regex)
	elif Constants.IDS == field:
		regex = "^([\w^\d]{2})(\d{5,})$"
		return validate_IDs(value, regex, var1)

	return False


def cleanKeywords(keys):
	keys = keys.strip()
	keys = re.sub("([ \t]){1, }", " ", keys)
	keys = keys.split(' ')
	pars = []
	for i in range(0, len(keys)):
		if len(keys[i]) < 3:
			continue
		pars.append(keys[i])
	return pars


if __name__ == '__main__':
	print "validations for different data types"
	print validate(Constants.NAME, 'ñaño')
	print validate(Constants.IDN, '111a1111-7')
	print validate(Constants.ISBN, '978-1-4454-9331-2')
	print validate(Constants.EMAIL, 'lala@lala.com')
