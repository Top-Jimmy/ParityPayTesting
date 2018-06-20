from page import Page
import main
from components import menu
from components import header
import time
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class LobbyPage(Page):
	url_tail = 'settings/employer/'
	dynamic = True

	def load(self):
		#raw_input('loading lobby page')
		try:
			self.load_body()
			self.menu = menu.SideMenu(self.driver, True)
			self.header = header.PrivateHeader(self.driver)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError) as e:
		    #print('Exception: ' + str(e))
		    pass
		return False

	def load_body(self):
		self.load_invitations_card()
		#print('loaded invite card')
		self.load_pending_elections_card()
		#print("loaded pening card")
		self.load_employees_card()
		#print('loaded emp card')

		self.cards = [self.invitations_card, self.pending_elections_card,
			self.employees_card]
		self.learn_more = [self.invitations_lm, self.pending_elections_lm,
			self.employees_lm]

		# Probably not on lobby page if there isn't at least 1 card
		card_exists = False
		for card in self.cards:
			if card is not None:
				card_exists = True
		if not card_exists:
			raise NoSuchElementException('No cards found on Lobby page')

	def load_invitations_card(self):
		find_by = self.driver.find_elements_by_class_name
		try:
			self.invitations_card = find_by('card')[0]
			self.invitations_lm = find_by('invitations_card')[0]
		except (NoSuchElementException, IndexError) as e:
			self.invitations_card = None
			self.invitations_lm = None

	def load_pending_elections_card(self):
		find_by = self.driver.find_elements_by_class_name
		try:
			self.pending_elections_card = find_by('card')[1]
			self.pending_elections_lm = find_by('payelections_card')[0]
		except (NoSuchElementException, IndexError) as e:
			self.pending_elections_card = None
			self.pending_elections_lm = None

	def load_employees_card(self):
		find_by = self.driver.find_elements_by_class_name
		try:
			self.employees_card = find_by('card')[2]
			self.employees_lm = find_by('employees_card')[0]
		except (NoSuchElementException, IndexError) as e:
			self.employees_card = None
			self.employees_lm = None

	def click_link(self, link_type='card', index=0):
		"""link_type: 'card', or 'learn_more'.  Index: 0, 1, 2"""

		# card or learn more link?
		if link_type.lower() == 'card':
			l = self.cards
		else:
			l = self.learn_more

		try:
			el = l[int(index)]
		except IndexError:
			raise Exception('Invalid card index')

		# make sure element is in view
		if not main.is_desktop():
			el_bottom = self.get_el_location(el, 'bottom')
			window_height = self.get_window_height()
			scroll_distance = el_bottom - window_height
			self.move('down', scroll_distance)

		# make sure menu is closed on desktop
		if not main.is_desktop():
			self.menu.close()
		el.click()
