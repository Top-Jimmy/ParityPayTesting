import abc
import time
import main
from selenium.common.exceptions import (TimeoutException, WebDriverException,
  NoSuchElementException, StaleElementReferenceException)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction as TA
from selenium.webdriver import ActionChains as AC

class Page:
  __metaclass__ = abc.ABCMeta
  """The super class for all page objects"""
  base_url = main.get_base_url()

  def __init__(self, driver):
    self.driver = driver

  def get_current_page(self):
    return self.driver.current_url

  def go(self, url=None):
    """Go to URL of page. *Web only*"""
    if main.is_web():
      if url is None:
        self.driver.get(Page.base_url + self.url_tail)
      elif Page.base_url not in url:
        self.driver.get(Page.base_url + url)
      else:
        self.driver.get(url)
      return self.on()

  def on(self, arg1=None, arg2=None):
    wait_time = 20
    try:
      if arg1 is None:
        WebDriverWait(self.driver, wait_time).until(lambda x: self.load())
      elif arg2 is None:
        WebDriverWait(self.driver, wait_time).until(lambda x: self.load(arg1))
      else:
        WebDriverWait(self.driver, wait_time).until(lambda x: self.load(arg1, arg2))
      return True
    except TimeoutException:
      print 'Failed to load: ' + str(self.__class__)[8:-2]
      self.try_print_header()
      return False

############## General ###############

  def try_print_header(self):
    # Attempt to find and print text of <h2>.
    try:
      header_txt = self.driver.find_element_by_tag_name('header').text
      print( 'h2= ' + header_txt)
    except NoSuchElementException:
      # Won't be able to find it if components don't render/network issues
      print('Could not find header element')

  def is_enabled(self, el):
    # put in try except incase component redraws
    try:
      return el.is_enabled()
    except WebDriverException:
      # probably not part of DOM anymore
      self.load()
      return False

  def is_public(self):
    # look for public logo
    return self.driver.find_element_by_xpath('//a[@href="/"]')

  def clear(self, input_element):
    """Ensures that an input element gets totally cleared. Use on
    elements that clear unreliably (autosave pages usually)"""
    for _ in range(3):
      time.sleep(.4)
      input_element.clear()
    return input_element.get_attribute('value') == ''

  def clear_input(self,input_element):
    length = len(input_element.get_attribute('value'))
    for i in xrange(length):
      input_element.send_keys(Keys.BACKSPACE)
      # time.sleep(.2)

  def number_of_elements(self, tag, text, attribute=None):
    """Return the number of elements of given tag that have the
    given text"""
    if attribute != None and attribute != 'text':
      xpath = "//{tag}[@{attribute}='{text}']".format(tag=tag, attribute=attribute, text=text)
    else:
      # has trouble parsing strings w/ ' or " chars
      num_double_quotes = text.count('"')
      if num_double_quotes > 0:
        xpath = '//{tag}[text() = \''.format(tag=tag) + text + '\']'
      else:
        xpath = "//{tag}[text() = \"".format(tag=tag) + text + "\"]"
    length = len(self.driver.find_elements_by_xpath(xpath))
    return length #len(self.driver.find_elements_by_xpath(xpath))

  def number_of_elements_containing(self, tag, text, attribute=None):
    """Return the number of elements of given tag that contain the
    given text or attribute"""
    if attribute != None and attribute != 'text':
      xpath = "//{tag}[contains(@{attribute}, '{text}')]".format(tag=tag, attribute=attribute, text=text)
    else:
      xpath = "//{tag}[contains(text(),\"".format(tag=tag) + text + "\")]"
    return len(self.driver.find_elements_by_xpath(xpath))

  def try_click(self, elId):
    try:
      el = self.driver.find_element_by_id(elId)
      self.move_to_el(el)
      return True
    except (NoSuchElementException, StaleElementReferenceException, WebDriverException) as e:
      return False

  def move_to_el(self, el, click=True):
    """Scroll until el is in view. Click unless click=False"""
    # if main.is_desktop():
    #     self.driver.execute_script("arguments[0].scrollIntoView();", el)
    # else:
    #     AC(self.driver).move_to_element(el).perform()

    # this seems to work better on Android web
    # move_to_element doesn't seem to handle the open keyboard very well
    # was having issues setting vals on business settings page
    self.driver.execute_script("arguments[0].scrollIntoView();", el)
    time.sleep(.6)
    if click:
      try: # might be 'visible', but under header. scroll up slightly
        el.click()
      except WebDriverException:
        self.move('up',60)
        el.click()
      time.sleep(1)

  def scroll_to_top(self):
    """scroll to top of page"""
    self.driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(.4)

  def scroll_to_bottom(self):
    """scroll to bottom of page"""
    script = 'window.scrollTo(0, document.body.scrollHeight)'
    self.driver.execute_script(script)
    time.sleep(.4)

  def move(self,direction,pixels):
    """move screen given pixels in given direction ('up','down')"""
    prefix = ''
    if direction.lower() == 'up':
      prefix = '-'

    script = 'window.scrollBy(0, {prefix}{pixels});'.format(prefix=prefix, pixels=str(pixels))
    self.driver.execute_script(script)
    time.sleep(1)

  def ios_scroll(self,direction,pixels):
    """Use TouchActions to scroll given amount up or down (ios)
    Note: cannot use TA on android w/out switching to native context"""
    if main.is_ios():
      prefix = '-'
      if direction.lower() == 'up':
        prefix = ''
      move_amount = int(prefix + str(pixels))

      TA(self.driver).press(None, 10, 400).move_to(None, 0, move_amount).release().perform()
      time.sleep(.6)

  # haven't tested on native yet.
  # works on desktop and ios/android web
  def click_el(self, el, force=False):
    opacity = el.value_of_css_property('opacity')
    print(opacity)
    if force or opacity == '0':
      script = 'arguments[0].click();'
      self.driver.execute_script(script, el)
    else:
      el.click()
    # if main.get_browser() == 'safari':
    #     # used on Safari for 'invisible' elements
    #     script = 'arguments[0].click();'
    #     self.driver.execute_script(script, el)
    # else:
    #     el.click()

  def get_el_location(self, el, attribute=None):
    # given element, return coordinates
    if el is not None:
      script = "return arguments[0].getBoundingClientRect();"
      location = self.driver.execute_script(script, el)
      if attribute is None:
        return location
      else:
        try:
          return location[attribute]
        except IndexError:
          err_str = ("Invalid attribute. Only accepts 'top', "
            "'bottom', 'left' or 'right'.")
          raise Exception(err_str)

  def get_window_height(self):
    return self.driver.execute_script('return window.innerHeight')

  def get_window_width(self):
    return self.driver.execute_script('return window.innerWidth')

  def try_hide_keyboard(self):
    """If open, close android keyboard"""
    if main.is_android():
      try:
        self.driver.hide_keyboard()
        time.sleep(.6)
      except WebDriverException:
        pass

  def has_horizontal_scroll(self):
    """Try to scroll 100px to right and return window offset"""
    self.driver.execute_script('window.scrollBy(100,0)', "")
    x_offset = self.driver.execute_script('return window.pageXOffset;')
    if x_offset != 0:
      return True
    return False

  def has_vertical_scroll(self):
    """Try to scroll 100px down and return window offset"""
    self.driver.execute_script("window.scrollTo(0, -100)")
    y_offset = self.driver.execute_script('return window.pageYOffset;')
    if y_offset != 0:
      return True
    return False

  def go_to_tab(self, index=0):
    # specify index of tab you want to go to (defaults to first tab)

    # only applicable to desktop
    if main.is_desktop():
      self.driver.switch_to.window(self.driver.window_handles[index])

# functions for error dialog

# need ids on error dialog container

  def read_error(self):
    """Return text of sendmi_error element"""
    try:
      # 'sendmi_error' is error div on most forms
      # different from 'required' error you will get for individual fields
      el = self.driver.find_element_by_id('sendmi_error')
      # script = 'return arguments[0].innerHTML;'
      # innerHTML = self.driver.execute_script(script, el)
      # print('type: ' + str(type(innerHTML)))
      # print(el.text)

      text = el.text
      index = text.find('alert')
      print(text[index + 5:])
      return text[index + 5:]
      # return self.parseReactText(innerHTML)
    except NoSuchElementException:
      return None

  def parseReactText(self, innerHTML):
    # Don't think we need this after react update
    # Will run into issues if you try to get regular text from react component
    beg_index = innerHTML.find('-->')+3
    end_index = innerHTML.find('<!--', beg_index)
    print(beg_index)
    print(end_index)
    print(innerHTML[beg_index: end_index])
    return innerHTML[beg_index: end_index]

  def has_error(self):
    try:
      headers = self.driver.find_elements_by_tag_name('h3')
      text = 'Server Connection Error'
      for i, header in enumerate(headers):
        header_text = header.text
        if header_text == text:
          return True

    except (NoSuchElementException, IndexError) as e:
      return False

# functions for custom keyboard
  # enter_currency('amount')
  # clear_currency(el_with_amount_as_text)
  # close_custom_keyboard()

  def keyboard_visible(self):
    """Is custom keyboard visible?"""
    try:
      keyboard = self.driver.find_element_by_class_name('custom_keyboard')
      return True
    except NoSuchElementException:
      return False

  def enter_currency(self, amount):
    """Enter given amount using custom keyboard then close keyboard
      Mobile ONLY
      Requires input is focused and custom keyboard is open"""
    try:
      self.keyboard = (
        self.driver.find_element_by_class_name('custom_keyboard'))

      for i in xrange(len(amount)):
        # raw_input('typing index:' + str(i) + ' char:' + str(amount[i]))
        self.click_custom_key(amount[i])

      self.close_custom_keyboard()
      return True # pass in el w/ amount and return it matches amount?
    except NoSuchElementException:
      return False

  def clear_currency(self, amount):
    """Given amount (as text), press backspace enough to clear.
      Input needs to be selected and custom keyboard open"""
    if amount != '':
      for i in xrange(len(amount)):
        self.click_custom_key('backspace')

  def close_custom_keyboard(self):
    """If open, close custom keyboard"""
    try:
      self.driver.find_element_by_class_name('key_header_bar').click()
    except NoSuchElementException:
      pass

  def click_custom_key(self, character):
    """Given valid character, press correct key on custom keyboard"""
    key_el = self.get_custom_key(character)
    if key_el is not None:
      # raw_input('clicking char: ' + character)
      key_el.click()

  def get_custom_key(self, character):
    """return custom keyboard element corresponding to given character"""
    keys = {
      '0': 'key_0',
      '1': 'key_1',
      '2': 'key_2',
      '3': 'key_3',
      '4': 'key_4',
      '5': 'key_5',
      '6': 'key_6',
      '7': 'key_7',
      '8': 'key_8',
      '9': 'key_9',
      '.': 'key_dot',
      'backspace': 'key_back'
    }
    try:
      # raw_input('looking for key w/ class: ' + keys[character])
      return self.driver.find_element_by_class_name(keys[character])
    except NoSuchElementException:
      print('could not find key w/ class ' + keys[character])
      return None



  @abc.abstractmethod
  def load(self):
    """ Loads the page elements into it's variables. Call after each
    time the page is reloaded"""

