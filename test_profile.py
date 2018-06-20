import time
import unittest
from decimal import *
import profiles
import browser
import main
import messages
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Total - 10
# TestElection - 3               Set pay election
	# test_multiple_elections
	# test_single_election
	# test_zero_election
# TestPS - 7     Employer pages, add/edit phone & email, edit pw
	# test_add_email
	# test_add_phone
	# test_change_language
	# test_change_password
	# test_employers
	# test_update_email
	# test_update_phone

class TestElection(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver,'cheeks')
		self.lili = profiles.Profile(self.driver, 'lili')
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	# @unittest.skipIf(main.is_android(), "Manually test Android")
	def test_multiple_elections(self):
		"""profile : Election .                           multiple elections"""
		# dependencies: sandy cheeks works for Dunkin' Donuts and multiverse
		eHome = self.cheeks.eHome_page
		election_page = self.cheeks.pay_election_page
		history_page = self.cheeks.election_history_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.setTab('election')

		# save button should be disabled and gray until changes are made
		self.assertFalse(eHome.is_enabled(eHome.save_button))
		disabled_color = 'rgb(170, 170, 170)'
		background = eHome.save_button.value_of_css_property('background')
		self.assertTrue(disabled_color in background)

		# set 2 pay elections
		business1 = "Dunkin' Donuts"
		business2 = "Multiverse"
		new_election1 = self.cheeks.generate_amount()
		new_election2 = self.cheeks.generate_amount()

		original_elections = eHome.get_elections()
		eHome.set_election(business1, new_election1)

		# save button should be enabled and blue after changes are made
		self.WDWait.until(EC.element_to_be_clickable((By.ID, 'save_election_button')))
		self.assertTrue(eHome.is_enabled(eHome.save_button))
		background = eHome.save_button.value_of_css_property('background')
		enabled_color = 'rgb(105, 214, 241)'
		self.assertTrue(enabled_color in background)

		eHome.set_election(business2, new_election2)
		new_elections = eHome.get_elections()
		new_total = str(Decimal(new_election1) + Decimal(new_election2))
		self.assertEqual(new_election1, new_elections[business1])
		self.assertEqual(new_election2, new_elections[business2])
		self.assertEqual(new_total, new_elections['total'])
		eHome.click_save_elections()

		# deal w/ prompt
		self.assertTrue(eHome.on('election'))
		self.assertTrue(eHome.has_election_prompt())
		self.assertFalse(eHome.has_save_election_button())
		eHome.clear_election_prompt()
		self.assertFalse(eHome.has_election_prompt())
		self.assertTrue(eHome.has_save_election_button())

		# checkout history
		eHome.view_election_history()
		self.assertTrue(history_page.on())
		history_entry1 = history_page.get_election(0)
		history_entry2 = history_page.get_election(1)

		if history_entry1['name'] == business1: # history_entry1 = Dunkin' Donuts
			elect1 = history_entry1
			elect2 = history_entry2
		else:                                   # history_entry1 = Multiverse
			elect1 = history_entry2
			elect2 = history_entry1

		self.assertTrue(elect1['amount'] == new_election1)
		self.assertTrue(elect1['name'] == business1)
		self.assertTrue(elect2['amount'] == new_election2)
		self.assertTrue(elect2['name'] == business2)

		# Elections should be pending
		history_page.header.click_back()
		self.assertTrue(eHome.on('election'))
		pending_elections = eHome.get_elections()
		self.assertTrue(pending_elections[business1 + " pending"])
		self.assertTrue(pending_elections[business2 + " pending"])

		# Check that custom keyboard stays open when toggling between inputs.
		if not main.is_desktop():
			pass

	# @unittest.skipIf(main.is_android() is True, "Manually test Android")
	def test_single_election(self):
		"""profile : Election .                              single election"""
		#dependencies: Lili is employee of 'Multiverse' w/ emp ID 13313113
		business = 'Multiverse'
		# process all pending elections for Multiverse
		lobby_page = self.nicol.lobby_page
		pe_page = self.nicol.pending_elections_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != business:
			lobby_page.menu.select_business(business)
			self.assertTrue(lobby_page.on())
		lobby_page.click_link('card', 1)
		self.assertTrue(pe_page.on())
		if pe_page.num_pending_elections() > 0:
			pe_page.mark_all_as_processed()
		pe_page.menu.sign_out()

		# lili: request new Multiverse election
		eHome = self.lili.eHome_page
		election_page = self.lili.pay_election_page
		history_page = self.lili.election_history_page
		self.assertTrue(self.lili.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.setTab('election')
		elections = eHome.get_elections()
		initial_election = elections[business]
		print(initial_election)
		# Lili should have single election field (no total)
		self.assertEqual(None, elections['total'])

		increase = self.lili.generate_amount()
		new_election = str(Decimal(initial_election) + Decimal(increase))
		print(new_election)

		eHome.set_election(business, new_election)
		new_elections = eHome.get_elections()
		self.assertEqual(new_election, new_elections[business])
		self.assertEqual(None, new_elections['total'])
		eHome.click_save_elections()
		self.assertTrue(eHome.on('election'))
		self.assertTrue(eHome.has_election_prompt())
		self.assertFalse(eHome.has_save_election_button())
		eHome.clear_election_prompt()
		self.assertFalse(eHome.has_election_prompt())
		self.assertTrue(eHome.has_save_election_button())

		# assert change is reflected in lili's election history
		eHome.view_election_history()
		self.assertTrue(history_page.on())
		election = history_page.get_election()
		self.assertTrue(election['name'] == business)
		self.assertTrue(election['amount'] == new_election)
		history_page.header.click_back()

		# election should be pending
		self.assertTrue(eHome.on('election'))
		pending_elections = eHome.get_elections()
		self.assertTrue(pending_elections[business + " pending"])
		eHome.menu.sign_out()

		# assert change is NOT reflected in Multiverse employee table
		emp_page = self.nicol.employee_page
		view_page = self.nicol.employee_view_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('employees')

		self.assertTrue(emp_page.on())
		lili = emp_page.get_employee('id','13313113')
		# should still be initial election
		# can fail if multiple elections have been requested w/out being processed.
		self.assertEqual(lili['election'], initial_election + " USD")
		self.assertNotEqual(lili['election'], new_election + " USD")

		self.assertTrue(emp_page.click_employee('id','13313113'))
		self.assertTrue(view_page.on())
		self.assertEqual(view_page.election.text, initial_election + " USD")
		self.assertNotEqual(view_page.election.text, new_election + " USD")
		view_page.header.click_back()
		self.assertTrue(emp_page.on())

		# process pending election and recheck employee table
		emp_page.menu.click_option('pending elections')
		self.assertTrue(pe_page.on())
		pe_page.mark_all_as_processed()
		pe_page.menu.click_option('employees')
		self.assertTrue(emp_page.on())

		lili = emp_page.get_employee('id', '13313113')

		# Doesn't always refresh quickly.
		# Force refresh if they're not equal right away
		if new_election + ' USD' == lili['election']:
			self.assertEqual('Active', lili['status'])
			self.assertEqual(new_election + ' USD', lili['election'])
		else:
			# Refresh and check again
			self.driver.refresh()
			self.assertTrue(emp_page.on())
			lili = emp_page.get_employee('id', '13313113')
			self.assertEqual('Active', lili['status'])
			self.assertEqual(new_election + ' USD', lili['election'])
		emp_page.menu.sign_out()

		# lili's election should not be pending
		self.assertTrue(self.lili.login(self.driver), messages.login)
		# not sure why this is different on native. I'm assuming app remembers which tab you were on
		if not main.is_web():
			self.assertTrue(eHome.on('election'))
		else:
			self.assertTrue(eHome.on())
			eHome.setTab('election')
		elections = eHome.get_elections()
		self.assertFalse(elections[business + ' pending'])
	test_single_election.e2e = True

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	# @unittest.skipIf(main.is_android() is True, "Manually test Android")
	def test_zero_election(self):
		"""profile : Election .                              zero   election"""
		# reset Lili's multiverse election back to 0
		business = 'Multiverse'
		eHome = self.lili.eHome_page
		election_page = self.lili.pay_election_page
		history_page = self.lili.election_history_page
		self.assertTrue(self.lili.login(self.driver), messages.login)

		# make sure lili has non-zero election
		self.assertTrue(eHome.on())
		eHome.setTab('election')
		elections = eHome.get_elections()
		initial_election = elections[business]
		if initial_election == '0.00':
			new_election = "1.00"
			eHome.set_election(business, new_election)
			new_elections = eHome.get_elections()
			self.assertEqual(new_election, new_elections[business])
			eHome.click_save_elections()
			eHome.clear_election_prompt()
			eHome.view_election_history()
			self.assertTrue(history_page.on())
			history_page.header.click_back()
			self.assertTrue(eHome.on('election'))
		eHome.menu.sign_out()

		lobby_page = self.nicol.lobby_page
		pe_page = self.nicol.pending_elections_page

		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != business:
				lobby_page.menu.select_business(business)
				self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('pending elections')

		self.assertTrue(pe_page.on())
		pe_page.mark_all_as_processed()
		# if main.is_desktop():
		#   pe_page.go_to_tab()
		#   self.assertTrue(lobby_page.on())    #fails if no elections pending.
		#   lobby_page.menu.sign_out()
		# else:
		pe_page.menu.sign_out()

		self.assertTrue(self.lili.login(self.driver), messages.login)

		# Seems like native app saves employeeTab even when you log out
		print('logged in')
		if main.get_browser() == 'native':
			self.assertTrue(eHome.on('election'))
		else:
			self.assertTrue(eHome.on())
			eHome.setTab('election')
		print('on eHome')
		new_election = "0.00"
		eHome.set_election(business, new_election)
		new_elections = eHome.get_elections()
		self.assertEqual(new_election, new_elections[business])
		eHome.click_save_elections()
		eHome.view_election_history()

		# assert change is reflected in lili's election history
		# Loading history page has failed before.
		# Seems to take forever for entries to load.
		self.assertTrue(history_page.on())
		election = history_page.get_election()
		self.assertTrue(election['name'] == business)
		self.assertTrue(election['amount'] == "0.00")
		history_page.header.click_back()

		# election should be pending
		self.assertTrue(eHome.on('election'))
		pending_elections = eHome.get_elections()
		self.assertTrue(pending_elections[business + " pending"])
		eHome.menu.sign_out()

		# Nicol: process election
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		if lobby_page.menu.get_current_business() != business:
				lobby_page.menu.select_business(business)
				self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('pending elections')

		self.assertTrue(pe_page.on())
		pe_page.mark_all_as_processed()


class TestPS(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver,'cheeks')
		self.alone6 = profiles.Profile(self.driver, 'alone6')
		# self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	def test_add_email(self):
		"""profile : PS .                                          add email"""
		# depenencies: expecting 1 existing email
		eHome = self.cheeks.eHome_page
		ps_page = self.cheeks.ps_page
		add_email_page = self.cheeks.ps_add_email_page
		confirmation_page = self.cheeks.ps_confirmation_page
		edit_email_page = self.cheeks.ps_edit_email_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('settings')

		self.assertTrue(ps_page.on())
		# remove email if it's there from last test
		new_email = "scheeks1@example.com"
		if ps_page.has_email(new_email):
				ps_page.edit_email(new_email)
				self.assertTrue(edit_email_page.on())
				edit_email_page.remove_email()
				self.assertTrue(ps_page.on())

		ps_page.add_email()

		self.assertTrue(add_email_page.on())
		self.assertTrue(add_email_page.continue_button.is_enabled())
		add_email_page.click_continue()
		# need some kind of wait here. Can fail if internet is slow at all.
		self.assertEquals(
			1,add_email_page.number_of_elements("p","Required"))
		add_email_page.set_email(new_email)
		add_email_page.click_continue() #id = code

		self.assertTrue(confirmation_page.on())
		#debug here
		confirmation_page.enter_code()

		self.assertTrue(ps_page.on())
		num_emails = len(ps_page.edit_email_buttons)
		self.assertEquals(2,num_emails)
		ps_page.edit_email(new_email)

		self.assertTrue(edit_email_page.on())
		edit_email_page.remove_email()

		self.assertTrue(ps_page.on())
		num_emails = len(ps_page.edit_email_buttons)
		self.assertEquals(1,num_emails)

	def test_add_phone(self):
		"""profile : PS .                                          add phone"""
		# dependencies: Sandy Cheeks with 1 phone#
		eHome = self.cheeks.eHome_page
		ps_page = self.cheeks.ps_page
		add_phone_page = self.cheeks.ps_add_phone_page
		confirmation_page = self.cheeks.ps_confirmation_page
		edit_phone_page = self.cheeks.ps_edit_phone_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('settings')

		self.assertTrue(ps_page.on())
		# remove phone# if there from last test
		new_phone = "(202) 554-2345"
		if ps_page.has_phone(new_phone):
				ps_page.edit_phone(new_phone)
				self.assertTrue(edit_phone_page.on())
				edit_phone_page.remove_phone()
				self.assertTrue(ps_page.on())

		self.assertEqual(1,len(ps_page.edit_phone_buttons))
		ps_page.add_phone()

		self.assertTrue(add_phone_page.on())
		add_phone_page.set_phone(new_phone)
		add_phone_page.click_continue()

		self.assertTrue(confirmation_page.on())
		confirmation_page.enter_code()

		self.assertTrue(ps_page.on())
		self.assertEqual(2,len(ps_page.edit_phone_buttons))
		ps_page.edit_phone(new_phone)

		self.assertTrue(edit_phone_page.on())
		edit_phone_page.remove_phone()

		self.assertTrue(ps_page.on())
		self.assertEquals(1,len(ps_page.edit_phone_buttons))

	def test_change_language(self):
		"""profile : PS .                                    CHANGE LANGUAGE"""
		# Must pass, else site will be in Spanish for subsequent tests
		# Can be expanded to verify persistance across session/logins?
		eHome = self.cheeks.eHome_page
		ps_page = self.cheeks.ps_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('settings')

		self.assertTrue(ps_page.on())
		ps_page.change_language('Spanish')
		self.assertTrue(ps_page.on())
		ps_page.change_language('English')
		self.assertTrue(ps_page.on())

	def test_change_password(self):
		"""profile : PS .                                    CHANGE PASSWORD"""
		# dependencies: Stand Alone4 w/ pw "asdfasdf"
		self.alone4 =  profiles.Profile(self.driver,'alone4')
		eHome = self.alone4.eHome_page
		ps_page = self.alone4.ps_page
		change_pw_page = self.alone4.ps_change_pw_page
		self.assertTrue(self.alone4.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('settings')

		self.assertTrue(ps_page.on())
		# failing on next line is login failure (wrong pw)
		ps_page.change_password()

		self.assertTrue(change_pw_page.on())
		original_pass = "asdfasdf"
		new_pass = "fibblejack"

		# Check Safari autofill issue
		self.assertEqual('', change_pw_page.get_current_pw())

		change_pw_page.click_continue()
		self.assertEquals(
			2,change_pw_page.number_of_elements("p","Required"))
		change_pw_page.enter_current_pw(original_pass)
		change_pw_page.click_continue()
		self.assertEquals(
			1,change_pw_page.number_of_elements("p","Required"))
		change_pw_page.enter_new_pw(new_pass)
		change_pw_page.click_continue()

		self.assertTrue(ps_page.on())
		ps_page.menu.sign_out()

		self.assertTrue(self.alone4.login(self.driver, new_pass), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('settings')

		self.assertTrue(ps_page.on())
		ps_page.change_password()

		self.assertTrue(change_pw_page.on())
		change_pw_page.enter_current_pw(new_pass)
		change_pw_page.enter_new_pw(original_pass)
		change_pw_page.click_continue()
		self.assertTrue(ps_page.on())

	# Should be fine on mobile (no drawer on employer page)
	def test_employers(self):
		"""profile : PS .                                          employers"""
		eHome = self.alone6.eHome_page
		ps_page = self.alone6.ps_page
		emp_page = self.alone6.employers_page
		self.assertTrue(self.alone6.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('settings')

		self.assertTrue(ps_page.on())
		# elements_containing = ps_page.number_of_elements_containing
		# num_employers = elements_containing('a','/settings/employer/','href')
		num_employers = ps_page.num_employers()
		print(num_employers)

		for i in xrange(num_employers):
			business_name = ps_page.employers[i].text
			ps_page.move_to_el(ps_page.employers[i])#.click()
			self.assertTrue(emp_page.on())
			self.assertFalse(emp_page.has_horizontal_scroll())

			# Check behavior after refresh (no refresh on native)
			if main.is_web():
				self.driver.refresh()
				self.assertTrue(emp_page.on())

			# Check menu (no menu on mobile)
			if main.is_desktop():
				# does not have employer buttons
				self.assertTrue(emp_page.menu.current_business is None)
				self.assertTrue(emp_page.menu.add_button is None)
				self.assertTrue(emp_page.menu.lobby is None)
				self.assertTrue(emp_page.menu.employees is None)
				self.assertTrue(emp_page.menu.pending is None)
				self.assertTrue(emp_page.menu.business_settings is None)
				self.assertTrue(emp_page.menu.admins is None)

				# has employee buttons
				self.assertTrue(emp_page.menu.eHome is not None)
				self.assertTrue(emp_page.menu.recipients is not None)

				# has universal buttons
				self.assertTrue(emp_page.menu.settings is not None)
				self.assertTrue(emp_page.menu.contact_us is not None)
				self.assertTrue(emp_page.menu.about is not None)
				self.assertTrue(emp_page.menu.terms_and_privacy is not None)
				self.assertTrue(emp_page.menu.logout is not None)

			emp_page.header.click_back()
			self.assertTrue(ps_page.on())

	def test_participate(self):
		"""profile : PS .                                        participate"""
		pass

	def test_update_email(self):
		"""profile : PS .                                       update email"""
		# dependencies: expecting default email (alone5@example.com)
		self.alone5 =  profiles.Profile(self.driver,'alone5')
		eHome = self.alone5.eHome_page
		ps_page = self.alone5.ps_page
		edit_email_page = self.alone5.ps_edit_email_page
		confirm_page = self.alone5.ps_confirmation_page
		self.assertTrue(self.alone5.login(self.driver), messages.login)

		# Sandy should not have permissions to any businesses
		self.assertTrue(eHome.on())
		eHome.menu.click_option('settings')

		self.assertTrue(ps_page.on())
		self.assertTrue(1 == len(ps_page.edit_email_buttons))
		ps_page.edit_email(0)

		self.assertTrue(edit_email_page.on())
		self.assertFalse(edit_email_page.is_enabled(edit_email_page.continue_button))
		original_email = "alone5@example.com"
		updated_email = "alone55@example.com"
		edit_email_page.set_email(updated_email)
		edit_email_page.click_continue()

		self.assertTrue(confirm_page.on())
		confirm_page.enter_code()

		self.assertTrue(ps_page.on())
		self.assertEqual(
			ps_page.edit_email_buttons[0].text, updated_email)
		ps_page.edit_email(0)

		self.assertTrue(edit_email_page.on())
		self.assertFalse(edit_email_page.remove_email())
		edit_email_page.set_email(original_email)
		edit_email_page.click_continue()

		self.assertTrue(confirm_page.on())
		confirm_page.enter_code()

		self.assertTrue(ps_page.on())
		num_emails = len(ps_page.edit_email_buttons)
		self.assertEqual(1, num_emails)
		self.assertEqual(ps_page.edit_email_buttons[0].text, original_email)

	def test_update_phone(self):
		"""profile : PS .                                       update phone"""
		# dependencies: sandy cheeks w/ phone# (202) 786-4237
		eHome = self.cheeks.eHome_page
		ps_page = self.cheeks.ps_page
		edit_phone_page = self.cheeks.ps_edit_phone_page
		confirmation_page = self.cheeks.ps_confirmation_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('settings')

		self.assertTrue(ps_page.on())
		self.assertEqual(1,len(ps_page.edit_phone_buttons))
		ps_page.edit_phone(0)

		self.assertTrue(edit_phone_page.on())
		self.assertEqual(None, edit_phone_page.remove_phone_button)
		new_phone = "(202) 554-2345"
		original_phone = "(202) 786-4237"

		# Test Safari autofill issue
		# Input should have existing phone#
		self.assertEqual(original_phone, edit_phone_page.get_phone())

		edit_phone_page.set_phone(new_phone)
		self.assertTrue(
				edit_phone_page.is_enabled(edit_phone_page.continue_button))
		edit_phone_page.click_continue()

		self.assertTrue(confirmation_page.on())
		confirmation_page.enter_code()

		self.assertTrue(ps_page.on())
		num_phones = len(ps_page.edit_phone_buttons)
		self.assertEqual(1, num_phones)
		ps_page.edit_phone(new_phone)

		self.assertTrue(edit_phone_page.on())
		edit_phone_page.set_phone(original_phone)
		edit_phone_page.click_continue()

		self.assertTrue(confirmation_page.on())
		confirmation_page.enter_code()

		self.assertTrue(ps_page.on())
		self.assertTrue(
			ps_page.edit_phone_buttons[0].text == original_phone)

