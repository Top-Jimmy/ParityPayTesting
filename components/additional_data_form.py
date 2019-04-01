from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from decimal import *
import main
import time
from component import Component
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Info required for sending to ATM: Carrier, phone#, DOB
class AddDataForm(Component):
	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.load_carrier_input()
		self.phone_input = self.driver.find_element_by_id('phone')
		self.dob_input = self.driver.find_element_by_id('birthdate')
		try:
			self.pin_input = self.driver.find_element_by_id('bbvapin')
			print('Should not have bbva pin')
			raise WebDriverException('Should not have bbva pin')
		except NoSuchElementException:
			pass

		self.continue_button = self.driver.find_element_by_id('recipient_additionaldata')
		# Click this to deselect inputs
		self.strong = self.driver.find_element_by_tag_name('strong')

	def load_carrier_input(self):
		el = self.driver.find_element_by_id('phone_carrier')
		# El for clicking and showing dropdown
		self.carrier_click = el.find_elements_by_tag_name('div')[2]
		# El for reading current value out of
		self.carrier_input = el.find_element_by_tag_name('input')

	def try_load_carrier_dd(self):
		# assumes carrier input has already been clicked
		cont = self.driver.find_element_by_id('menu-phone_carrier')
		self.carriers = {
			'movistar': self.driver.find_element_by_id('carrier_01'),
			'at&t': self.driver.find_element_by_id('carrier_iusacell'),
			'telcel': self.driver.find_element_by_id('carrier_telcel')
		}

	def set_carrier(self, carrier):
		if carrier:
			self.load_carrier_input()
			self.carrier_click.click()
			WDW(self.driver, 5).until(EC.element_to_be_clickable(
				(By.ID, 'carrier_01')))
			self.try_load_carrier_dd()
			self.carriers[carrier].click()
			WDW(self.driver, 5).until(EC.invisibility_of_element_located(
				(By.ID, 'carrier_01')))
		return True

	def get_carrier(self):
		# Convert text to 'carrier code'
		carriers = {
			'Movistar / Virgin': 'movistar',
			'AT&T': 'at&t',
			'TELCEL': 'telcel',
		}
		carrier_text = self.carrier_click.text
		print('carrier_text: ' + str(carrier_text))
		return carriers.get(carrier_text, None)

	def set_phone(self, phone):
		try:
			if phone:
				WDW(self.driver, 3).until(EC.element_to_be_clickable((By.ID, 'phone')))
				self.phone_input.click()
				self.phone_input.clear()
				self.phone_input.send_keys(phone)
				self.try_hide_keyboard()
				# Need additional click to get errors to show up
				self.phone_input.click()
				self.try_hide_keyboard()
			else:
				self.phone_input.clear()
				self.phone_input.click()
				self.try_hide_keyboard()
			return True
		except WebDriverException:
			# Not exactly sure why. Often have issues on android. (clicking other elements, etc)
			print('Additional Data form: Driver exception, Failed to set phone')

	def set_dob(self, dob):
		try:
			if dob:
				# if self.dob_input.get_attribute('value') != dob:
				self.dob_input.click()
				self.dob_input.clear()
				self.dob_input.send_keys(dob)
				self.try_hide_keyboard()
				# Need additional click to get errors to show up
				self.dob_input.click()
				self.try_hide_keyboard()
			else: # Set it to nothing
				self.dob_input.clear()
				self.dob_input.click()
				self.try_hide_keyboard()
			return True
		except WebDriverException:
			print('Additional Data form: Driver exception, Failed to set DOB')

	def dob_error(self):
		try:
			errorEl = self.driver.find_element_by_id('birthdate_helper')
			return errorEl.text
		except NoSuchElementException:
			return ''

	def set_info(self, info):
		WDW(self.driver, 10).until(lambda x: self.set_carrier(info['carrier']))
		WDW(self.driver, 10).until(lambda x: self.set_phone(info['phone']))
		WDW(self.driver, 30).until(lambda x: self.set_dob(info['dob']))
		self.try_hide_keyboard()

	def get_info(self):
		info = {
			'carrier': self.get_carrier(),
			'phone': self.phone_input.get_attribute('value'),
			'dob': self.dob_input.get_attribute('value'),
		}
		return info

	def click_continue(self):
		self.move_to_el(self.continue_button)


# Info required for sending to MX bank: DOB
class DOBForm(Component):
	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.dob_input = self.driver.find_element_by_id('birthdate')
		self.continue_button = self.driver.find_element_by_id('recipient_additionaldata')
		# Click this to deselect inputs
		self.strong = self.driver.find_element_by_tag_name('strong')

	def set_dob(self, dob):
		try:
			if dob:
				# if self.dob_input.get_attribute('value') != dob:
				print('clicking 1')
				self.dob_input.click()
				print('clearing')
				self.dob_input.clear()
				print('sending keys: ' + str(dob))
				self.dob_input.send_keys(dob)
				self.try_hide_keyboard()
				# Need additional click to get errors to show up
				print('clicking 2')
				self.dob_input.click()
				self.try_hide_keyboard()
			else: # Set it to nothing
				self.dob_input.clear()
				self.dob_input.click()
				self.try_hide_keyboard()
			return True
		except WebDriverException:
			print('Additional Data form: Driver exception, Failed to set DOB')

	def dob_error(self):
		try:
			errorEl = self.driver.find_element_by_id('birthdate_helper')
			return errorEl.text
		except NoSuchElementException:
			return ''

	def set_info(self, info):
		WDW(self.driver, 30).until(lambda x: self.set_dob(info['dob']))
		self.try_hide_keyboard()

	def get_info(self):
		return self.dob_input.get_attribute('value')

	def click_continue(self):
		self.move_to_el(self.continue_button)
