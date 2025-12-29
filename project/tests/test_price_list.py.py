from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    # Stealth settings to bypass detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def safe_click(driver, wait, xpath, description):
    """ Helper function to find, scroll, and click an element safely """
    try:
        print(f"Searching for element: {description}")
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1.5)  # Synchronization delay
        driver.execute_script("arguments[0].click();", element)
        print(f"Element clicked successfully: {description}")
    except Exception as e:
        print(f"Error: Failed to click {description}. Details: {e}")
        raise e

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 25)

    try:
        # Step 1: Initialization
        print("Connecting to D.co.il homepage...")
        driver.get("https://www.d.co.il/")
        time.sleep(3)

        # Step 2: Navigate to Price Lobby
        lobby_xpath = "//a[contains(@href, '/priceLoby/')]"
        safe_click(driver, wait, lobby_xpath, "Price Lobby Link")

        # Step 3: Navigate to Specific Price List
        target_xpath = "//a[contains(@href, '/priceList-27930/')]"
        safe_click(driver, wait, target_xpath, "Small Removals Price List")

        # Step 4: Verification phase
        wait.until(EC.url_contains("priceList-27930"))
        print(f"Verification passed. Target URL reached: {driver.current_url}")
        time.sleep(5)

    except Exception as e:
        print(f"Test execution failed: {e}")
        driver.save_screenshot("price_list_error.png")
        print("Diagnostic screenshot saved: price_list_error.png")

    finally:
        print("Closing session.")
        driver.quit()

if __name__ == "__main__":
    main()