from page import Page
from components import header
import main
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)

# Page for entering phone# when responding to invite or enrolling business

class EnrollFactor2Page(Page):
	url_tail = 'accept/factor2' # (respond to invite)
	# OR 'enroll-business/factor2' (enroll business)
	# will reload w/ something like enroll-business/factor2?shortCode=46704

	def load(self):
		try:
			self.load_body()
			# load header after body. Issues trying to load page
			self.header = header.PubHeader(self.driver)
			# # raw_input('loaded header')
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			WebDriverException) as e:
			#print(str(e) + '\n' + 'Exception on accept/factor2')
			return False

	def load_body(self):
		# IDS: need id on form
		self.form = self.driver.find_element_by_tag_name('form')
		self.why_button = self.form.find_element_by_tag_name('a')
		self.contact_input = self.form.find_element_by_tag_name('input')
		self.try_load_country_select()
		self.continue_button = self.form.find_element_by_class_name('primaryButton')

	def try_load_country_select(self):
		self.country_select = self.form.find_element_by_id('country_dropdown')
		#generating exception here, no such element.
		try:
			self.us = self.country_select.find_elements_by_tag_name('option')[0]
			self.mx = self.country_select.find_elements_by_tag_name('option')[1]
		except IndexError:
			self.us = None
			self.mx = None

	def click_why(self):
		self.why_button.click()

	def set_contact(self, infos):
		# input for entering email or phone
		# (depending on which one you entered previously)
		self.contact_input.clear()
		self.contact_input.send_keys(infos)

	def get_contact(self):
		return self.contact_input.get_attribute('value')

	def enter_contact(self,infos):
		self.set_contact(infos)
		self.click_continue()

	def select_mobile_location(self,location):
		self.country_select.click()
		time.sleep(.4)
		if location.lower() == 'united states' or location.lower() == 'us':
			self.us.click()
		elif location.lower() == 'mexico' or location.lower() == 'mx':
			self.mx.click()
		# not sure if select element needs to be reloaded after value is changed
		self.load_country_select()

	def click_continue(self):
		self.continue_button.click()



