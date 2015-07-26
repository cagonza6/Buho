#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys # detect SO
from os import system
import os.path

lockwin = False

                #########
                # Paths #
                #########
# It should be not mportant where the app is executed, then we use relative
# paths, it should wok on windows too.

homeDir = os.getcwd()                  # Automatically generated acoording where the script is running from
DataDir = '/Data/'                     # Name of the folder where the data is located
                                       # txt only
dataDir  = homeDir + DataDir           # folder with the txt information

sqdbPath = homeDir+'/database/Main.db' #path to the database SQlite
#???
topidfn  = "topid.dat"                 # 

                ###########
                # Configs #
                ###########
reqRut = False                         #if True, RUT es necesario para registrar un usuario
