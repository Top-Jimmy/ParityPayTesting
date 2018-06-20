from page import Page
from components import header
import main
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)

# Page for entering/confirming name when...
# 1: new employer creates account
# 2: new user responds to invite

class EnrollNamePage(Page):
	url_tail = "enroll-business/personal-name" # (employer signs up)
	# or "accept/personal-name" (responding to invite)
	dynamic = False

	def load(self):
		try:
			self.load_body()
			self.header = header.PubHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			WebDriverException, IndexError) as e:
			return False

	def load_body(self):
		self.form = self.driver.find_element_by_tag_name('form')
		self.continue_button = self.form.find_element_by_tag_name('button')
		self.first_name = self.form.find_elements_by_tag_name('input')[0]
		self.last_name = self.form.find_elements_by_tag_name('input')[1]

	def set_first_name(self,name):
		if main.is_android():
			self.try_hide_keyboard()
		self.first_name.click()
		self.first_name.clear()
		self.first_name.send_keys(name)

	def get_first_name(self):
		return self.first_name.get_attribute('value')

	def set_last_name(self,name):
		if main.is_android():
			self.try_hide_keyboard()
		self.last_name.click()
		self.last_name.clear()
		self.last_name.send_keys(name)

	def get_last_name(self):
		return self.last_name.get_attribute('value')

	def click_continue(self):
		if main.is_android():
			self.try_hide_keyboard()
		self.continue_button.click()