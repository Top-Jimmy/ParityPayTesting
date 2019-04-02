from page import Page
from components import menu
from components import header
import time
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, TimeoutException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ElectionHistoryPage(Page):
  url_tail = 'election-history'
  dynamic = False

  def load(self):
    try:
      # Should not be able to get to this page w/out at least 1 history entry.
      # Load page after at least 1 is clickable
      WDW(self.driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'election')))
      self.elections = self.load_elections()
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      print('true')
      return True
    except (NoSuchElementException, StaleElementReferenceException,
      TimeoutException) as e:
      print('false')
      return False

  def load_elections(self):
    return self.driver.find_elements_by_class_name('election')

  # def get_recent_election(self):
  #     if self.elections != None:
  #         spans = self.elections[0].find_elements_by_tag_name('span')
  #         name = spans[1].text[23:]
  #         amount = spans[2].text[:-4]
  #         election = {
  #             'name': name,
  #             'amount': amount
  #         }
  #         return election

  def get_election(self,index=0):
    if self.elections != None:
      try:
        span = self.elections[index].find_element_by_tag_name('span')
        divs = self.elections[index].find_elements_by_tag_name('div')
        # "Pay Election made with (Dunkin' Donuts)."
        name = divs[3].text[23:-1]
        amount = span.text[:-4]
        election = {
          'name': name,
          'amount': amount
        }
        return election
      except IndexError:
        pass
    return None