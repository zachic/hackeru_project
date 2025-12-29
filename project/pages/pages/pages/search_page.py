from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SearchPage(BasePage):
    SEARCH_INPUT = (By.ID, "query")

    def search_for(self, text):
        search_field = self.wait.until(By.element_to_be_clickable(self.SEARCH_INPUT))
        search_field.clear()
        search_field.send_keys(text)
        search_field.send_keys(Keys.ENTER)
