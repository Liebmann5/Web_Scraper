from bs4 import BeautifulSoup
from selenium import webdriver

from dotenv import load_dotenv
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import csv

import time

#! from fileName import className
from GoogleSearch import scraperGoogle
from CompanyOpeningsAndApplications import CompanyWorkflow
from datetime import datetime
import openpyxl
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

import requests


import sys
print("Here's some info about sys.executable: ", sys.executable)
import config
import site



import spacy
from fuzzywuzzy import fuzz
# import Legit.config as config
# ^ handle_custom_rules()
import config

import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from transformers import GPTNeoForCausalLM, GPT2Tokenizer, pipeline
import torch

import warnings

                #Run "python|python3 -u Legit/JobSearchWorkflow.py"
                #!!!!!!!!!!!!!!!!!!! TEST THIS HAS  CHECKLIST !!!!!!!!!!!!!!!!!!!!!!!!!!
                #https://jobs.lever.co/hive/9461e715-9e58-4414-bc9b-13e449f92b08/apply
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #ThisFolderWasMadeAtThreeAM/setup.sh
                #!!!!!!!!!!!!!!!!!!! chmod +x setup.sh & .bat !!!!!!!!!!!!!!!!!!!!!!!!!!

#! EXTRACT JOB_TYPE AS LIST OD len()=3 | {DESIRED_LOCATION, HYBRID, REMOTE}
#! SINCE I SWITCHED TO A VIRTUAL ENVIRONMENT FIGURE OUT HOW TO USE "python-dotenv"!!!
#! SINCE I SWITCHED TO A VIRTUAL ENVIRONMENT FIGURE OUT HOW TO USE "python-dotenv"!!!

class Workflow():
       
    def __init__(self):
        self.browser = None
        #self.google_search_results_links = None
        self.google_search_results_links = []
        self.time_program_ran = self.get_time()
        print("This program began running at " + self.time_program_ran)
        
        #TODO: Change this name... it's all the job info a user has previously applied to!!
        self.csv_data = []
 
        self.env_path = '.env'
        self.env_other_path = '../.env'
        #self.previous_job_data_csv_relative_path = r'../Scraper/JobsThatUserHasAppliedTo.csv'
        self.previous_job_data_csv_relative_path = r'DataOutput/JobsThatUserHasAppliedTo.csv'
        self.users_information = {}
        self.total_jobs_applied_to_count = 0
        self.total_jobs_applied_to_info = {} 
        self.previous_job_applications_data = []
        self.previously_applied_to_job_links = []
        self.last_time_user_applied = None
        self.todays_jobs_applied_to_info = {}
        
        self.senior_jobs_found = {}  #Job_Title, Company_Name, Job_Location, Todays_Date
        self.entry_jobs_found = {}
        
        self.custom_rules = None
        self.q_and_a = None
        
        
        #init_gpt_neo()
        self.tokenizer = None
        self.model = None
        #load_nlp()
        self.nlp = None
        #load_company_resources()
        self.lemmatizer = None
        
        
    def job_search_workflow(self):
        self.browser_setup()
        
        self.load_company_resources()
        self.ludacris_speed_apply_to_jobs()
        self.__del__()
        
        
        
        # self.google_search_results_links, last_link_from_google_search, user_desired_jobs = scraperGoogle(self.browser).user_requirements()
        google_search_results_links, last_link_from_google_search, user_desired_jobs = scraperGoogle(self.browser).user_requirements()
        print("DOPE")
        print(self.google_search_results_links)
        print("DOPER")
        time.sleep(3)

        self.google_search_results_links = self.filter_through_google_search_results(google_search_results_links)
        self.load_company_resources(self)
        self.apply_to_jobs(last_link_from_google_search, user_desired_jobs)
        
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
                print("That's kinda messed up dog... I give you an opportunity to pick and you pick some dumb crap.")
                print("You've squandered any further opportunities to decide stuff. I hope you are happy with yourself.")
                print("Don't worry clown I'll pick for you!")
                #TODO: Make else just check OS and return number of that OS's web browser!!!
                #! THIS IS A while loop.... so it runs until false
        return users_browser_choice, browser_name
    
    #! I have browser setup called 1st and then users_browser_choice b/c if the user uses the same browser over & over this will remember it!!!
    #? ALSO!!!... setting code up this way might lead to very good, safe, and secure code because in no way can an outside person send in any code right from the get go!!! Meaning if they can't use the browser to begin with then the rest of the code is rendered useless...  right?!?!?!?
    def browser_setup(self):
        users_browser_choice, browser_name = self.users_browser_choice()
        print('Execution Started -- Opening' + browser_name + 'Browser')
        
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
        print("Begin the sex Batman... Robin... I'll need an extra set of hands in a second so hang tight")
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
                # print("This is the dumb selenium element outerHTML: ")
                # print(soup_outer.prettify())
                # print("------------------------------------------------------")
                # print("This is the dumb selenium element innerHTML: ")
                # print(soup_inner.prettify())
                # print("------------------------------------------------------")
                # print("This is my attempt to find the <a>: ")
                # print(dumb_a_tag_link)
                # print("------------------------------------------------------Kenny Powers")
                # some_crap = self.test_click_element(dumb_a_tag_link)
                # print(some_crap)
                # time.sleep(15)
                if not self.safe_click(last_link_from_google_search):
                    print("Clicking on the element failed.")
                
                
                 
                
                # last_a_tag = last_link_from_google_search.find_element(By.TAG_NAME, 'a')
                # last_a_tag.click()
                clicked_link_from_google_search = True
                print("Accidently clamped my testicles b/c I needed to be punished")
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
            #self.todays_jobs_applied_to_info = CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.todays_jobs_applied_to_info, senior_experience=False).company_workflow(job_link)
            CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.todays_jobs_applied_to_info, senior_experience=False).test_this_pile_of_lard(job_link)
    '''
    
    
    #TODO: Try the way ChatGPT suggested seemed better -> StaleElementReferenceException
    def apply_to_jobs(self, last_link_from_google_search, user_desired_jobs):
        print("Begin the sex Batman... Robin... I'll need an extra set of hands in a second so hang tight")
        clicked_link_from_google_search = False
        for i in range(len(self.google_search_results_links) - 1, -1, -1):
            job_link = self.google_search_results_links[i]
            if not clicked_link_from_google_search:
                print(last_link_from_google_search)
                self.browser.execute_script("arguments[0].scrollIntoView();", last_link_from_google_search)
                print("Scrolled to this place...\n")
                time.sleep(5)

                diagnostics = self.diagnose_interaction(last_link_from_google_search)
                for check, result in diagnostics.items():
                    print(f"{check}: {result}")

                try:
                    # Try to click the element
                    if not self.safe_click(last_link_from_google_search):
                        print("Clicking on the element failed.")
                except Exception as e:
                    print(f"Safe click failed: {e}")
                
                clicked_link_from_google_search = True
                print("Accidently clamped my testicles b/c I needed to be punished")
                wait_fur_this = self.wait_for_element_explicitly(self.browser, 10, (By.TAG_NAME, 'a'), 'visibility')
                print("This time wasn't an accident!")
                time.sleep(4)

            else:
                print(job_link)
                self.browser.get(job_link)
                time.sleep(5)
            
            print("\n\n" + "--------------------------------------------" + "\nTransferring power to CompanyWorkflow")
            CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.todays_jobs_applied_to_info, senior_experience=False).test_this_pile_of_lard(job_link)

    def ludacris_speed_apply_to_jobs(self, user_desired_jobs=None):
        print("Begin the sex Batman... Robin... I'll need an extra set of hands in a second so hang tight")
        self.load_users_information()
        print("Accidently clamped my testicles b/c I needed to be punished")

        print("\n\n" + "--------------------------------------------" + "\nTransferring power to CompanyWorkflow")
        CompanyWorkflow(self, self.browser, self.users_information, user_desired_jobs, self.todays_jobs_applied_to_info, self.tokenizer, self.model, self.nlp, self.lemmatizer, self.custom_rules, self.q_and_a, senior_experience=False).test_this_pile_of_lard('https://www.google.com')

    def safe_click(self, element):
        print("safe_click()")
        
        # First, try clicking normally
        print("1) Normal click attempt")
        try:
            element.click()
            return True
        except Exception as e:
            print(f"1) Normal click failed: {e}")

        # Next, try waiting for the element to be clickable
        print("2) Waiting for element to be clickable attempt")
        try:
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.TAG_NAME, element.tag_name)))
            element.click()
            return True
        except TimeoutException as e:
            print(f"2) Waiting for element to be clickable failed: {e}")

        # Then, try scrolling the element into view and clicking
        print("3) Waiting for element to be clickable attempt")
        try:
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            return True
        except Exception as e:
            print(f"4) Scrolling and clicking failed: {e}")

        # Next, try checking if the element is displayed before clicking
        print(f"5.1) Checking visibility and clicking attempt")
        try:
            if element.is_displayed():
                element.click()
                return True
            else:
                print("5.2)Element is not visible")
        except Exception as e:
            print(f"5.3) Checking visibility and clicking failed: {e}")

        # Finally, try using JavaScript to perform the click
        print(f"6) JavaScript click attempt")
        try:
            self.browser.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"6) JavaScript click failed: {e}")

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
            if element.is_displayed():
                diagnostics["Displayed"] = "Yes"
            else:
                diagnostics["Displayed"] = "No"
        except Exception as e:
            diagnostics["Displayed"] = f"Error: {e}"

        # Check 3: Is the element enabled?
        try:
            if element.is_enabled():
                diagnostics["Enabled"] = "Yes"
            else:
                diagnostics["Enabled"] = "No"
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
            children = element.find_elements(By.XPATH, ".//*")
            if children:
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
        wait = WebDriverWait(browser, timeout)
        
        if condition == 'presence':
            return wait.until(EC.presence_of_element_located(locator_tuple))
        elif condition == 'visibility':
            return wait.until(EC.visibility_of_element_located(locator_tuple))
        elif condition == 'clickable':
            return wait.until(EC.element_to_be_clickable(locator_tuple))
        else:
            raise ValueError(f"Invalid condition: {condition}")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    
        
    def show_warning(message, category, filename, lineno, file=None, line=None):
        print(f"Warning: {message}")
    warnings.showwarning = show_warning
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                      LOAD RESOURCES AND LIBRARIES                             !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def load_company_resources(self):
        print("load_company_resources()")
        self.load_users_information()
        print("  Loaded Users Information...")
        self.load_custom_rules()
        print("  Loaded Custom Rules...")
        
        print(self.custom_rules)
        print(self.q_and_a)
        
        self.nlp_load()
        print("  Loaded Users Information...")
        
        model_3B_pars = 'EleutherAI/gpt-neo-2.7B'
        self.init_gpt_neo(model_3B_pars)
        print("  Initialized GPT-Neo-2.7B...")
        
        # self.test_gpt_neo(model_3B_pars)
        # print("  Testicalized GPT-Neo-2.7B...")
        
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
        print("load_custom_rules()")
        print("dir(config) = ", dir(config))
        
        for attr in dir(config):
            if not attr.startswith("__"):
                print(f"Attribute: {attr}")
                value = getattr(config, attr)
                
                if attr == "CUSTOM_RULES":
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
    
    # def filter_through_google_search_results(self):
    #     self.previous_job_applications_data = self.convert_csv_data(self.previous_job_data_csv_relative_path)
    #     self.google_search_results_links = self.ensure_no_duplicates(self.google_search_results_links)
    #     self.previously_applied_to_job_links = self.get_job_links_users_applied_to(self.previous_job_applications_data)  #and filter them out!
    #     self.filter_out_jobs_user_previously_applied_to(self.google_search_results_links, self.previously_applied_to_job_links)
    
    def filter_through_google_search_results(self, google_search_results_links):
        self.previous_job_applications_data = self.convert_csv_data(self.previous_job_data_csv_relative_path)
        google_search_results_links = self.ensure_no_duplicates(google_search_results_links)
        self.previously_applied_to_job_links = self.get_job_links_users_applied_to(self.previous_job_applications_data)  #and filter them out!
        self.filter_out_jobs_user_previously_applied_to(google_search_results_links, self.previously_applied_to_job_links)
        return google_search_results_links
    
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
    
    #TODO: Keep job url's
    #! Pretty sure this is this is the only time I use JobsThatUserHasAppliedTo.csv so it doesn't matter
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
        if self.last_time_user_applied == None:
            self.last_time_user_applied = extract_URLs_from_dictionary[-1][-1]
            print("And this is when you last applied... Tom")
            print(self.last_time_user_applied)
        return URLs_list
    
    #TODO: FINISH BOTH OF THESE!!
    #Use Quick Sort to sort jobs_previously_applied_to
    #! We run this when we finish running other_company_openings()!!!!
    #! And self.google_search_results_links can stay in the method b/c nothing changes this value!! (b/c if it needed any we already applied it!)
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
        
        print("These are all the links you already applied to... ")
        print(previously_applied_links)
        print("Swedish semen... yummy " + str(len(Lake_Minnetonka_Purified_list)) + " timber logs.\n")
        #print(Lake_Minnetonka_Purified_list)
        return Lake_Minnetonka_Purified_list
    
    def ensure_no_duplicates(self, list_to_filter):
        print("\nensure_no_duplicates() = ")
        
        unique_results = []
        for list_URL in list_to_filter:
                if list_URL not in unique_results:
                    unique_results.append(list_URL)
                else:   #THIS ELSE AND 2 PRINT STATEMENTS ARE PURELY FOR TESTING!!!
                    print("Repeated Link Found: ", end="")
                    print(list_URL)
        return unique_results
    
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
        parameters = {'Name':'Nick Liebmann', 'Email-id':'Liebmann.nicholas1@gmail.com','Message':'Hello cookies'}
        r = requests.post(f"{current_url}", data = parameters)
        print('The cookie is:')
        print(r.cookies.get_dict())
        print(r.text)

    def website_modified_cookie_info(self):
        print("website_modified_cookie_info()")
        current_url = self.browser.current_url
        session = requests.Session()
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














