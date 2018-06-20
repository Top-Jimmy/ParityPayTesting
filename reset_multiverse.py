import unittest
import time

from selenium.webdriver.support.wait import WebDriverWait

import browser
import profiles
import main

#TEST ON NINTENDO OF AMERICA BUSINESSES!!!

def setUp(self):
    self.driver = browser.start(main.get_env(),main.get_browser())
    self.nicol = profiles.Profile(self.driver,'nicol')
    self.employee = profiles.Profile(self.driver, 'lili')
    self.assertTrue(self.nicol.env_loaded())

  def tearDown(self):
    self.driver.quit()

def reset_multiverse():
  self.nicol.login()

  self.assertTrue(emp_page.on())

  #Remove old Multiverse, add new Multiverse, populate with needed employees.
  emp_page.load()
  emp_page.menu.open()
  self.assertTrue(emp_page.menu.has_business('Multiverse'))
  settings_page.go()
  self.assertTrue(settings_page.remove_business(
    "REMOVE MULTIVERSE"))
  WebDriverWait(self.driver,20).until(acct_page.on())    #profiles.py code
  self.assertTrue(acct_page.on())
  acct_page.menu.open()
  self.assertFalse(acct_page.menu.has_business('Multiverse'))

  add_page.go()
  add_page.load()
  add_page.add("Nintendo of America")
  prefilled_page.load()
  self.assertTrue(prefilled_page.click_details())

  prefilled_page.type_business_name('Multiverse')
  prefilled_page.type_dba('')
  prefilled_page.type_ein('4896434')
  prefilled_page.type_hr_email('nbolas@example.com')
  prefilled_page.type_line1('17 Whiteladies Road')
  prefilled_page.type_city('Avon')
  prefilled_page.select_state('New York')
  prefilled_page.type_postal_code('14414')
  prefilled_page.type_phone('(202) 548-4023')
  prefilled_page.type_website('http://multiverse-music.com')
  self.assertTrue(prefilled_page.click_submit())

  self.assertTrue(emp_page.on())

  emp_ids = ['13313113', '242464', '65410', 'SA-001', 'SA-002', 'SA-003',
    'SA-004', 'SA-005', 'SA-006']
  for emp in ['lili', 'cheeks', 'test', 'alone1', 'alone2', 'alone3', 'alone4',
    'alone5', 'alone6']:
    self.employee = profiles.Profile(self.driver,emp)
    credentials = self.employee.credentials
    first_name = credentials['first_name']
    last_name = credentials['last_name']
    email = credentials['email']
    phone = credentials['phone']
    emp_id = emp_ids[0]
    emp_ids.pop(0)

    onboard_existing_account(first_name, last_name, email, emp_id, phone)

  emps = [
    ['Zuriel', 'Conseco', 'zconseco@example.com'],
    ['Zuriel', 'Hernandez', 'zhernandez@example.com'],
    ['Jane', 'Doe', 'mime@example.com']
    ]
  emp_ids = ['9876543210', '0123456789', '99887766']
  #Remove Conseco, Terminate Hernandez, Invite Jane.
  while emp_ids:
    employee_id = emp_ids.pop(0)
    emp_page.click_plus()
    emp_page.click_add_employee()
    self.assertTrue(add_page.on())
    add_page.set_first_name(first_name)
    add_page.set_last_name(last_name)
    add_page.set_email(email)
    add_page.set_phone(phone)
    add_page.set_id(employee_id)
    add_page.click_employee_add()
    time.sleep(1)
    self.assertTrue(emp_page.on())
    if len(emp_ids) is 2:
      emp_page.remove_employee('id',employee_id)
    elif len(emp_ids) is 1:
      emp_page.terminate_employee('id',employee_id)


def onboard_existing_account(first_name, last_name, email, emp_id, phone=None):
  #profiles not passed in. onboard doesn't know nicol or employee.
  #Might know from global declaration (setUp)
  emp_page = self.nicol.employee_page
  add_page = self.nicol.employee_add_page
  election_page = self.employee.main_election_page
  #Employer generates invitation.
  emp_page.click_plus()
  emp_page.click_add_employee()
  self.assertTrue(add_page.on())
  add_page.set_first_name(first_name)
  add_page.set_last_name(last_name)
  add_page.set_email(email)
  add_page.set_phone(phone)
  add_page.set_id(emp_id)
  emp_ids.pop(0)
  add_page.click_employee_add()
  time.sleep(1)

  self.assertTrue(emp_page.on())
  urls = emp_page.get_secret_urls()
  emp_page.click_toast() # clear toast or cannot click logout (mobile)
  time.sleep(.4)
  employee = emp_page.get_employee('id',employee_id)
  self.assertEqual(first_name + ' ' + last_name, employee['name'])
  self.assertEqual(employee_id, employee['id'])
  self.assertEqual('Invited', employee['status'])
  emp_page.menu.open()
  emp_page.menu.sign_out()

  # employee responds to invitation
  acct_page = self.employee.account_page
  invite_page = self.employee.invite_page
  enroll_signin_page = self.employee.enroll_signin_page
  election_page = self.employee.main_election_page
  home_page = self.employee.home_page

  invite_page.go(urls['email_url'])
  invite_page.set_email(email)
  time.sleep(1)
  #"Already invited, please sign in" page.
  self.assertTrue(signin_page.on())
  signin_page.type_password(credentials['password'])
  #lili.invite_page.click_yes()
  time.sleep(1)
  self.assertTrue(election_page.on())
  election_page.set_election('Multiverse', '10.00')
  election_page.menu.open()
  election_page.menu.sign_out()

  # nicol asserts employee is in emp table.
  self.assertTrue(home_page.on())
  self.nicol.login()

  self.assertTrue(emp_page.on())
  employee = emp_page.get_employee('id',employee_id)
  self.assertEqual(first_name + ' ' + last_name, employee['name'])
  self.assertEqual(employee_id, employee['id'])
  self.assertEqual('Active', employee['status'])
