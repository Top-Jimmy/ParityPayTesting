from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from page import Page
from components import menu
from components import header
import main
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW

class AdminPage(Page):
	def load(self):
		try:
			self.body = self.load_body()
			self.header = header.PrivateHeader(self.driver)
			self.menu = menu.SideMenu(self.driver, True)
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def load_body(self):
		#self.add_admin_button = self.driver.find_element_by ('')
		self.table_toolbar = self.driver.find_element_by_class_name('table_toolbar')
		self.add_admin_button = self.table_toolbar.find_element_by_class_name('add_admin')
		if main.is_desktop():
			self.table = self.driver.find_element_by_tag_name('table')
			self.table_body = self.table.find_element_by_tag_name('tbody')
			# Wait until admin shows up in table (always at least 1)
			WDW(self.driver, 10).until(
				lambda x: self.table_body.find_elements_by_tag_name('tr') != [])
			self.administrators = self.table_body.find_elements_by_tag_name('tr')
		else:
			WDW(self.driver, 10).until(
				lambda x: self.driver.find_elements_by_class_name('table_entry') != [])
			self.administrators = self.driver.find_elements_by_class_name('table_entry')

	def click_add_admin(self):
		self.add_admin_button.click()

	def get_admin(self, name, info=True):
		"""Given name, return info on administrator"""
		admin = self.get_admin_by_name(name)
		if info:
			return self.get_admin_info(admin)
		else:
			return admin

	def get_admin_by_name(self, name):
		"""Return <tr> element matching given name"""
		if len(self.administrators) > 0:
			for admin in self.administrators:
				#Grabs only the name
				if self.read_perm(admin, 0) == name:
					return admin
		else:
			print('No admins in table')
		return None

	def get_admin_info(self, admin):
		"""Given admin <tr> element, return info on admin"""
		if admin is not None:
			admin_info = {}
			admin_info['name'] = self.read_perm(admin, 0)
			admin_info['members'] = self.read_perm(admin, 1)
			admin_info['org'] = self.read_perm(admin, 2)
			return admin_info
		return None

	def read_perm(self, admin, col_index):
		# 0: name, 1: manage employees, 2: manage business
		el = self.get_admin_el(admin, col_index)

		if col_index == 0: # return name of admin
			if main.is_desktop():
				return el.text
			else:
				#print(':' + str(el.text[6:]))
				return el.text[6:]
		else: # return whether admin has permission or not
			try:
				svg = el.find_element_by_tag_name('svg')
				return True
			except NoSuchElementException:
				return False

	def get_admin_el(self, admin, col_index):
		try:
			if main.is_desktop():
				el = admin.find_elements_by_tag_name('td')[col_index]
			else:
				el = admin.find_elements_by_class_name('table_entry_row')[col_index]
			return el
		except (NoSuchElementException, IndexError) as e:
			return None

	def num_admins(self):
		return len(self.administrators)

	def click_admin(self, name):
		admin = self.get_admin(name, False)
		if admin is not None:
			#Must click text on mobile. Extend hitbox to left edge?
			if not main.is_desktop():
				admin = admin.find_elements_by_class_name('table_entry_row')[0]
			self.move_to_el(admin)
		else:
			print('could not find admin with name: ' + name)

class AddAdminPage(Page):
	def load(self):
		try:
			self.body = self.load_body()
			self.header = header.PrivateHeader(self.driver)
			self.menu = menu.SideMenu(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			#print(str(e) + '\n')
			return False

	def load_body(self):
		self.new_invite_tab = self.driver.find_element_by_id('admin_new')
		self.existing_invite_tab = self.driver.find_element_by_id('admin_existing')
		self.load_form()
		self.send_button = self.driver.find_element_by_class_name('primaryButton')

	def load_form_new(self):
		self.form = self.driver.find_element_by_tag_name('form')
		inputs = self.form.find_elements_by_tag_name('input')
		self.first_name = inputs[0]
		self.last_name = inputs[1]
		self.dob = inputs[2]
		self.zipcode = inputs[3]
		self.email = inputs[4]
		self.phone = inputs[5]

	def load_form_existing(self):
		# list will have length of 0 if you are only employee
		WDW(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'existing_employee')))
		self.employees = self.driver.find_elements_by_class_name('existing_employee')
		self.search = self.driver.find_element_by_id('find_existing_employee')

	def load_form(self):
		try:
			self.load_form_new()
		except (NoSuchElementException, StaleElementReferenceException,
			IndexErrorException)as e:
			self.load_form_existing()
		except Exception as e:
			print e

	def current_tab(self):
		"""Determine selected tab by background color"""
		selected = "rgba(56, 217, 244,"
		if selected in self.new_invite_tab.value_of_css_property('color'):
			return 'new'
		elif selected in self.existing_invite_tab.value_of_css_property('color'):
			return 'existing'
		raise Exception("Unexpected tab behavior")

	def click_existing(self):
		try:
			# raw_input('about to click invite tab')
			self.existing_invite_tab.click()
			# raw_input('clicked invite tab')
			# Wait for search input
			WDW(self.driver, 10).until(
				EC.element_to_be_clickable((By.ID, 'find_existing_employee')))
			# raw_input('found search')
			self.load_form_existing()
		except Exception as e:
			print e
			raise e

	def click_new(self):
		try:
			self.load_form_new()
		except Exception as e:
			print e

	def set_first_name(self, first_name):
		self.first_name.clear()
		self.first_name.send_keys(first_name)

	def set_last_name(self, last_name):
		self.last_name.clear()
		self.last_name.send_keys(last_name)

	def set_dob(self, dob):
		self.dob.clear()
		self.dob.send_keys(dob)

	def set_zip(self, zipcode):
		self.zipcode.clear()
		self.zipcode.send_keys(zipcode)

	def set_email(self, email):
		self.email.clear()
		self.email.send_keys(email)

	def set_phone(self, phone):
		self.phone.clear()
		self.phone.send_keys(phone)

	def click_send(self):
		self.send_button.click()

	def get_employee_id(self, employee):
		emp_id = employee.find_element_by_tag_name('p').text
		return emp_id

	def get_employee_by_id(self, emp_id):
		if len(self.employees) > 0:
			for employee in self.employees:
				# If Admin-only, no employee ID element
				try:
					if employee.find_element_by_tag_name('p').text == emp_id:
						return employee
				except NoSuchElementException:
					pass
		return None

	def select_employee(self, emp_id):
		employee = self.get_employee_by_id(emp_id)
		if employee is not None:
			self.move_to_el(employee)
		else:
			print('could not find employee with id: ' + emp_id)

