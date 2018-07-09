from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys

from page import Page
from components import menu
from components import header
import main
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# page for adding/editing recipient
# differences: remove recipient button, text on button different

class RecipientNamePage(Page):
  # url_tail = 'add-recipient' or something like 'recipient/041d0651/edit'

  def load(self, loadDuplicate=False):
    try:
      self.loadDuplicate = loadDuplicate
      self.load_body()
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self):
    if (not self.loadDuplicate):
      self.form = self.driver.find_element_by_class_name('recipient_form')
      find_by = self.form.find_element_by_id
      self.load_location()
      self.first_name = find_by('recipient_first_name')
      self.last_name = find_by('recipient_surname')
      self.second_surname = find_by('recipient_second_surname')
      self.continue_button = find_by("add_recipient")
    else:
      self.load_duplicates()
    # no remove button anymore. Only have remove button on view page

  def load_location(self):
    cont = self.driver.find_element_by_id('country_dropdown')
    self.location = cont.find_elements_by_tag_name('div')[2]

  def load_duplicates(self):
    # Options aren't always there
    self.duplicate_view = self.try_load_duplicate_view()
    self.duplicate_send = self.try_load_duplicate_send()
    self.duplicate_add = self.try_load_duplicate_add()
    self.duplicate_continue = self.try_load_duplicate_continue()

  def try_load_duplicate_view(self):
    try:
      return self.driver.find_element_by_id('dupView')
    except NoSuchElementException:
      return None

  def try_load_duplicate_send(self):
    try:
      return self.driver.find_element_by_id('dupSendNow')
    except NoSuchElementException:
      return None

  def try_load_duplicate_add(self):
    try:
      return self.driver.find_element_by_id('dupAddAccount')
    except NoSuchElementException:
      return None

  def try_load_duplicate_continue(self):
    try:
      return self.driver.find_element_by_id('dupContinue')
    except NoSuchElementException:
      return None

  def click_duplicate_view(self):
    # Go to recipient card
    if self.duplicate_view:
      self.duplciate_view.click()

  def click_duplicate_send(self):
    # Send to existing recipient
    self.duplicate_send.click()

  def click_duplicate_add(self):
    # Add another account to existing recipient
    self.duplicate_add.click()

  def click_duplicate_continue(self):
    # Continue adding a new recipient
    self.duplicate_continue.click()
    # Used to go to address page... Now goes to add destination
    # WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'recipient_code')))
    # WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'radio_account')))

# location functionality

  def set_location(self, country):
    # raw_input('about to set location')
    self.location.click()
    # raw_input('set location')
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'menu-location')))
    #time.sleep(1)
    try:
      dd_cont = self.driver.find_element_by_id('menu-location')
      items = dd_cont.find_elements_by_tag_name('li')
      if country.lower() == "us" or country.lower() == "united states":
        # self.driver.find_element_by_id('location_us').click()
        items[0].click()
      elif country.lower() == "mx" or country.lower() == "mexico":
        # self.driver.find_element_by_id('location_mx').click()
        items[1].click()
    except NoSuchElementException:
      pass
    time.sleep(.4)

  # select country by typing keys, then selecting by pressing enter
  def type_country(self, country):
    # probably won't work on mobile (keyboard not open)
    el = self.location
    if main.is_ios():
      el = self.location.find_element_by_tag_name('button')
    el.click()
    ActionChains(self.driver).send_keys(country).perform()
    time.sleep(.4)
    ActionChains(self.driver).send_keys(Keys.ENTER).perform()
    time.sleep(.4)

  def get_location(self):
    return self.location.text # .split('\n')[1]

# name inputs functionaltiy

  def enter_name(self, name):
    # Convert from string to list
    if not isinstance(name, (list,)):
      name = name.split()
      if len(name) == 2: # Add index for second surname
        name.append('')

    if name[0] is not None:
      self.set_firstname(name[0])
    if name[1] is not None:
      self.set_lastname(name[1])
    if name[2] is not None:
      self.set_surname(name[2])
    self.click_continue()

  def set_firstname(self, text):
    # self.first_name.click()
    self.first_name.clear()
    self.first_name.send_keys(text)
    time.sleep(.2)

  def set_lastname(self, text):
    # self.last_name.click()
    self.last_name.clear()
    self.last_name.send_keys(text)
    time.sleep(.2)

  def set_surname(self, text):
    # self.second_surname.click()
    self.second_surname.clear()
    self.second_surname.send_keys(text)
    time.sleep(.2)

  def remove_recipient(self, remove=True):
    self.remove_button.click()
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'recip_remove_ok')))
    if remove: # click ok
      css = 'recip_remove_ok'
      self.driver.find_element_by_class_name(css).click()
    else:   # click cancel
      css = 'recip_remove_cancel'
      self.driver.find_element_by_class_name(css).click()
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'add_recipient_button')))
    #time.sleep(1)

  def click_continue(self):
    self.continue_button.click()
    WDW(self.driver, 10).until(lambda x : EC.presence_of_element_located(
      (By.ID, 'recipient_code'))
    or EC.presence_of_element_located((By.ID, 'dupContinue'))
    )
    #time.sleep(1)
    # look for duplicate form or address form
    # call try_load_duplicates after clicking continue to get duplicates


