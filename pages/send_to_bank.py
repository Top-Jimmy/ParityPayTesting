from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from components import menu
from page import Page
from components import header
from components import stepper
from components import send_form
from components import disclosure
import time
import main
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SendToBankPage(Page):
	url_tail = 'send-to-bank'
	dynamic = False

	def load(self, expectedStep=None):
		try:
			self.menu = menu.SideMenu(self.driver, False)
			self.header = header.PrivateHeader(self.driver)
			self.stepper = stepper.Stepper(self.driver)
			self.currentStep = self.stepper.get_current_step()
			if expectedStep and expectedStep != self.currentStep:
				print('Not on expected step. Expected: ' + str(expectedStep) + ', got: ' + str(self.currentStep))
				return False
			self.load_body()
			return True
		except (NoSuchElementException, StaleElementReferenceException,
		IndexError, WebDriverException) as e:
			return False

	def load_body(self):
		if self.currentStep[0] == 0:
			self.load_accounts()
		elif self.currentStep[0] == 1:
			self.load_amount()
		elif self.currentStep[0] == 2:
			self.load_confirm()

############################ Step 1: Account ################################

	def load_accounts(self):
		self.load_recipients()
		self.add_account_button = (
			self.driver.find_element_by_class_name('add_recipient_button'))

	def load_recipients(self):
		# Grab recipients and info for their bank accounts
		self.recipUL = self.driver.find_elements_by_class_name('recipAccounts')
		# Should have at least 1. Fail to load page if there aren't any
		fail = self.recipUL[0]

		self.recipients = {}
		for i, recip in enumerate(self.recipUL):
			name = self.read_recip_name(i)
			bank_accounts = self.recipUL[i].find_elements_by_tag_name('li')
			del bank_accounts[0] # 1st li is header crap
			accounts = []
			for i, account in enumerate(bank_accounts):
				text = bank_accounts[i].find_elements_by_tag_name('div')[1].text
				info = self.read_account_info(text)
				if main.is_ios():
					info['element'] = bank_accounts[i].find_elements_by_tag_name('div')[0]
				else:
					info['element'] = bank_accounts[i]
				accounts.append(info)
			self.recipients[name] = accounts

	# Examples...

	# Iterate through jose's accounts
	# jose = sendToBank.recipients['Jose Ortega']
	# 	for i, accountNumber in enumerate(account['accountNumber'] for account in jose):
	# 		print str(accountNumber)

	# accountNumber = sendToBank.recipients['Andrew Tidd'][0]['accountNumber']

	# {
	# 	u'Jose Ortega':
	# 		[
	# 			{'accountNumber': u'XXXX1234',
	# 			'bank': u'ZB, N.A. DBA Zions Bank',
	# 			'element': element },
	# 			{'accountNumber': u'XXXX1234',
	# 			'bank': u'ZB, N.A. DBA Zions Bank',
	# 			'element': element }
	# 		],
	# 	u'Andrew Tidd':
	# 		[{'accountNumber': u'XXX4',
	# 			'bank': u'ZB, N.A. DBA Zions Bank',
	# 			'element': element
	# 		}]
	# }

	def read_recip_name(self, index):
		text = self.recipUL[index].find_elements_by_tag_name('li')[0].text
		# i.e. "Accounts of {name} "
		return text[12:]

	def read_account_info(self, text):
		# Split into bank name and account number
		index = text.index('Account ')
		return {'bank': text[0:index], 'accountNumber': text[index+8:]}

	def add_account(self):
		self.scroll_to_bottom()
		self.add_account_button.click()

	def click_account(self, recipientName, accountIdentifier):
		try:
			recip = self.recipients[recipientName]
			if type(accountIdentifier) is int:
				# send_to_bank.recipients[recip][0]['element'].click()
				recip[accountIdentifier]['element'].click()
			else:
				# Try and match text
				for i, bankName in enumerate(account['bank'] for account in recip):
					if accountIdentifier in bankName:
						self.move_to_el(recip[i]['element'])
						# recip[i]['element'].click()
						break
			# Reload page. Should be on next step
			return self.on([1, 'Specify Amount'])
		except (IndexError, KeyError) as e:
			return False

		# jose = sendToBank.recipients['Jose Ortega']
		# for i, accountNumber in enumerate(account['accountNumber'] for account in jose):

############################ Step 2: Amount ################################

	def load_amount(self):
		# Sending to US banks only right now.
		self.send_form = send_form.SendForm(self.driver)

	def submit_send_form(self, reloadPage=True):
		self.send_form.click_continue()
		if reloadPage:
			self.on([2, "Confirm & Send"])

############################ Step 3: Confirm ################################

	def load_confirm(self):
		self.continue_button = self.driver.find_element_by_id('send_conf_button')
		self.disclosure = disclosure.Disclosure(self.driver)

############################ Stepper functions ################################

	def set_step(self, step, reloadPage=True):
		# Step: either int or text of step
		newStep = self.stepper.click_step(step)
		if reloadPage:
			self.on(newStep)


