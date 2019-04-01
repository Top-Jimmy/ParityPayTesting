#coding: utf-8
from page import Page
from components import menu
from components import header
from components import footer
from navigation import NavigationFunctions

import time
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import main


class InvitePreScreenPage(Page):

	def load(self):
		try:
			self.nav = NavigationFunctions(self.driver)
			anchors = self.driver.find_elements_by_tag_name('a')
			if len(anchors) == 2:
				self.browserButton = anchors[0]
				self.appButton = anchors[1]
			else:
				raw_input(len(anchors))
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
			return False

	def click(self, button='browser'):
		if button == 'browser':
			self.nav.click_el(self.browserButton)
		elif button == 'app':
			self.nav.click_el(self.appButton)
		else:
			raw_input('InvitePreScreenPage: Wrong button')

