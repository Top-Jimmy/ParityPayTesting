from page import Page
from components import header
import main
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)

#Page for entering password when existing user...
# 1: tries add business through enroll as employer form on public page
# 2: responds to invite

class EnrollSigninPage(Page):
	url_tail = "enroll-business/signin" # (enroll business)
	# accept/signin (respond to invite)

	def load(self):
		try:
			self.load_body()
			self.header = header.PubHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			WebDriverException) as e:
			print(str(e) + '\n')
			return False

	def load_body(self):
		self.form = self.driver.find_element_by_tag_name('form')
		self.password_input = self.form.find_element_by_tag_name('input')
		self.show_password = self.form.find_element_by_id('show_password')
		self.forgot_password = self.form.find_element_by_tag_name('a')
		# need Id for password strength text
		self.continue_button = self.form.find_element_by_tag_name('button')

	def set_password(self,pw):
		self.password_input.click()
		self.password_input.send_keys(pw)

	def get_password(self):
		return self.password_input.get_attribute('value')

	def click_show_password(self):
		self.show_password.click()
		time.sleep(.2)

	def click_forgot_password(self):
		self.forgot_password.click()

	def click_continue(self):
		self.continue_button.click()

	def enter_password(self,pw):
		self.set_password(pw)
		self.click_continue()
