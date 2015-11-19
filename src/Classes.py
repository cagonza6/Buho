# -*- coding: utf-8 -*

from Tools.Database import DBManager as DataBase
import config.GlobalConstants as Constants
from Tools.ItemTools import formatID


class BaseElement:

	def check(self):
		if not self.Data:
			return False
		return True

	def Data(self):
		if not self.check():
			return False
		return self.Data


class Reader(BaseElement):
	'''
	Clase Reader
	@id_: id of the user to search
	'''
	def __init__(self, id_):
		self.Data = False

		if id_:
			self.Data = DataBase.load_users(id_)
			if self.Data:
				self.Data['delays'] = DataBase.userDelays(self.ID())
				self.activeLoans = DataBase.userLoans(self.ID())
				# includes as a field the Id of the item
				if self.activeLoans:
					for i in range(0, len(self.activeLoans)):
						loan = self.activeLoans[i]
						self.activeLoans[i]['itemIdStr'] = formatID(loan['formatID'], loan['itemID'])

				self.duedItems = DataBase.userDuedItems(self.ID())
				if self.duedItems:
					for i in range(0, len(self.duedItems)):
						loan = self.duedItems[i]
						self.duedItems[i]['itemIdStr'] = formatID(loan['formatID'], loan['itemID'])

				self.history = DataBase.userHystory(self.ID())
				if self.history:
					for i in range(0, len(self.history)):
						loan = self.history[i]
						self.history[i]['itemIdStr'] = formatID(loan['formatID'], loan['itemID'])

	def ID(self):
		if not self.check():
			return False
		return self.Data['userID']

	def role(self):
		if not self.check():
			return False
		return self.Data['role']

	def id2str(self):
		if not self.check():
			return False
		return formatID(self.Data['role'], self.Data['userID'])

	def grade(self):
		if not self.check():
			return False
		return self.Data['grade']

	def gradeName(self):
		if not self.check():
			return False
		return self.Data['gradeName']

	def roleName(self):
		if not self.check():
			return False
		return self.Data['roleName']

	def status(self):
		if not self.check():
			return False
		return self.Data['status']

	def fullName(self):
		if not self.check():
			return False
		return self.Data['name'] + ' ' + self.Data['familyname']

	def name(self):
		if not self.check():
			return False
		return self.Data['name']

	def familyname(self):
		if not self.check():
			return False
		return self.Data['familyname']

	def IDN(self):
		if not self.check():
			return False
		return self.Data['IDN']

	def email(self):
		if not self.check():
			return False
		return self.Data['email']

	def address(self):
		if not self.check():
			return False
		return self.Data['address']

	def phone(self):
		if not self.check():
			return False
		return self.Data['phone']

	def cellphone(self):
		if not self.check():
			return False
		return self.Data['cellphone']

	def comments(self):
		if not self.check():
			return False
		return self.Data['comments']

	def loans(self):
		if not self.check():
			return False
		return self.Data['loans']

	def delays(self):
		if not self.check():
			return False
		return self.Data['delays']

'''
Clase Item
@id_: id of the item to search
'''


class Item(BaseElement):
	def __init__(self, id_):
		self.Data = False

		if id_:
			self.Data = DataBase.load_items(id_)
		if self.Data:
			self.history = DataBase.itemHistory(id_)

	def ID(self):
		if not self.check():
			return False
		return self.Data['itemID']

	def formatID(self):
		if not self.check():
			return False
		return self.Data['formatID']

	def id2str(self):
		if not self.check():
			return False
		return formatID(self.Data['formatID'], self.Data['itemID'])

	def formatName(self):
		if not self.check():
			return False
		return self.Data['formatName']

	def publisher(self):
		if not self.check():
			return False
		return self.Data['publisher']

	def barcode(self):
		if not self.check():
			return False
		if self.Data['barcode']:
			return self.Data['barcode']

	def ISBN(self):
		if not self.check():
			return False
		if self.Data['ISBN10']:
			return self.Data['ISBN10']
		elif self.Data['ISBN13']:
			return self.Data['ISBN13']
		return False

	def ISBN10(self):
		if not self.check():
			return False
		if self.Data['ISBN10']:
			return self.Data['ISBN10']
		return False

	def ISBN13(self):
		if not self.check():
			return False
		if self.Data['ISBN13']:
			return self.Data['ISBN13']
		return False

	def langIsoID(self):
		if not self.check():
			return False
		return self.Data['langIsoID']

	def language(self):
		if not self.check():
			return False
		return self.Data['language']

	def title(self):
		if not self.check():
			return False
		return self.Data['title']

	def author(self):
		if not self.check():
			return False
		return self.Data['author']

	def status(self):
		if not self.check():
			return False
		if self.loaned():
			status = Constants.STATUS_WARNING
		else:
			status = Constants.STATUS_VALID
		return status

	def loaned(self):
		if not self.check():
			return False
		return self.Data['loaned']

	def location(self):
		if not self.check():
			return False
		return self.Data['location']

	def year(self):
		if not self.check():
			return False
		return self.Data['year']

	def renewals(self):
		if not self.check():
			return False
		return self.Data['renewals']

	def comments(self):
		if not self.check():
			return False
		return self.Data['comments']

	def copy(self):
		if not self.check():
			return False
		return self.Data['copy']

	def getHistory(self):
		if self.history:
			return self.history
		return False
'''
Clase Loan
@id_: id of the item to search
'''


class Loan(BaseElement):
	def __init__(self, type_, id_):

		self.Data = False
		self.Data = DataBase.loan_data(type_, id_)

	def ID(self):
		if not self.check():
			return False
		return self.Data['loanID']

	def id2str(self):
		if not self.check():
			return False
		return formatID('LO', self.Data['loanID'])

	def itemID(self):
		if not self.check():
			return False
		return self.Data['itemID']

	def loanDate(self):
		if not self.check():
			return False
		return self.Data['loanDate']

	def userID(self):
		if not self.check():
			return False
		return self.Data['userID']

	def dueDate(self):
		if not self.check():
			return False
		return self.Data['dueDate']

	def renewals(self):
		if not self.check():
			return False
		return self.Data['renewals']


if __name__ == '__main__':

	item1 = Item(0)
	item2 = Item(1)
	print item1.id2str(), item2.id2str()

	loan1 = Loan(Constants.TYPE_LOAN, 0)
	loan2 = Loan(Constants.TYPE_LOAN, 1)
	print loan1.id2str(), loan2.id2str()

	reader1 = Reader(0)
	reader2 = Reader(1)
	print reader1.id2str(), reader2.id2str()
