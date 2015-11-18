#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

import config.GlobalConstants as Constants
from Tools.timeFunctions import todaysDate


def query2dic(cursor, row):
	dictionary = {}
	for idx, col in enumerate(cursor.description):
		dictionary[col[0]] = row[idx]
	return dictionary


# source: http://stackoverflow.com/questions/4610791/can-i-put-my-sqlite-connection-and-cursor-in-a-function
class DatabaseManager(object):
	def __init__(self, db="database/Main.db"):
		self.conn = sqlite3.connect(db)
		self.conn.row_factory = query2dic
		self.cur = self.conn.cursor()

	def close(self):
		self.__del__()

	def __del__(self):
		self.conn.close()

	def saveToLog(self, error):
		with open('sqliteLog.txt', 'a') as file:
			file.write(error + '\n')

	###################
	# General methods #
	###################
	def load_categories(self):
		query = "SELECT "
		query += "        formatID,  formatName,  formatNameShort "
		query += "FROM item_formats "
		query += "ORDER BY formatID "

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("load_categories:" + str(e))
			return False

		Result = self.cur.fetchall()
		return Result

	def load_languages(self):
		query = "SELECT "
		query += "        langIsoID,  Part2B,  Part2T,  Part1,  Ref_Name "
		query += "FROM languages "
		query += "ORDER BY langIsoID "

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("load_languages:" + str(e))
			return False

		Result = self.cur.fetchall()
		return Result

	def load_roles(self):
		query = "SELECT "
		query += "        roleID,  roleName, roleHasGrade "
		query += "FROM roles "
		query += "ORDER BY roleID "

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("load_roles:" + str(e))
			return False

		Result = self.cur.fetchall()
		return Result

	def load_grades(self):
		query = "SELECT "
		query += "        gradeID,  gradeName "
		query += "FROM grades "
		query += "ORDER BY gradeID "

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("load_grades:" + str(e))
			return False

		Result = self.cur.fetchall()
		return Result

	#########################
	# Items - Users Methods #
	#########################

# creation and modifications
	def save_new(self, type_, data_):
		if type_ == Constants.TYPE_ITEM:
			query = "INSERT INTO items ( format,  ISBN,  title,  author,  publisher,  year,  lang,  location, comments) "
			query += "VALUES           (   ?   ,   ?  ,    ?  ,    ?   ,     ?     ,    ? ,    ? ,     ?    ,    ?    );"
		elif type_ == Constants.TYPE_USER:
			query = "INSERT INTO users (  role,  name,  familyname,  IDN,  email,  address,  phone,  cellphone,  grade,  comments ) "
			query += "VALUES           (   ?  ,  ?  ,      ?     ,   ? ,    ?  ,    ?    ,    ?  ,    ?       ,   ?  ,      ?     );"
		else:
			return False

		error = False
		try:
			self.cur.execute(query, data_)
		except sqlite3.Error as e:
			self.saveToLog("save_new:" + str(e))
			error = True
			return False
		if not error:
			self.conn.commit()
		return True

	def edit_itemUser(self, type_, data_):
		if type_ == Constants.TYPE_ITEM:
			query = "UPDATE items SET format = ?,  ISBN = ? ,  title = ?,  author = ?,  publisher = ?,  year = ?,  lang = ?,  location = ?, comments = ? WHERE itemID = ?"

		elif type_ == Constants.TYPE_USER:
			query = "UPDATE users SET role = ?,  name = ?,  familyname = ?,  IDN = ?,  email = ?,  address = ?,  phone = ?,  cellphone = ?,  grade = ?,  comments = ? WHERE userID = ?"
		else:
			return False

		error = False
		try:
			self.cur.execute(query, data_)
		except sqlite3.Error as e:
			self.saveToLog("edit_itemUser:" + str(e))
			error = True
			return False
		if not error:
			self.conn.commit()
		return True

# search

	def search_users(self, sStatus, column_type, keys, role, grade):
		querrydata = []
		query = "SELECT "
		query += "      users.userID,  users.role,  users.name,  users.familyname,  users.IDN,"
		query += "      users.email,  users.address,  users.phone,  users.cellphone,  users.comments, "
		query += " users.IDN,  users.password,  users.status,  "
		query += "      grades.gradeName,  "
		query += "      roles.roleName,  roles.roleName,  "
		query += "      count(loans.userID) AS loans "
		query += "FROM users "
		query += "INNER JOIN grades ON users.grade = grades.gradeID "
		query += "INNER JOIN roles  ON users.role  = roles.roleID "
		query += "LEFT  JOIN loans  ON users.userID = loans.userID "
		query += "WHERE "

		if sStatus == Constants.ALL_USERS:
			query += "users.status >= 0 "
		if sStatus == Constants.BLOCKED_USERS:
			query += "users.status = 0 "
		if sStatus == Constants.AVAILABLE_USERS:
			query += "users.status > 0 "
		if sStatus == Constants.BANED_USER:
			query += "users.status = 2 "

		if role:
			role = str(role)
		else:
			role = '%'
		query += "AND users.role LIKE ? "
		querrydata.append(role)

		if grade:
			grade = int(grade)
			query += "AND users.grade = ? "
			querrydata.append(grade)
		column = 'name'  # default
		if column_type == Constants.NAME:
			column = 'name'
		if column_type == Constants.EMAIL:
			column = 'email'
		elif column_type == Constants.IDS:
			column = 'userID'

		if column_type == Constants.IDS:
			if len(keys):
				query += 'AND users.userID = ? '
				querrydata.append(keys[0])
		if len(keys):
			key = keys[0].lower()
			if column_type == Constants.NAME:
				query += "AND (instr(lower(users.name),  ? ) OR instr(lower(users.familyname),  ? ) ) "
				querrydata.append(key)
				querrydata.append(key)
				if len(keys) > 1:
					for i in range(1, len(keys)):
						key = keys[i].lower()
					query += "OR (instr(lower(users.name),  ? ) OR instr(lower(users.familyname),  ? ) ) "
					querrydata.append(key)
					querrydata.append(key)

			if column_type == Constants.EMAIL:
				for key in keys:
					query += "AND (users.email = ?) "
					querrydata.append(key.lower())

		query += "GROUP BY users.userID;"
		try:
			self.cur.execute(query, querrydata)
		except sqlite3.Error as e:
			self.saveToLog("search_users: " + str(e))
			return False
		Result = self.cur.fetchall()
		return Result

	def searchItemsFilters(self, sStatus, column_type, keys, format_):
		query = ''
		querrydata = []
		'''
		The validarion for id>0 is equivalent to search all the items,
		this one comes by default from the orginal method and is used to
		make the the methods searchItems() and duedItems() compatible

		if sStatus == Constants.ALL_ITEMS:
			query += "AND items.itemID >0 "
		'''
		if sStatus == Constants.AVAILABLE_ITEMS:
			query += "AND loans.itemID is NULL "
		elif sStatus == Constants.LOANED_ITEMS:
			query += "AND loans.itemID > 0  "
		elif sStatus == Constants.DUED_ITEMS:
			query += "AND loans.itemID > 0 and loans.dueDate < ?"
			querrydata.append(todaysDate())

		if format_:
			format_ = str(format_)
			query += "AND items.format = ? "
			querrydata.append(format_)

		column = 'title'  # default
		if column_type == Constants.AUTHOR:
			column = 'author'
		elif column_type == Constants.TITLE:
			column = 'title'
		elif column_type == Constants.PUBLISHER:
			column = 'publisher'
		elif column_type == Constants.IDS:
			column = 'itemID'

		if column_type == Constants.IDS:
			if len(keys):
				query += 'AND items.itemID = ? '
				querrydata.append(keys[0])
		elif len(keys):
			key = keys[0].lower()
			query += "AND instr(lower(items." + column + "),  ?) \n"
			querrydata.append(key)
			if len(keys) > 1:
				for i in range(1, len(keys)):
					key = keys[i].lower()
					query += "OR instr(lower(items." + column + "),  ?) \n"
					querrydata.append(key)
		query += "GROUP BY items.itemID;"
		return query, querrydata

	def searchItems(self, sStatus, column_type, keys, format_):
		query = "SELECT "
		query += "       items.itemID,  items.format,  items.ISBN,  items.title,  items.author,  items.publisher,  items.year,  items.location, items.comments,  "
		query += "       item_formats.formatName,  languages.Ref_Name AS language,  "
		query += "       count (loans.itemID) AS loaned, loans.dueDate, loans.loanDate, loans.renewals "
		query += "FROM "
		query += "    'items' "
		query += "    INNER JOIN item_formats ON items.format = item_formats.formatID "
		query += "    left JOIN languages    ON items.lang  = languages.langIsoID "
		query += "    left  JOIN loans        ON items.itemID = loans.itemID "
		query += "WHERE items.itemID > 0 \n"

		queryF, querrydata = self.searchItemsFilters(sStatus, column_type, keys, format_)
		query += queryF

		try:
			self.cur.execute(query, querrydata)
		except sqlite3.Error as e:
			self.saveToLog("searchItems: " + str(e))
			return False
		Result = self.cur.fetchall()
		return Result

	def duedItems(self, sStatus, column_type, keys, format_):
		query = "SELECT "
		query += "      loans.loanID, loans.itemID, loans.userID, loans.loanDate, loans.dueDate, loans.renewals, "
		query += "      items.author, items.format, items.publisher, items.title, items.year, items.lang AS language, "
		query += "      users.name, users.familyname, users.userID, users.role, "
		query += "      grades.gradeName "
		query += "FROM loans "
		query += "INNER JOIN users ON users.userID = loans.userID  "
		query += "INNER JOIN items ON loans.itemID = items.itemID "
		query += "LEFT JOIN grades ON users.grade = grades.gradeID "
		query += "WHERE dueDate < ? "

		queryF, querrydata = self.searchItemsFilters(sStatus, column_type, keys, format_)
		querrydata = [todaysDate()] + querrydata
		query += queryF

		try:
			self.cur.execute(query, querrydata)
		except sqlite3.Error as e:
			self.saveToLog("duedItems - Error :" + str(e))
			return False
		self.Result = self.cur.fetchall()
		return self.Result


# load information

	def load_items(self, itemID=False):

		query = "SELECT "
		query += "       items.itemID,  items.format,  items.ISBN,  items.title,  items.author, "
		query += "       items.publisher,  items.year,  items.location, items.comments,  "
		query += "       item_formats.formatName,  item_formats.formatID,  languages.langIsoID, "
		query += " languages.Ref_Name AS language, "
		query += "       count (loans.itemID) AS loaned,  renewals "
		query += "FROM "
		query += "    'items' "
		query += "    INNER JOIN item_formats ON items.format = item_formats.formatID "
		query += "    left JOIN languages    ON items.lang  = languages.langIsoID "
		query += "    left  JOIN loans        ON items.itemID = loans.itemID "
		if itemID:
			query += "WHERE items.itemID = ? "
		query += "    GROUP BY items.itemID; "

		try:
			if itemID:
				self.cur.execute(query, [itemID, ])
			else:
				self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("load_items:" + str(e))
			return False

		if itemID:
			Result = self.cur.fetchone()
		else:
			Result = self.cur.fetchall()

		return Result

	def load_users(self, readerID=False):

		query = "SELECT "
		query += "      users.userID,  users.role,  users.name,  users.familyname,  users.IDN, "
		query += "      users.email,  users.address,  users.phone,  users.cellphone,  users.comments, "
		query += " users.IDN,  users.password,  users.status, "
		query += "      grades.gradeID as grade, grades.gradeName,  "
		query += "      roles.roleName,  "
		query += "      count(loans.userID) AS loans "
		query += "FROM users "
		query += "INNER JOIN grades ON users.grade = grades.gradeID "
		query += "INNER JOIN roles  ON users.role  = roles.roleID "
		query += "LEFT  JOIN loans  ON users.userID = loans.userID "
		if readerID:
			query += "WHERE users.userID = ? "
		query += "GROUP BY users.userID;"

		try:
			if readerID:
				self.cur.execute(query, [readerID, ])
			else:
				self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("load_users:" + str(e))
			return False
		if readerID:
			Result = self.cur.fetchone()
		else:
			Result = self.cur.fetchall()
		return Result

	def loan_data(self, type_, id_):

		if type_ not in (Constants.TYPE_ITEM, Constants.TYPE_LOAN):
			return False
		query = "SELECT  "
		query += "loanID, itemID, userID, loanDate, dueDate, renewals "
		query += "FROM loans "
		if type_ == Constants.TYPE_ITEM:
			query += "WHERE itemID = ? "
		elif type_ == Constants.TYPE_LOAN:
			query += "WHERE loanID = ? "
		query += "Limit 1;"

		try:
			self.cur.execute(query, [id_, ])
		except sqlite3.Error as e:
			self.saveToLog("loan_data - Error :" + str(e))
			return False
		self.Result = self.cur.fetchone()
		return self.Result


# items transit: loans, renews... etc

	def loanItem(self, itemID, userID, loanDate, dueDate):
		data = [itemID, userID, loanDate, dueDate]
		self.query1 = "INSERT INTO loans   ( itemID, userID, loanDate, dueDate) VALUES ( ?,  ?,  ?,  ?);"
		self.query2 = "INSERT INTO history ( itemID, userID, loanDate, dueDate) VALUES ( ?,  ?,  ?,  ?);"

		error = False
		try:
			self.cur.execute(self.query1, data)
			self.cur.execute(self.query2, data)
		except sqlite3.Error as e:
			self.saveToLog("loanItem:" + str(e))
			error = True
			return False
		if not error:
			self.conn.commit()
		return True

	def renewItem(self, date, loanID):
		data = [date, loanID]
		self.query1 = "UPDATE loans   set renewals = renewals+1,  dueDate = ? WHERE loanID = ? "
		self.query2 = "UPDATE history set renewals = renewals+1,  dueDate = ? WHERE loanID = ? "

		error = False
		try:
			self.cur.execute(self.query1, data)
			self.cur.execute(self.query2, data)
		except sqlite3.Error as e:
			self.saveToLog("renewItem:" + str(e))
			error = True
			return False
		if not error:
			self.conn.commit()
		return True

	def returnItem(self, loanID):
		# Erease the Loan from the active loans (table)
		query1 = "DELETE FROM loans WHERE loanID = ?;"

		# updates the status of the loan in the history table.
		data2 = [todaysDate(), loanID]
		query2 = "UPDATE history set returnDate = ? WHERE loanID= ? ; "

		error = False
		try:
			self.cur.execute(query1, [loanID, ])
			self.cur.execute(query2, data2)
		except sqlite3.Error as e:
			self.saveToLog("returnItem - Error :" + str(e))
			error = True
			return False
		if not error:
			self.conn.commit()
		return True

# asociated to users, items and loans

	def itemHistory(self, itemID):

		if not itemID:
			return False
		query = "SELECT "
		query += "       history.renewals, history.returnDate, "
		query += "       history.loanId, history.dueDate, history.loanDate, "
		query += "       users.name, users.familyname, users.userID, users.role,"
		query += "       grades.gradeName "
		query += "FROM "
		query += "    history "
		query += "    LEFT  JOIN items        ON items.itemID = history.itemID "
		query += "    LEFT  JOIN users        ON history.userID = users.userID "
		query += "    LEFT  JOIN grades        ON users.grade = grades.gradeID "
		query += "WHERE history.itemID = ?"
		query += "GROUP BY history.loanId;"

		try:
			self.cur.execute(query, [itemID, ])
		except sqlite3.Error as e:
			self.saveToLog("itemHistory:" + str(e))
			return False

		Result = self.cur.fetchall()

		return Result

	def userHystory(self, userID):

		if not userID:
			return False
		query = "SELECT "
		query += "       items.itemID, items.title,  items.author, "
		query += "       items.publisher,  items.year, "
		query += "       item_formats.formatID, languages.Ref_Name AS language, "
		query += "       history.renewals, history.dueDate, history.returnDate "
		query += "FROM "
		query += "    'items' "
		query += "    INNER JOIN item_formats ON items.format = item_formats.formatID "
		query += "    left JOIN languages    ON items.lang  = languages.langIsoID "
		query += "    left  JOIN history        ON items.itemID = history.itemID "
		query += "WHERE history.userID = ? and history.returnDate > 1 "
		query += "    GROUP BY items.itemID; "

		try:
			self.cur.execute(query, [userID, ])
		except sqlite3.Error as e:
			self.saveToLog("userHystory:" + str(e))
			return False

		Result = self.cur.fetchall()

		return Result

	def userLoans(self, userID):

		if not userID:
			return False
		query = "SELECT "
		query += "       items.itemID, items.title,  items.author, "
		query += "       items.publisher,  items.year, "
		query += "       item_formats.formatID, languages.Ref_Name AS language, "
		query += "       count (loans.itemID) AS loaned,  renewals "
		query += "FROM "
		query += "    'items' "
		query += "    INNER JOIN item_formats ON items.format = item_formats.formatID "
		query += "    left JOIN languages    ON items.lang  = languages.langIsoID "
		query += "    left  JOIN loans        ON items.itemID = loans.itemID "
		query += "WHERE loans.userID = ? "
		query += "    GROUP BY items.itemID; "

		try:
			self.cur.execute(query, [userID, ])
		except sqlite3.Error as e:
			self.saveToLog("userLoans:" + str(e))
			return False

		Result = self.cur.fetchall()

		return Result

	def userDuedItems(self, userID):

		if not userID:
			return False
		query = "SELECT "
		query += "       items.itemID, items.title,  items.author, "
		query += "       items.publisher,  items.year, "
		query += "       item_formats.formatID, languages.Ref_Name AS language, "
		query += "       count (loans.itemID) AS loaned,  renewals "
		query += "FROM "
		query += "    'items' "
		query += "    INNER JOIN item_formats ON items.format = item_formats.formatID "
		query += "    left JOIN languages    ON items.lang  = languages.langIsoID "
		query += "    left  JOIN loans        ON items.itemID = loans.itemID "
		query += "WHERE loans.userID = ? and loans.dueDate < ?"
		query += "    GROUP BY items.itemID; "

		try:
			self.cur.execute(query, [userID, todaysDate()])
		except sqlite3.Error as e:
			self.saveToLog("userDuedItems:" + str(e))
			return False

		Result = self.cur.fetchall()

		return Result

	def userDelays(self, user_id):
		# Selects all the loand with a due date >= to the given one
		query = "SELECT "
		query += "count(userID) as delays "
		query += "FROM loans "
		query += "Where userID = ? and dueDate < ?;"

		try:
			self.cur.execute(query, [user_id, todaysDate()])
		except sqlite3.Error as e:
			self.saveToLog("userDelays:" + str(e))
			return False

		Result = self.cur.fetchone()
		return Result['delays']

	def lastNloans(self, limit=3):
		query = "SELECT  "
		query += "loans.itemID,  loans.loanID,  "
		query += "items.title,  items.author "
		query += "FROM loans "
		query += "INNER JOIN items ON loans.itemID = items.itemID "
		query += "GROUP BY loans.itemID "
		query += "ORDER BY loans.itemID DESC "
		query += "Limit 10;"

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("lastNloans - Error :" + str(e))
			return False
		self.Result = self.cur.fetchall()
		return self.Result

	def lastNreturns(self, limit=3):
		query = "SELECT "
		query += "history.itemID,  "
		query += "items.title,  items.author "
		query += "FROM history "
		query += "INNER JOIN items ON history.itemID = items.itemID "
		query += "WHERE returnDate>0 "
		query += "GROUP BY history.itemID "
		query += "Limit 10;"

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("lastNreturns - Error :" + str(e))
			return False
		self.Result = self.cur.fetchall()
		return self.Result

	def dueInDate(self, date):
		'''
		it will also used to get reports for items 
		'''
		query = "SELECT "
		query += "loans.itemID,  loans.loanID,  loans.renewals,  "
		query += "items.title,  items.author "
		query += "FROM loans "
		query += "INNER JOIN items ON loans.itemID = items.itemID "
		query += "WHERE dueDate = ? "
		query += "GROUP BY loans.itemID; "

		try:
			self.cur.execute(query, [date, ])
		except sqlite3.Error as e:
			self.saveToLog("duetoday - Error :" + str(e))
			return False
		self.Result = self.cur.fetchall()
		return self.Result

	# ############################
	# #### Used by Home Page #####
	# ############################

	def totalFromTable(self, table):
		if not table:
			return False
		if table == Constants.TABLE_USERS:
			query = ' SELECT count(userID) AS N FROM ' + Constants.TABLE_USERS
		if table == Constants.TABLE_ITEMS:
			query = ' SELECT count(itemID) AS N FROM ' + Constants.TABLE_ITEMS
		if table == Constants.TABLE_fORMATS:
			query = ' SELECT count(formatID) AS N FROM ' + Constants.TABLE_fORMATS
		if table == Constants.TABLE_HISTORY:
			query = ' SELECT count(loanID) AS N FROM ' + Constants.TABLE_HISTORY
		if table == Constants.TABLE_LOANS:
			query = ' SELECT count(loanID) AS N FROM ' + Constants.TABLE_LOANS

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("totalFromTable - Error :" + str(e))
			return False
		Result = self.cur.fetchone()
		if 'N' not in Result.keys():
			return 0
		return Result['N']

	def countReaderByStatus(self, status):
		if status in (Constants.AVAILABLE_USERS, Constants.BLOCKED_USERS):
			query = 'SELECT count(userID) as N FROM ' + Constants.TABLE_USERS + '  WHERE status = ' + str(status)
		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("countReaderByStatus - Error :" + str(e))
			return 0
		Result = self.cur.fetchone()
		if 'N' not in Result.keys():
			return 0
		return Result['N']

	def itemsInCategory(self):
		query = "SELECT "
		query += "       item_formats.formatName, count(items.format) as N "
		query += "FROM "
		query += "    'items' "
		query += "    INNER JOIN item_formats ON items.format = item_formats.formatID "
		query += "    GROUP BY items.format; "

		try:
			self.cur.execute(query)
		except sqlite3.Error as e:
			self.saveToLog("itemsInCategory:" + str(e))
			return False
		Result = self.cur.fetchall()
		return Result

	def delayedbooks(self, date_):
		# Selects all the loans with a due date >= to the given one
		query = "SELECT count(itemID) AS N FROM loans WHERE dueDate < ?"
		try:
			self.cur.execute(query, [date_, ])
		except sqlite3.Error as e:
			self.saveToLog("delayedbooks:" + str(e))
			return False

		Result = self.cur.fetchone()
		if 'N' not in Result.keys():
			return 0
		return Result['N']

DBManager = DatabaseManager()


if __name__ == '__main__':
	print DBManager.load_items(0)
