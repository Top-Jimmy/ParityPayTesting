from page import Page
from components import menu
from components import header
import main
from navigation import NavigationFunctions as nav

import time
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# page for selecting recipient after clicking 'Send Money' on Account page
# AND 'Recipient' page from menu
class RecipientPage(Page):
  # url_tail = '/select-recipient' or '/recipients'

  def load(self):
    # can't default to looking for hamburger because used for /select-recipient
    # and /recipients
    try:
      self.nav = nav(self.driver)
      self.load_body()
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException,
      IndexError) as e:
      return False

  def load_body(self):
    self.recipients = self.load_recipients()
    try:
      # secondary button (already has recipient)
      self.add_button = (
        self.driver.find_element_by_class_name('add_recipient_button'))
    except NoSuchElementException:
      # primary button (no recipients)
      self.add_button = (
        self.driver.find_element_by_id('add_recipient_button'))

  def load_recipients(self):
    recipients = self.driver.find_elements_by_class_name('recipient')
    fail = recipients[0]
    return recipients

  def get_recipient_by_name(self, name):
    """Return recipient element whos text matches name"""
    # Get div w/ name text. Compare text with given name
    if isinstance(name, (list,)):
      name = ' '.join(name)
    for i, recip in enumerate(self.recipients):
      text = recip.find_elements_by_tag_name('div')[5].text
      # print(text)
      if text == name:
        return recip # self.recipients[i]
    return None

  def get_recipient_by_index(self, index):
    try:
      recip = self.recipients[index]
    except IndexError:
      return None

  def click_recipient(self, identifier, action='send'):
    """Given index or name of recipient, find and click 'send' or 'edit'
      Can only edit on 'recipient select' page
    """
    if action == 'edit':
      self.edit_recipient(identifier)
    else:
      if type(identifier) is int:
        recip = self.get_recipient_by_index(identifier)
      else:
        recip = self.get_recipient_by_name(identifier)
      if recip != None:
        # need to grab recip's first div for ios (one with cursor:pointer)
        if main.is_ios():
          recip = recip.find_elements_by_tag_name('div')[0]
        self.move_to_el(recip)
      else:
        raise Exception("Error: could not find recipient: " + identifier)

  def edit_recipient(self, identifier):
    """Given index or name of recipient, find and click edit button.
      Return if on different page
    """
    if type(identifier) is int:
      recip = self.get_recipient_by_index(identifier)
    else:
      recip = self.get_recipient_by_name(identifier)
    recip_edit_button = recip.find_element_by_tag_name('a')
    self.click_element(recip_edit_button)

  def click_element(self, el):
    """Click given element"""
    if el is None:
      return False
    else:
      self.move_to_el(el)

  def num_recipients(self):
    return len(self.recipients)

  def edit_recipients(self, identifiers):
    # Click recipients that don't contain anything in list of identifiers
    # Return True if a recipient was edited. False if none were
    for recipient in self.recipients:
      text = recipient.find_elements_by_tag_name('div')[5].text
      matchesIdentifier = False
      for identifier in identifiers:
        if identifier in text:
          matchesIdentifier = True
      if not matchesIdentifier:
        # Click so we can delete it
        self.nav.click_el(recipient)
        return True

  def add_recipient(self):
    # ensure add button is visible on page
    self.scroll_to_bottom()
    WDW(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'add_recipient_button')))
    #time.sleep(.4)
    self.add_button.click()
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'recipient_second_surname')))
    #time.sleep(.4)

