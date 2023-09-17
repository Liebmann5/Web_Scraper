import time
import contextlib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException


from UsersFirstUse import UntouchedUser

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
        
        
        self.users_job_search_requirements = {}
        self.google_search_banner_titles = []
        
        
        
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
            "user_desired_job_titles": self.user_desired_jobs,
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
        #self.ludacris_speed()
        self.users_job_search_requirements = UntouchedUser().setup_test()
        self.user_desired_jobs = self.users_job_search_requirements["user_desired_job_titles"]
        #self.bad_locations = self.users_job_search_requirements["user_preferred_locations"]
        
        self.search_for_jobs()
        self.new_new_print_google_search_results()
        print("Returning back to JobSearchWorkflow\n\n")
        time.sleep(2)
        #return self.google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs, self.user_preferred_locations, self.user_preferred_workplaceType
        #self.init_users_job_search_requirements()
        return self.google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs, self.user_preferred_locations, self.user_preferred_workplaceType, self.users_job_search_requirements

    def search_for_jobs(self):
        job_titles = self.user_desired_jobs  #TODO: < Ummmm does that work

        print('Searching for ' + ", ".join(job_titles) + ' jobs...')
        search_bar = self.browser.find_element(By.NAME, "q")
        search_bar.clear()
        search_bar.send_keys('site:lever.co | site:greenhouse.io')     #('site:lever.co | site:greenhouse.io | site:workday.com')
        print('1/2')
        time.sleep(1)
        job_titles_string = ' ("'
        for i, job in enumerate(job_titles):
            if i == len(job_titles)-1 or len(job_titles) == 0:
                job_titles_string += f'{job}")'
            else:
                job_titles_string += f'{job}" | "'
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
    
    #TODO       -   -   -   -   - > user_preferred_locations
    def search_locations(self, search_bar):
        requested_job_locations = None
        if not self.user_preferred_locations:
            self.filter_search_time_frame(search_bar)
            #TODO: remove this 'return' when ready Forest
            return
        else:
            requested_job_locations = self.user_preferred_locations

        print("Specifying search to only return job's within the " + ", ".join(requested_job_locations) + " area...  maybe")
        print("1/2")
        time.sleep(1)
        print("most likely not though")
        job_locations_string = ' ("'
        for i, location in enumerate(requested_job_locations):
            if i == len(requested_job_locations):
                job_locations_string += f'{location}") '
            else:
                job_locations_string += f'{location}" | "'
        search_bar.send_keys(job_locations_string)
        print("2/2")
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
        print(f"Filtering by past {decisi}")
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
        print(f"Current Height == {str(prev_height)}")

        #! This is what does the actual scrolling!!!
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        print("Scrolled...")

        new_height = self.browser.execute_script("return document.body.scrollHeight")
        print(f"New Height == {str(new_height)}")
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
        print("I'm the issue 4")
            
    def search_results(self, list_first_index, list_last_index):
        #TODO: I forgot where this was supposed to be applied?!?!?!?!
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
            list_last_index = list_first_index + len(self.results_from_search)

        for count, results_link in enumerate(self.results_from_search[initial_length:], initial_length):
            print('--------------------------------')
            print(f"{str(count + 1)}/{str(list_last_index)}")
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

            #TODO: I believe I got rid of this
            if count == list_last_index:
                list_first_index = list_last_index
                break
            self.google_search_banner_titles.append(results_link.find_element(By.XPATH, ".//h3").text)
        print("\nI am at end of search_results()...")
        print(
            f"First Index = {str(list_first_index)} && Last Index = {str(list_last_index)}"
        )
        return list_last_index

    '''
    def get_more_results(self):
        try:
            if more_results := self.browser.find_element(By.XPATH, "//span[text()='More results']"):
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
    '''
    
    def get_more_results(self):
        try:
            if more_results := self.browser.find_element(By.XPATH, "//span[text()='More results']"):
                parent_a_element = more_results.find_element(By.XPATH, "./ancestor::a")
                is_hidden = False
                
                if parent_a_element.get_attribute('data-ve-view') != "":
                    print("Warning: 'More results' button found in the code but...   is HIDDEN")
                    is_hidden = True

                # aria_hidden_elements = parent_a_element.find_elements(By.XPATH, ".//*[@aria-hidden='true']")
                # if aria_hidden_elements:
                #     print("Warning: 'More results' button found in the code but...   is HIDDEN")
                #     is_hidden = True

                if not is_hidden:
                    print("Found the more_results button")
                    more_results.click()
                    print("Clicked 'More results' button")
                    time.sleep(2)
                    return True

            print("No 'More results' button found or button is hidden")
            print("THIS COULD BE THE REASON FOR ERRORS!! idk though dog... soundproof spectacles")
            return False
        except NoSuchElementException:
            print("No 'More results' button found")
            return False

    def end_of_search(self):
        #TODO: I forgot what this does??
        with contextlib.suppress(NoSuchElementException):
            if no_more_results := self.browser.find_element(By.XPATH, "//a[text()='repeat the search with the omitted results included']"):
                print("No more search results")
                time.sleep(2)
                return True
        return False 
    
    
    

    def print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.results_from_search):
            self.job_links_counter += 1
            print(f"Result #{self.job_links_counter} from Google Seaech")
            print("\tJob Title: ", end="")
            print(job)
            print("\tLink to Job: ", end="")
            print(self.links_to_jobs[i])
        print('--------------------------------------------')
        return
    
    def new_print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.results_from_search):
            self.job_links_counter += 1
            print(f"Result #{str(i + 1)} from Google Seaech")
            print("\tJob Title: ", end="")
            print(job)
            print("\tLink to Job: ", end="")
            print(self.links_to_jobs[i])
        print('--------------------------------------------')
        return
    
    def new_new_print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.google_search_results_links):
            self.job_links_counter += 1
            print(f"Result #{str(i + 1)} from Google Seaech")
            print("\tJob Title: ", end="")
            print(self.google_search_banner_titles[i])
            print("\tLink to Job: ", end="")
            print(self.google_search_results_links[i])
        print('--------------------------------------------')
        return











#site:lever.co | site:greenhouse.io | site:workday.com ("Software Engineer" | "Backend Engineer") -Senior -Sr location:us




#jobs.polymer.co





