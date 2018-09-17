import time
import main
from selenium.common.exceptions import (NoSuchElementException,
	WebDriverException, TimeoutException)
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction as TA
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW


class SideMenu():
	def __init__(self, driver, hamburger=False):
		self.driver = driver
		self.load(hamburger)

	def load(self, hamburger, loading_page=True):
		if hamburger and not main.is_desktop():
			self.hamburger = self.load_hamburger()
		else:
			self.hamburger = self.try_load_hamburger()
		if self.is_drawer_visible(loading_page):
			self.load_employer_buttons()
				# current business
				# lobby button
				# pending elections
				# invitations
				# employees button
				# business_settings button
				# admins
				# settings
			self.load_employee_buttons()
				# eHome
				# recipients
				# pay_election
				# settings
			self.load_employer_business_buttons()
				# businesses and add business button
				# No settings

			# only for dual role users
			self.role_switch = self.try_load_role_switch()

			# static options
			self.load_header()
			# profile
			# version
			self.try_load_general()

			# desktop only
			self.toggle_button = self.try_load_toggle()

			self.option_els = {
				'profile': self.profile,
				'ehome': self.eHome,
				'recipients': self.recipients,
				'lobby': self.lobby,
				'employees': self.employees,
				'pending elections': self.pending,
				'invitations': self.invitations,
				'business settings': self.business_settings,
				'admin': self.admins,
				'settings': self.settings,
				'contact us': self.contact_us,
				'about': self.about,
				'terms and privacy': self.terms_and_privacy,
				'sign out': self.logout
			}

	def load_header(self):
		# Since this is only called when menu is open (or skinny)
		# This stuff better already be loaded
		self.version = self.load_version()
		self.profile = self.driver.find_element_by_class_name('drawer_profile')

	def load_version(self):
		# make sure version is what we expect
		# should only be called when we know the drawer is open
			try:
				el = self.driver.find_element_by_class_name('drawer_version')
				text = el.text
				if text != main.get_version():
					raw_input('Does menu have version: ' + str(main.get_version()))
					err_msg = (
						"Update version in main.py to match app's version."
						"\nCreate tab for new version in spreadsheet."
						"\n" + text + " != " + main.get_version()
					)
					raise Exception(err_msg)
				return el
			except NoSuchElementException:
				return None

	def try_load_general(self):
		try:
			find_by = self.driver.find_element_by_class_name
			self.contact_us = find_by('drawer_support')
			self.about = find_by('drawer_about')
			self.terms_and_privacy = find_by('drawer_terms')
			self.logout = find_by('drawer_logout')
		except NoSuchElementException:
			pass

	def try_load_role_switch(self):
		# only get role switch for dual role users
		try:
			return self.driver.find_element_by_class_name('drawer_roleswitch')
		except NoSuchElementException:
			return None

########################### Employer Buttons #################################

	def load_employer_buttons(self):
		# load after toggling 'current_business'
		self.current_business = self.load_current_business()
		self.businesses = self.load_businesses()
		self.add_button = self.load_add_business_button()
		self.lobby = self.load_lobby()
		self.employees = self.load_employees_button()
		self.pending = self.load_pending_elections_button()
		self.invitations = self.load_invitations_button()
		self.business_settings = self.load_business_settings_button()
		self.admins = self.load_admins()
		self.settings = self.load_employer_settings()

	def load_current_business(self):
		# Only for employers
		try:
			return self.driver.find_element_by_id('drawer_selBus')
		except NoSuchElementException:
			# user is employee w/ no permissions
			return None

	def load_lobby(self):
		# home page for employer role
		try:
			return self.driver.find_element_by_class_name('drawer_admin')
		except NoSuchElementException:
			return None

	def load_employees_button(self):
		try:
			return self.driver.find_element_by_class_name('drawer_employees')
		except NoSuchElementException:
			return None

	def load_pending_elections_button(self):
		try:
			return self.driver.find_element_by_class_name('drawer_elections')
		except NoSuchElementException:
			return None

	def load_invitations_button(self):
		try:
			return self.driver.find_element_by_class_name('invitations')
		except NoSuchElementException:
			return None

	def load_business_settings_button(self):
		try:
			return self.driver.find_element_by_class_name('drawer_busSet')
		except NoSuchElementException:
			return None

	def load_admins(self):
		try:
			return self.driver.find_element_by_class_name('drawer_admins')
		except NoSuchElementException:
			return None

	def load_employer_settings(self):
		# Loads 'Settings' option in drawer when in employer role
		# if we're not in employer role it will get set in load_employee_settings()
		try:
			return self.driver.find_element_by_class_name('drawer_empSet')
		except (NoSuchElementException, IndexError): #IndexError:
			return None
		except Exception as e:
			raise e
			return None
		return None

###################### Employer Business buttons ############################

	def load_employer_business_buttons(self):
		self.current_business = self.load_current_business()
		self.businesses = self.load_businesses()
		self.add_button = self.load_add_business_button()

	def load_businesses(self):
		# businesses managed by employer (not including current business)
		# visible after clicking on current business
		# Part of Employer Select Business view
		try:
			return self.driver.find_elements_by_class_name('drawer_bus')
		except NoSuchElementException:
			return None

	def load_add_business_button(self):
		# Visible when employer clicks on current business
		# Part of Employer Select Business view
		try:
			# parent = self.driver.find_element_by_class_name('drawer_addBus')
			# return parent.find_element_by_tag_name('a')
			return self.driver.find_element_by_class_name('drawer_addBus')
		except NoSuchElementException:
			return None

########################## Employee buttons #############################

	def load_employee_buttons(self):
		try:
			find_by = self.driver.find_element_by_class_name
			self.eHome = find_by('drawer_account')
			self.recipients = find_by('drawer_recip')
			self.settings = self.load_personal_settings()
		except NoSuchElementException:
			# Should be in employer role.
			# self.settings will be set by load_employer_buttons
			self.eHome = None
			self.recipients = None

	def load_personal_settings(self):
		# ID for
		# Used to not show when current business was selected. Now it does 1/02
		try:
			return self.driver.find_element_by_class_name('drawer_persSet')
		except NoSuchElementException:
			return None

########################### General Buttons ##############################

	def try_load_toggle(self):
		"""Should only have menu toggle on desktop"""
		if main.is_desktop():
			try:
				return self.driver.find_element_by_class_name('mini-button')
			except NoSuchElementException:
				return None
		else:
			return None

	def load_hamburger(self):
		# Only call when you know there's hamburger on page
		header = self.driver.find_element_by_id('sendmi_appbar')
		return header.find_element_by_class_name('hamburger')

	def try_load_hamburger(self):
		# Should only have hamburger on mobile
		try:
			header = self.driver.find_element_by_id('sendmi_appbar')
			return header.find_element_by_class_name('hamburger')
			# svgs = header.find_elements_by_tag_name('svg')
			# if len(svgs) > 1:
			# 	return svgs[0]
		except (NoSuchElementException, WebDriverException) as e:
			pass
		return None

############################# Employer functions #############################
# assumes already in 'employer' role

	def click_current_business(self):
		# If employer, click current business and reload menu
		if self.get_role() == 'employer':
			self.current_business.click()
			time.sleep(.2)
			# reload page (current business stuff will cover employer buttons)
			# Should be no hamburger when menu is open
			self.load(hamburger=False, loading_page=False)

	def add_a_business(self):
		# if employer, make sure current business is selected
		# then click 'add a business' button
		self.open()
		if self.get_role() == 'employer':
			if self.is_default_employer_view():
				self.click_current_business()
			self.add_button.click()
			# should now be on add_business page

	def is_default_employer_view(self):
		# True: 'employees' and 'business settings' are visible
		# False: Current business selected and 'Add a business' button visible
		if self.add_button is None:
			return True
		return False

	def has_business(self, name):
		if self.get_role() == 'employer':
			if not self.is_drawer_visible():
				self.open()
			# Ensure employers are visible
			if self.is_default_employer_view():
				self.click_current_business()

			# Look in self.businesses
			for business in self.businesses:
				if name == business.text:
					return True

			# Look in current business
			if name == self.current_business.text:
				return True
			return False

	def select_business(self, name):
		"""If not current business, select business matching name
			If current, close menu"""
		if self.get_role() == 'employer':
			# check if name is current business
			if name == self.get_current_business():
				return True
			# check if there's other businesses
			self.open()
			if self.is_default_employer_view():
				self.click_current_business()
			for business in self.businesses:
				if business.text == name:
					business.click()
					#drawer_selBus title changes, alert pop-up appears
					time.sleep(.8)
					return True
			return False
		else:
			self.close()
			time.sleep(.4)

	def get_current_business(self):
		# return text of self.current_busines
		if self.get_role() == 'employer':
			if self.get_menu_status() == 'skinny':
				self.open()
			if self.current_business.is_displayed():
				return self.current_business.text
			else:
				# returns '' as text for hidden elements.
				# Get innerHTML and parse react stuff
				el = self.current_business.find_elements_by_tag_name('div')[1]
				script = 'return arguments[0].innerHTML;'
				innerHTML = self.driver.execute_script(script, el)

				text = self.parseReactText(innerHTML)
				return text

	def parseReactText(self, innerHTML):
		beg_index = innerHTML.find('-->')+3
		end_index = innerHTML.find('<!--', beg_index)
		return innerHTML[beg_index: end_index]

########################## Role Switching Functions ###########################

	def set_role(self, role):
		# Switch to given role (if role switch visible and not on given role)
		# test should handle loading new page (also reloads menu)
		if not self.is_drawer_visible():
			self.open()
		if self.user_can_switch_roles() and self.get_role() != role.lower():
			self.role_switch.click()
			WDW(self.driver, 10).until_not(
				EC.presence_of_element_located((By.CLASS_NAME, 'animated')))

	def user_can_switch_roles(self):
		# Return if user has ability to switch roles (role_switch is visible)

		if self.role_switch is not None:
			return True
		return False

	def get_role(self):
		# Return 'employee' or 'employer' depending on current role
		# will open the drawer on mobile
		if not main.is_desktop():
			self.open()
		try:
			if self.eHome is None:
				return 'employer'
		except AttributeError:
			# If current business is selected self.eHome isn't initialized
			return 'employer'
		return 'employee'

############################## General Functions ##############################

	def toggle(self):
		"""Only on desktop. Toggle between full/skinny menu"""
		if main.is_desktop():
			self.toggle_button.click()
			time.sleep(.2)
			self.load(hamburger=False, loading_page=False)

	def get_menu_status(self):
		"""Desktop: 'open' or 'skinny'
			Mobile: 'open' or 'closed'"""
		if main.is_desktop(): # desktop: 'open' or 'skinny'
			# check val of 'd' attribute on button's <path>
			# wide = "M15.41 16.09l-4.58-4.59 4.58-4.59L14 5.5l-6 6 6 6z"
			wide = "M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"
			# skinny = "M8.59 16.34l4.58-4.59-4.58-4.59L10 5.75l6 6-6 6z"
			skinny = "M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"

			path_el = self.toggle_button.find_element_by_tag_name('path')
			val = path_el.get_attribute('d')
			if val == wide:
				return 'open'
			elif val == skinny:
				return 'skinny'
			else:
				raise Exception('unexpected val in path element')

		else: # mobile: 'open' or 'closed'
			if self.is_drawer_visible():
				return 'open'
			return 'closed'

	def open(self):
		"""Mobile: make sure drawer is 'open'"""
		# desktop: make sure menu is 'open'
		if not main.is_desktop() and not self.is_drawer_visible():
			self.hamburger.click()
			WDW(self.driver, 2).until(
				EC.element_to_be_clickable((By.CLASS_NAME, 'drawer_profile')))
			# WDW(self.driver, 2).until(
			# 	EC.element_to_be_clickable((By.CLASS_NAME, 'drawer_support')))
			self.load(hamburger=False, loading_page=False)

			# make sure menu starts at top
			self.driver.execute_script("window.scrollTo(0, 0)")
			time.sleep(.4)
		elif main.is_desktop() and self.get_menu_status() == 'skinny':
			self.toggle()
			WDW(self.driver, 10).until(lambda x: self.get_menu_status() != 'skinny')
			self.load(hamburger=False, loading_page=False)

	def close(self, action='click'):
		if self.is_drawer_visible():
			if not main.is_desktop():
				# ios: Base coordinates off window.innerWidth/innerHeight
				# y position needs to be lower than browser header
				web_width = self.driver.execute_script('return window.innerWidth')
				click_x = web_width - 10
				click_y = 100
				duration = 100 # milliseconds

				# Android: TA only works in NATIVE view
				if main.is_android():
					# go to native context
					main.native_context(self.driver)

					# use native dimensions (different from webview dimensions)
					native_dimensions = self.driver.get_window_size()
					native_width = native_dimensions['width']

					click_x = native_width - 10
					# needs bigger value than WEBVIEW (to avoid clicking URL)
					click_y = 300


				if action == 'click': # Either option should work
					# position = [(click_x, click_y)]
					# self.driver.tap(position, duration)
					TA(self.driver).tap(x=click_x, y=click_y).perform()
					# 2nd click opens /account-detail on iOS native
					# TA(self.driver).tap(x=click_x, y=click_y).perform()
				elif action == 'swipe':
					# Either option should work
					# second set of coordinates are RELATIVE to click position

					# self.driver.swipe(click_x, click_y, -300, 0, duration)
					TA(self.driver).press(x=click_x, y=click_y).wait(
						duration).move_to(x=-200, y=0).release().perform()

				# back to webview context
				if main.is_android():
					main.webview_context(self.driver)

				# wait until drawer disappears
				WDW(self.driver, 10).until(lambda x: not self.is_profile_loaded())
			else: # Press escape
				self.toggle_button.click()

	def is_drawer_visible(self, loading_page=False):
		# this gets called a bunch of different places.
		# loading_page should be true when we're loading a page. load()
		try:
			# try to look for drawer container.
			drawer = self.driver.find_element_by_class_name('drawer_cont')
			# Then try and look for profile element (seems to load slower)
			WDW(self.driver, 1).until(lambda x: self.is_profile_loaded())
		except (NoSuchElementException, IndexError, TimeoutException) as e:
			# drawer does not exist
			return False

		# Mobile: no guarantee drawer will stay open.
		# will be temporarily visible if it's in the process of closing.
		if not main.is_desktop() and loading_page:
			# does drawer close within 1.5 seconds?
			try:
				WDW(self.driver, 2).until(lambda x: not self.is_profile_loaded())
				# drawer closed
				return False
			except TimeoutException:
				# drawer stayed open
				pass
		return True

	def is_profile_loaded(self):
		# Profile seems to load slower than rest of menu. Assume once this shows up that menu is completed.
		try:
			profile = self.driver.find_element_by_class_name('drawer_profile')
			return True
		except NoSuchElementException:
			return False

		# employer_profile = self.driver.find_elements_by_class_name('drawer_empSet')
		# if employee_profile == [] and employer_profile == []:
		# 	# profile not loaded
		# 	return False
		# return True

	def sign_out(self):
		self.hamburger = self.try_load_hamburger()
		self.open()
		self.click_option('sign out')
		self.confirm_sign_out()

	def confirm_sign_out(self):
		# mobile personal settings page has extra sign out option
		button = self.driver.find_element_by_class_name('logout_ok')
		button.click()
		try:
			if main.is_web():
				# Goes to home page
				# WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'contactEmail2')))
				WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'empEnroll')))
			else: # Native: goes to signin page
				 WDW(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit_si_button')))
		except TimeoutException:
			raise Exception("Menu: Could not find expected element after logout.")

	def click_option(self, option, forceWide=False):
		# don't use for...
		# logging out, clicking current business, adding business, switch roles

		# forceWide: make sure menu is open on desktop (not skinny)
		if not main.is_desktop() or forceWide:
			self.open()

		# make sure 'current business' isn't selected
		if self.add_button is not None:
			self.click_current_business()
		try:
			menu_option = self.option_els[option.lower()]
			if menu_option is not None:
				# scroll to option on mobile
				if not main.is_desktop():
					script = "arguments[0].scrollIntoView();"
					self.driver.execute_script(script, menu_option)
				menu_option.click()
		except IndexError:
			raise Exception('click_option(): Invalid menu option index')


	def is_option_selected(self, option):
		# does given option have white background in drawer?
		# assumes drawer is open
		try:
			menu_option = self.option_els[option.lower()]
			bg_color = menu_option.value_of_css_property('background-color')
			color = menu_option.value_of_css_property('color')
			# white background, blue text

			# returns different values depending on enviroment
			if 'rgba' in bg_color:
				if (bg_color == 'rgba(255, 255, 255, 1)' and
					color == 'rgba(56, 217, 244, 1)'):
					return True
			else: # safari desktop returns rgb
				if (bg_color == 'rgb(255, 255, 255)' and
					color == 'rgb(56, 217, 244)'):
					return True

			# print(bg_color)
			# print(color)
			return False
		except IndexError:
			raise Exception('is_option_selected(): Invalid menu option index')


############################# A/B functions ###################################

	def is_ab_open(self):
		# return True if A/B popup is visible
		try:
			ab_opt = self.driver.find_element_by_id('toggleCheck')
			return True
		except NoSuchElementException:
			return False

	def open_ab(self):
		# If A/B popup closed, click version 4 times to open
		if not self.is_ab_open():
			for i in xrange(4):
				self.version.click()

	def close_ab(self):
		# if A/B popup open, click cancel button
		if self.is_ab_open():
			cancel = self.driver.find_element_by_class_name('logout_cancel')
			cancel.click()

	def get_ab_options(self):
		# Return current A/B testing options
		self.open()
		if not self.is_ab_open():
			self.open_ab()
			WDW(self.driver, 10).until(
				EC.presence_of_element_located((By.ID, 'confirmCheck')))
		opts = {
			'toggle': self.get_ab_value('toggleCheck'),
			'dialog': self.get_ab_dialog('confirmCheck')
		}
		return opts

	def get_ab_checkbox(self, checkbox_id):
		try:
			return self.driver.find_element_by_id(checkbox_id)
		except NoSuchElementException:
			raise Exception('Incorrect checkbox_id. Could not find A/B option')

	def get_ab_value(self, checkbox):
		# Return True if given A/B option is checked
		# assumes drawer is open
		# 1. toggleCheck: sending has toggle (vs radio) for setting send speed
		# 2. confirmCheck: shows confirmation popup after sending
		if not self.is_ab_open():
			self.open_ab()

		return self.get_ab_checkbox(checkbox_id).is_enabled()

	def set_ab_value(self, checkbox_id, value=True):
		# given id of A/B checkbox and True/False, set given option.
		self.open()
		if not self.is_ab_open():
			self.open_ab()
			WDW(self.driver, 10).until(
				EC.presence_of_element_located((By.ID, 'confirmCheck')))

		checkbox = self.get_ab_checkbox(checkbox_id)

		# toggle checkbox if current value doesn't equal desired value
		if checkbox.is_selected() != value:

			#sometimes have click issues because checkbox opacity=0
			# currently have issues on Safari (desktop, maybe mobile)
			# todo: clickFunction
			if main.get_browser() == 'safari':
				script = 'arguments[0].click();'
				self.driver.execute_script(script, checkbox)
			else:
				checkbox.click()
			WDW(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'logout_ok')))
			self.driver.find_element_by_class_name('logout_ok').click()
			WDW(self.driver, 10).until_not(
				EC.visibility_of_element_located((By.CLASS_NAME, 'logout_ok')))
		else:
			# close A/B popup
			WDW(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'logout_cancel')))
			self.driver.find_element_by_class_name('logout_cancel').click()
			WDW(self.driver, 10).until_not(
				EC.visibility_of_element_located((By.CLASS_NAME, 'logout_cancel')))

		# Make sure confirmation dialog didn't show back up
		self.clear_confirmation_dialog()

		self.close()

	def clear_confirmation_dialog(self):
		# If you re-enable confirmation dialog A/B after sending transfer while on eHome
		# You'll probably get confirmation dialog show up.
		try:
			el = self.driver.find_element_by_id('confirmOkButton')
			el.click()
			WDW(self.driver, 10).until_not(
				EC.visibility_of_element_located((By.CLASS_NAME, 'logout_cancel')))
		except NoSuchElementException:
			pass

