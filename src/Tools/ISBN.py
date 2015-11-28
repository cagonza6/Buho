# -*- coding: utf-8 -*-
from isbnlib import clean as isbnclean
from isbnlib import is_isbn10, is_isbn13, to_isbn13, canonical, mask
import config.GlobalConstants as Constants


def isISBN(isbnlike):
	isbnlike = clean(isbnlike)
	if is_isbn10(isbnlike):
		return mask(canonical(isbnlike), separator='-')
	if is_isbn13(isbnlike):
		return mask(canonical(isbnlike), separator='-')
	return False


def formated(isbnlike):
	isbnClean = isISBN(clean(isbnlike))
	if not isbnClean:
		return isbnlike
	return mask(canonical(isbnClean), separator='-')


def clean(isbnlike):
	return isbnclean(str(isbnlike))


def isbn10(isbnlike):
	isbnlike = clean(isbnlike)
	if is_isbn10(isbnlike):
		return canonical(isbnlike)
	return Constants.NULL


def isbn13(isbnlike):
	isbnlike = clean(isbnlike)
	if isbn10(isbnlike):
		isbnlike = to_isbn13(isbnlike)
	if is_isbn13(isbnlike):
		return canonical(isbnlike)
	return Constants.NULL
