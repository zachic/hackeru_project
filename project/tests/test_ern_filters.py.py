import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Pytest Fixture to initialize and close the browser automatically
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # Stealth settings to bypass bot detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=options)
    yield driver  # This is where the test runs
    
    # Teardown: Close the browser after the test is done
    driver.quit()

# The Test Function (Must start with 'test_')
def test_ern_search_flow(driver):
    wait = WebDriverWait(driver, 25)

    # Step 1: Navigation
    driver.get("https://www.d.co.il/")

    # Step 2: Search execution for 'e.r.n'
    search_field = wait.until(EC.element_to_be_clickable((By.ID, "query")))
    search_field.clear()
    search_field.send_keys("e.r.n")
    search_field.send_keys(Keys.ENTER)

    # Step 3: Regional Filtering (Tel Aviv and Central District)
    region_xpath = "//div[@data-name='אזור ת\"א והמרכז']"
    region_filter = wait.until(EC.element_to_be_clickable((By.XPATH, region_xpath)))

    # Scroll to element for better reliability
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_filter)
    time.sleep(1.5)

    try:
        region_filter.click()
    except Exception:
        driver.execute_script("arguments[0].click();", region_filter)

    # Step 4: Synchronization pause
    time.sleep(3)

    # Step 5: Navigate to Recommended results tab
    recommended_xpath = "//a[contains(@href, '/recommended/')]"
    recommended_link = wait.until(EC.element_to_be_clickable((By.XPATH, recommended_xpath)))
    driver.execute_script("arguments[0].click();", recommended_link)

    # --- Step 6: Assertions (Verification) ---
    # This is the most important part for Pytest
    
    # Check if the URL contains 'recommended'
    wait.until(EC.url_contains("recommended"))
    assert "recommended" in driver.current_url, f"Verification failed! Current URL: {driver.current_url}"
    
    # Check if 'e.r.n' or the search results are visible
    assert "e.r.n" in driver.page_source or "E.R.N" in driver.page_source, "Verification failed! Search term not found on results page."
