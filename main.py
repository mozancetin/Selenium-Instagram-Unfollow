from selenium import webdriver
from getpass import getpass
import time
import sqlite3

kullanici_adi = str(input("Instagram Username: "))
sifre = str(input("Password: "))

op = webdriver.ChromeOptions()
op.add_argument("--headless")
op.add_argument("--window-size=1920, 1080")
browser = webdriver.Chrome(options=op)

# Giriş Yap
browser.get("https://www.instagram.com/")
print("Logging in.")

time.sleep(2)

username = browser.find_element_by_name("username")
password = browser.find_element_by_name("password")

username.send_keys(kullanici_adi)
password.send_keys(sifre)

loginButton = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
loginButton.click()

time.sleep(3)

menu = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a')
menu.click()

print("Successfully Logged In!")

time.sleep(2)

# Takipçi Sayfasına Ulaş
print("Going to the follower page.")

profilButton = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span')
profilButton.click()
time.sleep(2)

profil = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div/div[2]/div[2]/a[1]')
profil.click()

time.sleep(2)

followers = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
followers.click()

print("Going to the follower page has been successfully completed!")
time.sleep(3)

# Takipçileri Al
print("Getting followers. (This process may take time depending on how many followers you have.)")

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
    time.sleep(1)
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

print("Followers have been successfully received. Editing database.")
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
            print(f"{dbKisi[0]} has stopped following you!")
    
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
    print("Process completed. You can close the program and browse the database.")

addFollower()
time.sleep(2)
browser.close()
