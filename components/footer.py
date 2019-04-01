from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import main
from component import Component

# pages w/ public footer

# (1) home
# (2) enroll business
# (3) contact page (public)
# (4) about (public)

class PubFooter(Component):

	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.footer = self.driver.find_element_by_class_name('footer')
		self.logo = self.footer.find_element_by_id('public_logo')

		find_by = self.footer.find_elements_by_class_name
		self.footer_links = {
			'about us': find_by('linkDiv')[0],
			'for employees': find_by('linkDiv')[1],
			'for employers': find_by('linkDiv')[2],
			'sign in': find_by('linkDiv')[3],
			'terms and conditions': find_by('linkDiv')[4],
			'privacy policy': find_by('linkDiv')[5],
			'faqs': find_by('linkDiv')[6],
			'contact us': find_by('linkDiv')[7],
			'facebook': find_by('linkDiv')[8],
			'twitter': find_by('linkDiv')[9],
			'linked in': find_by('linkDiv')[10],
			# 'google+': find_by('linkDiv')[11],
			# 'youtube': find_by('linkDiv')[12]
		}

	def click_link(self,link_text):
		"""given text of link, move to element and click <a> el"""
		# print(link_text.lower())
		link = self.footer_links[link_text.lower()].find_element_by_tag_name('a')
		self.driver.execute_script("arguments[0].scrollIntoView();", link)
		time.sleep(.4)
		link.click()

	def click_logo(self):
		self.logo.click()
