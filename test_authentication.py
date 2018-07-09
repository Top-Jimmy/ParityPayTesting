import random
import string
import time
import unittest
import main
import browser
import profiles
import messages
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

	# Total - 13
	# TestForgotPassword - 4    Reset PW, Homepage links
	#     -test_invalid_inputs  expectedFailure, Bug: 145647407, INVALID
	#     -test_links
	#     -test_required_fields
	#     -test_success
	# TestLogin - 8             Login
	#     -test_action_success      (only on mobile web)
	#     -test_native_signin_success (only on native)
	#     -test_signin_success      (only on web)
	#     -test_dropdown_success       (only on desktop)
	#     -test_invalid_credentials
	#     -test_required_fields
	#     -test_invalid_inputs
	#     -test_logout_success
	# TestRemember - 1					Remember me
			# -test_remember_me

class TestForgotPassword(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.alone1 = profiles.Profile(self.driver, 'alone1')
		self.WDWait = WebDriverWait(self.driver, 15)

	def tearDown(self):
		self.driver.quit()

	# @unittest.skipIf(main.get_priority() < 3)
	@unittest.skip("S3 - Email input validation. Bug #145647407")
	def test_invalid_inputs(self):
		"""authentication : Forgot Password .           test_invalid inputs"""
		# assert inputs on 'Reset Password' page handle invalid credentials

		credentials = self.nicol.credentials
		signin_page = self.nicol.signin_page
		reset_page = self.nicol.reset_password_page
		email_page = self.nicol.reset_password_email_page

		# go to reset password page
		if main.is_web():
			self.assertTrue(reset_page.go())
		else:
			self.assertTrue(signin_page.on())
			signin_page.click_password_reset()
			self.assertTrue(reset_page.on())

		invalid_emails = ['invalid', 'invalid@', 'invalid.com','invalid@examplec.om']
		error = "Invalid email address"
		for email in invalid_emails:
			reset_page.set_email(email)
			reset_page.click_continue()
			time.sleep(.8)
			self.assertEqual(   # /reset-password validation fails
				1, reset_page.number_of_elements('div', error)) #Failed 6/6 3:49pm Accepts invalid inputs. Logged.
		invalid_phones = ['1234567890', '801123456']
		for phone in invalid_phones:
			error = (
				"\"{phone}\" is not a valid phone number in the United States."
			)
			reset_page.set_email(phone)
			reset_page.click_reset_password()
			time.sleep(.8)
			self.assertEqual(1, reset_page.number_of_elements(
				'div', error.format(phone=phone)))
		dne_ids = ['(801) 890-1234', 'notanemail@none.com']
		for dne_id in dne_ids:
			reset_page.request(dne_id)
			time.sleep(.8)
			self.assertTrue(reset_page.no_user_found(dne_id))
		reset_page.request(credentials['email'])

		email_page.load()
		email_page.set_passwords('a')
		email_page.click_continue()
		error = "Shorter than minimum length 8"
		self.assertEqual(1, email_page.number_of_elements('div', error))
		#No matching passwords check...
		'''error = "The passwords must match."
		email_page.set_password('ab')
		self.assertEqual(1, email_page.number_of_elements('div', error))'''

	# 'wrong credential' link removed. Not really worth testing
	# @unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	# def test_links(self):
	# 	"""authentication : Forgot Password .                   test_links"""
	# 	# assert 'Forgot Password' links are mapped as expected
	# 	credentials = self.nicol.credentials
	# 	signin_page = self.nicol.signin_page
	# 	reset_page = self.nicol.reset_password_page
	# 	code_page = self.nicol.reset_password_code_page
	# 	new_page = self.nicol.reset_password_new_page

	# 	# go to reset password page
	# 	if main.is_web():
	# 		self.assertTrue(reset_page.go())
	# 	else:
	# 		self.assertTrue(signin_page.on())
	# 		signin_page.click_password_reset()
	# 		self.assertTrue(reset_page.on())

	# 	self.assertTrue(reset_page.on())
	# 	reset_page.set_email(credentials['email'])
	# 	reset_page.click_continue()

	# 	self.assertTrue(code_page.on())
	# 	# Don't have wrong link at the moment
	# 	# code_page.click_wrong_link()

	# 	# self.assertTrue(reset_page.on())
	# 	# reset_page.set_email(credentials['email'])
	# 	# reset_page.click_continue()

	# 	# self.assertTrue(code_page.on())
	# 	code_page.enter_code()

	# 	self.assertTrue(code_page.on())
	# 	code_page.click_wrong_link()
	# 	if not reset_page.on():
	# 		# not sure why, sometimes 1st click doesn't work
	# 		code_page.click_wrong_link()

	# 	self.assertTrue(reset_page.on())
	# 	reset_page.set_email(credentials['email'])
	# 	reset_page.click_continue()

	# 	self.assertTrue(code_page.on()) # check your email
	# 	code_page.enter_code()

	# 	self.assertTrue(code_page.on()) # check your phone
	# 	code_page.enter_code()

	# 	self.assertTrue(new_page.on())

	@unittest.skipIf(main.get_priority() < 3, "Priority = 3")
	def test_required_fields(self):
		"""authentication : Forgot Password .          test_required fields"""
		# assert inputs on 'Reset Password' page are required as expected
		# Sometimes creates test-specific sendmi error message. Hits backend wierd?
		credentials = self.nicol.credentials
		signin_page = self.nicol.signin_page
		reset_page = self.nicol.reset_password_page
		code_page = self.nicol.reset_password_code_page
		new_page = self.nicol.reset_password_new_page
		lobby_page = self.nicol.lobby_page

		# go to reset password page
		if main.is_web():
			self.assertTrue(reset_page.go())
		else:
			self.assertTrue(signin_page.on())
			signin_page.click_password_reset()
			self.assertTrue(reset_page.on())

		self.assertTrue(reset_page.on())
		reset_page.click_continue()
		tag = 'p'
		error = "Required"
		error_count = reset_page.number_of_elements
		self.assertEqual(1, error_count(tag, error))
		reset_page.set_email('notanemail@none.com')
		# iOS: Sending keys does not remove 'required' error
		if not main.is_ios():
			self.assertEqual(0, error_count(tag, error))
		reset_page.set_email(credentials['email'])
		reset_page.click_continue()

		self.assertTrue(code_page.on())
		code_page.enter_code()
		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(new_page.on())
		new_page.click_continue()
		self.assertEqual(1, error_count(tag, error))
		new_page.set_password(credentials['password'])
		# iOS: Sending keys does not remove 'required' error
		if not main.is_ios():
			self.assertEqual(0, error_count(tag, error))
		new_page.click_continue()
		WebDriverWait(self.driver, 15).until(lambda x: EC.visibility_of_element_located(
			(By.CLASS_NAME, 'invitations_card')) or
			EC.visibility_of_element_located((By.ID, 'cash-bar'))
		)
		#raw_input('page?')
		self.assertTrue(lobby_page.on())

	def test_success(self):
		"""authentication : Forgot Password .                 test_success"""
		# assert "Forgot Password" functionality works as expected
		credentials = self.alone1.credentials
		reset_page = self.alone1.reset_password_page
		code_page = self.alone1.reset_password_code_page
		new_page = self.alone1.reset_password_new_page
		eHome = self.alone1.eHome_page
		election_page = self.alone1.pay_election_page
		ps_page = self.alone1.ps_page
		change_pw_page = self.alone1.ps_change_pw_page
		signin_page = self.alone1.signin_page

		# go to reset password page
		if main.is_web():
			reset_page.go()
		else:
			self.assertTrue(signin_page.on())
			signin_page.click_password_reset()
			self.assertTrue(reset_page.on())

		self.assertTrue(reset_page.on())
		reset_page.set_email(credentials["email"])
		reset_page.click_continue()
		self.assertTrue(code_page.on())
		code_page.enter_code()
		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(new_page.on())
		new_password = "asdfasdf1"
		new_page.enter_password(new_password)
		#Backend error here, timed out because of it.
		# WebDriverWait(self.driver, 15).until(
		# 	EC.presence_of_element_located((By.ID, 'save_election_button')))

		# Reset password through settings page.
		self.assertTrue(eHome.on('election'))
		eHome.menu.sign_out()

		self.assertTrue(self.alone1.login(self.driver, new_password), messages.login)
		# Currently no election for Stand Alone1, should go to eleciton page.
		self.assertTrue(election_page.on())
		election_page.menu.click_option('settings')
		self.assertTrue(ps_page.on())
		ps_page.change_password()
		self.assertTrue(change_pw_page.on())
		change_pw_page.enter_current_pw(new_password)
		change_pw_page.enter_new_pw(credentials["password"])
		change_pw_page.click_continue()
		self.assertTrue(ps_page.on())
	test_success.e2e = True


class TestLogin(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.nicol = profiles.Profile(self.driver,'nicol')
		self.WDWait = WebDriverWait(self.driver, 15)

	def tearDown(self):
		self.driver.quit()

	@unittest.skipIf(not main.is_web() or main.is_desktop() or main.get_priority() < 2,
		'Only get action menu on mobile web')
	def test_action_success(self):
		"""authentication : Login .                    test_action success"""
		# assert user can login through action menu
		credentials = self.nicol.credentials
		for_employers = self.nicol.for_employers
		signin_page = self.nicol.signin_page
		signin_code_page = self.nicol.signin_code_page
		lobby_page = self.nicol.lobby_page

		for_employers.go()
		self.assertTrue(for_employers.on())
		for_employers.header.select_action('Sign In')

		self.assertTrue(signin_page.on())
		signin_page.set_email(credentials['email'])
		signin_page.set_password(credentials['password'])
		signin_page.click_login()

		if signin_code_page.on(): # remember user?
			signin_code_page.enter_code()

		self.assertTrue(lobby_page.on())

	@unittest.skipIf(not main.is_desktop() or main.get_priority() < 2,
		'Signin dropdown only on desktop')
	def test_dropdown_success(self):
		"""authentication : Login .                  test_dropdown success"""
		# assert can login through signin dropdown
		credentials = self.nicol.credentials
		for_employers = self.nicol.for_employers
		signin_code_page = self.nicol.signin_code_page
		lobby_page = self.nicol.lobby_page

		for_employers.go()
		self.assertTrue(for_employers.on())
		for_employers.header.set_sign_in_email(credentials['email'])
		for_employers.header.set_sign_in_pw(credentials['password'])
		for_employers.header.click_login()

		self.assertTrue(signin_code_page.on())
		signin_code_page.enter_code()

		if signin_code_page.on(): # remember user?
			self.assertTrue(signin_code_page.enter_code())

		self.assertTrue(lobby_page.on())

	@unittest.skipIf(main.get_priority() < 3, "Priority = 3")
	def test_invalid_credentials(self):
		"""authentication : Login .              test_invalid credentials"""
		# assert 'Sign In' page inputs properly handle invalid credentials
		credentials = self.nicol.credentials
		signin_page = self.nicol.signin_page

		if main.is_web():
			signin_page.go()
		else:
			self.assertTrue(signin_page.on())

		signin_page.set_email(credentials['email'])
		signin_page.set_password(credentials['password'] + '0')
		signin_page.click_login()
		self.WDWait.until(EC.presence_of_element_located((By.ID, 'sendmi_error')))
		error = "Incorrect password, email address, or phone number."
		self.assertTrue(error in signin_page.read_error())

		signin_page.set_email('abc' + credentials['email'])
		signin_page.set_password(credentials['password'])
		signin_page.click_login()
		self.WDWait.until(EC.presence_of_element_located((By.ID, 'sendmi_error')))
		self.assertTrue(error in signin_page.read_error())

	@unittest.skipIf(main.get_priority() < 3, "Priority = 3")
	def test_invalid_inputs(self):
		"""authentication : Login .                    test_invalid inputs"""
		# Running this test > once might put your computer out of commission for
		# 15 minutes because it thinks you're trying to hack into accounts

		# assert 'Sign In' page handles invalid input as expected
		#Needs
		credentials = self.nicol.credentials
		signin_page = self.nicol.signin_page

		if not main.is_web():
			self.assertTrue(signin_page.on())
		else:
			signin_page.go()
		signin_page.set_password(credentials['password'])
		invalid_emails = ['invalid', 'invalid@', 'invalid.com']

		containers = ["div","p","div"]
		# errors = ["Incorrect password, email address, or phone number.",
		# 	"Please enter a valid email address, mobile phone number, or username.",
		# 	"Incorrect password, email address, or phone number."
		# ]
		error = "Please enter a valid email address."
		# errors = ["Incorrect password, email address, or phone number.",
		# 	"Please enter a valid email address.",
		# 	"Incorrect password, email address, or phone number."
		# ]
		for i, email in enumerate(invalid_emails):
			signin_page.set_email(email)
			signin_page.click_login()
			signin_page.check_captcha()

			# Wait for errors to show up
			if i == 1: # email input error
				# Validation changed on form at some point 4/10/2018
				# Fails to submit, but no error.
				pass
				# print('i: ' + str(i))
				# self.WDWait.until(
				# 	EC.text_to_be_present_in_element((By.ID, 'signin_form_user_helper'),
				# 		errors[i]))
			else: # form error
				print('i= ' + str(i))
				self.WDWait.until(
					EC.text_to_be_present_in_element((By.ID, 'sendmi_error'),
						error))

				self.assertEqual(1, signin_page.number_of_elements('span', error))

		invalid_phones = ['1234567890', '801123456']
		for phone in invalid_phones:
			error = "Please enter a valid email address, mobile phone number, or username."
			signin_page.set_email(phone)
			signin_page.click_login()

			# Validation changed on form at some point 4/10/2018
			# Fails to submit, but no error.
			# self.WDWait.until(
			# 	EC.text_to_be_present_in_element((By.ID, 'signin_form_user_helper'),
			# 		error))

			# self.assertEqual(1, signin_page.number_of_elements('p', error))

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_logout_success(self):
		"""authentication : Login .                   test_logout success"""
		# assert menu 'Sign Out' works as expected
		credentials = self.nicol.credentials
		for_employers = self.nicol.for_employers
		signin_page = self.nicol.signin_page
		lobby_page = self.nicol.lobby_page

		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.sign_out()
		if main.is_web():
			self.assertTrue(for_employers.on())
		else:
			self.assertTrue(signin_page.on())

	@unittest.skipIf(main.is_web() or main.get_priority() < 2,
	 'Test for native only')
	def test_native_signin_success(self):
		"""authentication : Login .            test_native signin success"""
		# assert can login through footer 'Sign In' link
		credentials = self.nicol.credentials
		signin_page = self.nicol.signin_page
		signin_code_page = self.nicol.signin_code_page

		self.assertTrue(signin_page.on())
		signin_page.set_email(credentials['email'])
		signin_page.set_password(credentials['password'])
		signin_page.click_login()

		self.assertTrue(signin_code_page.on())
		signin_code_page.enter_code()

	# Form validation changed at some point and none of these errors show up anymore
	@unittest.skip("Validation removed on signin form")
	def test_required_fields(self):
		"""authentication : Login .                 test_required fields"""
		# assert 'Sign In' page inputs are required as expected
		credentials = self.nicol.credentials
		signin_page = self.nicol.signin_page

		if not main.is_web():
			self.assertTrue(signin_page.on())
		else:
			signin_page.go()
		signin_page.click_login()

		error = 'Required'
		num_errors = 2
		self.WDWait.until(
			EC.text_to_be_present_in_element((By.ID, 'signin_form_user_helper'),
				error))
		self.assertEqual(2, signin_page.number_of_elements('p', error))

		# ios can't tell that email was updated so there's still 2 errors
		if not main.is_ios():
			signin_page.set_email(credentials['email'])
			self.WDWait.until(
				EC.text_to_be_present_in_element((By.ID, 'signin_form_pw_helper'),
					error))
			num_errors = 1
			self.assertEqual(1, signin_page.number_of_elements('p', error))
			signin_page.set_password(credentials['password'])

			self.assertEqual(0, signin_page.number_of_elements('p', error))

	@unittest.skipIf(not main.is_web() or main.get_priority() < 2,
	 'Test for web only')
	def test_signin_success(self):
		"""authentication : Login .                    test_signin success"""
		# assert can login through footer 'Sign In' link
		credentials = self.nicol.credentials
		for_employers = self.nicol.for_employers
		signin_page = self.nicol.signin_page
		signin_code_page = self.nicol.signin_code_page
		lobby_page = self.nicol.lobby_page

		for_employers.go()
		self.assertTrue(for_employers.on()) #scrollTo element.
		for_employers.footer.click_link('sign in')

		self.assertTrue(signin_page.on())
		self.assertTrue(signin_page.is_public())
		signin_page.set_email(credentials['email'])
		signin_page.set_password(credentials['password'])
		signin_page.click_login()

		self.assertTrue(signin_code_page.on())
		self.assertTrue(signin_code_page.is_public())
		signin_code_page.enter_code()


class TestRemember(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.nicol = profiles.Profile(self.driver,'nicol')

	def tearDown(self):
		self.driver.quit()

	# @unittest.skipIf(not main.is_web(), 'For web only')
	def test_remember_me(self):
		"""authentication : Remember .                    test_remember_me"""
		# Web: Remember me functionality works as expected
		# Native: Remember me functionality works automatically
		credentials = self.nicol.credentials
		for_employers = self.nicol.for_employers
		signin_page = self.nicol.signin_page
		signin_code_page = self.nicol.signin_code_page
		lobby_page = self.nicol.lobby_page

		# Login and 'remember me'
		if main.is_web():
			for_employers.go()
			self.assertTrue(for_employers.on()) #scrollTo element.
			for_employers.footer.click_link('sign in')

		self.assertTrue(signin_page.on())
		self.assertTrue(signin_page.is_public())
		signin_page.set_email(credentials['email'])
		signin_page.set_password(credentials['password'])
		signin_page.click_login()

		self.assertTrue(signin_code_page.on())
		self.assertTrue(signin_code_page.is_public())
		# Remember me should work automatically on native app
		if main.is_web():
			signin_code_page.click_remember()
		signin_code_page.enter_code()
		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'invitations_card')))

		self.assertTrue(lobby_page.on())
		lobby_page.menu.sign_out()

		# Sign back in. Should remember and skip code page
		if main.is_web():
			self.assertTrue(for_employers.on())
			for_employers.footer.click_link('sign in')
		self.assertTrue(signin_page.on())
		self.assertTrue(signin_page.is_public())
		signin_page.set_email(credentials['email'])
		signin_page.set_password(credentials['password'])
		signin_page.click_login()

		self.assertTrue(lobby_page.on())
