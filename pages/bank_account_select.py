from page import Page
from components import menu
from components import header
import main
import time
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, TimeoutException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# page for selecting/editing list of bank accounts (personal or recipient)

class BankAccountSelectPage(Page):
	url_tail = '/select-dest' #i.e. 'recipient/041d0651/select-dest'

	def load(self):
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def load_body(self):
		self.accounts = (
			self.driver.find_elements_by_class_name('accountDiv'))
		self.cashout_locations = (
			self.driver.find_elements_by_class_name('locationDiv'))
		self.try_load_icons()
		identifier = 'add_account_button'
		self.add_button = self.driver.find_element_by_class_name(identifier)

	def try_load_icons(self):
		# 'accountIcon' divs should be children of <li>
		# think we need to upgrade to react 16 to implement this.

		# In meantime...
		# Load div containing edit icons for each account
		# Return list of <a> elements (1 in each container)
		# use self.icons[i] to get edit button of destination[i]

		# Edit buttons for bank accounts
		self.i_conts = self.driver.find_elements_by_class_name('accountIcon')
		self.account_icons = [None]*len(self.i_conts)
		for i, cont in enumerate(self.i_conts):
			self.account_icons[i] = cont.find_element_by_tag_name('a')

		# Delete buttons for cashout locations
		self.location_conts = self.driver.find_elements_by_class_name('locationIcon')
		self.location_icons = [None]*len(self.location_conts)
		for i, cont in enumerate(self.location_conts):
			self.location_icons[i] = cont.find_element_by_tag_name('button')

	def num_accounts(self):
		return len(self.accounts)

	def num_cashout_locations(self):
		return len(self.cashout_locations)

	def num_destinations(self):
		return len(self.accounts) + len(self.cashout_locations)

	def get_destination(self, destination_type, identifier):
		# Given type and index of destination, return destination element
		# also return destination icon
		locations = self.accounts
		icons = self.account_icons
		if destination_type == 'cash':
			locations = self.cashout_locations
			icons = self.location_icons
		if type(identifier) is int:
			print(locations[identifier])
			return {
				'destination': locations[identifier],
				'icon': icons[identifier],
			}

			# if destination_type == 'bank':
			# 	return self.accounts[identifier]
			# else:
			# 	return self.cashout_locations[identifier]
		else:
			for i, dest in enumerate(locations):
				text = locations[i].text
				if identifier in text:
					print(locations[i])
					return {
						'destination': locations[i],
						'icon': icons[i],
					}
		return None

	# Need to update how <li> is being rendered.
	# Use destination index to grab right account/location_icons for now
	# def edit_destination(self, destination):
	# 	# Given destination element, find and click edit button (<a> element)
	# 	try:
	# 		# 'accountIcon' isn't child of destination element. Need to grab parent.
	# 		# print('type: ' + str(type(destination)))
	# 		# Have dev/Andrew move accountDiv class off the <li> and onto the parent div?
	# 		parent = self.driver.execute_script("arguments[0].parentNode;", destination) #Doesn't work on windows.
	# 		print(parent)
	# 		el = parent.find_element_by_class_name('accountIcon')
	# 		edit_button = el.find_element_by_tag_name('a')
	# 		self.move_to_el(edit_button)
	# 	except NoSuchElementException:
	# 		print('Unable to click edit button for destination')

	def select_destination(self, destination_type, identifier, action='select'):
		# Get destination then click on destination oredit icon depending on action
		# if type(identifier) is int:
		# 	account_index = identifier
		# else:
		# 	account_index = self.get_destination_index(identifier)

		destination = self.get_destination(destination_type, identifier)
		if destination is None:
			print('could not find destination. identifier={id} action={act}'.format(id=identifier,act=action))
		elif action == 'select':
			self.move_to_el(destination['destination'])
		elif action == 'edit':
			# Will delete cashout location
			self.move_to_el(destination['icon'])

			if destination_type == 'cash':
				# need to complete dialog before deleting cashout
				self.load_remove_cashout_dialog()

	def click_add(self):
		self.scroll_to_bottom()
		self.add_button.click()

	def load_remove_cashout_dialog(self):
		# Wait until buttons show up
		try:
			WDW(self.driver, 3).until(lambda x : EC.element_to_be_clickable(
	      (By.CLASS_NAME, 'okButton')))

			self.okButton = self.driver.find_element_by_class_name('okButton')
			self.cancelButton = self.driver.find_element_by_class_name('cancelButton')
		except TimeoutException:
			print('Could not load remove cashout dialog')
			self.okButton = None
			self.cancelButton = None

	def remove_cashout_location(self, action='delete'):
		# Assumes destination was already 'edited' and dialog loaded
		if action == 'delete':
			self.okButton.click()
			# wait for destination to disappear

		else:
			self.cancelButton.click()
		# not sure we need to reload if we didn't delete cashout
		self.load()

