from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from components import menu
from page import Page
from components import header
from components import stepper
import time
import main
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SendToCashoutPage(Page):
	url_tail = 'send-to-cashout'
	dynamic = False

	def load(self):
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver, True)
			self.header = header.PrivateHeader(self.driver)
			self.stepper = stepper.Stepper(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
		IndexError) as e:
			return False

	def load_body(self):
		pass

