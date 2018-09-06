#coding: utf-8
from page import Page
from components import menu
from components import header
import main
import time
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Note: Double WDW needed in load() to ensure email/phone lists load on the page.
#TODO: Add 'prefered language box' and test it's working properly across site/sessions

class SettingsPage(Page):
  url_tail = 'settings'
  dynamic = False

  def load(self):
    try:
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'settings_email')))
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'settings_phone')))
      self.load_body()
      self.menu = menu.SideMenu(self.driver, True)
      self.header = header.PrivateHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException,
      IndexError) as e:
      return False

  def load_body(self):
    self.form = self.driver.find_element_by_tag_name('form')

    self.load_language_selector()

    self.picture_selector = self.form.find_elements_by_tag_name('input')[0]
    self.first_name_input = self.form.find_element_by_id('settings_first_name')
    self.last_name_input = self.form.find_element_by_id('settings_last_name')
    find_els_by = self.form.find_elements_by_class_name
    find_el_by = self.form.find_element_by_class_name
    self.edit_email_buttons = find_els_by('settings_email')
    self.add_email_button = find_el_by('settings_add_email')
    self.edit_phone_buttons = find_els_by('settings_phone')
    self.add_phone_button = find_el_by('settings_add_phone')

    self.employers = self.load_employers()
    self.pin = self.load_pin()

    try:
      self.change_password_button = find_el_by('settings_pw_emp')
    except NoSuchElementException:
      try:
        self.change_password_button = find_el_by('settings_pw')
      except Exception as e:
        raise e
    except Exception as e:
      raise e

  def load_language_selector(self):
    self.language_cont = (
      self.form.find_element_by_class_name('settings_locale'))
    if main.is_ios():
      self.language_selector = (
        self.language_cont.find_elements_by_tag_name('div')[3])
    else:
      self.language_selector = (
        self.language_cont.find_element_by_tag_name('div'))

  def load_employers(self):
    try:
      className = 'settings_employer'
      time.sleep(2)
      return self.form.find_elements_by_class_name(className)
    except NoSuchElementException:
      return None

  def load_pin(self):
    # return 4 digit PIN
    pin_cont = self.driver.find_element_by_id('callmi_pin')
    text = pin_cont.text[:-4]
    return text

  def type_firstname(self,firstname):
    self.first_name_input.clear()
    self.first_name_input.send_keys(firstname)

  def type_lastname(self,lastname):
    self.last_name_input.clear()
    self.last_name_input.send_keys(lastname)

  def edit_email(self, identifier):
    # Seems like these periodically reload. Make sure elements are fresh
    find_els_by = self.form.find_elements_by_class_name
    self.edit_email_buttons = find_els_by('settings_email')
    if type(identifier) is int:
      self.move_to_el(self.edit_email_buttons[identifier])
      # self.edit_email_buttons[identifier].click()
    else:
      email_index = self.get_email_index(identifier)
      # self.edit_email_buttons[email_index].click()
      self.move_to_el(self.edit_email_buttons[email_index])

  def get_email_index(self, identifier):
    for i, email in enumerate(self.edit_email_buttons):
      text = self.edit_email_buttons[i].text
      if text == identifier:
        return i
    return None

  def has_email(self, email_name):
    find_els_by = self.form.find_elements_by_class_name
    self.edit_email_buttons = find_els_by('settings_email')
    for i, email in enumerate(self.edit_email_buttons):
      text = self.edit_email_buttons[i].text
      if text == email_name:
        return True
    return None

  def add_email(self):
    self.move_to_el(self.add_email_button)

  def edit_phone(self, identifier):
    find_els_by = self.form.find_elements_by_class_name
    try:
      self.edit_phone_buttons = find_els_by('settings_phone')
      if type(identifier) is int:
        self.move_to_el(self.edit_phone_buttons[identifier])
      else:
        phone_index = self.get_phone_index(identifier)
        phone_button = self.edit_phone_buttons[phone_index]
        if phone_button is None:
          print('Could not find phone#: ' + str(identifier))
          return False
        self.move_to_el(phone_button)
      return True
    except StaleElementReferenceException:
      return False

  def get_phone_index(self, identifier):
    for i, email in enumerate(self.edit_phone_buttons):
      text = self.edit_phone_buttons[i].text
      if text == identifier:
        return i
    return None

  def has_phone(self, phone_num):
    find_els_by = self.form.find_elements_by_class_name
    self.edit_phone_buttons = find_els_by('settings_phone')
    try:
      for i, phone in enumerate(self.edit_phone_buttons):
        text = self.edit_phone_buttons[i].text
        if text == phone_num:
          return True
      return False
    except StaleElementReferenceException:
      print('personal settings page probably reloaded')
      self.has_phone(phone_num)

  def add_phone(self):
    self.move_to_el(self.add_phone_button)
    # self.add_phone_button.click()

  def num_employers(self):
    self.employers = self.load_employers()
    return len(self.employers)

  def select_employer(self, employer):
    # See test_profile.py:TestPS.test_employers for selecting employers
    pass

  def change_password(self):
    self.scroll_to_bottom()
    self.change_password_button.click()

  def change_language(self, language):
    # via preferred language setting (not header)
    self.language_selector.click()
    WDW(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'settings_en')))
    try:
      if language.lower() == 'english':
        self.driver.find_element_by_class_name('settings_en').click()
      elif language.lower() == 'spanish':
        self.driver.find_element_by_class_name('settings_es').click()
      else:
        # function only accepts english or spanish as arguments
        fail = 1 + "2"
    except NoSuchElementException:
      # couldn't find language options
      fail = 1 + "2"
    WDW(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'settings_en')))
    self.load()
    return True

