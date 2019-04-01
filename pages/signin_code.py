#coding: utf-8
from page import Page
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.keys import Keys
import re
import time
import main
from components import header
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Page for entering confirmation code for EXISTING account

class SigninCodePage(Page):
  url_tail = 'signin/code'
  dynamic = False

  def load(self):
    try:
      self.load_body()
      self.header = header.PubHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      # print('Exception loading signin confirmation')
      return False

  def load_body(self):
    # import pdb; pdb.set_trace()
    h2 = self.driver.find_element_by_tag_name('h2')
    if h2:
      h2 = h2.text
    # if h2 and (h2 != "Let's make sure it's you!" and h2 != 'Vamos a asegurarnos de que eres tú!'):
    # Check your phone!
    if h2 and (h2 != "Check your messages!" and h2 != 'Vamos a asegurarnos de que eres tú!'):  
      print('ERROR: signin_code has an unexpected header!')
      self.fail = self.driver.find_element_by_id('fail')

    self.form = self.driver.find_element_by_tag_name('form')
    self.code_input = self.form.find_element_by_id('code')
    self.remember_checkbox = self.load_checkbox()
    self.continue_button = self.load_continue()
    self.code = self.get_code()
    # self.wrong_number_button = self.driver.find_element_by_name()

  def load_continue(self):
    # native has no continue button
    if main.is_web():
      return self.form.find_element_by_class_name('primaryButton')
    return None

  def load_checkbox(self):
    # No remmeber checkbox on native
    if main.is_web():
      return self.form.find_element_by_id('trust30')
    else:
      return None

  def click_remember(self):
    if main.is_web():
      self.move_to_el(self.remember_checkbox)
      time.sleep(.2)

  def get_code(self):
    time.sleep(.6)
    self.toast = (
      self.driver.find_element_by_id("testSnackId"))

    # some browsers split text into new line. Remove \n for consistency
    code = self.toast.text.replace('\n', '')
    if not main.is_desktop():
      self.try_click_toast()
    # raw_input('code: ' + str(code))

    # Format of code will differ depending on financial platform
    # Sendmi code: "Secret codes (click to dismiss):520-146"
    # Regex: r':[0-9]{3}-[0-9]{3}'
    # Wingcash code: "Secret codes (click to dismiss):443937 => phone:+12024871238"

    if ' => ' in code: # Wingcash
      return code[32:38]
    else:
      return code[32:39]

  def enter_code(self):
    self.scroll_to_bottom()
    self.code_input.clear()
    self.code_input.send_keys(self.code)
    if main.is_ios():
      self.code_input.send_keys('')
    # no continue button on native app
    if main.is_web():
      # WDW fails on Safari. Not sure why.
      if main.get_browser() == 'safari':
        time.sleep(1)
      else:
        WDW(self.driver, 10).until(
          EC.element_to_be_clickable((By.CLASS_NAME, 'primaryButton')))
      self.continue_button.click()

  # def code_accepted(self):
  #   # After entering code, wait until continue button is enabled.
  #   timeout = time.time() + 5
  #   is_enabled = False
  #   while is_enabled is False:
  #     if self.is_enabled(self.continue_button):
  #       is_enabled = True
  #       time.sleep(1)
  #     elif time.time() > timeout:
  #       break
  #     else:
  #       time.sleep(.5)
  #   if not is_enabled:
  #     print('\ncode continue button not enabled!')
  #   return is_enabled

  def try_click_toast(self):
    WDW(self.driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'sm-secret-code')))
    time.sleep(.2)
    try:
      self.driver.find_element_by_class_name("sm-secret-code").click()
    except (NoSuchElementException, WebDriverException) as e:
      pass

