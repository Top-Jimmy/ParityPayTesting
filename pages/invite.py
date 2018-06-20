from page import Page
from components import header
import time
import main
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys

# Page 1 of invite process (enter DOB and zip code)
class DOBPage(Page):
	url_tail = "/i/"
	dynamic = True

	def load(self):
		try:
			self.h1 = self.try_load_expired_header()
			# load continue button if normal, signin button if link is expired
			if self.h1 and self.h1.text == 'Oops!':
				self.load_expired_link()
			else:
				self.header = header.PubHeader(self.driver)
				self.load_body()

			return True
		except (NoSuchElementException,
			StaleElementReferenceException, IndexError) as e:
			return False

	def try_load_expired_header(self):
		# expired link has <h1> element w/ text 'Oops!'
		try:
			return self.driver.find_element_by_tag_name('h1')
		except NoSuchElementException:
			return None

	def load_expired_link(self):
		"""Invite has expired. Or error"""
		self.signin_button = self.driver.find_element_by_id('signin_button')

	def load_body(self):
		self.form = self.driver.find_element_by_tag_name('form')
		self.dob_input = self.form.find_element_by_id('dob')
		self.zip_input = self.form.find_element_by_id('zip')
		self.continue_button = (
			self.form.find_element_by_class_name('primaryButton'))

	def set_dob(self, dob):
		self.dob_input.clear()
		self.dob_input.send_keys(dob)

	def set_zip(self, zipcode):
		self.zip_input.clear()
		self.zip_input.send_keys(zipcode)

	def get_dob(self):
		return self.dob_input.get_attribute('value')

	def get_zip(self):
		return self.zip_input.get_attribute('value')

	def click_continue(self):
		if self.is_expired(): # (expired link)
			self.signin_button.click()
		else:                       # (normal link)
			self.continue_button.click()

	def is_expired(self):
		"""Return True if signin_button visible"""
		try:
			return self.signin_button.is_displayed()
		except Exception:
			return False

# Page for entering email when responding to invite for NEW user
# Page 2 of invite process
class InvitePage(Page):
	url_tail = "/i/" # i.e. https://ppay11.herokuapp.com/i/9acb52f3/934464476
	dynamic = True

	def load(self):
		try:
			self.header = header.PubHeader(self.driver)
			self.h2 = self.driver.find_element_by_tag_name('h2')
			# load continue button if normal, signin button if link is expired
			if self.h2.text == 'Oops!':
				self.load_expired_link()
			else:
				self.load_body()
			return True
		except (NoSuchElementException, StaleElementReferenceException, WebDriverException) as e:
			return False

	def load_expired_link(self):
		"""Invite has expired. Or error"""
		self.signin_button = self.driver.find_element_by_id('signin_button')

	def load_body(self):
		self.form = self.driver.find_element_by_tag_name('form')
		self.email_input = self.form.find_element_by_tag_name('input')
		self.continue_button = (
			self.form.find_element_by_class_name('primaryButton'))
		self.why_button = self.form.find_element_by_tag_name('a')

	def set_email(self,email):
		self.move_to_el(self.email_input)
		self.email_input.clear()
		self.email_input.send_keys(email)

	def enter_email(self,email):
		self.set_email(email)
		self.click_continue()

	def get_email(self):
		return self.email_input.get_attribute('value')

	def click_why(self):
		self.why_button.click()

	def click_continue(self):
		if self.h2.text == 'Oops!': # (expired link)
			self.signin_button.click()
		else:                       # (normal link)
			self.continue_button.click()

	def is_expired(self):
		"""Return True if signin_button visible"""
		try:
			return self.signin_button.is_displayed()
		except Exception:
			return False
