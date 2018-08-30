from page import Page
from components import menu
from components import header
# from components import additional_info
import main
import time
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, TimeoutException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# page for adding/editing recipient bank accounts

class BankAccountPage(Page):
	url_tail = '/add-dest' # i.e. 'recipient/0b5e5e91/add-account'
	# when creating recipient url = 'recipient/0b5e5e91/add-account-wiz'

	def load(self, pageType='add'):
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			WebDriverException) as e:
			return False

	def load_body(self):
		try:
			self.form = self.driver.find_element_by_class_name('account_form')
		except NoSuchElementException:
			self.form = None
		self.try_load_destination_radio()
		if self.get_destination_type() == 'bank':
			self.form = self.driver.find_element_by_class_name('account_form')
			self.try_load_location()
			self.try_load_mexico()
			self.try_load_us()
			# self.form = (
			# 	self.driver.find_element_by_class_name('dest_additionaldata_form'))
			# self.try_load_bbva()
			# self.try_load_soriana_cashout()


		self.continue_button = self.try_load_continue_button()
		self.remove_button = self.try_load_remove_button()

	def try_load_destination_radio(self):
		# Load bank account/cash-out location radio buttons
		# Don't exist when editing bank account
		try:
			self.radio_bank = self.driver.find_element_by_id('radio_account')
			self.radio_cashout = self.driver.find_element_by_id('radio_cashout')
		except NoSuchElementException:
			self.radio_bank = None
			self.radio_cashout = None

################## Load Bank Accounts ##################

	def try_load_location(self):
		try:
			# self.form = self.driver.find_element_by_class_name('account_form')
			cont = self.form.find_element_by_id('account_location')
			self.current_location = cont.find_elements_by_tag_name('div')[2]
		except NoSuchElementException:
			self.current_location = None

	def try_load_mexico(self):
		try:
			# self.form = self.driver.find_element_by_class_name('account_form')
			self.clabe_input = self.try_load_clabe()
			self.what_is_clabe = self.try_load_what_is_clabe()
		except NoSuchElementException:
			self.form = None
			self.clabe_input = None
			self.what_is_clabe = None

	def try_load_clabe(self):
		try:
			return self.form.find_element_by_id('account_clabe')
		except NoSuchElementException:
			return None

	def try_load_what_is_clabe(self):
		try:
			return self.driver.find_element_by_xpath('//a[@href="/what-is-clabe"]')
		except NoSuchElementException:
			return None

	def try_load_us(self):
		try:
			self.form = self.driver.find_element_by_class_name('account_form')
			self.routing_number = self.try_load_routing()
			self.account_number = self.try_load_account()
		except NoSuchElementException:
			self.form = None
			self.routing_number = None
			self.account_number = None
		finally:
			self.try_load_account_type()
				# checking
				# savings

	def try_load_account_type(self):
		"""Checking/Savings exists on US transactions only"""
		try:
			self.account_type = self.driver.find_element_by_id('account_type')
			labels = self.account_type.find_elements_by_tag_name('label')
			self.checking = labels[0]
			self.savings = labels[1]
		except Exception:    #allows keyboard interrupt.
			self.account_type = None
			self.checking = None
			self.savings = None

	def try_load_routing(self):
		try:
			return self.form.find_element_by_id('account_routing')
		except NoSuchElementException:
			return None

	def try_load_account(self):
		try:
			return self.form.find_element_by_id('account_number')
		except NoSuchElementException:
			return None


################## Cashout Locations ##################

	# def try_load_bbva(self):
	# 	if self.get_destination_type() == 'cashout':
	# 		self.addInfo.load()
			# use functions in additional_info.py component

	# def try_load_soriana_cashout(self):
	# 	if self.cashout_type == 'bbva':
	# 		# nothing to load. Continue button already loaded
	# 		pass
	# 	else:
	# 		try:
	# 			self.address_input = self.driver.find_element_by_id('addressInput')
	# 			self.cashout_locations = self.driver.find_elements_by_class_name('sm-place-menuitem')
	# 			self.expand_button = None #self.driver.find_element_by_id('') Needs id/class
	# 			self.continue_button = self.driver.find_element_by_class_name('sm-continue-button')
	# 		except Exception:
	# 			self.address_input = None
	# 			self.cashout_locations = None
	# 			self.expand_button = None
	# 			self.continue_button = None

	def try_load_continue_button(self):
		try:
			return self.driver.find_element_by_class_name('primaryButton')
		except NoSuchElementException:
			return None

	def try_load_remove_button(self):
		"""Only exists when editing destination"""
		try:
			self.form = self.driver.find_element_by_class_name('account_form')
			return (
				self.form.find_element_by_class_name('remove_account_button'))
		except NoSuchElementException:
			return None

	def get_destination_type(self):
		if self.radio_bank is None:
			# If radios don't exist, editing bank account
			return 'bank'
		if self.radio_bank.is_selected():
			return 'bank'
		elif self.radio_cashout.is_selected():
			return 'cashout'
		else:
			print("Thinks no destination type is set")
		return None

	def set_destination_type(self, dest_type):
		current_dest = self.get_destination_type
		if current_dest != None and current_dest != dest_type:
			self.scroll_to_top()
			if dest_type == 'bank':
				self.radio_bank.click()
				# Wait for add_account_button
				WDW(self.driver, 6).until(EC.element_to_be_clickable(
					(By.ID, 'add_account_button')))
			else:
				self.radio_cashout.click()
				# Wait for addressInput
				WDW(self.driver, 6).until(EC.element_to_be_clickable(
					(By.ID, 'addressInput')))
			self.load()

	def set_clabe(self, clabe):
		self.clabe_input.clear()
		self.clabe_input.send_keys(clabe)
		if main.is_ios():
			self.clabe_input.send_keys('')

	def set_routing(self, number):
		self.routing_number.click()
		self.routing_number.clear()
		self.routing_number.send_keys(number)

	def set_account(self, number):
		self.account_number.clear()
		self.account_number.send_keys(number)
		if main.is_ios():
			self.account_number.click()

	def get_routing(self):
		return self.routing_number.get_attribute('value')

	def get_account(self):
		return self.account_number.get_attribute('value')

	def set_account_type(self, acct_type):
		if main.is_android():
			self.try_hide_keyboard()
		if acct_type.lower() == 'checking':
			self.move_to_el(self.checking)
		if acct_type.lower() == 'savings':
			self.move_to_el(self.savings)
		time.sleep(.2)

	def is_checking(self):
		"""Return true if checking is visible and selected"""
		return self.checking.is_selected()

	def is_savings(self):
		return self.savings.is_selected()

	def get_account_type(self):
		# IDS: don't use xpath for setting account type
		acct_type = ""
		bg = "rgba(56, 217, 244, 1)"
		try:
			if self.checking.value_of_css_property('background-color') == bg:
				return 'checking'
			elif self.savings.value_of_css_property('background-color') == bg:
				return 'savings'
			# if self.checking.find_element_by_xpath(
			# 	"..").value_of_css_property("background-color") == bg:
			# 	return "checking"
			# elif self.savings.find_element_by_xpath(
			# 	"..").value_of_css_property("background-color") == bg:
			# 	return "savings"
			return None
		except NoSuchElementException:
			return None

	def set_location(self, country):
		country = country.lower()
		el = self.current_location
		# if main.is_ios():
		# 	el = self.current_location.find_element_by_tag_name('button')
		el.click()
		WDW(self.driver, 10).until(lambda x : EC.presence_of_element_located(
			(By.ID, 'location_mx'))
			or EC.presence_of_element_located((By.ID, 'location_us')))
		#time.sleep(1)
		try:
			if country == "us" or country == "united states":
				self.driver.find_element_by_id('location_us').click()
			elif country == "mx" or country == "mexico":
				self.driver.find_element_by_id('location_mx').click()
			'''WDW(self.driver, 10).until(lambda x: EC.element_to_be_clickable(
				(By.ID, 'account_clabe'))
			or EC.element_to_be_clickable((By.ID, 'account_routing'))
			)'''
			time.sleep(1)
			self.load_body()
		except NoSuchElementException:
			print('error! No location option! (ba_page): ' + country)

	# select country by typing keys, then selecting by pressing enter
	def type_location(self, country):
		self.current_location.click()
		ActionChains(self.driver).send_keys(country).perform()
		time.sleep(.4)
		ActionChains(self.driver).send_keys(Keys.ENTER).perform()
		time.sleep(.4)
		self.load_body()

	def set_account_name(self, name):
		"""Only valid for personal accounts"""
		if self.account_name is not None:
			self.account_name.clear()
			self.account_name.send_keys(name)

	def get_account_name(self):
		"""Only valid for personal accounts"""
		if self.account_name is not None:
			return self.account_name.get_attribute('value')

	def get_location(self):
		return self.current_location.text

	def remove(self, action='remove'):
		"""Remove account if remove button there"""
		if self.remove_button is not None:
			self.remove_button.click()
			try:
				self.load_remove_dialog()
				if action == 'remove':
					self.remove_ok.click()
				else:
					self.remove_cancel.click()
			except NoSuchElementException:
				print('could not load remove account dialog')

	def load_remove_dialog(self):
		# dialog after clicking 'remove' button
		self.remove_ok = self.driver.find_element_by_class_name('okButton')
		self.remove_cancel = (
			self.driver.find_element_by_class_name('cancelButton'))

	def click_continue(self):
		# Wait until continue button is enabled
		try:
			WDW(self.driver, 5).until(lambda x: self.is_enabled(self.continue_button))

			self.move_to_el(self.continue_button)
		except TimeoutException:
			raise TimeoutException("Bank Account: Continue button never enabled")

		# Wait until no longer on page anymore.
		try:
			WDW(self.driver, 5).until(
				EC.invisibility_of_element_located((By.CLASS_NAME, 'account_form')))
		except WebDriverException:
			# not part of DOM. probably not on page anymore
			pass

	def click_what_is_clabe(self):
		self.what_is_clabe.click()

################################  CASH-OUT  ####################################

	def search_cashout_address(self, address):
		# Type in address, select first result, go.
		self.address_input.clear()
		self.address_input.send_keys(address)
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sm-place-menuitem')))

	def select_cashout_location(self, destination):
		self.load() #refresh view to include new place-menuitem elements?
		#self.expand_button.click()
		'''for location in self.cashout_locations:
			if destination in location.text:
				location.click()''' #Needs identifier on 'expand' button
		WDW(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sm-place-menuitem')))
		self.cashout_locations[0].click()
		WDW(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sm-continue-button')))
		#raw_input('check continue button')
		self.driver.find_element_by_class_name('sm-continue-button').click()
		#not properly saving continue button for some reason?
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'send_money_button')))
		#return to recipient-view page (/recipient/ID/view)
