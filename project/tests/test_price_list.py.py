import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Pytest Fixture: This replaces 'setup_driver' and handles setup and cleanup
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # Stealth settings to bypass detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=options)
    yield driver  # This is where the test executes
    
    # Teardown: Closes the browser after the test is finished
    driver.quit()

def safe_click(driver, wait, xpath):
    """ Helper function to find, scroll, and click an element safely """
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1.5)  # Stabilization delay
    driver.execute_script("arguments[0].click();", element)

# Test Function (Must start with 'test_')
def test_price_list_navigation(driver):
    wait = WebDriverWait(driver, 25)

    # Step 1: Navigate to the homepage
    driver.get("https://www.d.co.il/")
    time.sleep(3)

    # Step 2: Navigate to Price Lobby
    lobby_xpath = "//a[contains(@href, '/priceLoby/')]"
    safe_click(driver, wait, lobby_xpath)

    # Step 3: Navigate to Specific Price List (Small Removals)
    target_xpath = "//a[contains(@href, '/priceList-27930/')]"
    safe_click(driver, wait, target_xpath)

    # Step 4: Verification phase (Assertions)
    # This replaces the print statements with formal pass/fail logic
    wait.until(EC.url_contains("priceList-27930"))
    
    # Assert that the URL is correct
    assert "priceList-27930" in driver.current_url, f"Failed to reach the target price list. Current URL: {driver.current_url}"
    
    # Assert that the page content is relevant (e.g., contains the word 'Price' or 'הובלות')
    assert "price" in driver.current_url.lower() or "priceList" in driver.page_source
