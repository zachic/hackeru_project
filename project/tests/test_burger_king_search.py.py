import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Pytest Fixture: This handles the browser setup and teardown
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    
    # Stealth settings to prevent bot detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Setting a realistic User-Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=options)
    yield driver  # This is where the test function will run
    
    # Teardown: Close the browser after the test is finished
    driver.quit()

# Test Function: Pytest will automatically find and run this function
def test_burger_king_search(driver):
    wait = WebDriverWait(driver, 25)

    # Step 1: Navigate to the website
    driver.get("https://www.d.co.il/")
    
    # Step 2: Search for 'Burger King' in Hebrew
    search_field = wait.until(EC.element_to_be_clickable((By.ID, "query")))
    search_field.clear()
    search_field.send_keys("בורגר קינג")
    search_field.send_keys(Keys.ENTER)

    # Step 3: Locate and click on the specific business result
    # We use the specific ID '80242228' to ensure we reach the correct branch
    bk_link_xpath = "//a[contains(@href, '/80242228/30455/') and (contains(text(), 'Burger King') or contains(text(), 'בורגר קינג'))]"
    bk_link = wait.until(EC.element_to_be_clickable((By.XPATH, bk_link_xpath)))
    
    # Scroll to the element and click it using JavaScript for better stability
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bk_link)
    time.sleep(1.5)
    driver.execute_script("arguments[0].click();", bk_link)

    # Step 4: Verification (Assertions)
    # Ensure the URL contains the expected business ID
    wait.until(EC.url_contains("80242228"))
    
    # Check if the URL is correct
    assert "80242228" in driver.current_url, f"Expected URL to contain 80242228, but got {driver.current_url}"
    
    # Check if 'Burger King' appears in the page source or title
    assert "Burger King" in driver.page_source or "בורגר קינג" in driver.title
