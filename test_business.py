import unittest
import time
import browser
import profiles
import main
import messages
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Total - 14
# TestDetails - 2       Add custom business
#     test_invalid_inputs
#     test_required_fields
# TestPrefilled - 7     Add business from map
	# test_find_success
	# test_handle_address
	# test_invalid_inputs
	# test_non_us
	# test_required_fields
	# test_success_skip
	# test_success_participate
# TestSettings - 5      Edit Business settings
#     test_business_remove
#     test_invalid_inputs
#     test_persist
#     test_required_fields
#     test_update

@unittest.skipIf(main.get_priority() < 3, "Priority = 3")
class TestDetails(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.boss = profiles.Profile(self.driver, 'boss')
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	@unittest.skipIf(main.is_ios(), "iOS")
	def test_invalid_inputs(self):
		"""business : Details .                         test_invalid_inputs"""
		# assert 'details' page handles invalid input correctly
		lobby_page = self.nicol.lobby_page
		add_page = self.nicol.add_business_page
		details_page = self.nicol.business_details_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		self.assertFalse(add_page.has_horizontal_scroll())
		add_page.click_cant_find()

		self.assertTrue(details_page.on())
		self.assertFalse(details_page.has_horizontal_scroll())
		# TODO assert ein input doesn't allow characters or symbols
		details_page.set('ein', '556787898')
		details_page.set('business_name', "Test Business")
		details_page.set('line1', "2093 Main Street")
		details_page.set('city', "Winslow")
		details_page.set('state', "Arizona")
		details_page.set('postal_code', "72561")
		details_page.set('phone', "622-746-4454")
		details_page.toggle_agree()
		self.assertTrue(details_page.agreed())

		invalid_emails = ['invalid', 'invalid@', 'invalid.com']
		error = "Invalid email address"
		tag = 'p'
		for email in invalid_emails:
			details_page.set('hr_email', email)
			details_page.click_continue()
			time.sleep(2)
			self.assertEqual(1, details_page.number_of_elements_containing(
				tag, error))
		details_page.set('hr_email', 'bogus@example.com')
		details_page.set('postal_code', '123456789012345678901')
		details_page.click_continue()
		error = "Expected Zip Code format: 12345 or 12345-1234."
		tag = 'p'
		self.assertEqual(
			1, details_page.number_of_elements(tag, error))
		details_page.set('postal_code', '98052')
		self.assertEqual(
			0, details_page.number_of_elements(tag, error))
		invalid_phones = ['1234567890', '801123456']
		for phone in invalid_phones:
			details_page.set('phone', phone)
			details_page.click_continue()
			error = " is not a valid phone number in US."
			#print(details_page.driver.find_element_by_id('phone_cont').text)
			#raw_input('did i get error text?')
			#self.WDWait.until(lambda x: error in details_page.driver.find_element_by_id("phone_cont").text)
			time.sleep(.5) # Hangs up on '801123456' error.
			self.assertEqual(1, details_page.number_of_elements_containing(
				tag, error))

	def test_required_fields(self):
		"""business : Details .                        test_required fields"""
		# assert 'Details' page inputs are required as expected
		# start and end test w/ Nintendo as current business
		lobby_page = self.boss.lobby_page
		emp_page = self.boss.employee_page
		add_page = self.boss.add_business_page
		details_page = self.boss.business_details_page
		settings_page = self.boss.business_settings_page
		prefilled_page = self.boss.business_prefilled_page
		eHome = self.boss.eHome_page
		emp_page = self.boss.employee_page
		default_business = 'Nintendo of Guatemala'
		new_busName = 'Nintendo of the Multiverse'
		self.assertTrue(self.boss.login(self.driver), messages.login)

		try:
			self.assertTrue(lobby_page.on())
		except Exception: # Doesn't have business selected
			self.assertTrue(eHome.on())
			eHome.menu.set_role('employer')
			self.assertTrue(lobby_page.on())

		self.WDWait.until_not(EC.presence_of_element_located((By.CLASS_NAME, 'animated')))
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		add_page.click_cant_find()

		self.assertTrue(details_page.on())
		details_page.click_continue()
		self.assertTrue(details_page.on())

		tag = 'p'
		error = 'Required'
		error_count = details_page.number_of_elements
		details_page.set('ein', '556787898')
		details_page.set('hr_email', '')
		details_page.click_continue()
		# Won't find 'Required' error for Terms checkbox (in <div>, not <p>)
		self.assertEqual(6, error_count(tag, error))
		details_page.set('business_name', new_busName)
		details_page.click_continue()
		self.assertEqual(5, error_count(tag, error))
		details_page.set('line1', '4600 150th Avenue Northeast')
		details_page.click_continue()
		self.assertEqual(4, error_count(tag, error))
		details_page.set('city', 'Redmond')
		details_page.click_continue()
		self.assertEqual(3, error_count(tag, error))

		details_page.set('state', 'Washington')
		# Failed on next line because it thought state was 'Required'...
		self.assertEqual('Washington', details_page.get('state'))
		details_page.set('state', "Nevada")
		self.assertEqual('Nevada', details_page.get('state'))
		details_page.click_continue()

		self.assertEqual(3, error_count(tag, error))
		details_page.set('postal_code', '98052')
		details_page.click_continue()
		self.assertEqual(2, error_count(tag, error))
		details_page.set('phone', '(425) 882-2040')
		details_page.click_continue()
		self.assertEqual(1, error_count(tag, error))
		self.assertEqual(1, error_count('div', error))
		details_page.toggle_agree()
		self.assertTrue(details_page.agreed())
		self.assertEqual(1, error_count(tag, error))
		details_page.click_continue()
		self.assertEqual(0, error_count('div', error))
		details_page.set('hr_email', "jfjfjfj@example.com")
		details_page.click_continue()

		self.assertTrue(lobby_page.on())

		# Loop to remove all instances of particular business
		has_business = lobby_page.menu.has_business(new_busName)
		while has_business:
			# make sure business is selected
			if lobby_page.menu.get_current_business() != new_busName:
				lobby_page.menu.select_business(new_busName)
				self.assertTrue(lobby_page.on())

			# remove business
			lobby_page.menu.click_option('business settings')
			self.assertTrue(settings_page.on())
			settings_page.remove_business("REMOVE " + new_busName)

			# change role
			self.assertTrue(eHome.on())
			eHome.menu.set_role('employer')
			self.assertTrue(lobby_page.on())

			self.WDWait.until_not(EC.presence_of_element_located((By.CLASS_NAME, 'animated')))
			# check if another instance of business
			has_business = lobby_page.menu.has_business(new_busName)

		# done removing business. Select default business
		self.assertFalse(lobby_page.menu.has_business(new_busName))
		lobby_page.menu.select_business(default_business)
		self.assertTrue(lobby_page.on())


class TestPrefilled(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.faker = profiles.Profile(self.driver, 'faker')
		self.tester = profiles.Profile(self.driver, 'tester')
		self.fire = profiles.Profile(self.driver, 'fire')
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_find_success(self):
		"""business : Prefilled .                       test_find_success"""
		# assert find business works
		credentials = self.nicol.credentials
		lobby_page = self.nicol.lobby_page
		add_page = self.nicol.add_business_page
		prefilled_page = self.nicol.business_prefilled_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		name = 'Nintendo of America'
		search_term = name + ' WA'
		add_page.add(search_term)
		self.WDWait.until(EC.presence_of_element_located((By.ID, 'ein')))
		self.assertTrue(prefilled_page.on())
		self.assertFalse(prefilled_page.has_horizontal_scroll())

		# assert values are autofilled
		prefilled_page.click_details()
		get = prefilled_page.get
		self.assertEqual(get('ein'), '')
		#most of the time fails on hr email (doesn't autofill???)
		self.assertEqual(get('hr_email'), credentials['email'])
		self.assertEqual(get('business_name'), name)
		self.assertEqual(get('dba'), name)
		self.assertEqual(get('line1'), '4600 150th Avenue Northeast')
		self.assertEqual(get('line2'), '')
		self.assertEqual(get('city'), 'Redmond')
		self.assertEqual(get('postal_code'), '98052')
		self.assertEqual(get('phone'), '(425) 882-2040')
		# url gets trimmed. no longer has anything after .com

		self.assertEqual(get('website'), 'http://nintendo.com')
		self.assertEqual(get('state'), 'Washington')

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_handle_address(self):
		""" business : Prefilled .                  test_handle_address"""
		# assert 'Add Business' handles selecting an address as expected
		lobby_page = self.nicol.lobby_page
		add_page = self.nicol.add_business_page
		prefilled_page = self.nicol.business_prefilled_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		address = "115 N Main Street Lehi"
		add_page.add(address)

		# business & DBA should be blank. Details should be open
		self.WDWait.until(EC.presence_of_element_located((By.ID, 'ein')))
		self.assertTrue(prefilled_page.on())
		self.assertEqual(
			"", prefilled_page.business_name_input.get_attribute('value')
		)
		self.assertEqual("", prefilled_page.dba_input.get_attribute('value'))

	@unittest.skipIf(main.get_priority() < 3, "Priority")
	def test_invalid_inputs(self):
		"""business : Prefilled .                   test_invalid_inputs"""
		# assert inputs on 'Prefilled' page handle invalid input as expected
		lobby_page = self.nicol.lobby_page
		add_page = self.nicol.add_business_page
		prefilled_page = self.nicol.business_prefilled_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		# raw_input('adding business')
		add_page.add("Nintendo of America WA")
		# raw_input('added?')
		self.assertTrue(prefilled_page.on())
		self.assertFalse(prefilled_page.agreed())
		prefilled_page.toggle_agree()
		self.assertTrue(prefilled_page.agreed())
		prefilled_page.click_details()
		prefilled_page.set('ein', '556787898')
		invalid_emails = ['invalid', 'invalid@', 'invalid.com']
		error = "Invalid email address"
		tag = 'p'
		for email in invalid_emails:
			prefilled_page.set('hr_email', email)
			prefilled_page.click_continue()
			self.assertEqual(1, prefilled_page.number_of_elements_containing(
				tag, error))
		prefilled_page.set('postal_code', '123456789012345678901')
		prefilled_page.click_continue()
		error = "Expected Zip Code format: 12345 or 12345-1234."
		self.assertEqual(
			1, prefilled_page.number_of_elements(tag, error))
		prefilled_page.set('postal_code', '98052')
		# ios won't know you've updated zip code unless you click continue
		if not main.is_ios():
			self.assertEqual(
				0, prefilled_page.number_of_elements(tag, error))
		invalid_phones = ['1234567890', '801123456']
		'''error = (
			'\"{phone}\" is not a valid phone number in the United States.'
		)'''
		error = " is not a valid phone number in US." #in the United States.
		for phone in invalid_phones:
			prefilled_page.set('phone', phone)
			prefilled_page.click_continue()
			#time.sleep(.2)
			self.assertEqual(1, prefilled_page.number_of_elements_containing(
				tag, error))
		prefilled_page.set('phone', '(425) 882-2040')

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_non_us(self):
		"""business : Prefilled .                           test_non_us """
		# assert cannot add non-US business
		lobby_page = self.nicol.lobby_page
		add_page = self.nicol.add_business_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		self.assertFalse(add_page.add("Nintendo of Canada", expectedFailure=True))

		# assert error message has expected text
		self.assertTrue(add_page.has_error())

	@unittest.skipIf(main.get_priority() < 3, "Priority")
	def test_required_fields(self):
		"""business : Prefilled .                    test_required fields"""
		# assert fields on 'Prefilled' page are required as expected
		# Should start and end test w/ ZZ Designs as current business
		lobby_page = self.faker.lobby_page
		emp_page = self.faker.employee_page
		add_page = self.faker.add_business_page
		prefilled_page = self.faker.business_prefilled_page
		settings_page = self.faker.business_settings_page
		eHome = self.faker.eHome_page
		default_business = 'ZZ Designs'
		new_busName = "Nintendo of America"
		tag = 'p'
		error = 'Required'
		self.assertTrue(self.faker.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		add_page.add(new_busName + " WA")
		self.assertTrue(prefilled_page.on())

		# should be 2 required errors before clearing details inputs
		prefilled_page.click_continue()
		error_count = prefilled_page.number_of_elements
		# 1 for EIN, 1 for terms and conditions
		self.assertEqual(1, error_count(tag, error))
		self.assertEqual(1, error_count('div', error))
		self.assertTrue(prefilled_page.on())
		prefilled_page.click_details()
		prefilled_page.toggle_agree()
		self.assertTrue(prefilled_page.agreed())

		#Clear form, then check error_counts
		prefilled_page.set('business_name', '')
		prefilled_page.set('dba', '')
		prefilled_page.set('ein', '')
		prefilled_page.set('hr_email', '')
		prefilled_page.set('line1', '')
		prefilled_page.set('city', '')
		prefilled_page.set('postal_code', '')
		prefilled_page.set('phone', '')
		prefilled_page.set('website', '')
		prefilled_page.click_continue()
		self.assertEqual(7, error_count(tag, error))
		prefilled_page.set('ein', '556787898')
		prefilled_page.click_continue()
		self.assertEqual(6, error_count(tag, error))
		prefilled_page.set('hr_email', 'jlsidkd@example.com')
		prefilled_page.click_continue()
		self.assertEqual(5, error_count(tag, error))
		prefilled_page.set('business_name', new_busName)
		prefilled_page.click_continue()
		self.assertEqual(4, error_count(tag, error))
		prefilled_page.set('line1', '123 Elm Street')
		prefilled_page.click_continue()
		self.assertEqual(3, error_count(tag, error))
		prefilled_page.set('city', 'Seattle')
		prefilled_page.click_continue()
		self.assertEqual(2, error_count(tag, error))
		prefilled_page.set('state', 'Nevada')
		prefilled_page.click_continue()
		self.assertEqual(2, error_count(tag, error))
		prefilled_page.set('postal_code', '99876')
		prefilled_page.click_continue()
		self.assertEqual(1, error_count(tag, error))
		prefilled_page.set('phone', '(678) 555-8675')
		time.sleep(.4) # iOS has weird issue.
		# If you change phone# and immediately submit form you get WSOD
		# Giving a little bit of time before submitting seems to avoid issue.
		prefilled_page.click_continue()
		if not lobby_page.on():
			raw_input('inspect')
		self.assertTrue(lobby_page.on())

		# Remove all Nintendo businesses
		has_business = lobby_page.menu.has_business(new_busName)
		while has_business:
			# make sure business is selected
			if lobby_page.menu.get_current_business() != new_busName:
				lobby_page.menu.select_business(new_busName)
				self.assertTrue(lobby_page.on())

			# remove business
			lobby_page.menu.click_option('business settings')
			self.assertTrue(settings_page.on())
			settings_page.remove_business("REMOVE " + new_busName)

			# change role
			self.assertTrue(eHome.on())
			eHome.menu.set_role('employer')
			self.assertTrue(lobby_page.on())

			# check if another instance of business
			has_business = lobby_page.menu.has_business(new_busName)

		# done removing business. Select default business
		self.assertFalse(lobby_page.menu.has_business(new_busName))
		lobby_page.menu.select_business(default_business)
		self.assertTrue(lobby_page.on())

	def test_success_skip(self):
		"""business : Prefilled .                   test_success_skip"""
		# assert adding 'Prefilled' business works as expected
		# Skip adding yourself as employee
		lobby_page = self.tester.lobby_page
		emp_page = self.tester.employee_page
		view_page = self.tester.employee_view_page
		admin_page = self.tester.admin_page
		add_page = self.tester.add_business_page
		prefilled_page = self.tester.business_prefilled_page
		settings_page = self.tester.business_settings_page
		eHome = self.tester.eHome_page
		default_business = 'ZZ Designs'
		name = 'Tester McTester'
		self.assertTrue(self.tester.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		new_busName = 'Nintendo of America'
		ein = '556787898'
		hr_email = "tester@example.com"
		add_page.add(new_busName + " WA")

		self.assertTrue(prefilled_page.on())
		prefilled_page.toggle_agree()
		prefilled_page.click_details()

		get = prefilled_page.get
		self.assertEqual(get('state'),'Washington')
		prefilled_page.set_state("California")
		self.assertEqual(get('state'),"California")

		self.assertTrue(prefilled_page.set('ein', ein))
		prefilled_page.set('hr_email', hr_email)
		#prefilled_page.toggle_agree()
		self.assertTrue(prefilled_page.agreed())
		prefilled_page.click_continue()

		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		self.assertEqual(1, emp_page.num_employees())
		emp = emp_page.get_employee('name', name)
		self.assertEqual(emp['status'], 'Admin')

		# should be sole admin in table w/ full privileges
		emp_page.menu.click_option('admin')
		self.assertTrue(admin_page.on())

		self.assertEqual(1, admin_page.num_admins())
		admin = admin_page.get_admin(name)
		self.assertTrue(admin['members'])
		self.assertTrue(admin['org'])

		# clicking admin entry should go to employee card
		admin_page.click_admin(name)
		self.assertTrue(view_page.on())
		#self.assertEqual('Admin', view_page.get_status())
		self.assertEqual('executive', view_page.get_admin_role())
		view_page.header.click_back()
		self.assertTrue(admin_page.on())
		admin_page.menu.click_option('business settings')

		# Business settings should be same as when we created business
		self.assertTrue(settings_page.on())
		get = settings_page.get
		self.assertEqual(get('ein'), ein)
		self.assertEqual(get('hr_email'), hr_email)
		self.assertEqual(get('business_name'), new_busName)
		self.assertEqual(get('dba'), new_busName)
		self.assertEqual(get('line1'), '4600 150th Avenue Northeast')
		self.assertEqual(get('line2'), '')
		self.assertEqual(get('city'), 'Redmond')
		self.assertEqual(get('postal_code'), '98052')
		self.assertEqual(get('phone'), '(425) 882-2040')

		self.assertEqual(get('website'), 'http://nintendo.com')
		self.assertEqual(get('state'), 'California')
		settings_page.remove_business("REMOVE NINTENDO OF AMERICA")

		self.assertTrue(eHome.on())
		eHome.menu.set_role('employer')
		self.assertTrue(lobby_page.on())
		# Loop to remove all instances of particular business
		has_business = lobby_page.menu.has_business(new_busName)
		while has_business:
			# make sure business is selected
			if lobby_page.menu.get_current_business() != new_busName:
				lobby_page.menu.select_business(new_busName)
				self.assertTrue(lobby_page.on())

			# remove business
			lobby_page.menu.click_option('business settings')
			self.assertTrue(settings_page.on())
			settings_page.remove_business("REMOVE " + new_busName)

			# change role
			self.assertTrue(eHome.on())
			eHome.menu.set_role('employer')
			self.assertTrue(lobby_page.on())

			# check if another instance of business
			has_business = lobby_page.menu.has_business(new_busName)

		# done removing business. Select default business
		self.assertFalse(lobby_page.menu.has_business(new_busName))
		lobby_page.menu.select_business(default_business)
		self.assertTrue(lobby_page.on())

	@unittest.skip("Participate dialog moved to post-approval")
	def test_success_participate(self):
		"""business : Prefilled .                  test_success_participate"""
		#dependencies: Should have no Nintendo of America business
		lobby_page = self.fire.lobby_page
		emp_page = self.fire.employee_page
		view_page = self.fire.employee_view_page
		admin_page = self.fire.admin_page
		add_page = self.fire.add_business_page
		prefilled_page = self.fire.business_prefilled_page
		settings_page = self.fire.business_settings_page
		eHome = self.fire.eHome_page
		participate_page = self.fire.participate_page
		main_election = self.fire.pay_election_page
		pending_elections = self.fire.pending_elections_page
		default_business = 'ZZ Designs'
		name = 'Firefox Boss'
		self.assertTrue(self.fire.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		new_busName = 'Nintendo of America'
		ein = '556787898'
		hr_email = "nicol@sendmi.com"
		add_page.add(new_busName + " WA")

		self.assertTrue(prefilled_page.on())
		prefilled_page.click_details()

		get = prefilled_page.get
		self.assertEqual(get('state'),'Washington')
		prefilled_page.set_state("California")
		self.assertEqual(get('state'),"California")

		prefilled_page.set('ein', ein)
		prefilled_page.set('hr_email', hr_email)
		prefilled_page.toggle_agree()
		prefilled_page.click_continue()

		self.assertTrue(emp_page.on())
		emp_page.handle_participate_dialog('participate')
		self.assertTrue(participate_page.on())
		participate_page.set_id('T-000')
		participate_page.set_dob('01/01/1984')
		participate_page.set_zip('12345')
		if participate_page.agreed() is not True:
			participate_page.click_agree()
		participate_page.click_submit()

		self.assertTrue(main_election.on())
		main_election.set_election('Nintendo of America', '15.00')
		main_election.click_save()

		self.assertTrue(eHome.on())
		eHome.menu.set_role('employer')
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		self.assertEqual(1, emp_page.num_employees())
		emp = emp_page.get_employee('name', name)
		self.assertEqual(emp['status'], 'Active')

		# should be sole admin in table w/ full privileges
		emp_page.menu.click_option('admin')
		self.assertTrue(admin_page.on())
		self.assertEqual(1, admin_page.num_admins())
		admin = admin_page.get_admin(name)
		self.assertTrue(admin['members'])
		self.assertTrue(admin['org'])

		# clicking admin entry should go to employee card
		admin_page.click_admin(name)
		self.assertTrue(view_page.on())
		self.assertEqual('Active', view_page.get_status())
		self.assertEqual('executive', view_page.get_admin_role())
		view_page.header.click_back()
		self.assertTrue(admin_page.on())
		admin_page.menu.click_option('pending elections')

		self.assertTrue(pending_elections.on())
		self.assertEqual(1, pending_elections.num_pending_elections())
		test_election = pending_elections.get_election('name', name)
		self.assertEqual(test_election['name'], name)
		self.assertEqual(test_election['amount'], '15.00')
		admin_page.menu.click_option('business settings')

		# Business settings should be same as when we created business
		self.assertTrue(settings_page.on())
		get = settings_page.get
		self.assertEqual(get('ein'), ein)
		self.assertEqual(get('hr_email'), hr_email)
		self.assertEqual(get('business_name'), new_busName)
		self.assertEqual(get('dba'), new_busName)
		self.assertEqual(get('line1'), '4600 150th Avenue Northeast')
		self.assertEqual(get('line2'), '')
		self.assertEqual(get('city'), 'Redmond')
		self.assertEqual(get('postal_code'), '98052')
		self.assertEqual(get('phone'), '(425) 882-2040')
		# no longer has stuff after .com (/corp/)

		self.assertEqual(get('website'), 'http://nintendo.com')
		self.assertEqual(get('state'), 'California')
		settings_page.remove_business("REMOVE NINTENDO OF AMERICA")

		self.assertTrue(eHome.on())
		eHome.menu.set_role('employer')
		self.assertTrue(lobby_page.on())
		# Loop to remove all instances of particular business
		has_business = lobby_page.menu.has_business(new_busName)
		while has_business:
			# make sure business is selected
			if lobby_page.menu.get_current_business() != new_busName:
				lobby_page.menu.select_business(new_busName)
				self.assertTrue(lobby_page.on())

			# remove business
			lobby_page.menu.click_option('business settings')
			self.assertTrue(settings_page.on())
			settings_page.remove_business("REMOVE " + new_busName)

			# change role
			self.assertTrue(eHome.on())
			eHome.menu.set_role('employer')
			self.assertTrue(lobby_page.on())

			# check if another instance of business
			has_business = lobby_page.menu.has_business(new_busName)

		# done removing business. Select default business
		self.assertFalse(lobby_page.menu.has_business(new_busName))
		lobby_page.menu.select_business(default_business)
		self.assertTrue(lobby_page.on())

class TestSettings(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.patrick = profiles.Profile(self.driver, 'patrick')
		self.krabs = profiles.Profile(self.driver, 'krabs')
		self.squid = profiles.Profile(self.driver, 'squid')
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_business_remove(self):
		"""business : Settings .                        test_business_remove"""
		# assert owner can remove business
		# requisites: "Subway" is removed after test
		lobby_page = self.krabs.lobby_page
		emp_page = self.krabs.employee_page
		add_page = self.krabs.add_business_page
		prefilled_page = self.krabs.business_prefilled_page
		settings_page = self.krabs.business_settings_page
		eHome = self.krabs.eHome_page
		default_business = 'Krusty Krab'
		self.assertTrue(self.krabs.login(self.driver), messages.login)

		business_name = 'Subway Highland Utah'
		self.assertTrue(lobby_page.on()) #login failure
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		add_page.add(business_name)
		self.assertTrue(prefilled_page.on())
		prefilled_page.set('ein', '234567847')
		prefilled_page.click_details()
		prefilled_page.set('business_name', business_name)
		prefilled_page.toggle_agree()
		prefilled_page.click_continue()

		self.assertTrue(lobby_page.on())
		self.assertEqual(business_name, lobby_page.menu.get_current_business())

		# Loop to remove all instances of particular business
		has_business = lobby_page.menu.has_business(business_name)
		while has_business:
			# make sure business is selected
			if lobby_page.menu.get_current_business() != business_name:
				lobby_page.menu.select_business(business_name)
				self.assertTrue(lobby_page.on())

			# remove business
			lobby_page.menu.click_option('business settings')
			self.assertTrue(settings_page.on())
			settings_page.remove_business("REMOVE " + business_name)

			# change role
			self.assertTrue(eHome.on())
			eHome.menu.set_role('employer')
			self.assertTrue(lobby_page.on())

			# check if another instance of business
			has_business = lobby_page.menu.has_business(business_name)

		# done removing business. Select default business
		self.assertFalse(lobby_page.menu.has_business(business_name))
		lobby_page.menu.select_business(default_business)
		self.assertTrue(lobby_page.on())

	@unittest.skipIf(main.get_priority() < 3, "Priority")
	def test_invalid_inputs(self):
		"""business : Settings .                      test_invalid_inputs"""
		# assert 'Business Settings' page handles invalid inputs as expected
		lobby_page = self.patrick.lobby_page
		emp_page = self.patrick.employee_page
		add_page = self.patrick.add_business_page
		prefilled_page = self.patrick.business_prefilled_page
		settings_page = self.patrick.business_settings_page
		eHome = self.patrick.eHome_page
		default_business = 'Chum Bucket'
		self.assertTrue(self.patrick.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != default_business:
				lobby_page.menu.select_business(default_business)
				self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		business_name = "Nintendo of America"
		search_term = business_name + ' WA'
		add_page.add(search_term)
		prefilled_page.load()
		ein = "66787665"
		prefilled_page.set('ein', ein)
		prefilled_page.toggle_agree()
		prefilled_page.click_continue()

		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('business settings')

		self.assertTrue(settings_page.on())
		settings_page.set('postal_code', '123456789012345678901')
		self.assertFalse(settings_page.saved())
		tag = 'p'
		error = "Expected Zip Code format: 12345 or 12345-1234."
		error_count = settings_page.number_of_elements
		self.assertEqual(1, error_count(tag, error))
		settings_page.set('postal_code', 'abc')
		self.assertFalse(settings_page.saved())
		self.assertEqual(1, error_count(tag, error))
		settings_page.set('postal_code', '98051')
		self.assertTrue(settings_page.saved())
		invalid_phones = ['1234567890', '801123456']
		error = " is not a valid phone number in US."
		for phone in invalid_phones:
			settings_page.set('phone', phone)
			self.assertFalse(settings_page.saved())
			self.assertEqual(1, prefilled_page.number_of_elements_containing(
				tag, error))
		settings_page.set('phone', '(425) 882-2040')
		settings_page.set('website', 'new site')
		self.assertFalse(settings_page.saved())
		error = "May not contain spaces."
		#time.sleep(1)
		self.assertEqual(
			1, settings_page.number_of_elements('p', error))
		site = 'www.nintendo.com'
		settings_page.set('website', site)
		self.assertTrue(settings_page.saved())
		self.assertEqual('http://' + site,
						 settings_page.get('website'))
		self.assertTrue(settings_page.saved())
		settings_page.remove_business("REMOVE NINTENDO OF AMERICA")

		self.assertTrue(eHome.on())
		eHome.menu.set_role('employer')
		self.assertTrue(lobby_page.on())

		# Loop to remove all instances of particular business
		has_business = lobby_page.menu.has_business(business_name)
		while has_business:
			# make sure business is selected
			if lobby_page.menu.get_current_business() != business_name:
				lobby_page.menu.select_business(business_name)
				self.assertTrue(lobby_page.on())

			# remove business
			lobby_page.menu.click_option('business settings')
			self.assertTrue(settings_page.on())
			settings_page.remove_business("REMOVE " + business_name)

			# change role
			self.assertTrue(eHome.on())
			eHome.menu.set_role('employer')
			self.assertTrue(lobby_page.on())

			# check if another instance of business
			has_business = lobby_page.menu.has_business(business_name)

		# done removing business. Select default business
		self.assertFalse(lobby_page.menu.has_business(business_name))
		lobby_page.menu.select_business(default_business)
		self.assertTrue(lobby_page.on())

	@unittest.skipIf(main.is_ios(), "Autosave input + iOS = suicide")
	def test_persist(self):
		"""business : Settings .                            test_persist"""
		#Change business settings and assert persistence across logins.
		lobby_page = self.nicol.lobby_page
		settings_page = self.nicol.business_settings_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() != business:
				lobby_page.menu.select_business(business)
				self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('business settings')
		self.assertTrue(settings_page.on())

		get = settings_page.get
		#change _init args to match Multiverse dictionary data?
		hr_init = settings_page.get('hr_email')
		dba_init = settings_page.get('dba')
		line1_init = settings_page.get('line1')
		line2_init = settings_page.get('line2')
		city_init = settings_page.get('city')
		postal_init = settings_page.get('postal_code')
		phone_init = settings_page.get('phone')
		site_init = settings_page.get('website')
		hr2 = 'hr@example.com'
		dba2 = 'New Dba'
		line12 = 'new line1'
		line22 = 'new line2'
		city2 = 'new city'
		postal2 = '80987'
		phone2 = '(801) 987-6576'
		site2 = 'http://new_site'
		settings_page.set('hr_email', hr2)
		settings_page.set('dba', dba2)
		settings_page.set('line1', line12)
		settings_page.set('line2', line22)
		settings_page.set('city', city2)
		settings_page.set('postal_code', postal2)
		settings_page.set('phone', phone2)
		settings_page.set('website', site2)

		self.assertTrue(settings_page.saved())
		settings_page.menu.sign_out()

		# login and make sure changes persisted
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('business settings')

		self.assertTrue(settings_page.on())
		hr_final = settings_page.get('hr_email')
		dba_final = settings_page.get('dba')
		line1_final = settings_page.get('line1')
		line2_final = settings_page.get('line2')
		city_final = settings_page.get('city')
		postal_final = settings_page.get('postal_code')
		phone_final = settings_page.get('phone')
		site_final = settings_page.get('website')
		self.assertEqual(hr2, hr_final)
		self.assertEqual(dba2, dba_final)
		self.assertEqual(line12, line1_final)
		self.assertEqual(line22, line2_final)
		self.assertEqual(city2, city_final)
		self.assertEqual(postal2, postal_final)
		self.assertEqual(phone2, phone_final)
		self.assertEqual(site2, site_final)

		multiverse_creds = profiles.credentials.get_credentials('multiverse')
		settings_page.set('hr_email', multiverse_creds['hr'])
		settings_page.set('dba', multiverse_creds['name'])
		settings_page.set('line1', multiverse_creds['line1'])
		settings_page.set('line2', '')
		settings_page.set('city', multiverse_creds['city'])
		settings_page.set('postal_code', multiverse_creds['postal_code'])
		settings_page.set('phone', multiverse_creds['phone'])
		settings_page.set('website', multiverse_creds['website'])

		self.assertTrue(settings_page.saved())

	@unittest.skipIf(main.get_priority() < 3, "Priority")
	def test_required_fields(self):
		"""business : Settings .                      test_required fields"""
		# assert 'Business Settings' page requires expected fields
		lobby_page = self.squid.lobby_page
		emp_page = self.squid.employee_page
		add_page = self.squid.add_business_page
		prefilled_page = self.squid.business_prefilled_page
		settings_page = self.squid.business_settings_page
		eHome = self.squid.eHome_page
		default_business = 'Salty Spitoon'
		self.assertTrue(self.squid.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.add_a_business()

		self.assertTrue(add_page.on())
		business_name = "Nintendo of America"
		search_term = business_name + ' WA'
		add_page.add(search_term)
		self.assertTrue(prefilled_page.on())
		ein = "66787665"
		prefilled_page.set('ein', ein)
		prefilled_page.toggle_agree()
		prefilled_page.click_continue()

		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('business settings')

		self.assertTrue(settings_page.on())
		settings_page.set('business_name','')
		settings_page.set('dba', '')
		settings_page.set('ein', '')
		settings_page.set('hr_email', '')
		settings_page.set('line1', '')
		settings_page.set('city', '')
		settings_page.set('postal_code', '')
		settings_page.set('phone', '')
		settings_page.set('website', '')

		error = 'Required'
		tag = 'p'
		error_count = settings_page.number_of_elements
		self.assertEqual(7, error_count(tag, error))
		settings_page.set('business_name', business_name)
		self.assertEqual(6, error_count(tag, error))
		settings_page.set('ein', ein)
		self.assertEqual(5, error_count(tag, error))
		settings_page.set('hr_email', "jslskdjf@example.com")
		self.assertEqual(4, error_count(tag, error))
		settings_page.set('line1', 'my address')
		self.assertEqual(3, error_count(tag, error))
		settings_page.set('city', 'my city')
		self.assertEqual(2, error_count(tag, error))
		settings_page.set('postal_code', '86778')
		self.assertEqual(1, error_count(tag, error))
		settings_page.set('phone', '(801) 756-9876')
		self.assertTrue(settings_page.saved())
		settings_page.click_remove()
		self.assertFalse(
			settings_page.confirm_remove_button_enabled())
		settings_page.set_remove_code('REMOVE NINTENDO OF AMERICA')
		self.assertTrue(
			settings_page.confirm_remove_button_enabled())
		settings_page.click_confirm_remove()

		self.assertTrue(eHome.on())
		eHome.menu.set_role('employer')
		self.assertTrue(lobby_page.on())
		# Loop to remove all instances of particular business
		has_business = lobby_page.menu.has_business(business_name)
		while has_business:
			# make sure business is selected
			if lobby_page.menu.get_current_business() != business_name:
				lobby_page.menu.select_business(business_name)
				self.assertTrue(lobby_page.on())

			# remove business
			lobby_page.menu.click_option('business settings')
			self.assertTrue(settings_page.on())
			settings_page.remove_business("REMOVE " + business_name)

			# change role
			self.assertTrue(eHome.on())
			eHome.menu.set_role('employer')
			self.assertTrue(lobby_page.on())

			# check if another instance of business
			has_business = lobby_page.menu.has_business(business_name)

		# done removing business. Select default business
		self.assertFalse(lobby_page.menu.has_business(business_name))
		lobby_page.menu.select_business(default_business)
		self.assertTrue(lobby_page.on())

	@unittest.skipIf(main.is_ios() or main.get_priority() < 2,
	 "Autosave input + iOS = suicide")
	def test_update(self):
		"""business : Settings .                             test_update"""
		# assert changes to 'Business Settings' page persist
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		settings_page = self.nicol.business_settings_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		name = "Multiverse"
		# ein1 = '4896434'
		self.assertTrue(lobby_page.on())
		# go to Multiverse business settings, select multiverse if needed
		if lobby_page.menu.get_current_business() != 'Multiverse':
			lobby_page.menu.select_business(name)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('business settings')

		self.assertTrue(settings_page.on())
		self.assertFalse(settings_page.has_horizontal_scroll())
		get = settings_page.get
		hr_init = get('hr_email')
		dba_init = get('dba')
		line1_init = get('line1')
		line2_init = get('line2')
		city_init = get('city')
		postal_init = get('postal_code')
		phone_init = get('phone')
		site_init = get('website')
		hr2 = 'hr@example.com'
		dba2 = 'New Dba'
		line12 = 'new line1'
		line22 = 'new line2'
		city2 = 'new city'
		postal2 = '80987'
		phone2 = '(801) 987-6576'
		site2 = 'http://new_site'

		settings_page.set('hr_email', hr2)
		settings_page.set('dba', dba2)
		settings_page.set('line1', line12)
		settings_page.set('line2', line22)
		settings_page.set('city', city2)
		settings_page.set('postal_code', postal2)
		settings_page.set('phone', phone2)
		settings_page.set('website', site2)

		self.assertTrue(settings_page.saved())
		settings_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		emp_page.menu.click_option('business settings')
		self.assertTrue(settings_page.on())
		#Test for persistence
		self.assertEqual(hr2, get('hr_email'))
		self.assertEqual(dba2, get('dba'))
		self.assertEqual(line12, get('line1'))
		self.assertEqual(line22, get('line2'))
		self.assertEqual(city2, get('city'))
		self.assertEqual(postal2, get('postal_code'))
		self.assertEqual(phone2, get('phone'))
		self.assertEqual(site2, get('website'))
		#Revert changes
		settings_page.set('hr_email', hr_init)
		settings_page.set('dba', dba_init)
		settings_page.set('line1', line1_init)
		settings_page.set('line2', line2_init)
		settings_page.set('city', city_init)
		settings_page.set('postal_code', postal_init)
		settings_page.set('phone', phone_init)
		settings_page.set('website', site_init)

