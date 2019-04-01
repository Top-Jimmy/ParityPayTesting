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

  def submit(self, email='', password='', submit=True):
    self.signInForm.submit(email, password, submit)

  def click_password_reset(self):
    self.signInForm.forgot_password()
    
  def check_captcha(self):
    # Check for captcha checkbox.
    timeout = time.time() + 5
    handledCaptcha = False
    while handledCaptcha is False:
      inputs = self.driver.find_elements_by_tag_name('input')
      if len(inputs) > 3:
        raw_input('Thinks signin form has more than 3 inputs. captcha?')
        # Too many failed login attempts. Toggle checkbox (input[2]) and resubmit form
        self.move_to_el(inputs[3])
        self.sign_in_submit(None, None)
        handledCaptcha = True
      elif time.time() > timeout:
        break
      else:
        time.sleep(.5)
    return handledCaptcha
