from page import Page
from components import header
from components import menu
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import main
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Page for entering confirmation code for updating personal settings. Code has 9 digits

class SettingsConfirmationPage(Page):
  url_tail = 'settings/code'
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
    self.toast = (
      self.driver.find_element_by_class_name("sm-secret-code"))
    self.code = self.read_code()
    self.form = self.driver.find_element_by_tag_name('form')
    self.code_input = self.form.find_element_by_tag_name('input')
    # self.wrong_email_button = self.driver.find_element_by_name()
    if main.is_web(): # no continue button on native
      self.continue_button = self.form.find_element_by_tag_name('button')

  def read_code(self):
    WDW(self.driver, 10).until(
      EC.element_to_be_clickable((By.CLASS_NAME, 'sm-secret-code')))
    code = self.toast.text
    code = code[:6]
    time.sleep(.2)
    self.click_toast()
    return code

  def click_toast(self):
    self.toast.click()
    time.sleep(.4)

  def remember_device(self):
    self.remember_checkbox.click()

  def enter_code(self):
    self.code_input.clear()
    self.code_input.send_keys(self.code)
    if main.is_ios():
      self.code_input.send_keys('')

    # iOS web. appears no need to click continue. Automatically validates after entering 9 digit code 2/20
    # no continue button on native app
    # if main.is_web():
    #   raw_input('about to wait for button to enable')
    #   WDW(self.driver, 10).until(lambda x : self.is_enabled(self.continue_button))
    #   self.continue_button.click()

  def code_accepted(self):
    # After entering code, wait until continue button is enabled.
    WDW(self.driver, 10).until(lambda x : self.is_enabled(self.continue_button))
    return self.is_enabled(self.continue_button)
