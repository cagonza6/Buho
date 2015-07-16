#!/usr/bin/python
# -*- coding: utf-8 -*

import json
import cfg
import Main
import codecs

from json import JSONEncoder
from json import JSONDecoder

class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__ 

def from_json_dict(json_object):
		if "name" in json_object:
			return cfg.User(json_object["idn"], json_object["status"], json_object["name"])
		if "title" in json_object:
			return cfg.Book(json_object["idn"], json_object["status"], json_object["title"], json_object["author"], json_object["owner"], json_object["cmnt"])
		else: 
			aux = {}
			for key in json_object.keys():
				aux[int(key)] = json_object[key]
			return aux
		
def from_json_us(json_object):
	return cfg.User(json_object["idn"], json_object["status"], json_object["name"])

def from_json_bk(json_object):
		return cfg.Book(json_object["idn"], json_object["status"], json_object["title"], json_object["author"], json_object["owner"], json_object["cmnt"])

op = "us"
if op == "bks":
	#~ #input
	#Main.begin_save()
	#~ ouf = codecs.open("try2.txt","w", 'utf-8')
	#~ json.dump(cfg.bks, ouf, ensure_ascii = False, cls = MyEncoder, encoding='utf-8')
	#~ #ouf = codecs.open("try2.txt","w", 'utf-8')
	#~ #ouf.write(aux)
	#~ ouf.close()
	#~ print cfg.ext
	#~ 
	#~ #output
	inf = codecs.open("try2.txt","r","utf-8")
	aux2 = json.load(inf, object_hook = from_json_dict)
	print aux2[3].GetTitle()
	inf.close()

else: 
	#~ #input
	#Main.begin_save()
	ouf = codecs.open("try.txt","w", 'utf-8')
	json.dump(cfg.uss, ouf, ensure_ascii = False, cls = MyEncoder, encoding='utf-8')
	ouf.close()
	#~ 
	#output
	inf = codecs.open("try.txt","r","utf-8")
	aux2 = json.load(inf, object_hook = from_json_dict)
	inf.close()
