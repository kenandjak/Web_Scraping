from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.environ.get("DATABASE_URL"))
db = client["Scraping"]
collection = db["blog"]


opt = Options()
opt.add_argument('window-size=900, 1200')

browser = webdriver.Firefox(options=opt)
browser.get('https://metos.com.br/blog/')

sleep(3)

i = 0
while(i < 5):
    elements = browser.find_elements(By.CLASS_NAME, 'elementor-widget-container')
    main = elements[4]
    posts = main.find_elements(By.CLASS_NAME, 'elementor-post__text')
    posts_lists = []
    for post in posts:
        title = post.find_element(By.CLASS_NAME, 'elementor-post__title')
        link = post.find_element(By.TAG_NAME, 'a').get_attribute('href')
        date = post.find_element(By.CLASS_NAME, 'elementor-post__meta-data')
        blog_posts = {
            'title': title.text,
            'link': link,
            'date': date.text
        }
        posts_lists.append(blog_posts)
    if(posts_lists):
        collection.insert_many(posts_lists)
    print(i+1)
    i += 1
    if(i < 5):
        searchButton = main.find_element(By.CSS_SELECTOR, 'nav a.page-numbers.next')
        browser.execute_script("arguments[0].scrollIntoView(true);", searchButton)
        sleep(2)
        searchButton.click()