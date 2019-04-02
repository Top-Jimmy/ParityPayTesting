# coding: utf-8
from page import Page
import time
import main
from components import header
from components import footer
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, TimeoutException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ForEmployeesPage(Page):
  url_tail = 'enroll-employee'
  dynamic = False

  # waiting: youtube, app store and play store links not created yet
  # waiting: terms/conditions, privacy,faq, contact us are demo pages
  # apply to test_mapping.py
  def load(self):
    try:
      self.load_body()
      self.header = header.PubHeader(self.driver)
      print('header')
      self.footer = footer.PubFooter(self.driver)
      print('footer')
      return True
    except (NoSuchElementException, StaleElementReferenceException,
      IndexError) as e:
      return False

  def load_body(self):
    find_by = self.driver.find_element_by_class_name
    self.learn_more_button = find_by('learnMoreButton')
    self.load_contact_input_forms()
    self.load_page_buttons()

  def load_contact_input_forms(self):
    """2 sets of contact inputs and buttons"""
    self.contact_forms = (
      self.driver.find_elements_by_class_name('home-contact-input'))
    find_by = self.contact_forms[0].find_element_by_tag_name
    self.contact_input1 = find_by('input')
    self.contact_button1 = find_by('button')

    find_by = self.contact_forms[1].find_element_by_tag_name
    self.contact_input2 = find_by('input')
    self.contact_button2 = find_by('button')

  def load_page_buttons(self):
    """1 redirects to employers page, 2 to bottom invite form
      2 go to about page"""
    find_by = self.driver.find_elements_by_class_name
    # enroll business page
    self.employer_but = find_by('employerButton')[0]
    # invite form
    self.contact_form_redirect_button1 = find_by('employerButton')[1]
    self.contact_form_redirect_button2 = find_by('employerButton')[2]
    # about page
    self.how_are_we_unique_button = find_by('employerButton')[3]
    self.about_our_mission_button = find_by('employerButton')[4]

  def click_learn_more(self):
    self.move_to_el(self.learn_more_button)

  def click_page_button(self, button_num):
    """given num (1,2,3,4,5) move to and select appropriate button"""
    el = None
    if button_num == 1:
      el = self.employer_but
    elif button_num == 2:
      el = self.contact_form_redirect_button1
    elif button_num == 3:
      el = self.contact_form_redirect_button2
    elif button_num == 4:
      el = self.how_are_we_unique_button
    elif button_num == 5:
      el = self.about_our_mission_button

    if el is not None:
      self.move_to_el(el)

  def set_contact_email(self, email, form_num=1):
    """given form_num (1,2), move to input and enter email"""
    el = self.contact_input1
    if form_num == 2:
      el = self.contact_input2

    self.move_to_el(el, False)
    el.clear()
    el.send_keys(email)

  def get_contact_email(self):
    # don't think it matters which one you grab (same form)
    return self.contact_input1.get_attribute('value')

  def click_contact_continue(self, form_num=1):
    but = self.contact_button1
    if form_num == 2:
      but = self.contact_button2
    self.move_to_el(but)

    # Wait until no longer on homepage
    try:
      # this element actually exists on homepage and for employers page
      WDW(self.driver, 5).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'home-contact-input')))
    except TimeoutException:
      print("Expected to go to map page, probably still on home page")

  def enter_contact_email(self, email, form_num=1):
    self.set_contact_email(email, form_num)
    self.click_contact_continue(form_num)

  def has_contact_form_error(self):
    # Does home page contact enroll form have expected error text?
    try:
      WDW(self.driver, 5).until(lambda x: self.has_expected_error_text())
      return True
    except TimeoutException:
      return False

  def has_expected_error_text(self):
    error_msg = "Your email address is required to continue"
    el = self.driver.find_element_by_class_name('error_textbox')
    return error_msg in el.text
