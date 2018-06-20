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

# Page for accepting user agreement when...
# 1: new employer creates account
# 2: new user responds to invite

class EnrollAcceptPage(Page):
	url_tail = "enroll-business/agreement" # (employer signs up)
	# or "accept/agreement" (responding to invite)

	def load(self):
		try:
			WDW(self.driver, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME, 'terms')))
			self.load_body()
			self.header = header.PubHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			WebDriverException) as e:
			return False

	def load_body(self):
		self.welcome_text = self.driver.find_element_by_tag_name('h1')
		self.continue_button = self.driver.find_element_by_class_name('primaryButton')
		# self.terms_of_service = self.driver.find_element_by_id('termsLink')
		# self.privacy_policy = self.driver.find_element_by_id('privacyLink')

	def get_first_name(self):
		"""Parse welcome_text and return name ('Welcome, first_name!')"""
		return self.welcome_text.text[9:-1]

	# def click_terms_of_service(self):
	# 	self.terms_of_service.click()

	# def click_privacy_policy(self):
	# 	self.privacy_policy.click()

	def click_continue(self, invite_type="employee"):
		self.move_to_el(self.continue_button)
		# Landing page depends on if this was employee or admin invite
		if invite_type == 'employee': # Should land on employee-welcome
			WDW(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'welcome-next')))
		elif invite_type == 'employer': #land on add business map
			WDW(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'busName')))
		else: # Should land on lobby page. Wait for invite card to show up
			WDW(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'invitations_card')))
