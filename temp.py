import profiles
import browser
import time
import unittest
import main

def run():
  andrew = profiles.Profile(browser.start(main.get_env(),main.get_browser()), 'andrew')

  andrew.login()
  andrew.employee_page.on()

  filters = andrew.employee_page.get_filters()

if __name__ == '__main__':
  run()



