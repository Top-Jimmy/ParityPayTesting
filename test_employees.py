import time
import unittest
import browser
import profiles
import main
import messages
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Total - 17
# TestAdd - 8           Add/Edit Employee
	# test_admin_existing
	# test_admin_new
	# test_existing
	# test_form
	# test_new
	# test_table_footer
	# test_table_invite
	# test_table_reinvite
# TestCSV
	# todo: csv tests
# TestDetails - 5       Sort/Filter Table, Set/Edit permissions
	# test_filter
	# test_permissions
	# test_profile
	# test_sort
	# test_verify_permissions
# TestInvitations - 2   Invite/Reinvite Employee
	# test_invite
	# test_reinvite     (times out)
# TestRemove - 2        Terminate/Remove Employee
	# test_self
	# test_success

class TestAdd(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.lili = profiles.Profile(self.driver, 'lili')
		self.poli = profiles.Profile(self.driver)
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	def test_admin_existing(self):
		"""employees : Add .                          test_admin_existing"""
		# Add existing employee (lili) as administrator
		lobby_page = self.nicol.lobby_page
		admin_page = self.nicol.admin_page
		add_admin_page = self.nicol.add_admin_page
		emp_page = self.nicol.employee_page
		view_page = self.nicol.employee_view_page

		emp_id = '13313113'

		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() is not business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('admin')

		self.assertTrue(admin_page.on())
		# Make sure Lili starts w/ no permissions
		if admin_page.get_admin('Lili Ana') is not None:
			admin_page.click_admin('Lili Ana')
			self.assertTrue(view_page.on())
			view_page.set_admin_role('none')
			self.assertTrue(view_page.on())
			view_page.header.click_back()
			self.assertTrue(admin_page.on())
			self.assertIsNone(admin_page.get_admin_by_name("Lili Ana"))

		admin_page.click_add_admin()

		self.assertTrue(add_admin_page.on())
		add_admin_page.click_existing()
		add_admin_page.select_employee(emp_id)

		self.WDWait.until(EC.presence_of_element_located((By.CLASS_NAME, 'table_toolbar')))
		self.assertTrue(admin_page.on())
		admin_page.menu.sign_out()

		# lobby_page = self.lili.lobby_page
		invite_page = self.lili.invitations_page
		pending_elections_page = self.lili.pending_elections_page
		employee_page = self.lili.employee_page

		self.assertTrue(self.lili.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())

		lobby_page.menu.click_option('invitations')
		self.assertTrue(invite_page.on())
		invite_page.menu.click_option('pending elections')
		self.assertTrue(pending_elections_page.on())
		pending_elections_page.menu.click_option('employees')
		self.assertTrue(employee_page.on())
		employee_page.menu.sign_out()

		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() is not business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('admin')

		self.assertTrue(admin_page.on())
		admin_page.click_admin('Lili Ana')
		self.assertTrue(view_page.on())
		#view_page.set_admin_role('executive') #workaround, perms not loading bug
		#self.assertTrue(view_page.on())
		view_page.set_admin_role('none')
		self.assertTrue(view_page.on())
	test_admin_existing.e2e = True

	@unittest.skipIf(not main.is_web(), 'native cannot get urls')
	def test_admin_new(self):
		"""employees : Add .                            test_admin_new"""
		# Infest admin table with Poli Wags.
		lobby_page = self.nicol.lobby_page
		admin_page = self.nicol.admin_page
		add_admin_page = self.nicol.add_admin_page
		emp_page = self.nicol.employee_page
		view_page = self.nicol.employee_view_page

		first_name = 'Bogus'
		last_name = 'Bogusen'
		full_name = first_name + ' ' + last_name
		email = self.nicol.generate_email()
		phone = '202341' + self.nicol.generate_number(4)
		dob = '01/01/1984'
		zip_code = '12345'

		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() is not business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('admin')

		self.assertTrue(admin_page.on())
		admin_page.click_add_admin()
		self.assertTrue(add_admin_page.on())
		self.assertEqual('new', add_admin_page.current_tab())

		add_admin_page.set_first_name(first_name)
		add_admin_page.set_last_name(last_name)
		add_admin_page.set_dob(dob)
		add_admin_page.set_zip(zip_code)
		add_admin_page.set_email(email)
		add_admin_page.click_send()

		self.assertTrue(emp_page.on())
		urls = emp_page.get_secret_urls()
		emp_page.click_toast() # clear toast or cannot click logout (mobile)
		emp_page.menu.sign_out()

		dob_page = self.poli.dob_page
		invite_page = self.poli.invite_page
		factor2_page = self.poli.enroll_factor2_page
		code_page = self.poli.enroll_code_page
		name_page = self.poli.enroll_name_page
		pw_page = self.poli.enroll_password_page
		accept_page = self.poli.enroll_accept_page
		lobby_page = self.poli.lobby_page
		emp_page = self.poli.employee_page
		invitations_page = self.poli.invitations_page
		pending_elections_page = self.poli.pending_elections_page
		home_page = self.poli.for_employers

		'''print(urls['email_url'])
		print(email)
		print(phone)'''
		self.driver.get(urls['email_url'])
		print(urls['email_url'])
		self.assertTrue(dob_page.on())
		dob_page.set_dob(dob)
		self.assertEqual(dob, dob_page.get_dob())
		dob_page.set_zip(zip_code)
		self.assertEqual(zip_code, dob_page.get_zip())
		dob_page.click_continue()

		self.assertTrue(invite_page.on())
		invite_page.enter_email(email)

		self.WDWait.until(EC.presence_of_element_located((By.ID, 'country_dropdown')))
		self.assertTrue(factor2_page.on())
		factor2_page.set_contact(phone)
		factor2_page.click_continue()

		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(name_page.on())
		name_page.click_continue()

		self.assertTrue(pw_page.on())
		pw_page.set_password('asdfasdf')
		pw_page.click_continue()

		self.assertTrue(accept_page.on())
		accept_page.click_continue('admin')

		self.assertTrue(lobby_page.on())

		lobby_page.menu.click_option('invitations')
		self.assertTrue(invitations_page.on())
		invitations_page.menu.click_option('pending elections')
		self.assertTrue(pending_elections_page.on())
		pending_elections_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		emp_page.menu.sign_out()

		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() is not business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('admin')

		self.assertTrue(admin_page.on())
		admin_page.click_admin(full_name)
		self.assertTrue(view_page.on())
		view_page.set_admin_role('none')

		self.assertTrue(view_page.on())
		view_page.header.click_back()
		self.assertTrue(admin_page.on())
		admin_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		# Remove all bogus bogusen employees
		employee = emp_page.get_employee('name', full_name)
		while employee:
			emp_page.remove_employee('name', full_name)
			self.assertTrue(emp_page.on())
			employee = emp_page.get_employee('name', full_name)

		self.assertIsNone(emp_page.get_employee('name', full_name))
	test_admin_new.e2e = True

	# @unittest.skipIf(not main.is_web() main.get_priority() < 2,
	#  'Cannot copy/paste invite url on native')
	@unittest.skip("Bug# 152052558. Same user duplicated in employee table")
	def test_existing(self):
		"""employees : Add .                               test_existing"""

		# kind of weird behavior. Sending invite to existing employee with
		# same email/phone, but different Employee ID.
		# responding to invite works as expected, but...
		# employee now in table twice.


		# assert sending invite to existing employee works as expected
		credentials = self.lili.credentials
		first_name = credentials['first_name']
		last_name = credentials['last_name']
		email = credentials['email']
		phone = credentials['phone']
		dob = '01/01/1984'
		zip_code = '12345'
		employee_id = self.nicol.generate_number(8)

		# nicol: send invite to lili
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		add_page = self.nicol.employee_add_page
		invitations_page = self.nicol.invitations_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		emp_page.click_plus()
		emp_page.click_add_employee()
		self.assertTrue(add_page.on())
		add_page.set_value('first_name', first_name)
		add_page.set_value('last_name', last_name)
		add_page.set_value('email', email)
		add_page.set_value('phone', phone)
		add_page.set_value('zip_code', zip_code)
		add_page.set_value('dob', dob)
		add_page.set_value('employee_id', employee_id)
		add_page.click_continue()
		time.sleep(1)

		# invitation should not initially show up in employee table
		self.assertTrue(emp_page.on())
		urls = emp_page.get_secret_urls()
		emp_page.click_toast() # clear toast or cannot click logout (mobile)
		time.sleep(.4)
		self.assertIsNone(emp_page.get_employee('id',employee_id),
			"New Invite should not be in employee table.")
		emp_page.menu.sign_out()

		# lili responds to invitation
		dob_page = self.lili.dob_page
		invite_page = self.lili.invite_page
		signin_page = self.lili.enroll_signin_page
		account_page = self.lili.account_page
		home_page = self.lili.for_employers

		self.driver.get(urls['email_url'])
		print(urls['email_url'])
		time.sleep(2)
		self.assertTrue(dob_page.on())
		dob_page.set_dob(dob)
		self.assertEqual(dob, dob_page.get_dob())
		dob_page.set_zip(zip_code)
		self.assertEqual(zip_code, dob_page.get_zip())
		dob_page.click_continue()

		self.assertTrue(invite_page.on())
		invite_page.enter_email(email)
		time.sleep(1)
		#"Already invited, please sign in" page.
		self.assertTrue(signin_page.on())
		signin_page.enter_password(credentials['password'])
		time.sleep(1)
		self.assertTrue(account_page.on())
		account_page.menu.sign_out()

		# nicol asserts lili is in invite table w/ right info then remove
		self.assertTrue(home_page.on())
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('invitations')

		self.assertTrue(invitations_page.on())
		invitation = (
			invitations_page.get_invitation('employee id', employee_id))
		self.assertEqual(first_name + ' ' + last_name, invitation['name'])
		self.assertEqual(employee_id, invitation['id'])
		self.assertEqual(phone, invitation['phone'])
		self.assertEqual(email, invitation['email'])

		invitations_page.toggle_invitation('employee id', employee_id)
		invitations_page.delete_invitations()

	@unittest.skipIf(main.get_priority() < 3, "Priority")
	def test_form(self):
		"""employees : Add .                                   test_form"""
		# assert add employee form works as expected
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		add_page = self.nicol.employee_add_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		emp_page.click_plus()
		emp_page.click_add_employee()

		# Assert must have valid email
		# Assert must have valid phone number
		email = 'email@example.com'
		bad_dob = '00/00/0000'
		dob = '12/31/1995'
		zip_code = '12345'
		employee_id = self.nicol.generate_number(8)

		tag = 'p'
		error1 = 'Required'
		# 5 required fields: first name, last name, id, dob, zip
		error2 = "Either the email address or mobile phone is required."
		dob_error = "Date Format: mm/dd/yyyy"
		zip_error = "Expected Zip Code format: 12345 or 12345-1234."
		num_el = add_page.number_of_elements
		num_containing = add_page.number_of_elements_containing

		self.assertTrue(add_page.on())
		self.assertEqual(0, num_el(tag, error1))
		add_page.click_continue()
		self.assertEqual(5, num_el(tag, error1))
		self.assertEqual(2, num_el(tag, error2))

		add_page.set_value('first_name', 'Poli')
		add_page.click_continue()
		self.assertEqual(4, num_el(tag, error1))

		add_page.set_value('last_name', 'Wag')
		add_page.click_continue()
		self.assertEqual(3, num_el(tag, error1))

		add_page.set_value('email', email)
		add_page.click_continue()
		self.assertEqual(0, num_el(tag, error2))

		add_page.set_value('employee_id', employee_id)
		add_page.click_continue()
		self.assertEqual(2, num_el(tag, error1))

		add_page.set_value('zip_code', zip_code[:-1])
		add_page.click_continue()
		self.assertEqual(1, num_el(tag, error1))
		self.assertEqual(1, num_el(tag, zip_error))
		add_page.set_value('zip_code', zip_code)
		add_page.click_continue()
		self.assertEqual(0, num_el(tag, zip_error))
		self.assertEqual(1, num_el(tag, error1))

		add_page.set_value('dob', bad_dob)
		add_page.click_continue()
		self.assertEqual(0, num_el(tag, error1))
		self.assertEqual(1, num_el(tag, dob_error))

		add_page.set_value('dob', dob)
		self.assertEqual(0, num_el(tag, error1))
		if not main.is_ios():
			self.assertEqual(0, num_el(tag, dob_error))

		# Shouldn't be able to put numbers in name fields
		name_error = 'Only letters are allowed.'
		add_page.set_value('first_name', "1name")
		add_page.click_continue()
		self.assertEqual(1, num_el(tag, name_error))
		add_page.set_value('last_name', "2name")
		add_page.click_continue()
		self.assertEqual(2, num_el(tag, name_error))
		add_page.set_value('first_name', 'Poli')
		add_page.set_value('last_name', 'Wag')

		# Should complain about invalid emails/phone#
		invalid_emails = ['invalid', 'invalid@', 'invalid.com']
		invalid_phones = ['1234567890', '801123456']#, '7775551234'] #555-0100 - 555-0199 reserved for fictional use (nationalnanpa.com)
		# helper elements don't exist until there's an error to display
		for i, email in enumerate(invalid_emails):
			add_page.set_value('email', invalid_emails[i])
			add_page.click_continue()
			self.WDWait.until(EC.presence_of_element_located((By.ID, 'undefined_helper')))
			email_error = self.driver.find_element_by_id('undefined_helper')
			self.WDWait.until(lambda x: "Invalid email address" in email_error.text)
			self.assertEqual(1, num_el(tag, 'Invalid email address'))
			self.assertEqual(0, num_containing(tag, 'not a valid phone number'))
		add_page.set_value('email', '')

		for i, phone in enumerate(invalid_phones):
			add_page.set_value('phone', invalid_phones[i])
			add_page.click_continue()
			self.assertEqual(0, num_el(tag, 'Invalid email address'))
			self.assertEqual(1, num_containing(tag, 'not a valid phone number'))

	def test_new(self):
		"""employees : Add .                                 test_new"""
		# create new invitation from employee table.
		# verify info is correct in invitations table
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		add_page = self.nicol.employee_add_page
		view_page = self.nicol.employee_view_page
		invitations_page = self.nicol.invitations_page
		invite_card = self.nicol.invitation_card_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = "Pagination"
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		# add employee
		self.assertTrue(emp_page.on())
		first_name = 'Poli'
		last_name = 'Wag'
		email = self.nicol.generate_email()
		phone = '202341' + self.nicol.generate_number(4)
		employee_id = self.nicol.generate_number(8)
		dob = '01/01/1984'
		zip_code = '12345'
		emp_page.click_plus()
		emp_page.click_add_employee()

		self.assertTrue(add_page.on())
		add_page.set_value('first_name', first_name)
		add_page.set_value('last_name', last_name)
		add_page.set_value('email', email)
		add_page.set_value('employee_id', employee_id)
		add_page.set_value('dob', dob)
		add_page.set_value('zip_code', zip_code)
		add_page.click_continue()

		self.assertTrue(emp_page.on())
		urls = emp_page.get_secret_urls()
		emp_page.click_toast()
		emp_page.menu.click_option('invitations')

		# make sure invitation is properly setup in invitations table
		self.assertTrue(invitations_page.on())
		invitation = (
			invitations_page.get_invitation('employee id', employee_id))
		# This will fail if > 15 invitations on 1st page
		if not invitation:
			# Assume it's on last page
			invitations_page.go_to_page('last')
			invitation = (
				invitations_page.get_invitation('employee id', employee_id))
		self.assertIsNotNone(invitation)
		self.assertEqual(first_name + ' ' + last_name, invitation['name'])
		self.assertEqual(employee_id, invitation['id'])
		self.assertEqual('', invitation['phone'])
		self.assertEqual(email, invitation['email'])

		# check out invitationCard
		invitations_page.click_invitation('employee id', employee_id)
		self.assertTrue(invite_card.on())
		self.assertEqual(invite_card.invite_info['id'], employee_id)
		self.assertEqual(invite_card.invite_info['zip'], zip_code)
		self.assertEqual(invite_card.invite_info['dob'], dob)
		self.assertEqual(invite_card.invite_info['email'], email)
		# self.assertEqual(invite_card.invite_info['date_created'], )
		self.assertEqual(invite_card.invite_info['status'], 'Sent')
		# can't edit info yet.
		invite_card.header.click_back()
		self.assertTrue(invitations_page.on())

		invitations_page.toggle_invitation('employee id', employee_id)
		invitations_page.delete_invitations()

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_table_footer(self):
		"""employees : Add .                           test_table_footer"""
		#dependencies: Nicol has business Pagination with 46 pending invites
		lobby_page = self.nicol.lobby_page
		invitations_page = self.nicol.invitations_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Pagination'
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())

		# should have 15 invitations and be on 1st page
		lobby_page.menu.click_option('invitations')
		self.assertTrue(invitations_page.on())
		self.assertEqual(15, invitations_page.num_invitations())
		self.assertEqual(1, invitations_page.current_page())
		self.assertFalse(invitations_page.previous_page())
		self.assertFalse(invitations_page.go_to_page('first'))
		self.assertFalse(invitations_page.go_to_page(5))

		# Go to page2
		self.assertTrue(invitations_page.next_page())
		self.assertEqual(15, invitations_page.num_invitations())
		self.assertEqual(2, invitations_page.current_page())

		# Go to page 3
		self.assertTrue(invitations_page.next_page())
		self.assertEqual(15, invitations_page.num_invitations())
		self.assertEqual(3, invitations_page.current_page())

		# Go to page 4
		self.assertTrue(invitations_page.next_page())
		self.assertEqual(1, invitations_page.num_invitations())
		self.assertEqual(4, invitations_page.current_page())
		self.assertFalse(invitations_page.next_page())
		self.assertFalse(invitations_page.go_to_page('last'))
		self.assertFalse(invitations_page.go_to_page(0))

		# Go back to page1
		self.assertTrue(invitations_page.previous_page())
		self.assertEqual(15, invitations_page.num_invitations())
		self.assertEqual(3, invitations_page.current_page())

		self.assertTrue(invitations_page.previous_page())
		self.assertEqual(15, invitations_page.num_invitations())
		self.assertEqual(2, invitations_page.current_page())

		self.assertTrue(invitations_page.previous_page())
		self.assertEqual(15, invitations_page.num_invitations())
		self.assertEqual(1, invitations_page.current_page())

		# Go to last page
		self.assertTrue(invitations_page.go_to_page('last'))
		self.assertEqual(1, invitations_page.num_invitations())
		self.assertEqual(4, invitations_page.current_page())

		# Go to first page
		self.assertTrue(invitations_page.go_to_page('first'))
		self.assertEqual(15, invitations_page.num_invitations())
		self.assertEqual(1, invitations_page.current_page())

	@unittest.skipIf(main.is_android(), "Cannot handle election download popups")
	def test_table_invite(self):
		"""employees : Add .                            test_table_invite"""
		# Nicol: create new invitation from invite table.
		# verify info is correct in table
		# verify invitation does not show up in employee table

		# Poli: respond to invitation and complete (don't set election)

		# Nicol: verify invitation removed from invite table (BUG)
		# verify Poli now in employee table ('inactive', $0)

		# Poli: set pay election

		# Nicol: check employee table (still 'inactive' and $0)
		# Check pending elections table and process
		# Check employee table ('active', new amount)

		lobby_page = self.nicol.lobby_page
		invitations_page = self.nicol.invitations_page
		add_page = self.nicol.employee_add_page
		emp_page = self.nicol.employee_page
		pe_page = self.nicol.pending_elections_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('invitations')

		# create invitation
		self.assertTrue(invitations_page.on())
		invitations_page.add_invitation()
		self.assertTrue(add_page.on())
		first_name = 'Poli'
		last_name = 'Wag'
		email = self.nicol.generate_email()
		#print('email: ' + email)
		phone = '202341' + self.nicol.generate_number(4)
		#print('phone: ' + phone)
		employee_id = self.nicol.generate_number(8)
		#print('id: ' + employee_id)
		dob = '01/01/1984'
		zip_code = '12345'
		password = 'asdfasdf'

		add_page.set_value('first_name', first_name)
		add_page.set_value('last_name', last_name)
		add_page.set_value('email', email)
		add_page.set_value('employee_id', employee_id)
		add_page.set_value('dob', dob)
		add_page.set_value('zip_code', zip_code)
		add_page.click_continue()

		# verify invitation in invitation table
		# Bug: on employee table
		self.assertTrue(invitations_page.on())
		urls = invitations_page.get_secret_urls()
		invitation = (
			invitations_page.get_invitation('employee id', employee_id))
		# will fail on this line if too many invites for Multiverse
		self.assertEqual(first_name + ' ' + last_name, invitation['name'])
		self.assertEqual(employee_id, invitation['id'])
		self.assertEqual('', invitation['phone'])
		self.assertEqual(email, invitation['email'])

		# verify invitation isn't in employee table yet
		invitations_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		self.assertIsNone(emp_page.get_employee('id',employee_id, False))
		emp_page.menu.sign_out()

		# respond to invitation (don't set pay election)
		eHome = self.poli.eHome_page
		dob_page = self.poli.dob_page
		invite_page = self.poli.invite_page
		factor2_page = self.poli.enroll_factor2_page
		code_page = self.poli.enroll_code_page
		name_page = self.poli.enroll_name_page
		pw_page = self.poli.enroll_password_page
		accept_page = self.poli.enroll_accept_page
		eWelcome = self.poli.employee_welcome
		eHome = self.poli.eHome_page
		# election_page = self.poli.pay_election_page
		# main_election_page = self.poli.election_page
		home_page = self.poli.for_employers

		self.driver.get(urls['email_url'])
		print(urls['email_url'])
		self.assertTrue(dob_page.on())

		dob_page.set_dob(dob)
		self.assertEqual(dob, dob_page.get_dob())
		dob_page.set_zip(zip_code)
		self.assertEqual(zip_code, dob_page.get_zip())
		dob_page.click_continue()

		self.assertTrue(invite_page.on())
		invite_page.enter_email(email)

		self.assertTrue(factor2_page.on())
		factor2_page.set_contact(phone)
		factor2_page.click_continue()

		self.assertTrue(code_page.on())
		code_page.enter_code()

		self.assertTrue(name_page.on())
		name_page.click_continue()

		self.assertTrue(pw_page.on())
		pw_page.set_password(password)
		pw_page.click_continue()

		self.assertTrue(accept_page.on())
		accept_page.click_continue()

		# Welcome Slides
		eWelcome.next()
		eWelcome.next()
		eWelcome.next()
		eWelcome.next()
		eWelcome.done()

		# Logged in!
		self.assertTrue(eHome.on('election'))
		eHome.menu.sign_out()
		# This shouldn't work on native app. Somehow it does...
		self.assertTrue(home_page.on())

		# Nicol: verify invitation and employee table
		self.nicol.signin_page.go()
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('invitations')
		self.assertTrue(invitations_page.on())
		self.assertIsNone(
			invitations_page.get_invitation('employee id', employee_id))

		invitations_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		emp_poli = emp_page.get_employee('id', employee_id)
		self.assertEqual('Inactive', emp_poli['status'])
		self.assertEqual('', emp_poli['election'])
		self.assertEqual('Poli Wag', emp_poli['name'])
		emp_page.menu.sign_out()

		# Poli: Set pay election
		self.assertTrue(home_page.on())
		self.assertTrue(
			self.poli.login(self.driver, password, email), messages.login)

		election_amount = '10.00'
		eHome.set_election(business, election_amount)
		eHome.click_save_elections()
		self.assertTrue(eHome.on('election'))
		eHome.menu.sign_out()
		self.assertTrue(home_page.on())

		# Nicol: check employee table (still 'inactive' and $0)
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		emp_poli = emp_page.get_employee('id', employee_id)
		# will fail on next line: Story# 153182320
		# self.assertEqual('Inactive', emp_poli['status'])
		self.assertEqual('', emp_poli['election'])
		self.assertEqual('Poli Wag', emp_poli['name'])

		# Check pending elections table and process
		emp_page.menu.click_option('pending elections')
		self.assertTrue(pe_page.on())
		poli_pe = pe_page.get_election('employee id', employee_id)
		self.assertEqual(election_amount, poli_pe['amount'])
		self.assertEqual('Poli Wag', poli_pe['name'])
		pe_page.toggle_election('employee id', employee_id)
		pe_page.mark_as_processed()

		# Check employee table ('active', new amount)
		pe_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		emp_poli = emp_page.get_employee('id', employee_id)
		# Doesn't always refresh quickly.
		# Force refresh if they're not equal right away
		if election_amount + ' USD' == emp_poli['election']:
			self.assertEqual('Active', emp_poli['status'])
			self.assertEqual(election_amount + ' USD', emp_poli['election'])
		else:
			# Refresh and check again
			self.driver.refresh()
			self.assertTrue(emp_page.on())
			emp_poli = emp_page.get_employee('id', employee_id)
			self.assertEqual('Active', emp_poli['status'])
			self.assertEqual(election_amount + ' USD', emp_poli['election'])

		emp_page.remove_employee('id',employee_id)
	test_table_invite.e2e = True

	def test_table_reinvite(self):
		"""employees : Add .                           test_table_reinvite"""
		lobby_page = self.nicol.lobby_page
		invitations_page = self.nicol.invitations_page
		add_page = self.nicol.employee_add_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('invitations')

		# create invitation
		self.assertTrue(invitations_page.on())
		invitations_page.add_invitation()
		self.assertTrue(add_page.on())
		first_name = 'Poli'
		last_name = 'Wag'
		email = self.nicol.generate_email()
		phone = '202341' + self.nicol.generate_number(4)
		employee_id = self.nicol.generate_number(8)
		dob = '01/01/1984'
		zip_code = '12345'
		print(email)
		print(phone)
		print(employee_id)

		add_page.set_value('first_name', first_name)
		add_page.set_value('last_name', last_name)
		add_page.set_value('email', email)
		add_page.set_value('employee_id', employee_id)
		add_page.set_value('dob', dob)
		add_page.set_value('zip_code', zip_code)
		add_page.click_continue()

		# resend invitation, respond, check in employee table
		self.assertTrue(invitations_page.on())
		invitations_page.click_toast()
		invitations_page.toggle_invitation('employee id', employee_id)
		self.assertTrue(invitations_page.resend_invitations())


class TestDetails(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.nicol = profiles.Profile(self.driver,'nicol')
		self.poli = profiles.Profile(self.driver)
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_filter(self):
		"""employees : Details .                             test_filter"""
		# assert employee table filtering works as expected
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		#time.sleep(.6)

		#self.assertTrue(emp_page.on())

		emp_page.toggle_filter()
		active_schema = [0,0,1,0,0]
		emp_page.set_filter(active_schema)
		self.assertEqual(active_schema,emp_page.get_filters())
		time.sleep(.4)
		emp_page.load()
		# self.assertEqual(5,emp_page.num_employees())
		#Alejandro, Lili, Nicol, Sandy, Test

		employed_schema = [0,1,1,0,0]
		emp_page.set_filter(employed_schema)
		self.assertEqual(employed_schema,emp_page.get_filters())
		last_row = emp_page.num_employees()-1
		emp_page.load()
		self.assertIsNotNone(emp_page.get_employee('index',last_row))

		removed_schema = [1,1,1,1,0]
		emp_page.set_filter(removed_schema)
		self.assertEqual(removed_schema,emp_page.get_filters())
		time.sleep(1)
		self.WDWait.until(lambda x: EC.visibility_of_element_located((By.TAG_NAME, 'tr'))
			or EC.visibility_of_all_elements_located((By.CLASS_NAME, 'employeeDiv'))
			)
		emp_page.load()
		#raw_input('table visible?')
		#Needs lots of time to refresh employee table.
		conseco = emp_page.get_employee('name',"Zuriel Conseco")
		time.sleep(.4)
		self.assertEqual(conseco['status'],"Removed")

		emp_page.set_filter([1,1,1,1,1])
		self.assertTrue(emp_page.filter_is_active(4))
		time.sleep(1)
		self.WDWait.until(lambda x: EC.visibility_of_element_located((By.TAG_NAME, 'tr'))
			or EC.visibility_of_all_elements_located((By.CLASS_NAME, 'employeeDiv'))
			)
		emp_page.load()
		hernandez = emp_page.get_employee('name',"Aaron Hernandez")
		#time.sleep(.4)
		self.assertEqual(hernandez['status'],"Terminated")
		#Dependencies: "Zuriel Conseco" in table as "Removed"
			#"Aaron Hernandez" in table as "Terminated"

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_permissions(self):
		"""employees : Details .                         test_permissions"""
		# assert owner can set permissions for employees
		# dependencies: Needs employee w/ ID: 41530011
		# email: PermissionTester@example.com, pw: asdfasdf
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		add_page = self.nicol.employee_add_page
		view_page = self.nicol.employee_view_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		time.sleep(.4)
		self.assertTrue(emp_page.on())
		employee_id = '41530011'
		self.assertTrue(emp_page.click_employee('id', employee_id))

		# view Poli Wag and edit permissions
		self.assertTrue(view_page.on())
		self.assertFalse(view_page.has_horizontal_scroll())
		if str(view_page.get_admin_role()) == 'manager':    #Force reset
			view_page.set_admin_role('none')
		view_page.set_admin_role('manager')
		self.assertEqual('manager', view_page.get_admin_role_radio()) #id: employee_info

		self.assertTrue(view_page.on())
		self.assertEqual('manager', view_page.get_admin_role())
		view_page.set_admin_role('executive')
		self.assertEqual('executive', view_page.get_admin_role_radio())

		self.assertTrue(view_page.on())
		self.assertEqual('executive', view_page.get_admin_role())
		view_page.set_admin_role('none')
		self.assertEqual('none', view_page.get_admin_role_radio())
		self.assertTrue(view_page.on())
		self.assertEqual('none', view_page.get_admin_role())
		view_page.header.click_back()
		# think it needs a decent timer to load employees.
		# Lots of extra permission tab clicks. Refine in future?

		self.assertTrue(emp_page.on())

	def test_profile(self):
		"""employees : Details .                        test_profile"""
		# assert employer can edit employee profile
		#dependencies: Employee "Stand Alone2" in table
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		view_page = self.nicol.employee_view_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != 'Multiverse':
			lobby_page.menu.select_business('Multiverse')
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		alone2 = emp_page.get_employee('name',"Stand Alone2")
		self.assertTrue(emp_page.click_employee('name', alone2['name']))

		self.assertTrue(view_page.on())
		self.assertEqual(alone2['name'],view_page.employee_name.text)
		self.assertEqual(alone2['id'],view_page.id.text)
		self.assertEqual(alone2['status'],view_page.status.text)
		if alone2['election'] == "":
			self.assertEqual("0.00 USD",view_page.election.text)
		else:
			self.assertEqual(alone2['election'],view_page.election.text)
		default_role = view_page.get_admin_role()

		# edit fields are as expected
		view_page.edit()
		self.assertFalse(view_page.save_changes.is_enabled())
		self.assertEqual(alone2['id'],view_page.get_id())
		self.assertEqual(alone2['name'], view_page.get_first_name()
			+ ' ' + view_page.get_last_name())

		# set and save new role, page loads as expected
		# toggle between none/manager (don't care what it is initially)
		new_role = 'manager'
		if default_role == new_role:
			new_role = 'none'
		view_page.set_admin_role(new_role)
		self.assertTrue(view_page.on())
		self.assertEqual(new_role, view_page.get_admin_role_radio())

		self.assertEqual(new_role, view_page.get_admin_role())

		# changes reflected in employee table
		view_page.header.click_back()
		self.assertTrue(emp_page.on())
		updated_alone2 = emp_page.get_employee('name', "Stand Alone2")
		self.assertEqual(updated_alone2['status'], alone2['status'])
		self.assertEqual(updated_alone2['election'], alone2['election'])

	def test_search(self):
		"""employees : Details .                              test_search"""
		# TODO
		# Assert the search function works properly (Name, Emp. ID)
		# Can't find old profiles (old = removed/terminated?)

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_sort(self):
		"""employees : Details .                               test_sort"""
		# assert employee table sort functionality works as expected
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != 'Multiverse':
			lobby_page.menu.select_business('Multiverse')
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		last_row = -1
		emp_page.set_sort(4)
		employee = emp_page.get_employee('index', 0)
		emp_page.set_sort(4, False)
		employee2 = emp_page.get_employee('index', last_row)
		self.assertEqual(employee, employee2)

		emp_page.set_sort(1)
		employee = emp_page.get_employee('index', 0)
		emp_page.set_sort(1, False)
		employee2 = emp_page.get_employee('index', last_row)
		self.assertEqual(employee, employee2)

		emp_page.set_sort(0)
		employee = emp_page.get_employee('index', 0)
		emp_page.set_sort(0, False)
		employee2 = emp_page.get_employee('index', last_row)
		self.assertEqual(employee, employee2)

	def test_verify_permissions(self):
		"""employees : Details .                   test_verify_permissions"""
		#Dependencies: Stand Alone3 empID = 301
		# also needs initial pay election set (otherwise land on election page)
		# Verify employee can use their permissions
		# (access employees and business-settings page)
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		view_page = self.nicol.employee_view_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		business = 'Multiverse'
		if lobby_page.menu.get_current_business() is not business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		# give alone3 'manager' role
		self.assertTrue(emp_page.on())
		alone3 = emp_page.get_employee('id','301')
		self.assertTrue(emp_page.click_employee('id',alone3['id']))
		self.assertTrue(view_page.on())
		if view_page.get_admin_role() != 'manager':
			view_page.set_admin_role('manager')
			self.assertEqual('manager', view_page.get_admin_role_radio())
			self.assertTrue(view_page.on())
		view_page.header.click_back()
		self.assertTrue(emp_page.on())
		emp_page.menu.sign_out()

		# verify alone3 can access manager content
		# should not be able to access admin/business settings
		self.alone3 = profiles.Profile(self.driver, 'alone3')
		lobby_page = self.alone3.lobby_page
		invitations_page = self.alone3.invitations_page
		pe_page = self.alone3.pending_elections_page
		emp_page = self.alone3.employee_page
		settings_page = self.alone3.business_settings_page
		admin_page = self.alone3.admin_page
		home_page = self.alone3.for_employers
		self.assertTrue(self.alone3.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('invitations')
		self.assertTrue(invitations_page.on())
		invitations_page.menu.click_option('pending elections')
		self.assertTrue(pe_page.on())
		pe_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		# should not have executive options in menu
		emp_page.menu.open()
		self.assertIsNone(emp_page.menu.admins)
		self.assertIsNone(emp_page.menu.business_settings)
		emp_page.menu.sign_out()

		# Nicol: give alone3 'executive' role
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		self.assertTrue(emp_page.click_employee('id','301'))
		self.assertTrue(view_page.on())
		view_page.set_admin_role('executive')
		self.assertEqual('executive', view_page.get_admin_role_radio())
		self.assertTrue(view_page.on())
		view_page.header.click_back()
		self.assertTrue(emp_page.on())
		emp_page.menu.sign_out()

		# verify alone3 can access executive pages (business settings, admin table)
		self.assertTrue(self.alone3.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('business settings')
		self.assertTrue(settings_page.on())
		settings_page.menu.click_option('admin')
		self.assertTrue(admin_page.on())
		admin_page.menu.sign_out()

		# reset alone3's permissions to None
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())
		self.assertTrue(emp_page.click_employee('id','301'))
		self.assertTrue(view_page.on())
		view_page.set_admin_role('none')
		self.assertEqual('none', view_page.get_admin_role_radio())
		self.assertTrue(view_page.on())
		self.assertEqual('none', view_page.get_admin_role())

# waiting: should be able to edit email/phone of pending invite
# after updating reinvite functionality...
	# takes quite a while after pressing ok to go back to employee page. Busy signal
# todo: verify email/text actually sends on reinvite
class TestInvitations(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.nicol = profiles.Profile(self.driver,'nicol')
		self.poli = profiles.Profile(self.driver)
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	# @unittest.skipIf(not main.is_web(), 'Cannot copy/paste invite URL on native')
	# @unittest.skip("Why link busted (# 156138803")
	def test_invite(self):
		"""employees : Invitations: .                         test_invite"""
		#Invite new employee, ensure invite link expires after use.
		lobby_page = self.nicol.lobby_page
		signin_page = self.nicol.signin_page
		emp_page = self.nicol.employee_page
		add_page = self.nicol.employee_add_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != 'Multiverse':
			lobby_page.menu.select_business('Multiverse')
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())

		first_name = 'Poli'
		last_name = 'Wag'
		email = self.nicol.generate_email()
		phone = '202491' + self.nicol.generate_number(4)
		employee_id = self.nicol.generate_number(8)
		dob = '01/01/1984'
		zip_code = '12345'

		emp_page.click_plus()
		emp_page.click_add_employee()

		self.assertTrue(add_page.on())
		add_page.set_value('first_name', first_name)
		add_page.set_value('last_name', last_name)
		add_page.set_value('email', email)
		add_page.set_value('employee_id', employee_id)
		add_page.set_value('dob', dob)
		add_page.set_value('zip_code', zip_code)
		add_page.click_continue()

		self.assertTrue(emp_page.on())
		urls = emp_page.get_secret_urls()
		print(urls)
		print(dob)
		print(zip_code)

		# self.assertIsNone(urls['phone'])
		# employee = emp_page.get_employee('id',employee_id)
		# self.assertEqual(first_name + " " + last_name, employee['name'])
		# self.assertEqual(employee_id, employee['id'])
		# self.assertEqual('Invited', employee['status'])
		emp_page.click_toast()
		emp_page.menu.sign_out()

		# go to url in invitation email, confirm email
		dob_page = self.poli.dob_page
		invite_page = self.poli.invite_page
		why_page = self.poli.why_email_page
		factor2_page = self.poli.enroll_factor2_page
		code_page = self.poli.enroll_code_page
		name_page = self.poli.enroll_name_page
		pw_page = self.poli.enroll_password_page
		accept_page = self.poli.enroll_accept_page
		eWelcome = self.poli.employee_welcome
		eHome = self.poli.eHome_page
		home_page = self.poli.for_employers

		self.driver.get(urls['email_url'])
		self.assertTrue(dob_page.on())
		dob_page.set_dob(dob)
		dob_page.set_zip(zip_code)
		dob_page.click_continue()

		self.assertTrue(invite_page.on())
		invite_page.click_why()

		self.assertTrue(why_page.on())
		why_page.click_continue()

		self.assertTrue(invite_page.on())
		invite_page.set_email(email)
		invite_page.click_continue()

		# Confirm phone#
		self.WDWait.until(EC.presence_of_element_located((By.ID, 'country_dropdown')))
		self.assertTrue(factor2_page.on())
		factor2_page.set_contact(phone)
		factor2_page.click_continue()

		# enter confirmation code
		self.assertTrue(code_page.on())
		code_page.enter_code()

		# Ensure name autofilled properly
		self.assertTrue(name_page.on())
		chk_first_name = name_page.get_first_name()
		chk_last_name = name_page.get_last_name()
		self.assertEqual(chk_first_name, first_name)
		self.assertEqual(chk_last_name, last_name)
		name_page.click_continue()

		#/accept/password -Create password, Continue
		self.assertTrue(pw_page.on())
		pw_page.set_password('asdfasdf')
		pw_page.click_continue()

		#/accept/agreement -Accept
		self.assertTrue(accept_page.on())
		accept_page.click_continue()

		# Welcome screens
		eWelcome.next()
		eWelcome.next()
		eWelcome.next()
		eWelcome.next()
		eWelcome.done()

		self.assertTrue(eHome.on('election'))

		#Ensure invite url is expired & user lands on account page
		self.driver.get(urls['email_url'])
		self.assertTrue(dob_page.on())
		self.assertTrue(dob_page.is_expired())
		# Sign back in and remove employee
		dob_page.click_continue()
		self.assertTrue(signin_page.on())
		signin_page.header.click_logo()

		self.assertTrue(home_page.on())
		self.assertTrue(home_page.header.signed_in())    #Expected behavior, signed in or out?
		home_page.header.sign_in()
		self.assertTrue(eHome.on('election'))
		eHome.menu.sign_out()

		self.assertTrue(home_page.on())
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		employee = emp_page.get_employee('id',employee_id)
		self.assertEqual('Inactive', employee['status'])

		emp_page.remove_employee('id',employee_id)

		# todo: different invite paths (respond to phone or email)
		# invite no phone
		# invite no email
		# respond to email - test_invite
		# respond to phone
		# autofill email
		# autofill change email
		# blank email
		# blank change email

	@unittest.skip("Always times out")
	def test_reinvite(self):
		"""employees : Invitations .                       test_reinvite"""
		# assert reinvite functionality works as expected
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		invite_page = self.nicol.invite_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != 'Multiverse':
			lobby_page.menu.select_business('Multiverse')
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		email = 'mime@example.com'
		employee_id = '21698411'
		self.assertTrue(emp_page.on())
		employee = emp_page.get_employee('id',employee_id)
		self.assertIsNotNone(employee)
		self.assertEqual('', employee['election'])
		self.assertEqual('Invited', employee['status'])
		emp_page.employee_menu('id',employee_id, 'Reinvite')
		emp_page.click_reinvite_ok()
		time.sleep(5)

		urls = emp_page.get_secret_urls()
		self.assertIsNotNone(urls['email'])
		self.assertIsNotNone(urls['phone'])
		self.assertNotEqual(urls['email_url'], urls['phone'])
		driver.get(urls['email_url'])
		WebDriverWait(driver, 8).until(
			lambda x: driver.find_element_by_class_name("btn-lg")
			)
		self.assertTrue(invite_page.on())
		driver.get(urls['phone_url'])
		WebDriverWait(driver, 5).until(
			lambda x: driver.find_element_by_class_name("btn-lg")
			)
		self.assertTrue(invite_page.on())
		#dependencies: Nicol has Multiverse employee with ID "216984100"
			# email "mime@fake.com" and status 'Invited'


class TestRemove(unittest.TestCase):
  def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.nicol = profiles.Profile(self.driver,'nicol')

  def tearDown(self):
		self.driver.quit()

  #@unittest.skip("Can click 'Remove' button on self. Bug #149857228")
  def test_self(self):
		"""employees : Remove .                                test_self"""
		# assert cannot remove self
		credentials = self.nicol.credentials
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		full_name = credentials['first_name'] + " " + credentials['last_name']
		try:
			emp_page.remove_employee('name',full_name)
			self.fail("Able to click remove on employer in employees list.")
		except (NoSuchElementException, WebDriverException):
			pass

  @unittest.skipIf(main.get_priority() < 2, "Priority = 2")
  def test_success(self):
		"""employees : Remove .                            test_success"""
		# TODO test that terminate and remove both work
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		add_page = self.nicol.employee_add_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != 'Multiverse':
			lobby_page.menu.select_business('Multiverse')
			self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		# new invites don't show up in employee table.
		# too lazy to go through entire invite process.
		# just remove random Poli Wag from Multiverse
		self.assertTrue(emp_page.on())
		emp_page.remove_employee('name', 'Poli Wag')
		self.assertTrue(emp_page.on())

		# self.assertTrue(emp_page.on())
		# email = 'svol@example.com'
		# emp_page.click_plus()
		# emp_page.click_add_employee()
		# self.assertTrue(add_page.on())
		# add_page.set_value('first_name', 'Sarkhan')
		# add_page.set_value('last_name', 'Vol')
		# add_page.set_value('email', email)
		# employee_id = ''.join(str(random.randint(0,9)) for _ in xrange(8))
		# add_page.set_value('employee_id', employee_id)
		# add_page.set_value('dob', '04/02/1234')
		# add_page.set_value('zip_code', '12345')
		# add_page.click_continue()
		# time.sleep(1)

		# self.assertTrue(emp_page.on())
		# emp_page.click_toast()
		# self.assertIsNotNone(emp_page.get_employee('id',employee_id), False)
		# emp_page.remove_employee('id',employee_id)
		# self.assertIsNone(emp_page.get_employee('id',employee_id, False))


