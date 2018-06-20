from page import Page
from components import menu
from components import header
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait
import time


class AddEmailPage(Page):
  url_tail = 'settings/add-email'
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
    self.email_input = self.form.find_element_by_tag_name('input')
    self.continue_button = self.form.find_element_by_tag_name('button')

  def set_email(self,email):
    self.email_input.clear()
    self.email_input.send_keys(email)

  def get_email(self):
    return self.email_input.get_attribute('value')

  def click_continue(self):
    self.continue_button.click()