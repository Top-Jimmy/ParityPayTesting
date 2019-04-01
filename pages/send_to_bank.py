
from components import menu
from page import Page
from components import header
from components import stepper
from components import send_form
from components import disclosure
from components import additional_data_form

from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.keys import Keys
import time
import main
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SendToBankPage(Page):
  url_tail = 'send-to-bank'
  dynamic = False

  def load(self, expectedStep=None):
    try:
      self.menu = menu.SideMenu(self.driver, False)
      self.header = header.PrivateHeader(self.driver)
      self.stepper = stepper.Stepper(self.driver)
      self.currentStep = self.stepper.get_current_step()
      # print('loading step: ' + str(self.currentStep[0]))
      if expectedStep and expectedStep != self.currentStep:
        print('Not on expected step. Expected: ' + str(expectedStep) + ', got: ' + str(self.currentStep))
        return False
      self.load_body()
      return True
    except (NoSuchElementException, StaleElementReferenceException,
    IndexError, WebDriverException) as e:
      return False

  def load_body(self):
    if self.currentStep[0] == 0:
      try:
        el = self.driver.find_element_by_id('birthdate')
        self.dob_form = additional_data_form.DOBForm(self.driver)
      except NoSuchElementException:
        self.load_accounts()
    elif self.currentStep[0] == 1:
      self.load_amount()
    elif self.currentStep[0] == 2:
      self.load_confirm()

############################ Step 1: Account ################################

  def load_accounts(self):
    self.load_recipients()
    self.add_account_button = (
      self.driver.find_element_by_class_name('add_recipient_button'))

  def load_recipients(self):
    # Grab recipients and info for their bank accounts
    self.recipUL = self.driver.find_elements_by_class_name('recipAccounts')
    # Should have at least 1. Fail to load page if there aren't any
    fail = self.recipUL[0]

    self.recipients = {}
    try:
      for i, recip in enumerate(self.recipUL):
        name = self.read_recip_name(i)
        bank_accounts = self.recipUL[i].find_elements_by_tag_name('li')
        del bank_accounts[0] # 1st li is header crap
        
        # Bank name, account #, clickable element
        accounts = []
        for i, account in enumerate(bank_accounts):
          divs = bank_accounts[i].find_elements_by_tag_name('div')
          # Desktop web: divs[1]
          # Mobile web: divs[0]
          # Mobile native: ?
          # for i, div in enumerate(divs):
          #   print(div.text)

          if main.is_web():
            text = divs[0].text
          else:
            text = divs[1].text
          info = self.read_account_info(text)

          if main.is_ios():
            info['element'] = divs[0]
          else:
            info['element'] = bank_accounts[i]
          accounts.append(info)
        self.recipients[name] = accounts
    except Exception as ex:
      template = "An exception of type {0} occurred. Arguments:\n{1!r}"
      message = template.format(type(ex).__name__, ex.args)
      raw_input(message)

  def read_recip_name(self, index):
    # Will return '' for user's own accounts
    text = self.recipUL[index].find_elements_by_tag_name('li')[0].text
    # i.e. "Accounts of {name} "
    return text[12:]

  def read_account_info(self, text):
    # Split into bank name and account number
    if text:
      try:
        index = text.index('Account ')
      except ValueError:
        try:
          index = text.index('CLABE ')
        except ValueError:
          raw_input('unable to read account info: ' + str(text))
      return {'bank': text[0:index], 'accountNumber': text[index+8:]}
    else:
      raise Exception("No account info. Passed in wrong div")

  def add_account(self):
    self.scroll_to_bottom()
    self.add_account_button.click()

  def click_account(self, recipientName, accountIdentifier, add_dob=False):
    clicked = False
    if isinstance(recipientName, (list,)):
      recipientName = ' '.join(recipientName)
    try:
      # Use '' to select user's accounts
      recip = self.recipients[recipientName]
      if type(accountIdentifier) is int:
        # send_to_bank.recipients[recip][0]['element'].click()
        recip[accountIdentifier]['element'].click()
      else:
        # Try and match text
        for i, bankName in enumerate(account['bank'] for account in recip):
          if accountIdentifier in bankName:
            self.move_to_el(recip[i]['element'])
            clicked=True
            break
      # Reload page. Should be on next step (unless need to add DOB for MX account)
      if not clicked:
        print('Failed to find/click account')
      if add_dob:
        return self.on([0, 'Choose Account'])
      else:
        return self.on([1, 'Specify Amount'])
    except (IndexError, KeyError) as e:
      return False

  def set_dob(self, dob):
    if self.dob_form:
      self.dob_form.set_info({'dob': dob})
      self.dob_form.click_continue()
      return self.on([1, 'Specify Amount'])

############################ Step 2: Amount ################################

  def load_amount(self):
    # Sending to US banks only right now.
    self.send_form = send_form.SendForm(self.driver)

  def submit_send_form(self, reloadPage=True):
    self.send_form.click_continue()
    if reloadPage:
      self.on([2, "Confirm & Send"])

############################ Step 3: Confirm ################################

  def load_confirm(self):
    self.continue_button = self.driver.find_element_by_id('send_conf_button')
    self.disclosure = disclosure.Disclosure(self.driver)

############################ Stepper functions ################################

  def set_step(self, step, reloadPage=True):
    # Step: either int or text of step
    newStep = self.stepper.click_step(step)
    if reloadPage:
      self.on(newStep)


