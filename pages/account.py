from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, TimeoutException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from components import menu
from page import Page
from components import header
import time
import main
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# WDW element: id = cash-bar

class AccountPage(Page):
	url_tail = 'account'
	dynamic = False
	#self.WDWait.until(EC.element_to_be_clickable((By.ID, 'cash-bar')))

	def load(self, has_transactions=False):
		WDW(self.driver, 10).until(lambda x: EC.text_to_be_present_in_element(
			(By.ID, 'cash-bar'), 'USD') or
			EC.text_to_be_present_in_element((By.ID, 'cash-bar'), 'money in your transfer savings')
		)
		#print('cash-bar text: ' + self.driver.find_element_by_id('cash-bar').text)
		# Should page have transactions?
		# If yes, fail loading until transactions load
		self.expect_transactions = has_transactions
		# print(self.expect_transactions)
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver, True)
			self.header = header.PrivateHeader(self.driver)
			# If we expect transactions, double check they're still 'valid'
			if self.expect_transactions:
				entry = self.transactions[0]
			return True
		except (NoSuchElementException, StaleElementReferenceException,
		IndexError) as e:
			return False

	def load_body(self):
		self.balance = self.try_load_balance()
		#print(self.balance.text)
		self.send_button = self.driver.find_element_by_id('send_money_button')
		if self.expect_transactions: # fail unless you find transactions
			self.transactions = self.load_transactions()
		else: # maybe has transactions. Don't care if it finds them.
			self.transactions = self.try_load_transactions()
		if self.expect_transactions and len(self.transactions) == 0:
			raw_input('Expected transactions. None found.')
		self.dialog_button = self.try_load_confirmation_dialog()

	def load_transactions(self):
		entries = self.driver.find_elements_by_class_name('history-entry')
		# Expect there to be transactions. Throw IndexError if there aren't any
		entry = entries[0]
		return entries

	def try_load_transactions(self):
		# Don't care if there are transactions
		try:
			return self.driver.find_elements_by_class_name('history-entry')
		except NoSuchElementException:
			return []

	def try_load_balance(self):
		try:
			self.balance_cont = self.driver.find_element_by_id('cash-bar')
			balance_amt = self.balance_cont.find_element_by_tag_name('span')
			#print('found balance_amt')
			#print(balance_amt)
			return balance_amt
		except NoSuchElementException:
			#print('failed to find balance.\n' + str(self.balance_cont))
			return None

	def try_load_confirmation_dialog(self):
		"""only there after sending and directing back to account page"""
		try:
			return self.driver.find_element_by_id('confirmOkButton')
		except NoSuchElementException:
			return None

	def clear_confirmation_dialog(self):
		if self.dialog_button != None:
			self.dialog_button.click()

		# Wait until confirmation dialog disappears
		WDW(self.driver, 5).until(
				EC.invisibility_of_element_located((By.ID, 'confirmOkButton')))

	def click_balance(self):
		if self.balance is None:
			self.try_load_balance()
		self.balance.click()

	def get_balance(self):
		if self.balance is None:
			self.try_load_balance()
		return self.balance.text[:-4]

	def send_money(self):
		self.send_button.click()
		try:
			WDW(self.driver, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME, 'recipient')))
		except TimeoutException:
			error = self.driver.find_element_by_tag_name('h2').text
			print("send money timeout: On page '" + error + "'")
			if 'Add Recipient' in error:
				raw_input('wtf')
			raise Exception(error)

	#Transaction code is duplicated in recipient_view.py

	def click_transaction(self, index=0):
		# Possible to load page before transactions show up
		if len(self.transactions) == 0:
			raw_input("No Transactions found")
		if main.is_ios():
			el = self.transactions[index].find_elements_by_tag_name('div')[0]
			el.click()
		else:
			self.transactions[index].click()
		WDW(self.driver, 10).until(EC.presence_of_element_located(
			(By.ID, 'transfer_ok_button')))

	def get_transaction(self, index=0):
		# Possible to load page before transactions show up
		# if len(self.transactions) == 0:
		# 	self.load()
		if len(self.transactions) == 0:
			raw_input("No Transactions found")

		try:
			transaction = self.transactions[index]
			spans = transaction.find_elements_by_tag_name('span')
			divs = transaction.find_elements_by_tag_name('div')

			# for i in xrange(len(divs)):
			# 	print(str(i) + " " + divs[i].text)
			# for i in xrange(len(spans)):
			# 	print(str(i) + " " + spans[i].text)

			# 0 To Lourdes Ortega
			# Arriving 26 March
			# -6.46 USD
			# 1
			# 2 To Lourdes Ortega
			# Arriving 26 March
			# 3 To Lourdes Ortega
			# 4 -6.46 USD
			# 0 To Lourdes Ortega
			# 1 Arriving 26 March
			# 2 Arriving
			# 3

			info = {
				'amount': self.read_transaction_amount(divs[4].text),
				'recipient': self.read_transaction_recipient(divs[3].text),
				'status': self.read_transaction_status(spans[1].text),
				# 'date': self.read_transaction_date(divs[5].text),
				'icon': self.read_transaction_icon(self.transactions[index])
			}
			# i.e. {'Completed','31 August 1:12 PM','-71.86','Lourdes Ortega','check'}
			return info
		except StaleElementReferenceException:
			# Transactions probably reloaded
			self.get_transaction(index)

	def read_transaction_amount(self, text):
		# print('transaction amount = ' + text)
		# Strip off last 4 characters (' USD')
		return text[:-4]

	def read_transaction_recipient(self, text):
		# to or from recipient?
		if text[:2] == 'To':
			return text[3:]
		else: # from
			return text[5:]

	def read_transaction_status(self, text):
		"""Return first word of transaction 'date' string"""
		spaceIndex = text.find(' ')
		if spaceIndex == -1:
			return text
		else:
			return text[0:spaceIndex]

	# def read_transaction_date(self,text):
	# 	"""Return everything after 1st word in transaction 'date' string"""
	# 	return text[text.find(' ')+1:]

	def read_transaction_icon(self, transaction):
		"""Interpret length of img src to determine image"""
		try:
			img = transaction.find_element_by_tag_name('img')
			return self.interpret_image(len(img.get_attribute('src')))
		except NoSuchElementException:
			# means there's no img element. Assume it's the spinner.
			return 'spinner'


	def interpret_image(self, img_src_length):
		"""Given length of img_src, determine which icon is used"""
		if img_src_length == 1302:
			return 'clock'
		elif img_src_length == 1314:
			return 'check'
		elif img_src_length == 1274:
			return 'x'
		else:
			return None

	#END DUPLICATED CODE

	def transaction_completes(self):
		# True: transaction[0] finishes w/in 20 seconds (speed=instant)
		timeout = time.time() + 25
		is_complete = False
		while is_complete is False:
			if self.transaction_is_complete():
				is_complete = True
			elif time.time() > timeout:
				break
			else:
				time.sleep(.5)

		return is_complete

		# try:
		#     WDW(self.driver,20).until(self.transaction_is_complete() is True)
		#     return True
		# except TimeoutException:
		#     return False

	def transaction_is_complete(self):
		# True if transaction[0] has 'check' icon
		try:
			info = self.get_transaction()
		except (WebDriverException, StaleElementReferenceException) as e:
			# page updated. reload and get transaction info again
			time.sleep(1) # give time for stuff to reload
			self.load(True)
			info = self.get_transaction()
		return info['icon'] == 'check'

		# Tend to get stale exception on Android, WebDriverException on ios


class AccountDetailsPage(Page):
	url_tail = '/account-detail'

	# FDIC drill down page

	def load(self):
		try:
			self.header = header.PrivateHeader(self.driver, 'Account Details')
			self.my_cash = self.driver.find_elements_by_tag_name('h1')
			self.sources = self.driver.find_elements_by_tag_name('li')

			# No Id for continue button.
			# Use class (should be only element w/ class)
			links = self.driver.find_elements_by_class_name('has-linkprops')
			if len(self.continue_button) > 1:
				fail = '1' + 2
			self.continue_button = links[0]

			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

		def click_continue(self):
			self.continue_button.click()




