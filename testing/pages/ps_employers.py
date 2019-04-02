from page import Page
from components import menu
from components import header
import time
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class EmployerPage(Page):
  url_tail = 'settings/employer/'
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
    self.employer_website = self.driver.find_element_by_tag_name('a')
    self.remove_employer_button = (
      self.driver.find_element_by_class_name('remove_account_button'))
