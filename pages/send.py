from page import Page
from components import menu
from components import header
import main
import time
from decimal import *
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, TimeoutException)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as AC
from appium.webdriver.common.touch_action import TouchAction as TA
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# 1st page of send process (personal account or to recipients)

class SendPage(Page):
  url_tail = '/send' #i.e. 'recipient/041d0651/send'

  def load(self):
    try:
      self.load_body()
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException) as e:
      return False

  def load_body(self):
    self.form = self.driver.find_element_by_class_name('sendForm')
    self.destinationType = self.load_destination_type()

    if self.destinationType == 'bbva':
      self.try_load_bbva_picker();
    else:
      self.usd_div = self.form.find_element_by_id('sourceAmountInput')
      self.usd_amount = (
        self.form.find_element_by_id('sourceAmountInput_number'))
      self.usd_input = self.form.find_element_by_id('sourceAmountInput_hide')
      self.mxn_div = self.try_load_mxn_div()
      self.mxn_amount = self.try_load_mxn_amount()
      self.mxn_input = self.try_load_mxn_input()
      self.try_load_delivery_speed()

    self.account_balance = (
      self.form.find_element_by_id('accountBalanceDiv'))
    self.exchange_rate = self.try_load_exchange_rate()

    self.destination = self.form.find_element_by_tag_name('a')
    self.continue_button = self.form.find_element_by_id('send_cont_button')

  def load_destination_type(self):
    # Only 2 viable options for now...
    # BBVA: has curency picker
    # US bank: has 2 currency inputs
    try:
      bbvaAmount = self.form.find_element_by_class_name('picker-item-selected')
      return 'bbva'
    except NoSuchElementException:
      return 'us'

  def try_load_bbva_picker(self):
    try:
      if main.is_desktop():
        self.pickerUp = self.form.find_element_by_id('currencyUp')
        self.pickerDown = self.form.find_element_by_id('currencyDown')
      else:
        self.pickerUp = None
        self.pickerDown = None
      self.pickerOptions = self.form.find_elements_by_class_name('picker-item')
      self.bbvaAmount = (
        self.form.find_element_by_class_name('picker-item-selected').text.replace(",", ""))
    except NoSuchElementException:
      self.pickerUp = None
      self.pickerDown = None
      self.pickerOptions = None
      self.bbvaAmount = None

  def try_load_mxn_div(self):
    # only there when sending to MX. Element you click on
    try:
      return self.form.find_element_by_id('destAmountInput')
    except NoSuchElementException:
      return None

  def try_load_mxn_amount(self):
    # only there when sending to MX. Element that has amount as text
    try:
      return self.form.find_element_by_id('destAmountInput_number') #_number
    except NoSuchElementException:
      return None

  def try_load_mxn_input(self):
    # hidden input element. Send keys to this el on desktop
    try:
      return self.form.find_element_by_id('destAmountInput_hide')
    except NoSuchElementException:
      return None

  def try_load_exchange_rate(self):
    # only there when sending to MX
    try:
      self.exchange_cont = (
        self.form.find_element_by_id('exchangeRateDiv'))
      return self.exchange_cont.find_element_by_tag_name('span')
    except NoSuchElementException:
      return None

  def try_load_delivery_speed(self):
    """Look for delivery speed stuff if sending to MX"""
    if self.mxn_div is not None:
      if 'SORIANA' not in self.destination.text:
        if self.toggle_or_radio() == 'radio':
          cont = self.form.find_element_by_id('radio_speed')
          inputs = cont.find_elements_by_tag_name('input')
          self.radio_fast = inputs[0]
          self.radio_instant = inputs[1]
          # self.radio_fast = (
          #   self.form.find_element_by_id('fastRadioButton'))
          # self.radio_instant = (
          #   self.form.find_element_by_id('instantRadioButton'))
        else:
          self.toggle = self.form.find_element_by_id('instantToggle')
      else:
        self.toggle = None

####################### BBVA functions ########################

  def get_picker_item(self, mxnAmount):
    # Return picker-item that corresponds to desired mxnAmount
    # amount must be multiple of 100
    for i, option in enumerate(self.pickerOptions):
      text = option.text.replace(",", "")
      print(text)
      if text == mxnAmount:
        return self.pickerOptions[i]
    return None

  def get_picker_index(self):
    # return index of currently selected item
    for i, option in enumerate(self.pickerOptions):
      classes = option.get_attribute('class')
      if 'picker-item-selected' in classes:
        return i
    return None

  def get_direction(self, desired_amount):
    # is current bbva amount clickable? If not, which direction does picker need to move?
    current_amount = self.form.find_element_by_class_name('picker-item-selected').text
    current_amount = current_amount.replace(",", "") # Strip out commas for Decimal functions

    difference = Decimal(desired_amount) - Decimal(current_amount)
    if (difference >= -200) and (difference <= 200):
      # Desired amount is w/in 200 of current amount. Desired amount should be clickable
      return 'click'
    elif difference > 200:
      # Element not visible. Scroll down
      return 'down'
    else:
      return 'up'

  def move_picker(self, direction):
    if main.is_desktop():
      if direction == 'down':
        self.pickerDown.click()
      else:
        self.pickerUp.click()
    else:
      if direction == 'down':
        self.pickerOptions[self.get_picker_index() + 2].click()
      else:
        self.pickerOptions[self.get_picker_index() - 2].click()


      # Doesn't work. Scrolls screen instead of picker
      # el = self.form.find_element_by_class_name('picker-item-selected')
      # location = el.location
      # size = el.size
      # click_x = str(Decimal(location['x']) + Decimal(size['width'])/2)
      # click_y = str(Decimal(location['y']) + Decimal(size['height'])/2)
      # native_dimensions = self.driver.get_window_size()
      # native_width = native_dimensions['width']
      # if direction == 'down':
      #   TA(self.driver).press(el).wait(
      #     100).move_to(x=0, y=-100).release().perform()
      # else:
      #   TA(self.driver).press(x=click_x, y=click_y).wait(
      #     duration).move_to(x=0, y=100).release().perform()


  def set_bbva_amount(self, mxnAmount):
    # move up or down until amount is clickable
    # amount must be in multiples of 100
    print(mxnAmount)
    if self.destinationType == 'bbva' and mxnAmount != self.bbvaAmount:
      env_type = main.get_env()

      while mxnAmount != self.bbvaAmount:
        direction = self.get_direction(mxnAmount)
        if direction == 'click':
          item = self.get_picker_item(mxnAmount)
          item.click()
        else:
          self.move_picker(direction)

        self.bbvaAmount = (
          self.form.find_element_by_class_name('picker-item-selected').text.replace(",", ""))

  def toggle_or_radio(self):
    """Is UI set to radio buttons or toggle switch?"""
    try:
      el = self.form.find_element_by_id('instantToggle')
      return 'toggle'
    except NoSuchElementException:
      return 'radio'

  def set_speed(self, speed='fast'):
    """Set toggle/radio to given speed"""
    if self.toggle_or_radio() == 'radio':
      self.set_speed_radio(speed)
    else: # toggle
      self.set_speed_toggle(speed)

  def get_speed(self, speed='toggle'):
    """Return speed indicated by radio/toggle"""
    if self.toggle_or_radio() == 'radio':
      return self.get_speed_radio()
    else: # default (toggle)
      return self.get_speed_toggle()

  def set_speed_radio(self, speed):
    # has issues clicking 'invisible' elements on Safari desktop
    if speed == 'instant':
      self.click_el(self.radio_instant)
      # self.radio_instant.click()
    else: # default (fast)
      self.click_el(self.radio_fast)
      # self.radio_fast.click()

  def get_speed_radio(self):
    """Which radio button is selected? Instant or Fast (default)?"""
    if self.radio_instant.get_attribute('checked'):
      return 'instant'
    else:
      return 'fast'

  def set_speed_toggle(self, speed):
    if self.get_speed_toggle() != speed:
      if main.is_ios():
        el = self.toggle.find_element_by_tag_name('input')
        el.click()
      else:
        self.move_to_el(self.toggle)

  def get_speed_toggle(self):
    el = self.toggle.find_element_by_tag_name('input')
    if el.get_attribute('checked'):
      return 'instant'
    else: # default (fast)
      return 'fast'

  def get_balance(self):
    return self.account_balance.text

  def get_exchange_rate(self):
    if self.exchange_rate is not None:
      return self.exchange_rate.text
    return None

  def clear_currency_input(self, currency_type):
    """Clear out amount of given currency_type"""
    # set focus on input
    el = None
    amount = ''
    if currency_type.lower() == 'usd':
      el = self.usd_amount
      amount = self.get_usd()
    elif currency_type.lower() == 'mxn':
      el = self.mxn_amount
      amount = self.get_mxn()

    el.click()

    # Desktop: hit backspace enough times to clear out current amount
    # Mobile: hit backspace (on custom keyboard) enough times to clear
    if main.is_desktop():
      for i in xrange(len(amount)):
        AC(self.driver).send_keys(Keys.BACKSPACE).perform()
    else: # Mobile: hit backspace on custom keyboard
      self.clear_currency(amount)

  def set_usd(self, amount):
    # clear current amount and enter given amount
    self.clear_currency_input('usd')
    if main.is_desktop():
      self.usd_input.send_keys(str(amount))
      # self.usd_div.send_keys(amount)
    else:
      self.enter_currency(amount)

  def set_mxn(self, amount):
    # clear current amount and enter given amount
    self.clear_currency_input('mxn')
    if main.is_desktop():
      self.mxn_input.send_keys(str(amount))
      # self.mxn_div.send_keys(amount)
    else:
      self.enter_currency(amount)

  def get_usd(self):
    return self.usd_amount.text

  def get_mxn(self):
    return self.mxn_amount.text

  def has_balance_error(self):
    """Return if page has 'You have no money to send.' msg"""
    # This text is difficult to parse (react crap and weird ascii chars).
    # Seems to change sometimes. Last updated 11/29
    try:
      self.error = (
        self.form.find_element_by_class_name('alert-dismissable'))
      self.error_button = self.error.find_element_by_tag_name('button')
      if self.error.text[14:] == 'You have no money to send.':
        return True
    except NoSuchElementException:
      pass
    return False

  def try_clear_balance_error(self):
    """If balance error on page, clear by clicking x"""
    if self.has_balance_error():
      # error not visible on mobile
      if not main.is_desktop():
        self.scroll_to_bottom()
      self.error_button.click()
      try:
        self.error_button.click()
      except Exception as e:
        pass
      time.sleep(.6)

  def click_account(self):
    self.destination.click()
    time.sleep(1)

  def get_account_info(self):
    # get div w/ text els. return bank name and clabe text
    acct_div = self.destination.find_elements_by_tag_name('div')[1]
    account_info = {
      'bank': acct_div.find_elements_by_tag_name('div')[0].text,
      'clabe': acct_div.find_elements_by_tag_name('div')[1].text
    }
    return account_info

  # def close_custom_keyboard(self):
  #   if not main.is_desktop():
  #     self.account_balance.click()
  #     time.sleep(.4)

  def click_continue(self):
    try:
      WDW(self.driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'primaryButton')))
    except TimeoutException:
      raise TimeoutException("Send page: Continue button not enabled.")
    self.continue_button.click()
    try:
      WDW(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'send_conf_button')))
    except TimeoutException:
      raise TimeoutException("Send Page: Could not find element on next page.")
    #time.sleep(5) #id = send_conf_button

