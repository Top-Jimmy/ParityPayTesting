import unittest
from decimal import *
import profiles
import browser
import main
import messages
import time
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# todo: test editing recipients country and verifying navigation, etc.

	# Total: 19
	# TestDuplicates - 5        Adding duplicate recipient functionality
		# test_duplicate_add
		# test_duplicate_continue
		# test_duplicate_send
		# test_duplicate_send_no_account
		# test_duplicate_send_no_address
	# TestEdit - 7              Edit name/address/accounts
		# test_add_account_redirect
		# test_delete_account
		# test_edit_account
		# test_edit_additional_info
		# test_edit_address
		# test_edit_cashout (not implemented)
		# test_edit_name
		# test_try_access_address
	# TestRecipients - 7        Add/Edit/Delete Recipients
		# *test_add_new_mx_bbva
		# test_add_new_mx_cash
		# test_add_new_mx_mx
		# *test_add_new_mx_us
		# test_add_new_us_cash
		# test_add_new_us_mx
		# *test_add_new_us_us


# @unittest.skipIf(main.get_priority() < 3, 'Priority')
@unittest.skip("Busted functionality")
class TestDuplicates(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver,'cheeks')

	def tearDown(self):
		self.driver.quit()

	def test_duplicate_add(self):
		""" test_recipients.py:TestDuplicates.test_duplicate_add """
		#dependencies: Recipient Rosa Castillo has an account
		eHome = self.cheeks.eHome_page
		recip_select_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		ba_page = self.cheeks.bank_account_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')
		self.assertTrue(recip_select_page.on())
		recip_select_page.click_add()

		self.assertTrue(name_page.on())
		name_page.set_location("Mexico")
		recip_name = ["Rosa", "Castillo", ""]
		name_page.enter_name(recip_name)
		name_page.try_load_duplicates()
		name_page.click_duplicate_add()

		self.assertTrue(recip_select_page.on())
		# self.assertTrue(ba_page.on())

	def test_duplicate_continue(self):
		""" test_recipients.py:TestDuplicates.test_duplicate_continue """
		#dependencies: Recipient Yolanda Castillo exists already.
		eHome = self.cheeks.eHome_page
		recip_select_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		# address_page = self.cheeks.recipient_address_page
		ba_page = self.cheeks.bank_account_page
		send_page = self.cheeks.send_page
		view_page = self.cheeks.recipient_view_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		 # Add duplicate recipient
		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')
		self.assertTrue(recip_select_page.on())
		recip_select_page.click_add()

		self.assertTrue(name_page.on())
		name_page.set_location("Mexico")
		recip_name = ["Yolanda", "Castillo",""]
		name_page.enter_name(recip_name)
		name_page.try_load_duplicates()

		name_page.click_duplicate_continue()

		# No address form anymore
		self.assertTrue(ba_page.on())

		# self.assertTrue(address_page.on())

		# # ios is a pain. Only set states visible when state dd opens
		# address = [
		# 	"101 Main Street",
		# 	"Col. Atlatilco",
		# 	"Mexico City",
		# 	"Puebla", # Ciudad de Mexico
		# 	"02383"
		# ]
		# address_page.set_address(address)

		# self.assertTrue(ba_page.on())
		ba_page.set_destination_type('bank')
		ba_page.set_location("United States")

		routing_num = "124000054"
		acct_num = self.cheeks.generate_number(17)
		ba_page.set_routing(routing_num)
		self.assertEqual(ba_page.get_routing(), routing_num)
		ba_page.set_account(acct_num)
		self.assertEqual(ba_page.get_account(), acct_num)
		ba_page.set_account_type('savings')
		ba_page.click_continue()

		self.assertTrue(send_page.on())
		send_page.header.click_back()

		# remove a Yolanda and make sure remaining Yolanda has no bank accounts
		self.assertTrue(recip_select_page.on())
		recip_select_page.click_recipient('Yolanda Castillo', 'edit')

		self.assertTrue(view_page.on())
		view_page.remove_recipient()

		self.assertTrue(recip_select_page.on())
		recip_select_page.click_recipient('Yolanda Castillo', 'edit')
		self.assertTrue(view_page.on())
		view_page.sel_tab('destinations')

		for i in xrange(view_page.num_accounts()):
			view_page.select_destination('bank', 0)
			self.assertTrue(ba_page.on())
			ba_page.remove()
			self.assertTrue(view_page.on())

	def test_duplicate_send(self):
		""" test_recipients.py:TestDuplicates.test_duplicate_send """
		eHome = self.cheeks.eHome_page
		recip_select_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		send_page = self.cheeks.send_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		# Add duplicate recipient
		self.assertTrue(eHome.on())
		eHome.send_money()

		self.assertTrue(recip_select_page.on())
		recip_select_page.click_add()

		# Recip has all info. Duplicate send should redirect to send page
		self.assertTrue(name_page.on())
		name_page.set_location("Mexico")
		recip_name = ["Jose", "Ortega",""]
		name_page.enter_name(recip_name)
		name_page.try_load_duplicates()
		name_page.click_duplicate_send()

		self.assertTrue(send_page.on())

	def test_duplicate_send_no_account(self):
		""" test_recipients.py:TestDuplicates.test_duplicate_send_no_account """
		# dependencies: Yolanda Castillo has address, but no bank accounts
		eHome = self.cheeks.eHome_page
		recip_select_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		ba_page = self.cheeks.bank_account_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		# Add duplicate recipient
		self.assertTrue(eHome.on())
		eHome.send_money()

		self.assertTrue(recip_select_page.on())
		recip_select_page.click_add()

		self.assertTrue(name_page.on())
		name_page.set_location("United States")
		recip_name = ["Yolanda", "Castillo",""]
		name_page.enter_name(recip_name)
		name_page.try_load_duplicates()
		# should land on bank account page
		name_page.click_duplicate_send()
		# this will fail if Yolanda has a bank account
		self.assertTrue(ba_page.on())

	#
	def test_duplicate_send_no_address(self):
		""" test_recipients.py:TestDuplicates.test_duplicate_send_no_address """
		# Reset Yolanda's account if this is failing.
		# Make sure there's only 1 recipient named Yolanda.
		# Should have 0 bank accounts
		eHome = self.cheeks.eHome_page
		recip_select_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		# address_page = self.cheeks.recipient_address_page
		send_page = self.cheeks.send_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		# Add duplicate recipient
		self.assertTrue(eHome.on())
		eHome.send_money()

		self.assertTrue(recip_select_page.on())
		recip_select_page.click_add()

		# Rosa has no address, duplicate send should redirect to address page
		self.assertTrue(name_page.on())
		name_page.set_location("Mexico")
		recip_name = ["Rosa", "Castillo",""]
		name_page.enter_name(recip_name)
		name_page.try_load_duplicates()
		name_page.click_duplicate_send()

		# should go to send form instead of address page
		# self.assertTrue(address_page.on())
		self.assertTrue(send_page.on())

		# todo: need 2 no account tests.
		# 1: recip has address, but no account
		# 2: recip has no address and no account
		# 3: us account??

@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
class TestEdit(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver,'cheeks')

	def tearDown(self):
		self.driver.quit()

	# @unittest.skip("Deprecated. Adding from 'send flows' added to bank and atm tests")
	# def test_add_account_redirect(self):
	# 	"""recipients : Edit .                          add_account_redirect"""
	# 	# Adding account from 'send flow' should redirect to send page

	# 	# Yolanda should end test w/ no bank accounts
	# 	eHome = self.cheeks.eHome_page
	# 	recip_page = self.cheeks.recipient_page
	# 	view_page = self.cheeks.recipient_view_page
	# 	ba_page = self.cheeks.bank_account_page
	# 	send_page = self.cheeks.send_page
	# 	sel_page = self.cheeks.bank_account_select_page
	# 	self.assertTrue(self.cheeks.login(self.driver), messages.login)

	# 	self.assertTrue(eHome.on())
	# 	eHome.send_money()

	# 	self.assertTrue(recip_page.on())
	# 	recip_page.click_recipient("Yolanda Castillo", 'edit')

	# 	# edit employee. Should be on default tab (info)
	# 	self.assertTrue(view_page.on())
	# 	self.assertEqual('info', view_page.current_tab())
	# 	view_page.sel_tab('destinations')
	# 	view_page.add_destination()

	# 	self.assertTrue(ba_page.on())
	# 	ba_page.set_destination_type('bank')
	# 	ba_page.set_location('us')
	# 	zions_routing = "124000054"
	# 	acct_number = "123456780001"
	# 	ba_page.set_account_type('savings')
	# 	ba_page.set_routing(zions_routing)
	# 	ba_page.set_account(acct_number)
	# 	ba_page.click_continue()

	# 	# Should be in 'send flow' and redirect to send page
	# 	self.assertTrue(send_page.on())
	# 	send_page.header.click_back()

	# 	self.assertTrue(recip_page.on())
	# 	recip_page.click_recipient("Yolanda Castillo", 'edit')
	# 	# remove Yolanda's bank accounts
	# 	self.assertTrue(view_page.on())
	# 	for i in xrange(view_page.num_accounts()):
	# 		view_page.select_destination('bank', 0)
	# 		self.assertTrue(ba_page.on())
	# 		ba_page.remove()
	# 		self.assertTrue(view_page.on())

	# 	self.assertTrue(view_page.on())
	# 	self.assertEqual(view_page.num_accounts(), 0)

	def test_delete_account(self):
		""" test_recipients.py:TestEdit.test_delete_account """
		# Adding account from 'recipient' page should redirect to view page
		# Yolanda should end test w/ no bank accounts
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		view_page = self.cheeks.recipient_view_page
		ba_page = self.cheeks.bank_account_page
		send_page = self.cheeks.send_page
		sel_page = self.cheeks.bank_account_select_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')

		self.assertTrue(recip_page.on())
		recip_page.click_recipient("Yolanda Castillo")

		# edit employee. Should be on default tab (info)
		self.assertTrue(view_page.on())
		self.assertEqual('info', view_page.current_tab())
		view_page.add_destination()

		self.assertTrue(ba_page.on())
		ba_page.set_location('us')
		zions_routing = "124000054"
		acct_number = "123456780001"
		ba_page.set_routing(zions_routing)
		ba_page.set_account(acct_number)
		ba_page.set_account_type('savings')
		ba_page.click_continue()

		# Should redirect recipient view page
		self.assertTrue(view_page.on())
		for i in xrange(view_page.num_accounts()):
			view_page.select_destination('bank', 0)
			self.assertTrue(ba_page.on())
			ba_page.remove()
			self.assertTrue(view_page.on())

		self.assertTrue(view_page.on())
		self.assertEqual(view_page.num_accounts(), 0)

	def test_edit_account(self):
		""" test_recipients.py:TestEdit.test_edit_account """
		# dependencies: Recip Roberto Ortega w/ zions bank account
		# 17 digit acct #, checking account.
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		view_page = self.cheeks.recipient_view_page
		ba_page = self.cheeks.bank_account_page
		send_page = self.cheeks.send_page
		sel_page = self.cheeks.bank_account_select_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')

		self.assertTrue(recip_page.on())
		recip_page.click_recipient("Roberto Ortega")

		# edit employee. Should be on default tab (info)
		self.assertTrue(view_page.on())
		self.assertEqual('info', view_page.current_tab())
		view_page.sel_tab('destinations')
		view_page.select_destination('bank', 0)

		self.assertTrue(ba_page.on())
		ba_page.header.click_back()

		self.assertTrue(view_page.on())
		view_page.select_destination('bank', 0)

		self.assertTrue(ba_page.on())
		zions_routing = "124000054"
		wells_routing = "121042882"
		self.assertEqual(
			zions_routing,
			ba_page.routing_number.get_attribute('value'))
		self.assertEqual('checking', ba_page.get_account_type())
		account_number = ba_page.account_number.get_attribute('value')
		acct_num_length = len(account_number)
		self.assertEqual(acct_num_length-4, account_number.count('X'))
		unredacted = account_number[-4:]
		self.assertEqual(0, unredacted.count('X'))

		ba_page.set_routing(wells_routing)
		self.assertEqual(
			wells_routing,
			ba_page.routing_number.get_attribute('value')
		)
		new_acct_num = self.cheeks.generate_number(3)

		ba_page.set_account(new_acct_num)
		ba_page.set_account_type('savings')
		self.assertEqual('savings', ba_page.get_account_type())
		ba_page.click_continue()

		self.assertTrue(view_page.on())
		view_page.select_destination('bank', 0)

		self.assertTrue(ba_page.on())
		new_acct_num = self.cheeks.generate_number(17)
		ba_page.set_routing(zions_routing)
		ba_page.set_account(new_acct_num)
		ba_page.set_account_type('checking')
		ba_page.click_continue()

		self.assertTrue(view_page.on())
		view_page.header.click_back()

		self.assertTrue(recip_page.on())

	def test_edit_additional_info(self):
		""" test_recipients.py:TestEdit.test_edit_additional_info """
		# Test that editing recipient's additional info persists
		# Dependencies: Roberto Ortega has BBVA cashout
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		view_page = self.cheeks.recipient_view_page
		info_page = self.cheeks.recipient_info_page

		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')

		self.assertTrue(recip_page.on())
		recip_page.click_recipient("Roberto Ortega")

		self.assertTrue(view_page.on())
		self.assertEqual('info', view_page.current_tab())
		view_page.edit_additional_info()

		# edit existing recipient info
		self.assertTrue(info_page.on())
		initial_info = info_page.addInfo.get_info()

		new_carrier = 'telcel'
		new_phone = self.cheeks.format_phone('202' + self.cheeks.generate_number(7))
		new_dob = self.cheeks.generate_rfc_dob()

		if initial_info['carrier'] == 'telcel':
			new_carrier = 'at&t'
		while new_phone == initial_info['phone']:
			new_phone = self.cheeks.format_phone('202' + self.cheeks.generate_number(7))
			while new_dob != initial_info['dob']:
				new_dob = self.cheeks.generate_rfc_dob()
		new_info = {
			'carrier': new_carrier,
			'phone': new_phone,
			'dob': new_dob,
		}
		info_page.addInfo.set_info(new_info)
		info_page.addInfo.click_continue()
		self.assertTrue(view_page.on())

		# verify info persisted
		view_page.edit_additional_info()
		self.assertTrue(info_page.on())
		updated_info = info_page.addInfo.get_info()
		self.assertEqual(new_info['carrier'], updated_info['carrier'])
		self.assertEqual(new_info['phone'], updated_info['phone'])
		self.assertEqual(new_info['dob'], updated_info['dob'])

	def test_edit_address(self):
		""" test_recipients.py:TestEdit.test_edit_address """
		# dependencies: Roberto Ortega starts w/ cur_address
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		view_page = self.cheeks.recipient_view_page
		address_page = self.cheeks.recipient_address_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')

		self.assertTrue(recip_page.on())
		recip_page.click_recipient("Roberto Ortega")

		self.assertTrue(view_page.on())
		self.assertEqual('info', view_page.current_tab())
		view_page.edit_address()

		self.assertTrue(address_page.on())
		address_page.header.click_back()

		self.assertTrue(view_page.on())
		view_page.edit_address()
		# ios is a pain. Only set states that are visible when state dd opens
		cur_address = [
			"101 Main Street",
			"Col. Atlatilco",
			"Cancun",
			"Sonora",
			"02383"
		]
		new_address = [
			"2005 State Street",
			"Centro",
			"Mexico City",
			"Quintana Roo",
			"06543"
		]
		self.assertTrue(address_page.on())
		# if this fails, reset address to cur_address
		# Todo: fix test so it doesn't matter what initial address is
		self.assertEqual(cur_address,address_page.get_address())
		address_page.set_address(new_address, dest_page='recipient_view')

		self.assertTrue(view_page.on())
		view_page.edit_address()

		self.assertTrue(address_page.on())
		self.assertEqual(new_address,address_page.get_address())
		address_page.set_address(cur_address, dest_page='recipient_view')

		self.assertTrue(view_page.on())
		view_page.header.click_back()

		self.assertTrue(recip_page.on())

	# def test_edit_cashout_mx(self):
	# 	"""recipients : Edit .                               edit_cashout_mx"""
	# 	# Create/Edit/Delete cashout location for MX based recipient
	# 	# Cannot edit right now, only delete. Tested in test_add_new_mx_cash
	# 	pass

	# def test_edit_cashout_us(self):
	# 	"""recipients : Edit .                               edit_cashout_us"""
	# 	# Create/Edit/Delete cashout location for US based recipient
	# 	# Cannot edit right now, only delete. Tested in test_add_new_us_cash
	# 	pass

	def test_edit_name(self):
		""" test_recipients.py:TestEdit.test_edit_name """
		# dependencies: recipient Roberto Ortega
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		view_page = self.cheeks.recipient_view_page
		name_page = self.cheeks.recipient_name_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')

		self.assertTrue(recip_page.on())
		recip_page.click_recipient("Roberto Ortega")

		self.assertTrue(view_page.on())
		self.assertEqual('info', view_page.current_tab())
		view_page.edit_name()

		self.assertTrue(name_page.on())
		name_page.header.click_back()

		self.assertTrue(view_page.on())
		view_page.edit_name()

		self.assertTrue(name_page.on())
		name = ["Roberto","Ortega",""]
		new_name = ["Romero","Garcia","Lopez"]
		name_page.enter_name(new_name)

		self.assertTrue(view_page.on())
		view_page.header.click_back()

		self.assertTrue(recip_page.on())
		recip_page.click_recipient("Romero Garcia Lopez")

		self.assertTrue(view_page.on())
		view_page.edit_name()

		self.assertTrue(name_page.on())
		name_page.enter_name(name)

		self.assertTrue(view_page.on())
		view_page.header.click_back()

		self.assertTrue(recip_page.on())
		recip_page.click_recipient("Roberto Ortega")
		self.assertTrue(view_page.on())

	@unittest.skipIf(not main.is_web(), "No urls on native")
	def test_try_access_address(self):
		""" test_recipients.py:TestEdit.test_try_access_address """
		# asserting can access address page by url
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		view_page = self.cheeks.recipient_view_page
		address_page = self.cheeks.recipient_address_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')

		self.assertTrue(recip_page.on())
		recip_page.click_recipient("Miguel Castillo")

		self.assertTrue(view_page.on())
		view_page.go_to_address()
		self.assertTrue(address_page.on())

class TestRecipients(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver,'cheeks')

	def tearDown(self):
		self.driver.quit()

	# @unittest.skip("Deprecated. Adding recipient w/ bbva destination added to atm tests")
	# def test_add_new_mx_bbva(self):
	# 	"""recipients : Recipients .                         add_new_mx_bbva"""
	# 	# Add MX based recipient w/ BBVA cashout
	# 	eHome = self.cheeks.eHome_page
	# 	recip_select_page = self.cheeks.recipient_page
	# 	name_page = self.cheeks.recipient_name_page
	# 	address_page = self.cheeks.recipient_address_page
	# 	ba_page = self.cheeks.bank_account_page
	# 	info_page = self.cheeks.recipient_info_page
	# 	clabe_page = self.cheeks.clabe_page
	# 	send_page = self.cheeks.send_page
	# 	view_page = self.cheeks.recipient_view_page
	# 	self.assertTrue(self.cheeks.login(self.driver), messages.login)

	# 	# Add MX based recipient
	# 	self.assertTrue(eHome.on())
	# 	eHome.send_money()
	# 	self.assertTrue(recip_select_page.on())
	# 	recip_select_page.click_add()
	# 	self.assertTrue(name_page.on())
	# 	name_page.set_location("Mexico")
	# 	name = self.cheeks.generate_name()
	# 	name_page.enter_name(name)

	# 	self.assertTrue(ba_page.on())
	# 	self.assertEqual('cashout', ba_page.get_destination_type())
	# 	ba_page.click_continue()

	# 	self.assertTrue(info_page.on())
	# 	rfc = (
	# 		self.cheeks.generate_string(4, 'upper') +
	# 		self.cheeks.generate_number(2) + '0' +
	# 		self.cheeks.generate_number(1, lower_bound=1) + '0' +
	# 		self.cheeks.generate_number(1, lower_bound=1)
	# 	)
	# 	info = {
	# 		'carrier': 'telcel',
	# 		'phone': '2022221234',
	# 		'rfc': rfc,
	# 		'pin': self.cheeks.generate_number(4)
	# 	}
	# 	info_page.set_info(info)
	# 	returned_info = info_page.get_info()
	# 	self.assertEqual(info['carrier'], returned_info['carrier'])
	# 	self.assertEqual(info['phone'], returned_info['phone'])
	# 	self.assertEqual(info['rfc'], returned_info['rfc'])
	# 	self.assertEqual(info['pin'], returned_info['pin'])
	# 	info_page.click_continue()

	# 	# Started from 'Send Money', should go to send page and back to recipient list
	# 	self.assertTrue(send_page.on())
	# 	send_page.header.click_back()
	# 	self.assertTrue(recip_select_page.on())
	# 	recip_select_page.click_recipient(name, 'edit')

	# 	self.assertTrue(view_page.on())
	# 	# Remove cashout location then remove recipient
	# 	view_page.sel_tab('destinations')
	# 	self.assertEqual(1, view_page.num_cashOut())
	# 	#view_page.select_destination('cash', 0)
	# 	view_page.remove_cashout_location(0)
	# 	self.assertEqual(0, view_page.num_cashOut())

	# 	view_page.remove_recipient()
	# 	self.assertTrue(recip_select_page.on())
	# test_add_new_mx_bbva.e2e = True

	# def test_add_new_mx_cashout(self):

	def test_add_new_mx_mx(self):
		""" test_recipients.py:TestRecipients.test_add_new_mx_mx """
		eHome = self.cheeks.eHome_page
		recip_select_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		address_page = self.cheeks.recipient_address_page
		ba_page = self.cheeks.bank_account_page
		clabe_page = self.cheeks.clabe_page
		send_page = self.cheeks.send_page
		view_page = self.cheeks.recipient_view_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		# Add MX based recipient
		self.assertTrue(eHome.on())
		eHome.send_money()
		self.assertTrue(recip_select_page.on())
		recip_select_page.click_add()
		self.assertTrue(name_page.on())
		name_page.set_location("Mexico")
		recip_name = self.cheeks.generate_name()
		name_page.enter_name(recip_name)

		self.assertTrue(address_page.on())
		address = [
			"101 Main Street",
			"Col. Atlatilco",
			"Mexico City",
			"Sinaloa", # Ciudad de Mexico
			"02383"
		]
		address_page.set_address(address)

		# Add MX bank account
		self.assertTrue(ba_page.on())
		ba_page.set_location("Mexico")
		ba_page.click_what_is_clabe()
		self.assertTrue(clabe_page.on())
		clabe_page.header.click_back()

		self.assertTrue(ba_page.on())
		ba_page.set_destination_type('bank')
		# should default to US bank. MX bank should not be option
		self.assertFalse(ba_page.account_number == None)
		self.assertIsNone(ba_page.clabe_input)
		ba_page.set_location("Mexico")
		# 002180900519159839 = valid clabe
		ba_page.set_clabe("032180000118359719")
		ba_page.click_continue()
		self.assertTrue(send_page.on())
		send_page.header.click_back()
		self.assertTrue(recip_select_page.on())

		identifier = " ".join(recip_name)
		recip_select_page.edit_recipient(identifier)

		self.assertTrue(view_page.on())
		view_page.edit_name()

		self.assertTrue(name_page.on())
		self.assertEqual(recip_name[0],
			name_page.first_name.get_attribute('value'))
		self.assertEqual(recip_name[1],
			name_page.last_name.get_attribute('value'))
		self.assertEqual(recip_name[2],
			name_page.second_surname.get_attribute('value'))
		name_page.header.click_back()
		self.assertTrue(view_page.on())
		view_page.remove_recipient()

		self.assertTrue(recip_select_page.on())

	# @unittest.skip("Deprecated: Functionality covered in send to bank/atm tests")
	# def test_add_new_mx_us(self):
	# 	"""recipients : Recipients .                           add_new_mx_us"""
	# 	eHome = self.cheeks.eHome_page
	# 	recip_select_page = self.cheeks.recipient_page
	# 	name_page = self.cheeks.recipient_name_page
	# 	address_page = self.cheeks.recipient_address_page
	# 	ba_page = self.cheeks.bank_account_page
	# 	send_page = self.cheeks.send_page
	# 	view_page = self.cheeks.recipient_view_page
	# 	self.assertTrue(self.cheeks.login(self.driver), messages.login)

	# 	self.assertTrue(eHome.on())
	# 	eHome.send_money()

	# 	self.assertTrue(recip_select_page.on())
	# 	recip_select_page.click_add()

	# 	self.assertTrue(name_page.on())
	# 	name_page.set_location("Mexico")
	# 	recip_name = self.cheeks.generate_name()
	# 	name_page.enter_name(recip_name)

	# 	# self.assertTrue(address_page.on())
	# 	# address = [
	# 	# 	"101 Main Street",
	# 	# 	"Col. Atlatilco",
	# 	# 	"Mexico City",
	# 	# 	"Sinaloa", # Ciudad de Mexico
	# 	# 	"02383"
	# 	# ]
	# 	# address_page.set_address(address)

	# 	self.assertTrue(ba_page.on())
	# 	ba_page.set_destination_type('bank')
	# 	self.assertEqual(ba_page.get_location(), 'United States')

	# 	routing_num = "124000054"
	# 	acct_num = self.cheeks.generate_number(17)
	# 	ba_page.set_routing(routing_num)
	# 	ba_page.set_account(acct_num)
	# 	ba_page.set_account_type('savings')
	# 	ba_page.click_continue()

	# 	self.assertTrue(send_page.on())
	# 	send_page.header.click_back()

	# 	self.assertTrue(recip_select_page.on())
	# 	identifier = " ".join(recip_name)
	# 	recip_select_page.edit_recipient(identifier)

	# 	self.assertTrue(view_page.on())
	# 	view_page.edit_name()

	# 	self.assertTrue(name_page.on())
	# 	self.assertEqual(recip_name[0],
	# 		name_page.first_name.get_attribute('value'))
	# 	self.assertEqual(recip_name[1],
	# 		name_page.last_name.get_attribute('value'))
	# 	self.assertEqual(recip_name[2],
	# 		name_page.second_surname.get_attribute('value'))
	# 	name_page.header.click_back()

	# 	self.assertTrue(view_page.on())
	# 	view_page.remove_recipient()

	# See bug# 155472162
	# redirects to wrong page after adding address for US recipient
	# @unittest.expectedFailure
	@unittest.skip("Not supporting cashout locations. 3/15/18")
	def test_add_new_us_cash(self):
		""" test_recipients.py:TestRecipients.test_add_new_us_cash """
		# Create US based recipient w/ cashout location
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		ba_page = self.cheeks.bank_account_page
		address_page = self.cheeks.recipient_address_page
		ba_select_page = self.cheeks.bank_account_select_page
		send_page = self.cheeks.send_page
		view_page = self.cheeks.recipient_view_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		# create US based recipient
		self.assertTrue(eHome.on())
		eHome.send_money()
		self.assertTrue(recip_page.on())
		recip_page.click_add()
		self.assertTrue(name_page.on())
		name_page.set_location('us')
		self.assertEqual('United States', name_page.get_location())

		name = self.cheeks.generate_name()
		name_page.enter_name(name)

		self.assertTrue(ba_page.on())
		address = [
			"Titanio 9530 ",
			"Valle de Infonavit ",
			"Monterrey ",
			"Nuevo Leon", # Actual address, public phone in Monterrey
			"64350"
		]

		# Add cashout location
		self.assertTrue(ba_page.on())
		self.assertTrue(ba_page.get_destination_type() == 'cashout')
		ba_page.search_cashout_address(address) #update to address if it's valid
		ba_page.select_cashout_location('Soriana')
		self.assertTrue(view_page.on())

		view_page.send_money()
		self.assertTrue(address_page.on())
		address_page.set_address(address)

		# Bug# 155472162
		# Redirects to bank account page instead of send page (already added cashout)

		self.assertTrue(send_page.on())
		send_page.menu.click_option('recipients')

		# Remove cashout location then remove recipient
		self.assertTrue(recip_select_page.on())
		recip_select_page.click_recipient(recip_name[0] + ' ' + recip_name[1] + ' ' + recip_name[2])
		self.assertTrue(view_page.on())

		view_page.sel_tab('destinations')
		self.assertEqual(1, view_page.num_cashOut())
		view_page.select_destination('cash', 0)
		view_page.remove_cashout_location(0)
		self.assertEqual(0, view_page.num_cashOut())

		view_page.remove_recipient()
		self.assertTrue(recip_select_page.on())

		# Currently no way to add cash-out location during creation process
		# Complete when bug# 155474937 is fixed

		# self.assertTrue(send_page.on())
		# send_page.header.click_back()

		# self.assertTrue(recip_page.on())
		# identifier = " ".join(name)
		# recip_page.edit_recipient(identifier)
		# self.assertTrue(view_page.on())
		# view_page.edit_name()

		# self.assertTrue(name_page.on())
		# self.assertEqual(name[0], name_page.first_name.get_attribute('value'))
		# self.assertEqual(name[1], name_page.last_name.get_attribute('value'))
		# self.assertEqual(
		#   name[2], name_page.second_surname.get_attribute('value'))
		# name_page.header.click_back()

		# self.assertTrue(view_page.on())
		# view_page.remove_recipient()

	@unittest.skip("Cannot add MX bank account. 3/15/18")
	def test_add_new_us_mx(self):
		""" test_recipients.py:TestRecipients.test_add_new_us_mx """
		# dependencies:
		eHome = self.cheeks.eHome_page
		recip_select_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		ba_page = self.cheeks.bank_account_page
		clabe_page = self.cheeks.clabe_page
		address_page = self.cheeks.recipient_address_page
		send_page = self.cheeks.send_page
		view_page = self.cheeks.recipient_view_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		# Add US recipient
		self.assertTrue(eHome.on())
		eHome.send_money()
		self.assertTrue(recip_select_page.on())
		recip_select_page.click_add()
		self.assertTrue(name_page.on())
		name_page.set_location("us")
		recip_name = self.cheeks.generate_name()
		name_page.enter_name(recip_name)

		# Add MX bank account
		self.assertTrue(ba_page.on())
		ba_page.set_location("Mexico")
		ba_page.click_what_is_clabe()
		self.assertTrue(clabe_page.on())
		clabe_page.header.click_back()

		self.assertTrue(ba_page.on())
		ba_page.set_location("Mexico")
		# 002180900519159839
		ba_page.set_clabe("032180000118359719")
		ba_page.click_continue()

		# should prompt for address because sending to MX bank account
		self.assertTrue(address_page.on())
		address = [
			"101 Main Street",
			"Col. Atlatilco",
			"Mexico City",
			"Sinaloa", # Ciudad de Mexico
			"02383"
		]
		address_page.set_address(address, dest_page='send')

		self.assertTrue(send_page.on())
		send_page.header.click_back()
		self.assertTrue(recip_select_page.on())

		identifier = " ".join(recip_name)
		recip_select_page.edit_recipient(identifier)

		self.assertTrue(view_page.on())
		view_page.edit_name()

		self.assertTrue(name_page.on())
		self.assertEqual(recip_name[0],
			name_page.first_name.get_attribute('value'))
		self.assertEqual(recip_name[1],
			name_page.last_name.get_attribute('value'))
		self.assertEqual(recip_name[2],
			name_page.second_surname.get_attribute('value'))
		name_page.header.click_back()

		self.assertTrue(view_page.on())
		view_page.remove_recipient()

	def test_add_new_us_us(self):
		""" test_recipients.py:TestRecipients.test_add_new_us_us """
		# Create US based recipient w/ US bank account.
		eHome = self.cheeks.eHome_page
		recip_page = self.cheeks.recipient_page
		name_page = self.cheeks.recipient_name_page
		ba_page = self.cheeks.bank_account_page
		ba_select_page = self.cheeks.bank_account_select_page
		send_page = self.cheeks.send_page
		view_page = self.cheeks.recipient_view_page
		self.assertTrue(self.cheeks.login(self.driver), messages.login)

		# create US based recipient
		self.assertTrue(eHome.on())
		eHome.menu.click_option('recipients')
		self.assertTrue(recip_page.on())
		recip_page.add_recipient()
		self.assertTrue(name_page.on())
		name_page.set_location('us')
		self.assertEqual('United States', name_page.get_location())

		name = self.cheeks.generate_name()
		name_page.enter_name(name)

		self.assertTrue(recip_page.on())
		recip_page.click_recipient(name)
		self.assertTrue(view_page.on())
		view_page.add_destination()

		self.assertTrue(ba_page.on())
		# ba_page.set_destination_type('bank')
		self.assertEqual('United States', ba_page.get_location())

		routing_num = "124000054"
		acct_num = self.cheeks.generate_number(17)
		ba_page.set_routing(routing_num)
		ba_page.set_account(acct_num)
		self.assertEqual('checking', ba_page.get_account_type())
		ba_page.set_account_type('savings')
		self.assertEqual('savings', ba_page.get_account_type())
		ba_page.click_continue()

		self.assertTrue(view_page.on())
		view_page.edit_name()

		self.assertTrue(name_page.on())
		self.assertEqual(name[0], name_page.first_name.get_attribute('value'))
		self.assertEqual(name[1], name_page.last_name.get_attribute('value'))
		self.assertEqual(
			name[2], name_page.second_surname.get_attribute('value'))
		name_page.header.click_back()

		self.assertTrue(view_page.on())
		view_page.remove_recipient()
