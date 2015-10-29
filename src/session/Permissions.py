from enum import IntEnum  # pip install enum34


class AccountsPermissionsEnum(IntEnum):
	SEE_USER_INFO    = pow(2, 0)
	PRINT_CARDS      = pow(2, 1)
	PRINT_OWN_CARD   = pow(2, 2)
	EDIT_OWN_ACCOUNT = pow(2, 3)
	EDIT_ACCOUNTS    = pow(2, 4)


class ItemPermissionsEnum(IntEnum):
	ADD_ITEM  = pow(2, 0)
	EDIT_ITEM = pow(2, 1)


class UserPermissionsEnum(IntEnum):
	ADD_USER  = pow(2, 0)
	EDIT_USER = pow(2, 1)


class LoanPermissionsEnum(IntEnum):
	LOAN_ITEMS      = pow(2, 0)
	RETRIEVE_ITEMS  = pow(2, 1)
	CAN_RENEW_LOAN  = pow(2, 2)
	CAN_EDIT_LOAN   = pow(2, 3)


class UserPermissions():
	def __init__(self, AccountsPermissionsEnum, itemPermissions, loanPermissions):
		self.permissions = AccountsPermissionsEnum
		pass

	def exists(self, value):
		if max(0, self.permissions & value):
			return True
		return False

	def can_see_user_info(self):
		return self.exists(AccountsPermissionsEnum.SEE_USER_INFO)

	def can_print_cards(self):
		return self.exists(AccountsPermissionsEnum.PRINT_CARDS)

	def can_edit_own_account(self):
		return self.exists(AccountsPermissionsEnum.EDIT_OWN_ACCOUNT)

	def can_edit_accounts(self):
		return self.exists(AccountsPermissionsEnum.EDIT_ACCOUNTS)


if __name__ == "__main__":
	userACPa = 0b0000010110
	userACPb = 0b0000001001

	userACP = userACPa + userACPb
	per = UserPermissions(userACP, 0, 0)

	print per.can_see_user_info()
	print per.can_print_cards()
	print per.can_edit_own_account()
	print per.can_edit_accounts()
