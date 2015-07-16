#!/usr/bin/python
# -*- coding: utf-8 -*-

#beginnning routines
#exit routines

from os import system
import cfg
import wx
import mMainWin
import os.path
import codecs
import json

from json import JSONEncoder
from json import JSONDecoder

class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__ 

def from_json_dict(json_object):
		if "name" in json_object:		#user
			aux = cfg.User(json_object["idn"], json_object["status"], json_object["name"])
			aux.SetBooks(json_object["books"])
			return aux
		if "title" in json_object:		#bk
			return cfg.Book(json_object["idn"], json_object["status"], json_object["isbn"], json_object["title"], json_object["author"], json_object["owner"], json_object["cmnt"])
		else: #es uno de los dicts de cfg.*s
			aux = {}
			for key in json_object.keys():
				aux[int(key)] = json_object[key]
			return aux
		
def load_data():
	#loading cfg.bks data:
	if os.path.exists(cfg.dataDir + "bks.dt"):
		inf_bk = codecs.open(cfg.dataDir + "bks.dt", "r", 'utf-8')
		cfg.bks = json.load(inf_bk, object_hook = from_json_dict)
		inf_bk.close()
		cfg.topidb = max(cfg.bks.keys())
	if len(cfg.bks) == 0: 
		cfg.bks[0] = cfg.ept_bk()
		cfg.topidb = 1
	#loading cfg.uss data:
	if os.path.exists(cfg.dataDir + "uss.dt"):
		inf_us = codecs.open(cfg.dataDir + "uss.dt", "r", 'utf-8')
		cfg.uss = json.load(inf_us, object_hook = from_json_dict)
		inf_us.close()
		cfg.topidu = max(cfg.uss.keys())
	#Even if there isn't anything officially, Bilbio is user cero
	if len(cfg.uss) == 0: 
		cfg.uss[1] = cfg.User(1, 1, "Biblioteca")
		cfg.topidu = 2
#Ends load_data

def end_save():
	ouf_bk = codecs.open(cfg.dataDir+"bks.dt","w", 'utf-8')
	json.dump(cfg.bks, ouf_bk, ensure_ascii = False, cls = MyEncoder, encoding='utf-8')
	ouf_bk.close()
	ouf_us = codecs.open(cfg.dataDir+"uss.dt","w", 'utf-8')
	json.dump(cfg.uss, ouf_us, ensure_ascii = False, cls = MyEncoder, encoding='utf-8')
	ouf_us.close()
	cfg.topidu = max(cfg.uss.keys())

#Ends end_save()

def end():
	end_save()
	exit()

if __name__ == '__main__':
	load_data()
	app = wx.App()
	mMainWin.MainWin(None)
	app.MainLoop()
	
	
#Non-JSON version
#~ #topid
#~ def extract_topid():  
	#~ auxf = codecs.open(cfg.dataDir + cfg.topidfn,"r","utf-8")
	#~ cfg.topidb = int(auxf.readline())
	#~ cfg.topidu = int(auxf.readline())
	#~ auxf.close()
#~ 
#~ def update_topid():
	#~ auxf = codecs.open(cfg.dataDir+cfg.topidfn,"w","utf-8")
	#~ auxf.write(str(cfg.topidb) + "\n")
	#~ auxf.write(str(cfg.topidu) + "\n")
	#~ auxf.close()
