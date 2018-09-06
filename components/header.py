from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction as TA

import time
import main
from component import Component
from navigation import NavigationFunctions


class PubHeader(Component):
	"""load content of element id='sendmi_public_appbar'"""

	def __init__(self, driver):
		self.driver = driver
		self.nav = NavigationFunctions(self.driver)
		self.load()

	def load(self):
		self.cont = self.driver.find_element_by_id('sendmi_public_appbar')
		find_by = self.cont.find_element_by_id

		# all environments *ignoring hybrid app (no homepage on hybrid)
		self.logo = find_by('public_logo_sm')
		self.language_dd = find_by('locale_dropdown')
		self.english = find_by('locale_en')
		self.spanish = find_by('locale_es')

		self.pre_signed_in = self.load_pre_sign_in()
		# desktop only
		if main.is_desktop():
			self.load_sign_in_dd()
		# forgot pw form loads when 'forgot' link clicked

		self.for_employers = self.load_employers_link()
		self.for_employees = self.load_employees_link()

		# mobile web only
		self.load_action_menu()

	def load_sign_in_dd(self):
		# signin dropdown only on desktop when not signed in
		# never on signin or signin/code
		if not self.signed_in():
			try:
				self.sign_in_button = (
					self.cont.find_element_by_id('signin_dropdown'))
				self.signin_form = self.cont.find_element_by_id('signin_form_id')
				find_by = self.signin_form.find_element_by_id
				self.sign_in_email = find_by('signin_form_user')
				self.sign_in_pw = find_by('signin_form_pw')
				self.sign_in_forgot_pw = find_by('forgot_password')
				self.sign_in_continue = find_by('submit_si_button')
				return
			except NoSuchElementException:
				pass
		self.sign_in_button = None
		self.signin_form = None
		self.sign_in_email = None
		self.sign_in_pw = None
		self.sign_in_forgot_pw = None
		self.sign_in_continue = None

	def load_pre_sign_in(self):
		# Desktop: item in header
		# Mobile: option in header action menu
		try:
			return self.cont.find_element_by_id("signin_myaccount")
		except NoSuchElementException:
			return None

	def load_employers_link(self):
		"""Desktop only. Pages: homepage, contact us, about"""
		# Note: Is same id for option in action menu
		try:
			return self.cont.find_element_by_id('public_enroll')
		except NoSuchElementException:
			return None

	def load_employees_link(self):
		"""Desktop only. Pages: enroll, contact us, about"""
		# Note: Is same id for option in action menu
		try:
			return self.cont.find_element_by_id('public_enroll_employees')
		except NoSuchElementException:
			return None

	def load_action_menu(self):
		# only on mobile (*no homepage on hybrid)
		# todo: use unique ID (signed_in conflicts with desktop header link)
		find_by = self.cont.find_element_by_id
		try:
			self.action_menu = find_by('nav_toggle')
			self.action_employers = self.load_employers_link()
			self.action_employees = self.load_employees_link()
			if self.signed_in():
				self.action_signed_in = find_by('signin_myaccount')
				self.action_sign_in = None
			else:
				self.action_sign_in = find_by('mobile_signin')
				self.action_signed_in = None
		except NoSuchElementException:
			self.action_menu = None
			self.action_employers = None
			self.action_employees = None
			self.action_sign_in = None
			self.action_signed_in = None

	# header functions

	def click_logo(self):
		"""click visible header logo"""
		logo = self.logo
		if main.is_desktop() and not self.logo.is_displayed():
			# scrolled to top on desktop and we need to load other logo
			logo = self.cont.find_element_by_id('public_logo')

		self.nav.click_el(logo)

	'''def give_feedback(self, happiness, messsage):
		self.scroll_to_top()
		self.feedback.click()
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'subbutkey')))
		#time.sleep(1)
		self.load_feedback_form(happiness, message)'''
	# Authenticated-user only functionality

	def load_feedback_form(self):
		pass

	def click_for_employers(self):
		if self.for_employers != None:
			self.for_employers.click()
			WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'demo_email')))

	def click_for_employees(self):
		if main.is_desktop():
			if self.for_employees != None:
				self.for_employees.click()
				WDW(self.driver,10).until(EC.presence_of_element_located((By.ID, 'contactEmail2')))
		else:
			self.select_action('employees')

	def select_action(self, text):
		# text: 'emp' (employers or employees), 'sign in', or 'signed in'
		self.nav.click_el(self.action_menu)
		if self.action_menu != None:
			if not self.action_menu_open():
				self.action_menu.click()
				WDW(self.driver, 10).until(lambda x:
					EC.element_to_be_clickable((By.ID, 'mobile_signin')) or
					EC.element_to_be_clickable((By.ID, 'signin_myaccount'))
				)
				time.sleep(.4)

			if text.lower() == 'employers':
				self.action_employers.click()
			elif text.lower() == 'employees':
				self.action_employees.click()
			elif text.lower() == 'sign in' and self.action_sign_in != None:
				self.action_sign_in.click()
			elif text.lower() == 'signed in' and self.action_signed_in != None:
				self.action_signed_in.click()
			return True
		return False

	def action_menu_open(self):
		# Does action menu exist (web only) and is it open?
		find_by = self.driver.find_element_by_class_name
		if (self.action_menu != None and
			find_by('navbar-collapse').is_displayed()):
			return True
		return False

	def sign_in_open(self):
		# is signin dropdown open?
		if main.is_desktop():
			el = self.sign_in_forgot_pw
			if el is not None and el.is_displayed():
				return True
		return False

	def click_sign_in(self):
		self.sign_in_button.click()

	def set_sign_in_email(self,email):
		if not self.sign_in_open():
			self.click_sign_in()
		self.sign_in_email.clear()
		self.sign_in_email.send_keys(email)

	def set_sign_in_pw(self,pw):
		if not self.sign_in_open():
			self.click_sign_in()
		self.sign_in_pw.clear()
		self.sign_in_pw.send_keys(pw)

	def click_forgot_pw(self):
		if not self.sign_in_open():
			self.click_sign_in()
		self.sign_in_forgot_pw.click()
		self.load_forgot_pw()

	def load_forgot_pw(self):
		try:
			self.forgot_form = self.cont.find_element_by_tag_name('form')
			find_by = self.forgot_form.find_element_by_tag_name

			self.forgot_input = (
				self.forgot_form.find_element_by_tag_name('input'))
			self.forgot_continue = (
				self.forgot_form.find_element_by_id('submit_button'))
		except NoSuchElementException:
			self.forgot_input = None
			self.forgot_continue = None

	def set_forgot_input(self,text):
		self.forgot_input.clear()
		self.forgot_input.send_keys(text)

	def click_forgot_continue(self):
		self.forgot_continue.click()

	def click_login(self):
		if not self.sign_in_open():
			self.click_sign_in()
		self.sign_in_continue.click()

	def signed_in(self):
		# is user signed in?
		# Used to tell which item we should expect in header/action dd
		return self.pre_signed_in is not None

	def sign_in(self):
		if self.signed_in():
			if main.is_desktop():
				self.move_to_el(self.pre_signed_in)
			else:
				self.select_action('signed in')

class PrivateHeader():
	def __init__(self, driver, page_title=None):
		self.driver = driver
		self.page_title = page_title
		self.load()

	def load(self):
		self.cont = self.driver.find_element_by_id('sendmi_appbar')
		# back button or hamburger icon? (no hamburger on desktop)
		self.back_button = None
		self.hamburger = None
		if self.menu_type() == 'back':
			self.back_button = self.driver.find_element_by_id('navback_button')
		elif main.get_env() != 'desktop':
			self.hamburger = self.cont.find_element_by_class_name('hamburger')

		self.feedback = self.cont.find_element_by_id('feedback_dropdown')
		try:
			self.english = self.driver.find_element_by_id('locale_en')
			self.spanish = self.driver.find_element_by_id('locale_es')
		except NoSuchElementException:
			self.english = None
			self.spanish = None

	def menu_type(self):
		# 'hamburger' on desktop doesn't actually have hamburger icon
		try:
			el = self.driver.find_element_by_id('navback_button')
			return 'back'
		except NoSuchElementException:
			return 'hamburger'

	def give_feedback(self, happiness, messsage):
		self.scroll_to_top()
		self.feedback.click()
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'subbutkey')))
		#time.sleep(1)
		self.load_feedback_form(happiness, message)

	def load_feedback_form(self):
		pass

	def get_page_title(self):
		return self.title.text

	def click_header(self):
		# Should allow clicking off of element
		header = self.driver.find_element_by_tag_name('header')
		self.driver.execute_script("arguments[0].scrollIntoView();", header)
		header.click()

	def click_back(self):
		if self.back_button != None:
			self.back_button.click()
			return True
		return False


