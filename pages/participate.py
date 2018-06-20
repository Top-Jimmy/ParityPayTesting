from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from page import Page
from components import menu
from components import header
import main
import time

class ParticipatePage(Page):
	def load(self):
		try:
			self.body = self.load_body()
			self.header = header.PrivateHeader(self.driver)
			self.menu = menu.SideMenu(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_body(self):
		self.form = self.driver.find_element_by_tag_name('form')
		inputs = self.form.find_elements_by_tag_name('input')
		self.emp_id = inputs[0]
		self.dob = inputs[1]
		self.zip = inputs[2]
		self.agree = inputs[3]
		self.submit = self.form.find_element_by_class_name('primaryButton')

	def set_id(self, id):
		self.scroll_to_top()
		self.emp_id.clear()
		self.emp_id.send_keys(id)

	def set_dob(self, dob):
		self.scroll_to_top()
		self.dob.clear()
		self.dob.send_keys(dob)

	def set_zip(self, zip_code):
		self.scroll_to_top()
		self.zip.clear()
		self.zip.send_keys(zip_code)

	def get_id(self):
		return self.emp_id.get_attribute('value')

	def get_dob(self):
		return self.dob.get_attribute('value')

	def get_zip(self):
		return self.zip.get_attribute('value')

	def click_agree(self):
		# checkbox likely needs to be reloaded every time its toggled or form submitted
		self.scroll_to_bottom()
		self.agree.click()

	def agreed(self):
		return self.agree.is_selected()

	def click_submit(self):
		self.submit.click()
		time.sleep(.4)
		# currently redirects to main election page (/main-election)




