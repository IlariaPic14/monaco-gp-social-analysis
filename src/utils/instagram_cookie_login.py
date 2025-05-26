#instagram_manual_cookie_login.py

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# === CONFIG ===

# Instagram scraping configuration
CHROMEDRIVER_PATH = "driver/chromedriver.exe"
COOKIES_OUTPUT_PATH = "instagram_cookies_scraper.json"
PROXY = "your-proxy-here"



# === SETUP DRIVER ===
def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    #options.add_argument(f"--proxy-server=http://{PROXY}")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# === LOGIN E SALVATAGGIO COOKIE ===
def login_and_save_cookies(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")

    user_input.send_keys(username)
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)

    print(" Attendi eventuale verifica in due passaggi (se richiesta)...")
    time.sleep(60)

    cookies = driver.get_cookies()
    with open(COOKIES_OUTPUT_PATH, "w") as f:
        json.dump(cookies, f)

    print(f" Cookie salvati in {COOKIES_OUTPUT_PATH}")
    driver.quit()

if __name__ == "__main__":
    driver = create_driver()
    login_and_save_cookies(driver, "INSTAGRAM_USERNAME", "INSTAGRAM_PSW")
