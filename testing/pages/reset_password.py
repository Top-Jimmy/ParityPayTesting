from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from page import Page
import page
import main
from components import header
from components import forgotPasswordForm


class ResetPasswordPage(Page):
  url_tail = 'reset-password'
  dynamic = False

  def load(self):
    try:
      self.forgotPWForm = forgotPasswordForm.ForgotPasswordForm(self.driver)
      WDW(self.driver, 10).until(lambda x: self.forgotPWForm.load())
      self.header = header.PubHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def submit(self, email='', submit=True):
    self.forgotPWForm.submit(email, submit)

class ResetPasswordCodePage(Page):
  url_tail = 'reset-password/code'
  dynamic = False

  def load(self):
    try:
      self.load_body()
      self.header = header.PubHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self):
    self.code = self.get_code()
    self.form = self.load_form()
    # Friday: clicking doesn't seem to work (desktop chrome)
    # self.wrong_link = self.form.find_element_by_tag_name('a')
    self.code_input = self.form.find_element_by_tag_name('input')
    # no continue button on native app
    if main.is_web():
      self.continue_button = (
        self.form.find_element_by_class_name('primaryButton'))

  def load_form(self):
    # Desktop: Sign In Form is only visible while open. Just return last form
    forms = self.driver.find_elements_by_tag_name('form') 
    return forms[-1]

  def click_wrong_link(self):
    if not main.is_desktop(): # this works for android web, not sure about native.
      self.scroll_to_top()
    self.wrong_link.click()

  def try_click_toast(self):
    try:
      self.driver.find_element_by_class_name("sm-secret-code").click()
    except NoSuchElementException:
      pass

  def get_code(self):
    time.sleep(.6)
    code = self.driver.find_element_by_id("testSnackId").text
    self.try_click_toast()
    return code[33:39]

  def enter_code(self):
    self.scroll_input_into_view()
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'code')))
    self.code_input.clear()
    self.code_input.send_keys(self.code)
    if main.is_ios():
      self.code_input.click()

    # no continue button on native app
    if main.is_web():
      # Don't try and find primary button: Desktop has signin form
      WDW(self.driver, 6).until(lambda x: self.is_enabled(self.continue_button))
      self.continue_button.click()

  def scroll_input_into_view(self):
    # Mobile: scroll so input in view
    if not main.is_desktop():
      el_bottom = self.get_el_location(self.code_input, 'bottom')
      window_height = self.get_window_height()
      # add 48 for continue button. Extra for ios web footer
      ios_footer = 0
      if main.is_ios() and main.is_web():
        ios_footer = 40
      scroll_distance = el_bottom - window_height + 48 + ios_footer
      self.move('down', scroll_distance)

  def click_continue(self):
    self.continue_button.click()


class ResetPasswordNewPage(Page):
  url_tail = 'reset-password/authenticated'
  dynamic = True  # normally false, ios web keeps seeing something like "shortcode=2200" appended to end

  def load(self):
    try:
      self.header = header.PubHeader(self.driver)
      return self.load_body()
    except (NoSuchElementException, StaleElementReferenceException, WebDriverException) as e:
      print(e)
      return False

  def load_body(self):
    try:
      self.h1 = self.driver.find_element_by_tag_name('h1')
      if self.h1.text != 'New Password':
        print('Not on new password page yet')
        return False
    except NoSuchElementException:
      print('New password page not loaded yet')
      return False
    self.form = self.load_form()
    self.password_input = self.form.find_element_by_tag_name('input')
    self.show_password_but = self.form.find_element_by_id('show_password')
    self.password_tips = self.form.find_element_by_class_name('password_tips')
    self.continue_button = self.form.find_element_by_class_name('primaryButton')
    return True

  def load_form(self):
    # Desktop: Sign In Form is only visible while open. Just return last form
    forms = self.driver.find_elements_by_tag_name('form') 
    return forms[-1]

  def set_password(self, password):
    self.password_input.click()
    self.password_input.clear()
    self.password_input.send_keys(password)

  def click_continue(self):
    self.continue_button.click()

  def enter_password(self,password):
    self.set_password(password)
    self.click_continue()


