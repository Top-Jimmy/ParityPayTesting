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
from signInForm import SignInForm
from forgotPasswordForm import ForgotPasswordForm
from navigation import NavigationFunctions


class PubHeader(Component):
	"""load content of element id='sendmi_public_appbar'"""

	def __init__(self, driver):
		self.driver = driver
		self.nav = NavigationFunctions(self.driver)
		self.load()

	def load(self):
		self.cont = self.load_cont()

		find_by = self.cont.find_element_by_id

		# Todo: Load Logo, language dd

		# ID nightmare...
		# self.logo = find_by('public_logo_sm')
		self.logo = find_by('public_logo')
		# self.language_dd = find_by('locale_dropdown')

		self.pre_signed_in = self.load_pre_sign_in()
		# desktop only
		if main.is_desktop():
			# signin dropdown only on desktop when not signed in
			# never on signin or signin/code
			# Contents of dropdown do not exist when dropdown is closed
			try:
				self.sign_in_button = (
					self.cont.find_element_by_id('signin_dropdown'))
			except NoSuchElementException:
				self.sign_in_button = None

		# forgot pw form loads when 'forgot' link clicked
		self.for_employers = self.load_employers_link()
		self.for_employees = self.load_employees_link()

		# mobile web only
		self.hamburger = self.try_load_hamburger()

	def load_cont(self):
		# IDs are a nightmare
		# look for sendmi_public_appbar or sendmi_appbar
		try:
			cont = self.driver.find_element_by_id('sendmi_appbar')
			return cont
		except NoSuchElementException:
			try:
				cont = self.driver.find_element_by_id('sendmi_public_appbar')
				return cont
			except NoSuchElementException:
				print('Failed to load appbar container')
				raise NoSuchElementException('Failed to load appbar container')

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
			return self.cont.find_element_by_id('public_enroll_employers')
		except NoSuchElementException:
			return None

	def load_employees_link(self):
		"""Desktop only. Pages: enroll, contact us, about"""
		# Note: Is same id for option in action menu
		try:
			return self.cont.find_element_by_id('public_enroll_employees')
		except NoSuchElementException:
			return None

	def try_load_hamburger(self):
		# Only on mobile. Menu contents only visible when open
		try:
			return self.driver.find_element_by_id('nav_toggle')
		except NoSuchElementException:
			return None

	# header functions

	def click_logo(self):
		"""click visible header logo"""
		logo = self.logo
		if main.is_desktop() and not self.logo.is_displayed():
			# scrolled to top on desktop and we need to load other logo
			logo = self.cont.find_element_by_id('public_logo')

		self.nav.click_el(logo)

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
		if self.hamburger != None:
			if not self.action_menu_open():
				self.nav.click_el(self.hamburger)
				WDW(self.driver, 10).until(lambda x:
					EC.element_to_be_clickable((By.ID, 'public_enroll')) or
					EC.element_to_be_clickable((By.ID, 'signin_myaccount'))
				)
				time.sleep(.4)

			elId = None
			if text.lower() == 'employers':
				elId = 'public_enroll_employers'
			elif text.lower() == 'employees':
				elId = 'public_enroll_employees'
			elif text.lower() == 'sign in':
				elId = 'public_enroll'
			elif text.lower() == 'signed in':
				elId = 'signin_myaccount'

			if elId:
				try:
					el = self.driver.find_element_by_id(elId)
				except NoSuchElementException:
					print('unable to find element w/ id: ' + str(elId))

			if el:
				self.nav.click_el(el)
				return True
		return False

	def action_menu_open(self):
		# Does action menu exist (web only) and is it open?
		find_by = self.driver.find_element_by_class_name
		if (self.hamburger != None):
			try:
				el = find_by('MuiDrawer-paperAnchorTop-069')
				return el.is_displayed()
			except NoSuchElementException:
				pass
		return False

	def sign_in_submit(self, email='', password='', submit=True):
		# No sign in dropdown on mobile
		if main.is_desktop():
			# Make sure dropdown is visible (won't have dropdown on signin page)
			if self.sign_in_button:
				if not self.sign_in_open():
					self.nav.click_el(self.sign_in_button)

				self.signInForm = SignInForm(self.driver)
				WDW(self.driver, 10).until(lambda x: self.signInForm.load())
				self.signInForm.submit(email, password, submit)

	def forgot_password_submit(self, email='', submit=True):
		# No forgor password dropdown on mobile
		if main.is_desktop():
			# Neither dropdowns are visible
			if not self.forgot_password_open() and not self.sign_in_open():
				self.nav.click_el(self.sign_in_button)
				self.signInForm = SignInForm(self.driver)

			# Sign In form is visible
			if self.sign_in_open():
				WDW(self.driver, 10).until(lambda x: self.signInForm.load())
				self.signInForm.forgot_password()

			# Should be on forgotPWForm
			self.forgotPWForm = ForgotPasswordForm(self.driver)
			WDW(self.driver, 10).until(lambda x: self.forgotPWForm.load())
			self.forgotPWForm.submit(email, submit)

	def sign_in_open(self):
		# is signin dropdown open?
		if main.is_desktop() and self.sign_in_button:
			try:
				el = self.driver.find_element_by_id('forgot_password')
				if el.is_displayed():
					return True
			except NoSuchElementException:
				pass
		return False

	def forgot_password_open(self):
		# Is forgot password form visible?
		if main.is_desktop() and self.sign_in_button:
			try:
				resetPWform = self.driver.find_element_by_class_name('resetPWForm')
				if resetPWform.is_displayed():
					return True
			except NoSuchElementException:
				pass
		return False

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


