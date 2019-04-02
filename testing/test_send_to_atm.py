import unittest
import time
from decimal import *
import profiles
import browser
import main
import messages

# TestATM - 6
	# test_add_recipient
	# test_duplicate
	# test_edit_pin (skipped)
	# test_learn_more
	# test_navigation
	# test_no_balance
	# test_success

class TestATM(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(), main.get_browser())
		self.cheeks = profiles.Profile(self.driver, 'cheeks')
		self.nicol = profiles.Profile(self.driver, 'nicol')

	def tearDown(self):
		self.driver.quit()

	def test_add_recipient(self):
		""" test_send_to_atm.py:TestATM.test_add_recipient """
		eHome = self.cheeks.eHome_page
		send_to_atm = self.cheeks.send_to_atm_page
		recipient_list = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		recip_card = self.cheeks.recipient_view_page

		# Add new recipient. Click back to recipient list. Add account for recipient.
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('atm')
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.add_recipient()
		self.assertTrue(name_page.on())
		self.assertEqual('Mexico', name_page.get_location())
		name_page.set_location('us')
		self.assertEqual('United States', name_page.get_location())
		name_page.set_location('mx')
		self.assertEqual('Mexico', name_page.get_location())
		recip = self.cheeks.generate_name()
		name_page.enter_name(recip)

		# Should be on additional data form
		self.assertTrue(send_to_atm.on([0, 'Recipient'], True))
		noCarrier = {
			'carrier': '',
			'phone': '2022221234',
			'dob': self.cheeks.generate_rfc_dob()
		}
		noDOB = {
			'carrier': 'telcel',
			'phone': '2022221234',
			'dob': ''
		}
		noPhone = {
			'carrier': 'at&t',
			'phone': '',
			'dob': self.cheeks.generate_rfc_dob()
		}
		allInfo = {
			'carrier': 'movistar',
			'phone': '(202) 222-1234',
			'dob': self.cheeks.generate_rfc_dob()
		}
		# Shouldn't be able to submit form w/out all info
		# Should get 'Required' error (not currently getting one for phone, no identifier on carrier)
		send_to_atm.data_form.set_info(noCarrier) # Do noCarrier first (cannot de-select carrier)
		send_to_atm.submit_data_form(False)
		# raw_input('noCarrier')
		self.assertTrue(send_to_atm.on([0, 'Recipient'], True))
		# self.assertTrue('Date Format: mm/dd/yyyy' in send_to_atm.data_form.dob_error())
		send_to_atm.data_form.set_info(noPhone)
		send_to_atm.submit_data_form(False)
		# raw_input('noPHone')
		self.assertTrue(send_to_atm.on([0, 'Recipient'], True))
		send_to_atm.data_form.set_info(noDOB)
		# raw_input('noDob')
		send_to_atm.submit_data_form(False)
		self.assertTrue('Required' in send_to_atm.data_form.dob_error())

		send_to_atm.data_form.set_info(allInfo)
		returned_info = send_to_atm.data_form.get_info()
		self.assertEqual(allInfo['carrier'], returned_info['carrier'])
		self.assertEqual(allInfo['phone'], returned_info['phone'])
		self.assertEqual(allInfo['dob'], returned_info['dob'])
		send_to_atm.submit_data_form()

		send_to_atm.set_step(0)
		send_to_atm.click_recipient(recip)
		self.assertTrue(send_to_atm.on([1, 'Amount']))
		if not main.is_desktop():
			send_to_atm.header.click_back()
			self.assertTrue(send_to_atm.on([0, 'Recipient']))
			send_to_atm.header.click_back()
			self.assertTrue(eHome.on())
			eHome.menu.click_option('recipients')
		else:
			send_to_atm.menu.click_option('recipients')

		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip)
		self.assertTrue(recip_card.on())
		recip_card.remove_recipient()
		self.assertTrue(recipient_list.on())

	def test_duplicate(self):
		""" test_send_to_atm.py:TestATM.test_duplicate """
		eHome = self.cheeks.eHome_page
		send_to_atm = self.cheeks.send_to_atm_page
		recipient_list = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		recip_card = self.cheeks.recipient_view_page

		# Trying to send to Jose should go back to send-to-atm and load 2nd step
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('atm')
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.add_recipient()
		self.assertTrue(name_page.on())
		recip1 = "Jose Ortega"
		name_page.enter_name(recip1)
		self.assertTrue(name_page.on(True))

		self.assertIsNotNone(name_page.duplicate_send)
		self.assertIsNotNone(name_page.duplicate_continue)
		self.assertIsNone(name_page.duplicate_add)
		self.assertIsNone(name_page.duplicate_view)

		name_page.click_duplicate_send()
		self.assertTrue(send_to_atm.on([1, 'Amount']))
		send_to_atm.set_step(0)

		# Trying to send to David should go back to send-to-atm w/ addInfo loaded
		send_to_atm.add_recipient()
		self.assertTrue(name_page.on())
		recip2 = "David Castillo"
		name_page.enter_name(recip2)
		self.assertTrue(name_page.on(True))
		name_page.click_duplicate_send()
		self.assertTrue(send_to_atm.on([0, 'Recipient'], True))

		# Adding duplicate of Rosa should go back to 1st step
		# Delete new recipient
		send_to_atm.header.click_back()
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.add_recipient()
		self.assertTrue(name_page.on())
		recip3 = "Rosa Castillo"
		name_page.enter_name(recip3)
		self.assertTrue(name_page.on(True))
		name_page.click_duplicate_continue()

		self.assertTrue(send_to_atm.on([0, 'Recipient'], True))
		if main.is_desktop():
			send_to_atm.menu.click_option('recipients')
		else:
			send_to_atm.header.click_back()
			self.assertTrue(send_to_atm.on([0, 'Recipient'], False))
			send_to_atm.header.click_back()
			self.assertTrue(eHome.on())
			eHome.menu.click_option('recipients')
		self.assertTrue(recipient_list.on())
		recipient_list.click_recipient(recip3)
		self.assertTrue(recip_card.on())

		recip_card.remove_recipient()
		self.assertTrue(recipient_list.on())

	# @unittest.skip("PIN no longer user generated")
	# def test_edit_pin(self):
	#   """ test_send_to_atm.py:TestATM.test_edit_pin """
	# 	# Send 100 MXN to Leticia (atm) with pin1. Send 100 to Leticia w/ pin2.
	# 	# Transfer details page should associate correct pin w/ correct transfer
	# 	eHome = self.cheeks.eHome_page
	# 	recip_list = self.cheeks.recipient_page
	# 	recip_view = self.cheeks.recipient_view_page
	# 	info_page = self.cheeks.recipient_info_page
	# 	send_to_atm = self.cheeks.send_to_atm_page
	# 	td_page = self.cheeks.td_page
	# 	recip = "Leticia Ortega"

	# 	# Read pin #1
	# 	self.assertTrue(self.cheeks.login(self.driver), messages.login)
	# 	eHome.menu.click_option('recipients')
	# 	self.assertTrue(recip_list.on())
	# 	recip_list.click_recipient(recip)
	# 	self.assertTrue(recip_view.on())
	# 	recip_view.edit_additional_info()
	# 	self.assertTrue(info_page.on())
	# 	info = info_page.addInfo.get_info()
	# 	pin1 = info['pin']

	# 	if main.is_desktop():
	# 		info_page.menu.click_option('ehome')
	# 	else:
	# 		info_page.header.click_back()
	# 		self.assertTrue(recip_view.on())
	# 		recip_view.header.click_back()
	# 		self.assertTrue(recip_list.on())
	# 		recip_list.menu.click_option('ehome')
	# 	self.assertTrue(eHome.on())
	# 	eHome.send('atm')

	# 	self.assertTrue(send_to_atm.on())
	# 	send_to_atm.click_recipient(recip)
	# 	self.assertTrue(send_to_atm.on([1, 'Amount']))
	# 	send_to_atm.send_form.set_bbva_amount('100')
	# 	send_to_atm.submit_send_form()

	# 	send_to_atm.disclosure.click_continue()
	# 	self.assertTrue(eHome.on('activity'))
	# 	self.assertEqual(pin1, eHome.get_dialog_pin())
	# 	eHome.clear_confirmation_dialog()
	# 	self.assertTrue(eHome.on('activity'))
	# 	eHome.click_transaction()
	# 	self.assertTrue(td_page.on(True))
	# 	self.assertEqual(pin1, td_page.get_pin())
	# 	td_page.header.click_back()
	# 	self.assertTrue(eHome.on('activity'))

	# 	# Change pin
	# 	eHome.menu.click_option('recipients')
	# 	self.assertTrue(recip_list.on())
	# 	recip_list.click_recipient(recip)
	# 	self.assertTrue(recip_view.on())
	# 	recip_view.edit_additional_info()
	# 	self.assertTrue(info_page.on())
	# 	pin2 = pin1
	# 	while pin1 == pin2:
	# 		pin2 = self.cheeks.generate_number(4)
	# 	info_page.addInfo.set_pin(pin2)
	# 	info_page.addInfo.click_continue()
	# 	self.assertTrue(recip_view.on())

	# 	if main.is_desktop():
	# 		recip_view.menu.click_option('ehome')
	# 	else:
	# 		recip_view.header.click_back()
	# 		self.assertTrue(recip_list.on())
	# 		recip_list.menu.click_option('ehome')
	# 	self.assertTrue(eHome.on('activity'))
	# 	eHome.send('atm')

	# 	# Send again. Verify pin2 is in transfer details
	# 	self.assertTrue(send_to_atm.on())
	# 	send_to_atm.click_recipient(recip)
	# 	self.assertTrue(send_to_atm.on([1, 'Amount']))
	# 	send_to_atm.send_form.set_bbva_amount('100')
	# 	send_to_atm.submit_send_form()

	# 	send_to_atm.disclosure.click_continue()
	# 	self.assertTrue(eHome.on('activity'))
	# 	eHome.clear_confirmation_dialog()
	# 	self.assertTrue(eHome.on('activity'))
	# 	eHome.click_transaction()
	# 	self.assertTrue(td_page.on(True))
	# 	self.assertEqual(pin2, td_page.get_pin())
	# 	td_page.header.click_back()
	# 	self.assertTrue(eHome.on('activity'))

	# 	# Verify transaction1 still has original pin
	# 	eHome.click_transaction(1)
	# 	self.assertTrue(td_page.on(True))
	# 	self.assertEqual(pin1, td_page.get_pin())

	def test_learn_more(self):
		""" test_send_to_atm.py:TestATM.test_learn_more """
		eHome = self.cheeks.eHome_page
		send_to_atm = self.cheeks.send_to_atm_page
		recipient_list = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		recip_card = self.cheeks.recipient_view_page

		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		# Action 0: How to send to ATM
		eHome.learn_more_action(0)
		eHome.how_to_close.click()
		time.sleep(1)
		eHome.learn_more_action(0)
		# Step 1
		self.assertTrue(eHome.how_to_close != None)
		self.assertTrue(eHome.how_to_next != None)
		self.assertTrue(eHome.how_to_done == None)
		eHome.click_how_to_next()
		# Step 2
		self.assertTrue(eHome.how_to_close != None)
		self.assertTrue(eHome.how_to_next != None)
		self.assertTrue(eHome.how_to_done == None)
		eHome.click_how_to_next()
		# Step 3
		self.assertTrue(eHome.how_to_close != None)
		self.assertTrue(eHome.how_to_next != None)
		self.assertTrue(eHome.how_to_done == None)
		eHome.click_how_to_next()
		# Step 4
		self.assertTrue(eHome.how_to_close == None)
		self.assertTrue(eHome.how_to_next == None)
		self.assertTrue(eHome.how_to_done != None)
		eHome.how_to_done.click()
		time.sleep(1)

		# Action 1: Find BBVA
		eHome.learn_more_action(1)
		eHome.find_atm('Monterrey')
		eHome.close_find_atm()
		time.sleep(3)

		# Action 2: FAQ
		# eHome.learn_more_action(2)
		# eHome.close_find_atm()
		# self.assertTrue(eHome.on('send'))

	def test_navigation(self):
		""" test_send_to_atm.py:TestATM.test_navigation """
		# Check back button and steps for all pages in send flow
		eHome = self.cheeks.eHome_page
		send_to_atm = self.cheeks.send_to_atm_page
		name_page = self.cheeks.recipient_name_page
		recip1 = 'David Castillo'
		recip2 = 'Jose Ortega'

		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('atm')
		self.assertTrue(send_to_atm.on())
		# Step 0 goes back to eHome
		send_to_atm.header.click_back()
		self.assertTrue(eHome.on('send'))
		eHome.send('atm')
		self.assertTrue(send_to_atm.on())
		# Cannot skip ahead to steps 1 or 2
		send_to_atm.set_step(1, reloadPage=False)
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.set_step(2, reloadPage=False)
		self.assertTrue(send_to_atm.on([0, 'Recipient']))

		# Clicking back on addInfo screen will go to step 0
		send_to_atm.click_recipient(recip1)
		self.assertTrue(send_to_atm.on([0, 'Recipient'], True))
		send_to_atm.header.click_back()
		self.assertTrue(send_to_atm.on([0, 'Recipient']))

		# Clicking back on amount step goes to step 0
		send_to_atm.click_recipient(recip2)
		self.assertTrue(send_to_atm.on([1, 'Amount']))
		send_to_atm.header.click_back()
		self.assertTrue(send_to_atm.on([0, 'Recipient']))

		# Can jump between 1st 2 steps after selecting recipient w/ info
		send_to_atm.click_recipient(recip2)
		self.assertTrue(send_to_atm.on([1, 'Amount']))
		send_to_atm.set_step(1)
		send_to_atm.set_step(1)
		# Can't jump to last step
		send_to_atm.set_step(2, reloadPage=False)
		self.assertTrue(send_to_atm.on([1, 'Amount']))

		# Can jump between all 3 steps after setting amount and clicking continue
		atm_amount = "100"
		send_to_atm.send_form.set_bbva_amount(atm_amount)
		send_to_atm.submit_send_form()
		send_to_atm.set_step(0)
		send_to_atm.set_step(1)
		self.assertEqual(atm_amount, send_to_atm.send_form.get_bbva_amount())
		send_to_atm.set_step(2)

		# Clicking back to beginning.
		# Clicking back on add recipient goes to 1st step
		send_to_atm.header.click_back()
		self.assertTrue(send_to_atm.on([1, 'Amount']))
		send_to_atm.header.click_back()
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.add_recipient()
		self.assertTrue(name_page.on())
		name_page.header.click_back()
		self.assertTrue(send_to_atm.on([0, 'Recipient']))

	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
	def test_no_balance(self):
		""" test_send_to_atm.py:TestATM.test_no_balance """
		# trying to send w/ no balance works as expected
		lobby_page = self.nicol.lobby_page
		eHome = self.nicol.eHome_page
		send_to_atm = self.nicol.send_to_atm_page
		recip = 'David Castillo'

		self.assertTrue(self.nicol.login(self.driver), messages.login)
		self.assertTrue(lobby_page.on())
		lobby_page.menu.set_role('employee')

		self.assertTrue(eHome.on())
		# menu should be closed on mobile
		if not main.is_desktop():
			self.assertFalse(eHome.menu.is_drawer_visible())
		eHome.send('atm')
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.click_recipient(recip)
		self.assertTrue(send_to_atm.on([1, 'Amount']))

		# Step 2 - Set amount, check for balance error
		self.assertEqual([1, 'Amount'], send_to_atm.currentStep)
		mxn_amount = self.nicol.generate_bbva_amount()
		print(mxn_amount)
		self.assertFalse(send_to_atm.send_form.is_form_enabled())
		self.assertTrue(send_to_atm.send_form.has_balance_error())
		send_to_atm.send_form.set_bbva_amount(mxn_amount)
		self.assertTrue(send_to_atm.send_form.has_balance_error())
		send_to_atm.send_form.try_clear_error()
		self.assertFalse(send_to_atm.send_form.has_balance_error())
		self.assertFalse(send_to_atm.send_form.is_form_enabled())

	def test_success(self):
		""" test_send_to_atm.py:TestATM.test_success """
		# David needs Zions and Wells Fargo bank accounts
		#Send and Disclosure pages interact as expected
		eHome = self.cheeks.eHome_page
		send_to_atm = self.cheeks.send_to_atm_page
		td_page = self.cheeks.td_page
		recip = 'Jose Ortega'

		# Login and select David Castillo
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		eHome.send('atm')
		self.assertTrue(send_to_atm.on())
		send_to_atm.click_recipient(recip)
		send_to_atm.set_step('Recipient')
		self.assertTrue(send_to_atm.on([0, 'Recipient']))
		send_to_atm.click_recipient(recip)
		self.assertTrue(send_to_atm.on([1, 'Amount']))

		# send page is setup as expected
		self.assertFalse(send_to_atm.send_form.is_form_enabled())
		self.assertEqual("0", send_to_atm.send_form.get_bbva_amount())
		balance = send_to_atm.send_form.get_balance()
		exchange_rate = send_to_atm.send_form.get_exchange_rate()
		self.assertNotEqual(None, exchange_rate)

		# send page amounts work as expected
		mxn = self.cheeks.generate_bbva_amount()
		send_to_atm.send_form.set_bbva_amount(mxn)
		usd = send_to_atm.send_form.get_usd()
		self.assertEqual(mxn, send_to_atm.send_form.get_bbva_amount())
		send_to_atm.submit_send_form()

		# disclosure page has everything we expect
		# check name and totals
		self.assertEqual(recip, send_to_atm.disclosure.get_name())

		# self.assertEqual(usd_amount, send_to_atm.disclosure.get_transfer_amount())
		fee = '1.00'
		self.assertEqual(fee, send_to_atm.disclosure.get_transfer_fee())
		self.assertEqual(mxn + " MXN", send_to_atm.disclosure.get_total_to_recipient())
		total = str(Decimal(usd) + Decimal(fee))
		self.assertEqual(total, send_to_atm.disclosure.get_transfer_total())

		# check exchange rate and disclosures
		self.assertEqual(exchange_rate, send_to_atm.disclosure.get_exchange_rate())

		self.assertFalse(send_to_atm.disclosure.has_d_30())
		self.assertFalse(send_to_atm.disclosure.has_d_less())
		self.assertTrue(send_to_atm.disclosure.has_d_notify())

		# send, clear confirmation dialog
		send_to_atm.disclosure.click_continue()
		self.assertTrue(eHome.on('activity'))
		self.assertTrue(eHome.clear_confirmation_dialog())
		self.assertTrue(eHome.on('activity'))

		# Check transaction
		data = eHome.get_transaction()
		self.assertEqual(data['amount'], '-' + total)
		# self.assertEqual(data['recipient'], recip)
		self.assertEqual(data['icon'], 'clock')
		self.assertEqual(data['status'], 'Sending') # Available

		# check td page
		eHome.click_transaction()
		self.assertTrue(td_page.on(True))
		self.assertEqual('clock', td_page.read_transaction_icon())
		self.assertEqual(td_page.send_now_button, None)
		self.assertEqual(td_page.cancel_button, None)
		td_page.click_continue()

		self.assertTrue(eHome.on('activity'))