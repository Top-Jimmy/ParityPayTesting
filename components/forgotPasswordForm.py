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

class ForgotPasswordForm(Component):
	def __init__(self, driver):
		self.driver = driver
		self.nav = NavigationFunctions(self.driver)

	def load(self):
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'resetPWForm')))
		self.form = self.driver.find_element_by_class_name('resetPWForm')
		self.email_input = self.form.find_element_by_id('login')
		self.continue_button = self.form.find_element_by_id('submit_button')
		return True

	def submit(self, email, submit):
		if email or email == '':
			self.set_email(email)
		if submit:
			self.nav.click_el(self.continue_button)

	def set_email(self, email):
		self.nav.set_input(self.email_input, email)





