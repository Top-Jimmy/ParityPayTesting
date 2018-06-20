from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as AC
from page import Page
from components import menu
from components import header
import time
import main
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW

class EmployeeViewPage(Page):
	url_tail = "employee/" #i.e. https://ppay11.herokuapp.com/employee/ead0ade1
	dynamic = True

	def load(self):
		try:
			self.admin_options = ['none', 'manager', 'executive']
			self.load_tabs()
			if self.selected_tab == 'info':
				self.load_information()
					# employee_name
					# edit_button
					# employee_id
					# enroll_date
					# status
					# election
					# edit form
				# print('loaded info')
			elif self.selected_tab == 'history':
				self.load_history()
					# Table with entries
						# election_amt
						# election_date
						# election_pdf
				# print('loaded history')
			elif self.selected_tab == 'permissions':
				self.load_permissions()
					# admin_radios
				# print('loaded perms')
			self.menu = menu.SideMenu(self.driver)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
				WebDriverException) as e:
			#print(str(e))
			return False

	def is_editing(self):
		try:
			el = self.driver.find_element_by_class_name('sm-employee-edit-form')
			return True
		except NoSuchElementException:
			return False

	def load_tabs(self):
		# elements always visible
		find_by = self.driver.find_element_by_id

		self.info_tab = self.driver.find_element_by_id("employee_info")
		self.permissions_tab = self.driver.find_element_by_id("employee_permissions")

		# history tab does not exist for admin only users
		try:
			self.history_tab = self.driver.find_element_by_id("employee_history")
		except NoSuchElementException:
			self.history_tab = None

		self.selected_tab = self.current_tab()
		# if all(x != None for x in (self.info_tab, self.history_tab)): #self.edit_button,self.employee_name)):
		# 	return True
		# else:
		# 	return False

	# def load_tabs(self):
	# 	# These should always be visible on employee_view page.
	# 	self.info_tab = self.driver.find_element_by_id("employee_info")
	# 	self.history_tab = self.driver.find_element_by_id("employee_history")
	# 	self.permissions_tab = self.driver.find_element_by_id("employee_permissions")
	# 	# try:
	# 	# 	self.info_tab = self.driver.find_element_by_id("employee_info")
	# 	# except (NoSuchElementException, StaleElementReferenceException) as e:
	# 	# 	self.info_tab = None
	# 	# 	print('Failed to load info tab. \n' + str(e))
	# 	# 	return False
	# 	# try:
	# 	# 	self.history_tab = self.driver.find_element_by_id("employee_history")
	# 	# except (NoSuchElementException, StaleElementReferenceException) as e:
	# 	# 	self.history_tab = None

	# 	# try:
	# 	# 	self.permissions_tab = self.driver.find_element_by_id("employee_permissions")
	# 	# except NoSuchElementException:
	# 	# 	self.permissions_tab = None
	# 	# except Exception as e:
	# 	# 	print(str(e))
	# 	# 	return False
	# 	# return True

########################## INFORMATION TAB ###############################

	def load_information(self):
		if self.is_editing():
			self.load_edit_form()
				# id_input
				# name_inputs (first/last)
				# save button
		else:
			self.body = self.driver.find_element_by_tag_name('section')
			self.employee_name = self.try_load_name()
			self.edit_button = self.try_load_edit()
			self.load_default()

	def try_load_edit(self):
		try:
			return self.body.find_element_by_tag_name('button')
		except NoSuchElementException:
			return None

	def try_load_name(self):
		try:
			return self.driver.find_element_by_tag_name("h1")
		except NoSuchElementException:
			return None

	def load_default(self):
		# visible when not editing
		self.info_table = self.try_load_info_table()
		self.id = self.try_load_id()
		self.status = self.try_load_status()
		#self.admin_role = self.try_load_admin_role()
		self.election = self.try_load_election()
		if all(x != None for x in (self.id,self.status,self.election)) or len(self.info_table.find_elements_by_tag_name('tr')) is 1:
			return True
		else:
			return False

	def try_load_info_table(self):
		try:
			return self.driver.find_element_by_tag_name('tbody')
		except NoSuchElementException:
			return None

	def try_load_id(self):
		try:
			row = self.info_table.find_elements_by_tag_name('tr')[0]
			return row.find_element_by_tag_name('td')
		except NoSuchElementException:
			return None

	def try_load_status(self):
		try:
			row = self.info_table.find_elements_by_tag_name('tr')[2]
			return row.find_element_by_tag_name('td')
		except (NoSuchElementException, IndexError):
			return None

	def try_load_election(self):
		try:
			row = self.info_table.find_elements_by_tag_name('tr')[3]
			return row.find_element_by_tag_name('td')
		except (NoSuchElementException, IndexError):
			return None

	def get_status(self):
		#Doesn't work when editing employee
		return self.status.text

	def load_edit_form(self):
		# elements only visible when editing
		if not self.is_editing():
			#print('not editing?')
			self.edit_form = None
			self.id_input = None
			self.first_name = None
			self.last_name = None
			self.save_changes = None
			return False
		else:
			#print('editing')
			css = 'sm-employee-edit-form'
			self.edit_form = self.driver.find_element_by_class_name(css)
			try:
				self.id_input = self.body.find_elements_by_tag_name('input')[0]
				self.first_name = self.body.find_elements_by_tag_name('input')[1]
				self.last_name = self.body.find_elements_by_tag_name('input')[2]
			except IndexError:
				self.id_input = None
				self.first_name = self.body.find_elements_by_tag_name('input')[0]
				self.last_name = self.body.find_elements_by_tag_name('input')[1]
			except Exception:
				#print(str(e))
				return False
			self.save_changes = self.edit_form.find_element_by_tag_name('button')
			return True

	def edit(self):
		"""Click edit button and return status of loading edit form"""
		if self.current_tab() != 'information':
			self.move_to_el(self.info_tab)
			self.load()

		self.move_to_el(self.edit_button)
		# Look for primary button (will be disabled initally)
		# should always be there no matter what user's role/status is
		WDW(self.driver, 10).until(
			EC.presence_of_element_located((By.CLASS_NAME, 'primaryButton')))
		self.load()

	def set_id(self,new_id):
		if not self.is_editing():
			self.edit()
			#print('clicked edit')
		try:
			self.id_input.clear()
			self.id_input.send_keys(new_id)
			time.sleep(.2)
			return True
		except NameError:
			return False

	def get_id(self):
		# get ID from self.id. self.id_input if editing
		if self.is_editing():
			#print('editing')
			return self.id_input.get_attribute('value')
		else:
			print('not editing')
			return self.id.text

	def set_first_name(self, name):
		if not self.is_editing():
			self.edit()
		try:
			self.first_name.clear()
			self.first_name.send_keys(name)
			time.sleep(.2)
			return True
		except NameError:
			return False

	def get_first_name(self):
		if self.is_editing():
			return self.first_name.get_attribute('value')
		else:
			return self.employee_name.split(' ')[0]

	def set_last_name(self, name):
		if not self.is_editing():
			self.edit()
		try:
			self.last_name.clear()
			self.last_name.send_keys(name)
			time.sleep(.2)
			return True
		except NameError:
			return False

	def get_last_name(self):
		if self.is_editing():
			return self.last_name.get_attribute('value')
		else:
			return self.employee_name.split(' ', 1)[1]
			#Return everything after 1st name (denoted by space)

	def click_save_changes(self):
		"""Click save, load stuff, return True if stuff loads
		return false if not editing, or save button disabled (no changes)"""
		if self.is_editing() and self.save_changes.is_enabled():
			self.save_changes.click()
			WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'primaryButton')))
			return self.load()
			# return self.load_default()
		return False


###################### HISTORY TAB ###############################

	def load_history(self):
		history_table = self.driver.find_element_by_tag_name('table')

	def load_first_entry(self):
		try:
			entry = self.history_table.find_elements_by_tag_name('tr')[0]
			self.election_amt = self.entry.find_elements_by_tag_name('td')[0]
			self.election_date = self.entry.find_elements_by_tag_name('td')[1]
			self.election_pdf = self.entry.find_elements_by_tag_name('td')[2]
			return True
		except Exception as e:
			self.election_amt = None
			self.election_date = None
			self.election_pdf = None
			return False


######################## PERMISSIONS TAB #############################

	def load_permissions(self):
		self.radio_group = self.driver.find_element_by_id('permission_group')
		self.admin_radios = self.radio_group.find_elements_by_tag_name('input')
		#self.admin_none = self.admin_radios.find_elements_by_tag_name('input')[0]
		#self.admin_manager = self.admin_radios.find_elements_by_tag_name('input')[1]
		#self.admin_executive = self.admin_radios.find_elements_by_tag_name('input')[2]

	def try_load_admin_role(self):
		try:
			row = self.info_table.find_elements_by_tag_name('tr')[4]
			td = row.find_element_by_tag_name('td')
			return td.text.lower()
		except NoSuchElementException:
			return None

	def role_to_index(self, admin_role):
		# Return index of radio button given role (none, manager, executive)
		return self.admin_options.index(admin_role)

	def current_radio(self):
		# Return text corresponding to currently selected radio button
		for i, radio in enumerate(self.admin_radios):
			if radio.is_selected():
				return self.admin_options[i]

	def get_admin_role_radio(self):
		# Return admin role according to radio buttons (edit mode)
		return self.current_radio()

	def get_admin_role(self):
		# Return admin role according to text (not editing)
		#click permissions tab, get highlighted radio, translate to role
		self.permissions_tab.click()
		self.load()
		return self.current_radio()
		'''if self.is_editing():
			self.click_edit()
		return self.admin_role'''

	def set_admin_role(self, admin_role):
		# Will not work for yourself (cannot edit own role)
		if self.current_tab() != 'permissions':
			self.permissions_tab.click()
			self.load()
		if admin_role in self.admin_options:
			# permission checkboxes should always be visible now (in the right tab)
			# make sure role checkboxes are visible and above save button
			# if not main.is_desktop():
			# 	self.scroll_to_top() # start at top of page
			# 	el_bottom = self.get_el_location(self.admin_radios[2], 'bottom')
			# 	window_height = self.get_window_height()
			# 	# add 48 for save button (legacy)
			# 	scroll_distance = el_bottom - window_height
			# 	self.move('down', scroll_distance)

			# toggle radio
			# print(self.admin_radios)
			self.admin_radios[self.role_to_index(admin_role)].click()

			# Need some kind of pause to let stuff load or you'll get WebDriverException.
			# Not sure if there's a WDWait that makes sense.
			time.sleep(.4)
		else:
			raise Exception("Unexpected admin role: " + str(admin_role))

	def role_is_editable(self,index):
		return self.admin_radios[index].is_enabled()

	def current_tab(self):
		"""Determine selected tab by background color"""
		selected = "rgba(56, 217, 244,"
		if selected in self.info_tab.value_of_css_property('color'):
			return 'info'
		elif self.history_tab is not None and selected in self.history_tab.value_of_css_property('color'):
			return 'history'
		elif self.permissions_tab is not None and selected in self.permissions_tab.value_of_css_property('color'):
			return 'permissions'
		raise Exception("Unexpected tab behavior!")