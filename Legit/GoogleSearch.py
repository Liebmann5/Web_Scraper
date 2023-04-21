from bs4 import BeautifulSoup
from selenium import webdriver

#from dotenv import load_dotenv
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

class scraperGoogle():
    
    def __init__(self, browser):
        self.browser = browser
        self.job_titles = []
        self.good_locations = None
        self.bad_locations = None
        self.list_first_index = 0
        self.list_last_index = 0
        self.links_to_jobs = []
        
    def ludacris_speed(self):
        self.job_titles.append("software engineer")
        self.job_titles.append("backend engineer")
        self.search_for_jobs()
    
    def user_requirements(self):
        self.ludacris_speed()
        
        print("Well well well. Somebody needs a job... figures someone like you"
              + " is wanting more money! What a weiner your parents raised. You weiner!")
        #time.sleep(1)
        print("Any who just go ahead and type out the job title you want. "
              + " each job title press ENTER! (When you press ENTER it will probably take "
              + "you to the next line, this is normal... illiterately speaking of course)")
        #time.sleep(1)
        print("Try and keep it to around 3-4 you eager eagle. Exceling past these "
              + "numbers will yield less results, so thats why.")
        #time.sleep(1)
        print("Fianlly for the love of the Hoover Dam please spell the everything correctly! "
              + "If you're not confident then highlight the name with your mouse and click\n"
              + " COPY. When you come back here just right click. If you don't have a right"
              + " click well then huh. Life is tough but get your crap together cause idk")
        #time.sleep(1)
        #TODO       
        # print("Ok now yrs of exp?")
        # user_exp = input()
        # yrs_of_exp.append(user_exp)
        #     -> Add as global like this =>   yrs_of_exp = None  =>  b/c it's an empty string
        # print("Ok and which locations?")
        # location = input()
        # (.env).add(location)    #so it's saved on their system
        # user_location.appemd(location)
        #     ==> When printed in search do   ==>   " & near=" + user_location
        #self.search_for_jobs(self)
        return self.links_to_jobs

    def search_for_jobs(self):     #! (self, self.browser) -> self.browser as parameter is dumb b/c arguments are meant to accept values from other places and self.browser's value was set in the constructor so... piece the crap together Nick
        job_titles = self.job_titles  #TODO: < Ummmm does that work
        
        print('Searching for ' + ", ".join(job_titles) + ' jobs...    you lazy son of 21 guns')
        search_bar = self.browser.find_element(By.NAME, "q")
        search_bar.clear()
        search_bar.send_keys('site:lever.co | site:greenhouse.io | site:workday.com')
        print('1/2')
        time.sleep(1)
        job_titles_string = ' ("'
        for i, job in enumerate(job_titles):
            if i == len(job_titles)-1 or len(job_titles) == 0:
                job_titles_string += (job + '")')
            else:
                job_titles_string += (job + '" | "')
        search_bar.send_keys(job_titles_string)
        print('2/2')
        print("Searching google for...       adult films?")
        time.sleep(1)

        self.search_locations(self, search_bar)
        return
    
    #TODO
    def search_locations(self, search_bar):
        self.filter_search_time_frame(search_bar)
        
        #NOTE: [if not variable] checks if the length of variable is = to 0; variable here is a 'list[]' too!! 
        if not self.good_locations and not self.bad_locations:
            #self.filter_search_time_frame(self, browser)
            self.filter_search_time_frame(search_bar)
        
        #NOTE: HERE add SPACE to the BEGININNG because we don't care about the end!!!
        search_location = " & "
        for count, add_location in enumerate(self.good_locations):
            if count == len(self.good_locations):
                search_location += (" near=" + add_location + " ")
                #! ADD: Find out how to add more location!!!!!                
        for count, exclude_location in self.bad_locations:
            if count == len(self.bad_locations):
                search_location += ("!(near=" + exclude_location + ")")
        
        search_bar.send_keys(search_location)
        self.filter_search_time_frame(self, search_bar)
        return
    
    def filter_search_time_frame(self, browser, search_bar):
        search_bar.send_keys(Keys.RETURN)
        print("TAAAA DDDAAAAAA")
        time.sleep(1)
        
        tools_butt = browser.find_element(By.XPATH, "//div[text()='Tools']")
        tools_butt.click()
        
        any_time_butt = browser.find_element(By.XPATH, "//div[text()='Any time']")
        any_time_butt.click()
        decisi = "24"
        
        if decisi == "24":
            past_24 = browser.find_element(By.XPATH, "//a[text()='Past 24 hours']")
            past_24.click()
        elif decisi == "7":
            past_week = browser.find_element(By.XPATH, "//a[text()='Past week']")
            past_week.click()
        else:
            raise TypeError('ERROR: Didnt pick a registered time!')
        print("Filtering by past " + decisi)
        time.sleep(1)
        self.search_results(browser, self.list_first_index, self.list_last_index)
        return
        
    def search_results(self, list_first_index, list_last_index):
        if list_first_index == 0:
            search_results = self.browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index})")
            print(f"Number of search results: {len(search_results)}")
            list_last_index = len(search_results)
            
        if list_first_index == 0:
            search_results = self.browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index})")
            print(f"Number of search results: {len(search_results)}")
            list_last_index = len(search_results)
        else:
            search_results = self.browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index+1})")
        
        for count, results_link in enumerate(search_results, list_first_index):
            print('--------------------------------')
            print(str(count+1) + "/" + str(list_last_index))
            print(results_link)
            link = results_link.find_element(By.CSS_SELECTOR, "a")  #"h3.LC201b > a"
            print(f"Here is link #{count+1}: ", end="")
            job_link = link.get_attribute("href")
            self.links_to_jobs.append(job_link)
            #print(link.get_attribute("href"))
            print(job_link)

            google_search_buttony = link.find_element(By.TAG_NAME, "h3")
            google_search_button = google_search_buttony.get_attribute('innerHTML')
            
            if count == list_last_index:
                list_first_index = list_last_index
                break
        print("All done loser!")
        time.sleep(1)
        #TODO: Write a condition that calls increment_search when no more links and the call adds 'search_results'
        self.increment_search_results(list_first_index, list_last_index, google_search_button)
        return list_first_index, list_last_index
    
    def increment_search_results(self, list_first_index, list_last_index, google_search_button):
        current_height = self.browser.execute_script("return document.body.scrollHeight")
        print('\n\n\n')
        print("increment_search_results")
        print("****************************************************************")
        print("Current Height == " + str(current_height))
        
        while True:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            print("Scrolled...")          
            current_list_length = list_last_index-list_first_index
            if (current_list_length%100) == 1:
                print("Length of the current list == " + str(current_list_length))
            search_results = self.browser.find_elements(By.XPATH, "//div[@class='g']")
            if len(search_results) < list_last_index:
                print("No more search results")
                break
            # try:
            #     no_more_results = browser.find_element(By.XPATH, "//a[text()='repeat the search with the omitted results included']")
            #     print("No more search results")
            #     break
            # except NoSuchElementException:
            #     pass
            #**************************************************************************************************************
            # new_height = browser.execute_script("return document.body.scrollHeight")
            # print("New Height == " + str(new_height))
            
            #if new_height == current_height:
            try:
                more_results = self.browser.find_element(By.XPATH, "//span[text()='More results']")
                if more_results:
                    print("Found the more_results == ", end="")
                    print(more_results)
                    more_results.click()
                    print("Clicked 'More results' button")
                    time.sleep(1)
                elif not more_results:
                    print("NOTHING == more_results")
            except NoSuchElementException:
                return  ("ERROR: Didn't work I guess idk??")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            print("New Height == " + str(new_height))
            if new_height == current_height:
                print("No more search results")
                break
        #--------------------------------------------------------------------   
            current_height = new_height
            list_first_index, list_last_index = self.search_results(list_first_index, list_last_index)
            print("Current height == " + str(current_height))
        print("****************************************************************")
        print('\n\n\n')
        
        print("Scrolled to the end of search results, GOOBER!")
        time.sleep(2.5)
        print("++++++++++++++++++++++++++++++++++++++++++++++")

        # scraperGoogleJob(self.links_to_jobs, browser).deal_with_links(google_search_button)
        self.click_this_thing(google_search_button)
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        return
        
    def click_this_thing(self, google_search_button):
        application_company = None
        
        for job_index in self.links_to_jobs[::-1]:
            # print("D")
            # d = "h"
            # if d == "d":
            #     h3_element = self.browser.find_element(By.XPATH, '//h3')
            #     ancestor_element = h3_element.find_element(By.XPATH, './ancestor::*')
            #     print(ancestor_element.get_attribute('outerHTML'))
            #     #linky = self.browser.get(job_index)
            #     #print(linky)
            #     print("\D/")
            #     selenium_google_link = self.browser.find_element(By.XPATH, f'//a/h3[text()="{google_search_button}"]')
            #     parent_a_tag_xpath = selenium_google_link.find_element(By.XPATH, '..').get_attribute('outerHTML')
            #     print(parent_a_tag_xpath)
            #     print("Defence")
            selenium_google_link = self.browser.find_element(By.XPATH, f'//ancestor::a/h3[not(descendant::br)][contains(text(), "{google_search_button}")]')
            selenium_google_link.click()
            self.browser.implicitly_wait(5)
            time.sleep(3)
        return






#site:lever.co | site:greenhouse.io | site:workday.com ("Software Engineer" | "Backend Engineer") -Senior -Sr location:us




















