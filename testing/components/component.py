from selenium.common.exceptions import WebDriverException
import main
import time

class Component:
	"""The super class for all component objects"""

	def __init__(self, driver):
		self.driver = driver

	def try_hide_keyboard(self):
		"""If open, close android keyboard"""
		if main.is_android():
			try:
				self.driver.hide_keyboard()
				time.sleep(.6)
			except (WebDriverException, AttributeError) as e:
				pass

	def scroll_to_top(self):
		"""scroll to top of page"""
		self.driver.execute_script("window.scrollTo(0, 0)")
		time.sleep(.4)

	def scroll_to_bottom(self):
		"""scroll to bottom of page"""
		script = 'window.scrollTo(0, document.body.scrollHeight)'
		self.driver.execute_script(script)
		time.sleep(.4)

	def move_to_el(self, el, click=True):
		"""Scroll until el is in view. Click unless click=False"""
		self.driver.execute_script("arguments[0].scrollIntoView();", el)
		time.sleep(.6)
		if click:
			try: # might be 'visible', but under header. scroll up slightly
				el.click()
			except WebDriverException:
				self.move('up',60)
				el.click()
			time.sleep(1)