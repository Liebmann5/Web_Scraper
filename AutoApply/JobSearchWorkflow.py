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
from GoogleSearch import scraperGoogle
from CompanyOpeningsAndApplications import CompanyWorkflow
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


import sys
print("Here's some info about sys.executable: ", sys.executable)
import site
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s',
    filename='app.log', 
    filemode='w'
)




class Workflow():
    """
    Manages the overall job search and application workflow.
    
    This class encapsulates the entire process of a job search workflow, including browser setup, executing job searches, filtering results, applying to jobs, and managing job application data.
    """
       
    def __init__(self):
        """
        Initializes the Workflow class with default values and configurations.
        
        Sets up initial lists for storing job search links, job application data, and user preferences. It also configures paths for environmental variables and previous job data, as well as initializing various attributes related to job search and application tracking.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
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
        """
        Executes the main job search and application workflow.
        
        This method orchestrates the entire job search process, from setting up the browser, filtering search results, loading company resources, to applying to jobs and closing the browser session. It utilizes various helper methods to perform each step in the workflow.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        self.browser_setup()
        
        # self.load_company_resources()
        # self.ludacris_speed_apply_to_jobs()
        # self.__del__()
        
        #TODO: GET RID OF OLD VARIABLES - last_link_from_google_search, user_desired_jobs, user_preferred_locations, etc....
        google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs, self.user_preferred_locations, user_preferred_workplaceType, users_job_search_requirements = scraperGoogle(self.browser).user_requirements()
        print("DOPE")
        print(google_search_results_links)
        print("DOPER")
        time.sleep(3)

        self.google_search_results_links, job_links_organized_by_company = self.filter_through_google_search_results(google_search_results_links)
        self.load_company_resources()
        #self.apply_to_jobs(last_link_from_google_search, self.google_search_results_links, user_desired_jobs, user_preferred_locations, user_preferred_workplaceType, job_links_organized_by_company)
        self.refactored_apply_to_jobs(self.google_search_results_links, users_job_search_requirements, job_links_organized_by_company)
        
        self.close_browser()
        
    
    
    
    
       
        
        
    #TODO: change variable name => users_browser_choice#TODO: change variable name => users_browser_choice   ->->   users_browser_choice_name??users_browser_choice_name??
    #TODO: Setup browser HERE... b/c only the 1st run of this programm should take a long time for info setup!! The 2nd
    #TODO: time they run it just ask them what browser... HERE lol then if they make any changes GoogleSearch.py takes effect!
    def users_browser_choice(self):
        """
        Retrieves the user's preferred browser choice for the job search.
        
        This method prompts the user to choose a web browser for conducting the job search. It defaults to a predetermined choice if the user does not make a selection or if an invalid selection is made.
        
        Parameters:
        - None
        
        Returns:
        - tuple: Contains the user's browser choice as an integer and the browser's name as a string.
        
        Note:
        - Currently, this method returns a default value without user input. Future implementations should include user input handling.
        """
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
        """
        Configures and initializes the web browser based on the user's choice.
        
        Sets up the desired web browser with specific options to enhance the job search process, such as disabling notifications and setting page load timeouts. It opens a Google page to verify the internet connection and browser setup.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
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
        """
        Closes the web browser session at the end of the job search workflow.
        
        This method safely quits the browser session, ensuring that all resources are properly released.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        self.browser.quit()
        print('Execution Ending -- Webdriver session is Closing')
    
    def get_time(self):
        """
        Retrieves the current time formatted as a string.
        
        Provides the current date and time in "YYYY-MM-DD HH:MM:SS" format, useful for timestamping events within the job search process.
        
        Parameters:
        - None
        
        Returns:
        - str: The current date and time as a string.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_date(self):
        """
        Retrieves the current date formatted as a string.
        
        Provides the current date in "YYYY-MM-DD" format, useful for date-stamping job applications or other relevant activities.
        
        Parameters:
        - None
        
        Returns:
        - str: The current date as a string.
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    
    
    
    
    
    
    
    #DEPRICATED
    def apply_to_jobs(self, last_link_from_google_search, google_search_results_links, user_desired_jobs, user_preferred_locations, user_preferred_workplaceType, job_links_organized_by_company):
        """
        (Deprecated) Attempts to apply to jobs based on the gathered search results.
        
        This method iterates through Google search results links and attempts to interact with each job posting. It is marked as deprecated and should no longer be used in favor of a refactored approach.
        
        Parameters:
        - last_link_from_google_search: The last job link from Google search results.
        - google_search_results_links (list[str]): A list of job links from Google search results.
        - user_desired_jobs (list[str]): A list of job titles the user desires.
        - user_preferred_locations (list[str]): A list of preferred job locations by the user.
        - user_preferred_workplaceType (list[str]): A list of preferred workplace types by the user.
        - job_links_organized_by_company (dict): Job links organized by company.
        
        Returns:
        - None
        
        Note:
        - This method contains legacy code and is recommended for refactoring or replacement.
        """
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


    def refactored_apply_to_jobs(self, google_search_results_links, users_job_search_requirements, job_links_organized_by_company):
        """
        Applies to jobs using refactored logic based on the search results and user preferences.
        
        Iterates over Google search results and applies to jobs, handling page interactions and diagnostics. It incorporates user preferences and requirements into the job application process.
        
        Parameters:
        - google_search_results_links (list[str]): A list of job links from Google search results.
        - users_job_search_requirements (dict): User-defined job search requirements including desired job titles, locations, and workplace types.
        - job_links_organized_by_company (list): Organized job links by company for targeted applications.
        
        Returns:
        - None
        """
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
                    # Diagnose the page state if the expected condition fails
                    diagnostics = self.diagnose_page_state(self.browser)
                    print("Diagnostics after clicking a link:", diagnostics)
                
                clicked_link_from_google_search = True
                print("Accidently clicked whoops...")
                
                
                
                
                time.sleep(2)
                try:
                    self.wait_for_element_explicitly(self.browser, 5, (By.TAG_NAME, 'a'), 'visibility')
                except Exception as e:
                    print(f"wait_for_element_explicitly() failed: {e}")
                    # Diagnose the page state if the expected condition fails
                    diagnostics = self.diagnose_page_state(self.browser)
                    print("Diagnostics after clicking a link:", diagnostics)
                
                
                

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
        """
        Transitions a job link into a Selenium WebElement.
        
        Given a job link URL, this method finds and returns the corresponding WebElement on the page.
        
        Parameters:
        - job_link (str): The URL of the job link to be transitioned into a Selenium WebElement.
        
        Returns:
        - WebElement: The WebElement corresponding to the job link URL.
        """
        return self.browser.find_element(By.CSS_SELECTOR, f'a[href="{job_link}"]')
    
    def ludacris_speed_apply_to_jobs(self, user_desired_jobs=None):
        """
        Quickly applies to jobs using a predefined set of user job preferences.
        
        Initiates an accelerated job application process using predefined or specified user job preferences, transferring control to the CompanyWorkflow for actual application.
        
        Parameters:
        - user_desired_jobs (list[str], optional): A list of job titles the user desires, defaults to None.
        
        Returns:
        - None
        """
        print("Begin the powerCore Batman... Robin... I'll need an extra set of hands in a second so hang tight")
        self.load_users_information()
        print("Accidently clicked that whoops...")

        print("\n\n" + "--------------------------------------------" + "\nTransferring power to CompanyWorkflow")
        CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.jobs_applied_to_this_session, self.tokenizer, self.model, self.nlp, self.lemmatizer, self.custom_rules, self.q_and_a, self.custom_synonyms).test_this_pile_of_lard('https://www.google.com')

    def safe_click(self, element):
        """
        Attempts to safely click a WebElement, trying multiple strategies.
        
        This method attempts to click on a given WebElement using various strategies to handle common issues like element not being clickable, being covered by another element, or not being visible.
        
        Parameters:
        - element (WebElement): The WebElement to click.
        
        Returns:
        - bool: True if the click was successful, False otherwise.
        """
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
        """
        Diagnoses interaction issues with a given WebElement.
        
        Performs a series of checks on the WebElement to diagnose common interaction issues, such as visibility or being covered by another element.
        
        Parameters:
        - element (WebElement): The WebElement to diagnose.
        
        Returns:
        - dict: A dictionary of diagnostic results.
        """
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
        """
        Waits explicitly for an element to satisfy a specific condition.
        
        Waits for a web element, specified by its locator tuple, to meet a given condition within a timeout period.
        
        Parameters:
        - browser (WebDriver): The Selenium WebDriver instance.
        - timeout (int): The timeout in seconds.
        - locator_tuple (tuple): The locator tuple for the WebElement.
        - condition (str): The condition to wait for ('presence', 'visibility', or 'clickable').
        
        Returns:
        - WebElement: The WebElement if the condition is met within the timeout period.
        
        Raises:
        - ValueError: If an invalid condition is specified.
        """
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
    
    def diagnose_page_state(self, browser):
        """
        Diagnoses the current state of the page.
        
        Collects diagnostics about the current state of the page, such as the current URL and the visibility of certain elements.
        
        Parameters:
        - browser (WebDriver): The Selenium WebDriver instance.
        
        Returns:
        - dict: A dictionary containing diagnostic information about the page state.
        """
        diagnostics = {}
        
        # Current URL
        diagnostics['Current URL'] = browser.current_url
        
        # Check for presence of 'a' tags
        try:
            a_tags = browser.find_elements(By.TAG_NAME, 'a')
            diagnostics['Number of <a> Tags'] = len(a_tags)
            diagnostics['First <a> Tag Visible'] = a_tags[0].is_displayed() if a_tags else 'No <a> tags found'
        except NoSuchElementException:
            diagnostics['Number of <a> Tags'] = 'No <a> tags found'

        # Additional checks can be added here

        return diagnostics
    
    def ensure_page_loaded(self, browser, timeout=30):
        """
        Ensures that a page is fully loaded within a specified timeout period.
        
        Waits for basic indicators of page load completion, such as URL changes or visibility of specific elements, to ensure the page is fully loaded.
        
        Parameters:
        - browser (WebDriver): The Selenium WebDriver instance.
        - timeout (int, optional): The timeout in seconds, defaults to 30.
        
        Returns:
        - None
        
        Note:
        - Additional dynamic content loading checks can be added as needed.
        """
        try:
            # Wait for the URL to change if needed
            WebDriverWait(browser, timeout).until(EC.url_changes(browser.current_url))

            # Wait for at least one 'a' tag to be visible
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, 'a')))
            
            # Additional checks for dynamic content can be added here

        except TimeoutException:
            # Handle timeout exception
            print("Page did not load as expected within the timeout period.")
            diagnostics = self.diagnose_page_state(browser)
            print("Diagnostics:", diagnostics)
    
    def consolidate_job_links_by_company(self, job_link, job_links_organized_by_company):
        """
        Consolidates job links by company for organized access.
        
        Matches a given job link against a list of job links organized by company, aiding in the organization and application process.
        
        Parameters:
        - job_link (str): The job link to be matched and consolidated.
        - job_links_organized_by_company (list): A list of job links organized by company.
        
        Returns:
        - mixed: The matched company URL list if a match is found; otherwise, returns the original job link.
        """
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
        """
        Custom warning display function.
        
        Overrides the default warning display to print warnings with a specific format.
        
        Parameters:
        - message (str): The warning message.
        - category (Warning): The category of the warning.
        - filename (str): The name of the file in which the warning occurred.
        - lineno (int): The line number at which the warning occurred.
        - file (Optional[IO]): The file object to write the warning to, defaults to None.
        - line (Optional[str]): The line of code that generated the warning, defaults to None.
        
        Returns:
        - None
        """
        print(f"Warning: {message}")
    warnings.showwarning = show_warning
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                      LOAD RESOURCES AND LIBRARIES                             !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    #! HERE HERE HERE          CHANGE  GPT-Neo-#.#B            HERE HERE HERE
    def load_company_resources(self):
        """
        Loads various resources and libraries necessary for the job search process.
        
        Initiates the loading of user information, custom rules, Natural Language Processing resources, and initializes GPT-Neo and NLTK libraries.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        print("\nload_company_resources()")
        self.load_users_information()
        print("  Loaded Users Information...")
        self.load_custom_rules()
        print("  Loaded Custom Rules...")
        
        # print(self.custom_rules)
        # print(self.q_and_a)
        
        self.nlp_load()
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
        """
        Loads user information from the .env file into the class attribute.
        
        Reads the .env file line by line, extracting key-value pairs and storing them in a dictionary attribute for later use.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        self.users_information = {}
        with open(self.env_path) as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split('=', 1)
                    value = value.strip("'")  # Remove quotes around the value
                    self.users_information[key] = value
        #self.print_users_information()
    
    def print_users_information(self):
        """
        Prints the loaded user information to the console.
        
        Iterates over the users_information dictionary and prints each key-value pair.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        print('--------USERS .ENV INFO--------')
        for key, value in self.users_information.items():
            print(f"{key}: {value}")
        print('-------------------------------')
    #!---------------------------------------
    
    #!------------ config -------------------
    def load_custom_rules(self):
        """
        Loads custom rules defined in the config module into class attributes.
        
        Iterates through attributes of the config module that do not start with "__", checking for specific custom rules and synonyms to load them into class attributes.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        print("\nload_custom_rules()")
        print("dir(config) = ", dir(config))
        
        for attr in dir(config):
            if not attr.startswith("__"):
                print(f"Attribute: {attr}")
                value = getattr(config, attr)
                
                if attr in ["CUSTOM_RULES", "CUSTOM_SYNONYMS"]:
                    value = value[0]
                
                if isinstance(value, dict):
                    setattr(self, attr.lower(), value)
                    for key, val in value.items():
                        print(f"Key: {key}, Value: {val}")
                else:
                    print(f"Value: {value}")

        
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
        """
        Initializes NLTK resources, specifically downloading the WordNet data if not already present.
        
        Checks for the presence of WordNet data and downloads it if necessary, ensuring NLTK functionalities are ready for use.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        try:
            #Try to access WordNet
            nltk.corpus.wordnet.synsets('word')
        except LookupError:
            #If WordNet is not present, download it
            nltk.download('wordnet')
    
    def from_website_gptneo_setup(self):
        """
        Downloads and Initializes the requested GPT-Neo model with the users GPU.
        
        Loads the GPT-Neo model and tokenizer with the specified model name, setting them up for use in generating text or processing inputs.
        
        Parameters:
        - model_name (str): The name of the GPT-Neo model to download.
        
        Returns:
        - None
        """
        #https://gist.github.com/pszemraj/791d72587e718aa90ff2fe79f45b3cfe
        model_3B_pars = 'EleutherAI/gpt-neo-2.7B'
        
        #gpu_mem = round(gpu_mem_total() / 1024, 2)
        
    def init_gpt_neo(self, model_name):
        """
        Initializes the GPT-Neo model and tokenizer for text generation.
        
        Loads the GPT-Neo model and tokenizer with the specified model name, setting them up for use in generating text or processing inputs.
        
        Parameters:
        - model_name (str): The name of the GPT-Neo model to load.
        
        Returns:
        - None
        """
        print("init_gpt_neo()")
        #self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.check_cuda_compatibility()
        self.model = GPTNeoForCausalLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        #return self.tokenizer, self.model
        
    def clean_gpt_out(self, text, remove_breaks=True):
        """
        Cleans the output from GPT-Neo text generation for readability and formatting.
        
        Uses the clean-text library to remove unwanted characters, fix unicode, and optionally strip line breaks from the generated text.
        
        Parameters:
        - text (str): The text output from GPT-Neo to be cleaned.
        - remove_breaks (bool, optional): Whether to remove line breaks from the text, defaults to True.
        
        Returns:
        - str: The cleaned text.
        """
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
        """
        Tests the GPT-Neo model by generating a response to a given prompt.
        
        Sets up the text-generation pipeline with the specified model, generates a response to a test prompt, and prints the cleaned output.
        
        Parameters:
        - model_name (str): The name of the GPT-Neo model to test.
        
        Returns:
        - None
        """
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
        """
        Checks for CUDA availability and prints the CUDA version if available.
        
        Verifies if the CUDA environment is available for PyTorch operations, aiding in model performance optimization.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        print("check_cuda_compatibility()")
        if torch.cuda.is_available():
            print("CUDA is available!")
            print(f"CUDA version: {torch.version.cuda}")
        else:
            print("CUDA is not available.")
            
    def nlp_load(self):
        """
        Loads Spacy's English medium model into the class attribute for NLP operations.
        
        Prepares the Spacy NLP model for text processing tasks such as tokenization, part-of-speech tagging, and named entity recognition.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        print("nlp_load()")
        self.nlp = spacy.load("en_core_web_md")
        #self.nlp.add_pipe()
        #return self.nlp
        return
    
    def __del__(self):
        """
        Custom destructor for the class to ensure proper cleanup of resources upon deletion.
        
        Specifically deletes the loaded GPT-Neo model and tokenizer to free up memory resources.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
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
        """
        Filters through Google search results to remove duplicates and previously applied jobs.
        
        This method processes the list of Google search results by removing duplicates, filtering out jobs previously applied to, and organizing remaining job links by company.
        
        Parameters:
        - google_search_results_links (list[str]): A list of job links obtained from Google search.
        
        Returns:
        - tuple: A tuple containing the filtered list of Google search results links and a list of job links organized by company.
        """
        print("filter_through_google_search_results()")
        self.previous_job_applications_data = self.convert_csv_data(self.previous_job_data_csv_relative_path)
        google_search_results_links = self.ensure_no_duplicates(google_search_results_links)
        self.previously_applied_to_job_links = self.get_job_links_users_applied_to(self.previous_job_applications_data)
        self.filter_out_jobs_user_previously_applied_to(google_search_results_links, self.previously_applied_to_job_links)
        google_search_results_links, job_links_organized_by_company = self.encapsulate_companies_urls(google_search_results_links)
        return google_search_results_links, job_links_organized_by_company
    
    def convert_csv_data(self, csv_relative_path):
        """
        Converts CSV data from a given file path into a list of lists.
        
        Reads the CSV file, skipping the header row, and converts each row into a list, with each cell's '=>' replaced by ','.
        
        Parameters:
        - csv_relative_path (str): The relative path to the CSV file.
        
        Returns:
        - list: A list of lists containing the CSV data.
        """
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
        """
        Ensures that a list contains no duplicate elements.
        
        Processes a given list and returns a new list with all duplicate elements removed.
        
        Parameters:
        - list_to_filter (list): The list to filter for duplicates.
        
        Returns:
        - list: A list with duplicates removed.
        """
        print("\nensure_no_duplicates()")
        
        unique_results = []
        for list_URL in list_to_filter:
                if list_URL not in unique_results:
                    unique_results.append(list_URL)
        return unique_results
    
    #TODO: Keep job url's
    #! Pretty sure this is the only time I use JobsThatUserHasAppliedTo.csv so it doesn't matter
    def get_job_links_users_applied_to(self, extract_URLs_from_dictionary):
        """
        Ensures that a list contains no duplicate elements.
        
        Processes a given list and returns a new list with all duplicate elements removed.
        
        Parameters:
        - list_to_filter (list): The list to filter for duplicates.
        
        Returns:
        - list: A list with duplicates removed.
        """
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
        """
        Filters out jobs from a list that the user has previously applied to.
        
        Compares a list of job links against a list of previously applied job links and removes any matches.
        
        Parameters:
        - list_to_filter (list): The list of current job links to filter.
        - previously_applied_links (list): A list of job links that the user has previously applied to.
        
        Returns:
        - list: A filtered list of job links excluding previously applied jobs.
        """
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
    
    #TODO: Write a special rule for embed 'companyNames'! If they have filter them by the 'for=forValue' forValue instead!!
    def encapsulate_companies_urls(self, list_to_filter):
        """
        Organizes job links by company base URLs to encapsulate company-specific job listings.
        
        Parses and groups job links by their base company URLs to assist in company-specific job application processes.
        
        Parameters:
        - list_to_filter (list): A list of job links to organize by company.
        
        Returns:
        - tuple: A tuple containing the updated list of job links and a list of job links organized by company.
        """
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
        """
        Prints two lists side by side for comparison.
        
        Used for debugging or comparison purposes to show how job links are filtered and updated through the process.
        
        Parameters:
        - list_to_filter (list): The original list of job links.
        - updated_google_search_results_links (list): The updated list of job links after filtering.
        
        Returns:
        - None
        """
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
        """
        Writes job application data to a CSV file.
        
        Appends a row of job application data to an existing CSV file for record-keeping purposes.
        
        Parameters:
        - job_data (list): A list of job application data to write to the CSV file.
        
        Returns:
        - str: A confirmation message indicating the data write operation is completed.
        """
        with open ('job_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            #for row in writer:
            writer.writerow(job_data)
        return "All done!"
    
   
   
   
   



    def cookie_information(self):
        """
        Fetches and prints cookie information for the current web page.
        
        Sends a POST request to the current URL with predefined parameters and prints out the cookies and response text.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        print("cookie_information()")
        current_url = self.browser.current_url
        #parameters = {'Name':'{FIRST_NAME} {LAST_NAME}', 'Email-id':'{EMAIL}','Message':'Hello cookies'}
        parameters = {'Name':'firstName lastName', 'Email-id':'Liebmann.nicholas1@gmail.com','Message':'Hello cookies'}
        r = requests.post(f"{current_url}", data = parameters)
        print('The cookie is:')
        print(r.cookies.get_dict())
        print(r.text)

    def website_modified_cookie_info(self):
        """
        Fetches and prints modified cookie information after interacting with the website.
        
        Uses a session to send a POST request with predefined parameters to the current URL and prints the modified cookies and response text.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
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
