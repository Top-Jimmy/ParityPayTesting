from page import Page
from components import menu
from components import header
import time
import main
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class EditPhonePage(Page):
  url_tail = 'settings/edit-phone'
  dynamic = True

  def load(self):
    try:
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'edit_tel')))
      self.load_body()
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self):
    self.form = self.driver.find_element_by_tag_name('form')
    self.phone_input = self.form.find_element_by_tag_name('input')
    self.continue_button = self.form.find_element_by_tag_name('button')

    self.remove_phone_button = self.try_load_remove_button()

  def try_load_remove_button(self):
    try:
      return self.form.find_element_by_class_name('remove_number_button')
    except NoSuchElementException:
      return None

  def try_load_remove_popup(self):
    try:
      self.remove_button = (
        self.driver.find_element_by_class_name('remove_ok'))
      self.cancel_button = (
        self.driver.find_element_by_class_name('remove_cancel'))
    except NoSuchElementException:
      self.remove_button = None
      self.cancel_button = None

  def remove_phone(self, attempt=True):
    if self.remove_phone_button != None:
      self.remove_phone_button.click()
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'remove_ok')))
      self.try_load_remove_popup()
      if attempt:
        self.remove_button.click()
      else:
        self.remove_cancel.click()
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'callmi_pin')))


  def set_phone(self,phone):
    self.phone_input.clear()
    self.phone_input.send_keys(phone)
    if main.is_ios():
      self.phone_input.send_keys('')

  def get_phone(self):
    return self.phone_input.get_attribute('value')

  def click_continue(self):
    self.continue_button.click()