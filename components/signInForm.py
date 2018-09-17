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
		self.forgot_password_button = self.form.find_element_by_id('forgot_password')
		self.continue_button = self.form.find_element_by_id('submit_si_button')
		return True

	def submit(self, email, password, submit):
		print('Form: submitting sign in form')
		if email or email == '':
			self.set_email(email)
		print('Form: set email')
		if password or password == '':
			self.set_password(password)
		print('Form: set password')
		if submit:
			self.nav.click_el(self.continue_button)

	def set_email(self, email):
		raw_input('about to set email')
		self.nav.set_input(self.email_input, email)
		raw_input('set email?')

	def set_password(self, password):
		raw_input('about to set password')
		self.nav.set_input(self.password_input, password)
		raw_input('set password?')

	def toggle_password(self):
		self.nav.click_el(self.show_password_button)

	def forgot_password(self):
		self.nav.click_el(self.forgot_password_button)





