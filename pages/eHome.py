from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import main

from components import menu
from page import Page
from components import header
from navigation import NavigationFunctions


class EHomePage(Page):
	url_tail = 'home'
	dynamic = False

	def load(self, expectedTab='send'):
		self.expected_tab = expectedTab
		self.nav = NavigationFunctions(self.driver)
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver, True)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
		IndexError) as e:
			return False

	def load_body(self):
		# self.balance = self.load_balance()
		self.send_tab = self.driver.find_element_by_class_name('send_tab')
		self.election_tab = self.driver.find_element_by_class_name('election_tab')
		self.activity_tab = self.driver.find_element_by_class_name('activity_tab')
		self.tabs = [self.send_tab, self.election_tab, self.activity_tab]
		self.tab_names = ['send', 'election', 'activity']
		self.currentTab = self.get_current_tab()

		# expectedTab will be 'login' when default login function is used.
		# Don't expect a certain tab in that situation
		if self.expected_tab == 'login' or self.expected_tab == self.currentTab:
			if self.currentTab == 'send':
				self.load_send_tab()
			elif self.currentTab == 'election':
				self.load_election_tab()
			elif self.currentTab == 'activity':
				self.load_activity_tab()
			# print('loaded tab: ' + str(self.currentTab))
		else:
			raise IndexError('eHome does not have expected tab selected')

	def get_current_tab(self):
		for i, tab in enumerate(self.tabs):
			color = self.tabs[i].value_of_css_property('color')
			selected_color = '56, 217, 244'
			if selected_color in color:
				return self.tab_names[i]
		return None

	def setTab(self, tab):
		self.scroll_to_top()
		tab_index = self.tab_names.index(tab)
		self.tabs[tab_index].click()
		self.on(tab)

##################### Send Tab #######################

	def load_send_tab(self):
		self.cards = self.driver.find_elements_by_class_name('card')
		self.card_titles = self.driver.find_elements_by_class_name('card-title')
		self.cardNames = ['bank', 'atm']
		self.send_to_bank = self.cards[0]
		self.send_to_atm = self.cards[1]
		self.learn_more = self.send_to_atm.find_element_by_class_name('atm_learn_more')

	def send(self, sendOption):
		if not sendOption:
			return
		if self.currentTab != 'send':
			self.setTab('send')

		index = self.cardNames.index(sendOption)
		if main.is_desktop():
			# raw_input('about to click card: ' + str(sendOption))
			self.cards[index].click()
			# raw_input('clicked?')
		else:
			# iOS: Clicking card doesn't do anything for some reason
			# raw_input('about to click card title: ' + str(sendOption))
			self.card_titles[index].click()
			# raw_input('clicked?')
		# Should be new page (send-to-bank, send-to-atm, send-to-cashout)

	def learn_more_action(self, action):
		try:
			self.move_to_el(self.learn_more)
		except WebDriverException:
			raw_input('inspect')
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'bank_get_started')))
		time.sleep(1)
		# action[0] is 'Get Started' button on card. action[1,2,3] are what we want
		actions = self.driver.find_elements_by_class_name('bank_get_started')
		if action == 0: # How to send to atm
			actions[1].click()
			WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'welcome-skip')))
			self.load_how_to()
		elif action == 1: # Find BBVA Bancomer locations
			actions[2].click()
			self.load_find_atm()
		elif action == 2: # FAQ
			actions[3].click()
			# Todo: Load 'coming soon' popup

	def load_how_to(self):
		try:
			# Don't get close/next buttons on last step. Only get done button on last step
			self.how_to_close = self.driver.find_element_by_class_name('welcome-skip')
			self.how_to_next = self.driver.find_element_by_class_name('welcome-next')
			self.how_to_done = None
		except NoSuchElementException:
			self.how_to_close = None
			self.how_to_next = None
			self.how_to_done = self.driver.find_element_by_class_name('welcome-done')

	def click_how_to_next(self):
		if self.how_to_next:
			self.how_to_next.click()
			time.sleep(1)
			self.load_how_to()

	def load_find_atm(self):
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'bbva_address')))
		self.atm_locator = self.driver.find_element_by_id('bbva_address')

	def find_atm(self, locator):
		if self.atm_locator:
			self.atm_locator.send_keys(locator)
		
	def close_find_atm(self):
		if main.is_desktop():
			AC(self.driver).send_keys(Keys.ESCAPE).perform()
		else:
			self.atm_locator.send_keys(Keys.ESCAPE)
			# press_keycode() only works on Android
			# main.native_context(self.driver)
			# self.driver.press_keycode(27)
			# main.webview_context(self.driver)

##################### Election Tab #######################

	def load_election_tab(self):
		self.election_form = self.driver.find_element_by_tag_name('form')
		self.election_table = self.election_form.find_element_by_tag_name('table')
		time.sleep(.4) # Need wait otherwise it thinks there's 0 employers
		self.total = self.try_load_total()
		self.employers = self.driver.find_elements_by_class_name('election_entry')
		self.save_button = self.try_load_save_button()
		self.election_prompt = self.try_load_election_prompt()
		self.history_button = (
			self.election_form.find_element_by_class_name('election_history'))

	def try_load_total(self):
		# Won't have total if user only has 1 business
		# Note: Need to load after small sleep. (page defaults to showing total)
		try:
			return self.driver.find_element_by_class_name('election_total')
		except NoSuchElementException:
			return None

	def try_load_save_button(self):
		# Not present after setting an election. Need to clear election prompt
		try:
			return self.election_form.find_element_by_class_name('primaryButton')
		except NoSuchElementException:
			return None

	def try_load_election_prompt(self):
		# Only present after setting/editing an election
		try:
			prompt = self.driver.find_element_by_class_name('election_prompt')
			return prompt
			# Prompt is now toast-like. No button to clear
			# return prompt.find_element_by_tag_name('button')
		except NoSuchElementException:
			return None

	def try_load_history_button(self):
		try:
			return self.election_form.find_element_by_tag_name('a')
		except NoSuchElementException:
			return None

	def view_election_history(self, expecting='prompt'):
		if self.currentTab != 'election':
			self.setTab('election')

		time.sleep(2)
		self.history_button.click()
		# Link should not redirect while election form is submitting.
		# Wait until election prompt shows up before clicking history button
		# Or, if prompt was cleared, should have save button back

	def num_employers(self):
		if self.currentTab != 'election':
			self.setTab('election')
		return len(self.employers)

	def get_employer_row(self,employer):
		if self.currentTab != 'election':
			self.setTab('election')
		# Given employer name or index in table, return <tbody> el from table
		try:
			if self.num_employers() == 1:
				return self.employers[0]
			elif type(employer) == int:
				return self.employers[employer]
			else:
				for row in self.employers:
					row_employer = row.find_element_by_tag_name("span").text
					if row_employer == "From " + employer:
						return row
		except NoSuchElementException:
			pass
		return None

	def set_focus_on_employer(self, employer_row):
		if self.currentTab != 'election':
			self.setTab('election')
		# Given employer_row, click right element to set focus

		# html is different for single vs multiple employers
		if self.num_employers() == 1:
			tr = employer_row.find_elements_by_tag_name('tr')[0]
		else:
			tr = employer_row.find_elements_by_tag_name('tr')[1]
		div = tr.find_elements_by_tag_name('div')[1]
		self.move_to_el(div)

	def get_election_amount(self, employer_row):
		if self.currentTab != 'election':
			self.setTab('election')
		# Given employer_row, return current amount
		# Use get_election_total() for returning total amount

		# html is different for single vs multiple employers
		if self.num_employers() == 1:
			tr = employer_row.find_elements_by_tag_name('tr')[0]
		else:
			tr = employer_row.find_elements_by_tag_name('tr')[1]
		div = tr.find_elements_by_tag_name('div')[2]
		return div.text

	def get_election_total(self):
		if self.currentTab != 'election':
			self.setTab('election')
		# requires multiple employers
		# return text of div in last employer row
		return self.total.find_element_by_tag_name('td').text

	def get_election_status(self, employer_row):
		"""Return whether election is 'pending' or not"""
		if self.currentTab != 'election':
			self.setTab('election')
		try:
			# should have div w/ class and color should be blue
			el = employer_row.find_element_by_class_name('pending_election')
			color = el.value_of_css_property('color')
			expected_color = 'rgba(56, 217, 244, 1)' # chrome
			if color == expected_color:
				return True
			return False
		except NoSuchElementException:
			return False

	def clear_pay_election(self, employer_row):
		# set focus and clear out existing election for given employer row el
		if self.currentTab != 'election':
			self.setTab('election')
		self.set_focus_on_employer(employer_row)
		amount = self.get_election_amount(employer_row)
		# desktop: hit backspace until input clear
		if main.is_desktop():
			for i in xrange(len(amount)):
				AC(self.driver).send_keys(Keys.BACKSPACE).perform()
		else: # Mobile: hit backspace on custom keyboard
			self.clear_currency(amount)

	def set_election(self, employer, amount):
		if self.currentTab != 'election':
			self.setTab('election')
		employer_row = self.get_employer_row(employer)
		if employer_row is not None:
			self.clear_pay_election(employer_row)
			# should still be focused
			if main.is_desktop():
				AC(self.driver).send_keys(amount).perform()
			else:
				self.enter_currency(amount)

	def get_elections(self):
		if self.currentTab != 'election':
			self.setTab('election')
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'election_entry')))
		num_employers = self.num_employers()
		elections = {}
		if (num_employers == 1):
			name = self.driver.find_element_by_tag_name("strong").text
			elections[name] = self.get_election_amount(self.employers[0])
			elections[name + ' pending'] = self.get_election_status(self.employers[0])
			elections["total"] = None
		else:
			for i in xrange(num_employers):
				name = self.employers[i].find_element_by_tag_name('span').text[5:]
				elections[name] = self.get_election_amount(self.employers[i])
				elections[name + ' pending'] = self.get_election_status(self.employers[i])

			# get total from last row in self.employers
			self.load()
			elections['total'] = self.get_election_total()
		return elections

	def click_save_elections(self):
		if self.currentTab != 'election':
			self.setTab('election')
		if self.save_button is not None:
			self.save_button.click()
		# Not redirecting anywhere right now

	def has_election_prompt(self):
		# Will be toast type prompt on desktop. Blue popup on mobile?
		return self.try_load_election_prompt() is not None

	def has_save_election_button(self):
		return self.save_button is not None

##################### Activity Tab #######################

	def load_activity_tab(self):
		self.transactions = self.load_transactions()
		self.dialog_button = self.try_load_confirmation_dialog()

	def load_transactions(self):
		entries = self.driver.find_elements_by_class_name('history-entry')
		# Expect there to be transactions. Throw IndexError if there aren't any
		entry = entries[0]
		return entries

	def try_load_confirmation_dialog(self):
		"""only there after sending and directing back to eHome page"""
		try:
			return self.driver.find_element_by_id('confirmOkButton')
		except NoSuchElementException:
			return None

	def get_dialog_pin(self):
		# return pin from text in dialog popup
		if self.dialog_button is not None:
			try:
				dialog = self.driver.find_element_by_class_name('sendConfirmDialog')
				text = dialog.text
				index = text.index('(')
				return text[index+1:index+5]
			except NoSuchElementException:
				return None

	def clear_confirmation_dialog(self):
		if self.dialog_button != None:
			self.dialog_button.click()

			# Wait until confirmation dialog disappears
			WDW(self.driver, 5).until(
					EC.invisibility_of_element_located((By.ID, 'confirmOkButton')))
			return True
		print('No transfer confirmation popup')
		return False

	def click_transaction(self, index=0):
		if self.currentTab != 'activity':
			self.setTab('activity')
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
		if self.currentTab != 'activity':
			self.setTab('activity')
		# Possible to load page before transactions show up
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

			info = {
				'amount': self.read_transaction_amount(divs[4].text),
				'recipient': self.read_transaction_recipient(divs[3].text),
				'status': self.read_transaction_status(spans[2].text),
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
			# Not displaying destination bank anymore (Oct 2018)
			# To David Castillo at ZB, N.A. DBA Zions Bank
			# atIndex = text.index(' at ')
			# return text[3:atIndex]
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

	def transaction_completes(self):
		if self.currentTab != 'activity':
			self.setTab('activity')
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

	def transaction_is_complete(self):
		if self.currentTab != 'activity':
			self.setTab('activity')
		# True if transaction[0] has 'check' icon
		try:
			info = self.get_transaction()
		except (WebDriverException, StaleElementReferenceException) as e:
			# page updated. reload and get transaction info again
			time.sleep(1) # give time for stuff to reload
			self.load(True)
			info = self.get_transaction()
		return info['icon'] == 'check'

##################### General #######################

	def load_balance(self):
		try:
			balance = self.driver.find_element_by_class_name('account_balance')
			# div child has href
			return balance.find_elements_by_tag_name('div')[0]
		except (NoSuchElementException, IndexError) as e:
			return None

	def get_balance(self):
		"""Return value of account balance"""
		if self.balance:
			text = self.balance.text
			index1 = text.index('$') + 1
			index2 = text.index(' USD')
			return text[index1:index2]

# class AccountDetailsPage(Page):
# 	url_tail = '/account-detail'

# 	# FDIC drill down page

# 	def load(self):
# 		try:
# 			self.header = header.PrivateHeader(self.driver, 'Account Details')
# 			self.my_cash = self.driver.find_elements_by_tag_name('h1')
# 			self.sources = self.driver.find_elements_by_tag_name('li')

# 			# No Id for continue button.
# 			# Use class (should be only element w/ class)
# 			links = self.driver.find_elements_by_class_name('has-linkprops')
# 			if len(self.continue_button) > 1:
# 				fail = '1' + 2
# 			self.continue_button = links[0]

# 			return True
# 		except (NoSuchElementException, StaleElementReferenceException) as e:
# 			return False

# 		def click_continue(self):
# 			self.continue_button.click()




