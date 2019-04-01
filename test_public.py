import unittest
import profiles
import browser
import time
import main
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Total - 12
	# TestContactFlow - 2
	# -test_invalid_inputs
	# -test_required_fields
	# TestForEmployees - 4
	#    -test_about_page
	#    -test_contact_us_page
	#    -test_for_employees_page
	#    -test_for_employees_buttons
	# TestForEmployers - 6
	#    -test_demo_form
	#    -test_for_employers_page
	#    -test_invalid_inputs
	#    -test_required_fields
	#    -test_success_existing
	#		 -test_success_new

@unittest.skipIf(not main.is_web() or main.get_priority() < 3, 'Priority')
class TestContactFlow(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.WDWait = WebDriverWait(self.driver, 10)	#Timeout after 10 sec.

	def tearDown(self):
		self.driver.quit()

	def test_invalid_inputs(self):
		""" test_public.py:TestContactFlow.test_invalid_inputs """
		# assert "Contact Flow" fields correctly handle invalid input
		credentials = self.nicol.credentials
		for_employees = self.nicol.for_employees
		map_page = self.nicol.contact_map_page
		form_page = self.nicol.contact_form_page

		for_employees.go()
		self.assertTrue(for_employees.on())

		for_employees.enter_contact_email(credentials['email'])

		self.assertTrue(map_page.on())
		map_page.add('Nintendo of America 98052')

		self.assertTrue(form_page.on())
		form_page.set_name('Test Request')
		invalid_phones = ['1234567890', '801123456']
		error = (
			"\"{phone}\" is not a valid phone number in US."
			)

		for phone in invalid_phones:
			form_page.set_phone(phone)
			form_page.click_continue()
			self.WDWait.until(
				EC.text_to_be_present_in_element((By.ID, 'phone_helper'),
					error.format(phone=phone))
			)
			self.assertEqual(1, form_page.number_of_elements(
			'p', error.format(phone=phone)))

	def test_required_fields(self):
		""" test_public.py:TestContactFlow.test_required_fields """
		# assert "Contact Flow" fields are required as expected
		credentials = self.nicol.credentials
		for_employees = self.nicol.for_employees
		map_page = self.nicol.contact_map_page
		form_page = self.nicol.contact_form_page

		for_employees.go()
		self.assertTrue(for_employees.on())
		for_employees.click_contact_continue()
		self.assertTrue(for_employees.has_contact_form_error())
		self.assertTrue(for_employees.on())
		for_employees.enter_contact_email(credentials['email'])

		self.assertTrue(map_page.on())
		map_page.add('Nintendo of America 98052')

		self.assertTrue(form_page.on())
		self.assertFalse(form_page.continue_button.is_enabled())
		error = 'Required'

		self.assertEqual(0, form_page.number_of_elements('p', error))
		form_page.set_name('')
		# ios: need to remove focus from name input to get required error
		form_page.set_phone('')
		self.assertFalse(form_page.continue_button.is_enabled())

		form_page.click_continue()
		self.WDWait.until(
			EC.text_to_be_present_in_element((By.ID, 'name_helper'), error))
		self.assertEqual(1, form_page.number_of_elements('p', error))


@unittest.skipIf(not main.is_web(),"No public About page on native")
class TestForEmployees(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	def test_about_page(self):
		""" test_public.py:TestForEmployees.test_about_page """
		# assert about page links and forms work as expected
		for_employers = self.nicol.for_employers
		for_employees = self.nicol.for_employees
		about_page = self.nicol.about_public_page
		map_page = self.nicol.contact_map_page

		for_employers.go()
		for_employers.footer.click_link('about us')

		# header logo
		self.assertTrue(about_page.on())
		about_page.header.click_logo()
		self.assertTrue(for_employers.on())
		for_employers.footer.click_link('about us')

		# header employee and employers buttons
		self.assertTrue(about_page.on())
		about_page.click_employee_button()

		self.assertTrue(for_employees.on())
		for_employees.footer.click_link('about us')

		# page 'employers' learn more button
		self.assertTrue(about_page.on())
		about_page.click_employer_button()
		self.assertTrue(for_employers.on())
		for_employers.footer.click_link('about us')

		# page invite employer form
		self.assertTrue(about_page.on())
		about_page.enter_invite_employer_email('')
		error_msg = 'Your email address is required to continue'
		self.WDWait.until(
			EC.text_to_be_present_in_element((By.CLASS_NAME, 'error_textbox'),
			error_msg)
		)
		num_errors = about_page.number_of_elements
		self.assertEqual(1,num_errors('span', error_msg))
		about_page.enter_invite_employer_email('bogus@example.com')
		self.assertTrue(map_page.on())

	def test_contact_us_page(self):
		""" test_public.py:TestForEmployees.test_contact_us_page """
		# assert Contact Us page links and forms work as expected
		for_employers = self.nicol.for_employers
		contact_page = self.nicol.contact_us_page
		map_page = self.nicol.contact_map_page

		for_employers.go()
		for_employers.footer.click_link('contact us')

		# header logo
		self.assertTrue(contact_page.on())
		contact_page.header.click_logo()
		self.assertTrue(for_employers.on())
		for_employers.footer.click_link('contact us')

		# header employee and employers buttons
		self.assertTrue(contact_page.on())
		if main.is_desktop():
			contact_page.header.click_for_employers()
			self.assertTrue(for_employers.on())
			for_employers.footer.click_link('contact us')

			self.assertTrue(contact_page.on())
			contact_page.header.click_for_employers()
		else:
			contact_page.header.select_action('employers')
			self.assertTrue(for_employers.on())
			for_employers.footer.click_link('contact us')

			self.assertTrue(contact_page.on())
			contact_page.header.select_action('employers')
		self.assertTrue(for_employers.on())
		for_employers.footer.click_link('contact us')

		# page invite employer form
		self.assertTrue(contact_page.on())
		contact_page.enter_invite_employer_email('')
		error_msg = 'Your email address is required to continue'
		self.WDWait.until(
			EC.text_to_be_present_in_element((By.CLASS_NAME, 'error_textbox'),
			error_msg)
		)
		num_errors = contact_page.number_of_elements
		self.assertEqual(1, num_errors('span', error_msg))
		contact_page.enter_invite_employer_email('bogus@example.com')
		self.assertTrue(map_page.on())

	def test_for_employees_page(self):
		""" test_public.py:TestForEmployees.test_for_employees_page """
		for_employees = self.nicol.for_employees
		contact_page = self.nicol.contact_us_page
		for_employers = self.nicol.for_employers
		code_page = self.nicol.reset_password_code_page
		signin_page = self.nicol.signin_page
		reset_page = self.nicol.reset_password_page
		about_page = self.nicol.about_public_page
		pub_terms_page = self.nicol.pub_terms_page
		pub_privacy_page = self.nicol.pub_privacy_page
		map_page = self.nicol.contact_map_page
		form_page = self.nicol.contact_form_page
		credentials = self.nicol.credentials

		for_employers.go()
		self.assertTrue(for_employers.on())
		for_employers.header.click_for_employees()
		self.assertTrue(for_employees.on())

		# for employers link
		if main.is_desktop():
			for_employees.header.click_for_employers()
		else:
			self.assertTrue(for_employees.header.select_action('employers'))

		self.assertTrue(for_employers.on())
		for_employers.header.click_for_employees()
		self.assertTrue(for_employees.on())

		# sign in/forgot pw
		if main.is_desktop():
			self.assertFalse(for_employees.header.sign_in_open())
			for_employees.header.sign_in_submit('', '')
			for_employees.header.sign_in_submit('asdf', 'asdf2', False)
			for_employees.header.forgot_password_submit('7774563334')
			
		else:
			self.assertTrue(for_employees.header.select_action("sign in"))
			self.assertTrue(signin_page.on())
			signin_page.signInForm.submit('asdf', 'asdf2', False)
			signin_page.signInForm.forgot_password()
			self.assertTrue(reset_page.on())
			reset_page.submit('7774563334')

		self.assertTrue(code_page.on())
		code_page.header.click_logo()
		self.assertTrue(for_employers.on())
		for_employers.header.click_for_employees()
		self.assertTrue(for_employees.on())

		# contact us form
		email = credentials['email']
		for_employees.set_contact_email(email)
		self.assertEqual(email,for_employees.get_contact_email())
		for_employees.click_contact_continue()
		self.assertTrue(map_page.on())
		map_page.header.click_logo()
		self.assertTrue(for_employers.on())
		for_employers.header.click_for_employees()
		self.assertTrue(for_employees.on())

		# footer links
		for_employees.footer.click_link('for employers')
		self.assertTrue(for_employers.on())
		for_employers.header.click_for_employees()
		self.assertTrue(for_employees.on())

		for_employees.footer.click_link('sign in')
		self.assertTrue(signin_page.on())
		signin_page.header.click_logo()
		self.assertTrue(for_employers.on())
		for_employers.header.click_for_employees()
		self.assertTrue(for_employees.on())

		for_employees.footer.click_link('about us')
		self.assertTrue(about_page.on())
		about_page.header.click_for_employees()
		self.assertTrue(for_employees.on())

		for_employees.footer.click_link('contact us')
		self.assertTrue(contact_page.on())
		contact_page.header.click_for_employees()
		self.assertTrue(for_employees.on())

		for_employees.footer.click_link('terms and conditions')
		self.assertTrue(pub_terms_page.on())
		pub_terms_page.header.click_for_employees()
		self.assertTrue(for_employees.on())

		for_employees.footer.click_link('privacy policy')
		self.assertTrue(pub_privacy_page.on())
		pub_privacy_page.header.click_for_employees()
		self.assertTrue(for_employees.on())

		# waiting: faq is demo page. Build as released

		for_employees.footer.click_link('facebook')
		for_employees.go_to_tab()
		for_employees.footer.click_link('twitter')
		for_employees.go_to_tab()
		for_employees.footer.click_link('google+')
		for_employees.go_to_tab()
		for_employees.footer.click_link('linked in')
		for_employees.go_to_tab()

	@unittest.skipIf(main.get_priority() < 2, "Priority")
	def test_for_employees_buttons(self):
		""" test_public.py:TestForEmployees.test_for_employees_buttons """
		# test buttons on home page behave as expected
		for_employers = self.nicol.for_employers
		for_employees = self.nicol.for_employees
		about_page = self.nicol.about_public_page

		# learn more button
		for_employers.go()
		for_employers.header.click_for_employees()
		self.assertTrue(for_employees.on())
		for_employees.click_learn_more()
		self.assertTrue(for_employees.employer_but.is_displayed())

		# button 1: enroll business page
		for_employees.click_page_button(1)
		self.assertTrue(for_employers.on())
		for_employers.header.click_for_employees()

		# button 2,3: home page contact form2
		self.assertTrue(for_employees.on())
		for_employees.click_page_button(2)
		self.assertTrue(for_employees.contact_forms[1].is_displayed())
		for_employees.click_page_button(3)
		self.assertTrue(for_employees.contact_forms[1].is_displayed())

		# button 4,5: about page
		for_employees.click_page_button(4)
		self.assertTrue(about_page.on())
		about_page.header.click_logo()
		self.assertTrue(for_employers.on())
		for_employers.header.click_for_employees()

		self.assertTrue(for_employees.on())
		for_employees.click_page_button(5)
		self.assertTrue(about_page.on())


@unittest.skipIf(not main.is_web() or main.get_priority() < 3, 'Priority')
class TestForEmployers(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.poli = profiles.Profile(self.driver)
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	def test_demo_form(self):
		""" test_public.py:TestForEmployers.test_demo_form """
		# assert Employers
		for_employers = self.nicol.for_employers

		for_employers.go()
		email = 'bogus@example.com'
		for_employers.enter_demo_request_email(email)
		self.assertTrue(for_employers.clear_demo_request_popup())

		self.assertTrue(for_employers.get_demo_request_email() == email)

	def test_for_employers_page(self):
		""" test_public.py:TestForEmployers.test_for_employers_page """
		credentials = self.nicol.credentials
		for_employers = self.nicol.for_employers
		code_page = self.nicol.enroll_code_page

		for_employers.go()
		self.assertTrue(for_employers.on())
		for_employers.enter_employer_email(credentials['email'])
		self.assertTrue(code_page.on())

	# @unittest.skipIf(not main.is_web(),"No home/enroll on native")
	@unittest.skip("Need regex and error handling on homepage form. Bug #150529199")
	def test_invalid_inputs(self):
		""" test_public.py:TestForEmployers.test_invalid_inputs """
		# assert inputs on "For Employers" page handle bad input as expected
		for_employers = self.nicol.for_employers
		code_page = self.nicol.enroll_code_page
		factor2_page = self.nicol.enroll_factor2_page
		name_page = self.nicol.enroll_name_page
		password_page = self.nicol.enroll_password_page
		accept_page = self.nicol.enroll_accept_page

		self.assertTrue(for_employers.go())
		error_count = for_employers.number_of_elements
		invalid_emails = ['invalid', 'invalid@', 'invalid.com',
			'invalid@.com', 'spaced out@example.com']
		invalid_phones = ['1234567890', '801123456', '7775551234', '12345678901234']
		tag = 'p'
		error = "Valid email"
		# Failing. See Bug #150529199.
		for email in invalid_emails:
			self.assertFalse(for_employers.enter_employer(email))
			self.assertEqual(error_count(tag, error))
		error = "Please enter a valid phone number"
		for phone in invalid_phones:
			self.assertFalse(for_employers.enter_employer(phone))
			# WDW until error shows up
			self.assertEqual(1, error_count(tag, error))
		self.assertTrue(for_employers.enter_employer('jbooth@example.com'))
		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(factor2_page.on())
		error_count = factor2_page.number_of_elements
		error = "Please enter a valid phone number"
		for phone in invalid_phones:
			factor2_page.enter_contact(phone)
			# WDW until error shows up
			self.assertTrue(1, error_count(tag, error))
		factor2_page.enter_contact('2024979756')

		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(name_page.on())
		error_count = name_page.number_of_elements
		error = "Name error"    #Page does not show error text.
		invalid_names = ['1234567890', '!@#$%^&*'] #Allow spaces in names?
		for name in invalid_names:
			name_page.set_first_name(name)
			name_page.set_last_name(name)
			name_page.click_continue()
			# WDW until error shows up
			self.assertEqual(2, error_count(tag, error))
		name_page.set_first_name("Jean-Michael")
		name_page.set_last_name("Jones-Mikelson")
		name_page.click_continue()

		self.assertTrue(password_page.on())
		error_count = password_page.number_of_elements
		error = "Shorter than minimum length 8"
		password_page.set_password('a')
		password_page.click_continue()
		# WDW until error shows up
		self.assertEqual(1, error_count(tag, error))
		password_page.set_password("eighty-seven")
		password_page.click_continue()

		self.assertTrue(accept_page.on())
		self.assertTrue(for_employers.go())

		for_employers.enter_employer('2024979756')
		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(factor2_page.on())
		error_count = factor2_page.number_of_elements
		error = "Please enter a valid email address."
		for email in invalid_emails:
			factor2_page.enter_contact(email)
			# WDW until error shows up
			self.assertEqual(1, error_count(tag, error))
		factor2_page.enter_contact('jbooth@example.com')

		self.assertTrue(code_page.on())

	def test_required_fields(self):
		""" test_public.py:TestForEmployers.test_required_fields """
		# assert "For Employers" page inputs are required as expected
		for_employers = self.nicol.for_employers
		code_page = self.nicol.enroll_code_page
		factor2_page = self.nicol.enroll_factor2_page #1 field, phone #
		name_page = self.nicol.enroll_name_page #2 fields, first/last name
		password_page = self.nicol.enroll_password_page #1 field, password
		accept_page = self.nicol.enroll_accept_page

		for_employers.go()
		self.assertTrue(for_employers.on())
		for_employers.enter_employer_email('')
		error = "A valid email address is required to enroll"
		self.WDWait.until(
			EC.text_to_be_present_in_element((By.CLASS_NAME, 'error_textbox'),
			error)
		)
		self.assertEqual(1, for_employers.number_of_elements('span', error))
		self.assertTrue(for_employers.on())
		for_employers.enter_employer_email('jbooth@example.com')

		self.assertTrue(code_page.on())
		self.assertFalse(code_page.is_enabled(code_page.continue_button))
		code_page.enter_code()

		self.assertTrue(factor2_page.on())
		factor2_page.click_continue()
		error = 'Required'
		# Mobile phone input does not have id
		self.WDWait.until(
			EC.text_to_be_present_in_element((By.ID, 'undefined_helper'),
			error)
		)
		self.assertEqual(1, factor2_page.number_of_elements('p', error))
		factor2_page.enter_contact('2024979756')

		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(name_page.on())
		name_page.click_continue()
		self.WDWait.until(
			EC.text_to_be_present_in_element((By.ID, 'undefined_helper'),
			error)
		)
		self.assertEqual(2, name_page.number_of_elements('p', error))
		name_page.set_first_name("Jeremy")
		name_page.click_continue()
		self.assertEqual(1, name_page.number_of_elements('p', error))
		name_page.set_last_name("Booth")
		name_page.click_continue()

		self.assertTrue(password_page.on())
		password_page.click_continue()
		# no good way to identify error <p> for password input
		self.assertEqual(1, password_page.number_of_elements('p', error))
		password_page.set_password("eighty-seven")
		password_page.click_continue()

		self.assertTrue(accept_page.on())
		accept_page.header.click_logo()

		self.assertTrue(for_employers.on())

	def test_success_existing(self):
		""" test_public.py:TestForEmployers.test_success_existing """
		# login through employer enroll form using existing user's credentials
		credentials = self.nicol.credentials
		for_employers = self.nicol.for_employers
		for_employees = self.nicol.for_employees
		code_page = self.nicol.enroll_code_page
		signin_page = self.nicol.enroll_signin_page
		factor2_page = self.nicol.enroll_factor2_page
		name_page = self.nicol.enroll_name_page
		pw_page = self.nicol.enroll_password_page
		accept_page = self.nicol.enroll_accept_page

		lobby_page = self.nicol.lobby_page

		for_employers.go()
		self.assertTrue(for_employers.on())
		for_employers.enter_employer_email(credentials['email'])

		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(signin_page.on())
		signin_page.enter_password(credentials['password'])
		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
			(By.CLASS_NAME, 'invitations_card'))
		) # Needs an extraordinarily long wait for some reason.
		self.assertTrue(lobby_page.on())
		lobby_page.menu.sign_out()
		self.assertTrue(for_employers.on())

	def test_success_new(self):
		""" test_public.py:TestForEmployers.test_success_new """
		# enroll through employer enroll form using new credentials
		for_employers = self.poli.for_employers
		code_page = self.poli.enroll_code_page
		signin_page = self.poli.enroll_signin_page
		factor2_page = self.poli.enroll_factor2_page
		name_page = self.poli.enroll_name_page
		pw_page = self.poli.enroll_password_page
		accept_page = self.poli.enroll_accept_page

		add_page = self.poli.add_business_page
		prefilled_page = self.poli.business_prefilled_page
		emp_page = self.poli.employee_page
		lobby_page = self.poli.lobby_page
		settings_page = self.poli.ps_page

		# Enroll Poli and create business
		first_name = 'Poli'
		last_name = 'Wag'
		email = self.poli.generate_email()
		phone = '202495' + self.poli.generate_number(4)    #Was 202491xxxx
		#print(email)
		#print(phone)
		ein = self.poli.generate_number(8)
		password = 'asdfasdf'

		for_employers.go()
		self.assertTrue(for_employers.on())
		for_employers.enter_employer_email(email)

		self.assertTrue(code_page.on())
		self.assertTrue(code_page.is_public())
		code_page.enter_code()

		self.assertTrue(factor2_page.on())
		self.assertTrue(factor2_page.is_public())
		factor2_page.enter_contact(phone)

		self.assertTrue(code_page.on())
		self.assertTrue(code_page.is_public())
		code_page.enter_code()

		self.assertTrue(name_page.on())
		self.assertTrue(name_page.is_public())
		name_page.set_first_name(first_name)
		name_page.set_last_name(last_name)
		name_page.click_continue()

		self.assertTrue(pw_page.on())
		self.assertTrue(pw_page.is_public())
		pw_page.set_password(password)
		pw_page.click_continue()
		self.assertTrue(accept_page.on())
		self.assertTrue(accept_page.is_public())
		accept_page.click_continue('employer')

		self.assertTrue(add_page.on())
		add_page.add('Nintendo of America 98052')

		self.assertTrue(prefilled_page.on())
		prefilled_page.set('ein', ein)
		prefilled_page.toggle_agree()
		# Have had issues loading lobby page
		# Don't load lobby page unless sure we've left prefilled page
		self.assertTrue(prefilled_page.click_continue())

		# verify menu has admin only stuff
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		emp_page.menu.open()
		self.assertIsNotNone(emp_page.menu.lobby)
		self.assertIsNotNone(emp_page.menu.invitations)
		self.assertIsNotNone(emp_page.menu.pending)
		self.assertIsNotNone(emp_page.menu.business_settings)
		self.assertIsNotNone(emp_page.menu.admins)
		self.assertIsNotNone(emp_page.menu.settings)

		# should not have role switch or employee stuff
		self.assertIsNone(emp_page.menu.role_switch)
		self.assertIsNone(emp_page.menu.eHome)
		self.assertIsNone(emp_page.menu.recipients)

		# Go to personal settings page and verify menu has same options
		emp_page.menu.click_option('settings')
		self.assertTrue(settings_page.on())

		self.assertTrue(settings_page.on())
		settings_page.menu.open()
		self.assertIsNotNone(settings_page.menu.lobby, "Missing lobby opt in menu")
		self.assertIsNotNone(settings_page.menu.invitations)
		self.assertIsNotNone(settings_page.menu.pending)
		self.assertIsNotNone(settings_page.menu.business_settings)
		self.assertIsNotNone(settings_page.menu.admins)
		self.assertIsNotNone(settings_page.menu.settings)
		self.assertIsNone(settings_page.menu.role_switch)
		self.assertIsNone(settings_page.menu.eHome)
		self.assertIsNone(settings_page.menu.recipients)
	test_success_new.e2e = True
