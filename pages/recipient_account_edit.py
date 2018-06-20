from page import Page
from components import menu
from components import header
import time
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RecipientAccountEditPage(Page):
  url_tail = '/edit-account/' #i.e. 'recipient/0b5e5e91/edit-account'
  dynamic = True

  # or /recipient/ce099502/edit-account/0d0e5f99??

  def load(self):
    try:
      self.load_body()
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self):
    #Ensure try_load functions handle ALL their NoSuchElementExceptions
    self.form = self.driver.find_element_by_class_name('account_form')
    self.current_location = self.form.find_element_by_id('account_location')
    self.location_menu = self.form.find_elements_by_tag_name('button')[0]
    self.try_load_mexico()
      # clabe_input
      # what_is_clabe
    self.try_load_us()
      # routing_number
      # account_number
      # checking
      # savings
    self.continue_button = (
      self.form.find_element_by_id('add_account_button'))

  def try_load_us(self):
    self.routing_number = self.try_load_routing()
    self.account_number = self.try_load_account()
    self.try_load_account_type()
      # type_cont
      # checking
      # savings

  def try_load_account_type(self):
    try:
      self.type_cont = self.form.find_element_by_id('account_type')
      find_by = self.type_cont.find_elements_by_tag_name
      self.checking = find_by('input')[0]
      self.savings = find_by('input')[1]
    except NoSuchElementException:
      self.type_cont = None
      self.checking = None
      self.savings = None

  def try_load_routing(self):
    try:
      return self.form.find_element_by_id('account_routing')
    except NoSuchElementException:
      return None

  def try_load_account(self):
    try:
      return self.form.find_element_by_id('account_number')
    except NoSuchElementException:
      return None

  def try_load_mexico(self):
    self.clabe_input = self.try_load_clabe()
    # IDS: need id on what_is_clabe. assuming 1 <a>...
    self.what_is_clabe = self.try_load_what_is_clabe()

  def try_load_clabe(self):
    try:
      return self.form.find_element_by_id('account_clabe')
    except NoSuchElementException:
      return None

  def try_load_what_is_clabe(self):
    try:
      return self.driver.find_element_by_xpath('//a[@href="/what-is-clabe"]')
    except NoSuchElementException:
      return None

  def set_location(self,location):
    self.location_menu.click()
    time.sleep(.4)
    WDW(self.driver, 10).until(EC.visibility_of(self.driver.find_element_by_id('account_location')))
    self.driver.find_element_by_id('account_location').click()
    WDW(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'account_location')))
    if location == "United States":
      self.try_load_us()
    else:
      self.try_load_mexico()

  def set_account_type(self,acct_type):
    if acct_type == 'checking':
      self.checking.click()
    if acct_type == 'savings':
      self.savings.click()
    time.sleep(.2)

  def get_account_type(self):
    acct_type = ""
    bg = "rgba(56, 217, 244, 1)"
    try:
      if self.checking.find_element_by_xpath(
        "..").value_of_css_property("background-color") == bg:
        return "checking"
      elif self.savings.find_element_by_xpath(
        "..").value_of_css_property("background-color") == bg:
        return "savings"
      return None
    except NoSuchElementException:
      return None

  def set_clabe(self,clabe):
    self.clabe_input.clear()
    self.clabe_input.send_keys(clabe)

  def set_account_number(self,number):
    self.account_number.clear()
    self.account_number.send_keys(number)

  def set_routing_number(self,number):
    self.routing_number.clear()
    self.routing_number.send_keys(number)

  def click_what_is_clabe(self):
    self.what_is_clabe.click()

  def click_save(self):
    self.save_button.click()

  def remove_account(self,test=False):
    self.remove_button.click()
    time.sleep(.6)
    text = "Remove"
    if test:
      text = "Cancel"
    xpath = "//button/div/span[text()='" + text + "']"
    self.driver.find_element_by_xpath(xpath).click()

