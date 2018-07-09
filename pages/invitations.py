# coding: utf-8
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException, TimeoutException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from page import Page
from components import menu
from components import header
import main
import time
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Employer functionality: Table showing pending invitations

class InvitationsPage(Page):
	url_tail = 'invitations'
	dynamic = False

	def load(self):
		try:
			WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table_toolbar')))
			self.load_body()
			self.header = header.PrivateHeader(self.driver)
			self.menu = menu.SideMenu(self.driver, True)
			return True
		except (NoSuchElementException, StaleElementReferenceException,
			IndexError, AttributeError) as e:
			print('exception loading invitations page!')
			return False

	def load_body(self):
		self.empty_msg = self.try_load_empty_msg()
		self.load_toolbar()
		time.sleep(.4)
		self.load_table()

	def try_load_empty_msg(self):
		try:
			return self.driver.find_element_by_class_name('noneMessage')
		except NoSuchElementException:
			return None

	def load_toolbar(self):
		# universal toolbar options
		self.toolbar = self.driver.find_element_by_class_name('table_toolbar')
		self.info_icon = self.toolbar.find_element_by_tag_name('svg')
		self.info_span = self.try_load_info_span()

		bg_color = self.toolbar.value_of_css_property('background-color')
		default_color = 'rgba(0, 0, 0'
		# default_color = 'rgba(0, 0, 0, 0.12)'
		find_by = self.toolbar.find_elements_by_tag_name
		if default_color in bg_color:
			# default toolbar options
			self.add_button = self.toolbar.find_element_by_class_name('send_invitation')
			# selected toolbar options
			self.resend_button = None
			self.delete_button = None
			self.selected_str = None
		else:
			# default toolbar options
			self.add_button = None
			# selected toolbar options
			self.resend_button = find_by('button')[0]
			self.delete_button = find_by('button')[1]
			self.selected_str = find_by('span')[0]

	def try_load_info_span(self):
		try:
			return self.toolbar.find_elements_by_tag_name('span')[1]
		except (NoSuchElementException, IndexError) as e:
			return None

	def load_table(self):
		# only get table header on desktop
		if main.is_desktop():
			self.load_table_header()
		self.load_table_body()
		self.load_table_footer()

	def load_table_header(self):
		# Should only get called on desktop
		try:
			self.table = self.driver.find_element_by_tag_name('table')
			self.table_header = self.table.find_element_by_tag_name('thead')
			self.header_cols = self.table_header.find_elements_by_tag_name('th')
			self.select_all = (
				self.table_header.find_element_by_tag_name('input'))
		except (NoSuchElementException, IndexError) as e:
			# No invitations (or on wrong page)
			self.table = None
			self.table_header = None
			self.select_all = None

	def load_table_body(self):
		if self.table_is_empty():
			# No invitations (or on wrong page)
			self.table_body = None
			self.invitations = None
		elif main.is_desktop():
			# Seems possible to think there's no 'empty_msg' when table is
			self.table_body = self.table.find_element_by_tag_name('tbody')
			self.invitations = self.table_body.find_elements_by_tag_name('tr')
		else:
			self.table_body = None
			self.invitations = self.driver.find_elements_by_class_name('table_entry')

	def load_table_footer(self):
		self.table_footer = self.try_load_footer()
		if self.has_footer():
			self.footer_buttons = self.try_load_footer_buttons()
			self.first_page_button = self.try_load_first_page_but()
			self.last_page_button = self.try_load_last_page_but()

	def try_load_footer(self):
		try:
			return self.driver.find_element_by_id('table_footer')
		except NoSuchElementException:
			return None

	def try_load_footer_buttons(self):
		try:
			return self.table_footer.find_elements_by_tag_name('button')
		except NoSuchElementException:
			return None

	def try_load_first_page_but(self):
		try:
			return self.table_footer.find_element_by_class_name('first_page')
		except NoSuchElementException:
			return None

	def try_load_last_page_but(self):
		try:
			return self.table_footer.find_element_by_class_name('last_page')
		except NoSuchElementException:
			return None

###################### General table info ###############################

	def table_is_empty(self):
		return self.empty_msg is not None

	def is_info_showing(self):
		"""Is information span showing?"""
		return True if (self.info_span is not None) else False

	def num_invitations(self):
		if self.invitations is not None:
			return len(self.invitations)

	def table_state(self):
		bg_color = self.toolbar.value_of_css_property('background-color')
		selected_color = 'rgba(56, 217, 244'
		# color returned by browser can vary. Don't check for exact match
		if selected_color in bg_color:
			# table has at least 1 invitation selected
			return 'selected'
		return 'default'

	def all_selected(self):
		return self.select_all.is_selected()

	def get_num_selected(self):
		"""Return # of selected invitations according to self.selected_str"""
		if self.table_state() == 'selected':
			return self.selected_str[:-9] # 2 selected
		return 0

	def get_mobile_row_index(self, row_index):
	  # Want to ignore text at beginning of each 'table_entry_row'
	  # Given row_index, return starting index for each row

	  # name, employee id, phone number, email, date invited
	  indexes = [6, 13, 14, 7, 14]
	  return indexes[row_index]

	def get_invitation_info(self, table_entry):
	  """Given invitation entry parse out info"""
	  el_input = table_entry.find_element_by_tag_name('input')
	  if main.is_desktop():
	    # DESKTOP: get info out of each column
	    tds = table_entry.find_elements_by_tag_name('td')
	    info = {
	      'selected': el_input.is_selected(),
	      'name': tds[1].text,
	      'id': tds[2].text,
	      'phone': tds[3].text,
	      'email': tds[4].text,
	      'date': tds[5].text
	    }
	  else:
	    # MOBILE: get info out of each row
	    rows = table_entry.find_elements_by_class_name('table_entry_row')

	    info = {
	      'selected': el_input.is_selected(),
	      'name': rows[0].text[6:],
	      'id': rows[1].text[13:],
	      'phone': rows[2].text[14:],
	      'email': rows[3].text[7:],
	      'date': rows[4].text[14:]
	    }
	  # print(str(info))
	  return info

	def get_table_entry(self, find_by, identifier):
	  # find_by: 'index' or name of column header
	  # identifier: index of invitation or string we try to match in col[find_by]
	  if self.empty_msg is None:
	    table_entry = None
	    if find_by == 'index':
	      return self.invitations[identifier]
	    elif main.is_desktop():
	      # Given find_by, get right column.
	      # Return entry w/ data in col that matches identifier
	      column_index = self.get_column_index(find_by)
	      for i, invitation in enumerate(self.invitations):
	        tds = invitation.find_elements_by_tag_name('td')
	        if tds[column_index].text == identifier:
	          table_entry = self.invitations[i]
	    else:
	      # Given find_by, get right row.
	      # Return entry w/ data in row that matches identifier
	      row_index = self.get_row_index(find_by)
	      for i, invitation in enumerate(self.invitations):
	        rows = invitation.find_elements_by_class_name('table_entry_row')
	        index = self.get_mobile_row_index(row_index)
	        if rows[row_index].text[index:].lower() == identifier.lower():
	          table_entry = self.invitations[i]

	    if table_entry is not None:
	      return table_entry
	  return None  # no invitations or couldn't find w/ given info

	def get_column_index(self, column_text):
	  # Desktop: return index of column that matches given text
	  for i, column in enumerate(self.header_cols):
	    if column_text.lower() == column.text.lower():
	      return i
	  msg = str(column_text) + " is not a column header (Invitations)"
	  raise Exception(msg)

	def get_row_index(self, row_text):
	  # Mobile: return index of row that matches given text
	  rows = ['name', 'employee id', 'phone number', 'email', 'date invited']
	  for i, row in enumerate(rows):
	    if row_text.lower() == rows[i].lower():
	      return i
	  msg = str(row_text) + " is not a row header (Invitations)"
	  raise Exception(msg)

	def get_invitation(self, find_by, identifier, info=True):
	  invitation = self.get_table_entry(find_by, identifier)
	  if invitation is not None and info:
	    return self.get_invitation_info(invitation)
	  return invitation

	def click_invitation(self, find_by, identifier):
	 	invitation = self.get_table_entry(find_by, identifier)
	 	if(main.is_desktop() is False):
	 		row = invitation.find_element_by_class_name('table_entry_row')
	 	else:
	 		row = invitation.find_elements_by_tag_name('td')[1]

	 	self.move_to_el(row)
	 	# should be on invitationCard


	############################# Functionality #################################

	def toggle_info(self):
		self.info_icon.click()
		time.sleep(.4)
		self.load()

	def toggle_all(self):
		self.select_all.click()
		self.load()

	def toggle_invitation(self, find_by='index', identifier=0):
		invitation = self.get_table_entry(find_by, identifier)
		if invitation is not None:
			checkbox = invitation.find_element_by_tag_name('input')
			if not checkbox.is_selected():
				self.move_to_el(checkbox)
				self.load()

	def resend_invitations(self):
		# resend currently selected invitations
		if self.table_state() == 'selected':
			self.scroll_to_top()
			self.resend_button.click()
			try:
				WDW(self.driver, 3).until(
					EC.presence_of_element_located((By.CLASS_NAME, 'snackbar')))
			except TimeoutException:
				raise Exception("Resent invitations but could not find snackbar")
			return self.load()
		return False

	def resend_all_invitations(self):
		# resend all invitations
		if not self.all_selected():
			self.toggle_all()
		return self.resend_invitations()

	def delete_invitations(self):
		# delete currently selected invitations
		if self.table_state() == 'selected':
			self.scroll_to_top()
			self.delete_button.click()
			time.sleep(.4)
			return self.load()
		return False

	def delete_all_invitations(self):
		# delete all invitations
		if not self.all_selected():
			self.toggle_all()
		return self.delete_invitations()

	def add_invitation(self):
		if self.table_state() == 'default':
			self.add_button.click()

############################### Toast Functions ###############################

	def get_secret_urls(self):
		WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'testSnackId')))
		#time.sleep(1)
		self.load()
		elem = self.driver.find_elements_by_class_name("sm-secret-code")
		try:
			email_string = elem[0].text
			try:
				email_url = email_string[0:email_string.index(' => ')]
			except ValueError:
				pass
			email = email_string[email_string.index('email:') + 6:]
		except NoSuchElementException:
			email = None
			email_url = None
		try:
			phone_string = elem[1].text
			phone = phone_string[phone_string.index('phone:') + 6:]
			phone_url = phone_string[0:phone_string.index(' => ')]
		except IndexError:
			phone = None
			phone_url = None
		return {'email': email, 'phone': phone, 'email_url': email_url,
			'phone_url': phone_url}

	def click_toast(self):
		if self.has_toast():
			self.toast.click()
			time.sleep(.4)

	def has_toast(self):
		# is toast visible on page?
		try:
			self.toast = self.driver.find_element_by_id('testSnackId')
			return True
		except NoSuchElementException:
			return False

	############################### Footer Functions ##############################

	def has_footer(self):
		return self.table_footer is not None

	def num_footer_buttons(self):
		if self.has_footer():
			return len(self.footer_buttons())

	def index_of_current_page(self):
		# return index of disabled footer button
		if self.has_footer():
			for i, button in enumerate(self.footer_buttons):
				if not button.is_enabled():
					return i

	def current_page(self):
		if self.has_footer():
			cur_index = self.index_of_current_page()
			return int(self.footer_buttons[cur_index].text)
		else:
			return 1

	def go_to_page(self, page):
		# Go to 'first', 'last', or {int} page. Return whether reloading page
		if self.has_footer():
			new_page = True
			if type(page) is int and page != self.current_page():
				new_page = self.go_to_page_number(page)
			elif page == 'first' and self.first_page_button is not None:
				self.scroll_to_bottom()
				self.first_page_button.click()
			elif page == 'last' and self.last_page_button is not None:
				self.scroll_to_bottom()
				self.last_page_button.click()
			else:
				new_page = False
			if new_page:
			   time.sleep(1)
			   return self.load()
		return False

	def go_to_page_number(self, page):
		# Given page#, return whether possible to go to new page or not

		# Can navigate to First/Last by passing in int(page) of first/last page
		for i, button in enumerate(self.footer_buttons):
			text = button.text
			if text == str(page):
				self.scroll_to_bottom()
				button.click()
				time.sleep(1)
				return self.load()
		return False

	def next_page(self):
		# Go to next page and reload. Return False if on last page
		current_index = self.index_of_current_page()
		# raw_input('current_index: ' + str(current_index))
		last_index = len(self.footer_buttons) - 1
		# raw_input('last_index: ' + str(last_index))
		if current_index < last_index:
			self.scroll_to_bottom()
			self.footer_buttons[current_index + 1].click()
			time.sleep(1)
			return self.load()
		return False

	def previous_page(self):
		# Go to previous page and reload. Return false if on 1st page
		current_index = self.index_of_current_page()
		if current_index != 0:
			self.scroll_to_bottom()
			self.footer_buttons[current_index - 1].click()
			time.sleep(1)
			return self.load()
		return False
