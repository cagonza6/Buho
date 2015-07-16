#!/usr/bin/python
# -*- coding: utf-8 -*-

#beginnning routines
#exit routines

#metodos y paquetes del system
import cfg
from classes import *

from os import system
import os.path
import wx
import mMainWin
import codecs
import json
from json import JSONEncoder
from json import JSONDecoder




class MyEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__ 

def from_json_dict(json_object):
		if "name" in json_object:		#user
			aux = User(json_object["idn"], json_object["status"], json_object["name"])
			aux.SetBooks(json_object["books"])
			return aux
		if "title" in json_object:		#bk
			return Book(json_object["idn"], json_object["status"], json_object["isbn"], json_object["title"], json_object["author"], json_object["owner"], json_object["cmnt"])
		else: #es uno de los dicts de cfg.*s
			aux = {}
			for key in json_object.keys():
				aux[int(key)] = json_object[key]
			return aux

def load_data():
	#loading cfg.bks data:
	bookspath=cfg.dataDir+"bks.dt"
	if os.path.exists(bookspath):
		print "Loading File: ["+bookspath+"]"
		inf_bk = codecs.open(cfg.dataDir + "bks.dt", "r", 'utf-8')
		cfg.bks = json.load(inf_bk, object_hook = from_json_dict)
		inf_bk.close()
		cfg.topidb = max(cfg.bks.keys())
	else:
		print "Debug: File not Found ["+bookspath+"]"
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
	bookspath=cfg.dataDir+"bks.dt"
	print "Tratando de guardar ["+bookspath+"]"
	ouf_bk = codecs.open(bookspath,"w", 'utf-8')
	json.dump(cfg.bks, ouf_bk, ensure_ascii = False, cls = MyEncoder, encoding='utf-8')
	ouf_bk.close()
	userspath=cfg.dataDir+"uss.dt"
	ouf_us = codecs.open(userspath,"w", 'utf-8')
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
