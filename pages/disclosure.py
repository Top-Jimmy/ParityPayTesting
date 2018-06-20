from page import Page
from components import menu
from components import header
import time
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys

# Last page before initiating transfer

class PreDisclosurePage(Page):
	url_tail = 'send-dfi-step2'

	def load(self):
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_body(self):
		self.form = self.driver.find_element_by_class_name('sendForm')
		# see code snippets for results
		# num_divs = len(self.form.find_elements_by_tag_name('div'))
		# for i in xrange(num_divs):
		#     text = self.form.find_elements_by_tag_name('div')[i].text

		self.name = self.get_name()
		self.load_table()

		self.exchange_rate = self.try_load_exchange_rate()
		self.total_to_recipient = self.try_load_total_to_recipient()
		self.load_disclosure_statements()
		self.continue_button = self.form.find_element_by_id('send_conf_button')

	def get_name(self):
		# Ignore stuff before name (Send payroll from Dunkin' Donuts to Jose Ortega)
		text = self.form.find_elements_by_tag_name('div')[2].text
		index = text.find(' to ') + 4
		return text[index - len(text):]

	def load_table(self):
		"""Table containing transfer amount, fees, and total"""
		self.table_rows = self.form.find_elements_by_tag_name('tr')
		# returns amount only (in USD)
		self.transfer_amount = (
			self.table_rows[0].find_elements_by_tag_name('td')[0].text)
		self.transfer_fee = (
			self.table_rows[1].find_elements_by_tag_name('td')[0].text[2:])
		self.transfer_total = (
			self.table_rows[2].find_elements_by_tag_name('td')[0].text)

	def try_load_exchange_rate(self):
		"""Amount in MXN. Only exists when sending to MX"""
		try:
			return self.form.find_element_by_id('exchangeRateDiv')
		except NoSuchElementException:
			return None

	def try_load_total_to_recipient(self):
		"""Amount in MXN, only exists when sending to MX"""
		try:
			return self.form.find_element_by_id('totalRecipDiv')
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
			return self.form.find_element_by_id('disclose30MinDiv')
		except NoSuchElementException:
			return None

	def try_load_d_less(self):
		"""Recipient may receive less due to fees charged by..."""
		try:
			return self.form.find_element_by_id('discloseLessDiv')
		except NoSuchElementException:
			return None

	def try_load_d_notify(self):
		"""You'll be notified when the transfer is complete."""
		try:
			return self.form.find_element_by_id('discloseNotifyDiv')
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

	def get_transfer_amount(self):
		return self.transfer_amount

	def get_transfer_fee(self):
		return self.transfer_fee

	def get_transfer_total(self):
		return self.transfer_total

	def get_total_to_recipient(self):
		return self.total_to_recipient.text

	def num_disclosures(self):
		return len(self.statements)

	def click_continue(self):
		self.continue_button.click()

