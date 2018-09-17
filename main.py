
# env: 'android', 'ios', 'desktop'
# browser (mobile): 'native', 'web'
# browser (desktop): 'Chrome', 'Firefox', 'Safari'
# priority: Certain tests will skip depending on priority
# cancel transactions: Will cancel pending transactions at end of send tests
config = {
  'env': 'android',
  'browser': 'native',
  'priority_level': 4,
  'cancel_transaction': True,
  'device_farm': False
}
# base_url = 'localhost:3000/'                  # local
# base_url = 'http://localtest.sendmi.com:3000/'
base_url =  "https://test.sendmi.com/"   # google test server
if config['browser'] is 'native':
  version = 'V 1.1.0'
else:
  version = 'V 1.1.0'

def get_env():
  return config['env'].lower()

def get_browser():
  return config['browser'].lower()

def get_priority():
  # 1 (run tests w/ priority of 1)
    # major functionality (End-to-end? def. as normal user paths)
  # 2 (run tests w/ priority <= 2)
    # more coverage
  # 3 (run tests w/ priority <= 3)
    # required fields
    # invalid inputs
  # 4 (run tests w/ priority <= 4)
    # fringe cases?
  return config['priority_level']

def get_base_url():
  return base_url

def cancel_transaction():
  return config['cancel_transaction']

def get_version():
  return version

def is_device_farm():
  return config['device_farm']




def is_web():
  return config['browser'] != 'native'

def is_desktop():
  return config['env'] is 'desktop'

def is_android():
  return config['env'] is 'android'

def is_ios():
  return config['env'] is 'ios'




def native_context(driver):
  """Switch from webview to native context"""
  current = driver.current_context
  views = driver.contexts
  # views = ['NATIVE_APP', 'CHROMIUM'] (android)
  for view in views:
    if view == 'NATIVE_APP':
      driver.switch_to.context(view)

def webview_context(driver):
  """Switch from native to webview context"""
  current = driver.current_context
  views = driver.contexts
  for view in views:
    if view != 'NATIVE_APP':
      driver.switch_to.context(view)


