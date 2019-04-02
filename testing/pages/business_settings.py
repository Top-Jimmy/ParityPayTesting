from selenium.webdriver.common.keys import Keys
from page import Page
from components import menu
from components import header
from navigation import NavigationFunctions
import time
import main
from selenium.webdriver import ActionChains as AC
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, TimeoutException)
from selenium.webdriver.support.ui import WebDriverWait

class BusinessSettingsPage(Page):
	url_tail = 'business-settings'
	dynamic = False

	def load(self):
		try:
			self.nav = NavigationFunctions(self.driver)
			self.load_body()
			self.header = header.PrivateHeader(self.driver)
			self.menu = menu.SideMenu(self.driver)
			if main.is_web() and main.is_ios():
				self.clear_ios_footer()
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def load_body(self):
		self.form = self.driver.find_element_by_tag_name('form')
		self.load_business_name()
		self.load_dba()
		self.load_ein()
		self.load_hr()
		self.load_phone()
		self.load_website()

		self.load_address()
		self.remove_button = (
			self.driver.find_element_by_class_name('removeButton'))

	def load_business_name(self):
		cont = self.driver.find_element_by_id('busName_cont')
		# Android native: grab parent of input
		# else: grab input
		# if main.is_android() and not main.is_web():
		# 	self.business_name_input = cont.find_elements_by_tag_name('div')[1]
		# else:
		self.business_name_input = cont.find_element_by_tag_name('input')

	def load_dba(self):
		cont = self.driver.find_element_by_id('dba_cont')
		# if main.is_android() and not main.is_web():
		# 	self.dba_input = cont.find_elements_by_tag_name('div')[1]
		# else:
		self.dba_input = cont.find_element_by_tag_name('input')

	def load_ein(self):
		cont = self.driver.find_element_by_id('ein_cont')
		# if main.is_android() and not main.is_web():
		# 	self.ein_input = cont.find_elements_by_tag_name('div')[1]
		# else:
		self.ein_input = cont.find_element_by_tag_name('input')

	def load_hr(self):
		cont = self.driver.find_element_by_id('hr_cont')
		# if main.is_android() and not main.is_web():
		# 	self.hr_email_input = cont.find_elements_by_tag_name('div')[1]
		# else:
		self.hr_email_input = cont.find_element_by_tag_name('input')

	def load_phone(self):
		cont = self.driver.find_element_by_id('phone_cont')
		# if main.is_android() and not main.is_web():
		# 	self.phone_input = cont.find_elements_by_tag_name('div')[1]
		# else:
		self.phone_input = cont.find_element_by_tag_name('input')

	def load_website(self):
		cont = self.driver.find_element_by_id('website_cont')
		# if main.is_android() and not main.is_web():
		# 	self.website_input = cont.find_elements_by_tag_name('div')[1]
		# else:
		self.website_input = cont.find_element_by_tag_name('input')

	def load_address(self):
		find_by_id = self.form.find_element_by_id
		# line1, line2, city, state, zip
		self.line1_input = find_by_id('recipient_line1')
		self.line2_input = find_by_id('recipient_line2')
		self.city_input = find_by_id('recipient_city')
		self.state_cont = self.form.find_element_by_class_name('state_dropdown')
		self.state_dd = self.state_cont.find_elements_by_tag_name('div')[3]
		self.postal_code_input = find_by_id('recipient_code')

		# cont = self.driver.find_element_by_id('zip_cont')
		# if main.is_android() and not main.is_web():
		# 	self.postal_code_input = cont.find_elements_by_tag_name('div')[1]
		# else:
		# 	self.postal_code_input = cont.find_element_by_tag_name('input')

	def clear_ios_footer(self):
		# scroll down a little bit to lose ios browser footer. Scroll back to top
		self.ios_scroll('down',100)
		self.scroll_to_top()
		time.sleep(1)

	def set_state(self, state):
		if self.state_dd.tag_name != 'input':
			self.nav.click_el(self.state_dd)
			time.sleep(1)
			ActionChains(self.driver).send_keys(state).perform()
			ActionChains(self.driver).send_keys(Keys.ENTER).perform()
			time.sleep(1)
		else:
			self.state_dd.clear()
			self.state_dd.send_keys(state)

	# select state by typing keys, then selecting state by pressing enter
	def type_state(self,state):
		ActionChains(self.driver).move_to_element(self.state_dd).perform()
		self.nav.click_el(self.state_dd)
		time.sleep(1.4) # wait before sending keys
		ActionChains(self.driver).send_keys(state).perform()
		time.sleep(.4)
		ActionChains(self.driver).send_keys(Keys.ENTER).perform()

	def set(self, name, value):
		"""Set text of input element with given name"""
		# don't use for setting state. Use type_state() or set_state()
		el = self.get_el(name)
		# AC(self.driver).move_to_element(el).perform()
		# time.sleep(.6)
		# autosave causes issues if you don't use clear_input() instead of clear()
		# self.clear_input(el)
		self.nav.set_input(el, value)

	def get_el(self, name):
		"""Return input element given name. None if invalid name"""
		if name == 'business_name':
			return self.business_name_input
		elif name == 'dba':
			return self.dba_input
		elif name == 'ein':
			return self.ein_input
		elif name == 'hr_email':
			return self.hr_email_input
		elif name == 'line1':
			return self.line1_input
		elif name == 'line2':
			return self.line2_input
		elif name == 'city':
			return self.city_input
		elif name == 'postal_code':
			return self.postal_code_input
		elif name == 'phone':
			return self.phone_input
		elif name == 'website':
			return self.website_input
		elif name == 'state':
			return self.state_cont
		else:
			return None

	def get(self, name):
		"""Given name, return the value of element"""
		el = self.get_el(name)
		if el is not None:
			# State: return text (not label text) Else: return input value
			if name == 'state':
				div = el.find_elements_by_tag_name('div')[0]
				return div.text
			return el.get_attribute('value')
		return None

	def remove_business(self, code):
		self.click_remove()
		self.set_remove_code(code)
		self.click_confirm_remove()

	def click_remove(self):
		"""Click 'remove' button, then load elements in confirmation popup"""
		self.nav.dismiss_keyboard() # Hide keyboard first. Otherwise you won't be at bottom of page
		self.scroll_to_bottom()
		self.remove_button = (
			self.driver.find_element_by_class_name('removeButton'))
		self.nav.click_el(self.remove_button, True)
		time.sleep(1)
		self.try_load_remove_popup()

	def try_load_remove_popup(self):
		try:
			self.confirm_code_input = (
				self.driver.find_element_by_id('removeBusCode'))
			buttons = self.driver.find_elements_by_tag_name('button')
			self.cancel_remove_button = (
				self.driver.find_element_by_class_name('remove_business_cancel'))
			self.confirm_remove_button = (
				self.driver.find_element_by_class_name('remove_business_ok'))
		except NoSuchElementException:
			self.confirm_code_input = None
			self.cancel_remove_button = None
			self.confirm_remove_button = None

	def click_cancel_remove(self):
		self.nav.click_el(self.cancel_remove_button)

	def click_confirm_remove(self):
		if main.is_android():
			self.try_hide_keyboard()
			time.sleep(.4)
		self.move_to_el(self.confirm_remove_button)
		time.sleep(2)

	def set_remove_code(self, code):
		self.confirm_code_input.clear()
		self.confirm_code_input.send_keys(code)
		if main.is_ios(): # send_keys doesn't seem to update react component.
			self.confirm_code_input.send_keys('')

	def confirm_remove_button_enabled(self):
		"""Does confirm remove button exist and is it enabled?"""
		if self.confirm_remove_button is None:
			return False
		return self.confirm_remove_button.is_enabled()

	def saved(self):
		"""Determines if the form is valid"""
		try:
			WebDriverWait(self.driver, 6).until_not(
				lambda x: x.find_element_by_class_name('uil-ring-css'))
			return True
		except TimeoutException:
			return False

