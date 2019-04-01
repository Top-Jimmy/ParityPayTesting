from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException, TimeoutException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from decimal import *
import time

from navigation import NavigationFunctions
from component import Component
import main

class SendForm(Component):

	def __init__(self, driver):
		self.driver = driver
		self.nav = NavigationFunctions(self.driver)
		self.load()

	def load(self):
		self.form = self.driver.find_element_by_class_name('sendForm')
		self.type = self.load_destination_type()

		if self.type == 'atm':
			self.try_load_bbva_picker();
		else:
			self.usd_div = self.form.find_element_by_id('sourceAmountInput')
			self.usd_amount = (
				self.form.find_element_by_id('sourceAmountInput_number'))
			self.usd_input = self.form.find_element_by_id('sourceAmountInput_hide')
			self.mxn_div = self.try_load_mxn_div()
			self.mxn_amount = self.try_load_mxn_amount()
			self.mxn_input = self.try_load_mxn_input()
			# BBVA doesn't have a speed option for MX accounts
			# self.try_load_delivery_speed()

		self.account_balance = (
			self.form.find_element_by_id('accountBalanceDiv'))
		self.exchange_rate = self.try_load_exchange_rate()

		# self.destination = self.form.find_element_by_tag_name('a')
		self.continue_button = self.form.find_element_by_id('send_cont_button')

	def load_destination_type(self):
		# Destination types...
		# 'atm': has currency picker
		# 'bank': has id=sourceAmountInput
		# 'cashout': not implemented yet
		try:
			bbvaAmount = self.form.find_element_by_class_name('picker-item-selected')
			return 'atm'
		except NoSuchElementException:
			return 'bank'

	def try_load_bbva_picker(self):
		try:
			if main.is_desktop():
				self.pickerUp = self.form.find_element_by_id('currencyUp')
				self.pickerDown = self.form.find_element_by_id('currencyDown')
			else:
				self.pickerUp = None
				self.pickerDown = None
			self.pickerOptions = self.form.find_elements_by_class_name('picker-item')
			self.bbvaAmount = (
				self.form.find_element_by_class_name('picker-item-selected').text.replace(",", ""))
			self.bbvaUSDAmount = (
				self.form.find_element_by_class_name('usd_amount').text)
		except NoSuchElementException:
			self.pickerUp = None
			self.pickerDown = None
			self.pickerOptions = None
			self.bbvaAmount = None
			self.bbvaUSDAmount = None
			print('failed to load bbva picker')

	def try_load_mxn_div(self):
		# only there when sending to MX. Element you click on
		try:
			return self.form.find_element_by_id('destAmountInput')
		except NoSuchElementException:
			return None

	def try_load_mxn_amount(self):
		# only there when sending to MX. Element that has amount as text
		try:
			return self.form.find_element_by_id('destAmountInput_number') #_number
		except NoSuchElementException:
			return None

	def try_load_mxn_input(self):
		# hidden input element. Send keys to this el on desktop
		try:
			return self.form.find_element_by_id('destAmountInput_hide')
		except NoSuchElementException:
			return None

	def try_load_exchange_rate(self):
		# only there when sending to MX
		try:
			self.exchange_cont = (
				self.form.find_element_by_id('exchangeRateDiv'))
			return self.exchange_cont.find_element_by_tag_name('span')
		except NoSuchElementException:
			return None

	def try_load_delivery_speed(self):
		"""Look for delivery speed stuff if sending to MX"""
		if self.mxn_div is not None:
			if 'SORIANA' not in self.destination.text:
				if self.toggle_or_radio() == 'radio':
					cont = self.form.find_element_by_id('radio_speed')
					inputs = cont.find_elements_by_tag_name('input')
					self.radio_fast = inputs[0]
					self.radio_instant = inputs[1]
					# self.radio_fast = (
					#   self.form.find_element_by_id('fastRadioButton'))
					# self.radio_instant = (
					#   self.form.find_element_by_id('instantRadioButton'))
				else:
					self.toggle = self.form.find_element_by_id('instantToggle')
			else:
				self.toggle = None

####################### BBVA functions ########################

	def get_picker_item(self, mxnAmount):
		# Return picker-item that corresponds to desired mxnAmount
		# amount must be multiple of 100
		for i, option in enumerate(self.pickerOptions):
			text = option.text.replace(",", "")
			# print(text)
			if text == mxnAmount:
				return self.pickerOptions[i]
		return None

	def get_picker_index(self):
		# return index of currently selected item
		for i, option in enumerate(self.pickerOptions):
			classes = option.get_attribute('class')
			if 'picker-item-selected' in classes:
				return i
		return None

	def get_direction(self, desired_amount):
		# is current bbva amount clickable? If not, which direction does picker need to move?
		current_amount = self.form.find_element_by_class_name('picker-item-selected').text
		current_amount = current_amount.replace(",", "") # Strip out commas for Decimal functions

		difference = Decimal(desired_amount) - Decimal(current_amount)
		if (difference >= -200) and (difference <= 200):
			# Desired amount is w/in 200 of current amount. Desired amount should be clickable
			return 'click'
		elif difference > 200:
			# Element not visible. Scroll down
			return 'down'
		else:
			return 'up'

	def move_picker(self, direction):
		if main.is_desktop():
			if direction == 'down':
				self.nav.click_el(self.pickerDown)
			else:
				self.nav.click_el(self.pickerUp)
		else:
			if direction == 'down':
				self.nav.click_el(self.pickerOptions[self.get_picker_index() + 2])
			else:
				self.nav.click_el(self.pickerOptions[self.get_picker_index() - 2])

	def set_bbva_amount(self, mxnAmount):
		# move up or down until amount is clickable
		# amount must be in multiples of 100
		if self.type == 'atm' and mxnAmount != self.bbvaAmount:
			# env_type = main.get_env()

			while mxnAmount != self.bbvaAmount:
				direction = self.get_direction(mxnAmount)
				if direction == 'click':
					item = self.get_picker_item(mxnAmount)
					self.nav.click_el(item)
				else:
					self.move_picker(direction)
				time.sleep(.4)

				clsName = 'picker-item-selected'
				self.bbvaAmount = (
					self.form.find_element_by_class_name(clsName).text.replace(",", ""))
				self.bbvaUSDAmount = (
					self.form.find_element_by_class_name('usd_amount').text)

	def get_bbva_amount(self):
		if self.type == 'atm':
			return self.bbvaAmount

	def toggle_or_radio(self):
		"""Is UI set to radio buttons or toggle switch?"""
		try:
			el = self.form.find_element_by_id('instantToggle')
			return 'toggle'
		except NoSuchElementException:
			return 'radio'

	def set_speed(self, speed='fast'):
		"""Set toggle/radio to given speed"""
		if self.toggle_or_radio() == 'radio':
			self.set_speed_radio(speed)
		else: # toggle
			self.set_speed_toggle(speed)

	def get_speed(self, speed='toggle'):
		"""Return speed indicated by radio/toggle"""
		if self.toggle_or_radio() == 'radio':
			return self.get_speed_radio()
		else: # default (toggle)
			return self.get_speed_toggle()

	def set_speed_radio(self, speed):
		# has issues clicking 'invisible' elements on Safari desktop
		if speed == 'instant':
			self.click_el(self.radio_instant)
		else: # default (fast)
			self.click_el(self.radio_fast)

	def get_speed_radio(self):
		"""Which radio button is selected? Instant or Fast (default)?"""
		if self.radio_instant.get_attribute('checked'):
			return 'instant'
		else:
			return 'fast'

	def set_speed_toggle(self, speed):
		if self.get_speed_toggle() != speed:
			if main.is_ios():
				el = self.toggle.find_element_by_tag_name('input')
				self.nav.click_el(el)
			else:
				self.move_to_el(self.toggle)

	def get_speed_toggle(self):
		el = self.toggle.find_element_by_tag_name('input')
		if el.get_attribute('checked'):
			return 'instant'
		else: # default (fast)
			return 'fast'

	def get_balance(self):
		return self.account_balance.text

	def get_exchange_rate(self):
		if self.exchange_rate is not None:
			return self.exchange_rate.text
		return None

	def clear_currency_input(self, currency_type):
		"""Clear out amount of given currency_type"""
		# set focus on input
		el = None
		amount = ''
		if currency_type.lower() == 'usd':
			el = self.usd_amount
			amount = self.get_usd()
		elif currency_type.lower() == 'mxn':
			el = self.mxn_amount
			amount = self.get_mxn()

		if el:
			self.nav.click_el(el)

		# Desktop: hit backspace enough times to clear out current amount
		# Mobile: hit backspace (on custom keyboard) enough times to clear
		if main.is_desktop():
			for i in xrange(len(amount)):
				AC(self.driver).send_keys(Keys.BACKSPACE).perform()
		else: # Mobile: hit backspace on custom keyboard
			self.clear_currency(amount)

	def set_usd(self, amount):
		# clear current amount and enter given amount
		self.clear_currency_input('usd')
		if main.is_desktop():
			self.usd_input.send_keys(str(amount))
			# self.usd_div.send_keys(amount)
		else:
			self.enter_currency(amount)

	def set_mxn(self, amount):
		# clear current amount and enter given amount
		self.clear_currency_input('mxn')
		if main.is_desktop():
			self.mxn_input.send_keys(str(amount))
			# self.mxn_div.send_keys(amount)
		else:
			self.enter_currency(amount)

	def get_usd(self):
		if self.type == 'atm':
			return self.bbvaUSDAmount
		else:
			amount = (self.usd_amount.text).replace(',', '')
			return amount

	def get_mxn(self):
		return self.mxn_amount.text

	def has_error(self):
		try:
			self.error = self.form.find_element_by_class_name('alert-danger')
			self.error_button = self.error.find_element_by_tag_name('button')
			return True
		except NoSuchElementException:
			self.error = None
			self.error_button = None
		return False

	def has_balance_error(self):
		"""Return if page has 'You have no money to send.' msg"""
		# This text is difficult to parse (react crap and weird ascii chars).
		# Seems to change sometimes. Last updated 11/29
		if self.has_error():
			try:
				error_p = self.error.find_element_by_tag_name('div')
				if self.nav.get_text(error_p) == 'You have no money to send.':
					return True
			except NoSuchElementException:
				pass
		return False

	def has_upper_limit_error(self):
		if self.has_error():
			try:
				error_p = self.error.find_element_by_tag_name('div')
				raw_input(self.nav.get_text(error_p))
				if 'exceed your deposit limit of USD $999 per day' in self.nav.get_text(error_p):
					return True
			except NoSuchElementException:
				pass
		return False

	def try_clear_error(self):
		if self.has_error():
			# error not visible on mobile
			if not main.is_desktop():
				self.scroll_to_bottom()
			self.nav.click_el(self.error_button)
			time.sleep(.6)

	def click_account(self):
		self.nav.click_el(self.destination)
		time.sleep(1)

	def get_account_info(self):
		# get div w/ text els. return bank name and clabe text
		acct_div = self.destination.find_elements_by_tag_name('div')[1]
		account_info = {
			'bank': acct_div.find_elements_by_tag_name('div')[0].text,
			'clabe': acct_div.find_elements_by_tag_name('div')[1].text
		}
		return account_info

	################## Custom Currency Keyboard ##########################

	def enter_currency(self, amount):
		"""Enter given amount using custom keyboard then close keyboard
			Mobile ONLY
			Requires input is focused and custom keyboard is open"""
		try:
			self.keyboard = (
				self.driver.find_element_by_class_name('custom_keyboard'))

			for i in xrange(len(amount)):
				# raw_input('typing index:' + str(i) + ' char:' + str(amount[i]))
				self.click_custom_key(amount[i])

			self.close_custom_keyboard()
			return True # pass in el w/ amount and return it matches amount?
		except NoSuchElementException:
			return False

	def clear_currency(self, amount):
		"""Given amount (as text), press backspace enough to clear.
			Input needs to be selected and custom keyboard open"""
		if amount != '':
			for i in xrange(len(amount)):
				self.click_custom_key('backspace')

	def close_custom_keyboard(self):
		"""If open, close custom keyboard"""
		try:
			el = self.driver.find_element_by_id('accountBalanceDiv')
			self.nav.click_el(el)
		except NoSuchElementException:
			print('SendForm: Could not find acct balance to close keyboard')

	def click_custom_key(self, character):
		"""Given valid character, press correct key on custom keyboard"""
		key_el = self.get_custom_key(character)
		if key_el is not None:
			self.nav.click_el(key_el)

	def get_custom_key(self, character):
		"""return custom keyboard element corresponding to given character"""
		keys = {
			'0': 'key_0',
			'1': 'key_1',
			'2': 'key_2',
			'3': 'key_3',
			'4': 'key_4',
			'5': 'key_5',
			'6': 'key_6',
			'7': 'key_7',
			'8': 'key_8',
			'9': 'key_9',
			'.': 'key_dot',
			'backspace': 'key_back'
		}
		try:
			return self.driver.find_element_by_class_name(keys[character])
		except NoSuchElementException:
			print('could not find key w/ class ' + keys[character])
			return None

	def is_form_enabled(self):
		return self.continue_button.is_enabled()

	def click_continue(self):
		self.continue_button = self.form.find_element_by_id('send_cont_button')
		try:
			WDW(self.driver, 10).until(
				EC.element_to_be_clickable((By.ID, 'send_cont_button')))
		except TimeoutException:
			raise TimeoutException("Send page: Continue button not enabled.")
		self.nav.click_el(self.continue_button)
		try:
			WDW(self.driver, 10).until(
				EC.presence_of_element_located((By.ID, 'send_conf_button')))
		except TimeoutException:
			raise TimeoutException("Send Page: Could not find element on next page.")
