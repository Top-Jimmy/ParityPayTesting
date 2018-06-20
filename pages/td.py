from page import Page
from components import header
from components import menu
import main
import time
from selenium.common.exceptions import (NoSuchElementException,
  WebDriverException, StaleElementReferenceException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Transfer Details: page shown after sending money

class TransferDetailsPage(Page):
  url_tail = '/sent' #i.e. 'transfer/15717205387'
  dynamic = True

  def load(self, hasPin=False):
    try:
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      self.load_body(hasPin)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self, hasPin):
    # w/in 30 minute window only
    self.send_now_button = self.try_load_send_now()
    self.cancel_button = self.try_load_cancel()
    self.pin = self.try_load_pin(hasPin)

    # alwayus
    self.continue_button = self.driver.find_element_by_id('transfer_ok_button')
    self.icon_type = self.read_transaction_icon()

  def try_load_pin(self, hasPin):
    if hasPin:
      # Force pin to load. Fail loading if it's not there
      return self.driver.find_element_by_class_name('bbva_pin')
    else:
      try:
        return self.driver.find_element_by_class_name('bbva_pin')
      except NoSuchElementException:
        return None

  def try_load_send_now(self):
    try:
      return self.driver.find_element_by_id('send_now_button')
    except NoSuchElementException:
      return None

  def try_load_cancel(self):
    try:
      return self.driver.find_element_by_id('cancel_transfer_button')
    except NoSuchElementException:
      return None

  def read_transaction_icon(self):
    """Interpret length of img src to determine image"""
    img = self.driver.find_elements_by_tag_name('img')[0]
    return self.interpret_image(len(img.get_attribute('src')))

  def interpret_image(self,img_src_length):
    """Given length of img_src, determine which icon is used"""
    if img_src_length == 1302:
      return 'clock'
    elif img_src_length == 1314:
      return 'check'
    elif img_src_length == 1274:
      return 'x'
    else:
      return None

  def get_pin(self):
    if self.pin:
      return self.pin.text

  def click_continue(self):
    self.continue_button.click()

  def send_now(self, action='send'):
    if self.send_now_button is not None:
      self.send_now_button.click()
      time.sleep(.4)
      return self.send_now_dialog(action)

  def send_now_dialog(self,action):
    # True: 'send now' was successful. Should be back on acct page
    # False: unsuccessful or took more than 20 seconds
    try:
      dialog = self.driver.find_element_by_class_name('sendmiDlg')
      if action is not None:
        buttons = dialog.find_elements_by_tag_name('button')
        if action == 'send':
          buttons[1].click()
          WDW(self.driver, 20).until_not(EC.presence_of_element_located((By.ID, 'send_now_button')))
        elif action == 'cancel':
          buttons[0].click()
        # will spin until we hear back from bankaool (~8 seconds)
        # Goes back to acct page when done.
        # Look for element for 20 seconds or until page changes
        '''timeout = time.time() + 25
        while time.time() < timeout:
          try:
            text = self.send_now_button.text
            # sometimes get stale exception
            # sometimes get webdriverException 'unknown server-side error'
          except (WebDriverException, StaleElementReferenceException) as e:
            # probably successful and not on td page anymore
            return True
          if time.time() > timeout:
            # took too long.
            return False
          else:
            time.sleep(.5)'''

        #Clicked cancel or not on td page anymore
        return True
    except NoSuchElementException:
      pass
    # had issues loading/navigating dialog or performing desired action
    return False

  def cancel_transaction(self, action='cancel transfer'):
    if self.cancel_button is not None:
      self.cancel_button.click()
      time.sleep(.4)
      self.cancel_dialog(action)

  def cancel_dialog(self, action):
    try:
      dialog = self.driver.find_element_by_class_name('sendmiDlg')
      if action is not None:
        buttons = dialog.find_elements_by_tag_name('button')
        if action == 'cancel transfer':
          buttons[1].click()
          WDW(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'send_money_button')))
        elif action == 'cancel':
          buttons[0].click()
          #WDW(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'cancel_transfer_button')))
        # should be almost instant
        #time.sleep(1)
    except NoSuchElementException:
      pass






