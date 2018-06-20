from page import Page
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction as TA
from selenium.webdriver.common.keys import Keys
import main
from components import header
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW

# 1st page of contact flow. User finds business on map (after entering email on home_page)
# todo: map 'x' button when location is selected and add to test
class ContactMapPage(Page):
	url_tail = '/locate'
	dynamic = True # i.e. contact/14716b91/locate

	def load(self):
		try:
			self.location_input = self.driver.find_element_by_id('busName')
			self.try_load_continue_button()
			self.header = header.PubHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def try_load_continue_button(self):
		try:
			find_by = self.driver.find_element_by_class_name
			# self.continue_button = (
			# find_by("sm-continue-button").find_element_by_tag_name('button'))
			self.continue_button = find_by("sm-continue-button")
		except NoSuchElementException:
			self.continue_button = None

	def add(self, location, option=1):
		self.select_location(location, option)
		WDW(self.driver, 10).until(EC.presence_of_element_located(
			(By.CLASS_NAME, 'sm-continue-button')))
		#time.sleep(1)
		self.click_continue()

	def select_location(self, location, option=1):
		self.set_location(location)
		self.options = (
			self.driver.find_elements_by_class_name("sm-place-menuitem"))
		try:
			self.options[option-1].click()
		except IndexError:
			raise Exception("Could not find any google maps search results")

	def set_location(self, location):
		self.location_input.clear()
		self.location_input.send_keys(location)
		if main.is_ios():
			self.location_input.click()

		WDW(self.driver, 10).until(EC.presence_of_element_located(
			(By.CLASS_NAME, 'sm-place-menuitem')))
		#time.sleep(2)

	def click_continue(self):
		# continue button only there when business is selected
		self.try_load_continue_button()
		time.sleep(.4)
		self.click_el(self.continue_button, True)

		# # weird behavior on android. Normal click seems to do nothing.
		# if main.is_android():

		#     main.native_context(self.driver)
		#     css = 'android.widget.Button'
		#     buttons = self.driver.find_elements_by_class_name(css)
		#     TA(self.driver).tap(buttons[2]).perform()
		#     main.webview_context(self.driver)
		# else:
		#     self.continue_button.click()
		#time.sleep(1)
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'comment')))


class ContactFormPage(Page):
	url_tail = '/complete' # '/contact/14716b91/complete'
	dynamic = True

	def load(self):
		try:
			self.load_body()
			self.header = header.PubHeader(self.driver)
			return True
		except (IndexError, NoSuchElementException) as e:
			return False

	def load_body(self):
		self.form = self.load_form()
		find_by = self.form.find_elements_by_tag_name
		find_class = self.form.find_element_by_class_name

		self.name_input = find_by('input')[0]
		self.phone_input = find_by('input')[1]
		self.comment = find_by('textarea')
		# self.continue_button = (
		# 	find_class('primaryButton').find_element_by_tag_name('button'))
		self.continue_button = find_class('primaryButton')

	def load_form(self):
		# on desktop ignore 'sign in' dropdown form
		if main.is_desktop():
			print('got 2nd form')
			return self.driver.find_elements_by_tag_name('form')[1]
		return self.driver.find_element_by_tag_name('form')

	def set_name(self,name):
		self.name_input.clear()
		self.name_input.send_keys(name)
		time.sleep(.4)

	def get_name(self):
		return self.name_input.get_attribute('value')

	def set_phone(self,phone):
		self.phone_input.clear()
		self.phone_input.send_keys(phone)
		time.sleep(.4)

	def get_phone(self):
		return self.phone_input.get_attribute('value')

	def set_comment(self,comment):
		self.comment.clear()
		self.comment.send_keys(comment)
		time.sleep(.4)

	def get_comment(self):
		return self.comment.get_attribute('value')

	def click_continue(self):
		# Desktop chrome throws error if you try to click disabled button
		# Parent div will capture click
		if self.continue_button.is_enabled():
			self.move_to_el(self.continue_button)

	def get_continue_button_status(self):
		if self.continue_button is not None:
			return 'enabled' if self.continue_button.is_enabled() else 'disabled'
		return None
