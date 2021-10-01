from selenium import webdriver
import time
import sqlite3

kullanici_adi = str(input("Instagram Username: "))
sifre = str(input("Password: "))

op = webdriver.ChromeOptions()
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
op.add_argument("--headless")
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
    username = browser.find_element_by_name('username')
    password = browser.find_element_by_name('password')
except Exception:
    browser.get_screenshot_as_file("screenshot.png")

username.send_keys(kullanici_adi)
password.send_keys(sifre)

loginButton = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
loginButton.click()

time.sleep(5)

browser.get(f"https://www.instagram.com/{kullanici_adi}/followers/")
time.sleep(5)
followers = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
followers.click()


print("\n>> Going to the follower page has been successfully completed!")
time.sleep(3)

# Takipçileri Al
print(">> Getting followers. (This process may take time depending on how many followers you have.)")

jscommand = """
followers = document.querySelector(".isgrP");
followers.scrollTo(0, followers.scrollHeight);
var lenOfPage=followers.scrollHeight;
return lenOfPage;
"""

lenOfPage = browser.execute_script(jscommand)
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = browser.execute_script(jscommand)
    if lastCount == lenOfPage:
        match=True

time.sleep(2)

db = sqlite3.connect("followers.sqlite")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS followers(username TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS unfollow(username TEXT)")
db.close()

kisiler = browser.find_elements_by_css_selector("._0imsa")
takipciler = []

for kisi in kisiler:
    takipci = kisi.text
    takipciler.append(takipci)

print(">> Followers have been successfully received. Editing database.")
time.sleep(2)

def addFollower():
    db = sqlite3.connect("followers.sqlite")
    cursor = db.cursor()

    sorgu = "SELECT * FROM followers"
    cursor.execute(sorgu)
    dbKisiler = cursor.fetchall()

    for dbKisi in dbKisiler:
        if dbKisi[0] in takipciler:
            takipciler.pop(takipciler.index(dbKisi[0]))
        else:
            sorgu2 = "DELETE FROM followers WHERE username = ?"
            cursor.execute(sorgu2, (dbKisi[0],))
            db.commit()

            sorgu3 = "INSERT INTO unfollow VALUES(?)"
            cursor.execute(sorgu3, (dbKisi[0],))
            db.commit()
            print(f">> {dbKisi[0]} has stopped following you!")
    
    for i in takipciler:
        sorgu4 = "SELECT * FROM unfollow WHERE username = ?"
        cursor.execute(sorgu4, (i,))
        result = cursor.fetchall()

        if len(result) > 0:
            sorgu5 = "DELETE FROM unfollow WHERE username = ?"
            cursor.execute(sorgu5, (i,))
            db.commit()

        sorgu6 = "INSERT INTO followers VALUES(?)"
        cursor.execute(sorgu6, (i,))
        db.commit()
        print(f"New follower: {i}")
    
    db.close()
    print(">> Process completed. You can close the program and browse the database.")

addFollower()
time.sleep(2)
browser.close()
