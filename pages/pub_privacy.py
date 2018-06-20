from page import Page
from components import header
from components import menu
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)

# Public page w/ privacy policy (from home page footer)

class PubPrivacyPage(Page):
  url_tail = 'privacy'
  dynamic = False

  def load(self):
    try:
      self.load_body()
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PubHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self):
    self.cont = self.driver.find_element_by_class_name('terms')
    self.iframe = self.cont.find_element_by_tag_name('iframe')