from page import Page
import main
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from components import header

class WhyEmailPage(Page):
  url_tail = "why-personal-email-public"

  def load(self):
    try:
      self.header = header.PubHeader(self.driver)
      # Will be 2 if Sign In form is open on desktop
      primaryButtons = self.driver.find_elements_by_class_name('primaryButton')
      if len(primaryButtons) > 1:
        self.continue_button = primaryButtons[1]
      else:
        self.continue_button = primaryButtons[0]
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def click_continue(self):
    """click page's action button and return to enroll process"""
    self.continue_button.click()


class WhyPhonePage(Page):
  url_tail = 'why-phone'

  def load(self):
    try:
      self.header = header.PubHeader(self.driver)
      self.continue_button = self.driver.find_element_by_id('bogus')
      # need to get id for button

      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def click_continue(self):
    """click page's action button and return to enroll process"""
    self.continue_button.click()

class PasswordTipsPage(Page):
  url_tail = 'password-tips'

  def load(self):
    try:
      self.header = header.PubHeader(self.driver)
      self.continue_button = self.driver.find_element_by_id('bogus')
      # need to get id for button

      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def click_continue(self):
    self.continue_button.click()