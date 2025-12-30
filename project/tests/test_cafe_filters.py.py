import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Pytest Fixture: Handles the browser setup (Setup) and closing (Teardown)
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    
    # Stealth settings to avoid bot detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Human-like User Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=options)
    yield driver  # This is where the test function will execute
    
    # Cleanup after test finishes
    driver.quit()

# Test Function: Pytest looks for functions starting with 'test_'
def test_d_co_il_search_flow(driver):
    wait = WebDriverWait(driver, 25)

    # Step 1: Navigate to the homepage
    driver.get("https://www.d.co.il/")
    
    # Step 2: Search for 'קפה' (Coffee)
    search_field = wait.until(EC.element_to_be_clickable((By.ID, "query")))
    search_field.clear()
    search_field.send_keys("קפה")
    search_field.send_keys(Keys.ENTER)

    # Step 3: Apply Regional Filter (Tel Aviv and Central District)
    region_xpath = "//div[@data-name='אזור ת\"א והמרכז']"
    region_filter = wait.until(EC.element_to_be_clickable((By.XPATH, region_xpath)))

    # Ensure the element is visible before clicking
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_filter)
    time.sleep(1.5)

    try:
        region_filter.click()
    except Exception:
        # Fallback to JavaScript click if standard click is intercepted
        driver.execute_script("arguments[0].click();", region_filter)

    # Step 4: Synchronization
    time.sleep(3)

    # Step 5: Filter by Recommended results
    recommended_xpath = "//a[contains(@href, '/recommended/')]"
    recommended_link = wait.until(EC.element_to_be_clickable((By.XPATH, recommended_xpath)))
    driver.execute_script("arguments[0].click();", recommended_link)

    # Final Verification (Assertion)
    # Pytest uses 'assert' to verify if the test passed or failed
    wait.until(EC.url_contains("recommended"))
    
    # Assertion 1: Check if the URL contains the expected filter word
    assert "recommended" in driver.current_url, f"Expected URL to contain 'recommended', but got {driver.current_url}"
    
    # Assertion 2: Verify that the search term 'קפה' is still present in the results
    assert "קפה" in driver.page_source or "קפה" in driver.title, "Search term 'קפה' was not found in results"
