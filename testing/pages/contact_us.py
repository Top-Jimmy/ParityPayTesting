# coding: utf-8
from page import Page
from components import menu
from components import header
from components import footer
import time
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys

class ContactPublicPage(Page):
	url_tail = "contact-us"
	dynamic = False

	def load(self):
		try:
			self.h1 = self.driver.find_element_by_tag_name('h1')
			if not self.h1.text == 'Contact Us': # not on right page
				self.driver.find_element_by_id('bogus')

			self.header = header.PubHeader(self.driver)
			self.footer = footer.PubFooter(self.driver)
			self.form = self.driver.find_element_by_class_name('enrollCont')
			find_by = self.form.find_element_by_tag_name
			self.invite_employer_input = find_by('input')
			self.invite_employer_button = find_by('button')
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

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


class ContactPrivatePage(Page):
	url_tail = "feedback"
	dynamic = False

	def load(self):
		try:
			# print('loading contact us')
			self.h1 = self.driver.find_element_by_tag_name('h1')
			# print('loaded h1')
			if not self.h1.text == 'Contact Us': # not on right page
				print('wrong page')
				self.driver.find_element_by_id('bogus')
			# print('loading menu')
			self.menu = menu.SideMenu(self.driver, True)
			# print('loading header')
			self.header = header.PrivateHeader(self.driver)
			# print('done loading contact page')
			# probably getting removed
			# (doesn't make sense when you're logged in...)
			# self.form = self.driver.find_element_by_class_name('enrollCont')
			# find_by = self.form.find_element_by_tag_name
			# self.invite_employer_input = find_by('input')
			# self.invite_employer_button = find_by('button')

			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

