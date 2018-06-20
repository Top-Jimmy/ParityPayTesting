from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
import main
from page import Page
from components import menu
from components import header
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RecipientAddressPage(Page):
  url_tail = '/address' #recipient/539d0002/address
            # or recipient/xxxxxxxx/address-wiz for new mx recipients
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
    self.name = self.driver.find_element_by_tag_name('strong')
    css = 'recip_address_form'
    self.form = self.driver.find_element_by_class_name(css)
    find_by = self.form.find_element_by_id
    self.address1 = find_by('recipient_line1')
    self.address2 = find_by('recipient_line2')
    self.city = find_by('recipient_city')
    self.load_state_dd()
    self.postal = find_by('recipient_code')
    self.continue_button = (
      self.form.find_element_by_class_name('primaryButton'))

  def load_state_dd(self):
    self.state_cont = self.form.find_element_by_class_name('state_dropdown')
    self.state = self.state_cont.find_elements_by_tag_name('div')[3]

  def set_address(self, address, dest_page='dest'):
    self.address1.clear()
    self.address1.send_keys(address[0])
    self.address2.clear()
    self.address2.send_keys(address[1])
    self.city.clear()
    self.city.send_keys(address[2])
    if main.is_android(): # hide keyboard (probably covering state element)
      self.try_hide_keyboard()
    self.select_state(address[3])

    self.postal.clear()
    self.postal.send_keys(address[4])
    self.click_continue()
    # Redirect page could be destination picker (normal) or...
    # send page (US recipient sending to MX bank account or cashout)
    if dest_page == 'send':
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'sourceAmountInput')))
    elif dest_page == 'recipient_view':
      WDW(self.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'recipient_remove')))
    else: # destination page (default)
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'radio_cashout')))

  def get_address(self):
    address = [None]*5
    address[0] = self.address1.get_attribute('value')
    address[1] = self.address2.get_attribute('value')
    address[2] = self.city.get_attribute('value')
    address[3] = self.state.text
    address[4] = self.postal.get_attribute('value')
    return address

  def click_continue(self):
    self.continue_button.click()

  def select_state(self, state):
    self.state.click()
    #WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sm-state-menuitem')))
    time.sleep(1)

    self.try_load_state_els()
    self.state_els[self.get_state_index(state)].click()

    # can't send keys on ios (keyboard not open)
    # If sendKeys is slow will cause issues.
    # Makes it impossible to select state by typing. Click on native
    # load state elements and click desired index
    # if not main.is_web() or main.is_ios():
    #   self.try_load_state_els()
    #   self.state_els[self.get_state_index(state)].click()
    #   # self.state_els[20].click()
    # else:
    #   ActionChains(self.driver).send_keys(state).perform()
    #   ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    #WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'sm-state-menuitem')))
    time.sleep(1)

  # select state by typing keys, then pressing enter
  def type_state(self, state):
    self.state.click()
    ActionChains(self.driver).send_keys(state).perform()
    time.sleep(.4)
    ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    time.sleep(.4)

  def try_load_state_els(self):
    """Only visible when state dropdown is open"""
    try:
      self.state_els = (
        self.driver.find_elements_by_class_name('sm-state-menuitem'))
    except NoSuchElementException:
      self.state_els = None

  def get_state_index(self, state):
    """Get index of desired state in dropdown menu elements"""
    if state.lower() == 'nuevo leon':
      return 18
    elif state.lower() == 'puebla':
      return 20
    elif state.lower() == 'quintana roo':
      return 22
    elif state.lower() == 'sinaloa':
      return 24
    elif state.lower() == 'sonora':
      return 25




