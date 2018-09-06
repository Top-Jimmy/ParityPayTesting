from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from page import Page
from components import header
from components import menu
import time

class AddEmployeesCSV1Page(Page):
	url_tail = 'add-employees'
	dynamic = False

	def load(self):
		pass

class AddEmployeesCSV2Page(Page):
	url_tail = 'add-employees-step2'
	dynamic = False

	def load(self):
		pass