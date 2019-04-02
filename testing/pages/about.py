#coding: utf-8
from page import Page
from components import menu
import time
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import main
from components import header
from components import footer

class AboutPublicPage(Page):
	url_tail = "about"
	dynamic = False

	def load(self):
		#logo, language select
		try:
			find_by = self.driver.find_elements_by_class_name
			self.employee_button = find_by('employerButton')[0]
			self.employer_button = find_by('employerButton')[1]

			self.form = self.load_form()
			find_by = self.form.find_element_by_tag_name
			self.invite_employer_input = find_by('input')
			self.invite_employer_button = find_by('button')
			self.header = header.PubHeader(self.driver)
			self.footer = footer.PubFooter(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def load_form(self):
		el = self.driver.find_element_by_class_name('enrollCont')
		return el.find_element_by_tag_name('form')

	def set_invite_employer_email(self,email):
		self.move_to_el(self.invite_employer_input)
		self.invite_employer_input.clear()
		self.invite_employer_input.send_keys(email)
		time.sleep(.4)

	def get_invite_employer_email(self):
		return self.invite_employer_input.get_attribute('value')

	def click_invite_employer_continue(self):
		self.move_to_el(self.invite_employer_button)

	def enter_invite_employer_email(self,email):
		self.set_invite_employer_email(email)
		self.click_invite_employer_continue()

	def click_employee_button(self):
		"""Learn More button redirecting to home page"""
		self.move_to_el(self.employee_button)

	def click_employer_button(self):
		self.move_to_el(self.employer_button)

class AboutPrivatePage(Page):
	url_tail = 'about-auth'
	dynamic = False

	def load(self):
		try:
			self.menu = menu.SideMenu(self.driver, True)
			self.header = header.PrivateHeader(self.driver, 'About Us')
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

