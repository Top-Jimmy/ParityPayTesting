from page import Page
from components import header
import main
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Page for entering password when...
# 1: new employer creates account
# 2: new user responds to invite

class EnrollPasswordPage(Page):
	url_tail = "enroll-business/password" # (employer signs up)
	# or "accept/personal-name" (responding to invite)
	dynamic = False

	def load(self):
		try:
			WDW(self.driver, 10).until(
				EC.presence_of_element_located((By.ID, 'show_password')))
			self.load_body()
			self.header = header.PubHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			WebDriverException) as e:
			return False

	def load_body(self):
		self.form = self.driver.find_element_by_tag_name('form')
		self.password_input = self.form.find_element_by_tag_name('input')
		self.show_password = self.form.find_element_by_id('show_password')
		self.password_tips = self.form.find_element_by_class_name('password_tips')
		self.password_strength = self.form.find_element_by_id('scoreSpan')
		self.continue_button = self.form.find_element_by_class_name('primaryButton')

	def set_password(self,pw):
		if main.is_android():
			self.try_hide_keyboard()
		self.password_input.click()
		self.password_input.send_keys(pw)

	def get_password(self):
		return self.password_input.get_attribute('value')

	def get_password_strength(self):
		# might need to get child <span> of self.password_strength
		return self.password_strength.text

	def click_pw_tips(self):
		self.password_tips.click()

	def click_show_password(self):
		self.show_password.click()

	def click_continue(self):
		if main.is_android():
			self.try_hide_keyboard()
		self.continue_button.click()

