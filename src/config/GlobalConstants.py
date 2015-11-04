# -*- coding: utf-8 -*-

# ######## General #################
NULL = ''

# ######## GENERAL STATUS ##########
STATUS_INVALID = 0
STATUS_VALID   = 1
STATUS_WARNING = 2


# ######## Items Constants #########
AVAILABLE_ITEMS = 0
LOANED_ITEMS    = 1
ALL_ITEMS       = 2
DUED_ITEMS      = 3

# ######## Items Constants #########
BLOCKED_USERS   = 0
AVAILABLE_USERS = 1
BANED_USER      = 2
ALL_USERS       = 3

# ###### Stuff type definition ######
TYPE_ITEM = 1
TYPE_USER = 2
TYPE_LOAN = 3

# ######## DataBase ################
ITEM_BOOK  = 'BK'
ITEM_MUSIC = 'MU'

# ######## DB fields #######
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

# ######## Icons ####################
ICON_VALID   = ":/status/resources/pixmap/icons/status/status-ok.png"
ICON_INVALID = ":/status/resources/pixmap/icons/status/status-no.png"
ICON_WARNING = ":/status/resources/pixmap/icons/status/status-warning.png"


# ####### Loan constants ##############
LOAN_SPAN         = 14
RENEWAL_LIMIT     = 2
ST_MAX_LOANS      = 3

##################################
###### Developers Only ###########
##################################

###### Table Names ###############
# Note: keep your hands out of here

TABLE_USERS = 'users'
TABLE_ITEMS = 'items'
TABLE_fORMATS = 'item_formats'
TABLE_LOANS = 'loans'
TABLE_HISTORY = 'history'

