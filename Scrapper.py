from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys
import requests, re
from bs4 import BeautifulSoup
import json


USERNAME = "USERNAME"
PASSWORD="PASSWORD"
hashTag = "#cat"


options = Options()
options.add_argument('--headless')

print("Initializing ...")
driver = webdriver.Firefox(options=options)
driver.get("https://www.instagram.com/accounts/login/")

try:
    WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.NAME,'username')))
except:
    print("Cant Load")

# LOGIN
print("Logging in as {0} ...".format(USERNAME))
driver.find_element_by_xpath("//input[@type='text']").send_keys(USERNAME)
driver.find_element_by_xpath("//input[@type='password']").send_keys(PASSWORD)
driver.find_element_by_xpath("//button[@type='submit']").click()
not_now = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
not_now = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

# Saving auth cookies and header.
print("Saving session ...")
headers = {
"User-Agent":
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}
s = requests.session()
s.headers.update(headers)

for cookie in driver.get_cookies():
    c = {cookie['name']: cookie['value']}
    s.cookies.update(c)

# SEARCH FOR THE HASH TAG AND OPEN IT
print("Search for {0}".format(hashTag))
searchbox = driver.find_element_by_xpath("//input[@placeholder='Search']")
searchbox.clear()
keyword = hashTag
searchbox.send_keys(keyword)
time.sleep(3)
searchbox.send_keys(Keys.ENTER)
searchbox.send_keys(Keys.ENTER)
time.sleep(2)

# SCROLL ENTIRE WINDOW
for _ in range(5):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    print("Scrolled",(_+1))
    time.sleep(2)


# EXTRACT ALL THE LINKS OF POSTS
print("Extracting posts ...")
p=driver.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]')
postLinks=[]
for e in p:
    postLinks.append(e.find_element_by_xpath('.//a').get_attribute("href"))

# OPEN NEW WINDOW FOR POSTS
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])

users_data=[]

# ITERATING THROUGH ALL THE POSTS
print("Extracting user data ...")
for link in postLinks:
    # GET USER PROFILE LINK
    driver.get(link)
    profile_url = driver.find_element_by_xpath('//div[@class="e1e1d"]').find_element_by_xpath('.//a').get_attribute("href")
    time.sleep(2)

    # OPEN USER PROFILE VIA REQUEST
    response = s.get(profile_url)
    content = response.text

    # EXTRACTING DATA USING REGEX FROM JSON

    # "graphql":{"user":{     -     ,"edge_felix_video_timeline"
    start = '"graphql":{"user":{'
    end = ',"edge_felix_video_timeline"'
    r = content[content.find(start)+len(start):content.rfind(end)]

    regex = []
    # followers:  ,"edge_followed_by":{"count":183401},"fbid":"17841410439120825"
    regex.append({'start':'"edge_followed_by":{"count":', 'end':'},"fbid"'})
    # followings:  ,"edge_follow":{"count":1},"follows_viewer"
    regex.append({'start':'"edge_follow":{"count":','end':'},"follows_viewer"'})
    # fullname:  "full_name":"Cats \u0026 Kitties","has_ar_effects":false
    regex.append({'start':'"full_name":"','end':'","has_ar_effects"'})
    # private/verified:  ,"is_private":false,"is_verified":false,"edge_mutual_followed_by"
    regex.append({'start':',"is_private":','end':',"is_verified"'})
    regex.append({'start':'"is_verified":','end':',"edge_mutual_followed_by"'})
    # username:  ,"username":"meowflow","connected_fb_page"
    regex.append({'start':',"username":"','end':'","connected_fb_page"'})
    user = []

    # USE REGEX TO EXTRACT ALL THE REQUIRED FIELDS
    for i in regex:
        data = r[r.find(i['start'])+len(i['start']):r.rfind(i['end'])]
        user.append(data)
    users_data.append(user)
    print(user)

driver.quit()