# coding: utf-8
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, TimeoutException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from page import Page
from components import menu
from components import header
import main
import time

class PendingElectionsPage(Page):
  url_tail = 'pending-elections'
  dynamic = False

  def load(self):
    try:
      # Want to avoid scenario where page loads before entries are rendered
      WDW(self.driver, 10).until(lambda x: self.loaded())
      self.load_body()
      self.header = header.PrivateHeader(self.driver)
      self.menu = menu.SideMenu(self.driver, True)
      return True
    except (NoSuchElementException, StaleElementReferenceException,
      IndexError) as e:
      return False

  def load_body(self):
    self.load_contents()
    self.load_toolbar()
    self.load_table()

  def load_contents(self):
    # Empty message loads before loading entries.
    # Give time for entries to load
    time.sleep(.4)
    self.empty_msg = self.try_load_empty_msg()
    self.pending_elections = self.try_load_elections()
    # print('pending elections: ' + str(len(self.pending_elections)))

    # If neither empty_msg and pending_elections loaded, page is not fully loaded
    if self.empty_msg is None and self.pending_elections == []:
      raise NoSuchElementException('Pending Election table not fully loaded')

  def try_load_elections(self):
    try:
      if main.is_desktop():
        self.table = self.driver.find_element_by_tag_name('table')
        self.table_body = self.table.find_element_by_tag_name('tbody')
        return self.table_body.find_elements_by_tag_name('tr')
      else:
        return self.driver.find_elements_by_class_name('table_entry')
    except NoSuchElementException:
      return None

  def try_load_empty_msg(self):
    try:
      return self.driver.find_element_by_class_name('noneMessage')
    except NoSuchElementException:
      return None

  def load_toolbar(self):
    self.toolbar = self.driver.find_element_by_class_name('table_toolbar')
    self.info_icon = self.toolbar.find_element_by_tag_name('svg')
    self.info_span = self.try_load_info_span()

    bg_color = self.toolbar.value_of_css_property('background-color')
    default_color = 'rgba(0, 0, 0'
    if default_color in bg_color:
      self.selected_str = None
      self.process_button = None
    else:
      self.selected_str = (
        self.toolbar.find_elements_by_tag_name('span')[0])
      self.process_button = (
        self.toolbar.find_element_by_tag_name('button'))

  def try_load_info_span(self):
    try:
      return self.toolbar.find_elements_by_tag_name('span')[1]
    except (NoSuchElementException, IndexError) as e:
      return None

  def load_table(self):
    self.load_table_header()
    self.load_table_footer()

  def load_table_header(self):
    try:
      self.table = self.driver.find_element_by_tag_name('table')
      self.table_header = self.table.find_element_by_tag_name('thead')
      self.header_cols = self.table_header.find_elements_by_tag_name('th')
      self.select_all = (
        self.table_header.find_element_by_tag_name('input'))
    except (NoSuchElementException, IndexError) as e:
      # No invitations or on mobile (or on wrong page)
      self.table = None
      self.header_cols = None
      self.select_all = None

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
    """Is information span in header showing?"""
    return True if (self.info_span is not None) else False

  def num_pending_elections(self):
    # returns # on current page, not total
    if self.pending_elections is not None:
      return len(self.pending_elections)

  def table_state(self):
    bg_color = self.toolbar.value_of_css_property('background-color')
    selected_color = 'rgba(56, 217, 244, 1)' # chrome
    # 'rgb(56, 217, 244)'
    if bg_color == selected_color:
      # table has at least 1 pending election selected
      return 'selected'
    return 'default'

  def all_selected(self):
    # only has mass select on desktop
    if main.is_desktop():
      return self.select_all.is_selected()

  def get_num_selected(self):
    """Return # of selected elections according to self.selected_str"""
    if self.table_state() == 'selected':
      return self.selected_str[1:-9] # x2 selected
    return 0

  def get_mobile_row_index(self, row_index):
    # Want to ignore text at beginning of each 'table_entry_row'
    # Given row_index, return starting index for each row
    indexes = [6, 13, 18, 11]
    return indexes[row_index]

  def get_election_info(self, table_entry):
    """Given election entry parse out info"""
    el_input = table_entry.find_element_by_tag_name('input')
    if main.is_desktop():
      # DESKTOP: get info out of each column
      tds = table_entry.find_elements_by_tag_name('td')
      info = {
        'selected': el_input.is_selected(),
        'name': tds[1].text,
        'id': tds[2].text,
        'amount': tds[3].text,
        'routing': tds[4].text,
        'account': tds[5].text,
        'time_requested': tds[6].text
      }
    else:
      # MOBILE: get info out of each row
      rows = table_entry.find_elements_by_class_name('table_entry_row')

      info = {
        'selected': el_input.is_selected(),
        'name': rows[0].text[6:],
        'id': rows[1].text[13:],
        'amount': rows[2].text[18:],
        'routing': rows[3].text[15:],
        'account': rows[4].text[15:],
        'time_requested': rows[5].text[11:],
      }
    # print(str(info))
    return info

  def get_table_entry(self, find_by, identifier):
    # find_by: 'index' or name of column header
    # identifier: index of election or string we try to match in col[find_by]
    if self.empty_msg is None:
      table_entry = None
      if find_by == 'index':
        return self.pending_elections[identifier]
      elif main.is_desktop():
        # Given find_by, get right column.
        # Return entry w/ data in col that matches identifier
        column_index = self.get_column_index(find_by)
        for i, election in enumerate(self.pending_elections):
          tds = election.find_elements_by_tag_name('td')
          if tds[column_index].text == identifier:
            table_entry = self.pending_elections[i]
      else:
        # Given find_by, get right row.
        # Return entry w/ data in row that matches identifier
        row_index = self.get_row_index(find_by)
        for i, election in enumerate(self.pending_elections):
          rows = election.find_elements_by_class_name('table_entry_row')
          index = self.get_mobile_row_index(row_index)
          if rows[row_index].text[index:].lower() == identifier.lower():
            table_entry = self.pending_elections[i]

      if table_entry is not None:
        return table_entry
    return None  # no pending elections or couldn't find w/ given info

  def get_column_index(self, column_text):
    # Desktop: return index of column that matches given text
    for i, column in enumerate(self.header_cols):
      if column_text.lower() == column.text.lower():
        return i
    msg = str(column_text) + " is not a column header (Pending Elections)"
    raise Exception(msg)

  def get_row_index(self, row_text):
    # Mobile: return index of row that matches given text
    rows = ['name', 'employee id', 'requested amount', 'requested']
    for i, row in enumerate(rows):
      if row_text.lower() == rows[i].lower():
        return i
    msg = str(row_text) + " is not a row header (Pending Elections)"
    raise Exception(msg)

  def get_election(self, find_by, identifier, info=True):
    election = self.get_table_entry(find_by, identifier)
    if election is not None and info:
      return self.get_election_info(election)
    return election

############################# Functionality #################################

  def view_history(self):
    if self.table_state() == 'default':
      self.history_link.click()

  def toggle_info(self):
    self.info_icon.click()
    time.sleep(.4)
    self.load()

  def toggle_all(self):
    self.select_all.click()
    self.load()

  def toggle_election(self, find_by='index', identifier=0):
    election = self.get_table_entry(find_by, identifier)
    checkbox = election.find_element_by_tag_name('input')
    if not checkbox.is_selected():
      self.move_to_el(checkbox)
      self.load()

  def select_all_elections(self):
    for i, election in enumerate(self.pending_elections):
      checkbox = election.find_element_by_tag_name('input')
      self.move_to_el(checkbox)
    self.load()

  def mark_all_as_processed(self):
    # If any pending elections...
    # select all and mark as processed
    # Desktop: use mass command.
    # Mobile: select each individually
    if self.empty_msg is None:
      if main.is_desktop() and not self.all_selected():
        self.toggle_all()
      elif not main.is_desktop() and not self.all_selected():
        self.select_all_elections()
      return self.mark_as_processed()
    return True

  def mark_as_processed(self):
    # process currently selected elections
    if self.table_state() == 'selected':
      self.scroll_to_top()
      self.process_button.click()

      # Should stay on page. Reload page
      # if not main.is_desktop():
      #   self.driver.refresh()
      time.sleep(2)
      self.load()
      time.sleep(.4)
      return True
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
    last_index = len(self.footer_buttons) - 1
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

  def loaded(self):
    # Try to find either noneMessage or table entries
    try:
      WDW(self.driver, 8).until(lambda x:
        EC.element_to_be_clickable((By.CLASS_NAME, "noneMessage")) or
        EC.element_to_be_clickable((By.TAG_NAME, "tr"))
      )

      # Wait a second and verify they still exist
      time.sleep(1)
      WDW(self.driver, 8).until(lambda x:
        EC.element_to_be_clickable((By.CLASS_NAME, "noneMessage")) or
        EC.element_to_be_clickable((By.TAG_NAME, "tr"))
      )
      return True
    except TimeoutException:
      # couldn't find either
      return False
