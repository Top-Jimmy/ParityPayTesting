from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys

from navigation import NavigationFunctions
from page import Page
from components import header
from components import menu
import time


class AddEmployeePage(Page):
	url_tail = 'add-employee'
	dynamic = False

	def load(self):
		try:
			self.nav = NavigationFunctions(self.driver)
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

		self.add_button = find_by('button')[0]
		self.inputs = {
			'first_name': find_by('input')[0],
			'last_name': find_by('input')[1],
			'employee_id': find_by('input')[2],
			'dob': find_by('input')[3],
			'zip_code': find_by('input')[4],
			'email': find_by('input')[5],
			'phone': find_by('input')[6],
		}

	def set_value(self, input_id, value):
		try:
			form_input = self.inputs[input_id]
			self.nav.set_input(form_input, value)
			# form_input.clear()
			# form_input.send_keys(value)
		except IndexError:
			raise Exception("Add Employee form: incorrect input index")

	def get_value(self, input_id):
		try:
			form_input = self.inputs[input_id]
			return form_input.get_attribute('value')
		except IndexError:
			raise Exception('Add Employee form: incorrect input index')

	def click_continue(self):
		self.nav.click_el(self.add_button)
		time.sleep(.4)

