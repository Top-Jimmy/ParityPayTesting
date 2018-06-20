# import unittest
# import time
# from decimal import *
# import profiles
# import browser
# import main
# import messages

# # Missing
# # -No 'Send Now' functionality
# # -MX transfer entries display MXN amount instead of US amount.

# # Total: 22
# # TestActivityTab - 2       Send behavior from recipient view page
# 	# test_activity_success
# 	# test_activity_td
# # TestDefaultBehavior - 5      Default bank account behavior
# 	# test_create_new_bank_account
# 	# test_custom_keyboard_mx
# 	# test_custom_keyboard_us
# 	# test_edit_bank_account
# 	# test_send_logout
# 	# test_send_to_bank_account
# # TestMXCash - 2
# 	# test_send_bbva (not implemented)
# 	# test_send_cashout (not implemented)
# # TestMXFast - 8            Sending to MX account w/ 30 min window
# 	# test_fast_cancel
# 	# test_fast_send_now
# 	# test_fast_send_screens
# 	# test_fast_success
# 	# test_fast_td
# 	# test_mx_links
# 	# test_no_balance
# 	# test_remember_send_speed
# # TestMXInstant - 3         Sending to MX account instantly
# 	# test_instant_send_screens
# 	# test_instant_success
# 	# test_instant_td
# # TestUS - 4
# 	# test_no_balance
# 	# test_us_send_screens
# 	# test_us_success
# 	# test_us_td

# class TestTest(unittest.TestCase):
# 	def setUp(self):
# 		self.driver = browser.start(main.get_env(), main.get_browser())
# 		self.andrew = profiles.Profile(self.driver, 'andrew')

# 	def tearDown(self):
# 		self.driver.quit()

# 	def test_basic(self):
# 		"""send: TestTest .                 test_basic"""
# 		lobby_page = self.andrew.lobby_page
# 		eHome = self.andrew.eHome_page
# 		sendToBank = self.andrew.send_to_bank_page

# 		self.assertTrue(self.andrew.login(self.driver), messages.login)
# 		self.assertTrue(lobby_page.on())
# 		lobby_page.menu.set_role('employee')

# 		self.assertTrue(eHome.on())
# 		eHome.setTab('election')
# 		eHome.setTab('activity')

# 		eHome.send('bank')
# 		self.assertTrue(sendToBank.on())


# class TestActivityTab(unittest.TestCase):
# 	def setUp(self):
# 		self.driver = browser.start(main.get_env(), main.get_browser())
# 		self.cheeks = profiles.Profile(self.driver, 'cheeks')
# 		# self.WDWait = WebDriverWait(self.driver, 10)

# 	def tearDown(self):
# 		self.driver.quit()

# 	def test_activity_success(self):
# 		"""send : ActivityTab .                             activity_success"""
# 		# sending from recipient card works and ends up on account page
# 		# Currently sending to US bank account
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		view_page = self.cheeks.recipient_view_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and view Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.menu.click_option('recipients')

# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		self.assertTrue(view_page.on())
# 		view_page.sel_tab('activity')
# 		view_page.send_money()

# 		# generate random US amount and send
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		usd_total = disclosure_page.get_transfer_total()
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and checkout entry
# 		self.assertTrue(eHome.on())
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on(True))

# 		data = eHome.get_transaction()
# 		self.assertEqual(data['amount'], '-' + usd_total)
# 		self.assertEqual(data['recipient'], recip)
# 		self.assertEqual(data['icon'], 'clock')

# 		self.assertEqual(data['status'], 'Arriving')

# 		# checkout td page
# 		eHome.click_transaction()
# 		self.assertTrue(td_page.on())
# 		td_page.click_continue()

# 		self.assertTrue(eHome.on())

# 	def test_activity_td(self):
# 		"""send : ActivityTab .                                  activity_td"""
# 		# going to td page from recipient card goes back to activity tab
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page
# 		recip_page = self.cheeks.recipient_page
# 		view_page = self.cheeks.recipient_view_page

# 		# Login and send to Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount and send
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		usd_total = disclosure_page.get_transfer_total()
# 		disclosure_page.click_continue()

# 		# go to recipient card and checkout entry in activity tab
# 		self.assertTrue(eHome.on())
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on())
# 		eHome.menu.click_option('recipients')

# 		self.assertTrue(recip_page.on())
# 		recip_page.click_recipient(recip)

# 		self.assertTrue(view_page.on())
# 		view_page.sel_tab('activity')

# 		transaction = view_page.get_transaction()
# 		self.assertEqual(transaction['amount'], '-' + usd_total)
# 		self.assertEqual(transaction['recipient'], recip)
# 		self.assertEqual(transaction['icon'], 'clock')
# 		self.assertEqual(transaction['status'], 'Arriving')

# 		# clicking 'OK' on td page should go back to recipient activity tab
# 		view_page.click_transaction()
# 		self.assertTrue(td_page.on())
# 		td_page.click_continue()
# 		self.assertTrue(view_page.on())

# 		# cancelling transaction should go to account page
# 		# Note: MX banks are disabled for now
# 		# view_page.click_transaction()
# 		# self.assertTrue(td_page.on())
# 		# td_page.cancel_transaction()
# 		# raw_input('what page on?')
# 		# self.assertTrue(eHome.on())

# @unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# class TestDefaultBehavior(unittest.TestCase):
# 	def setUp(self):
# 		self.driver = browser.start(main.get_env(),main.get_browser())
# 		self.cheeks = profiles.Profile(self.driver,'cheeks')

# 	def tearDown(self):
# 		self.driver.quit()

# 	def test_create_new_bank_account(self):
# 		"""send : DefaultBehavior .                  create_new_bank_account"""
# 		# Default bank account should be set to most recently created one
# 		pass

# 	def test_edit_bank_account(self):
# 		"""send : DefaultBehavior .                        edit_bank_account"""
# 		# Default bank account should be most recently edited one
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		view_page = self.cheeks.recipient_view_page
# 		ba_page = self.cheeks.bank_account_page

# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on(True))
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'David Castillo'
# 		recip_page.click_recipient(recip)

# 		# figure out current 'default' bank. We will edit other bank (new_bank)
# 		self.assertTrue(send_page.on())
# 		bank1 = 'Zions Bank'
# 		bank2 = 'Wells Fargo Bank'
# 		initial_bank_info = send_page.get_account_info()

# 		new_bank = ''
# 		if bank1 in initial_bank_info['bank']:
# 			new_bank = bank2
# 		else:
# 			new_bank = bank1

# 		# Change account# of new_bank
# 		send_page.header.click_back()
# 		self.assertTrue(recip_page.on())
# 		recip_page.click_recipient(recip, 'edit')
# 		self.assertTrue(view_page.on())
# 		view_page.select_destination('bank', new_bank)
# 		self.assertTrue(ba_page.on())
# 		new_acct_num = self.cheeks.generate_number(12)
# 		ba_page.set_account(new_acct_num)
# 		ba_page.click_continue()

# 		# assert new_bank is now default
# 		self.assertTrue(view_page.on())
# 		view_page.send_money()
# 		self.assertTrue(send_page.on())
# 		new_bank_info = send_page.get_account_info()
# 		self.assertTrue(new_bank.lower() in new_bank_info['bank'].lower())

# 	def test_send_to_bank_account(self):
# 		"""send : DefaultBehavior .                     send_to_bank_account"""
# 		# Default bank account should be one most recently sent to
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		sel_page = self.cheeks.bank_account_select_page

# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on(True))
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'David Castillo'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount, set speed, change bank account
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)

# 		# figure out which bank is 'default'. want to send to other one
# 		bank1 = 'Zions Bank'
# 		bank2 = 'Wells Fargo Bank'
# 		initial_bank_info = send_page.get_account_info()

# 		new_bank = ''
# 		if bank1 in initial_bank_info['bank']:
# 			new_bank = bank2
# 		else:
# 			new_bank = bank1

# 		send_page.click_account()
# 		self.assertTrue(sel_page.on())

# 		sel_page.select_destination('bank', new_bank)
# 		self.assertTrue(send_page.on())
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		disclosure_page.click_continue()

# 		self.assertTrue(eHome.on(True))
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on(True))
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip_page.click_recipient(recip)

# 		self.assertTrue(send_page.on())
# 		new_bank_info = send_page.get_account_info()
# 		self.assertTrue(new_bank.lower() in new_bank_info['bank'].lower())

# 	def test_send_logout(self):
# 		"""send : DefaultBehavior .                           send_logout"""
# 		# Default bank account should be one most recently sent to.
# 		# Should persist after logging out/back in.
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		sel_page = self.cheeks.bank_account_select_page

# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on(True))
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'David Castillo'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount, set speed
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)

# 		# figure out which bank is 'default'. want to send to other one
# 		bank1 = 'Zions Bank'
# 		bank2 = 'Wells Fargo Bank'
# 		initial_bank_info = send_page.get_account_info()

# 		new_bank = ''
# 		if bank1 in initial_bank_info['bank']:
# 			new_bank = bank2
# 		else:
# 			new_bank = bank1

# 		send_page.click_account()
# 		self.assertTrue(sel_page.on())

# 		sel_page.select_destination('bank', new_bank)
# 		self.assertTrue(send_page.on())
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		disclosure_page.click_continue()

# 		self.assertTrue(eHome.on(True))
# 		eHome.clear_confirmation_dialog()
# 		eHome.menu.sign_out()

# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip_page.click_recipient(recip)

# 		self.assertTrue(send_page.on())
# 		new_bank_info = send_page.get_account_info()
# 		self.assertTrue(new_bank.lower() in new_bank_info['bank'].lower())

# 	# @unittest.skipIf(main.is_desktop(), "Custom keyboard mobile only")
# 	@unittest.skip("No MX banks")
# 	def test_custom_keyboard_mx(self):
# 		"""send : DefaultBehavior .                       custom_keyboard_mx"""
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)

# 		self.assertTrue(eHome.on(True))
# 		eHome.send_money()
# 		self.assertTrue(recip_page.on())
# 		recip = 'Leticia Ortega'
# 		recip_page.click_recipient(recip)
# 		self.assertTrue(send_page.on())

# 		# Custom keyboard should stay open when toggling between MXN/USD inputs
# 		send_page.usd_amount.click()
# 		self.assertTrue(send_page.keyboard_visible())
# 		send_page.mxn_div.click()
# 		self.assertTrue(send_page.keyboard_visible())

# 		# Custom keyboard should close when clicking off it.
# 		send_page.account_balance.click()
# 		self.assertFalse(send_page.keyboard_visible())

# 		# 'Continue' button should submit w/ 1 click when keyboard is open
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		send_page.click_continue()
# 		self.assertTrue(disclosure_page.on())

# 	@unittest.skipIf(main.is_desktop(), "Custom keyboard mobile only")
# 	def test_custom_keyboard_us(self):
# 		"""send : DefaultBehavior .                       custom_keyboard_us"""
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)

# 		self.assertTrue(eHome.on(True))
# 		eHome.send_money()
# 		self.assertTrue(recip_page.on())
# 		recip = 'David Castillo'
# 		recip_page.click_recipient(recip)
# 		self.assertTrue(send_page.on())

# 		# Custom keyboard should close when clicking off it.
# 		send_page.account_balance.click()
# 		self.assertFalse(send_page.keyboard_visible())

# 		# 'Continue' button should submit w/ 1 click when keyboard is open
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		send_page.click_continue()
# 		self.assertTrue(disclosure_page.on())

# # @unittest.skip("Not implemented yet")
# class TestMXCashout(unittest.TestCase):
# 	def setUp(self):
# 		self.driver = browser.start(main.get_env(),main.get_browser())
# 		self.cheeks = profiles.Profile(self.driver,'cheeks')

# 	def tearDown(self):
# 		self.driver.quit()

# 	def test_send_bbva(self):
# 		"""send : MXCashout .                                      send_bbva"""
# 		# Send to MX cashout recipient (Jose Ortega)
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)

# 		self.assertTrue(eHome.on())
# 		eHome.send_money()
# 		self.assertTrue(recip_page.on())
# 		recip = 'Jose Ortega'
# 		recip_page.click_recipient(recip)
# 		self.assertTrue(send_page.on())

# 		amount = self.cheeks.generate_bbva_amount()
# 		send_page.set_bbva_amount(amount)

# 	test_send_bbva.e2e = True

# 	def test_send_cashout(self):
# 		"""send : MXCashout .                                      send_bbva"""
# 		# Send to MX cashout recipient (Jose Ortega)
# 		pass
# 	#test_send_bbva.e2e = True

# @unittest.skip("No MX bank accounts")
# class TestMXFast(unittest.TestCase):
# 	def setUp(self):
# 		self.driver = browser.start(main.get_env(),main.get_browser())
# 		self.cheeks = profiles.Profile(self.driver,'cheeks')
# 		self.nicol = profiles.Profile(self.driver,'nicol')

# 	def tearDown(self):
# 		self.driver.quit()

# 	def test_fast_cancel(self):
# 		"""send : MXFast .                                       fast_cancel"""
# 		# can cancel 'fast' transaction
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on(True))
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount and send
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		mxn_amount = send_page.get_mxn()
# 		time.sleep(.4)
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		usd_total = disclosure_page.get_transfer_total()
# 		fee = disclosure_page.get_transfer_fee()
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and checkout entry
# 		self.assertTrue(eHome.on(True))
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on(True))

# 		# checkout td page
# 		eHome.click_transaction()
# 		self.assertTrue(td_page.on())

# 		# test cancel dialog td
# 		td_page.cancel_transaction('cancel')
# 		self.assertTrue(td_page.on())

# 		# actually cancel and end up on account page
# 		td_page.cancel_transaction()
# 		self.assertTrue(eHome.on(True))

# 		data = eHome.get_transaction()
# 		# amount will be gray (no effect on balance) and will not have '-'
# 		total = Decimal(usd_amount) + Decimal(fee)
# 		self.assertEqual(data['amount'], str(total))
# 		self.assertEqual(data['recipient'], recip)
# 		self.assertEqual(data['icon'], 'x')
# 		self.assertEqual(data['status'], 'Canceled')

# 		eHome.click_transaction()
# 		self.assertTrue(td_page.on())

# 	def test_fast_send_now(self):
# 		"""send : MXFast .                                     fast_send_now"""
# 		# can 'send now' fast transaction
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount and send
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		mxn_amount = send_page.get_mxn()
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		usd_total = disclosure_page.get_transfer_total()
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and checkout entry
# 		self.assertTrue(eHome.on())
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on(True))

# 		# checkout td page
# 		eHome.click_transaction()
# 		self.assertTrue(td_page.on())

# 		# test td page 'send now' dialog
# 		self.assertTrue(td_page.send_now('cancel'))
# 		self.assertTrue(td_page.on())

# 		# actually 'send now' and end up on account page
# 		self.assertTrue(td_page.send_now())
# 		self.assertTrue(eHome.on(True))

# 		data = eHome.get_transaction()
# 		self.assertEqual(data['amount'], '-' + usd_total)
# 		self.assertEqual(data['recipient'], recip)
# 		self.assertEqual(data['icon'], 'check')
# 		self.assertEqual(data['status'], 'Completed')

# 		eHome.click_transaction()
# 		self.assertTrue(td_page.on())
# 	test_fast_send_now.e2e = True

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_fast_send_screens(self):
# 		"""send : MXFast .                                 fast_send_screens"""
# 		#Send and Disclosure pages interact as expected
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()
# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# send page is setup as expected
# 		self.assertTrue(send_page.on())
# 		self.assertFalse(send_page.is_enabled(send_page.continue_button))
# 		disabled_color = 'rgb(170, 170, 170)'
# 		background = send_page.continue_button.value_of_css_property('background')
# 		self.assertTrue(disabled_color in background)
# 		self.assertEqual('fast', send_page.get_speed())
# 		self.assertEqual("0",send_page.get_usd())
# 		self.assertEqual("0",send_page.get_mxn())
# 		balance = send_page.get_balance()
# 		exchange_rate = send_page.get_exchange_rate()

# 		# send page amounts work as expected
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		self.assertTrue(send_page.is_enabled(send_page.continue_button))
# 		background = send_page.continue_button.value_of_css_property('background')
# 		enabled_color = 'rgb(105, 214, 241)'
# 		self.assertTrue(enabled_color in background)
# 		self.assertEqual(usd_amount,send_page.get_usd())
# 		mxn_amount = send_page.get_mxn()

# 		# should ignore leading 0
# 		send_page.set_mxn('0.00')
# 		self.assertEqual('0.00', send_page.get_usd())
# 		send_page.set_mxn(mxn_amount)
# 		self.assertEqual(usd_amount, send_page.get_usd())

# 		# check speed changes are as expected
# 		send_page.exchange_rate.click()
# 		send_page.set_speed('instant')
# 		self.assertEqual('instant', send_page.get_speed())
# 		send_page.set_speed('fast')
# 		self.assertEqual('fast', send_page.get_speed())

# 		# check disclosure page has everything we expect
# 		send_page.click_continue()
# 		# check name and totals
# 		self.assertTrue(disclosure_page.on())
# 		self.assertEqual(recip, disclosure_page.name)
# 		self.assertEqual(usd_amount, disclosure_page.get_transfer_amount())
# 		transfer_fee = disclosure_page.get_transfer_fee()
# 		self.assertEqual("1.00",transfer_fee)
# 		total = Decimal(usd_amount) + Decimal(transfer_fee)
# 		self.assertEqual(str(total),disclosure_page.get_transfer_total())

# 		# check exchange rate, total to recipient, amount, fee and total
# 		self.assertEqual(exchange_rate, disclosure_page.get_exchange_rate())
# 		self.assertEqual(
# 			mxn_amount + " MXN" , disclosure_page.get_total_to_recipient())
# 		self.assertEqual(usd_amount, disclosure_page.transfer_amount)
# 		fee = '1.00'
# 		self.assertEqual(fee, disclosure_page.transfer_fee)
# 		total = Decimal(usd_amount) + Decimal(fee)
# 		self.assertEqual(str(total), disclosure_page.transfer_total)

# 		# disclosures
# 		self.assertTrue(disclosure_page.has_d_30())
# 		self.assertTrue(disclosure_page.has_d_less())
# 		self.assertTrue(disclosure_page.has_d_notify())

# 		# clicking back should go to send screen
# 		disclosure_page.header.click_back()
# 		self.assertTrue(send_page.on())
# 		send_page.click_continue()
# 		self.assertTrue(disclosure_page.on())

# 		# send, clear confirmation dialog
# 		disclosure_page.click_continue()
# 		self.assertTrue(eHome.on(True))

# 		if main.cancel_transaction():
# 			eHome.clear_confirmation_dialog()
# 			eHome.click_transaction()
# 			self.assertTrue(td_page.on())
# 			td_page.cancel_transaction()

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_fast_success(self):
# 		"""send : MXFast .                                      fast_success"""
# 		# Can send to MX account w/ 30 min window. Entry is as expected
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		original_balance = eHome.get_balance()
# 		eHome.send_money()
# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount and send
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		mxn_amount = send_page.get_mxn()
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		usd_total = disclosure_page.get_transfer_total()
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and checkout entry
# 		self.assertTrue(eHome.on())
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on(True))

# 		data = eHome.get_transaction()
# 		self.assertEqual(data['amount'], '-' + usd_total)
# 		self.assertEqual(data['recipient'], recip)
# 		self.assertEqual(data['icon'], 'clock')
# 		self.assertEqual(data['status'], 'Scheduled')

# 		# subtract $1 from difference to account for transfer fee.
# 		new_balance = eHome.get_balance()
# 		difference = str(Decimal(original_balance) - Decimal(new_balance)-1)
# 		self.assertEqual(difference, usd_amount)

# 		# checkout td page
# 		eHome.click_transaction()
# 		self.assertTrue(td_page.on())

# 		if main.cancel_transaction():
# 			td_page.cancel_transaction()

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_fast_td(self):
# 		"""send : MXFast .                                           fast_td"""
# 		# Transfer details is as expected for fast MX transfer
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and send random amount to Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		time.sleep(.6)
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and checkout entry and td page
# 		self.assertTrue(eHome.on())
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on())
# 		eHome.click_transaction()

# 		self.assertTrue(td_page.on())
# 		self.assertEqual('clock', td_page.read_transaction_icon())
# 		self.assertTrue(td_page.send_now_button is not None)
# 		self.assertTrue(td_page.cancel_button is not None)

# 		if main.cancel_transaction():
# 			td_page.cancel_transaction()

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_mx_links(self):
# 		"""send : MXFast .                                          mx_links"""
# 		# Send 'side pages' are accessible and navigation works as expected
# 		#dependencies: Recipient Lourdes Ortega with 1 MX account
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		sel_page = self.cheeks.bank_account_select_page
# 		ba_page = self.cheeks.bank_account_page
# 		td_page = self.cheeks.td_page

# 		# select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		'''if recip_page.num_recipients() != 8:
# 			print('num recips = ' + str(recip_page.num_recipients))'''
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# can go to edit bank account
# 		self.assertTrue(send_page.on())
# 		send_page.click_account()
# 		self.assertTrue(sel_page.on())
# 		self.assertEqual(1, sel_page.num_accounts())
# 		sel_page.select_destination('bank', 0, 'edit')
# 		self.assertTrue(ba_page.on())
# 		ba_page.header.click_back()

# 		# can go to add bank account
# 		self.assertTrue(sel_page.on())
# 		sel_page.click_add()
# 		self.assertTrue(ba_page.on())
# 		ba_page.header.click_back()
# 		self.assertTrue(sel_page.on())
# 		sel_page.select_destination('bank', 0)

# 		# set amount and continue to acct page
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		send_page.click_continue()

# 		self.assertTrue(disclosure_page.on())
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and checkout entry
# 		self.assertTrue(eHome.on())
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on())
# 		eHome.click_transaction()

# 		self.assertTrue(td_page.on())
# 		self.assertEqual('clock', td_page.icon_type)

# 		self.assertTrue(td_page.send_now_button is not None)
# 		self.assertTrue(td_page.cancel_button is not None)

# 		if main.cancel_transaction():
# 			td_page.cancel_transaction()

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_no_balance(self):
# 		"""send : MXFast .                                        no_balance"""
# 		# trying to send w/ no balance works as expected
# 		lobby_page = self.nicol.lobby_page
# 		eHome = self.nicol.eHome_page
# 		send_to_bank = self.nicol.send_to_bank_page
# 		recip = "Lourdes Ortega"

# 		# Try to send money to Lourdes Ortega
# 		self.assertTrue(self.nicol.login(self.driver), messages.login)
# 		self.assertTrue(lobby_page.on())
# 		lobby_page.menu.set_role('employee')

# 		self.assertTrue(eHome.on())
# 		# menu should be closed on mobile
# 		if not main.is_desktop():
# 			self.assertFalse(eHome.menu.is_drawer_visible())
# 		eHome.send('bank')
# 		self.assertTrue(send_to_bank.on())
# 		self.assertEqual('Choose Account', send_to_bank.stepper.current_step)
# 		send_to_bank.recipients[recip][0]['element'].click()




# 		# eHome.send_money()

# 		# self.assertTrue(recip_page.on())
# 		# recip_page.click_recipient(recip)

# 		# # generate random US amount and send
# 		# self.assertTrue(send_page.on())
# 		# usd_amount = self.nicol.generate_amount()
# 		# send_page.set_usd(usd_amount)
# 		# self.assertFalse(send_page.is_enabled(send_page.continue_button))
# 		# self.assertTrue(send_page.on())

# 		# self.assertTrue(send_page.has_balance_error())
# 		# send_page.exchange_rate.click()
# 		# send_page.try_clear_balance_error()
# 		# # didn't clear balance error? Other element would receive click
# 		# self.assertFalse(send_page.has_balance_error())

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_remember_send_speed(self):
# 		"""send : MXFast .                               remember_send_speed"""
# 		# should retain send speed when switching bank accounts
# 		# Leticia should have 2 mx accounts
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		sel_page = self.cheeks.bank_account_select_page

# 		# Login and select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'Leticia Ortega'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount, set speed, change bank account
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		send_page.exchange_rate.click()    #clear away mobile keyboard
# 		send_page.set_speed('instant')

# 		# figure out which bank is 'default'. want to select other one
# 		bank1 = 'BBVA Bancomer'
# 		bank2 = 'Banco Nacional'
# 		initial_bank_info = send_page.get_account_info()

# 		new_bank = ''
# 		if bank1 in initial_bank_info['bank']:
# 			new_bank = bank2
# 		else:
# 			new_bank = bank1

# 		send_page.click_account()
# 		self.assertTrue(sel_page.on())

# 		sel_page.select_destination('bank', new_bank)
# 		self.assertTrue(send_page.on())

# 		self.assertEqual(send_page.get_speed_toggle(), 'instant')

# @unittest.skip("No MX bank accounts")
# class TestMXInstant(unittest.TestCase):
# 	def setUp(self):
# 		self.driver = browser.start(main.get_env(),main.get_browser())
# 		self.cheeks = profiles.Profile(self.driver,'cheeks')

# 	def tearDown(self):
# 		self.driver.quit()

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_instant_send_screens(self):
# 		"""send : MXInstant .                           instant_send_screens"""
# 		#Send and Disclosure pages interact as expected
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# send page is setup as expected
# 		self.assertTrue(send_page.on())
# 		self.assertFalse(send_page.is_enabled(send_page.continue_button))
# 		self.assertEqual('fast', send_page.get_speed())
# 		self.assertEqual("0",send_page.get_usd())
# 		self.assertEqual("0",send_page.get_mxn())
# 		balance = send_page.get_balance()
# 		exchange_rate = send_page.get_exchange_rate()

# 		# send page amounts work as expected
# 		usd_amount = self.cheeks.generate_amount(digits=1)
# 		send_page.set_usd(usd_amount)
# 		self.assertEqual(usd_amount,send_page.get_usd())
# 		mxn_amount = send_page.get_mxn()

# 		send_page.set_mxn('0.00')
# 		self.assertEqual('0.00', send_page.get_usd())
# 		send_page.set_mxn(mxn_amount)
# 		self.assertEqual(usd_amount, send_page.get_usd())

# 		# check speed changes are as expected
# 		self.assertEqual('fast', send_page.get_speed())
# 		send_page.set_speed('instant')
# 		self.assertEqual('instant', send_page.get_speed())

# 		# check disclosure page has everything we expect
# 		send_page.click_continue()
# 		# check name and totals
# 		self.assertTrue(disclosure_page.on())
# 		self.assertEqual(recip, disclosure_page.name)

# 		self.assertEqual(usd_amount, disclosure_page.get_transfer_amount())
# 		transfer_fee = '1.00'

# 		self.assertEqual(transfer_fee,disclosure_page.get_transfer_fee())
# 		usd_total = Decimal(usd_amount) + Decimal(transfer_fee)
# 		self.assertEqual(str(usd_total), disclosure_page.get_transfer_total())

# 		# check exchange rate and total to recipient
# 		self.assertEqual(exchange_rate, disclosure_page.get_exchange_rate())
# 		self.assertEqual(
# 			mxn_amount + " MXN" , disclosure_page.get_total_to_recipient())

# 		# disclosures
# 		self.assertFalse(disclosure_page.has_d_30())
# 		self.assertTrue(disclosure_page.has_d_less())
# 		self.assertTrue(disclosure_page.has_d_notify())

# 		# send, clear confirmation dialog, verify entry
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and checkout entry
# 		self.assertTrue(eHome.on(True))
# 		eHome.clear_confirmation_dialog()

# 		# Note: Sends instantly when WingCash stands in as bank API.
# 		# Note: Just wait for transaction to complete. Skipping next block of code
# 		# should initially be 'sending'
# 		# data = eHome.get_transaction()
# 		# self.assertEqual(data['amount'], '-' + str(usd_total))
# 		# self.assertEqual(data['recipient'], recip)
# 		# self.assertEqual(data['icon'], 'spinner')
# 		# self.assertEqual(data['status'], 'Sending')

# 		# wait to complete and verify success
# 		self.assertTrue(eHome.transaction_completes())
# 		self.assertTrue(eHome.on(True))
# 		data = eHome.get_transaction()
# 		self.assertEqual(data['amount'], '-' + str(usd_total))
# 		self.assertEqual(data['recipient'], recip)
# 		self.assertEqual(data['icon'], 'check')
# 		self.assertEqual(data['status'], 'Completed')

# 	def test_instant_success(self):
# 		"""send : MXInstant .                                instant_success"""
# 		# Can send to MX account instantly. Entry looks as expected
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount, select instant, send
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		mxn_amount = send_page.get_mxn()
# 		send_page.set_speed('instant')
# 		send_page.click_continue()

# 		# continue through disclosure page
# 		self.assertTrue(disclosure_page.on())
# 		usd_total = disclosure_page.get_transfer_total()
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and confirm entry data is expected
# 		self.assertTrue(eHome.on(True))
# 		eHome.clear_confirmation_dialog()

# 		self.assertTrue(eHome.transaction_completes())
# 		self.assertTrue(eHome.on(True))
# 		data = eHome.get_transaction()
# 		self.assertEqual(data['amount'], '-' + usd_total)
# 		self.assertEqual(data['recipient'], recip)
# 		self.assertEqual(data['icon'], 'check')
# 		self.assertEqual(data['status'], 'Completed')

# 		# checkout td page
# 		eHome.click_transaction()

# 		self.assertTrue(td_page.on())

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_instant_td(self):
# 		"""send : MXInstant .                                     instant_td"""
# 		# Transfer entry behaves as expected for instant MX transfer
# 		eHome = self.cheeks.eHome_page
# 		recip_page = self.cheeks.recipient_page
# 		send_page = self.cheeks.send_page
# 		td_page = self.cheeks.td_page

# 		# Login and select Lourdes Ortega
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		self.assertTrue(eHome.on())
# 		eHome.send_money()

# 		self.assertTrue(recip_page.on())
# 		recip = 'Lourdes Ortega'
# 		recip_page.click_recipient(recip)

# 		# generate random US amount, set speed, and send
# 		self.assertTrue(send_page.on())
# 		usd_amount = self.cheeks.generate_amount()
# 		send_page.set_usd(usd_amount)
# 		send_page.set_speed('instant')
# 		send_page.click_continue()

# 		# continue through disclosure page
# 		self.assertTrue(disclosure_page.on())
# 		disclosure_page.click_continue()

# 		# clear confirmation dialog and checkout td page
# 		self.assertTrue(eHome.on(True))
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.transaction_completes())
# 		self.assertTrue(eHome.on(True))
# 		eHome.click_transaction()

# 		# td page icon matches, does not have 30 min window functionality
# 		self.assertTrue(td_page.on())
# 		time.sleep(.5)
# 		self.assertEqual('check', td_page.read_transaction_icon())
# 		self.assertEqual(td_page.send_now_button, None)
# 		self.assertEqual(td_page.cancel_button, None)
# 		td_page.click_continue()

# 		self.assertTrue(eHome.on())

# class TestUS(unittest.TestCase):
# 	def setUp(self):
# 		self.driver = browser.start(main.get_env(),main.get_browser())
# 		self.cheeks = profiles.Profile(self.driver,'cheeks')
# 		self.nicol = profiles.Profile(self.driver,'nicol')

# 	def tearDown(self):
# 		self.driver.quit()

# 	def test_navigation(self):
# 		"""send : US .              test_navigation"""
# 		# Check back button and steps for all pages in send flow
# 		eHome = self.cheeks.eHome_page
# 		send_to_bank = self.cheeks.send_to_bank_page
# 		td_page = self.cheeks.td_page
# 		recip = 'David Castillo'

# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		eHome.send('bank')
# 		self.assertTrue(send_to_bank.on())
# 		# SendToBank goes back to eHome
# 		send_to_bank.header.click_back()
# 		self.assertTrue(eHome.on('send'))
# 		eHome.send('bank')
# 		self.assertTrue(send_to_bank.on())
# 		# Cannot skip ahead to steps 1 or 2
# 		send_to_bank.set_step(1, reloadPage=False)
# 		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
# 		send_to_bank.set_step(2, reloadPage=False)
# 		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
# 		send_to_bank.click_account(recip, 0)

# 		# Amount step: cannot go to step 3
# 		send_to_bank.set_step(2, reloadPage=False)
# 		self.assertTrue(send_to_bank.on([1, 'Specify Amount']))
# 		# Can go forward to last 2 steps after setting amount and clicking continue
# 		usd_amount = self.cheeks.generate_amount()
# 		send_to_bank.send_form.set_usd(usd_amount)
# 		send_to_bank.submit_send_form()
# 		self.assertTrue(send_to_bank.on([2, 'Confirm & Send']))
# 		send_to_bank.set_step(0)
# 		send_to_bank.set_step(1)
# 		self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())
# 		send_to_bank.set_step(2)
# 		# check in different order
# 		send_to_bank.set_step(0)
# 		send_to_bank.set_step(2)
# 		send_to_bank.set_step(1)
# 		self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())

# 		# Go back to eHome. Shouldn't be able to skip ahead
# 		send_to_bank.header.click_back()
# 		self.assertTrue(eHome.on())
# 		eHome.send('bank')
# 		self.assertTrue(send_to_bank.on())
# 		send_to_bank.set_step(1, reloadPage=False)
# 		send_to_bank.set_step(2, reloadPage=False)
# 		self.assertEqual([0, 'Choose Account'] , send_to_bank.stepper.get_current_step())

# 	@unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	def test_no_balance(self):
# 		"""send : US .                                            no_balance"""
# 		# trying to send w/ no balance works as expected
# 		lobby_page = self.nicol.lobby_page
# 		eHome = self.nicol.eHome_page
# 		send_to_bank = self.nicol.send_to_bank_page
# 		recip = 'Lourdes Ortega'

# 		self.assertTrue(self.nicol.login(self.driver), messages.login)
# 		self.assertTrue(lobby_page.on())
# 		lobby_page.menu.set_role('employee')

# 		self.assertTrue(eHome.on())
# 		# menu should be closed on mobile
# 		if not main.is_desktop():
# 			self.assertFalse(eHome.menu.is_drawer_visible())
# 		eHome.send('bank')
# 		self.assertTrue(send_to_bank.on())
# 		self.assertEqual([0, 'Choose Account'], send_to_bank.currentStep)
# 		send_to_bank.click_account(recip, 'Wells Fargo Bank')


# 		# Step 2 - Set amount, check for balance error
# 		self.assertEqual([1, 'Specify Amount'], send_to_bank.currentStep)
# 		usd_amount = self.nicol.generate_amount()
# 		self.assertFalse(send_to_bank.send_form.is_form_enabled())
# 		self.assertTrue(send_to_bank.send_form.has_balance_error())
# 		send_to_bank.send_form.set_usd(usd_amount)
# 		self.assertTrue(send_to_bank.send_form.has_balance_error())
# 		send_to_bank.send_form.try_clear_balance_error()
# 		self.assertFalse(send_to_bank.send_form.has_balance_error())

# 	def test_us_success(self):
# 		"""send : US .                                       us_send_screens"""
# 		#Send and Disclosure pages interact as expected
# 		eHome = self.cheeks.eHome_page
# 		send_to_bank = self.cheeks.send_to_bank_page
# 		td_page = self.cheeks.td_page
# 		recip = 'David Castillo'

# 		# Login and select David Castillo
# 		self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 		eHome.send('bank')
# 		self.assertTrue(send_to_bank.on())
# 		send_to_bank.click_account(recip, 'Wells Fargo Bank')
# 		send_to_bank.set_step('Choose Account')
# 		# send_to_bank.header.click_back()
# 		self.assertTrue(send_to_bank.on([0, 'Choose Account']))
# 		send_to_bank.click_account(recip, 'Zions Bank')

# 		# send page is setup as expected
# 		self.assertFalse(send_to_bank.send_form.is_form_enabled())
# 		self.assertEqual("0", send_to_bank.send_form.get_usd())
# 		balance = send_to_bank.send_form.get_balance()
# 		self.assertEqual(None, send_to_bank.send_form.exchange_rate)

# 		# send page amounts work as expected
# 		usd_amount = self.cheeks.generate_amount()
# 		send_to_bank.send_form.set_usd(usd_amount)
# 		self.assertEqual(usd_amount, send_to_bank.send_form.get_usd())
# 		send_to_bank.submit_send_form()

# 		# disclosure page has everything we expect
# 		# check name and totals
# 		self.assertEqual(recip, send_to_bank.disclosure.get_name())
# 		self.assertEqual(usd_amount, send_to_bank.disclosure.get_transfer_amount())
# 		fee = '0.00'
# 		self.assertEqual(fee, send_to_bank.disclosure.get_transfer_fee())
# 		total = Decimal(usd_amount) + Decimal(fee)
# 		self.assertEqual(str(total), send_to_bank.disclosure.get_transfer_total())

# 		# check exchange rate and disclosures
# 		self.assertEqual(None, send_to_bank.disclosure.get_exchange_rate())

# 		self.assertFalse(send_to_bank.disclosure.has_d_30())
# 		self.assertFalse(send_to_bank.disclosure.has_d_less())
# 		self.assertTrue(send_to_bank.disclosure.has_d_notify())

# 		# send, clear confirmation dialog
# 		send_to_bank.disclosure.click_continue()
# 		self.assertTrue(eHome.on('activity'))
# 		eHome.clear_confirmation_dialog()
# 		self.assertTrue(eHome.on('activity'))

# 		# Check transaction
# 		data = eHome.get_transaction()
# 		self.assertEqual(data['amount'], '-' + usd_amount)
# 		self.assertEqual(data['recipient'], recip)
# 		self.assertEqual(data['icon'], 'clock')
# 		self.assertEqual(data['status'], 'Arriving')

# 		# check td page
# 		eHome.click_transaction()
# 		self.assertTrue(td_page.on())
# 		self.assertEqual('clock', td_page.read_transaction_icon())
# 		self.assertEqual(td_page.send_now_button, None)
# 		self.assertEqual(td_page.cancel_button, None)
# 		td_page.click_continue()

# 		self.assertTrue(eHome.on('activity'))

# 	# def test_us_success(self):
# 	# 	"""send : US .                                            us_success"""
# 	# 	# Can send to US account. Entry is as expected
# 	# 	eHome = self.cheeks.eHome_page
# 	# 	recip_page = self.cheeks.recipient_page
# 	# 	send_page = self.cheeks.send_page
# 	# 	td_page = self.cheeks.td_page

# 	# 	# Login and select David Castillo
# 	# 	self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 	# 	self.assertTrue(eHome.on())
# 	# 	eHome.send_money()

# 	# 	self.assertTrue(recip_page.on())
# 	# 	recip = 'David Castillo'
# 	# 	recip_page.click_recipient(recip)

# 	# 	# generate random US amount and send
# 	# 	self.assertTrue(send_page.on())
# 	# 	usd_amount = self.cheeks.generate_amount()
# 	# 	send_page.set_usd(usd_amount)
# 	# 	send_page.click_continue()

# 	# 	self.assertTrue(disclosure_page.on())
# 	# 	disclosure_page.click_continue()

# 	# 	# clear confirmation dialog and checkout entry
# 	# 	self.assertTrue(eHome.on(True))
# 	# 	eHome.clear_confirmation_dialog()

# 	# 	data = eHome.get_transaction()
# 	# 	self.assertEqual(data['amount'], '-' + usd_amount)
# 	# 	self.assertEqual(data['recipient'], recip)
# 	# 	self.assertEqual(data['icon'], 'clock')
# 	# 	self.assertEqual(data['status'], 'Arriving')

# 	# 	# checkout td page
# 	# 	eHome.click_transaction()
# 	# 	self.assertTrue(td_page.on())
# 	# test_us_success.e2e = True

# 	# @unittest.skipIf(main.get_priority() < 2, "Priority = 2")
# 	# def test_us_td(self):
# 	# 	"""send : US .                                                 us_td"""
# 	# 	# Can send to US account. TD page is as expected
# 	# 	eHome = self.cheeks.eHome_page
# 	# 	recip_page = self.cheeks.recipient_page
# 	# 	send_page = self.cheeks.send_page
# 	# 	td_page = self.cheeks.td_page

# 	# 	# Login and select David Castillo
# 	# 	self.assertTrue(self.cheeks.login(self.driver), messages.login)
# 	# 	self.assertTrue(eHome.on())
# 	# 	eHome.send_money()

# 	# 	self.assertTrue(recip_page.on())
# 	# 	recip = 'David Castillo'
# 	# 	recip_page.click_recipient(recip)

# 	# 	# generate random US amount and send
# 	# 	self.assertTrue(send_page.on())
# 	# 	usd_amount = self.cheeks.generate_amount()
# 	# 	send_page.set_usd(usd_amount)
# 	# 	send_page.click_continue()

# 	# 	self.assertTrue(disclosure_page.on())
# 	# 	disclosure_page.click_continue()

# 	# 	# clear confirmation dialog and checkout entry
# 	# 	self.assertTrue(eHome.on(True))
# 	# 	eHome.clear_confirmation_dialog()
# 	# 	data = eHome.get_transaction()
# 	# 	# will be USD amount after wingcash updates
# 	# 	self.assertEqual(data['amount'], '-' + usd_amount)
# 	# 	self.assertEqual(data['recipient'], recip)
# 	# 	self.assertEqual(data['icon'], 'clock')
# 	# 	self.assertEqual(data['status'], 'Arriving')

# 	# 	# td page icon matches, does not have 30 min window functionality
# 	# 	eHome.click_transaction()
# 	# 	self.assertTrue(td_page.on())
# 	# 	self.assertEqual('clock', td_page.read_transaction_icon())
# 	# 	self.assertEqual(td_page.send_now_button, None)
# 	# 	self.assertEqual(td_page.cancel_button, None)
# 	# 	td_page.click_continue()

# 	# 	self.assertTrue(eHome.on())

