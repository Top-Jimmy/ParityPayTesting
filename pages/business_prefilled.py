from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, TimeoutException, WebDriverException)
from page import Page
from components import menu
from components import header
import time
from selenium.webdriver import ActionChains as AC
import main
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Different from business_details.py
# Get to page by adding a business, typing in info, selecting from options, and clicking "Continue".

class BusinessPrefilledPage(Page):
	url_tail = 'add-business/prefilled'
	dynamic = False

	def load(self):
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def load_body(self):
		self.form = self.driver.find_element_by_class_name('form-horizontal')
		find_by = self.form.find_elements_by_tag_name
		self.ein_input = find_by('input')[0]
		self.hr_email_input = find_by('input')[1]
		self.details_button = find_by('button')[0]
		self.load_agree_checkbox()

		self.continue_button = self.form.find_element_by_class_name('primaryButton')
		self.load_details() # for when you add address and details auto opens

	def load_agree_checkbox(self):
		if main.is_desktop() and main.get_browser() == 'safari':
			# Safari doesn't like clicking the input element
			labels = self.driver.find_elements_by_tag_name('label')
			self.agree_checkbox = labels[-1]
		else:
			self.agree_checkbox = self.form.find_element_by_id('agreed')

	def click_details(self):
		if main.is_android(): # may need to close keyboard
			self.try_hide_keyboard()
		self.scroll_to_top()
		self.details_button.click()
		self.load_details()
		time.sleep(1)

	def load_details(self):
		try:
			find_by = self.form.find_element_by_id
			self.business_name_input = find_by('title')
			self.dba_input = find_by('dba')
			self.line1_input = find_by('recipient_line1')
			self.line2_input = find_by('recipient_line2')
			self.city_input = find_by('recipient_city')

			# Container div
			self.state_cont = self.form.find_element_by_class_name('state_dropdown')
			# Div w/ value as text
			self.state_dd = self.state_cont.find_elements_by_tag_name('div')[3]

			self.postal_code_input = find_by('recipient_code')
			self.phone_input = find_by('phone')
			self.website_input = find_by('website')
			return True
		except (NoSuchElementException, IndexError) as e:
			return False
		time.sleep(1)

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
			return self.state_dd
		else:
			return None

	def get(self, name):
		el = self.get_el(name)
		if el is not None:
			if name == 'state':
				return el.text
			return el.get_attribute('value')
		return None

	def set(self, name, value):
		"""Given name of el, set desired value"""
		# don't use for setting state. Use type_state() or set_state()
		el = self.get_el(name)
		hasNewValue = False
		if el is not None:
			AC(self.driver).move_to_element(el).perform()
			if name == 'state':
				time.sleep(.4)
				self.set_state(value)
				hasNewValue = True
			else:
				# Sometimes has issues setting value (component redraws?).
				# Loop until it actually sets it
				el.clear()

				timeout = time.time() + 5
				while hasNewValue is False:
					el.send_keys(value)
					if self.get(name) == value:
						hasNewValue = True
					elif time.time() > timeout:
						break
					else:
						time.sleep(.5)
		return hasNewValue

	def set_state(self, state):
		#raw_input(self.state_dd.text)
		self.move_to_el(self.state_dd)
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sm-state-menuitem')))
		states = self.driver.find_elements_by_class_name('sm-state-menuitem')
		for i, st in enumerate(states):
			text = states[i].text
			if state in text:
				states[i].click()
				break
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'sm-state-menuitem')))

	# select state by typing keys, then selecting state by pressing enter
	def type_state(self,state):
		# move to input below state (so add button doesn't cover on mobile)
		AC(self.driver).move_to_element(self.postal_code_input).perform()
		self.state_dd.click()
		time.sleep(2) # need decent wait before sending keys
		AC(self.driver).send_keys(state).perform()
		time.sleep(1)
		AC(self.driver).send_keys(Keys.ENTER).perform()
		time.sleep(1)

	def toggle_agree(self):
		# agree_checkbox is touchy.
		# Think you need to reload form after clicking checkbox or submitting form
		# (only need to reload form after submission if you toggle checkbox afterwards)
		self.scroll_to_bottom()
		selected = self.agreed()
		# if main.get_browser() == 'safari':
		# 	self.agree_cont.click()
		# else:

		# Hope this works for all environments
		self.move_to_el(self.agree_checkbox)
		if selected is self.agreed():
			print('checkbox not altered!')
		time.sleep(.4)

	def agreed(self):
		# Is agree checkbox selected or not?
		checkbox = self.agree_checkbox
		if main.is_desktop() and main.get_browser() == 'safari':
			checkbox = self.form.find_element_by_id('agreed')
		try:
			return checkbox.is_selected()
		except (StaleElementReferenceException, WebDriverException) as e:
			# Reload page and check again
			self.load()
			checkbox = self.form.find_element_by_id('agreed')
			return checkbox.is_selected()

	def click_continue(self):
		self.scroll_to_bottom()
		time.sleep(.2)
		self.continue_button.click()

		# Have had issues trying to load lobby page after clicking continue
		# Try to verify not on prefilled page anymore
		try:
			WDW(self.driver, 2).until_not(
				EC.presence_of_element_located((By.ID, 'agreed')))
			return True
		except TimeoutException:
			# still on page. Need to reload
			self.load()
			return False

