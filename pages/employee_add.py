from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from components import header
from components import menu
import time
from selenium.webdriver import ActionChains


class AddEmployeePage(Page):
	url_tail = 'add-employee'
	dynamic = False

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
		self.form = self.driver.find_element_by_tag_name('form')
		find_by = self.form.find_elements_by_tag_name
		self.first_name_input = find_by('input')[0]
		self.last_name_input = find_by('input')[1]
		self.id_input = find_by('input')[2]
		self.dob_input = find_by('input')[3]
		self.zip_input = find_by('input')[4]
		self.email_input = find_by('input')[5]
		self.phone_input = find_by('input')[6]
		self.add_button = find_by('button')[0]

		self.inputs = {
			'first_name': self.first_name_input,
			'last_name': self.last_name_input,
			'employee_id': self.id_input,
			'dob': self.dob_input,
			'zip_code': self.zip_input,
			'email': self.email_input,
			'phone': self.phone_input
		}

	def set_value(self, input_id, value):
		try:
			form_input = self.inputs[input_id]
			form_input.clear()
			form_input.send_keys(value)
		except IndexError:
			raise Exception("Add Employee form: incorrect input index")

	def get_value(self, input_id):
		try:
			form_input = self.inputs[input_id]
			return form_input.get_attribute('value')
		except IndexError:
			raise Exception('Add Employee form: incorrect input index')

	def click_continue(self):
		self.add_button.click()
		# [OPERATION for el in el_list if CONDITION]
		'''WDW(self.driver, 10).until(lambda x:
			for error in self.driver.find_elements_by_id('undefined_helper'): 'Required' in error.text
			or EC.presence_of_element_located((By.CLASS_NAME, 'table_toolbar'))
			) '''
		# give time for error msgs to load
		time.sleep(.4)

