from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains as AC
from page import Page
from components import menu
from components import header
import time
import main

class InvitationCardPage(Page):
	url_tail = "invitation/" #i.e. https://test.sendmi.com/invitation/0fd9050f
	dynamic = True

	def load(self):
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def load_body(self):
		self.invitee = self.driver.find_element_by_tag_name('h1').text
		self.try_load_default()

	def try_load_default(self):
		try:
			table = self.driver.find_element_by_tag_name('table')
			rows = table.find_elements_by_tag_name('tr')
			invitation_fields = ['id', 'zip', 'dob', 'email', 'date_created', 'status']
			self.invite_info = {}
			for i, row in enumerate(rows):
				text = row.find_element_by_tag_name('td').text
				self.invite_info[invitation_fields[i]] = text
		except NoSuchElementException:
			self.invite_info = None

	def try_load_edit(self):
		try:
			# load inputs
			pass
		except NoSuchElementException:
			# inputs = None
			pass