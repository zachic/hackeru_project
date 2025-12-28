import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    # Start Chrome Browser
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0")  # Helps avoid bot detection

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    yield driver  # The test runs here

    # Close browser after test
    driver.quit()