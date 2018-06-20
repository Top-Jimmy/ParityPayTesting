from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, TimeoutException, WebDriverException)
from page import Page
from components import menu
from components import header
import time
import main
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Different from business_prefilled.py
# Get to page by adding business and clicking "Can't find business".

class BusinessDetailsPage(Page):
	url_tail = 'add-business/detail'
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
		find_by_id = self.form.find_element_by_id
		self.ein_input = find_by('input')[0]
		self.hr_email_input = find_by('input')[1]
		self.business_name_input = find_by('input')[2]
		self.dba_input = find_by('input')[3]

		self.line1_input = find_by_id('recipient_line1')
		self.line2_input = find_by_id('recipient_line2')
		self.city_input = find_by_id('recipient_city')

		# not sure which el we need to click
		self.state_cont = self.form.find_element_by_class_name('state_dropdown')
		self.state_dd = self.state_cont.find_elements_by_tag_name('div')[3]
		self.postal_code_input = find_by_id('recipient_code')
		self.phone_input = find_by('input')[9]
		self.website_input = find_by('input')[10]
		self.continue_button = self.form.find_element_by_class_name('primaryButton')

		self.load_agree_checkbox()

	def load_agree_checkbox(self):
		# cont = self.form.find_element_by_id('agreed')
		# self.agree_checkbox = cont.find_element_by_tag_name('input')
		self.agree_checkbox = self.form.find_element_by_id('agreed')

	# def toggle_agree(self):
	# 	self.scroll_to_bottom()
	# 	self.agree_checkbox.click()
	# 	time.sleep(.4)
	# 	self.load_body()

	def toggle_agree(self):
		# agree_checkbox is touchy.
		# Think you need to reload form after clicking checkbox or submitting form
		# (only need to reload form after submission if you toggle checkbox afterwards)
		self.scroll_to_bottom()
		selected = self.agreed()
		if main.get_browser() == 'safari':
			self.agree_cont.click()
		else:
			self.agree_checkbox.click()
		if selected is self.agreed():
			print('checkbox not altered!')
		time.sleep(.4)

	def agreed(self):
		try:
			return self.agree_checkbox.is_selected()
		except (StaleElementReferenceException, WebDriverException) as e:
			self.load()
			return self.agree_checkbox.is_selected()

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
			if main.is_ios(): # click doesn't regester on self.state_cont
				return self.state_dd
			return self.state_cont
		else:
			return None

	def get(self, name):
		"""Return the text of the element with the given name"""
		el = self.get_el(name)
		if el is not None:
			if name == 'state':
				# ignore text in label
				if not main.is_ios(): # ios: el is already the child
					el = el.find_elements_by_tag_name('div')[0]
				return el.text
			return el.get_attribute('value')
		return None

	def set(self, name, value):
		"""Pass in name of el and desired value. Don't use for setting state"""
		el = self.get_el(name)
		if el is not None:
			self.move_to_el(el)
			if name == 'state':
				time.sleep(.4)
				self.set_state(value)
			else:
				el.clear()
				el.send_keys(value)

				# ios: Inputs dont seem to update unless you click after setting value
				# i.e. 'Required' errors won't show up just for sending keys.
				if main.is_ios():
					el.click()

	def set_state(self, state_text):
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sm-state-menuitem')))
		try:
			self.states = self.driver.find_elements_by_class_name('sm-state-menuitem')
			for i, state in enumerate(self.states):
				text = self.states[i].text
				if text == state_text:
					self.states[i].click()
					break
		except NoSuchElementException:
			# couldn't find state. De-select dropdown
			AC(self.driver).send_keys(Keys.ESC).perform()
		WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'sm-state-menuitem')))

	# select state by typing keys, then selecting state by pressing enter
	def type_state(self,state):
		self.move_to_el(self.state_dd)
		# AC(self.driver).move_to_element(self.state_dd).perform()
		# self.state_dd.click()
		time.sleep(1.4) # need decent wait before sending keys
		AC(self.driver).send_keys(state).perform()
		time.sleep(.4)
		AC(self.driver).send_keys(Keys.ENTER).perform()
		time.sleep(.4)

	# def click_continue(self):
	# 	el = self.continue_button
	# 	self.scroll_to_bottom()
	# 	# AC(self.driver).move_to_element(el).perform()
	# 	el.click()
	# 	time.sleep(.4)

	def click_continue(self):
		self.scroll_to_bottom()
		time.sleep(.2)
		self.continue_button.click()

		try:
			WDW(self.driver, 2).until_not(
				EC.presence_of_element_located((By.ID, 'agreed')))
			# not on details page anymore
		except TimeoutException:
			# still on page. Need to reload
			self.load()