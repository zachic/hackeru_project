from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    # Stealth settings to bypass bot detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 25)

    try:
        # Step 1: Navigation
        print("Navigating to D.co.il homepage...")
        driver.get("https://www.d.co.il/")

        # Step 2: Search for 'קפה'
        print("Initiating search for: קפה")
        search_field = wait.until(EC.element_to_be_clickable((By.ID, "query")))
        search_field.clear()
        search_field.send_keys("קפה")
        search_field.send_keys(Keys.ENTER)

        # Step 3: Apply Regional Filter
        print("Applying regional filter: Tel Aviv and Central District")
        region_xpath = "//div[@data-name='אזור ת\"א והמרכז']"
        region_filter = wait.until(EC.element_to_be_clickable((By.XPATH, region_xpath)))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_filter)
        time.sleep(1.5)

        try:
            region_filter.click()
        except Exception:
            driver.execute_script("arguments[0].click();", region_filter)

        # Step 4: Synchronization
        time.sleep(3)

        # Step 5: Filter by Recommended
        print("Applying filter: Recommended results")
        recommended_xpath = "//a[contains(@href, '/recommended/')]"
        recommended_link = wait.until(EC.element_to_be_clickable((By.XPATH, recommended_xpath)))
        driver.execute_script("arguments[0].click();", recommended_link)

        # Verification
        wait.until(EC.url_contains("recommended"))
        print(f"Workflow completed successfully. Final URL: {driver.current_url}")

    except Exception as e:
        print(f"Error encountered during execution: {e}")
        driver.save_screenshot("search_error_screenshot.png")
        print("Error screenshot saved as 'search_error_screenshot.png'")

    finally:
        print("Closing browser and cleaning up.")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()