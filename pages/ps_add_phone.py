from page import Page
from components import menu
from components import header
import time
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class AddPhonePage(Page):
  url_tail = 'settings/add-phone'
  dynamic = False

  def load(self):
    try:
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

  def set_phone(self,phone):
    self.phone_input.clear()
    self.phone_input.send_keys(phone)

  def get_phone(self):
    return self.phone_input.get_attribute('value')

  def click_continue(self):
    self.continue_button.click()
