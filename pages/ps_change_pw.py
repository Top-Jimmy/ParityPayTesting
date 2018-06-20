from page import Page
from components import menu
from components import header
import time
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class ChangePasswordPage(Page):
  url_tail = 'settings/password'
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
    print('form')
    self.current_pw = self.form.find_element_by_id('current_password')
    print('current')
    self.new_pw = self.form.find_element_by_id('new_password')
    print('new')
    self.password_tips = self.load_pw_tips()
    print('password')
    self.continue_button = self.form.find_element_by_id('submit_button')
    print('done')

  def load_pw_tips(self):
    div = self.form.find_element_by_class_name('password-strength-meter')
    return div.find_element_by_class_name('password_tips')

  def enter_current_pw(self,password):
    self.current_pw.click()
    self.current_pw.clear()
    self.current_pw.send_keys(password)

  def enter_new_pw(self,password):
    self.current_pw.click()
    self.new_pw.clear()
    self.new_pw.send_keys(password)

  def get_current_pw(self):
    return self.current_pw.get_attribute('value')

  def get_new_pw(self):
    return self.new_pw.get_attribute('value')

  def click_continue(self):
    self.continue_button.click()


