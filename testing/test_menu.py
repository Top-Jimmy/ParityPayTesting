import unittest
import time
import profiles
import browser
import main
import messages

# Total: 7
	# TestAB - 2                                A/B Testing options
		# test_confirmation_dialog
		# test_toggle
	# TestDefaultBehavior - 3            Options hide/show, navigation works
		# test_employee_buttons
		# test_employer_businesses
		# test_employer_buttons
	# TestRoleSwitching - 2              Role Switching works as expected
		# test_landing_pages
		# test_remembers_role

@unittest.skipIf(main.get_priority() < 3,"Priority")
class TestAB(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver,'cheeks')
		# self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	def test_confirmation_dialog(self):
		""" test_menu.py:TestAB.test_confirmation_dialog """
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		recip = 'Lourdes Ortega'

		# Should not get confirmation dialog when sending and option is turned off
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.set_ab_value('confirmCheck', False)
		self.assertTrue(eHome.on())
		eHome.send('bank')

		self.assertTrue(send_to_bank.on())
		send_to_bank.click_account(recip, 'Zions Bank')
		usd_amount = self.cheeks.generate_amount()
		send_to_bank.send_form.set_usd(usd_amount)
		send_to_bank.submit_send_form()
		send_to_bank.disclosure.click_continue()

		self.assertTrue(eHome.on('activity'))
		self.assertTrue(eHome.dialog_button is None)

		data = eHome.get_transaction()
		self.assertEqual(data['amount'], '-' + usd_amount)
		self.assertEqual(data['recipient'], recip)
		self.assertEqual(data['icon'], 'clock')
		self.assertEqual(data['status'], 'Arriving')
		eHome.menu.set_ab_value('confirmCheck', True)

	# out of date
	@unittest.skip("No speed toggle")
	def test_toggle(self):
		""" test_menu.py:TestAB.test_toggle """
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		send_page = self.cheeks.send_page
		td_page = self.cheeks.td_page

		# Login and select Lourdes Ortega
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		self.assertTrue(eHome.on())

		eHome.menu.set_ab_value('toggleCheck', False)
		eHome.send_money()

		self.assertTrue(recip_page.on())
		recip = 'Lourdes Ortega'
		recip_page.click_recipient(recip)

		# should have radio buttons
		self.assertTrue(send_page.on())
		self.assertEqual('radio', send_page.toggle_or_radio())
		usd_amount = self.cheeks.generate_amount()
		send_page.set_usd(usd_amount)
		# mxn_amount = send_page.get_mxn()
		send_page.set_speed('instant')
		self.assertEqual('instant', send_page.get_speed())
		send_page.click_continue()

		# continue through disclosure page
		self.assertTrue(disclosure_page.on())
		usd_total = disclosure_page.get_transfer_total()
		disclosure_page.click_continue()

		# clear confirmation dialog and confirm transaction completes
		self.assertTrue(eHome.on(True))
		eHome.clear_confirmation_dialog() #id send_money_button
		self.assertTrue(eHome.transaction_completes())
		self.assertTrue(eHome.on(True))
		data = eHome.get_transaction()
		self.assertEqual(data['amount'], '-' + usd_total)
		self.assertEqual(data['recipient'], recip)
		self.assertEqual(data['icon'], 'check')
		self.assertEqual(data['status'], 'Completed')

		# reset A/B, verify toggle is back
		eHome.menu.set_ab_value('toggleCheck', True)
		eHome.send_money()

		self.assertTrue(recip_page.on())
		recip = 'Lourdes Ortega'
		recip_page.click_recipient(recip)

		# should have toggle switch
		self.assertTrue(send_page.on())
		self.assertEqual('toggle', send_page.toggle_or_radio())

class TestDefaultBehavior(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.alone = profiles.Profile(self.driver,'alone6')
		self.nicol = profiles.Profile(self.driver, 'nicol')
		# self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	# Swipe not supported on materialUI 1.0
	# def test_basic(self):
	# 	"""Menu : DefaultBehavior .                                    basic"""
	# 	# Test different ways to open/close menu
	# 	eHome = self.cheeks.eHome_page

	# 	self.cheeks.login(self.driver)
	# 	self.assertTrue(acct_page.on())

	# 	if main.is_desktop():
	# 		# open
	# 		self.assertEqual(acct_page.menu.get_menu_status(), 'skinny')
	# 		acct_page.menu.open()
	# 		self.assertEqual(acct_page.menu.get_menu_status(), 'open')

	# 		# close
	# 		acct_page.menu.close()
	# 		self.assertEqual(acct_page.menu.get_menu_status(), 'skinny')
	# 	else:
	# 		# open
	# 		self.assertEqual(acct_page.menu.get_menu_status(), 'closed')
	# 		acct_page.menu.open()
	# 		self.assertEqual(acct_page.menu.get_menu_status(), 'open')

	# 		# close by click
	# 		acct_page.menu.close()
	# 		self.assertEqual(acct_page.menu.get_menu_status(), 'closed')

	# 		# open by swipe
	# 		acct_page.menu.open()
	# 		self.assertEqual(acct_page.menu.get_menu_status(), 'open')

	# 		# close by swipe
	# 		acct_page.menu.close('swipe')
	# 		self.assertEqual(acct_page.menu.get_menu_status(), 'closed')


	def test_employee_buttons(self):
		""" test_menu.py:TestDefaultBehavior.test_employee_buttons """
		# Stand Alone6 should have no employer permissions
		eHome = self.alone.eHome_page
		recip_page = self.alone.recipient_page
		send_page = self.alone.send_page
		election_page = self.alone.pay_election_page
		ps_page = self.alone.ps_page
		contact_us_page = self.alone.feedback_page
		about_page = self.alone.about_private_page

		self.assertTrue(self.alone.login(self.driver), messages.login)

		# waiting: terms and privacy
		pages = [eHome, recip_page, ps_page, contact_us_page, about_page]
		redirects = ['eHome', 'recipients', 'settings', 'contact us', 'about']

		# Alone6: go through employee pages, assert menu is open
		# 1. should have employee buttons, but not employer buttons
		# 2. should have menu toggle, but no hamburger
		# 3. current page should be highlighted in drawer
		for i, page in enumerate(pages):
			#print('asserting on page: ' + page.__class__.__name__)
			self.assertTrue(page.on())
			# desktop: test toggle between skinny/open menu
			if main.is_desktop():
				page.menu.toggle()
				self.assertTrue(page.menu.is_drawer_visible())
				self.assertEqual('skinny', page.menu.get_menu_status())
				self.assertTrue(page.menu.is_option_selected(redirects[i]))

				# set back to 'open'
				page.menu.toggle()
			else:
				# mobile: defaults to closed menu
				# closes after changing pages
				# print('test: visible?')
				self.assertFalse(page.menu.is_drawer_visible())
				self.assertEqual('closed', page.menu.get_menu_status())
				# print('test: opening menu')
				page.menu.open()

			for index in xrange(len(pages)):
				# print('checking selection on page index: ' + str(index))
				if index == i:
					# current page should be highlighted
					self.assertTrue(page.menu.is_option_selected(redirects[index]))
				else:
					# non-current pages should not highlighted
					self.assertFalse(page.menu.is_option_selected(redirects[index]))

			# menu should be 'open' in employee role
			self.assertTrue(page.menu.is_drawer_visible())
			self.assertEqual('open', page.menu.get_menu_status())
			self.assertEqual('employee', page.menu.get_role())

			# has employee buttons
			self.assertTrue(page.menu.eHome is not None)
			self.assertTrue(page.menu.recipients is not None)

			# has universal buttons and role switch
			self.assertTrue(page.menu.settings is not None)
			self.assertTrue(page.menu.contact_us is not None)
			self.assertTrue(page.menu.about is not None)
			self.assertTrue(page.menu.terms_and_privacy is not None)
			self.assertTrue(page.menu.logout is not None)
			# role switch depends on Alone6's current permissions.
			# Default should be no permissions (no role switch)
			self.assertTrue(page.menu.role_switch is None)

			# does not have employer buttons or role switch
			self.assertTrue(page.menu.current_business is None)
			# If drawer has add_button probably means user has no employers
			self.assertTrue(page.menu.add_button is None)
			self.assertTrue(page.menu.lobby is None)
			self.assertTrue(page.menu.employees is None)
			self.assertTrue(page.menu.pending is None)
			self.assertTrue(page.menu.business_settings is None)
			self.assertTrue(page.menu.admins is None)

			# desktop: should have toggle, hamburger not visible
			if main.is_desktop():
				self.assertTrue(page.menu.toggle_button is not None)
				self.assertTrue(page.menu.toggle_button.is_displayed())
				self.assertIsNone(page.menu.hamburger)
			else:
				# mobile: no toggle, has hamburger
				self.assertEqual(None, page.menu.toggle_button)
				self.assertTrue(page.menu.hamburger is not None)

			# go to next page (logout on last loop)
			# raw_input('end of loop: ' + page.__class__.__name__)
			try:
				page.menu.click_option(redirects[i+1])
			except IndexError:
				page.menu.sign_out()

	def test_employer_businesses(self):
		""" test_menu.py:TestDefaultBehavior.test_employer_businesses """
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		settings_page = self.nicol.business_settings_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.click_link('card', 2)

		self.assertTrue(emp_page.on())

	# assert basic menu behavior
		if not main.is_desktop():
			# open menu on mobile
			self.assertFalse(emp_page.menu.is_drawer_visible())
			emp_page.menu.open()

		self.assertTrue(emp_page.menu.is_drawer_visible())
		self.assertEqual('open', emp_page.menu.get_menu_status())
		self.assertEqual('employer', emp_page.menu.get_role())

	# clicking current business hides/shows right stuff
		emp_page.menu.click_current_business()

		# has universal buttons
		self.assertTrue(emp_page.menu.contact_us.is_displayed())
		self.assertTrue(emp_page.menu.about is not None)
		self.assertTrue(emp_page.menu.terms_and_privacy.is_displayed())
		self.assertTrue(emp_page.menu.logout.is_displayed())

		# does not have employer buttons (except current and add button)
		self.assertTrue(emp_page.menu.current_business.is_displayed())
		self.assertTrue(emp_page.menu.add_button.is_displayed())
		# Nicol should have businesses.. No idea why this is here
		# self.assertEqual([], emp_page.menu.businesses)
		self.assertEqual(None, emp_page.menu.lobby)
		self.assertEqual(None, emp_page.menu.employees)
		self.assertEqual(None, emp_page.menu.business_settings)
		self.assertEqual(None, emp_page.menu.admins)
		self.assertEqual(None, emp_page.menu.settings)

		# desktop: should have toggle, no hamburger
		if main.is_desktop():
			self.assertTrue(emp_page.menu.toggle_button is not None)
			self.assertTrue(emp_page.menu.toggle_button.is_displayed())
			self.assertIsNone(emp_page.menu.hamburger)
		else:
			# mobile: no toggle, has hamburger
			self.assertEqual(None, emp_page.menu.toggle_button)
			self.assertTrue(emp_page.menu.hamburger is not None)

	 # closing current business hides/shows right stuff
		emp_page.menu.click_current_business()

		# has universal buttons
		self.assertTrue(emp_page.menu.settings.is_displayed())
		self.assertTrue(emp_page.menu.contact_us.is_displayed())
		self.assertTrue(emp_page.menu.about is not None)
		self.assertTrue(emp_page.menu.terms_and_privacy.is_displayed())
		self.assertTrue(emp_page.menu.logout.is_displayed())

		# employer buttons
		self.assertTrue(emp_page.menu.current_business.is_displayed())
		self.assertEqual(None, emp_page.menu.add_button)
		self.assertEqual([], emp_page.menu.businesses)
		self.assertTrue(emp_page.menu.lobby.is_displayed())
		self.assertTrue(emp_page.menu.employees.is_displayed())
		self.assertTrue(emp_page.menu.business_settings.is_displayed())
		self.assertTrue(emp_page.menu.admins.is_displayed())

		# desktop: should have toggle, hamburger not visible
		if main.is_desktop():
			self.assertTrue(emp_page.menu.toggle_button is not None)
			self.assertTrue(emp_page.menu.toggle_button.is_displayed())
			self.assertIsNone(emp_page.menu.hamburger)
		else:
			# mobile: no toggle, has hamburger
			self.assertEqual(None, emp_page.menu.toggle_button)
			self.assertTrue(emp_page.menu.hamburger is not None)

	def test_employer_buttons(self):
		""" test_menu.py:TestDefaultBehavior.test_employer_buttons """
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		pe_page = self.nicol.pending_elections_page
		settings_page = self.nicol.business_settings_page
		admin_page = self.nicol.admin_page
		ps_page = self.nicol.ps_page
		contact_us_page = self.nicol.feedback_page
		about_page = self.nicol.about_private_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		# waiting: terms and privacy
		pages = [lobby_page, emp_page, pe_page, settings_page, admin_page, ps_page,
			 contact_us_page, about_page]
		redirects = ['lobby', 'employees', 'pending elections',
			'business settings', 'admin', 'settings', 'contact us', 'about']

		# Nicol: go through employee pages, assert menu is open
		# menu should have employer buttons, but not employee buttons
		# current page should be highlighted in drawer
		for i, page in enumerate(pages):
			print('asserting on page: ' + page.__class__.__name__)
			self.assertTrue(page.on())

			# desktop: test toggle between skinny/open menu
			if main.is_desktop():
				page.menu.toggle()
				self.assertTrue(page.menu.is_drawer_visible())
				self.assertEqual('skinny', page.menu.get_menu_status())
				self.assertTrue(page.menu.is_option_selected(redirects[i]))

				# set back to 'open'
				page.menu.toggle()
			else:
				# mobile: defaults to closed menu
				# closes after changing pages
				self.assertFalse(page.menu.is_drawer_visible())
				self.assertEqual('closed', page.menu.get_menu_status())
				page.menu.open()

			for index in xrange(len(pages)):
				# print('checking selection on page index: ' + str(index))
				if index == i:
					# current page highlighted in menu
					self.assertTrue(page.menu.is_option_selected(
						redirects[index]))
				else:
					# non-current pages not highlighted in menu
					self.assertFalse(page.menu.is_option_selected(
						redirects[index]))

			# menu should be 'open' with employer role
			self.assertTrue(page.menu.is_drawer_visible())
			self.assertEqual('open', page.menu.get_menu_status())
			self.assertEqual('employer', page.menu.get_role())

			# does not have employee buttons
			self.assertTrue(page.menu.eHome is None)
			self.assertTrue(page.menu.recipients is None)

			# has universal buttons
			self.assertTrue(page.menu.settings is not None)
			self.assertTrue(page.menu.contact_us is not None)
			self.assertTrue(page.menu.about is not None)
			self.assertTrue(page.menu.terms_and_privacy is not None)
			self.assertTrue(page.menu.logout is not None)

			# has employer buttons and role switch
			self.assertTrue(page.menu.current_business is not None)
			self.assertTrue(page.menu.lobby is not None)
			self.assertTrue(page.menu.employees is not None)
			self.assertTrue(page.menu.pending is not None)
			self.assertTrue(page.menu.business_settings is not None)
			self.assertTrue(page.menu.admins is not None)
			self.assertTrue(page.menu.role_switch is not None)

			# desktop: should have toggle, no hamburger
			if main.is_desktop():
				self.assertTrue(page.menu.toggle_button is not None)
				self.assertTrue(page.menu.toggle_button.is_displayed())
				self.assertIsNone(page.menu.hamburger)
			else:
				# mobile: no toggle, has hamburger
				self.assertEqual(None, page.menu.toggle_button)
				self.assertTrue(page.menu.hamburger is not None)

			# go to next page (logout on last loop)
			try:
				page.menu.click_option(redirects[i+1])
			except IndexError:
				page.menu.sign_out()


class TestRoleSwitching(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.nicol = profiles.Profile(self.driver, 'nicol')
		self.tester = profiles.Profile(self.driver, 'test')
		# self.WDWait = WebDriverWait(self.driver, 10)

	def tearDown(self):
		self.driver.quit()

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_landing_pages(self):
		""" test_menu.py:TestRoleSwitching.test_landing_pages """
		# Changing roles should land on expected pages
		# Employer default: 'employee' page (should eventually get lobby page)
		# Employee default: 'account' page
		lobby_page = self.nicol.lobby_page
		ps_page = self.nicol.ps_page
		eHome = self.nicol.eHome_page
		recip_page = self.nicol.recipient_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		# Go to 'employee' role
		self.assertTrue(lobby_page.on())
		lobby_page.menu.click_option('settings')
		self.assertTrue(ps_page.on())
		self.assertEqual('employer', ps_page.menu.get_role())
		ps_page.menu.set_role('employee')
		self.assertTrue(eHome.on())

		#Desktop: Menu should maintain state
		#Mobile: Menu should close after switching
		if main.is_desktop():
			self.assertEqual('open', eHome.menu.get_menu_status())
		else:
			self.assertEqual('closed', eHome.menu.get_menu_status())

		# Go to 'employer' role
		eHome.menu.click_option('recipients')
		self.assertTrue(recip_page.on())

		recip_page.menu.set_role('employer')
		self.assertTrue(lobby_page.on())

		if main.is_desktop():
			self.assertEqual('open', lobby_page.menu.get_menu_status())
		else:
			self.assertEqual('closed', lobby_page.menu.get_menu_status())

		# repeat steps w/ skinny nav
		if main.is_desktop():
			lobby_page.menu.toggle()
			self.assertEqual('skinny', lobby_page.menu.get_menu_status())
			lobby_page.menu.click_option('settings')
			self.assertTrue(ps_page.on())
			ps_page.menu.set_role('employee')

			# menu should stay skinny
			self.assertTrue(eHome.on())
			self.assertEqual('skinny', eHome.menu.get_menu_status())

			# go back to 'employer' role
			eHome.menu.click_option('recipients')
			self.assertTrue(recip_page.on())
			self.assertEqual('skinny', recip_page.menu.get_menu_status())
			recip_page.menu.set_role('employer')

			self.assertTrue(lobby_page.on())
			self.assertEqual('skinny', lobby_page.menu.get_menu_status())

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_remembers_role(self):
		""" test_menu.py:TestRoleSwitching.test_remembers_role """
		# User profile defaults to employer role
		lobby_page = self.nicol.lobby_page
		emp_page = self.nicol.employee_page
		eHome = self.nicol.eHome_page
		recip_page = self.nicol.recipient_page
		self.assertTrue(self.nicol.login(self.driver), messages.login)

		self.assertTrue(lobby_page.on())
		lobby_page.menu.set_role('employee')

		self.assertTrue(eHome.on())
		eHome.menu.sign_out()

		# asserts remembers 'employee' role when logging back in
		# self.nicol.login(self.driver)
		# self.assertTrue(acct_page.on())

		# # reset back to employer role
		# acct_page.menu.set_role('employer')
		# self.assertTrue(emp_page.on())

		# not remembering role when logging out.
		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())





