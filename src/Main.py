#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import mMainWin


if __name__ == '__main__':
	app = wx.App()
	mMainWin.MainWin(None)
	app.MainLoop()
