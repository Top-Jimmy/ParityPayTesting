# coding: utf-8
from page import Page
from components import menu
from components import header
from navigation import NavigationFunctions
import main

import time
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

# WDW find element: class = sm-employee-table

# loading
# employee functions
# add menu functions
# filter functions
# sort functions
# general functions

class EmployeePage(Page):
	url_tail = 'employees'
	dynamic = False
	debug = False

#################################### Loading ##################################

	def load(self):
		try:
			WDW(self.driver, 10).until(lambda x:
				EC.presence_of_element_located((By.CLASS_NAME, 'sm-employee-table')) or
				EC.presence_of_element_located((By.CLASS_NAME, 'employeeDiv'))
				)
			self.nav = NavigationFunctions(self.driver)
			self.load_body()
			if EmployeePage.debug:
				raw_input('1')
			self.header = header.PrivateHeader(self.driver)
			if EmployeePage.debug:
				raw_input('2')
			self.menu = menu.SideMenu(self.driver, True)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_body(self):
		# employees, add button, filter toggle, search input

		# this line might fail if you're actually on account page (IndexError)
		# Other inputs exist if filter options are visible
		self.search_input = self.driver.find_elements_by_tag_name('input')[0]
		find_by = self.driver.find_element_by_class_name
		if EmployeePage.debug:
				raw_input('3')
		self.employees = self.load_employees()
		if EmployeePage.debug:
				raw_input('4')
		self.add_button = self.driver.find_element_by_id('fab_button')
		self.filter_button = (
			self.driver.find_element_by_class_name('filter_toggle'))
		if EmployeePage.debug:
				raw_input('5')
		self.filter_pane = self.driver.find_element_by_class_name(
			'ReactCollapse--collapse')
		if EmployeePage.debug:
				raw_input('6')
		self.try_load_filter_opts()
		if EmployeePage.debug:
				raw_input('7')
		self.try_load_sort_opts()
		if EmployeePage.debug:
				raw_input('8')

	def load_employees(self):
		# Should always be at least 1 entry in table.
		# Fail to load page if cant find any
		if main.is_desktop(): # return table row elements
			find_by = self.driver.find_element_by_class_name
			css = 'sm-employee-table'
			table = find_by(css)
			employees = table.find_elements_by_tag_name('tr')[1:]
		else:               # return employee entry elements
			employees = self.driver.find_elements_by_class_name('employeeDiv')
		if len(employees) == 0:
			raise NoSuchElementException("Couldn't find employees in table.")
		return employees

	def try_load_filter_opts(self):
		"""Only visible when filter button is toggled"""
		opts = [None]*5
		if self.filters_open():
			try:
			# possibly need to grab child of each opt for ios
				opts[0] = self.driver.find_element_by_id('filter_invited')
				opts[1] = self.driver.find_element_by_id('filter_inactive')
				opts[2] = self.driver.find_element_by_id('filter_active')
				opts[3] = self.driver.find_element_by_id('filter_removed')
				opts[4] = self.driver.find_element_by_id('filter_terminated')
			except NoSuchElementException:
				pass
		self.filter_opts = opts

	def try_load_sort_opts(self):
		# desktop: grab <th> els from first table
		# mobile: page inputs (if visible)
		opts = [None]*5
		if main.is_desktop():
			t = self.driver.find_elements_by_class_name('sm-employee-table')
			opts = t[0].find_elements_by_tag_name('th')
		elif self.filters_open():
			# Mobile: only there when filters are open
			opts[0] = self.driver.find_element_by_id('sort_first_name')
			opts[1] = self.driver.find_element_by_id('sort_employee_id')
			opts[2] = self.driver.find_element_by_id('sort_state')
			opts[3] = self.driver.find_element_by_id('sort_elect_amount')
			opts[4] = self.driver.find_element_by_id('sort_modified')
		self.sort_opts = opts

	def load_participate_dialog(self):
		try:
			buttons = self.driver.find_elements_by_tag_name('button')
			self.participate = buttons[-2]
			self.skip = buttons[-1]
			# IDs not pushed to test server yet.
			# self.participate = self.driver.find_element_by_id("newBus_participate")
			# self.skip = self.driver.find_elements_by_id("newBus_skip")
			return True
		except NoSuchElementException:
			self.participate = None
			self.skip = None
			return False

	def handle_participate_dialog(self, action='skip'):
		self.load_participate_dialog()
		if self.participate is not None:
			if action == 'participate':
				self.participate.click()
			else:
				self.skip.click()
				time.sleep(1)
		else:
			print('No participate dialog found')

########################### Employee/Table functions ##########################

	def num_employees(self):
		return len(self.employees)

	def get_employee(self, find_by, identifier, get_info=True):
		""" find_by: 'index', 'name', 'id'
			identifier: string
			get_info: True=return employee data, False=return employee element
		"""
		emp = None
		if find_by == 'index':
			emp = self.employees[int(identifier)]
		elif find_by == 'name':
			emp = self.get_emp_by_name(identifier)
		elif find_by == 'id':
			emp = self.get_emp_by_id(identifier)

		if emp is None:
			return None
		elif get_info:
			return self.get_emp_data(emp)
		else:
			return emp

	def get_emp_by_name(self,name):
		for employee in self.employees:
			find_by = employee.find_elements_by_tag_name
			if main.is_desktop():
				text = find_by('td')[0].text
			else:
				text = find_by('div')[2].text

			# raw_input(text)
			if text == name:
				#print('found employee: ' + name)
				return employee
		return None

	def get_emp_by_id(self,emp_id):
		for employee in self.employees:
			find_by = employee.find_elements_by_tag_name
			# print(employee.text)
			tds = find_by('td')
			# raw_input('# tds: ' + str(len(tds)))

			if main.is_desktop():
				el = find_by('td')[1]
				text = el.text
			else:
				el = find_by('div')[3]
				text = str(el.text)[13:]

			if text == emp_id:
				return employee
		return None

	def get_emp_data(self,employee):
		""" given employee div, parse text and return employee dict """
		emp = None
		find_by = employee.find_elements_by_tag_name
		if str(type(employee)) != "<type 'NoneType'>" and main.is_desktop():
			# columns = employee.find_elements_by_tag_name("td")
			emp = {
				'name': find_by('td')[0].text,
				'id': find_by('td')[1].text,
				'status': find_by('td')[2].text,
				'election': find_by('td')[3].text,
				'date_changed': find_by('td')[4].text
			}
		elif str(type(employee)) != "<type 'NoneType'>":
			emp = {
				'name': find_by('div')[2].text,
				'id': find_by('div')[3].text[13:],
				'status': find_by('div')[4].text[8:], #Fail 4:20p, StaleEl
				'election': find_by('div')[5].text[17:], #Fail 4:15p, StaleEl
				'date_changed': find_by('div')[6].text[14:]
			}

		# raw_input(str(emp))
		return emp

	def employee_menu(self, find_by, identifier, command_text='click'):
		"""Find employee, 'click': just open menu, 'reinvite', 'remove' """
		emp = self.get_employee(find_by, identifier, False)
		try:
			emp_menu = emp.find_element_by_tag_name('button')
			# move to emp. click toast (if visible)
			self.nav.click_el(emp_menu)
			# AC(self.driver).move_to_element(emp).perform()
			time.sleep(.2)
			self.click_toast()
			time.sleep(.2)

			# open emp menu, click action matching command_text
			self.move_to_el(emp_menu)
			time.sleep(.4)
			if command_text != 'click':
				class_name = "{command}_employee".format(command=command_text.lower())
				option = self.driver.find_element_by_class_name(class_name)
				option.click()
				WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'confirm_remove')))
				if command_text.lower() == 'remove':
					self.load_remove_form()
		except NoSuchElementException:
			print('something went wrong in employee_menu()')

	def load_reinvite_form(self):
		# shouldn't have invites in table anymore
		pass
		# self.reinvite_cancel_button = (
		# 	self.driver.find_element_by_xpath("//span[text() = 'Cancel']")
		# )
		# self.reinvite_ok_button = (
		# 	self.driver.find_element_by_xpath("//span[text() = 'OK']")
		# )

	def cancel_reinvite(self):
		self.reinvite_cancel_button.click()

	def reinvite(self):
		self.reinvite_ok_button.click()
		time.sleep(1)

	def load_remove_form(self):
		self.remove_select_cont = self.driver.find_element_by_id('remove_select')
		self.remove_select = (
			self.remove_select_cont.find_elements_by_tag_name('div')[2])
		self.remove_cancel_button = (
			self.driver.find_element_by_class_name('cancel_remove')
		)
		self.remove_remove_button = (
			self.driver.find_element_by_class_name('confirm_remove')
		)

	def select_remove_new_status(self, new_status):
		self.remove_select.click()
		time.sleep(1)
		action = AC(self.driver)
		action.send_keys(new_status)
		action.send_keys(Keys.ENTER)
		action.perform()

	def remove_employee(self, find_by, identifier, remove=True):
		self.employee_menu(find_by, identifier, 'Remove')
		time.sleep(.2)
		self.remove_remove_button.click()

		# Table redraws after removing someone. Wait for first employee to go stale
		try:
			WDW(self.driver, 10).until(EC.staleness_of(self.employees[0]))
		except (WebDriverException, NoSuchElementException,
			StaleElementReferenceException) as e:
			# employee element probably already gone
			pass

		# Wait for table to redraw
		if main.is_desktop():
			WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sm-employee-table')))
		else:
			WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'employeeDiv')))

		# Should be good to go. Load page
		self.load()

	def click_employee(self, find_by, identifier):
		emp = self.get_employee(find_by,identifier,False)
		if emp is None:
			print('no employee found')
			return False
		else:
			if main.is_ios(): # ios needs to click a child div (not menu div)
				emp = emp.find_elements_by_tag_name('div')[3]
			#elif main.is_desktop():
			#	emp = emp.find_elements_by_tag_name('td')[1]
			self.click_toast()
			# move_to_el handles navigating to employee and clicking
			self.move_to_el(emp) # emp.click()
			time.sleep(.4)
			return True

############################ Add Employee Functions ###########################

	def click_plus(self):
		self.add_button.click()
		time.sleep(.4)
		try:
			find_by = self.driver.find_element_by_id
			self.add_employee_button = find_by('add_employee')
			# only has multiple employees option on desktop
			if main.is_desktop():
				self.add_multiple_employees = find_by('add_employees')
		except NoSuchElementException:
			fail = 1 + '2'
			# problem if these elements don't exist

	def click_add_employee(self):
		self.add_employee_button.click()

	def click_add_multiple_employees(self):
		self.add_multiple_employees.click()

################################## Filter Functions ###########################

	def filters_open(self):
		# are filter options visible on page?

		return self.filter_pane.size['height'] != 0
		# Filters always drawn on page, tucked in zero-height el when not shown.
		# BUG: May return True, where should be False, if filter options pane is closing, but not closed.

	def filter_is_active(self, index):
		# self.filter_opts[index].find_element_by_xpath("parent::*")
		prop = 'background-color'
		color = 'rgba(56, 217, 244, 1)'
		el = self.filter_opts[index].find_elements_by_tag_name('div')[0]
		# raw_input('bg: ' + el.value_of_css_property(prop))
		return el.value_of_css_property(prop) == color

	def toggle_filter(self):
		"""Click element to hide/show filter options"""
		#print('toggling filter')
		self.filter_button.click()
		#WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'filter_terminated')))
		time.sleep(1)
		# update filter/sort options
		self.try_load_filter_opts()
		if not main.is_desktop():
			self.try_load_sort_opts()
		#raw_input('what happening?')
		time.sleep(1)

	def set_filter(self, pattern):
		"""toggle individual filter (int), or apply pattern (list)"""

		# make sure filter options visible
		if not self.filters_open():
			self.toggle_filter()

		if type(pattern) is int:
			self.filter_opts[pattern].click()
		elif type(pattern) is list:
			current_filter = self.get_filters()
			for i in xrange(len(pattern)):
				if (pattern[i] != current_filter[i]):
					self.filter_opts[i].click()
					time.sleep(.4)

		time.sleep(1) #Can't get a WDW condition to load correctly.
		WDW(self.driver, 20).until(lambda x:
			EC.visibility_of_element_located((By.TAG_NAME, 'tr'))
			or EC.visibility_of_all_elements_located((By.CLASS_NAME, 'employeeDiv'))
			)
		self.load()

	def get_filters(self):
		filters = [None]*5
		for i, filt in enumerate(self.filter_opts):
			if self.filter_is_active(i):
				filters[i] = 1
			else:
				filters[i] = 0
		return filters

################################ Sort Functions ###############################

	def get_active_sort(self):
		if main.is_desktop():
			return self.get_active_desktop_sort()
		else:
			return self.get_active_web_sort()

	def get_active_desktop_sort(self):
		"""return index in self.sort_opts that is currently active"""
		# non-active options have opacity of 0.2
		for i in xrange(5):
			# raw_input(str(i))
			arrow_el = (
				self.sort_opts[i].find_element_by_tag_name("svg")
			)
			opacity = arrow_el.value_of_css_property("opacity")
			if opacity != "0.2":
				return i
		return None

	def get_active_web_sort(self):
		"""Return index in self.sort_opts that is currently active"""
		# ensure sort options are visible
		if not main.is_desktop() and not self.filters_open():
		#if main.is_desktop() is not True and self.filters_open() is False:
			self.toggle_filter()

		# return index of sort opt that has active color
		for i, opt in enumerate(self.sort_opts):
			prop = 'background-color'
			color = 'rgba(56, 217, 244, 1)'
			if opt.value_of_css_property(prop) == color:
				return i

	def get_sort_direction(self):
		"""Determine index of current sort setting.
			return True if sort is normal, False if reverse"""
		direction = True
		if main.is_desktop():
			active_index = self.get_active_desktop_sort()
			arrow_el = (
				self.sort_opts[active_index].find_element_by_tag_name("path")
			)
			path = arrow_el.get_attribute('d')
			if path == "M7 14l5-5 5 5z":   # vs "M7 10l5 5 5-5z" for normal
				direction = False
		else:
			direction = self.get_mobile_sort_direction()
		return direction

	def get_mobile_sort_direction(self):
		"""Return opposite of reverse order checkbox selected status"""
		if not self.filters_open():
			self.toggle_filter()

		# should be 2 inputs. Search, reverse checkbox
		reverse_order_checkbox = (
			self.driver.find_elements_by_tag_name('input')[1])
		return not reverse_order_checkbox.is_selected()

	def get_sort(self):
		column = self.get_active_sort()
		direction = self.get_sort_direction()
		return [column, direction]

	def click_sort(self, index):
		self.sort_opts[index].click()
		time.sleep(.2)

	def get_first_emp(self):
		self.load()
		return self.get_employee('index', 0)

	def set_sort(self, index, direction=True):
		# open sort options if not visible (always vis on desktop)
		# Index: 0=name, 1=ID, 2=Status, 3=election 4=date changed
		if not main.is_desktop() and not self.filters_open():
			self.toggle_filter()

		cur_sort = self.get_sort()
		old_first_emp = self.get_first_emp()
		#first_emp = self.get_employee('index', 0)

		if cur_sort[0] != int(index) or cur_sort[1] != direction:
			if cur_sort[0] != int(index):
				self.click_sort(index)
				cur_sort = self.get_sort()

			if cur_sort[1] != direction:
				self.reverse_sort(cur_sort[0])

		#raw_input('waiting on...?')
		#giving time for page to update. WDW until old_first_el != first_el and first_el is not None?
			time.sleep(2)
			'''WDW(self.driver, 10).until(lambda x:
				EC.presence_of_element_located((By.TAG_NAME , 'tr')) or
				EC.visibility_of_element_located((By.CLASS_NAME ,'employeeDiv'))
				)'''
			#	lambda x : old_first_emp != self.get_first_emp() and self.get_first_emp() is not None
			#	)
		self.load()

	def reverse_sort(self, index):
		"""Desktop: Toggle current sort. Web: Click sort toggle button"""
		if main.is_desktop():
			self.click_sort(index)
		else:
			self.click_sort_toggle()

	def click_sort_toggle(self):
		reverse_order_checkbox = (
			self.driver.find_elements_by_tag_name('input')[1])
		reverse_order_checkbox.click()

############################### Toast Functions ###############################

	def get_secret_urls(self):
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'testSnackId')))
		self.load()
		elem = self.driver.find_elements_by_class_name("sm-secret-code")
		try:
			email_string = elem[0].text
			try:
				email_url = email_string[0:email_string.index(' => ')]
			except ValueError:
				pass
			email = email_string[email_string.index('email:') + 6:]
		except NoSuchElementException:
			email = None
			email_url = None
		try:
			phone_string = elem[1].text
			phone = phone_string[phone_string.index('phone:') + 6:]
			phone_url = phone_string[0:phone_string.index(' => ')]
		except IndexError:
			phone = None
			phone_url = None
		return {'email': email, 'phone': phone, 'email_url': email_url,
			'phone_url': phone_url}

	def click_toast(self):
		if self.has_toast():
			self.toast.click()
			time.sleep(.4)

	def has_toast(self):
		# is toast visible on page?
		try:
			self.toast = self.driver.find_element_by_id('testSnackId')
			return True
		except NoSuchElementException:
			return False


