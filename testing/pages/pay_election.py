from page import Page
from components import menu
from components import header
import main
import time
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PayElectionPage(Page):
  url_tail = 'election'
  dynamic = False

  def load(self):
    try:
      # may need WDW for total element (seems like elections load a little slower)
      self.load_body()
      self.menu = menu.SideMenu(self.driver, True)
      self.header = header.PrivateHeader(self.driver,'Pay Election')
      return True
    except (NoSuchElementException, StaleElementReferenceException,
      IndexError) as e:
      return False

  def load_body(self):
    self.form = self.driver.find_element_by_tag_name('form')
    self.table = self.form.find_element_by_tag_name('table')
    time.sleep(.4) # Need wait otherwise it thinks there's 0 employers
    self.total = self.try_load_total()
    self.employers = self.driver.find_elements_by_class_name('election_entry')
    self.save_button = self.form.find_element_by_class_name('primaryButton')
    self.history_button = self.try_load_history_button()
    # print('election entries: ' + str(len(self.employers)))

  def try_load_total(self):
    # Won't have total if user only has 1 business
    # Note: Need to load after small sleep. (page defaults to showing total)
    try:
      return self.driver.find_element_by_class_name('election_total')
    except NoSuchElementException:
      return None

  def try_load_history_button(self):
    # History button not present when responding to invitation for new user
    try:
      return self.form.find_element_by_tag_name('a')
    except NoSuchElementException:
      return None

  def num_employers(self):
    return len(self.employers)

  def get_employer_row(self,employer):
    # Given employer name or index in table, return <tbody> el from table
    try:
      if self.num_employers() == 1:
        return self.employers[0]
      elif type(employer) == int:
        return self.employers[employer]
      else:
        for row in self.employers:
          row_employer = row.find_element_by_tag_name("span").text
          if row_employer == "From " + employer:
            return row
    except NoSuchElementException:
      pass
    return None

  def set_focus_on_employer(self, employer_row):
    # Given employer_row, click right element to set focus

    # html is different for single vs multiple employers
    if self.num_employers() == 1:
      tr = employer_row.find_elements_by_tag_name('tr')[0]
    else:
      tr = employer_row.find_elements_by_tag_name('tr')[1]
    div = tr.find_elements_by_tag_name('div')[1]
    div.click()

  def get_election_amount(self, employer_row):
    # Given employer_row, return current amount
    # Use get_election_total() for returning total amount

    # html is different for single vs multiple employers
    if self.num_employers() == 1:
      tr = employer_row.find_elements_by_tag_name('tr')[0]
    else:
      tr = employer_row.find_elements_by_tag_name('tr')[1]
    div = tr.find_elements_by_tag_name('div')[2]
    return div.text

  def get_election_total(self):
    # requires multiple employers
    # return text of div in last employer row
    return self.total.find_element_by_tag_name('td').text

  def get_election_status(self, employer_row):
    """Return whether election is 'pending' or not"""
    try:
      # should have div w/ class and color should be blue
      el = employer_row.find_element_by_class_name('pending_election')
      color = el.value_of_css_property('color')
      expected_color = 'rgba(56, 217, 244, 1)' # chrome
      if color == expected_color:
        return True
      return False
    except NoSuchElementException:
      return False

  def clear_pay_election(self, employer_row):
    # set focus and clear out existing election for given employer row el
    self.set_focus_on_employer(employer_row)
    amount = self.get_election_amount(employer_row)
    # desktop: hit backspace until input clear
    if main.is_desktop():
      for i in xrange(len(amount)):
        AC(self.driver).send_keys(Keys.BACKSPACE).perform()
    else: # Mobile: hit backspace on custom keyboard
      self.clear_currency(amount)

  def set_election(self, employer, amount):
    employer_row = self.get_employer_row(employer)
    if employer_row is not None:
      self.clear_pay_election(employer_row)
      # should still be focused
      if main.is_desktop():
        AC(self.driver).send_keys(amount).perform()
      else:
        self.enter_currency(amount)

  def get_elections(self):
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'election_entry')))
    num_employers = self.num_employers()
    elections = {}
    if (num_employers == 1):
      name = self.driver.find_element_by_tag_name("strong").text
      # emp_input = self.table_rows[0].find_element_by_tag_name('input')
      elections[name] = self.get_election_amount(self.employers[0])
      elections[name + ' pending'] = self.get_election_status(self.employers[0])
      elections["total"] = None
    else:
      for i in xrange(num_employers):
        name = self.employers[i].find_element_by_tag_name('span').text[5:]
        elections[name] = self.get_election_amount(self.employers[i])
        elections[name + ' pending'] = self.get_election_status(self.employers[i])

      # get total from last row in self.employers
      self.load()
      elections['total'] = self.get_election_total()
    return elections

  def click_save(self):
    self.save_button.click()
    # might be going to history page, or account page (/main-election)
    # WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'election')))
    WDW(self.driver, 10).until(lambda x:
      EC.presence_of_element_located((By.CLASS_NAME, 'election')) or
      EC.element_to_be_clickable((By.ID, 'cash-bar'))
    )

  def click_history(self):
    self.history_button.click()

