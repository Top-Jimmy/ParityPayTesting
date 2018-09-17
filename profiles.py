import credentials
from pages import *
import main
import string
import random
from decimal import *
import time
import sys
import messages
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.common.exceptions import (TimeoutException, NoSuchElementException)

class Profile:
  def __init__(self, driver, name=None):
    self.driver = driver
    self.credentials = credentials.get_credentials(name)
    if name is not None:
      self.businesses = dict([(x, credentials.get_credentials(x)) for x in
                  self.credentials['businesses']])

    # Pages
    # syntax: self.whatever = filename(same as in __init__.py).Classname(driver)
    self.signin_page = signin.SigninPage(driver)
    self.signin_code_page = signin_code.SigninCodePage(driver)
    self.reset_password_page = reset_password.ResetPasswordPage(driver)
    self.reset_password_code_page = (
      reset_password.ResetPasswordCodePage(driver)
    )
    self.reset_password_new_page = (
      reset_password.ResetPasswordNewPage(driver)
    )
    # enroll process (business or responding to invite)
    self.dob_page = invite.DOBPage(driver)
    self.invite_page = invite.InvitePage(driver)

    self.enroll_code_page = enroll_code.EnrollCodePage(driver)
    self.enroll_factor2_page = enroll_factor2.EnrollFactor2Page(driver)
    self.enroll_name_page = enroll_name.EnrollNamePage(driver)
    self.enroll_password_page = enroll_password.EnrollPasswordPage(driver)
    self.enroll_accept_page = enroll_accept.EnrollAcceptPage(driver)
    self.enroll_signin_page = enroll_signin.EnrollSigninPage(driver)

    self.why_email_page = why.WhyEmailPage(driver)
    self.why_phone_page = why.WhyPhonePage(driver)
    self.password_tips_page = why.PasswordTipsPage(driver)

    self.for_employers = for_employers.ForEmployersPage(driver) # Home page
    self.for_employees = for_employees.ForEmployeesPage(driver)
    self.contact_map_page = contact_flow.ContactMapPage(driver)
    self.contact_form_page = contact_flow.ContactFormPage(driver)
    self.about_public_page = about.AboutPublicPage(driver)
    self.about_private_page = about.AboutPrivatePage(driver)
    self.pub_terms_page = pub_terms.PubTermsPage(driver)
    self.pub_privacy_page = pub_privacy.PubPrivacyPage(driver)
    self.add_business_page = add_business.AddBusinessPage(driver)
    self.business_details_page = (
      business_details.BusinessDetailsPage(driver)
    )
    self.business_prefilled_page = (
      business_prefilled.BusinessPrefilledPage(driver)
    )
    self.business_settings_page = (
      business_settings.BusinessSettingsPage(driver)
    )
    self.admin_page = admin.AdminPage(driver)
    self.add_admin_page = admin.AddAdminPage(driver)

    self.employee_welcome = employee_welcome.EmployeeWelcomePage(driver)
    self.account_page = account.AccountPage(driver)
    self.eHome_page = eHome.EHomePage(driver)
    self.account_details_page = account.AccountDetailsPage(driver)
    self.send_to_bank_page = send_to_bank.SendToBankPage(driver)
    self.send_to_atm_page = send_to_atm.SendToATMPage(driver)
    self.send_to_cashout = send_to_cashout.SendToCashoutPage(driver)
    self.recipient_page = recipient.RecipientPage(driver)
    self.recipient_name_page = recipient_name.RecipientNamePage(driver)
    self.recipient_view_page = recipient_view.RecipientViewPage(driver)
    self.recipient_address_page = (
      recipient_address.RecipientAddressPage(driver))
    self.recipient_info_page = (
      recipient_info.RecipientInfoPage(driver))
    self.bank_account_page = bank_account.BankAccountPage(driver)
    self.bank_account_select_page = (
      bank_account_select.BankAccountSelectPage(driver))
    self.send_page = send.SendPage(driver)
    self.td_page = td.TransferDetailsPage(driver)
    self.clabe_page = what_is_clabe.ClabePage(driver)

    self.lobby_page = lobby.LobbyPage(driver)
    self.invitations_page = invitations.InvitationsPage(driver)
    self.invitation_card_page = invitation_card.InvitationCardPage(driver)
    self.pending_elections_page = (
      pending_elections.PendingElectionsPage(driver))
    self.employee_page = employees.EmployeePage(driver)
    self.employee_add_page = employee_add.AddEmployeePage(driver)
    self.employee_add_csv1_page = (
      employee_add_csv.AddEmployeesCSV1Page(driver))
    self.employee_add_csv2_page = (
      employee_add_csv.AddEmployeesCSV2Page(driver))
    self.employee_view_page = employee_view.EmployeeViewPage(driver)

    self.ps_page = personal_settings.SettingsPage(driver)
    self.participate_page = participate.ParticipatePage(driver)
    self.ps_edit_email_page = ps_edit_email.EditEmailPage(driver)
    self.ps_add_email_page = ps_add_email.AddEmailPage(driver)
    self.ps_edit_phone_page = ps_edit_phone.EditPhonePage(driver)
    self.ps_add_phone_page = ps_add_phone.AddPhonePage(driver)
    self.ps_confirmation_page = (
      ps_confirmation.SettingsConfirmationPage(driver))
    self.ps_change_pw_page = ps_change_pw.ChangePasswordPage(driver)
    self.employers_page = ps_employers.EmployerPage(driver)

    self.pay_election_page = pay_election.PayElectionPage(driver)
    self.election_history_page = (
      pay_election_history.ElectionHistoryPage(driver))
    self.contact_us_page = contact_us.ContactPublicPage(driver)
    self.feedback_page = contact_us.ContactPrivatePage(driver)

    # Components
    # self.additional_info = additional_info.AddInfo(driver)

  def login(self, driver, password=None, email=None):
    # Enter credentials
    if (main.is_web() and self.signin_page.go()) or self.signin_page.on():
      if password is None:
        password = self.credentials['password']
      if email is None:
        email = self.credentials['email']
      self.signin_page.submit(email, password)
    else:
      # Couldn't loading signin page
      raise Exception(messages.login_signin)

    # Wait for Sign In Screen to disappear
    try:
      WDW(self.driver, 5).until_not(EC.presence_of_element_located((By.ID, 'signin_form_user')))
    except TimeoutException:
      # Something went wrong on Sign In page
      print('Login: Never left Sign In page')

      print('Login: Looking for Sign In error')
      try:
        WDW(driver, 4).until(
          EC.presence_of_element_located((By.ID, 'sendmi_error')))
        error = self.driver.find_element_by_id('sendmi_error')
        # probably has password error
        print(error.text)
        print(messages.login_error)
        raise Exception(messages.login_error)
      except (TimeoutException, NoSuchElementException) as e:
        # No password error.
        # Captcha checkbox from too many failed login attempts?
        print('Login: No Sign In error. Checking for captcha')
        if self.signin_page.check_captcha():
          print('Login: Found and handled captcha')
          # had too many failed login attempts. Should be on code page now
          # WDW(self.driver, 10).until(lambda x: self.signin_code_page.load())
          # self.signin_code_page.enter_code()
        else:
          # No captcha checkbox. Check if user was remembered and code page was skipped
          try:
            WDW(driver, 8).until(
              EC.presence_of_element_located((By.ID, 'sendmi_appbar')))
          except TimeoutException:
            # Couldn't find header. White screen?
            raise TimeoutException("Login: Whitescreen?")

    # try and load signin confirmation page. Enter code if page loads
    check_for_error = False
    try:
      WDW(self.driver, 10).until(lambda x: self.signin_code_page.load())
      self.signin_code_page.enter_code()
    except TimeoutException:
      # signin confirmation didn't load
      check_for_error = True

    # Signin Code page didn't load. Wrong password?
    # if check_for_error:
    #   try:
    #     WDW(driver, 4).until(
    #       EC.presence_of_element_located((By.ID, 'sendmi_error')))
    #     error = self.driver.find_element_by_id('sendmi_error')
    #     # probably has password error
    #     print(error.text)
    #     print(messages.login_error)
    #     raise Exception(messages.login_error)
    #   except (TimeoutException, NoSuchElementException) as e:
    #     # No password error.
    #     # Captcha checkbox from too many failed login attempts?
    #     if self.signin_page.check_captcha():
    #       # had too many failed login attempts. Should be on code page now
    #       WDW(self.driver, 10).until(lambda x: self.signin_code_page.load())
    #       self.signin_code_page.enter_code()
    #     else:
    #       # No captcha checkbox. Check if user was remembered and code page was skipped
    #       try:
    #         WDW(driver, 8).until(
    #           EC.presence_of_element_located((By.ID, 'sendmi_appbar')))
    #       except TimeoutException:
    #         # Couldn't find header. White screen?
    #         raise TimeoutException("Login: Whitescreen?")

    # Should be logged in. Wait for an authenticated page to load
    try:
      WDW(driver, 15).until(lambda x: self.lobby_page.load()
          or self.eHome_page.load('login'))
      #extended because slow-as-frozen-mud Android emulator
      #pay-election page included for accounts that have not set an election.
      return True
    except TimeoutException:
      raise TimeoutException(messages.login_landing_exception)
    except Exception as e:
      msg = "Login: Unexpected error:", sys.exc_info()[0]
      print(msg)
      raise Exception(msg)
    return False

  def generate_name(self, surname=True):
    name = [None]*3
    name[0] = (
      self.generate_string(1, 'upper') +
      self.generate_string(7, 'lower')
    )
    name[1] = (
      self.generate_string(1, 'upper') +
      self.generate_string(7, 'lower')
    )
    name[2] = (
      self.generate_string(1, 'upper') +
      self.generate_string(7, 'lower')
    )

    #   random.choice(string.ascii_uppercase) +
    #   ''.join(random.choice(string.ascii_lowercase) for _ in xrange(7))
    # )
    # name[1] = (
    #   random.choice(string.ascii_uppercase) +
    #   ''.join(random.choice(string.ascii_lowercase) for _ in xrange(7))
    # )
    # if surname:
    #   name[2] = (
    #     random.choice(string.ascii_uppercase) +
    #     ''.join(
    #       random.choice(string.ascii_lowercase) for _ in xrange(7))
    #   )
    return name

  def generate_string(self, num_digits=7, case='lower'):
    if 'upper' in case:
      if num_digits < 2:
        return random.choice(string.ascii_uppercase)
      else:
        return ''.join(random.choice(string.ascii_uppercase) for _ in xrange(num_digits))
    else:
      if num_digits < 2:
        return random.choice(string.ascii_lowercase)
      else:
        return ''.join(random.choice(string.ascii_lowercase) for _ in xrange(num_digits))

  def generate_email(self):
    return 'a' + ''.join(
      random.choice(string.ascii_letters + string.digits) for _ in
      xrange(10)) + '@example.com'

  def generate_amount(self, digits=1):
    # Generate random 2 digit number and random cents.
    # Never has leading 0
    first = str(random.randint(1, 9))
    second = ''
    if digits == 2:
      second = str(random.randint(0, 9))
    cents = ''.join(str(random.randint(0, 9)) for _ in xrange(2))
    return first + second + "." + cents

  def generate_number(self, num_digits, lower_bound=0, upper_bound=9):
    # Return random number of length 'num_digits'
    if num_digits < 2:
      return str(random.randint(int(lower_bound), int(upper_bound)))
    else:
      return ''.join(str(random.randint(int(lower_bound), int(upper_bound))) for _ in xrange(num_digits))

  def generate_rfc_dob(self):
    # RFC format: yymmdd
    # Dob format: mm/dd/yy
    year = '19' + ''.join(str(random.randint(0, 9)) for _ in xrange(2))
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 30)).zfill(2)
    values = [month, day, year]
    return '/'.join(values)

  def generate_bbva_amount(self, small_amount=True):
    # Increments of 100, 0-8,000
    upper_max = 7
    if small_amount:
      upper_max = 1
    first = str(random.randint(0, upper_max))
    second = str(random.randint(0, 9))
    if first == '0':
      if second == '0':
        return "100"
      else:
        return second + "00"
    else:
      return first + second + "00"

  def quit(self):
    self.driver.quit()
