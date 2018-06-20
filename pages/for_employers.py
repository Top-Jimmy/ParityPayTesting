# coding: utf-8
from page import Page
import time
import main
from components import header
from components import footer
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, TimeoutException)
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ForEmployersPage(Page):
  url_tail = 'enroll-business' # Now home page. '' will work
  dynamic = False

  def load(self):
    try:
      WDW(self.driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'form-control')))
      self.load_body()
      self.header = header.PubHeader(self.driver)
      self.footer = footer.PubFooter(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self):
    find_by = self.driver.find_element_by_class_name
    self.learn_more_button = find_by('learnMoreButton')
    self.load_employer_enroll_form() # form towards top of page
    self.load_demo_request_form() # form towards bottom of page
    self.load_page_buttons()

  def load_employer_enroll_form(self):
    self.employer_enroll_form = (
      self.driver.find_element_by_class_name('emp_enroll'))

    find_by = self.employer_enroll_form.find_element_by_tag_name
    self.employer_enroll_input = find_by('input')
    self.employer_enroll_button = find_by('button')

  def load_demo_request_form(self):
    self.demo_request_form = (
      self.driver.find_element_by_class_name('enrollCont'))

    find_by = self.demo_request_form.find_element_by_tag_name
    self.demo_request_input = find_by('input')
    self.demo_request_button = find_by('button')

  def load_page_buttons(self):
    """3 buttons that redirect to employers page, 2 go to about page"""
    find_by = self.driver.find_elements_by_class_name
    # redirects to homepage
    self.employee_button = find_by('employerButton')[0]
    # scrolls up to 1st contact form
    self.enroll_now_button = find_by('employerButton')[1]
    # redirects to about page
    self.about_our_mission_button = find_by('employerButton')[2]

  def click_page_button(self,buttton_num):
    """given num (1,2,3) move to and select appropriate button"""
    el = None
    if button_num == 1:
      el = self.employee_button
    elif button_num == 2:
      el = self.enroll_now_button
    elif button_num == 3:
      el = self.about_our_mission_button

    if el is not None:
      AC(self.driver).move_to_element(el).perform()
      el.click()

  def set_employer_email(self,email):
    AC(self.driver).move_to_element(self.employer_enroll_input).perform()
    self.employer_enroll_input.clear()
    self.employer_enroll_input.send_keys(email)

  def get_employer_email(self):
    return self.employer_enroll_input.get_attribute('value')

  def click_employer_enroll_continue(self):
    AC(self.driver).move_to_element(self.employer_enroll_button).perform()
    self.employer_enroll_button.click()

    # Wait until no longer on page
    try:
      WDW(self.driver, 5).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'form-control')))
    except TimeoutException:
      print("Expected to go to enroll-business/code, still on for employers page")

  def enter_employer_email(self,email):
    self.set_employer_email(email)
    self.click_employer_enroll_continue()

  def set_demo_request_email(self,email):
    AC(self.driver).move_to_element(self.demo_request_input).perform()
    self.demo_request_input.clear()
    self.demo_request_input.send_keys(email)

  def get_demo_request_email(self):
    return self.demo_request_input.get_attribute('value')

  def click_demo_request_continue(self):
    AC(self.driver).move_to_element(self.demo_request_button).perform()
    self.demo_request_button.click()

  def enter_demo_request_email(self,email):
    self.set_demo_request_email(email)
    self.click_demo_request_continue()

  def clear_demo_request_popup(self):
    try:
      el = self.driver.find_element_by_class_name('logout_cancel')
      el.click()
      #time.sleep(.4)
      #WDW(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'demo_email')))
      return True
    except NoSuchElementException:
      return False
