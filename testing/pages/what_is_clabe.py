from page import Page
from components import header
from components import menu
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)

# Page for entering confirmation code for EXISTING account

class ClabePage(Page):
  url_tail = 'what-is-clabe'
  dynamic = False

  def load(self):
    try:
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False