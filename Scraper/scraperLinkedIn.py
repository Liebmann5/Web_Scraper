from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
#OOOOORRRRRRRRR     https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5
#from decouple import config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     IN ORDER TO RUN MAKE SURE PYTHON INTERPRETER == 311
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class scrapeLinkedIn():
    
    browser = None
    
    
    def someCrap(self, test):
        print('Execution started-- Opening Firefox Browser')
        
        options = Options()
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("extensions.enabledScopes", 0)
        options.set_preference("browser.bookmarks.showMobileBookmarks", False)
        options.set_preference("browser.toolbars.bookmarks.visibilty", "never")
        options.set_preference("signon.rememberSignons", False)
        options.set_preference("places.history.enabled", False)
        
        browser = webdriver.Firefox(options=options)
        browser.set_page_load_timeout(30)
        
        if test == 0:
            browser.get('http://www.yahoo.com')
        elif test == 1:
            browser.get('https://linkedin.com')
        assert 'Yahoo' in browser.title
        
        elem = browser.find_element(By.NAME, 'p')
        elem.send_keys('seleniumhq' +  Keys.RETURN)
        
        time.sleep(5)
        
        browser.quit()
        print('Execution ending-- Webdriver session is closed')
    
        #"C:\Program Files\Mozilla Firefox\firefox.exe"
    
    
    
    
    
    def linkedin_login(browser):
        if:
            username = browser.find_element_by_id("username")
        elif:
            va=2
            
        username.send_keys(os.getenv('LINKEDIN_USERNAME'))
        password.send_keys(os.getenv('LINKEDIN_PASSWORD'))
        
        browser.find_element_by_xpath("//button[@type='submit']").click()













   
    
if __name__ == '__main__':
    scraper = scrapeLinkedIn()
    scraper.someCrap(0)
    
    
    
    
    
# HEADLESS MODE
# options = webdriver.FirefoxOptions()
# options.add_argument('-headless')
# browser = webdriver.Firefox(firefox_options=options)