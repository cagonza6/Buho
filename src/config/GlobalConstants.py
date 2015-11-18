# -*- coding: utf-8 -*-

# ######## General ################
NULL = ''
EMPTY = ' '

# ######## GENERAL STATUS #########
STATUS_INVALID = 0
STATUS_VALID   = 1
STATUS_WARNING = 2


# ######## Items Constants ########
AVAILABLE_ITEMS = 0
LOANED_ITEMS    = 1
ALL_ITEMS       = 2
DUED_ITEMS      = 3

# ######## Items Constants ########
BLOCKED_USERS   = 0
AVAILABLE_USERS = 1
BANED_USER      = 2
ALL_USERS       = 3

# ##### Stuff type definition #####
TYPE_FLAG = 0
TYPE_ITEM = 1
TYPE_USER = 2
TYPE_LOAN = 3

# ######## DataBase ###############
ITEM_BOOK  = 'BK'
ITEM_MUSIC = 'MU'

# ############ DB fields ##########
# Enumerations used mostly to in validations and DB saving processes

TITLE     = 1
AUTHOR    = 2
PUBLISHER = 3
YEAR      = 4
ISBN      = 5
NAME      = 6
IDN       = 7
IDS       = 8
EMAIL     = 9
PHONE     = 10
CELPHONE  = 11
COMMENTS  = 12

# ######## Icons ##################
ICON_VALID = ":/status/resources/pixmap/icons/status/status-ok.png"
ICON_INVALID = ":/status/resources/pixmap/icons/status/status-no.png"
ICON_WARNING = ":/status/resources/pixmap/icons/status/status-warning.png"
ICON_UNAVAILABLE = ":/status/resources/pixmap/icons/status/status-unavailable.png"


# ####### Loan constants ##########
LOAN_SPAN     = 14
RENEWAL_LIMIT = 2
ST_MAX_LOANS  = 3

# ####### Paper orientation #######
PAPER_PORTAIL = 0
PAPER_LANDSCAPE = 1

# #### Column width for reports ###

WIDTH_NUM = 14
WIDTH_ID = 25
WIDTH_NAME = 42
WIDTH_GRADE = 15
WIDTH_DATE = 25
WIDTH_DELAY = 21
WIDTH_OTHER = 21


# #################################
# ##### Developers Only ###########
# #################################

# ##### Table Names ###############
# Note: keep your hands out of here

TABLE_USERS = 'users'
TABLE_ITEMS = 'items'
TABLE_fORMATS = 'item_formats'
TABLE_LOANS = 'loans'
TABLE_HISTORY = 'history'


# #################################
'''
Actinos to take to transit fro window to window sometimes.
At the moment just used in HomePage to call other windows in MainWindow.
'''


#Note:  Never use 0 here
ACTION_RETURN_ITEM = 1
ACTION_EDIT_LOAN = 2

