from page import Page
from selenium.common.exceptions import (NoSuchElementException,
	StaleElementReferenceException)
import main
import time

class NativeSplashPage(Page):
	def load(self):
		try:
			find_by = self.driver.find_element_by_id
			self.language_selector = find_by('locale_dropdown')
			self.english = find_by('locale_en')
			self.spanish = find_by('locale_es')
			self.next_button = find_by('nextButton')
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def click_next(self):
		self.next_button.click()

	def select_language(self,lang):
		if not self.english.is_displayed():
			self.language_selector.click()
			time.sleep(.2)
		if lang is 'English':
			self.english.click()
		elif lang is 'Spanish':
			self.spanish.click()
		time.sleep(.4)

	# def click_next(self):
	#     self.next_button.click()
	#     if main.is_ios() and not main.is_web():
	#         time.sleep(1)

#screen 2 (native_splash2)
class NativeSplashPage2(Page):
	def load(self):
		try:
			find_by = self.driver.find_element_by_id
			self.logo = find_by('public_logo')
			self.next_button = find_by('startButton')
			self.language_selector = find_by('locale_dropdown')
			self.english = find_by('locale_en')
			self.spanish = find_by('locale_es')
			return True
		except (NoSuchElementException, StaleElementReferenceException) as e:
			return False

	def click_next(self):
		self.next_button.click()

	def select_language(self,lang):
		if not self.english.is_displayed():
			self.language_selector.click()
			time.sleep(.2)
		if lang is 'English':
			self.english.click()
		elif lang is 'Spanish':
			self.spanish.click()
		time.sleep(.4)

	# def click_logo(self):
	#     self.logo.click()
	#     time.sleep(.4)

	# def click_next(self):
	#     self.next_button.click()
	#     if main.is_ios() and not main.is_web():
	#         time.sleep(1)
