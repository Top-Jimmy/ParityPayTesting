import unittest
import time
from decimal import *
import profiles
import browser
import main
import messages

# TestBank - 9
	# test_add_account
	# test_add_mx_recipient
	# test_add_us_recipient
	# test_duplicate
	# test_navigation
	# test_no_balance
	# test_refund_mx
	# test_success_mx
	# test_success_us
	# test_upper_limit

class TestBank(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver, 'cheeks')
		self.nicol = profiles.Profile(self.driver, 'nicol')

	def tearDown(self):
		self.driver.quit()

	def test_add_account(self):
		""" test_send_to_bank.py:TestBank.test_add_account """
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
		""" test_send_to_bank.py:TestBank.test_add_mx_recipient """
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
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))

		# Delete recip_1		
		send_to_bank.header.click_back()
		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')
		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip_1)
		self.assertTrue(recip_card.on())
		recip_card.remove_recipient()
		self.assertTrue(recipient_list.on())

	def test_add_us_recipient(self):
		""" test_send_to_bank.py:TestBank.test_add_us_recipient """
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

		# Go to recipients and delete new recipient + any remaining from failed tests
		send_to_bank.header.click_back()
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		send_to_bank.header.click_back()
		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')
		self.assertTrue(recipient_list.on())
		# recipient_list.click_recipient(recip_1)
		# self.assertTrue(recip_card.on())
		# recip_card.remove_recipient()
		# self.assertTrue(recipient_list.on())

		# Delete non-Castillo/Ortega recipients
		while recipient_list.edit_recipients(['Sandy Cheeks', 'Castillo', 'Ortega']):
			self.assertTrue(recip_card.on())
			recip_card.remove_recipient()
			self.assertTrue(recipient_list.on())

	def test_duplicate(self):
		""" test_send_to_bank.py:TestBank.test_duplicate """
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
		""" test_send_to_bank.py:TestBank.test_navigation """
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
		""" test_send_to_bank.py:TestBank.test_no_balance """
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
		send_to_bank.send_form.try_clear_error()
		self.assertFalse(send_to_bank.send_form.has_balance_error())

	def test_refund_mx(self):
		""" test_send_to_bank.py:TestBank.test_refund_mx """
		# Send to Lourdes Ortega's MX bank account (bad clabe)
		# STP test server puts non '846' clabes in refund state
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		td_page = self.cheeks.td_page
		recip_card = self.cheeks.recipient_view_page
		recipient = 'Lourdes Ortega'
		bank_name = 'BBVA Bancomer'
		usd_amount = self.cheeks.generate_amount()
		fee = '1.00'
		total = str(Decimal(usd_amount) + Decimal(fee))

		# Login and select Lourdes Ortega
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on())
		self.assertTrue(send_to_bank.click_account(recipient, bank_name))
		send_to_bank.set_step('Choose Account')
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		self.assertTrue(send_to_bank.click_account(recipient, bank_name))

		# send page is setup as expected
		self.assertFalse(send_to_bank.send_form.is_form_enabled())
		self.assertEqual("0", send_to_bank.send_form.get_usd())
		balance = send_to_bank.send_form.get_balance()
		self.assertNotEqual(None, send_to_bank.send_form.exchange_rate)

		# send page: usd amount
		send_to_bank.send_form.set_usd(usd_amount)
		self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())
		send_to_bank.send_form.click_continue()

		# disclosure page: name, amount, fee, total, exchange rate, disclosures
		self.assertTrue(send_to_bank.on([2, 'Confirm & Send']))
		self.assertEqual(recipient, send_to_bank.disclosure.get_name())
		self.assertEqual(usd_amount, send_to_bank.disclosure.get_transfer_amount())
		self.assertEqual(fee, send_to_bank.disclosure.get_transfer_fee())
		self.assertEqual(total, send_to_bank.disclosure.get_transfer_total())
		self.assertNotEqual(None, send_to_bank.disclosure.get_exchange_rate())
		self.assertFalse(send_to_bank.disclosure.has_d_30())
		self.assertTrue(send_to_bank.disclosure.has_d_less())
		self.assertTrue(send_to_bank.disclosure.has_d_notify())

		# Send, confirmation dialog
		send_to_bank.disclosure.click_continue()
		self.assertTrue(eHome.on('activity'))
		self.assertTrue(eHome.clear_confirmation_dialog())
		self.assertTrue(eHome.on('activity'))

		# HistoryEntry: sending, clock
		data = eHome.get_transaction()
		self.assertEqual(data['amount'], '-' + total)
		self.assertEqual(data['recipient'], recipient)
		self.assertEqual(data['icon'], 'clock')
		self.assertEqual(data['status'], 'Sending')

		# TransferDetails: sending, clock, actions.
		eHome.click_transaction()
		self.assertTrue(td_page.on())
		self.assertEqual('clock', td_page.read_transaction_icon())
		self.assertEqual(td_page.send_now_button, None)
		self.assertEqual(td_page.cancel_button, None)
		self.assertEqual(td_page.delay_disclosure, None)

		# Should go into 'delayed' state soon (wait ~5 seconds)
		time.sleep(4)
		self.driver.refresh() # Works on native app?
		self.assertTrue(td_page.on())
		self.assertEqual('clock', td_page.read_transaction_icon())
		self.assertEqual(td_page.send_now_button, None)
		self.assertEqual(td_page.cancel_button, None)
		raw_input('disclosure?')
		self.assertNotEqual(td_page.delay_disclosure, None)

		# Recipient link
		td_page.click_recip_link()
		self.assertTrue(recip_card.on())
		recip_card.header.click_back()
		self.assertTrue(td_page.on())

		# TransferDetails: Cancel/Refund transfer:
		td_page.refund_transaction('cancel')
		self.assertTrue(td_page.on())
		self.assertEqual('clock', td_page.read_transaction_icon())
		self.assertEqual(td_page.send_now_button, None)
		self.assertEqual(td_page.cancel_button, None)
		self.assertNotEqual(td_page.delay_disclosure, None)

		td_page.refund_transaction()
		self.assertTrue(td_page.on())
		self.assertEqual('x', td_page.read_transaction_icon())
		self.assertEqual(td_page.send_now_button, None)
		self.assertEqual(td_page.cancel_button, None)
		self.assertEqual(td_page.delay_disclosure, None)
		self.assertEqual(td_page.cancel_button, None)
		td_page.click_continue()

		# HistoryEntry: Canceled
		# (Will be on send tab instead of activity because of refresh)
		self.assertTrue(eHome.on('send'))
		eHome.setTab('activity')
		self.assertTrue(eHome.on('activity'))
		data = eHome.get_transaction()
		self.assertEqual(data['amount'], '-' + total)
		self.assertEqual(data['recipient'], recipient)
		self.assertEqual(data['icon'], 'x')
		self.assertEqual(data['status'], 'Canceled')

	def test_success_mx(self):
		""" test_send_to_bank.py:TestBank.test_success_mx """
		# Send to Lourdes Ortega's MX bank account
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		td_page = self.cheeks.td_page
		recip_card = self.cheeks.recipient_view_page
		recip = 'Lourdes Ortega'
		bank_name = 'Sistema de Transferencias y Pagos STP'
		usd_amount = self.cheeks.generate_amount()
		fee = '1.00'

		# Login and select Lourdes Ortega
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on())
		self.assertTrue(send_to_bank.click_account(recip, 'BBVA Bancomer'))
		send_to_bank.set_step('Choose Account')
		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
		self.assertTrue(send_to_bank.click_account(recip, 'BBVA Bancomer'))

		# send page is setup as expected
		self.assertFalse(send_to_bank.send_form.is_form_enabled())
		self.assertEqual("0", send_to_bank.send_form.get_usd())
		balance = send_to_bank.send_form.get_balance()
		self.assertNotEqual(None, send_to_bank.send_form.exchange_rate)

		# send page amounts work as expected
		send_to_bank.send_form.set_usd(usd_amount)
		self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())
		send_to_bank.send_form.click_continue()

		# disclosure page: name, amount, fee, totals, exchange rate, disclosures
		self.assertTrue(send_to_bank.on([2, 'Confirm & Send']))
		self.assertEqual(recip, send_to_bank.disclosure.get_name())
		self.assertEqual(usd_amount, send_to_bank.disclosure.get_transfer_amount())
		self.assertEqual(fee, send_to_bank.disclosure.get_transfer_fee())
		total = str(Decimal(usd_amount) + Decimal(fee))
		self.assertEqual(total, send_to_bank.disclosure.get_transfer_total())
		self.assertNotEqual(None, send_to_bank.disclosure.get_exchange_rate())
		self.assertFalse(send_to_bank.disclosure.has_d_30())
		self.assertTrue(send_to_bank.disclosure.has_d_less())
		self.assertTrue(send_to_bank.disclosure.has_d_notify())

		# send, clear confirmation dialog
		send_to_bank.disclosure.click_continue()
		self.assertTrue(eHome.on('activity'))
		self.assertTrue(eHome.clear_confirmation_dialog())
		self.assertTrue(eHome.on('activity'))

		# HistoryEntry: Sending, clock
		data = eHome.get_transaction()
		self.assertEqual(data['amount'], '-' + total)
		self.assertEqual(data['recipient'], recip)
		self.assertEqual(data['icon'], 'clock')
		self.assertEqual(data['status'], 'Sending')

		# TransferDetails: Clock, actions, recipient link, delay disclosure
		eHome.click_transaction()
		self.assertTrue(td_page.on())
		self.assertEqual('clock', td_page.read_transaction_icon())
		self.assertEqual(td_page.send_now_button, None)
		self.assertEqual(td_page.cancel_button, None)
		self.assertEqual(td_page.delay_disclosure, None)
		td_page.click_recip_link()
		self.assertTrue(recip_card.on())
		recip_card.header.click_back()
		self.assertTrue(td_page.on())
		td_page.click_continue()

		self.assertTrue(eHome.on('activity'))

	def test_success_us(self):
		""" test_send_to_bank.py:TestBank.test_success_us """
		# Send to David Castillo's US bank account
		eHome = self.cheeks.eHome_page
		send_to_bank = self.cheeks.send_to_bank_page
		td_page = self.cheeks.td_page
		recip = 'David Castillo'

		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('bank')
		self.assertTrue(send_to_bank.on())
		self.assertTrue(send_to_bank.click_account(recip, 'Wells Fargo Bank'))
		send_to_bank.set_step('Choose Account')
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
		self.assertTrue(eHome.clear_confirmation_dialog())
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


	# def test_upper_limit(self):
	# 	""" test_send_to_bank.py:TestBank.test_upper_limit """
	# 	# Send >$1000 to David Castillo's US bank account.
	# 	self.juan = profiles.Profile(self.driver, 'juan')
	# 	eHome = self.juan.eHome_page
	# 	send_to_bank = self.juan.send_to_bank_page
	# 	td_page = self.juan.td_page
	# 	recip = 'Juan This One at Sendmi Rodriguz'
	# 	usd_amount = '1000.00'

	# 	self.assertTrue(self.juan.login(self.driver), messages.login)
	# 	eHome.send('bank')
	# 	self.assertTrue(send_to_bank.on())
	# 	self.assertTrue(send_to_bank.click_account('', 'J.P. Morgan Chase'))

	# 	# send page is setup as expected
	# 	self.assertFalse(send_to_bank.send_form.is_form_enabled())
	# 	self.assertEqual("0", send_to_bank.send_form.get_usd())
	# 	balance = send_to_bank.send_form.get_balance()
	# 	self.assertEqual(None, send_to_bank.send_form.exchange_rate)

	# 	# send page amounts work as expected
	# 	send_to_bank.send_form.set_usd(usd_amount)
	# 	self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())
	# 	send_to_bank.send_form.click_continue()

	# 	# disclosure page has everything we expect
	# 	self.assertTrue(send_to_bank.on([2, 'Confirm & Send']))
	# 	# check name and totals
	# 	self.assertEqual(recip, send_to_bank.disclosure.get_name())

	# 	self.assertEqual(usd_amount, send_to_bank.disclosure.get_transfer_amount())
	# 	fee = '0.00'
	# 	self.assertEqual(fee, send_to_bank.disclosure.get_transfer_fee())
	# 	total = Decimal(usd_amount) + Decimal(fee)
	# 	self.assertEqual(str(total), send_to_bank.disclosure.get_transfer_total())

	# 	# check exchange rate and disclosures
	# 	self.assertEqual(None, send_to_bank.disclosure.get_exchange_rate())

	# 	self.assertFalse(send_to_bank.disclosure.has_d_30())
	# 	self.assertFalse(send_to_bank.disclosure.has_d_less())
	# 	self.assertTrue(send_to_bank.disclosure.has_d_notify())

	# 	# try to send, verify error
	# 	send_to_bank.disclosure.click_continue()
	# 	time.sleep(2)
	# 	self.assertTrue(send_to_bank.disclosure.has_upper_limit_error())
	# 	send_to_bank.disclosure.try_clear_error()
	# 	self.assertFalse(send_to_bank.disclosure.has_upper_limit_error())



# Functionality

# 1. Choose Account (US or MX)
	# Add Account (US or MX)
		# Add Recipient (US or MX)

# 2. Set amount

# 3. Confirm

# Confirmation popup

# HistoryEntry

# TransferDetails




# Check
# General
	# back button

# 1. Choose Account

# 2.

# 3
# amount, fee, total
# disclosures



# Document
# Difference between US/MX based recipients
	# Default bank type?

# Difference between sending to US/MX bank vs ATM

# Differences between test/prod
	# Test: STP: Non-STP clabes get rejected (error 1?)
	# Test: ACH/STP:  transfers get returned from Jeff's account?








