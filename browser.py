from os import environ
import os, sys
from selenium import webdriver
from appium import webdriver as appium_webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.webdriver import FirefoxProfile
# import org.openqa.selenium.remote.DesiredCapabilities;
import main

def get_url(env, device_farm):
  if env == 'desktop':
    return 'http://127.0.0.1:5050/wd/hub'
  elif device_farm:
    # AWS Device Farm:
    return 'http://localhost:4723/wd/hub'
    # Sauce Labs:
    # return 'http://us1.appium.testobject.com/wd/hub'
  else:
    return 'http://localhost:4723/wd/hub'

def get_desired_caps(env, browser, device_farm, chrome_options=False):
  if env == 'android':
    if device_farm:
      # AWS Device farm: Use empty desiredCapabilities.
      desired_caps = {}

      # SauceLabs
      # desired_caps = {
      #   'platformName': 'Android',
      #   'platformVersion': '8.0',
      #   'testobject_api_key': 'D508E2C406424DE2BDEEC40F6F95EB52',
      #   'deviceName': 'LG Nexus 5X Free',
      #   'testobject_appium_version': '1.5.2-patched-chromedriver'
      # }
    elif browser == 'native':
      app_path = '/Users/andrewtidd/ppay10/cordova/platforms/android/build/outputs/apk/android-debug.apk'
      # app_path = 'C:/Users/Jeff/Desktop/virtualenvs/android-debug.apk'
      desired_caps = {
        'platformName': 'Android',
        'platformVersion': '8.0',
        'deviceName': 'Pixel_API_24',
        'avd': 'Pixel_API_24',
        'app': app_path,
        'autoWebview': 'true',
        'autoGrantPermissions': 'true'
      }
    else: # web
      desired_caps = {
        'platformName': 'Android',
        'platformVersion': '8.0',
        'deviceName': 'Pixel_API_24',
        'browserName': 'Chrome',
        'avd': 'Pixel_API_24',
        'autoGrantPermissions': 'true',
        'automationName': 'UiAutomator2',
      }
  elif env == 'ios':
    if browser == 'native':
      app_path = '/Users/andrewtidd/ppay10/cordova/platforms/ios/build/emulator/sendmi.app'
      desired_caps = {
        'platformName': 'iOS',
        'platformVersion': '11.2',
        'deviceName': 'iPhone SE',
        'app': app_path,
        'automationName': 'XCUITest',
        'autoWebview': 'true'
      }
    else: # web
      desired_caps = {
        'platformName': 'iOS',
        'platformVersion': '11.2',
        'browserName': 'Safari',
        'deviceName': 'iPhone SE',
        'automationName': 'XCUITest'
      }

  else: # env == 'desktop'
    if browser.lower() == 'firefox':
      desired_caps = webdriver.DesiredCapabilities.FIREFOX
    elif browser.lower() == 'safari':
      desired_caps = webdriver.DesiredCapabilities.SAFARI
      safari_options = {'cleanSession': True}
      desired_caps['safariOptions'] = safari_options
    else:
      desired_caps = webdriver.DesiredCapabilities.CHROME
      if chrome_options:
        path = "/Users/andrewtidd/Desktop/ChromeProfile"
        chrome_options = {'args': ['--user-data-dir='+path]}
        desired_caps['chromeOptions'] = chrome_options

  # if device_farm:
  #     desired_caps['testobject_api_key'] = 'D508E2C406424DE2BDEEC40F6F95EB52'
  #     desired_caps['deviceName'] = 'LG Nexus 5X Free'
  return desired_caps

def get_profile():
  """Used only for the firefox 'remember me' test"""
  profile_dir = sys.path[0]
  profile_path = os.path.join(profile_dir, '0kajmvjw.TestBot')
  profile = FirefoxProfile(profile_path)
  return profile

def get_chrome_options():
  path = "/Users/andrewtidd/Library/Application Support/Google/Chrome/Default"
  options = webdriver.ChromeOptions()
  options.add_argument("user-data-dir=" + path)
  return options

# expected params:
#   env={'desktop','ios','android'}
#   browser={'Chrome','Firefox','Safari'}
def start(env=None, browser=None, cached=False, chrome_options=False):
  env = main.get_env()

  if browser is None:
    browser = main.get_browser()
  device_farm = main.is_device_farm()

  url = get_url(env, device_farm)
  desired_caps = get_desired_caps(env, browser, device_farm, chrome_options)

  # appium or selenium driver?
  remote = webdriver.Remote # selenium
  if env != 'desktop':
    remote = appium_webdriver.Remote # appium

  # loading profile? (only on desktop Firefox)
  if browser.lower() == 'firefox' and cached:
    driver = remote(url, desired_caps, browser_profile=get_profile())
  else:
    driver = remote(url, desired_caps)
  # elif browser.lower() == 'chrome' and chrome_options:
  #   driver = remote(url, desired_caps, chrome_options=get_chrome_options())


  if env == 'desktop':
    # set default window settings
    driver.set_window_size(1200, 960)
    if browser.lower() == 'safari':
      driver.maximize_window()
    # driver.set_window_position(0, 0)
    browser_name = driver.desired_capabilities['browserName']

  # # on native, switch to webview
  # instead of setting when starting driver, setting 'autoWebview': 'true'
  # when testing android native

  if device_farm:
    current = driver.current_context
    views = driver.contexts
    for view in views:
      print(str(view))
      if view != 'NATIVE_APP':
        driver.switch_to.context(view)

  return driver

  # appuim server documentation
  # https://appium.io/slate/en/master/?ruby#appium-server-capabilities


