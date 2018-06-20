from page import Page
import main
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 5 Slides users see when they finish invitation process.

class EmployeeWelcomePage(Page):
  url_tail = "employee-welcome"

  def load(self):
    try:
      # Add id to 5 buttons. Nothing else is consistently on page
      # self.skip = self.driver.find_element_by_class_name('welcome-skip')
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def next(self):
    try:
      nextButton = self.driver.find_element_by_class_name('welcome-next')
      self.move_to_el(nextButton)
      time.sleep(.6)
    except NoSuchElementException:
      pass

  def skip(self):
    # Should go to employee home page
    try:
      skip = self.driver.find_element_by_class_name('welcome-skip')
      self.move_to_el(skip)

      # Wait for employeeHome to load (election tab)
      WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'account_balance')))
    except NoSuchElementException:
      pass

  def done(self):
    # Only on last slide
    try:
      done = self.driver.find_element_by_class_name('welcome-done')
      self.move_to_el(done)

      # Wait for employeeHome to load (election tab)
      WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'account_balance')))
    except NoSuchElementException:
      pass