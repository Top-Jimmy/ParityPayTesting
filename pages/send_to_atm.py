from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from components import menu
from page import Page
from components import header
from components import stepper
from components import send_form
from components import disclosure
from components import additional_data_form
import time
import main
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SendToATMPage(Page):
	url_tail = 'send-to-atm'
	dynamic = False

	def load(self, expectedStep=None, isDataStep=False):
		try:
			self.stepper = stepper.Stepper(self.driver)
			self.currentStep = self.stepper.get_current_step()
			self.menu = menu.SideMenu(self.driver, False)
			self.header = header.PrivateHeader(self.driver)
			# print(self.currentStep)
			# print(str(isDataStep))
			if expectedStep and expectedStep != self.currentStep:
				print('Not on expected step. Expected: ' + str(expectedStep) + ', got: ' + str(self.currentStep))
				return False
			self.load_body(isDataStep)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
		IndexError, WebDriverException) as e:
			return False

	def load_body(self, isDataStep):
		if self.currentStep[0] == 0:
			self.load_recipients(isDataStep)
		elif self.currentStep[0] == 1:
			self.load_amount()
		elif self.currentStep[0] == 2:
			self.load_confirm()

############################ 1. Recipient Step ################################

	def load_recipients(self, isDataStep):
		# Recipient list or additional data form?
		# self.add_recipient_button = self.try_load_add_button()
		# self.addData_button = self.try_load_additional_data_button()
		if isDataStep: # Additional data form
			# print('loading info')
			self.load_additional_info()
		else: # Recipient list (default)
			# print('loading recipients')
			# todo: sometimes page loads before button is there, so it's None
			# Sometimes fails test_send_to_atm.py:TestATM.test_add_recipient
			self.add_recipient_button = self.try_load_add_button()
			self.recipients = self.try_load_recipients()

	def try_load_add_button(self):
		try:
			return self.driver.find_element_by_class_name('add_recipient_button')
		except NoSuchElementException:
			return None

	def try_load_additional_data_button(self):
		try:
			return self.driver.find_element_by_class_name('recipient_additionaldata')
		except NoSuchElementException:
			return None

	def try_load_recipients(self):
		try:
			return self.driver.find_elements_by_class_name('recipient')
		except NoSuchElementException:
			return []

	def load_additional_info(self):
		self.data_form = additional_data_form.AddDataForm(self.driver)
		# self.data_form = self.driver.find_element_by_tag_name('form')

	def get_recipient_by_name(self, name):
		"""Return recipient element whos text matches name"""
		# Get div w/ name text. Compare text with given name
		if isinstance(name, (list,)):
			name = ' '.join(name)
		for i, recip in enumerate(self.recipients):
			text = recip.find_elements_by_tag_name('div')[5].text
			# print(text)
			if text == name:
				return recip # self.recipients[i]
		return None

	def get_recipient_by_index(self, index):
		try:
			recip = self.recipients[index]
		except IndexError:
			return None

	def click_recipient(self, identifier):
		"""Given index or name of recipient, find and click 'send' or 'edit'
			Can only edit on 'recipient select' page
		"""
		if type(identifier) is int:
			recip = self.get_recipient_by_index(identifier)
		else:
			recip = self.get_recipient_by_name(identifier)
		if recip != None:
			# need to grab recip's first div for ios (one with cursor:pointer)
			if main.is_ios():
				recip = recip.find_elements_by_tag_name('div')[0]
			self.move_to_el(recip)
			# Not necessarily on next step. Handle reloading in test
		else:
			raise Exception("Error: could not find recipient: " + identifier)

	def add_recipient(self):
		self.scroll_to_bottom()
		self.add_recipient_button.click()
		# Should be on /add-recipient (recipient_name_page)

	def submit_data_form(self):
		if self.data_form:
			self.data_form.click_continue()
			self.on([1, "Amount"])


############################ 2. Amount Step ###################################

	def load_amount(self):
		self.send_form = send_form.SendForm(self.driver)

	def submit_send_form(self, reloadPage=True):
		self.send_form.click_continue()
		if reloadPage:
			self.on([2, "Confirm"])

############################ 3. Confirm Step ##################################

	def load_confirm(self):
		self.disclosure = disclosure.Disclosure(self.driver)

############################ Stepper functions ################################

	def set_step(self, step, reloadPage=True):
		# Step: either int or text of step
		newStep = self.stepper.click_step(step)
		if reloadPage:
			self.on(newStep)
