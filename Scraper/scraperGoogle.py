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

from scraperGoogleJob import scraperGoogleJob   #? ERASED THE b (in import)


class scraperGoogle():
    
    def __init__(self):
        print(scraperGoogleJob)   #? ERASED THE b
        self.browser = None
        self.job_titles = []
        self.list_first_index = 0
        self.list_last_index = 0
        self.links_to_jobs = []
    
    def user_requirements(self):
        #global job_titles     #! ERROR: the code didn't like this with .append() for whatever reason!!!?!?!?
        
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
        print("When you are done, type ONLY the number of your preferred web browser then press ENTER")
        print(f"\t1) FireFox")
        print(f"\t2) Safari")
        print(f"\t3) Chrome")
        print(f"\t4) Edge")
        while True:
            user_jobs = input()
            user_jobs.strip()
            #if user_jobs == 1:   #! ERROR: comparing a string to an int!!!!
            if user_jobs == "1":
                return 1, " FireFox "
            elif user_jobs == "2":
                return 2, " Safari "
            elif user_jobs == "3":
                return 3, " Chrome "
            elif user_jobs == "4":
                return 4, " Edge "
            else:     #TODO: Make else just check OS and return number of that OS's web browser!!!
                self.job_titles.append(user_jobs)
         
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
    
    def browser_setup(self, test):
        #user_browser_choice, browser_name = self.user_requirements()
        user_browser_choice, browser_name = 2, " Safari "
        self.job_titles.append("software engineer")
        self.job_titles.append("backend engineer")
        print('Execution Started -- Opening' + browser_name + 'Browser')
        
        if user_browser_choice == 1:
            browser = self.browser
            
            options = FirefoxOptions()
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("extensions.enabledScopes", 0)
            options.set_preference("browser.toolbars.bookmarks.visibilty", "never")
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("places.history.enabled", False)
            
            browser = webdriver.Firefox(options=options)
            browser.set_page_load_timeout(30)
        elif user_browser_choice == 2:
            browser = self.browser
            
            options = SafariOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
                
            browser = webdriver.Safari(options=options)
            browser.set_page_load_timeout(30)
        elif user_browser_choice == 3:
            browser = self.browser
            
            options = ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            
            browser = webdriver.Chrome(options=options)
            browser.set_page_load_timeout(30)
        
        if(test == 0):
            browser.get('https://www.google.com')
            self.search_for_jobs(browser)
        else:
            raise ConnectionError('ERROR: Check Internet Connection')
        
        browser.quit()
        print('Execution Ending -- Webdriver session is Closing')
        
    def search_for_jobs(self, browser):
        job_titles = self.job_titles
        
        print('Searching for ' + ", ".join(job_titles) + ' jobs...    you lazy son of 21 guns')
        search_bar = browser.find_element(By.NAME, "q")
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
        #TODO: Uncomment below and erease    .search_time_frame() !!!!
        #self.search_locations(self, browser, search_bar)
        self.search_time_frame(browser, search_bar)
        return
    
    #TODO
    def search_locations(self, browser, search_bar):
        global good_locations
        global bad_locations
        
        #NOTE: [if not variable] checks if the length of variable is = to 0; variable here is a 'list[]' too!! 
        if not good_locations and not bad_locations:
            self.search_time_frame(self, browser)
        
        #NOTE: HERE add SPACE to the BEGININNG because we don't care about the end!!!
        search_location = " & "
        for count, add_location in enumerate(good_locations):
            if count == len(good_locations):
                search_location += (" near=" + add_location + " ")
                #! ADD: Find out how to add more location!!!!!                
        for count, exclude_location in bad_locations:
            if count == len(bad_locations):
                search_location += ("!(near=" + exclude_location + ")")
        
        search_bar.send_keys(search_location)
        self.search_time_frame(self, browser, search_bar)
        return
    
    def search_time_frame(self, browser, search_bar):
        search_bar.send_keys(Keys.RETURN)
        print("TAAAADDDAAAAAA")
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
        
    def search_results(self, browser, list_first_index, list_last_index):
        if list_first_index == 0:
            search_results = browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index})")
            print(f"Number of search results: {len(search_results)}")
            list_last_index = len(search_results)
            
        if list_first_index == 0:
            search_results = browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index})")
            print(f"Number of search results: {len(search_results)}")
            list_last_index = len(search_results)
        else:
            search_results = browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index+1})")
        
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
            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            # scraperGoogleJob(job_link)
            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            google_search_buttony = link.find_element(By.TAG_NAME, "h3")
            google_search_button = google_search_buttony.get_attribute('innerHTML')
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            if count == list_last_index:
                list_first_index = list_last_index
                break
        print("All done loser!")
        time.sleep(1)
        #TODO: Write a condition that calls increment_search when no more links and the call adds 'search_results'
        self.increment_search_results(browser, list_first_index, list_last_index, google_search_button)
        return list_first_index, list_last_index
    
    def increment_search_results(self, browser, list_first_index, list_last_index, google_search_button):
        current_height = browser.execute_script("return document.body.scrollHeight")
        print('\n\n\n')
        print("increment_search_results")
        print("****************************************************************")
        print("Current Height == " + str(current_height))
        
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            print("Scrolled...")
           
            current_list_length = list_last_index-list_first_index
            #**************************************************************************************************************
            if (current_list_length%100) == 1:
                print("Length of the current list == " + str(current_list_length))
        #--------------------------------------------------------------------
            search_results = browser.find_elements(By.XPATH, "//div[@class='g']")
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
                more_results = browser.find_element(By.XPATH, "//span[text()='More results']")
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
            new_height = browser.execute_script("return document.body.scrollHeight")
            print("New Height == " + str(new_height))
            if new_height == current_height:
                print("No more search results")
                break
        #--------------------------------------------------------------------   
            current_height = new_height
            list_first_index, list_last_index = self.search_results(browser, list_first_index, list_last_index)
            print("Current height == " + str(current_height))
        print("****************************************************************")
        print('\n\n\n')
        
        print("Scrolled to the end of search results, GOOBER!")
        time.sleep(2.5)
        print("++++++++++++++++++++++++++++++++++++++++++++++")

        scraperGoogleJob(self.links_to_jobs, browser).deal_with_links(google_search_button)
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        return
        

if __name__ == '__main__':
    scraper = scraperGoogle()
    scraper.browser_setup(0)







#site:lever.co | site:greenhouse.io | site:workday.com ("Software Engineer" | "Backend Engineer") -Senior -Sr location:us






# In order to show you the most relevant results, we have omitted some entries very similar to
# the 225 already displayed.
# If you like, you can "repeat the search with the omitted results included."







# HOW TO SET UP SAFARI !!!!!
#    1) Open Safari.
#    2) Click on Safari in the top menu bar.
#    3) Click on Preferences.
#    4) Click on Advanced.
#    5) At the bottom, check the box next to "Show Develop menu in menu bar".
#    6) Click on Develop in the top menu bar.
#    7) Click on Allow Remote Automation.



