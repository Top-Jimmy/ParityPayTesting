from page import Page
from components import header
import main
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# universal page for entering code to validate phone/email.
# used for enrolling your business or responding to an invite

class EnrollCodePage(Page):
	url_tail = 'enroll-business/code' # (enrolling your business)
	# url_tail = 'accept/code' (responding to invite)
	dynamic = False

	def load(self):
		try:
			self.load_body()
			self.header = header.PubHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			WebDriverException) as e:
			print(str(e) + '\n')
			return False

	def load_body(self):
		self.code = self.get_code()
		self.form = self.driver.find_element_by_tag_name('form')
		self.wrong_button = self.form.find_element_by_tag_name('a')
		self.code_input = self.form.find_element_by_tag_name('input')
		self.continue_button = self.form.find_element_by_tag_name('button')
		# num_inputs = len(self.form.find_elements_by_tag_name('input'))
		# num_buttons = len(self.form.find_elements_by_tag_name('button'))
		# num_a = len(self.form.find_elements_by_tag_name('a'))

		# if num_inputs != 1:
		#     print "Too many inputs in EnrollCodePage form"
		# if num_buttons != 1:
		#     print "Too many buttons in EnrollCodePage form"
		# if num_a != 1:
		#     print "Too many anchors in EnrollCodePage form"

	def try_click_toast(self):
		try:
			self.driver.find_element_by_class_name("sm-secret-code").click()
		except NoSuchElementException:
			pass

	def get_code(self):
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'testSnackId')))
		#time.sleep(.6)
		code = self.driver.find_element_by_id("testSnackId").text
		self.try_click_toast()
		return code[33:39]

	def enter_code(self):
		self.code_input.clear()
		self.code_input.send_keys(self.code)
		if main.is_ios():
			self.code_input.send_keys('')

		if self.code_accepted():
			self.continue_button.click()
		else:
			raise Exception("Took too long to validate login code")

	def code_accepted(self):
		# After entering code, wait until continue button is enabled.
		timeout = time.time() + 5
		is_enabled = False
		while is_enabled is False:
			if self.is_enabled(self.continue_button):
				is_enabled = True
			elif time.time() > timeout:
				break
			else:
				time.sleep(.5)
		return is_enabled

	def click_continue(self):
		self.continue_button.click()

	def click_wrong_button(self):
		self.wrong_button.click()

