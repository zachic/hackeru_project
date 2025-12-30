import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 1. This Fixture replaces the 'setup_driver' function
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=options)
    yield driver  # This is where the test logic will run
    driver.quit() # This happens after the test, replacing the 'finally' block

def safe_click(driver, wait, xpath):
    """ Helper function to find, scroll, and click an element safely """
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1.5)
    driver.execute_script("arguments[0].click();", element)

# 2. This function replaces 'def main()'. Pytest will run it automatically.
def test_price_lobby_navigation(driver):
    wait = WebDriverWait(driver, 25)

    # Step 1: Navigation
    driver.get("https://www.d.co.il/")
    time.sleep(3)

    # Step 2: Price Lobby
    lobby_xpath = "//a[contains(@href, '/priceLoby/')]"
    safe_click(driver, wait, lobby_xpath)

    # Step 3: Specific Price List
    target_xpath = "//a[contains(@href, '/priceList-27930/')]"
    safe_click(driver, wait, target_xpath)

    # Step 4: Verification (Assertion)
    # Instead of 'if/else' or 'print', we use 'assert' to verify the result
    wait.until(EC.url_contains("priceList-27930"))
    
    assert "priceList-27930" in driver.current_url, f"Failed to reach target URL. Current: {driver.current_url}"
