from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException

class scraperGoogle():
    
    def __init__(self, browser):
        self.browser = browser
        self.user_desired_jobs = []
        self.good_locations = None
        self.bad_locations = None
        self.list_first_index = 0
        self.list_last_index = 0
        self.links_to_jobs = []
        self.previous_results_count = 0
        self.job_links_counter = 0
        self.results_from_search = []
        self.google_search_results_links = []
        #TODO: No longer needed so get rid of this
        self.last_link_from_google_search = None
        
        
        #NOTE: NEW  NEW  NEW  NEW  NEW  NEW  NEW  NEW  NEW  NEW
        self.users_job_search_requirements = {}
        
        
        
        #! NEW  NEW  NEW  NEW  NEW  NEW  NEW  NEW  NEW
        self.user_preferred_workplaceType = ["in-office", "hybrid", "remote"]
        self.user_preferred_locations = []
        #NOTE: if senior_experience is true then everything is fair game but...  if it's False create this new variable!!!!
        # if senior_experience == False:
        #     self.avoid_these_job_titles = ["senior", "sr", "principal", "lead", "manager"]
        #self.senior_experience = senior_experience
        self.avoid_these_job_titles = ["senior", "sr", "principal", "lead", "manager"]
        
        
        
        
    
    #TODO: Uhhhhh?  Maybe this should be added to ManageUserJobSearch.py?!?!?!
    def fill_users_job_search_requirements(self, *args):
        for arg in args:
            #Fairly certain this is absolutely wrong but it's just here as a Note...
            self.users_job_search_requirements('user_desired_job_title').append(arg)
        
    #TODO: ENSURE THIS IS CORRECT !!!!!
        #TODO: Add variable  user_blacklisted_locations == self.bad_locations
    def init_users_job_search_requirements(self):
        self.users_job_search_requirements = {
            "user_desired_job_title": self.user_desired_jobs,
            "user_preferred_locations": self.user_preferred_locations,
            "user_preferred_workplaceType": self.user_preferred_workplaceType,
            "employment_type": [],  #Not really something I'm checking for
            "entry_level": True, 
        }
    
    
    
    
    
    
    #TODO: LAST_APPLIED => If anythng less than 3 days -> 24 hrs | If anything > 3 days filter by -> Past Week | If anything > 2 weeks just do -> anytime
        #TODO: But show the user LAST_APPLIED and let them pick
        
    def ludacris_speed(self):
        self.user_desired_jobs.append("software engineer")
        return
    
    def plaid_speed(self):
        self.user_desired_jobs.append("software engineer")
        self.user_desired_jobs.append("backend engineer")
        self.user_desired_jobs.append("full-stack engineer")
        #self.user_desired_jobs.append("frontend engineer")
        #self.user_desired_jobs.append("engineer")
        self.search_for_jobs()
        return
    
    def purely_for_testing_and_examples(self, walkthrough_choice):
        if walkthrough_choice == 'ludacris':
            self.ludacris_speed()
        elif walkthrough_choice == 'plaid':
            self.plaid_speed()
        self.new_new_print_google_search_results()
        print("Returning back to JobSearchWorkflow")
        time.sleep(2)
        return self.google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs
    
    def user_requirements(self):
        self.ludacris_speed()
        
        self.search_for_jobs()
        self.new_new_print_google_search_results()
        print("Returning back to JobSearchWorkflow\n\n")
        time.sleep(2)
        #return self.google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs, self.user_preferred_locations, self.user_preferred_workplaceType
        self.init_users_job_search_requirements()
        return self.google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs, self.user_preferred_locations, self.user_preferred_workplaceType, self.users_job_search_requirements

    def search_for_jobs(self):     #! (self, self.browser) -> self.browser as parameter is dumb b/c arguments are meant to accept values from other places and self.browser's value was set in the constructor so... piece the stuff together Nick
        job_titles = self.user_desired_jobs  #TODO: < Ummmm does that work
        
        print('Searching for ' + ", ".join(job_titles) + ' jobs...    you lazy son of 21 guns')
        search_bar = self.browser.find_element(By.NAME, "q")
        search_bar.clear()
        search_bar.send_keys('site:lever.co | site:greenhouse.io')     #('site:lever.co | site:greenhouse.io | site:workday.com')
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

        self.search_locations(search_bar)
        return
    
    '''
    #NOTE: google already returns too few jobs AND since time is not of the essance... this will hopefully lead the users to find some hidden gems!!!
    # def filter_out_experience(self, search_bar):
    #     if self.senior_experience == False:
    #         search_bar.send_keys(('-'.join(self.avoid_these_job_titles) + ' '))
    '''
    
    #NOTE: Ok so because google can't do it's job the locations are more so just suggestions!! At least
        #for all the jobs in this 'returned list' from the 'google search'... once I get to the internal
        #company job list I can prioritize location!!!
    #TODO       -   -   -   -   - > user_preferred_locations
    def search_locations(self, search_bar):
        requested_job_locations = None
        if not self.user_preferred_locations:
            self.filter_search_time_frame(search_bar)
            #?????? Adding a return right here cause if I don't then won't the rest of this method run?????
            return
        else:
            requested_job_locations = self.user_preferred_locations
        
        print("Specifying search to only return job's within the " + ", ".join(requested_job_locations) + " area")
        print("1/2")
        time.sleep(1)
        job_locations_string = ' ("'
        for i, location in enumerate(requested_job_locations):
            if i == len(requested_job_locations):
                job_locations_string += (location + '") ')
            else:
                job_locations_string += (location + '" | "')
        search_bar.send_keys(job_locations_string)
        print("2/2")
        
        




        
        # #NOTE: [if not variable] checks if the length of variable is = to 0; variable here is a 'list[]' too!! 
        # if not self.good_locations and not self.bad_locations:
        #     self.filter_search_time_frame(search_bar)
        #     return 
        
        # #NOTE: HERE add SPACE to the BEGININNG because we don't care about the end!!!
        # search_location = " & "
        # for count, add_location in enumerate(self.good_locations):
        #     if count == len(self.good_locations):
        #         search_location += (" near=" + add_location + " ")
        #         #! ADD: Find out how to add more location!!!!!                
        # for count, exclude_location in self.bad_locations:
        #     if count == len(self.bad_locations):
        #         search_location += ("!(near=" + exclude_location + ")")
        
        # search_bar.send_keys(search_location)
        self.filter_search_time_frame(search_bar)
        return
    
    def filter_search_time_frame(self, search_bar):
        search_bar.send_keys(Keys.RETURN)
        print("TAAAA DDDAAAAAA")
        time.sleep(1)
        self.adjust_viewport()
        print("GET SUCKED WIZARD!")
        time.sleep(1)
        
        tools_butt = self.browser.find_element(By.XPATH, "//div[text()='Tools']")
        tools_butt.click()
        
        any_time_butt = self.browser.find_element(By.XPATH, "//div[text()='Any time']")
        any_time_butt.click()
        decisi = "24"
        
        if decisi == "24":
            past_24 = self.browser.find_element(By.XPATH, "//a[text()='Past 24 hours']")
            past_24.click()
        elif decisi == "7":
            past_week = self.browser.find_element(By.XPATH, "//a[text()='Past week']")
            past_week.click()
        else:
            raise TypeError('ERROR: Didnt pick a registered time!')
        print("Filtering by past " + decisi)
        time.sleep(1)
        #self.search_results(self.list_first_index, self.list_last_index)
        #self.job_search_workflow()
        #self.search_results(self.list_first_index)
        self.process_search_results()
        return
    
    def adjust_viewport(self):   
        # Get the current window size
        window_width = self.browser.execute_script("return window.innerWidth;")
        window_height = self.browser.execute_script("return window.innerHeight;")

        # Set the viewport to match the window size
        self.browser.execute_script(f"document.documentElement.style.setProperty('width', '{window_width}px');")
        self.browser.execute_script(f"document.documentElement.style.setProperty('height', '{window_height}px');")
        self.browser.execute_script("document.documentElement.style.setProperty('overflow', 'hidden');")
    


    def scroll_to_bottom(self):
        prev_height = self.browser.execute_script("return document.body.scrollHeight")
        print('\n\n\n')
        print("increment_search_results")
        print("****************************************************************")
        print("Current Height == " + str(prev_height))
        
        #! This is what does the actual scrolling!!!
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #------------------------------------------------------------------------------------------------------
        #     self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # ============
        #     # Scroll down in smaller increments
        #     scroll_increment = current_height // 5
        #     for _ in range(5):
        #         self.browser.execute_script(f"window.scrollBy(0, {scroll_increment});")
        #         time.sleep(1)
        time.sleep(1)
        print("Scrolled...")
        
        new_height = self.browser.execute_script("return document.body.scrollHeight")
        print("New Height == " + str(new_height))
        return new_height != prev_height

    def process_search_results(self):
        list_first_index = 0
        list_last_index = 0
        while True:
            list_last_index = self.search_results(list_first_index, list_last_index)
            
            if not self.scroll_to_bottom():
                if self.end_of_search():
                    print("I'm the issue 2")
                    break
                
                if not self.get_more_results():
                    print("I'm the issue 3")
                    break
            # else:
            #     list_first_index = list_last_index
        print("I'm the issue 4")
            
    def search_results(self, list_first_index, list_last_index):
        # Wait for the last result from the previous search to appear on the page
        # if self.results_from_search:
        #     last_result = self.results_from_search[-1]
        #     WebDriverWait(self.browser, 10).until(
        #         EC.visibility_of(last_result)
        #     )
        initial_length = len(self.results_from_search)
        
        if list_first_index == 0:
            self.results_from_search = self.browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index})")
            list_last_index = len(self.results_from_search)
        else:
            self.results_from_search = self.browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index+1})")
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! vvvvvvvvvvvvvvvvvvvvvvv  IF THERE ARE ANY ISSUES ITS B/C OF THIS !!!!!!!!!!!!!
            list_last_index = list_first_index + len(self.results_from_search)

        for count, results_link in enumerate(self.results_from_search[initial_length:], initial_length):
            print('--------------------------------')
            print(str(count+1) + "/" + str(list_last_index))
            print(results_link)
            link = results_link.find_element(By.CSS_SELECTOR, "a")  #"h3.LC201b > a"
            print(f"Here is link #{count+1}: ", end="")
            job_link = link.get_attribute("href")
            print(job_link)
            self.google_search_results_links.append(job_link)
            
            if (count+1) == list_last_index:
                self.last_link_from_google_search = results_link
                print("\nvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
                print(self.last_link_from_google_search)
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
            
            #TODO: I have no effing idea what the heck this is supposed to do or it's purpose... I'm dumb
            if count == list_last_index:
                list_first_index = list_last_index
                break
        print("\nI am at end of search_results()...")
        print("First Index = " + str(list_first_index) + " && Last Index = " + str(list_last_index))
        return list_last_index

    def get_more_results(self):
        try:
            more_results = self.browser.find_element(By.XPATH, "//span[text()='More results']")
            if more_results:
                print("Found the more_results button")
                more_results.click()
                print("Clicked 'More results' button")
                time.sleep(2)
                return True
            else:
                print("No 'More results' button found")
                print("THIS COULD BE THE REASON FOR ERRORS!! idk though dog... soundproof spectacles")
                return False
        except NoSuchElementException:
            print("No 'More results' button found")
            return False

    def end_of_search(self):
        try:
            no_more_results = self.browser.find_element(By.XPATH, "//a[text()='repeat the search with the omitted results included']")
            if no_more_results:
                print("No more search results")
                time.sleep(2)
                return True
        except NoSuchElementException:
            pass
        return False 
    
    
    

    def print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.results_from_search):
            self.job_links_counter += 1
            print("Result #" + str(self.job_links_counter) + " from Google Seaech")
            print("\tJob Title: ", end="")
            print(job)
            print("\tLink to Job: ", end="")
            print(self.links_to_jobs[i])
        print('--------------------------------------------')
        #time.sleep(30)
        return
    
    def new_print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.results_from_search):
            self.job_links_counter += 1
            print("Result #" + str(i+1) + " from Google Seaech")
            print("\tJob Title: ", end="")
            print(job)
            print("\tLink to Job: ", end="")
            print(self.links_to_jobs[i])
        print('--------------------------------------------')
        #time.sleep(30)
        return
    
    def new_new_print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.google_search_results_links):
            self.job_links_counter += 1
            print("Result #" + str(i+1) + " from Google Seaech")
            print("\tJob Title: ", end="")
            print(job)
            print("\tLink to Job: ", end="")
            print(self.google_search_results_links[i])
        print('--------------------------------------------')
        #time.sleep(30)
        return











#site:lever.co | site:greenhouse.io | site:workday.com ("Software Engineer" | "Backend Engineer") -Senior -Sr location:us




#jobs.polymer.co





