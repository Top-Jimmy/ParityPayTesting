from page import Page
from components import menu
from components import header
from components import additional_data_form
from selenium.common.exceptions import (NoSuchElementException,
  StaleElementReferenceException)

class RecipientInfoPage(Page):
  # url_tail = "/recipient/035a005a/additionaldata"

  def load(self):
    try:
      self.menu = menu.SideMenu(self.driver)
      self.header = header.PrivateHeader(self.driver)
      self.addInfo = additional_data_form.AddDataForm(self.driver)
      return True
    except (NoSuchElementException, StaleElementReferenceException, IndexError) as e:
      return False

