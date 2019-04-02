import random
import string
import time
import unittest
import main
import browser
import profiles
import messages
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@unittest.skip("No test. No.")
class TestDeviceFarmBasics(unittest.TestCase):
	def setUp(self):
		self.driver = browser.start(main.get_env(),main.get_browser())
		self.cheeks = profiles.Profile(self.driver,'cheeks')

	def tearDown(self):
		self.driver.quit()

	def test_us(self):
		"""farm : DeviceFarmBasics .                                 test_us"""
		acct_page = self.cheeks.account_page
		recip_page = self.cheeks.recipient_page
		send_page = self.cheeks.send_page
		disclosure_page = self.cheeks.disclosure_page
		td_page = self.cheeks.td_page

		# Login and select David Castillo
		self.assertTrue(self.cheeks.login(self.driver), messages.login)
		self.assertTrue(acct_page.on())
		acct_page.send_money()

		self.assertTrue(recip_page.on())
		recip = 'David Castillo'
		recip_page.click_recipient(recip)

		# generate random US amount and send
		self.assertTrue(send_page.on())
		usd_amount = self.cheeks.generate_amount()
		send_page.set_usd(usd_amount)
		send_page.click_continue()

		self.assertTrue(disclosure_page.on())
		disclosure_page.click_continue()

		# clear confirmation dialog and checkout entry
		self.assertTrue(acct_page.on(True))
		acct_page.clear_confirmation_dialog()

		data = acct_page.get_transaction()
		self.assertEqual(data['amount'], '-' + usd_amount)
		self.assertEqual(data['recipient'], recip)

		# US transactions are wonky.
		# self.assertEqual(data['icon'], 'clock')
		# self.assertEqual(data['status'], 'Arriving')

		# checkout td page
		acct_page.click_transaction()
		self.assertTrue(td_page.on())

