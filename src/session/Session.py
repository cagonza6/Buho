# -*- coding: utf-8 -*-

ROLES_INFO = False  # Session.ROLES_INFO
FORMAT_TYPE_INFO = False  # Session.FORMAT_TYPE_INFO
LANGUAGES_INFO = False  # Session.LANGUAGES_INFO
GRADES_INFO = False  # Session.GRADES_INFO

def roleNeedsGrade(role_):
	for role in ROLES_INFO:
		if role['roleID'] == role_:
			if role['roleHasGrade']:
				return True
	return False
