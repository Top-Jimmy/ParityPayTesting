from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, TimeoutException, WebDriverException)
from selenium.webdriver.common.keys import Keys

from page import Page
from components import menu
from components import header
import time
import main
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# name, address, account overview for existing recipient
class RecipientViewPage(Page):
  url_tail = 'view' # i.e. recipient/052a0d0c/view
  dynamic = True

  def load(self):
    try:
      self.load_body()
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self):
    self.buttons = self.driver.find_elements_by_tag_name('button')
    if len(self.buttons) < 5:
      raise NoSuchElementException('not on view page yet')
    self.information_tab = self.buttons[1]
    self.destinations_tab = self.buttons[2]
    self.activity_tab = self.buttons[3]
    self.try_load_information_tab()
    self.try_load_destinations_tab()
    self.try_load_activity()

    # self.send_money_button = (
    #   self.driver.find_element_by_id('send_money_button'))

################ Info tab #####################

  def try_load_information_tab(self):
    """Name and Address, remove recipient button"""
    try:
      # href is first div of 'name' and 'address' classes
      name_div = self.driver.find_element_by_class_name('recipient-name')
      self.name = name_div.find_elements_by_tag_name('div')[0]
      self.remove_recipient_button = (
        self.driver.find_element_by_class_name('recipient_remove'))
      self.try_load_address()
      self.try_load_additional_info()
    except NoSuchElementException:
      self.name = None
      self.remove_recipient_button = None

  def try_load_address(self):
    """Information tab. Grab first div of 'address' class"""
    # might not exist, even on Info tab.
    try:
      address_div = (
        self.driver.find_element_by_class_name('recipient-address'))
      self.address = address_div.find_elements_by_tag_name('div')[0]
    except NoSuchElementException:
      self.address = None

  def try_load_additional_info(self):
    # Shouldn't exist until recipient has BBVA destination
    try:
      additional_div = (
        self.driver.find_element_by_class_name('recipient-additional'))
      self.additional = additional_div.find_elements_by_tag_name('div')[0]
    except NoSuchElementException:
      self.additional = None

  def edit_name(self):
    if self.current_tab() != 'info':
      self.sel_tab('info')
    self.name.click() # Should be on name page

  def edit_address(self):
    if self.current_tab() != 'info':
      self.sel_tab('info')
    self.address.click() # Should be on address page

  def edit_additional_info(self):
    if self.current_tab() != 'info':
      self.sel_tab('info')
    if self.additional is not None:
      self.additional.click() # Should end up on additional info page

  def remove_recipient(self, remove=True):
    if self.current_tab() != 'info':
      self.sel_tab('info')

    self.remove_recipient_button.click()
    time.sleep(.4)
    if remove:
      class_name = 'recip_remove_ok'
      self.driver.find_element_by_class_name(class_name).click()
    else:
      class_name ='recip_remove_cancel'
      self.driver.find_element_by_class_name(class_name).click()




################# Destination Tab ####################

  def try_load_destinations_tab(self):
    # Should only be there if Destination tab is selected
    try:
      self.add_destination_button = (
        self.driver.find_element_by_class_name('add_cashout_button'))
      self.load_bank_accounts()
      self.load_cash_out_locations()
    except NoSuchElementException:
      self.accounts = []
      self.cash_out_locations = []
      self.add_destination_button = None

  def load_bank_accounts(self):
    """May have 0 or more accounts. Accounts Tab. 1st div has href"""
    accts = self.driver.find_elements_by_class_name('recipient-account')
    num_accounts = len(accts)
    self.accounts = [None]*num_accounts
    for i, account in enumerate(accts):
      anchor_el = accts[i].find_element_by_tag_name('div')
      self.accounts[i] = anchor_el

  def load_cash_out_locations(self):
    """May have 0 or more cash out locations. 1st div has href"""
    cashOut_locations = self.driver.find_elements_by_class_name("recipient-cashout")
    num_locations = len(cashOut_locations)
    self.cash_out_locations = [None]*num_locations
    for i, location in enumerate(cashOut_locations):
      anchor_el = cashOut_locations[i].find_element_by_tag_name('div')
      self.cash_out_locations[i] = anchor_el

################### Activity Tab #######################

  def try_load_activity(self):
    """May have 0 or more activity entries"""
    try:
      self.transactions = (
        self.driver.find_elements_by_class_name('history-entry'))
    except NoSuchElementException:
      self.transactions = []





# start destination tab

  def get_destination(self, dest_type, identifier):
    """Get bank account or cash out location by index, or match text"""
    if self.current_tab() != 'destinations':
      self.sel_tab('destinations')

    locations = self.accounts
    if dest_type == 'cash':
      locations = self.cash_out_locations

    if type(identifier) is int:
      return locations[identifier]

    for i, dest in enumerate(locations):
      text = locations[i].text
      if identifier in text:
        return locations[i]
    return None

  def select_destination(self, dest_type, identifier, action='select'):
    if self.current_tab() != 'destinations':
      self.sel_tab('destinations')
    destination = self.get_destination(dest_type, identifier)
    if destination is None:
      print('could not find destination. identifier = {id} action = {act}'.format(id=identifier,act=action))
    # only option on this page is to edit
    self.move_to_el(destination)
    if dest_type == 'cash':
      self.load_remove_cashout_dialog()

  def add_destination(self):
    if self.current_tab() != 'destinations':
      self.sel_tab('destinations')

    self.scroll_to_bottom()
    self.add_destination_button.click()
    WDW(self.driver, 10).until(lambda x : EC.presence_of_element_located(
      (By.ID, 'recipient_second_surname'))
      or EC.presence_of_element_located((By.ID, 'account_clabe'))
    )

  def num_accounts(self):
    # will return 0 if not on destination tab
    return len(self.accounts)

  def num_cashOut(self):
    # will return 0 if not on destination tab
    return len(self.cash_out_locations)

  def load_remove_cashout_dialog(self):
    # Wait until buttons show up
    try:
      WDW(self.driver, 3).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, 'okButton')))

      self.okButton = self.driver.find_element_by_class_name('okButton')
      self.cancelButton = self.driver.find_element_by_class_name('cancelButton')
    except TimeoutException:
      print('Could not load remove cashout dialog')
      self.okButton = None
      self.cancelButton = None

  def remove_cashout_location(self, identifier, action='delete'):
    # Assumes destination was already 'edited' and dialog loaded
    if action == 'delete':
      destination = self.get_destination('cash', identifier)
      dest_delete = destination.find_element_by_tag_name('svg')
      self.move_to_el(dest_delete)
      self.load_remove_cashout_dialog()
      self.okButton.click()
      # wait for destination to disappear
      try:
        WDW(self.driver, 5).until(EC.staleness_of(destination))
      except TimeoutException:
        print("Expected cashout to be deleted. Still there")
      except WebDriverException:
        # element is probably not attached to DOM. Should be good.
        pass
      finally:
        self.load() #always want to reload page?
    else:
      self.cancelButton.click()


# end destination tab
# start general functions

  def go_to_address(self):
    # try to navigate to address url.
    url = self.driver.current_url
    url = url.replace('/view','/address')
    self.driver.get(url)
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'recipient_code')))


  def current_tab(self):
    """Which tab is currently selected? info, destinations, or activity"""
    if self.name is not None:
      return 'info'
    elif self.add_destination_button is not None:
      return 'destinations'
    else:
      return 'activity'

  def sel_tab(self, tab='info'):
    """Select given tab ('info', 'destinations', or 'activity')"""
    if tab.lower() == 'activity':
      self.activity_tab.click()
      # This wait is not sufficient. Transactions load slower than transfer-history
      # Will reload in click_transaction() if they didn't load properly
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'transfer-history')))
      self.load()
    elif tab.lower() == 'destinations':
      self.destinations_tab.click()
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'add_cashout_button')))
      self.load()
    else: # info
      self.information_tab.click()
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'recipient-name')))
      self.load()

  def send_money(self):
    self.send_money_button.click()
    time.sleep(.4)

  #Transaction code is duplicated in account.py

  def click_transaction(self, index=0):
    # Possible to load page before transactions show up
    if len(self.transactions) == 0:
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'history-entry')))
      self.load()

    if main.is_ios():
      el = self.transactions[index].find_elements_by_tag_name('div')[0]
      el.click()
    else:
      self.transactions[index].click()
    WDW(self.driver, 10).until(EC.presence_of_element_located(
      (By.ID, 'transfer_ok_button')))

  def get_transaction(self, index=0):
    # Possible to load page before transactions show up
    if len(self.transactions) == 0:
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'history-entry')))
      self.load()

    transaction = self.transactions[index]
    spans = transaction.find_elements_by_tag_name('span')
    divs = transaction.find_elements_by_tag_name('div')

    info = {
      'amount': self.read_transaction_amount(divs[4].text),
      'recipient': self.read_transaction_recipient(divs[3].text),
      'status': self.read_transaction_status(spans[1].text),
      # 'date': self.read_transaction_date(divs[5].text),
      'icon': self.read_transaction_icon(self.transactions[index])
    }
    return info

  def read_transaction_amount(self, text):
    # print('transaction amount = ' + text)
    return text[:-4]

  def read_transaction_recipient(self, text):
    # to or from recipient?
    if text[:2] == 'To':
      return text[3:]
    else: # from
      return text[5:]

  def read_transaction_status(self, text):
    """Return first word of transaction 'date' string"""

    spaceIndex = text.find(' ')
    if spaceIndex == -1:
      return text
    else:
      return text[0:spaceIndex]

  # def read_transaction_date(self,text):
  #   """Return everything after 1st word in transaction 'date' string"""
  #   return text[text.find(' ')+1:]

  def read_transaction_icon(self, transaction):
    """Interpret length of img src to determine image"""
    try:
      img = transaction.find_element_by_tag_name('img')
      return self.interpret_image(len(img.get_attribute('src')))
    except NoSuchElementException:
      # means there's no img element. Assume it's the spinner.
      return 'spinner'


  def interpret_image(self, img_src_length):
    """Given length of img_src, determine which icon is used"""
    if img_src_length == 1302:
      return 'clock'
    elif img_src_length == 1314:
      return 'check'
    elif img_src_length == 1274:
      return 'x'
    else:
      # raw_input('unexpected img_src_length (account.py)')
      return None
