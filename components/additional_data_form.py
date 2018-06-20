from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from decimal import *
import main
import time
from component import Component
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AddDataForm(Component):
	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		el = self.driver.find_element_by_id('phone_carrier')
		self.carrier_click = el.find_elements_by_tag_name('div')[2]
		self.carrier_input = el.find_element_by_tag_name('input')
		self.phone_input = self.driver.find_element_by_id('phone')
		self.rfc_input = self.driver.find_element_by_id('rfc')
		self.pin_input = self.driver.find_element_by_id('bbvapin')
		self.continue_button = self.driver.find_element_by_id('recipient_additionaldata')
		# Click this to deselect inputs
		self.strong = self.driver.find_element_by_tag_name('strong')

	def try_load_carrier_dd(self):
		# assumes carrier input has already been clicked
		cont = self.driver.find_element_by_id('menu-phone_carrier')
		self.carriers = {
			'movistar': self.driver.find_element_by_id('carrier_01'),
			'iusacell': self.driver.find_element_by_id('carrier_iusacell'),
			'telcel': self.driver.find_element_by_id('carrier_telcel'),
			'unefon': self.driver.find_element_by_id('carrier_unefon'),
			'nextel': self.driver.find_element_by_id('carrier_nextel')
		}

	def set_carrier(self, carrier):
		self.carrier_click.click()
		WDW(self.driver, 3).until(EC.element_to_be_clickable(
			(By.ID, 'carrier_01')))
		self.try_load_carrier_dd()
		self.carriers[carrier].click()
		WDW(self.driver, 3).until(EC.invisibility_of_element_located(
			(By.ID, 'carrier_01')))

	def get_carrier(self):
		# Convert text to 'carrier code'
		carriers = {
			'Movistar / Virgin': 'movistar',
			'IUSACELL (AT&T)': 'iusacell',
			'TELCEL': 'telcel',
			'UNEFON (AT&T)': 'unefon',
			'NEXTEL (AT&T)': 'nextel'
		}
		return carriers[self.carrier_click.text]

	def set_phone(self, phone):
		WDW(self.driver, 3).until(EC.element_to_be_clickable((By.ID, 'phone')))
		self.phone_input.click()
		self.phone_input.clear()
		self.phone_input.send_keys(phone)
		# Need additional click to get errors to show up
		self.phone_input.click()

	def set_rfc(self, rfc):
		WDW(self.driver, 3).until(EC.element_to_be_clickable((By.ID, 'rfc')))
		self.rfc_input.clear()
		self.rfc_input.send_keys(rfc)
		# To get error messages to show up...
		if main.is_android():
			self.try_hide_keyboard()
			self.scroll_to_top()
			self.strong.click()
		elif main.is_ios():
			self.rfc_input.click()
			self.phone_input.click()
			self.try_hide_keyboard()

	def set_pin(self, pin):
		WDW(self.driver, 3).until(EC.element_to_be_clickable((By.ID, 'bbvapin')))
		self.pin_input.clear()
		self.pin_input.send_keys(pin)
		self.try_hide_keyboard()
		self.pin_input.click()

	def set_info(self, info):
		self.set_carrier(info['carrier'])
		self.set_phone(info['phone'])
		self.set_rfc(info['rfc'])
		self.set_pin(info['pin'])
		self.try_hide_keyboard()

	def get_info(self):
		info = {
			'carrier': self.get_carrier(),
			'phone': self.phone_input.get_attribute('value'),
			'rfc': self.rfc_input.get_attribute('value'),
			'pin': self.pin_input.get_attribute('value')
		}
		return info

	def click_continue(self):
		self.move_to_el(self.continue_button)