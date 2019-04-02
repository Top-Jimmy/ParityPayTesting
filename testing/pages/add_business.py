from navigation import NavigationFunctions
from page import Page
from components import menu
from components import header
import main

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, ElementNotVisibleException,
	WebDriverException, TimeoutException)
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW


class AddBusinessPage(Page):
	url_tail = 'add-business'
	dynamic = False

	def load(self):
		try:
			# Make sure on map page
			WDW(self.driver, 10).until(lambda x: EC.element_to_be_clickable(
				(By.ID, 'busName')) and self.try_click('busName'))
			self.nav = NavigationFunctions(self.driver)
			self.load_body()
			self.menu = menu.SideMenu(self.driver)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def load_body(self):
		by_class = self.driver.find_element_by_class_name
		self.location_input = self.driver.find_element_by_id('busName')
		self.cant_find_button = by_class('sm-skip-button')

	def add(self, location, option=0, expectedFailure=False):
		if self.select_location(location, option):
			timer = 10
			if expectedFailure: # Don't want to wait full 10 seconds when adding non-US business
				timer = 2
			try:
				WDW(self.driver, timer).until(EC.presence_of_element_located((By.ID, 'agreed')))
				return True
			except Exception as e:
				print('failed to add business')
				return False

	def select_location(self, location, option=0):
		self.type_location(location)
		self.try_hide_keyboard()

		unsetOption = True
		count = 0
		while count < 5:
			try:
				if self.options is not None:
					self.nav.click_el(self.options[option])
					# self.options[option].click()
					try:
						WDW(self.driver, 5).until(EC.element_to_be_clickable(
							(By.CLASS_NAME, 'sm-continue-button')))
						self.click_continue()
						return True
					except TimeoutException:
						# no continue button (i.e. adding non-us business)
						pass
				return False
			except StaleElementReferenceException:
				# Page might have reloaded
				print('Failed to click location option.')
			count += 1

		return False

	def type_location(self, location):
		self.location_input.clear()
		self.location_input.send_keys(location)
		if main.is_ios():
			self.location_input.click()
		# Wait a couple seconds. Sometimes options change as you type
		time.sleep(2)
		# wait up to 5 seconds for options to show up
		presence = EC.presence_of_all_elements_located
		try:
			self.options = WDW(self.driver, 10).until(
				presence((By.CLASS_NAME, 'sm-place-menuitem')))
		except TimeoutException:
			self.options = None

	def num_results(self):
		self.options = (
			self.driver.find_elements_by_class_name("sm-place-menuitem"))
		return len(self.options)

	def click_continue(self):
		try:
			# need to grab <button> for ios web
			find_by = self.driver.find_element_by_class_name
			self.continue_button = find_by('sm-continue-button')
			self.continue_button.click()
			WDW(self.driver, 10).until_not(EC.presence_of_element_located(
				(By.CLASS_NAME, 'sm-continue-button')))
		except (NoSuchElementException, ElementNotVisibleException,
			 WebDriverException) as e:
			pass

	def click_cant_find(self):
		self.cant_find_button.click()
		time.sleep(.2)

	def click_skip(self):
		self.skip_button.click()

	def has_error(self): # page has non-US business error message
		try:
			error_div = self.driver.find_element_by_class_name('alert-danger')
			text = 'sendmi is only available to businesses in the United States.'
			return text == error_div.text
		except NoSuchElementException:
			return False




