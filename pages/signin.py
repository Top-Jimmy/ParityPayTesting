from page import Page
import main
from components import header
from components import signInForm

from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, TimeoutException)
import time
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SigninPage(Page):
  url_tail = 'signin'
  dynamic = False

  def load(self):
    try:
      WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'signin_form_user')))
      self.signInForm = signInForm.SignInForm(self.driver)
      WDW(self.driver, 10).until(lambda x:self.signInForm.load())
      # self.load_body()
      self.header = header.PubHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException, IndexError) as e:
      #print('Exception loading signin page')
      return False
    except TimeoutException:
      return False

  # def load_body(self):
  #   self.form = self.driver.find_element_by_id('signin_form_id')
  #   find_by = self.form.find_element_by_id
  #   self.email_input = find_by('signin_form_user')
  #   self.pw_input = find_by('signin_form_pw')
  #   self.reset_button = find_by('forgot_password')
  #   self.continue_button = find_by('submit_si_button')
  #   self.has_captcha = self.try_load_captcha()

  # def try_load_captcha(self):
  #   # look for text on page. If has captcha, wait like 5 seconds after submit
  #   text = "Bypass CAPTCHA (for testing only)"
  #   captcha = self.number_of_elements_containing("span", text)
  #   if captcha > 0:
  #     return True
  #   return False

  def submit(self, email='', password='', submit=True):
    self.signInForm.submit(email, password, submit)

  def click_password_reset(self):
    self.signInForm.forgot_password()

  # def authenticate(self, email='', password=''):
  #   self.set_email(email)
  #   WDW(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'signin_form_pw')))
  #   self.set_password(password)
  #   WDW(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit_si_button')))
  #   self.click_login()

  # def set_email(self, email):
  #   self.email_input.clear()
  #   self.email_input.send_keys(email)
  #   self.email_input.click()

  # def set_password(self, password):
  #   self.pw_input.clear()
  #   self.pw_input.send_keys(password)
  #   if main.is_ios():
  #     self.pw_input.click()

  # def click_password_reset(self):
  #   if main.is_android(): # may need to close keyboard
  #     self.try_hide_keyboard()
  #   self.reset_button.click()

  def check_captcha(self):
    # Check for captcha checkbox.
    timeout = time.time() + 5
    handledCaptcha = False
    while handledCaptcha is False:
      inputs = self.driver.find_elements_by_tag_name('input')
      if len(inputs) > 2:
        # Too many failed login attempts. Toggle checkbox (input[2]) and resubmit form
        self.move_to_el(inputs[2])
        self.sign_in_submit(None, None)
        handledCaptcha = True
      elif time.time() > timeout:
        break
      else:
        time.sleep(.5)
    return handledCaptcha
