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
    # Stealth settings to avoid bot detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Human-like User Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(options=options)


def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 25)

    try:
        # Step 1: Navigate to the homepage
        print(" Step 1: Navigating to D.co.il...")
        driver.get("https://www.d.co.il/")

        # Step 2: Search for 'בורגר קינג'
        print(" Step 2: Searching for 'בורגר קינג'...")
        search_field = wait.until(EC.element_to_be_clickable((By.ID, "query")))
        search_field.clear()
        search_field.send_keys("בורגר קינג")
        search_field.send_keys(Keys.ENTER)

        # Step 3: Click on the specific business result (Burger King Tel Aviv)
        print(" Step 3: Selecting Burger King, Tel Aviv...")
        # Using the specific link for the Tel Aviv branch (ID 80242228/30455)
        bk_link_xpath = "//a[contains(@href, '/80242228/30455/') and contains(text(), 'Burger King')]"
        bk_link = wait.until(EC.element_to_be_clickable((By.XPATH, bk_link_xpath)))

        # Scroll to ensure the link is visible
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bk_link)
        time.sleep(1.5)

        # Click the link
        print(" Clicking on the business profile link...")
        driver.execute_script("arguments[0].click();", bk_link)

        # Final Verification
        wait.until(EC.url_contains("80242228"))
        print(f" Success! Reached the business page: {driver.current_url}")

    except Exception as e:
        print(f" Error encountered: {e}")
        driver.save_screenshot("navigation_step_error.png")
        print("📸 Screenshot saved as 'navigation_step_error.png'")

    finally:
        # Keep the browser open for 5 seconds for visual confirmation
        print(" Task finished. Closing browser in 5 seconds...")
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()