from selenium import webdriver
import time
import sqlite3
from selenium.webdriver.common.by import By

kullanici_adi = str(input("Instagram Username: "))
sifre = str(input("Password: "))


op = webdriver.ChromeOptions()
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
# op.add_argument("--headless")
op.add_argument("--incognito")
op.add_argument("--disable-extensions")
op.add_argument("--proxy-server='direct://'")
op.add_argument("--proxy-bypass-list=*")
op.add_argument("--start-maximized")
op.add_argument('--disable-gpu')
op.add_argument('--disable-dev-shm-usage')
op.add_argument('--no-sandbox')
op.add_argument('--ignore-certificate-errors')
browser = webdriver.Chrome(options=op)

# Giriş Yap
browser.get("https://www.instagram.com/")
print(">> Logging in.")

time.sleep(2)
try:
    username = browser.find_element(By.NAME, 'username')  # cagrimangir
    password = browser.find_element(By.NAME, 'password')  # Cagri61659301???
except Exception:
    browser.get_screenshot_as_file("screenshot.png")

username.send_keys(kullanici_adi)
password.send_keys(sifre)

loginButton = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
loginButton.click()

time.sleep(5)

browser.get(f"https://www.instagram.com/{kullanici_adi}/followers/")
time.sleep(5)


print("\n>> Going to the follower page has been successfully completed!")
time.sleep(3)

# Takipçileri Al
print(">> Getting followers. (This process may take time depending on how many followers you have.)")

time.sleep(3)
# import ipdb;ipdb.set_trace()
while True:
    all_elements = [element for element in browser.find_elements(By.CLASS_NAME, '_acap') if element.text=="Remove"]
    if len(all_elements) == 0: break;
    for element in all_elements: 
        time.sleep(3)
        element.click()
        time.sleep(5)
        browser.find_element(By.CLASS_NAME, '_a9--').click()

    browser.get(f"https://www.instagram.com/{kullanici_adi}/followers/")
    time.sleep(5)
    

time.sleep(2)
browser.close()
