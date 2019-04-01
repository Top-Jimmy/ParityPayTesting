from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from decimal import *
import time

import main
from component import Component
from navigation import NavigationFunctions

# Last screen confirming transfer details before actually sending

class Disclosure(Component):

	def __init__(self, driver):
		self.driver = driver
		self.nav = NavigationFunctions(self.driver)
		self.load()

	def load(self):
		self.container = self.driver.find_element_by_class_name('sendForm')
		# see code snippets for results
		# num_divs = len(self.form.find_elements_by_tag_name('div'))
		# for i in xrange(num_divs):
		#     text = self.form.find_elements_by_tag_name('div')[i].text

		self.name = self.read_name()
		self.load_table()

		self.exchange_rate = self.try_load_exchange_rate()
		self.total_to_recipient = self.try_load_total_to_recipient()
		self.load_disclosure_statements()
		self.continue_button = self.container.find_element_by_id('send_conf_button')

	def read_name(self):
		# Ignore stuff before name (Send payroll from Dunkin' Donuts to Jose Ortega)
		text = self.container.find_elements_by_tag_name('div')[2].text
		index = text.find(' to ') + 4
		return text[index - len(text):]

	def load_table(self):
		"""Table containing transfer amount, fees, and total"""
		self.table_rows = self.container.find_elements_by_tag_name('tr')
		# returns amount only (in USD)
		self.transfer_amount = self.nav.get_text(
			self.table_rows[0].find_elements_by_tag_name('td')[0])
		# Transfer fee row contains "+ " and "&nbsp;1.00" (desktop chrome)
		self.transfer_fee = (
			self.table_rows[1].find_elements_by_tag_name('td')[0].text[2:])
		self.transfer_total = self.nav.get_text(
			self.table_rows[2].find_elements_by_tag_name('td')[0])

	def try_load_exchange_rate(self):
		"""Amount in MXN. Only exists when sending to MX"""
		try:
			return self.container.find_element_by_id('exchangeRateDiv')
		except NoSuchElementException:
			return None

	def try_load_total_to_recipient(self):
		"""Amount in MXN, only exists when sending to MX"""
		try:
			return self.container.find_element_by_id('totalRecipDiv')
		except NoSuchElementException:
			return None

	def load_disclosure_statements(self):
		"""Up to 3 disclosure statements"""
		self.disclosure_30 = self.try_load_d_30()
		self.disclosure_less = self.try_load_d_less()
		self.disclosure_notify = self.try_load_d_notify()

	def try_load_d_30(self):
		"""You have 30 minutes to cancel this transfer..."""
		try:
			return self.container.find_element_by_id('disclose30MinDiv')
		except NoSuchElementException:
			return None

	def try_load_d_less(self):
		"""Recipient may receive less due to fees charged by..."""
		try:
			return self.container.find_element_by_id('discloseLessDiv')
		except NoSuchElementException:
			return None

	def try_load_d_notify(self):
		"""You'll be notified when the transfer is complete."""
		try:
			return self.container.find_element_by_id('discloseNotifyDiv')
		except NoSuchElementException:
			return None

	def has_d_30(self):
		return self.disclosure_30 is not None

	def has_d_less(self):
		return self.disclosure_less is not None

	def has_d_notify(self):
		return self.disclosure_notify is not None

	def get_exchange_rate(self):
		if self.exchange_rate is not None:
			return self.exchange_rate.text
		return None

	def get_name(self):
		return self.name

	def get_transfer_amount(self):
		return self.transfer_amount.replace(',', '')

	def get_transfer_fee(self):
		return self.transfer_fee.strip()

	def get_transfer_total(self):
		return self.transfer_total.replace(',', '')

	def get_total_to_recipient(self):
		return self.total_to_recipient.text

	def num_disclosures(self):
		return len(self.statements)

	def click_continue(self):
		self.nav.click_el(self.continue_button)

	def has_error(self):
		try:
			self.error = self.driver.find_element_by_class_name('alert-danger')
			self.error_button = self.error.find_element_by_tag_name('button')
			return True
		except NoSuchElementException:
			self.error = None
			self.error_button = None
		return False

	def has_upper_limit_error(self):
		if self.has_error():
			try:
				error_p = self.error.find_element_by_tag_name('div')
				# raw_input(self.nav.get_text(error_p))
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
