#!/usr/bin/python
# -*- coding: utf-8 -*-
import re


def cleanKeywords(keys):
	keys = keys.strip()
	keys = re.sub("([ \t]){1,}", " ", keys)
	keys = keys.split(' ')
	pars = []
	for i in range(0, len(keys)):
		if len(keys[i]) < 3:
			continue
		pars.append(keys[i])
	return pars


if __name__ == '__main__':
	print "regexe methods"
