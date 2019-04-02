from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from decimal import *
import time

import main
from navigation import NavigationFunctions
from component import Component

# Email input, password input, show password button, 
# Forgot password link, sign in button
class SignInForm(Component):
	def __init__(self, driver):
		self.driver = driver
		self.nav = NavigationFunctions(self.driver)

	def load(self):
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'signin_form_id')))
		self.form = self.driver.find_element_by_id('signin_form_id')
		self.email_input = self.form.find_element_by_id('signin_form_user')
		self.password_input = self.form.find_element_by_id('signin_form_pw')
		self.show_password_button = self.form.find_element_by_id('show_password')
		self.forgot_password_button = self.form.find_element_by_id('forgot_password') # (link to reset password)
		self.continue_button = self.form.find_element_by_id('submit_si_button')
		# self.nav.print_source()
		# raw_input('source?')
		return True

	def submit(self, email, password, submit):
		if email or email == '':
			self.set_email(email)
		if password or password == '':
			self.set_password(password)
		if submit:
			self.nav.click_el(self.continue_button)

	def set_email(self, email):
		self.nav.set_input(self.email_input, email)

	def set_password(self, password):
		self.nav.set_input(self.password_input, password)

	def toggle_password(self):
		self.nav.click_el(self.show_password_button)

	def forgot_password(self):
		self.nav.dismiss_keyboard() # Android web needs to close keyboard. Native not tested.
		self.nav.click_el(self.forgot_password_button)





