# -*- coding: utf-8 -*-
import re

import session.Session as Session
import config.GlobalConstants as Constants
from Tools import validations

def cleanKeywords(keys, isID):
	keys = keys.strip()
	keys = re.sub("([ \t]){1,}", " ", keys)
	keys = keys.split(' ')
	pars = []
	for i in range(0, len(keys)):
		key = keys[i].strip()
		if len(key) < 3:
			continue
		if isID == Constants.IDS:
			key = str(cleanPrefix(key))
			if not key:
				continue
		pars.append(key)
	return pars

def cleanPrefix(key0):
	key, aux = validations.validate(Constants.IDS, key0, Session.FORMAT_TYPE_INFO)
	if key:
		return key
	key, aux = validations.validate(Constants.IDS, key0, Session.ROLES_INFO)
	if key:
		return key
	return False


if __name__ == '__main__':
	print "regexe methods"
