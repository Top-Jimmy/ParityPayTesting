import unittest
import time
from decimal import *
import profiles
import browser
import main
import messages

# TestBank - 6
	# test_add_account
	# test_add_mx_recipient
	# test_add_us_recipient
	# test_duplicate
	# test_navigation
	# test_no_balance
	# test_success

class TestBank(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver,'cheeks')
		self.nicol = profiles.Profile(self.driver,'nicol')

	def tearDown(self):
		self.driver.quit()

	def test_add_account(self):
		"""SendToBank: Bank .              test_add_account"""
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		recipient_list = self.cheeks.recipient_page
		recip_card = self.cheeks.recipient_view_page
		bank_page = self.cheeks.bank_account_page
		recip = 'David Castillo'

		# Give David a Wells Fargo account. Delete it.
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.add_account()
		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip)

		self.assertTrue(bank_page.on())
		routing_num = "031000503"
		acct_num = self.cheeks.generate_number(8)
		bank_page.set_routing(routing_num)
		bank_page.set_account(acct_num)
		bank_page.set_account_type('savings')
		bank_page.click_continue()
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))

		self.assertTrue(send_to_bank.click_account(recip, 'Wells Fargo Bank'))
		if not main.is_desktop():
			send_to_bank.header.click_back()
			self.assertTrue(send_to_bank.on([0, 'Choose Account']))
			send_to_bank.header.click_back()
			self.assertTrue(eHome.on())
			eHome.menu.click_option('recipients')
		else:
			send_to_bank.menu.click_option('recipients')

		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip)
		self.assertTrue(recip_card.on())
		recip_card.select_destination('bank', 'Wells Fargo')

		self.assertTrue(bank_page.on())
		bank_page.remove()
		self.assertTrue(recip_card.on())

	def test_add_mx_recipient(self):
		"""SendToBank: Bank .               test_add_mx_recipient"""
		# Should remember DOB when adding info for ATM
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		send_to_atm = self.cheeks.send_to_atm_page
		recipient_list = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		bank_page = self.cheeks.bank_account_page
		recip_card = self.cheeks.recipient_view_page
		
		recip_1 = self.cheeks.generate_name()
		clabe = '032180000118359719'
		dob = self.cheeks.generate_rfc_dob()

		# Add new US recipient. Click back to recipient list. Add account for recipient.
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.add_account()
		self.assertTrue(recipient_list.on())
		recipient_list.add_recipient()

		self.assertTrue(name_page.on())
		self.assertEqual('Mexico', name_page.get_location())
		name_page.set_location('us')
		self.assertEqual('United States', name_page.get_location())
		name_page.set_location('mx')
		self.assertEqual('Mexico', name_page.get_location())
		name_page.enter_name(recip_1)

		# Should go directly to adding a bank account after adding recipient
		# Bank account location should default to location of recipient
		self.assertTrue(bank_page.on())
		bank_page.header.click_back()
		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip_1)
		self.assertTrue(bank_page.on())
		routing_num = "031000503"
		acct_num = self.cheeks.generate_number(8)
		self.assertEqual('Mexico', bank_page.get_location())
		bank_page.set_location('us')
		self.assertEqual('United States', bank_page.get_location())
		bank_page.set_location('mx')
		self.assertEqual('Mexico', bank_page.get_location())
		bank_page.set_clabe(clabe)
		bank_page.click_continue()

		# MX accounts should prompt for DOB after selecting bank account
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		self.assertTrue(send_to_bank.click_account(recip_1, 0, True))
		send_to_bank.set_dob(dob)

		# Verify DOB is autofilled when trying to send to ATM
		send_to_bank.menu.click_option('ehome')
		self.assertTrue(eHome.on())
		eHome.send('atm')
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.click_recipient(recip_1)
		self.assertTrue(send_to_atm.on([0, 'Recipient'], True))
		info = send_to_atm.data_form.get_info()
		self.assertEqual(info['dob'], dob)

		# Delete recip_1		
		send_to_atm.header.click_back()
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.header.click_back()
		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')
		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip_1)
		self.assertTrue(recip_card.on())
		recip_card.remove_recipient()
		self.assertTrue(recipient_list.on())

	def test_add_us_recipient(self):
		"""SendToBank: Bank .               test_add_us_recipient"""
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		recipient_list = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		bank_page = self.cheeks.bank_account_page
		recip_card = self.cheeks.recipient_view_page

		recip_1 = self.cheeks.generate_name()
		routing_num = "031000503"
		acct_num = self.cheeks.generate_number(8)

		# Add new US recipient. Click back to recipient list. Add account for recipient.
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.add_account()
		self.assertTrue(recipient_list.on())
		recipient_list.add_recipient()

		self.assertTrue(name_page.on())
		self.assertEqual('Mexico', name_page.get_location())
		name_page.set_location('us')
		self.assertEqual('United States', name_page.get_location())
		name_page.enter_name(recip_1)

		# Should go directly to adding a bank account after adding recipient
		# Bank account location should default to location of recipient
		self.assertTrue(bank_page.on())
		bank_page.header.click_back()
		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip_1)
		self.assertTrue(bank_page.on())
		self.assertEqual('United States', bank_page.get_location())
		bank_page.set_location('mx')
		self.assertEqual('Mexico', bank_page.get_location())
		bank_page.set_location('us')
		bank_page.set_routing(routing_num)
		bank_page.set_account(acct_num)
		bank_page.set_account_type('savings')
		bank_page.click_continue()

		# Shouldn't ask for DOB when sending to US bank account
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.click_account(recip_1, 0)
		self.assertTrue(send_to_bank.on([1, 'Specify Amount']))

		# Go to recipients and delete both
		send_to_bank.header.click_back()
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.header.click_back()
		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')
		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip_1)
		self.assertTrue(recip_card.on())
		recip_card.remove_recipient()
		self.assertTrue(recipient_list.on())

	def test_duplicate(self):
		"""SendToBank: Bank .                             test_duplicate"""
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		recipient_list = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		bank_page = self.cheeks.bank_account_page
		recip_card = self.cheeks.recipient_view_page

		# Trying to add account for Jose should redirect to /add-account
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.add_account()
		self.assertTrue(recipient_list.on())
		recipient_list.add_recipient()
		self.assertTrue(name_page.on())
		recip1 = "Jose Ortega"
		name_page.enter_name(recip1)
		self.assertTrue(name_page.on(True))

		# Should only have option to add account or continue adding duplicate
		self.assertIsNone(name_page.duplicate_send)
		self.assertIsNotNone(name_page.duplicate_continue)
		self.assertIsNotNone(name_page.duplicate_add)
		self.assertIsNone(name_page.duplicate_view)

		name_page.click_duplicate_add()
		self.assertTrue(bank_page.on())
		bank_page.header.click_back()
		self.assertTrue(recipient_list.on())
		recipient_list.header.click_back()
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))

		# Adding duplicate of Rosa should go to /add-account
		send_to_bank.add_account()
		self.assertTrue(recipient_list.on())
		recipient_list.add_recipient()
		self.assertTrue(name_page.on())
		recip2 = "Rosa Castillo"
		name_page.enter_name(recip2)
		self.assertTrue(name_page.on(True))
		name_page.click_duplicate_continue()
		self.assertTrue(bank_page.on())
		bank_page.header.click_back()
		self.assertTrue(recipient_list.on())

		# Delete duplicate
		if main.is_desktop():
			recipient_list.menu.click_option('recipients')
		else:
			recipient_list.header.click_back()
			self.assertTrue(send_to_bank.on())
			send_to_bank.header.click_back()
			self.assertTrue(eHome.on())
			eHome.menu.click_option('recipients')
		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip2)
		self.assertTrue(recip_card.on())
		recip_card.remove_recipient()
		self.assertTrue(recipient_list.on())

	def test_navigation(self):
		"""SendToBank: Bank .                     test_navigation"""
		# Check back button and steps for all pages in send flow
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		td_page = self.cheeks.td_page
		recip = 'David Castillo'

		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on())
		# SendToBank goes back to eHome
		send_to_bank.header.click_back()
		self.assertTrue(eHome.on('send'))
		eHome.send('bank')
		self.assertTrue(send_to_bank.on())
		# Cannot skip ahead to steps 1 or 2
		send_to_bank.set_step(1, reloadPage=False)
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.set_step(2, reloadPage=False)
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		self.assertTrue(send_to_bank.click_account(recip, 0))

		# Amount step: cannot go to step 3
		send_to_bank.set_step(2, reloadPage=False)
		self.assertTrue(send_to_bank.on([1, 'Specify Amount']))
		# Can go forward to last 2 steps after setting amount and clicking continue
		usd_amount = self.cheeks.generate_amount()
		send_to_bank.send_form.set_usd(usd_amount)
		send_to_bank.send_form.click_continue()
		self.assertTrue(send_to_bank.on([2, 'Confirm & Send']))
		send_to_bank.set_step(0)
		send_to_bank.set_step(1)
		self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())
		send_to_bank.set_step(2)
		# check in different order
		send_to_bank.set_step(0)
		send_to_bank.set_step(2)
		send_to_bank.set_step(1)
		self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())

		# Go back to eHome.
		send_to_bank.set_step(2)
		send_to_bank.header.click_back()
		self.assertTrue(send_to_bank.on([1, 'Specify Amount']))
		send_to_bank.header.click_back()
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.header.click_back()

		# Shouldn't be able to skip ahead
		self.assertTrue(eHome.on())
		eHome.send('bank')
		self.assertTrue(send_to_bank.on())
		send_to_bank.set_step(1, reloadPage=False)
		send_to_bank.set_step(2, reloadPage=False)
		self.assertEqual([0, 'Choose Account'] , send_to_bank.stepper.get_current_step())

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_no_balance(self):
		"""SendToBank: Bank .                                       no_balance"""
		# trying to send w/ no balance works as expected
		lobby_page = self.nicol.lobby_page
		eHome = self.nicol.eHome_page
		send_to_bank = self.nicol.send_to_bank_page
		recip = 'Lourdes Ortega'

		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.set_role('employee')

		self.assertTrue(eHome.on())
		# menu should be closed on mobile
		if not main.is_desktop():
			self.assertFalse(eHome.menu.is_drawer_visible())
		eHome.send('bank')
		self.assertTrue(send_to_bank.on())
		self.assertEqual([0, 'Choose Account'], send_to_bank.currentStep)
		self.assertTrue(send_to_bank.click_account(recip, 'Wells Fargo Bank'))


		# Step 2 - Set amount, check for balance error
		self.assertEqual([1, 'Specify Amount'], send_to_bank.currentStep)
		usd_amount = self.nicol.generate_amount()
		self.assertFalse(send_to_bank.send_form.is_form_enabled())
		self.assertTrue(send_to_bank.send_form.has_balance_error())
		send_to_bank.send_form.set_usd(usd_amount)
		self.assertTrue(send_to_bank.send_form.has_balance_error())
		send_to_bank.send_form.try_clear_balance_error()
		self.assertFalse(send_to_bank.send_form.has_balance_error())

	def test_us_success(self):
		"""SendToBank: Bank .                          test_us_success"""
		# David needs Zions and Wells Fargo bank accounts
		#Send and Disclosure pages interact as expected
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		td_page = self.cheeks.td_page
		recip = 'David Castillo'

		# Login and select David Castillo
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on())
		self.assertTrue(send_to_bank.click_account(recip, 'Wells Fargo Bank'))
		send_to_bank.set_step('Choose Account')
		# send_to_bank.header.click_back()
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		self.assertTrue(send_to_bank.click_account(recip, 'Zions Bank'))

		# send page is setup as expected
		self.assertFalse(send_to_bank.send_form.is_form_enabled())
		self.assertEqual("0", send_to_bank.send_form.get_usd())
		balance = send_to_bank.send_form.get_balance()
		self.assertEqual(None, send_to_bank.send_form.exchange_rate)

		# send page amounts work as expected
		usd_amount = self.cheeks.generate_amount()
		send_to_bank.send_form.set_usd(usd_amount)
		self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())
		send_to_bank.send_form.click_continue()

		# disclosure page has everything we expect
		self.assertTrue(send_to_bank.on([2, 'Confirm & Send']))
		# check name and totals
		self.assertEqual(recip, send_to_bank.disclosure.get_name())

		self.assertEqual(usd_amount, send_to_bank.disclosure.get_transfer_amount())
		fee = '0.00'
		self.assertEqual(fee, send_to_bank.disclosure.get_transfer_fee())
		total = Decimal(usd_amount) + Decimal(fee)
		self.assertEqual(str(total), send_to_bank.disclosure.get_transfer_total())

		# check exchange rate and disclosures
		self.assertEqual(None, send_to_bank.disclosure.get_exchange_rate())

		self.assertFalse(send_to_bank.disclosure.has_d_30())
		self.assertFalse(send_to_bank.disclosure.has_d_less())
		self.assertTrue(send_to_bank.disclosure.has_d_notify())

		# send, clear confirmation dialog
		send_to_bank.disclosure.click_continue()
		self.assertTrue(eHome.on('activity'))
		eHome.clear_confirmation_dialog()
		self.assertTrue(eHome.on('activity'))

		# Check transaction
		data = eHome.get_transaction()
		self.assertEqual(data['amount'], '-' + usd_amount)
		self.assertEqual(data['recipient'], recip)
		self.assertEqual(data['icon'], 'clock')
		self.assertEqual(data['status'], 'Arriving')

		# check td page
		eHome.click_transaction()
		self.assertTrue(td_page.on())
		self.assertEqual('clock', td_page.read_transaction_icon())
		self.assertEqual(td_page.send_now_button, None)
		self.assertEqual(td_page.cancel_button, None)
		td_page.click_continue()

		self.assertTrue(eHome.on('activity'))