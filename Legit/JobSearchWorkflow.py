import os
import csv
import time
import openpyxl
import requests
import config

import nltk
import torch
import spacy
import warnings
from fuzzywuzzy import fuzz
from datetime import datetime
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from transformers import GPTNeoForCausalLM, GPT2Tokenizer, pipeline

from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

#! from fileName import className
from GoogleSearch import scraperGoogle
from CompanyOpeningsAndApplications import CompanyWorkflow


import sys
print("Here's some info about sys.executable: ", sys.executable)
import site






#!!!!!!!!!!!!!!!!!!! THIS MIGHT HELP WITH LOCATION STUFF !!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!! https://towardsdatascience.com/transform-messy-address-into-clean-data-effortlessly-using-geopy-and-python-d3f726461225 !!!!!!!!!!!!!!!!!!!!!!!!!!

#NOTE: "Mechanize" - a python import that I believe I want to refer to for browser security methods


                #Run "python|python3 -u Legit/JobSearchWorkflow.py"
                #!!!!!!!!!!!!!!!!!!! TEST THIS HAS  CHECKLIST !!!!!!!!!!!!!!!!!!!!!!!!!!
                #https://jobs.lever.co/hive/9461e715-9e58-4414-bc9b-13e449f92b08/apply
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #ThisFolderWasMadeAtThreeAM/setup.sh
                #!!!!!!!!!!!!!!!!!!! chmod +x setup.sh & .bat !!!!!!!!!!!!!!!!!!!!!!!!!!

#! EXTRACT JOB_TYPE AS LIST OD len()=3 | {DESIRED_LOCATION, HYBRID, REMOTE}
#NOTE: When sending data to Google Sheets for total of anything just do (self.jobs_applied_to_this_session + self.current_jobs_details)



class Workflow():
       
    def __init__(self):
        self.browser = None
        self.google_search_results_links = []
        #TODO: Change this name... it's all the job info a user has previously applied to!!
        self.csv_data = []
        self.env_path = '.env'
        self.previous_job_data_csv_relative_path = r'DataCollection/JobsThatUserHasAppliedTo.csv'
        self.users_information = {}
        self.total_jobs_applied_to_count = 0
        self.total_jobs_applied_to_info = {}
        self.previous_job_applications_data = []
        self.previously_applied_to_job_links = []
        self.last_time_user_applied = None
        self.jobs_applied_to_this_session = {}
        self.user_preferred_workplaceType = []

        self.senior_jobs_found = {}  #Job_Title, Company_Name, Job_Location, Todays_Date
        self.entry_jobs_found = {}

        self.custom_rules = None
        self.q_and_a = None
        self.custom_synonyms = None

        #init_gpt_neo()
        self.tokenizer = None
        self.model = None
        #load_nlp()
        self.nlp = None
        #load_company_resources()
        self.lemmatizer = None

        self.time_program_ran = self.get_time()
        print(f"This program began running at {self.time_program_ran}")
        
        
    def job_search_workflow(self):
        self.browser_setup()
        
        # self.load_company_resources()
        # self.ludacris_speed_apply_to_jobs()
        # self.__del__()
        
        #TODO: GET RID OF OLD VARIABLES - last_link_from_google_search, user_desired_jobs, user_preferred_locations, etc....
        # self.google_search_results_links, last_link_from_google_search, user_desired_jobs = scraperGoogle(self.browser).user_requirements()
        #google_search_results_links, last_link_from_google_search, user_desired_jobs, user_preferred_locations, user_preferred_workplaceType = scraperGoogle(self.browser).user_requirements()
        #google_search_results_links, last_link_from_google_search, user_desired_jobs, user_preferred_locations, user_preferred_workplaceType, users_job_search_requirements = scraperGoogle(self.browser).user_requirements()
        google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs, self.user_preferred_locations, user_preferred_workplaceType, users_job_search_requirements = scraperGoogle(self.browser).user_requirements()
        print("DOPE")
        print(google_search_results_links)
        print("DOPER")
        time.sleep(3)

        self.google_search_results_links, job_links_organized_by_company = self.filter_through_google_search_results(google_search_results_links)
        self.load_company_resources()
        #self.apply_to_jobs(last_link_from_google_search, self.google_search_results_links, user_desired_jobs, user_preferred_locations, user_preferred_workplaceType, job_links_organized_by_company)
        self.refatored_apply_to_jobs(self.google_search_results_links, users_job_search_requirements, job_links_organized_by_company)
        
        self.close_browser()
        
    
    
    
    
    
    
       
        
        
    #TODO: change variable name => users_browser_choice#TODO: change variable name => users_browser_choice   ->->   users_browser_choice_name??users_browser_choice_name??
    #TODO: Setup browser HERE... b/c only the 1st run of this programm should take a long time for info setup!! The 2nd
    #TODO: time they run it just ask them what browser... HERE lol then if they make any changes GoogleSearch.py takes effect!
    def users_browser_choice(self):
        users_browser_choice, browser_name = 1, " Firefox "
        #users_browser_choice, browser_name = 2, " Safari "
        #users_browser_choice, browser_name = 3, " Chrome "
        return users_browser_choice, browser_name
        print("When you are done, type ONLY the number of your preferred web browser then press ENTER")
        print(f"\t1) FireFox")
        print(f"\t2) Safari")
        print(f"\t3) Chrome")
        print(f"\t4) Edge")
        while True:
            user_jobs = input()
            user_jobs.strip()
            
            if user_jobs == "1":
                users_browser_choice = " FireFox "
                break
            elif user_jobs == "2":
                users_browser_choice = " Safari "
                break
            elif user_jobs == "3":
                users_browser_choice = " Chrome "
                break
            elif user_jobs == "4":
                users_browser_choice = " Edge "
                break
            else:
                print("That's kinda messed up dog... I give you an opportunity to pick and you pick nothing.")
                print("You've squandered any further opportunities to decide stuff. I hope you are happy with yourself.")
                print("Don't worry, the council shall discuss and provide a pick for you!")
                #TODO: Make else just check OS and return number of that OS's web browser!!!
                #! THIS IS A while loop.... so it runs until false
        return users_browser_choice, browser_name
    
    #! I have browser setup called 1st and then users_browser_choice b/c if the user uses the same browser over & over this will remember it!!!
    def browser_setup(self):
        users_browser_choice, browser_name = self.users_browser_choice()
        print(f'Execution Started -- Opening{browser_name}Browser')

        if users_browser_choice == 1:
            options = FirefoxOptions()
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("extensions.enabledScopes", 0)
            options.set_preference("browser.toolbars.bookmarks.visibilty", "never")
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("places.history.enabled", False)

            self.browser = webdriver.Firefox(options=options)
            self.browser.set_page_load_timeout(30)
        elif users_browser_choice == 2:
            options = SafariOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")

            self.browser = webdriver.Safari(options=options)
            self.browser.set_page_load_timeout(30)
        elif users_browser_choice == 3:
            options = ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")

            self.browser = webdriver.Chrome(options=options)
            self.browser.set_page_load_timeout(30)
        elif users_browser_choice == 4:
            options = EdgeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")

            self.browser = webdriver.Edge(options=options)
            self.browser.set_page_load_timeout(30)

        #TODO:   if (browser is open == True && browser is ready == True)
        #assert 'Yahoo' in browser.title
        try:
            self.browser.get('https://www.google.com')
        except:
            raise ConnectionError('ERROR: Check Internet Connection')
        return
    
    def close_browser(self):
        self.browser.quit()
        print('Execution Ending -- Webdriver session is Closing')
    
    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_date(self):
        return datetime.now().strftime("%Y-%m-%d")
    
    
    
    
    
    
    
    
    
    
    
    
    '''
    def apply_to_jobs(self, last_link_from_google_search, user_desired_jobs):
        print("Begin the powerCore Batman... Robin... I'll need an extra set of hands in a second so hang tight")
        clicked_link_from_google_search = False
        # for job_link in self.google_search_results_links[::1]:
        for i in range(len(self.google_search_results_links) - 1, -1, -1):   #? I think this goes last to first???
            job_link = self.google_search_results_links[i]
            if not clicked_link_from_google_search:
                print(last_link_from_google_search)
                #self.browser.find_element(By.X_PATH, )
                
                self.browser.execute_script("arguments[0].scrollIntoView();", last_link_from_google_search)
                print("Scrolled to this place...\n")
                time.sleep(5)
                
                
                
                
                
                diagnostics = self.diagnose_interaction(last_link_from_google_search)
                for check, result in diagnostics.items():
                    print(f"{check}: {result}")
                # element_code_outer = last_link_from_google_search.get_attribute('outerHTML')
                # element_code_inner = last_link_from_google_search.get_attribute('innerHTML')
                # soup_outer = BeautifulSoup(element_code_outer, 'html.parser')
                # soup_inner = BeautifulSoup(element_code_inner, 'html.parser')
                # dumb_a_tag_link = soup_inner.find('a')
                # print("------------------------------------------------------")
                # print("This is the selenium element outerHTML: ")
                # print(soup_outer.prettify())
                # print("------------------------------------------------------")
                # print("This is the selenium element innerHTML: ")
                # print(soup_inner.prettify())
                # print("------------------------------------------------------")
                # print("This is my attempt to find the <a>: ")
                # print(dumb_a_tag_link)
                # print("------------------------------------------------------Kenny Powers")
                # some_thing = self.test_click_element(dumb_a_tag_link)
                # print(some_thing)
                # time.sleep(15)
                if not self.safe_click(last_link_from_google_search):
                    print("Clicking on the element failed.")
                
                
                 
                
                # last_a_tag = last_link_from_google_search.find_element(By.TAG_NAME, 'a')
                # last_a_tag.click()
                clicked_link_from_google_search = True
                print("Accidently punished")
                wait_fur_this = self.wait_for_element_explicitly(self.browser, 10, (By.TAG_NAME, 'a'), 'visibility')
                print("This time wasn't an accident!")
                time.sleep(4)



                #print("\n\n\n???????????????????????????????????????????????????")
                #self.cookie_information()
                #self.website_modified_cookie_info()
                #print("???????????????????????????????????????????????????\n\n\n")



            else:
                print(job_link)
                self.browser.get(job_link)
                time.sleep(5)
            print("\n\n" + "--------------------------------------------" + "\nTransferring power to CompanyWorkflow")
            #self.jobs_applied_to_this_session = CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.jobs_applied_to_this_session, senior_experience=False).company_workflow(job_link)
            CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.jobs_applied_to_this_session, senior_experience=False).test_this_pile_of_lard(job_link)
    '''
    
    
    #DEPRICATED
    def apply_to_jobs(self, last_link_from_google_search, google_search_results_links, user_desired_jobs, user_preferred_locations, user_preferred_workplaceType, job_links_organized_by_company):
        print("Begin the  Batman... Robin... I'll need an extra set of hands in a second so hang tight")
        clicked_link_from_google_search = False
        for i in range(len(google_search_results_links) - 1, -1, -1):
            job_link = google_search_results_links[i]
            if not clicked_link_from_google_search:
                # print(last_link_from_google_search)
                # self.browser.execute_script("arguments[0].scrollIntoView();", last_link_from_google_search)
                
                print("job_link = ", job_link)
                job_link_element = self.transition_link_into_selenium(job_link)
                print("job_link_element = ", job_link_element)
                self.browser.execute_script("arguments[0].scrollIntoView();", job_link_element)
                
                
                
                #!WinMerge WinMerge WinMerge WinMerge WinMerge WinMerge WinMerge
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_link_element)
                #! ^ WinMerge ^ WinMerge ^ WinMerge ^ WinMerge ^ WinMerge ^ WinMerge ^ WinMerge
                print("Scrolled to this place...\n")
                time.sleep(3)	#!OLD TIME = 5 && NEW TIME = 2 ssoooooo... POSSIBLY DUE TO too LITTLE TIME!!!!

                diagnostics = self.diagnose_interaction(job_link_element)
                for check, result in diagnostics.items():
                    print(f"{check}: {result}")

                try:
                    # Try to click the element
                    if not self.safe_click(job_link_element):
                        print("Clicking on the element failed.")
                except Exception as e:
                    print(f"Safe click failed: {e}")
                
                clicked_link_from_google_search = True
                print("Accidently clamped my testicles b/c I needed to be punished")
                
                #OG OG OG OG OG OG OG OG OG OG OG OG OG OG OG OG
                #wait_fur_this = self.wait_for_element_explicitly(self.browser, 10, (By.TAG_NAME, 'a'), 'visibility')
                
                #NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW
                # wait_fur_this = self.wait_for_element_explicitly(self.browser, 10, (By.TAG_NAME, 'a'), 'visibility')
                self.wait_for_element_explicitly(self.browser, 10, (By.TAG_NAME, 'a'), 'visibility')

                print("This time wasn't an accident!")
                time.sleep(4)

            else:
                print(job_link)
                self.browser.get(job_link)
                time.sleep(5)
            
            job_link = self.consolidate_job_links_by_company(job_link, job_links_organized_by_company)
            print("\n\n" + "--------------------------------------------" + "\nTransferring power to CompanyWorkflow")
            #CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.jobs_applied_to_this_session, senior_experience=False).test_this_pile_of_lard(job_link)
            CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, user_preferred_locations, user_preferred_workplaceType, self.jobs_applied_to_this_session, self.tokenizer, self.model, self.nlp, self.lemmatizer, self.custom_rules, self.q_and_a, self.custom_synonyms).company_workflow(job_link)
        print("Hip Hip Hooray  Hip Hip Hooray  Hip Hip Hooray you just applied to literally every job in america!")
        return


    def refatored_apply_to_jobs(self, google_search_results_links, users_job_search_requirements, job_links_organized_by_company):
        print("Begin the powerCore Batman... Robin... I'll need an extra set of hands in a second so hang tight")
        clicked_link_from_google_search = False
        for i in range(len(google_search_results_links) - 1, -1, -1):
            job_link = google_search_results_links[i]
            if not clicked_link_from_google_search:
                print("job_link = ", job_link)
                job_link_element = self.transition_link_into_selenium(job_link)
                print("job_link_element = ", job_link_element)
                self.browser.execute_script("arguments[0].scrollIntoView();", job_link_element)

                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_link_element)
                print("Scrolled to this place...\n")
                time.sleep(3)

                diagnostics = self.diagnose_interaction(job_link_element)
                for check, result in diagnostics.items():
                    print(f"{check}: {result}")

                try:
                    # Try to click the element
                    if not self.safe_click(job_link_element):
                        print("Clicking on the element failed.")
                except Exception as e:
                    print(f"Safe click failed: {e}")
                
                clicked_link_from_google_search = True
                print("Accidently clicked whoops...")
                
                self.wait_for_element_explicitly(self.browser, 10, (By.TAG_NAME, 'a'), 'visibility')

                print("Or was it an accident!")
                time.sleep(4)

            else:
                print(job_link)
                self.browser.get(job_link)
                time.sleep(5)
            
            job_link = self.consolidate_job_links_by_company(job_link, job_links_organized_by_company)
            print("\n\n" + "--------------------------------------------" + "\nTransferring power to CompanyOpeningsAndApplications")
            #CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, user_preferred_locations, user_preferred_workplaceType, self.jobs_applied_to_this_session, self.tokenizer, self.model, self.nlp, self.lemmatizer, self.custom_rules, self.q_and_a, self.custom_synonyms).company_workflow(job_link)
            CompanyWorkflow(self, self.browser, self.users_information, users_job_search_requirements, self.jobs_applied_to_this_session, self.tokenizer, self.model, self.nlp, self.lemmatizer, self.custom_rules, self.q_and_a, self.custom_synonyms).company_workflow(job_link)
        print("Hip Hip Hooray  Hip Hip Hooray  Hip Hip Hooray  you should hear back from these companies in like 8+ months or so")
        return






    def transition_link_into_selenium(self, job_link):
        return self.browser.find_element(By.CSS_SELECTOR, f'a[href="{job_link}"]')
    
    def ludacris_speed_apply_to_jobs(self, user_desired_jobs=None):
        print("Begin the powerCore Batman... Robin... I'll need an extra set of hands in a second so hang tight")
        self.load_users_information()
        print("Accidently clicked that whoops...")

        print("\n\n" + "--------------------------------------------" + "\nTransferring power to CompanyWorkflow")
        CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.jobs_applied_to_this_session, self.tokenizer, self.model, self.nlp, self.lemmatizer, self.custom_rules, self.q_and_a, self.custom_synonyms).test_this_pile_of_lard('https://www.google.com')

    def safe_click(self, element):
        print("safe_click()")
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print("1) Normal click attempt")
        current_url = self.browser.current_url
        try:
            element.click()
            WebDriverWait(self.browser, 10).until(EC.url_changes(current_url))
            return True
        except:
            print("This dumb thing didn't work!")
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print("2) Waiting for element to be clickable attempt")
        try:
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.TAG_NAME, element.tag_name)))
            element.click()
            WebDriverWait(self.browser, 10).until(EC.url_changes(current_url))
            return True
        except TimeoutException as e:
            print(f"2) Waiting for element to be clickable failed: {e}")
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print("3) Waiting for element to be clickable attempt")
        try:
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            WebDriverWait(self.browser, 10).until(EC.url_changes(current_url))
            return True
        except Exception as e:
            print(f"4) Scrolling and clicking failed: {e}")
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print("5.1) Checking visibility and clicking attempt")
        try:
            if element.is_displayed():
                element.click()
                WebDriverWait(self.browser, 10).until(EC.url_changes(current_url))
                return True
            else:
                print("5.2)Element is not visible")
        except Exception as e:
            print(f"5.3) Checking visibility and clicking failed: {e}")
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print("6) JavaScript click attempt")
        try:
            self.browser.execute_script("arguments[0].click();", element)
            WebDriverWait(self.browser, 10).until(EC.url_changes(current_url))
            return True
        except Exception as e:
            print(f"6) JavaScript click failed: {e}")
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # If all methods fail, return False
        return False

    def diagnose_interaction(self, element):
        diagnostics = {}

        # Check 1: Is the element present in the DOM?
        try:
            self.browser.find_element(By.XPATH, element.tag_name)
            diagnostics["Present in DOM"] = "Yes"
        except Exception as e:
            diagnostics["Present in DOM"] = f"No, Error: {e}"

        # Check 2: Is the element displayed?
        try:
            diagnostics["Displayed"] = "Yes" if element.is_displayed() else "No"
        except Exception as e:
            diagnostics["Displayed"] = f"Error: {e}"

        # Check 3: Is the element enabled?
        try:
            diagnostics["Enabled"] = "Yes" if element.is_enabled() else "No"
        except Exception as e:
            diagnostics["Enabled"] = f"Error: {e}"

        # Check 4: Can we scroll to the element?
        try:
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            diagnostics["Scroll Into View"] = "Success"
        except Exception as e:
            diagnostics["Scroll Into View"] = f"Error: {e}"

        # Check 5: Can we click the element normally?
        try:
            element.click()
            diagnostics["Normal Click"] = "Success"
        except Exception as e:
            diagnostics["Normal Click"] = f"Error: {e}"

        # Check 6: Can we click the element using JavaScript?
        try:
            self.browser.execute_script("arguments[0].click();", element)
            diagnostics["JavaScript Click"] = "Success"
        except Exception as e:
            diagnostics["JavaScript Click"] = f"Error: {e}"

        # Check 7: Does the element have any children that could be interfering with the click?
        try:
            if children := element.find_elements(By.XPATH, ".//*"):
                diagnostics["Has Children"] = f"Yes, count: {len(children)}"
            else:
                diagnostics["Has Children"] = "No"
        except Exception as e:
            diagnostics["Has Children"] = f"Error: {e}"

        # Check 8: Is the element covered by another element?
        try:
            covering_element = self.browser.execute_script(
                "var elem = arguments[0],"
                "  box = elem.getBoundingClientRect(),"
                "  cx = box.left + box.width / 2,"
                "  cy = box.top + box.height / 2,"
                "  e = document.elementFromPoint(cx, cy);"
                "for (; e; e = e.parentElement) {"
                "  if (e === elem)"
                "    return true"
                "}"
                "return false;", element)
            diagnostics["Covered by another element"] = "No" if covering_element else "Yes"
        except Exception as e:
            diagnostics["Covered by another element"] = f"Error: {e}"

        return diagnostics

    def wait_for_element_explicitly(self, browser, timeout, locator_tuple, condition):
        print("wait_for_element_explicitly()")
        wait = WebDriverWait(browser, timeout)
        
        if condition == 'presence':
            return wait.until(EC.presence_of_element_located(locator_tuple))
        elif condition == 'visibility':
            return wait.until(EC.visibility_of_element_located(locator_tuple))
        elif condition == 'clickable':
            return wait.until(EC.element_to_be_clickable(locator_tuple))
        else:
            raise ValueError(f"Invalid condition: {condition}")
    
    def consolidate_job_links_by_company(self, job_link, job_links_organized_by_company):
        print("\nconsolidate_job_links_by_company()\n")
        for companies_url_list in job_links_organized_by_company:
            print("\tjob_link = ", job_link)
            print("\t\tvs.")
            print("\tcompanies_url_list[0] = ", companies_url_list[0])
            
            if companies_url_list[0] == job_link:
                print("MATCH FOUND!!!!!")
                return companies_url_list
            print("\n--------------------------------\n")
        return job_link
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    
        
    def show_warning(message, category, filename, lineno, file=None, line=None):
        print(f"Warning: {message}")
    warnings.showwarning = show_warning
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                      LOAD RESOURCES AND LIBRARIES                             !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    #! HERE HERE HERE          CHANGE  GPT-Neo-#.#B            HERE HERE HERE
    def load_company_resources(self):
        print("load_company_resources()")
        self.load_users_information()
        print("  Loaded Users Information...")
        self.load_custom_rules()
        print("  Loaded Custom Rules...")
        
        # print(self.custom_rules)
        # print(self.q_and_a)
        
        # self.nlp_load()
        print("  Loaded Users Information...")
        
        # model_3B_pars = 'EleutherAI/gpt-neo-2.7B'
        # self.init_gpt_neo(model_3B_pars)
        # print("  Initialized GPT-Neo-2.7B...")
        
        # model_3B_pars = 'EleutherAI/gpt-neo-1.3B'
        # self.init_gpt_neo(model_3B_pars)
        # print("  Initialized GPT-Neo-1.3B...")
        
        self.init_nltk()
        print("  Initialized nltk...")
        
        self.lemmatizer = WordNetLemmatizer()
        print("  Loaded WordNetLemmatizer()...")
    
    #!------------- .env --------------------
    def load_users_information(self):
        self.users_information = {}
        with open(self.env_path) as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split('=', 1)
                    value = value.strip("'")  # Remove quotes around the value
                    self.users_information[key] = value
        #self.print_users_information()
    
    def print_users_information(self):
        print('--------USERS .ENV INFO--------')
        for key, value in self.users_information.items():
            print(f"{key}: {value}")
        print('-------------------------------')
    #!---------------------------------------
    
    #!------------ config -------------------
    def load_custom_rules(self):
        print("\nload_custom_rules()")
        print("dir(config) = ", dir(config))
        
        for attr in dir(config):
            if not attr.startswith("__"):
                print(f"Attribute: {attr}")
                value = getattr(config, attr)
                
                #if attr == "CUSTOM_RULES" or attr == "CUSTOM_SYNONYMS":
                if attr in ["CUSTOM_RULES", "CUSTOM_SYNONYMS"]:
                    value = value[0]
                
                if isinstance(value, dict):
                    setattr(self, attr.lower(), value)
                #     for key, val in value.items():
                #         print(f"Key: {key}, Value: {val}")
                # else:
                #     print(f"Value: {value}")

        
        # attributes = [attr for attr in dir(config) if not attr.startswith("__")]
        
        # for attr in attributes:
        #     print("attr = ", attr)
        #     value = getattr(config, attr)
        #     print("value = ", value)
            
        #     if isinstance(value, dict):
        #         print("dict = ", dict)
        #         globals()[attr.lower()] = value
    #!---------------------------------------
    
    def init_nltk(self):
        try:
            #Try to access WordNet
            nltk.corpus.wordnet.synsets('word')
        except LookupError:
            #If WordNet is not present, download it
            nltk.download('wordnet')
    
    def from_website_gptneo_setup(self):
        #https://gist.github.com/pszemraj/791d72587e718aa90ff2fe79f45b3cfe
        model_3B_pars = 'EleutherAI/gpt-neo-2.7B'
        
        #gpu_mem = round(gpu_mem_total() / 1024, 2)
        
    def init_gpt_neo(self, model_name):
        print("init_gpt_neo()")
        #self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.check_cuda_compatibility()
        self.model = GPTNeoForCausalLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        #return self.tokenizer, self.model
        
    def clean_gpt_out(self, text, remove_breaks=True):
        from cleantext import clean
        cleaned_text = clean(text,
                         fix_unicode=True,               # fix various unicode errors
                        to_ascii=True,                  # transliterate to closest ASCII representation
                        lower=False,                     # lowercase text
                        no_line_breaks=remove_breaks,   # fully strip line breaks as opposed to only normalizing them
                        no_urls=True,                  # replace all URLs with a special token
                        no_emails=True,                # replace all email addresses with a special token
                        no_phone_numbers=True,         # replace all phone numbers with a special token
                        no_numbers=False,               # replace all numbers with a special token
                        no_digits=False,                # replace all digits with a special token
                        no_currency_symbols=True,      # replace all currency symbols with a special token
                        no_punct=False,                 # remove punctuations
                        replace_with_punct="",          # instead of removing punctuations you may replace them
                        replace_with_url="",
                        replace_with_email="",
                        replace_with_phone_number="",
                        replace_with_number="",
                        replace_with_digit="0",
                        replace_with_currency_symbol="",
                        lang="en"                       # set to 'de' for German special handling
                        )
        return cleaned_text
    
    def test_gpt_neo(self, model_name):
        print("\ntest_gpt_neo()")
        print("The module name of GPT-Neo-2.7B is ", end='')
        print(GPTNeoForCausalLM.__module__)
        
        device = 0 if torch.cuda.is_available() else -1
        generator = pipeline("text-generation", model=model_name, device=device)
        
        prompt = "Question: Is Bengali, India in the United States?"
        response_min_chars = 10
        response_max_chars = 500
        from cleantext import clean
        import pprint as pp
        import gc
        from datetime import timedelta
        gc.collect()
        
        
        
        with warnings.catch_warnings(record=True) as w:
            #https://stackoverflow.com/questions/7370801/how-do-i-measure-elapsed-time-in-python
            start_time = time.time()
            
            warnings.filterwarnings("always", module='transformers.models.gpt_neo.modeling_gpt_neo')
            #All WARNINGS that GPT-Neo caused
            # warnings.filterwarnings("always", module='transformers.GPTNeoForCausalLM')
            # warnings.filterwarnings("always", module='transformers.GPT2Tokenizer')
            
            try:
                response = generator(prompt, do_sample=True, min_length=response_min_chars, max_length=response_max_chars,
                                                                                            clean_up_tokenization_spaces=True,
                                                                                            return_full_text=True)
            except Exception as e:
                print("An error occured while running the generator()")
                print(e)
                
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"The generator() took {str(timedelta(seconds=elapsed_time))}")
        
        print("----------------------\n")
        for warnins in w:
            print(str(warnins.message))
        
        
        
        
        gc.collect()
        print("Prompt: \n")
        pp.pprint(prompt)
        print("\nResponse: \n")
        out3_dict = response[0]
        pp.pprint(self.clean_gpt_out(out3_dict["generated_text"], remove_breaks=True), compact=True)
        
    def check_cuda_compatibility(self):
        print("check_cuda_compatibility()")
        if torch.cuda.is_available():
            print("CUDA is available!")
            print(f"CUDA version: {torch.version.cuda}")
        else:
            print("CUDA is not available.")
            
    def nlp_load(self):
        print("nlp_load()")
        self.nlp = spacy.load("en_core_web_md")
        #self.nlp.add_pipe()
        #return self.nlp
        return
    
    def __del__(self):
        # Delete the model when the object is destroyed
        del self.model
        del self.tokenizer
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                                                               !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                         GET RID OF BAD LINKS                                  !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def filter_through_google_search_results(self, google_search_results_links):
        print("filter_through_google_search_results()")
        self.previous_job_applications_data = self.convert_csv_data(self.previous_job_data_csv_relative_path)
        google_search_results_links = self.ensure_no_duplicates(google_search_results_links)
        self.previously_applied_to_job_links = self.get_job_links_users_applied_to(self.previous_job_applications_data)
        self.filter_out_jobs_user_previously_applied_to(google_search_results_links, self.previously_applied_to_job_links)
        google_search_results_links, job_links_organized_by_company = self.encapsulate_companies_urls(google_search_results_links)
        return google_search_results_links, job_links_organized_by_company
    
    def convert_csv_data(self, csv_relative_path):
        print("\nconvert_csv_data() =")
        csv_to_list = []
        
        with open(csv_relative_path, 'r') as file:
            csv_reader = csv.reader(file)
            
            # Skip the header row
            next(csv_reader)
            
            for row in csv_reader:
                updated_row = [cell.replace('=>', ',') for cell in row]
                csv_to_list.append(updated_row)
        print(csv_to_list)
        return csv_to_list
    
    #TODO: You are a doofus implement THE BETTER WAY!
    def ensure_no_duplicates(self, list_to_filter):
        print("\nensure_no_duplicates()")
        
        unique_results = []
        for list_URL in list_to_filter:
                if list_URL not in unique_results:
                    unique_results.append(list_URL)
        return unique_results
    
    #TODO: Keep job url's
    #! Pretty sure this is the only time I use JobsThatUserHasAppliedTo.csv so it doesn't matter
    def get_job_links_users_applied_to(self, extract_URLs_from_dictionary):
        print("\nget_job_links_users_applied_to() =")
        URLs_list = []
        
        for row in extract_URLs_from_dictionary:
            links_row = row[0]
            print("If my calculations are correct this should print a link MUAH HA HA... ", end="")
            print(links_row)
            URLs_list.append(links_row)
            
        print("These are all the links you already applied to... Tom")
        print(URLs_list)
        if not self.last_time_user_applied:
            self.last_time_user_applied = extract_URLs_from_dictionary[-1][-1]
            print("And this is when you last applied... Tom")
            print(self.last_time_user_applied)
        return URLs_list
    
    #TODO: Only include links that are within the past 6 months for "previously_applied_links" !!!
    def filter_out_jobs_user_previously_applied_to(self, list_to_filter, previously_applied_links):
        print("\nfilter_out_jobs_user_previously_applied_to()")
        Lake_Minnetonka_Purified_list = []
        
        for list_URL in list_to_filter:
            found = False
            for previously_applied_URL in previously_applied_links:
                if list_URL == previously_applied_URL:
                    print("Match list_URL: ", end='')
                    print(list_URL)
                    print("Match previously_applied_URL: ", end='')
                    print(previously_applied_URL)
                    #previously_applied_links.append(previously_applied_URL)
                    found = True
                    break
            if not found:
                Lake_Minnetonka_Purified_list.append(list_URL)

        return Lake_Minnetonka_Purified_list
    
    def encapsulate_companies_urls(self, list_to_filter):
        print("\nencapsulate_companies_urls()")
        updated_google_search_results_links = []
        job_links_organized_by_company = []
        seen_urls = set()
        #Purely for testing
        count = 0

        for indexed_job in list_to_filter:
            parsed_url = urlparse(indexed_job)
            base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
            company_url = '/'.join(parsed_url.path.strip('/').split('/')[:1])
            company_base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, company_url, '', '', ''))

            if company_base_url not in seen_urls:
                seen_urls.add(company_base_url)
                updated_google_search_results_links.append(indexed_job)
                company_filtered_list = [url for url in list_to_filter if company_base_url in url]
                if len(company_filtered_list) > 1:
                    count=count+1
                    print(f"{str(count)}) company_filtered_list = {company_filtered_list}")
                    print(f"                         = {len(company_filtered_list)}")
                    job_links_organized_by_company.append(company_filtered_list)

        self.print_lists_side_by_side(list_to_filter, updated_google_search_results_links)
        return updated_google_search_results_links, job_links_organized_by_company

    def print_lists_side_by_side(self, list_to_filter, updated_google_search_results_links):
        print("\n\n    Sup Norrington")
        print("Index | List to Filter URL | Updated Google Search Results URL")
        print("------|-------------------|-----------------------------------")
        for i in range(max(len(list_to_filter), len(updated_google_search_results_links))):
            list_to_filter_url = list_to_filter[i] if i < len(list_to_filter) else "N/A"
            updated_url = updated_google_search_results_links[i] if i < len(updated_google_search_results_links) else "N/A"
            print(f"{i:5} | {list_to_filter_url:20} | {updated_url}")

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                                                               !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  
        
      
    
    
    
    
    
    
    
    
    
    
    
    #TODO: Do stuff at very end or once CompanyOpeningsAndApplications.py instance ends!!
    def write_to_csv(self, job_data):
        with open ('job_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            #for row in writer:
            writer.writerow(job_data)
        return "All done!"
    
   
   
   
   











    def cookie_information(self):
        print("cookie_information()")
        current_url = self.browser.current_url
        #parameters = {'Name':'{FIRST_NAME} {LAST_NAME}', 'Email-id':'{EMAIL}','Message':'Hello cookies'}
        parameters = {'Name':'firstName lastName', 'Email-id':'Liebmann.nicholas1@gmail.com','Message':'Hello cookies'}
        r = requests.post(f"{current_url}", data = parameters)
        print('The cookie is:')
        print(r.cookies.get_dict())
        print(r.text)

    def website_modified_cookie_info(self):
        print("website_modified_cookie_info()")
        current_url = self.browser.current_url
        session = requests.Session()
        #parameters = {'Name':'{FIRST_NAME} {LAST_NAME}', 'Email-id':'{EMAIL}','Message':'Hello cookies'}
        parameters = {'Name':'Nick Liebmann', 'Email-id':'Liebmann.nicholas1@gmail.com','Message':'Hello cookies'}
        r = session.post(f"{current_url}", data=parameters)
        print('The cookie is:')
        print(r.cookies.get_dict())
        print(r.text)



 


   
    
    
    
        

if __name__ == '__main__':
    workflow = Workflow()
    workflow.job_search_workflow()







#site:lever.co | site:greenhouse.io | site:workday.com ("Software Engineer" | "Backend Engineer") -Senior -Sr location:us






# Web_Scraper/
# ├── config.py
# ├── Legit
# │   ├── JobSearchWorkflow.py
# │   ├── GoogleSearch.py
# │   └── CompanyOpeningsAndApplications.py
# ├── .env
# ├── README.md
# └── Scraper
#     ├── scraperGoogle.py
#     ├── scraperGoogleJob.py
#     ├── TestingSelenium.py
#     └── JobData.csv













