from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoAlertPresentException, NoSuchElementException
import os
import base64
from dotenv import load_dotenv
import time


class scrapeLinkedIn:
    def __init__(self):
        self.website = webdriver.Firefox()
        #self.website.maximize_window()

    def browser_setup(self, option):
        if option == 1:
            # Try logging in with incorrect password
            self.the_internet(self.website)
        elif option == 2:
            # Find and click checkboxes
            pass
        elif option == 3:
            # Right-click context menu
            pass
        elif option == 4:
            # Basic authorization
            self.the_internet(self.website)

    def the_internet_basic_auth(self, browser):
        browser.get('http://the-internet.herokuapp.com/basic_auth')
        time.sleep(3)
        
        dotenv_path = '.env'    #`../.env`
        load_dotenv(dotenv_path)
        username = os.getenv('THE_INTERNET_USERNAME')
        password = os.getenv('THE_INTERNET_PASSWORD')
        current_url = browser.current_url
        url_with_auth = f"https://{username}:{password}@{current_url.split('//')[1]}"
        
        try:
            alert = browser.switch_to.alert
            alert.dismiss()
        except:
            pass
        
        browser.get(url_with_auth)
        time.sleep(5)


    def the_internet(self, browser):
        browser.get('http://the-internet.herokuapp.com/')
        time.sleep(2)
        
        page_title = browser.find_element(By.TAG_NAME, "title")
        print("Page Title == " + str(page_title))
        time.sleep(1)
        basic_auth_butt = browser.find_element(By.XPATH, "//a[contains(text(), 'Basic Auth')]")
        print("Basic Auth  ->  button == " + str(basic_auth_butt))
        
        
        #@@@@@@@@@@@
        dotenv_path = '.env'    #`../.env`
        load_dotenv(dotenv_path)
        username = os.getenv('THE_INTERNET_USERNAME').strip()
        password = os.getenv('THE_INTERNET_PASSWORD').strip()
        print("Username == " + username)
        print(type(username))
        print("Password == " + password)
        print(type(password))
        current_url = browser.current_url
        print("Current URL == " + current_url)
        basic_auth_login = f'{username}:{password}' #.encode('UTF-8')
        print("Login Beginning URL == ")
        print(basic_auth_login)
        #encoded_basic = base64.b64encode(basic_auth_login).decode('UTF-8')
        #print("Login Decoded Begininng URL == " + encoded_basic)
        # headers = { 'Authorization': f'Basic {encoded_basic}' }
        try:
            #! These were supposed to bring up the developers tools but that crap didn't happen obvi
            #https://stackoverflow.com/questions/33915900/error-type-object-keys-has-no-attribute-chord
            #browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.F12)
            #browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.SHIFT + "e")
            print("GO NOW!!!! GO NICK AND DO SEX!!")
            time.sleep(5)   #Well this dumb crap worked I hate coding
            
            basic_auth_butt.click()            
            alert = browser.switch_to.alert
            sys_popup = alert.text
            print("The pop-up says == " + sys_popup)
            alert2 = WebDriverWait(browser, 10).until(EC.alert_is_present())  # ? EC = ExpectedConditions ?
            time.sleep(3)
            #alert.send_keys("admin" + Keys.TAB + "admin" + Keys.RETURN)
            #alert.send_keys(username)
            # alert.send_keys(f'{username}\ue004{password}')
            #login_url = f'http://{basic_auth_login}@the-internet.herokuapp.com/basic_auth'
            login_url = 'http://admin:admin@the-internet.herokuapp.com/basic_auth'
            #browser.get(f'http://{username}:{password}@the-internet.herokuapp.com/')
            print("Login URL == " + login_url)
            browser.get(login_url)
            time.sleep(3)
            #alert.accept()
        except UnexpectedAlertPresentException:
            pass
        #basic_auth_butt.click()
        # http_response = requests.get(current_url, headers=headers)
        # print('Well strip me nude reverend. That crap was tight!')
        #@@@@@@@@@@@
        
        print("You made it mother sucker!")
        #basic_auth_butt.click()
        #time.sleep(3)
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #   Basic Authorization (popups always appear!)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        try:
            alert = browser.switch_to.alert
            alert.dismiss()
            print('Eff that homo alert')
        except:
            pass
        
        #\\\\\\\\\\\\\\\\\\\\\\ This crap might work idk
        # alert = browser.switch_to.alert
        # alert.dismiss()
        # time.sleep(5)
        # print('Eff that homo alert')
        #\\\\\\\\\\\\\\\\\\\\\\
        
        #This is the 'relative path'(start from code go to destination) rather the 'absolute path' starts from the root 'C:/Users/user

        return
    
    
    
# def alert_type(self, browser):
    # username = 'admin'
    # password = 'admin'
    # try:
    #     # Check if it's a system level authentication dialog box
    #     alert = WebDriverWait(browser, 5).until(EC.alert_is_present())
    #     alert.send_keys(username + Keys.TAB + password + Keys.RETURN)
    #     return

    # except NoAlertPresentException:
    #     # Check if it's an iFrame alert
    #     try:
    #         iframe = WebDriverWait(browser, 5).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe")))
    #         WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit"))).click()
    #         return
    #     except (TimeoutException, NoSuchElementException):
    #         # Check if it's a user made alert
    #         if len(browser.window_handles) > 1:
    #             browser.switch_to.window(browser.window_handles[1])
    #             # Add code here to handle the user made alert
    #             return
    #         else:
    #             # Handle the case where no alert is present
    #             return   
    





if __name__ == '__main__':
    scraper = scrapeLinkedIn()
    scraper.browser_setup(4)












# Current URL == http://the-internet.herokuapp.com/
# Login Beginning URL ==
# b'admin:admin@'
# Login Decoded Begininng URL == YWRtaW46YWRtaW5A
# The pop-up says == This site is asking you to sign in.
# Login URL == http://YWRtaW46YWRtaW5Athe-internet.herokuapp.com/




# Current URL == http://the-internet.herokuapp.com/
# Login Beginning URL ==
# b"b'admin':b'admin'@"
# Login Decoded Begininng URL == YidhZG1pbic6YidhZG1pbidA
# The pop-up says == This site is asking you to sign in.
# Login URL == http://YidhZG1pbic6YidhZG1pbidAthe-internet.herokuapp.com/

