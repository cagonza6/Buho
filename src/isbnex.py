#!/usr/bin/python
# -*- coding: utf-8 -*-

import isbnlib as ilb

isbn13 = "978-958-041-013-3"
isbn10 = "9507398899"
unregistered = "9789567705139"

#~ if ilb.is_isbn10(isbn10): print "Funca"
#~ else: print "no funca"
#~ 
#~ if ilb.is_isbn13(isbn13): print "Funca"
#~ else: print "no funca"

print ilb.meta(isbn10)


