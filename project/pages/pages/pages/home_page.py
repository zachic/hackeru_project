from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    # Locators
    SEARCH_FIELD = (By.ID, "search-term")
    CITY_FIELD = (By.ID, "location-term")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.d.co.il/"

    def open_site(self):
        self.driver.get(self.url)

    def perform_search(self, business_type, city_name):
        self.enter_text(self.SEARCH_FIELD, business_type)
        self.enter_text(self.CITY_FIELD, city_name)
        self.click_element(self.SEARCH_BUTTON, f"Search for {business_type} in {city_name}")
