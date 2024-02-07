#This class currently includes the entire application process from deciding if candidate fits the description and description
#fits the user to applying! It also finds the specifics company other job openings webpage and applies to at max the 5 best
#matches. The last thing needed here is figuring out the logic handling for answering questions!

from urllib import request
import requests
from urllib.parse import urlparse, parse_qs, urljoin
from bs4 import BeautifulSoup
import csv
import bs4
from bs4 import Tag
from bs4.element import NavigableString
import spacy
from fuzzywuzzy import fuzz
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import torch
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException



import re
import config
import concurrent.futures
import json


import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# import codecs
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
from bs4 import UnicodeDammit
#import chardet

# https://www.sqlitetutorial.net/sqlite-insert/
# https://www.w3resource.com/sqlite/sqlite-update.php
# https://www.pythontutorial.net/python-basics/python-write-csv-file/
# https://vhernando.github.io/sqlite3-cheat-sheet
# https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager-webext/?src=search
# https://www.freecodecamp.org/news/how-to-build-a-todo-app-with-react-typescript-nodejs-and-mongodb/
# https://www.freecodecamp.org/news/deploying-a-mern-application-using-mongodb-atlas-to-heroku/
# https://www.digitalocean.com/community/tutorials/how-to-build-a-react-to-do-app-with-react-hooks
# https://github.com/typescript-cheatsheets/react
# https://www.freecodecamp.org/news/react-props-cheatsheet/
# tp-link POE switch TL-SG105MPE
# https://practicaldatascience.co.uk/data-science/how-to-parse-url-structures-using-python

# https://www.codementor.io/blog/python-web-scraping-63l2v9sf2q
# https://gist.github.com/magicznyleszek/809a69dd05e1d5f12d01


#https://gworks.bamboohr.com/careers/38


#https://stackoverflow.com/questions/40697845/what-is-a-good-practice-to-check-if-an-environmental-variable-exists-or-not
#https://pyshark.com/manage-environment-variables-using-dotenv-in-python/
#https://docassemble.org/docs/security.html


#!!!!!!!!!!!!!!!!!!!!!!!!
# TODO
# Make a method called stamp_variable() that before going to the next iteration in the index applies the 'status' key-value input to self.current_jobs_details!!!
# Unicode - these give me ERRORS; figure out a way to either fix this or bypass it!!
    # Ex) <span class="s1">💰</span>
# Add lookout for 'Secret' keywords!!  (Ex. Top Secret Clearance, Secret Clearance, etc.)
# The meta information retrieved from the page includes an Open Graph (OG) URL: https://boards.greenhouse.io/cruise/jobs/5285116
# IGNORE/SKIP THESE: https://boards.eu.greenhouse.io/embed/job_board?for=iremboltd&b=https%3A%2F%2Firembo.com%2Fcareers%2F
# FOR INITIAL LINK WE FIRST LOOK FOR THE self.companys_internal_job_openings_URL AND VISIT IT IF FOUND...
    # BUT IF FOUND AND AFTER WE VISIT IT WE RETURN BACK TO THE INITIAL LINK!!! This is an !ERROR! ssooo check if that link is present in the 'Internal-Job-Listing' page and if yes skip it!
#!!!!!!!!!!!!!!!!!!!!!!!!


#NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
#greenhouse:
# <button aria-describedby="cover_letter-allowable-file-types" class="unstyled-button link-button" data-source="attach" name="button" type="button">Attach</button>

#NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE


class CompanyWorkflow():

    def __init__(self, JobSearchWorkflow_instance, browser, users_information, users_job_search_requirements, jobs_applied_to_this_session, tokenizer, model, nlp, lemmatizer, custom_rules, q_and_a, custom_synonyms):
        if JobSearchWorkflow_instance is None or browser is None:
            raise ValueError("JobSearchWorkflow_instance and browser cannot be None.")
        
        self.JobSearchWorkflow_instance = JobSearchWorkflow_instance
        self.browser = browser
        self.current_url = None
        self.list_of_links = []
        self.users_information = users_information
        self.users_job_search_requirements = users_job_search_requirements
        self.application_company_name = None
        self.companys_internal_job_openings_URL = None
        self.prior_experience_keywords = ["senior", "sr", "principal", "lead", "manager", "director"]
        self.jobs_applied_to_this_session = jobs_applied_to_this_session
        self.one_resume_label = False
        self.form_input_details = {}
        self.form_input_extended = None
        self.tokenizer = tokenizer
        self.model = model
        self.nlp = nlp
        self.lemmatizer = lemmatizer
        self.custom_rules = custom_rules
        self.q_and_a = q_and_a
        self.custom_synonyms = custom_synonyms
        self.env_path = '.env'
        self.job_application_webpage = ["Internal-Job-Listings", "Job-Description", "Job-Application", "Submitted-Application"]
        self.soup_elements = {}
        self.variable_elements = {}
        self.current_jobs_details = {}
        self.website_data = {}
        
        self.website_elements_relative_path = r'AutoApply/website_elements.json'
        #self.job_workplaceType = ["in-office", "hybrid", "remote"]
        
        
        #TODO: FIGURE THIS OUT FIGURE THIS OUT
        self.companys_every_job_detail = {}
        #TODO: FIGURE THIS OUT FIGURE THIS OUT
        
        
        
    #NEW NEW NEW
    def write_to_text_file():
        # When writing to a file
        # with open('terminalOutput.txt', 'w', encoding='utf-8', errors='ignore') as f:
        #     print(soup.prettify(), file=f)
        with io.open('terminalOutput.txt', 'a', encoding='utf-8') as file:
            file.write(f"Result for stuff\n")

    
    
    def keep_jobs_applied_to_info(self):
        print("\nkeep_jobs_applied_to_info()")
        self.jobs_applied_to_this_session.append(self.current_jobs_details)
        
    def reset_webpages_soup_elements(self):
        print("\nreset_webpages_soup_elements()")
        self.soup_elements = {}

    #!TODO: Look into JSON for this stuff!!
    def reset_webpages_variable_elements(self):
        print("\nreset_webpages_variable_elements()")
        self.variable_elements = {}

    def reset_every_job_variable(self):
        print("\nreset_every_job_variable()")
        self.init_current_jobs_details()
        self.reset_webpages_soup_elements()
        self.reset_webpages_variable_elements()
        self.form_input_details = {}
        self.form_input_extended = None

    # HERE JUST AS A REMINDER!!!
    # def init_users_job_search_requirements(self): = = =>  users_job_search_requirements
    #     self.users_job_search_requirements = {
    #         "user_desired_job_titles": [],
    #         "user_preferred_locations": [],
    #         "user_preferred_workplaceType": ["in-office", "hybrid", "remote"],
    #         "employment_type": [],
    #         "entry_level": True, 
    #     }
    
    def init_current_jobs_details(self):
        print("\ninit_current_jobs_details()")
        self.current_jobs_details = {
            "job_url": None,
            "job_title": None,
            "job_location": None,
            "company_name": None,
            "job_workplaceType": None,
            "company_department": None,
            "job_id_number": None,
            "job_release_date": None,
            "employment_type": None,
            "experience_level": None,
            "years_of_experience": None,
            "company_industry": None,
        }
    

    #Get length of list and in the while have an if count < length run self.determine_current_page()
    #TODO: ^ Needs to be implemented because if a job is only up for 30 seconds then whenn we visit it we'll get redirected back to internal job openings
    def company_workflow(self, incoming_link):
        # sourcery skip: remove-redundant-pass
        print("\ncompany_workflow()")
        print(f">>>>>  {incoming_link}")
        #! self.current_url HERE AND ONLY HERE is different becuase this link comes from google_search_results!!!!!
        if isinstance(incoming_link, list):
            self.current_url = incoming_link[0]
            self.list_of_links = incoming_link.copy()
        elif isinstance(incoming_link, str):
            self.current_url = incoming_link
            self.list_of_links.append(incoming_link)

        self.determine_application_company_name()
        og_webpage_num = self.determine_current_page(self.current_url)
        print(f"       og_webpage_num = {og_webpage_num}")
        #print(f"       og_webpage_num = " + {og_webpage_num})
        webpage_num = og_webpage_num
        initial_link_processed_internal_job_listings = False
        if webpage_num == 0:
            self.companys_internal_job_openings_URL = self.current_url
        elif self.is_internal_job_openings_URL_present(self.current_url):
            webpage_num = 0
            # Flag to control one-time execution
            initial_link_processed_internal_job_listings = True

        index = 0
        #TODO: incorporate index into ==> self.current_jobs_details {MAYBE ensure order is all good!!}!!!!!!!!!
        while index < len(self.list_of_links):
            link = self.list_of_links[index]
            if self.companys_every_job_detail:
                self.fetch_matching_current_jobs_details(link)
            
            # if self.current_url != link:
            if self.check_if_webpage_changed():
                print("DIDN'T WORK!!!!")
                self.change_page(link)
            else:
                print("Should only skip the 1st index as that will be the only current_url value that we assign to current_value prior to an iteration in this for loop")
                pass
            
            print(f"The current url is {self.current_url}")
                
            #TODO: refactor this!
                #! FAILS: If "Internal-Job-Listings" is the initial webpage this ruins
            if not self.companys_internal_job_openings_URL:
                self.try_finding_internal_job_openings_URL() #link !!!!!!!
                webpage_num = 0
            if self.job_application_webpage[webpage_num] == "Internal-Job-Listings":
                print("\n   >Internal-Job-Listings<")
                self.check_companies_other_job_openings(link)
                if initial_link_processed_internal_job_listings:
                    webpage_num = og_webpage_num
                else:
                    # NEW NEW NEW NEW
                    if len(self.list_of_links) == 1 and link == self.companys_internal_job_openings_URL:
                        print("The initial link was self.companys_internal_job_openings_URL and no jobs were found so skip this crummy company!")
                        #continue
                        pass
                    else:
                    # NEW NEW NEW NEW
                        webpage_num = 1
            print(f"       webpage_num = {webpage_num}")
            #*******************************************************
            #*******************************************************
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
            # #TODO: change webpage --> self.companys_internal_job_openings_URL
            #     #??? What if already on this page??? Like what if it is the initial link!?!?!?
            # if self.browser.current_url != self.companys_internal_job_openings_URL:
            #     self.change_page(self.companys_internal_job_openings_URL)
            # self.soup_elements['soup'] = self.apply_beautifulsoup(self.current_url, "lxml")
            # list_of_job_urls = self.collect_companies_current_job_openings(self.soup_elements['soup'])
            # self.update_list_of_links(list_of_job_urls)
            # self.filter_list_of_links()
            # self.change_page(link)
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            #*******************************************************
            #*******************************************************
            
            #TODO: FIGURE THIS FLOW OUT!!!!
            self.reset_webpages_soup_elements()
            if self.job_application_webpage[webpage_num] == "Job-Description":
                print("\n   >Job-Description<")
                webpage_num = self.analyze_job_suitabililty()
                if self.job_application_webpage[webpage_num] == "Job-Application":
                    print("\n   >Job-Application<")
                    webpage_num = self.apply_to_job()
                if self.job_application_webpage[webpage_num] == "Submitted-Application":
                    print("\n   >Submitted-Application<")
                    self.confirmation_webpage_proves_application_submitted()
                    webpage_num = 1
            else:
                print("   >If determine_current_page() returns 2 it cant be accessed and the while will just skip to the next link!<")
                self.reset_every_job_variable()
                webpage_num = 1
            
            print(f"WHILE WHILE\n   self.list_of_links = {self.list_of_links}\n")    
            index += 1
        return print("--------------------------------------------\nTransferring power to JobSearchWorkflow")
    
    
    
    #print("\n()")
#!======= company_workflow variables ==========
    def determine_application_company_name(self):
        """
        Determines the company handling the application which is essentially just the current URL in the `CompanyOpeningsAndApplications` class.
        The options use to be ashby, greenhouse, and lever! I say 'use to' because the goal of this class was to be capable of working for any
        and all online job applications. My assumption was by having 3 different forms allowed me to seperate each and compare them against each
        other to figure out how to do just that.
        UPDATE: Figured it out by treating it like a hierarchy structure and breaking it down. 
        
        Args:
            self: The instance of the `CompanyOpeningsAndApplications` class.

        Returns:
            None

        Examples:
            ```
            coaa = CompanyOpeningsAndApplications()
            coaa.determine_application_company_name()
            ```
        """
        print("\ndetermine_application_company_name()")
        #self.set_current_url()
        
        print(f"       self.current_url = {self.current_url}")
        #https://jobs.eu.lever.co/payu/5c0cb9f5-e898-4fcc-8da2-30cfc48f5faf
        if "jobs." in self.current_url and ".lever.co" in self.current_url:
            self.application_company_name = "lever"
        elif "boards." in self.current_url and ".greenhouse.io" in self.current_url:
            self.application_company_name = "greenhouse"
        else:
            print("Neither 'lever' nor 'greenhouse' ssooo...   idk")

    
    #TODO: add variable => self.soup_elements
    def apply_beautifulsoup(self, job_link, parser):
        #*******************************************************
        #*******************************************************
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        print("\napply_beautifulsoup()")
        if parser == "lxml":
            result = requests.get(job_link)
            content = result.text
            soup = BeautifulSoup(content, "lxml")
        elif parser == "html":
            page = requests.get(job_link)
            result = page.content
            soup = BeautifulSoup(result, "html.parser")           
        return soup
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #*******************************************************
        #*******************************************************
        """
        Applies BeautifulSoup parsing to a given job link using the specified parser in the `CompanyOpeningsAndApplications` class.
        UPDATE: BeautifulSoup is having a lot of trouble with 'encodings'!!

        Args:
            self: The instance of the `CompanyOpeningsAndApplications` class.
            job_link (str): The link of the job to parse.
            parser (str): The parser to use for parsing the job link. Valid values are "lxml" and "html".

        Returns:
            BeautifulSoup: The parsed soup object.

        Examples:
            ```
            coaa = CompanyOpeningsAndApplications()
            soup = coaa.apply_beautifulsoup("https://example.com/job", "lxml")
            ```

        """
        #------------------------------------------
        # import chardet
        # from bs4 import UnicodeDammit
        # print("\napply_beautifulsoup()")
        
        
        # #result = requests.get(job_link)
        # response = requests.get(job_link)
        # #response = result.text
    
        # # Detect the encoding using chardet
        # detected_encoding = chardet.detect(response.content)['encoding']
        # print("Detected Encoding:", detected_encoding)

        # # Use UnicodeDammit to convert to UTF-8
        # unicode_dammit = UnicodeDammit(response.content)
        # print("UnicodeDammit Original Encoding:", unicode_dammit.original_encoding)
        # print("UnicodeDammit Declared HTML Encoding:", unicode_dammit.declared_html_encoding)
        
        # unicode_sucks = UnicodeDammit(response.content, [detected_encoding])
        # content = unicode_sucks.unicode_markup
        
        # if parser == "lxml":
        #     # result = requests.get(job_link)
            
        #     # result.encoding = 'utf-8'
            
        #     # content = result.text
        #     soup = BeautifulSoup(content, "lxml")
        # elif parser == "html":
        #     # page = requests.get(job_link)
            
        #     # page.encoding = 'utf-8'
            
        #     # result = page.content
        #     # soup = BeautifulSoup(result, "html.parser")
        #     soup = BeautifulSoup(content, "html.parser")
            
        # # Convert the soup object to a string and handle encoding issues
        # return soup
        #------------------------------------------
        # response = requests.get(job_link)

        # # Detect encoding using chardet
        # encoding = chardet.detect(response.content)['encoding']

        # # Use UnicodeDammit to handle encoding
        # unicode_dammit = UnicodeDammit(response.content, [encoding])
        # fixed_html = unicode_dammit.unicode_markup

        # if parser == "lxml":
        #     soup = BeautifulSoup(fixed_html, "lxml")
        # elif parser == "html":
        #     soup = BeautifulSoup(fixed_html, "html.parser")

        # return soup
        #------------------------------------------
        # response = requests.get(job_link)

        # # Use UnicodeDammit to handle encoding
        # unicode_dammit = UnicodeDammit(response.content)
        # fixed_html = unicode_dammit.unicode_markup

        # if parser == "lxml":
        #     soup = BeautifulSoup(fixed_html, "lxml")
        # elif parser == "html":
        #     soup = BeautifulSoup(fixed_html, "html.parser")

        # return soup


    def update_soup_elements(self, soup, **kwargs):
        print("\nupdate_soup_elements()")
        self.soup_elements.update({'soup': soup, **kwargs})
    
    def update_list(self, list_of_new_values, list_to_update):
        print("\nupdate_list()")
        list_to_update.extend(list_of_new_values)
        return list_to_update
    
    def update_list_of_links(self, list_of_job_urls):
        print("\nupdate_list_of_links()")
        self.list_of_links.extend(list_of_job_urls)
#!==============================================
    
#!========== changing webpages tools ===========
    #NOTE: "Single Responsibility Principle" - which states that a function should do one thing and do it well
    def change_page(self, link):
        print("\nchange_page()")
        try:
            self.browser.get(link)
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            # self.set_current_url()
            self.adjust_for_new_webpage()
        except Exception as e:
            print(f"An error occured while changing webpages: {e}")
        
    def set_current_url(self):
        print("\nset_current_url()")
        self.current_url = self.browser.current_url
    
    # Mainly just for clicking buuttons!!  Like last job in "Internal-Job-Listings" and clicking submit, etc.
    def check_for_webpage_change(self):
        print("\ncheck_for_webpage_change()")
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        if self.check_if_webpage_changed():
            self.adjust_for_new_webpage()
            return True
        return False
    
    def check_if_webpage_changed(self):
        print("\ncheck_if_webpage_changed()")
        #TODO: Is there a need for this here or is check_for_webpage_change() good enough!!
            #?? I think so cause then I can just click then call this method immediately and this method will do the waiting!
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        return self.browser.current_url != self.current_url

    def adjust_for_new_webpage(self):
        print("\nadjust_for_new_webpage()")
        self.set_current_url()
        self.reset_webpages_soup_elements()
        self.reset_webpages_variable_elements()
#!==============================================    
    



#!============== misc tools ====================
    #TODO: Make sure that if I update the values in self.current_jobs_details after running this they'll affect the ones in self.all_job_details
    def fetch_matching_current_jobs_details(self, link):
        for correct_current_jobs_details in self.companys_every_job_detail:
            if correct_current_jobs_details['job_url'] == link:
                self.current_jobs_details = correct_current_jobs_details
    
    def click_this_button(self, button):
        self.scroll_to_element(button)
        button.click()
        if self.check_for_webpage_change():
            #Do stuff
            pass
    
    def scroll_to_element(self, element):
        print("\nscroll_to_element()")
        if isinstance(element, Tag):
            tag_name = element.name
            attrs = element.attrs
            css_selectors = [f"{tag_name}"]
            for attr, value in attrs.items():
                if isinstance(value, list):
                    value = " ".join(value)
                    css_selectors.append(f"[{attr}='{value}']")
            css_selector = "".join(css_selectors)
            element = self.browser.find_element(By.CSS_SELECTOR, css_selector)
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(3)
        return

    def dismiss_random_popups(self):
        print("\ndismiss_random_popups()")
        wait = WebDriverWait(self.browser, 10)
        try:
            overlay_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cc-desktop button.cc-dismiss')))
            time.sleep(2)
            if overlay_close_button.is_displayed() and overlay_close_button.is_enabled():
                overlay_close_button.click()
        except TimeoutException:
            print("ok that took a while because I thought there would be a pop-up...     ONWARD I suppose!")
        except ElementNotInteractableException:
            print("Failed to click the 'Dismiss' button because it's not interactable.")

    #! NOT IN USE: don't have a use for this anymore but keeping it in case I do
    def troubleshoot_xpath(self):
        print("\ntroubleshoot_xpath()")
        for link in self.list_of_links:
            try:
                self.browser.get(link)
                time.sleep(2)
                job_title = self.browser.title
                google_search_name = job_title.split("-")[0].strip()
                selenium_google_link = self.browser.find_element(By.XPATH, f'//ancestor::a/h3[not(descendant::br)][text()="{google_search_name}"]')
                selenium_google_link.click()
                WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
                self.browser.switch_to.window(self.browser.window_handles[-1])
                self.scrape_job_page()
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
            except NoSuchElementException:
                print(f"No search result found for: {google_search_name}")
                continue

    #TODO: Figure out HOW AND WHERE to implement this!!!!!
    #NOTE: https://pypi.org/project/fasttext-langdetect/
    #NOTE: pip install fasttext-langdetect
    #NOTE: https://fasttext.cc/docs/en/language-identification.html
    # def check_language_of_webpage(self, text):
    def check_language_of_webpage(self):
        import fasttext
        soup = self.soup_elements['soup']
        text = soup.get_text()
        model = fasttext.load_model('lid.176.bin')
        predictions = model.predict(text)
        language_of_webpage = predictions[0][0].replace('__label__', '')
        #TODO: Determine whether this should go here or somewhere else!!
        # if language_of_webpage == 'en':
        #     return True
        # else:
        #     return False
        # = = = = 
        # return language_of_webpage == 'en'
        return language_of_webpage
#!==============================================

#??????????? FIX
#*********** FIX
# TODO TODO  FIX
#!===== companys_internal_job_openings_URL =====
    def alter_url_to_job(self, current_url, job_opening_href):
        print("\nalter_url_to_job()")
        print(f" current_url = {current_url}")
        print(f" job_opening_href = {job_opening_href}")
        button_to_job_description = job_opening_href
        job_link = job_opening_href.get('href')
        domain_name = self.try_adjusting_this_link(current_url)
        job_path = job_opening_href.get('href')
        job_url = domain_name + job_path
        print(f"    --> {job_url}")
        return job_url

    def url_parser(self, url):
        print("url_parser()")
        parts = urlparse(url)
        directories = parts.path.strip('/').split('/')
        queries = parts.query.strip('&').split('&')
        
        elements = {
            'scheme': parts.scheme,
            'netloc': parts.netloc,
            'path': parts.path,
            'params': parts.params,
            'query': parts.query,
            'fragment': parts.fragment,
            'directories': directories,
            'queries': queries,
        }
        
        return elements
    
    def recognized_pattern_based_url(self, link):
        print(f"\nrecognized_pattern_based_url()")
        elements = self.url_parser(link)
    
        # Keep only the first segment of the path
        new_path = elements['directories'][0] if elements['directories'] else ''
        
        # Reconstruct the URL with the new path
        new_url = f"{elements['scheme']}://{elements['netloc']}/{new_path}"

        return new_url
    
    def try_finding_internal_job_openings_URL(self):
        print("\ntry_finding_internal_job_openings_URL()")

        # List of methods that return possible links
        link_methods = [
            lambda: self.soup_elements['soup'].find_all('a'),
            lambda: self.hard_coded_link_extraction(self.current_url)
        ]

        # Apply BeautifulSoup to the current URL
        self.soup_elements['soup'] = self.apply_beautifulsoup(self.current_url, "lxml")

        # Iterate through the link methods and process the links
        for link_method in link_methods:
            possible_links = link_method()
            if self.is_internal_job_openings_URL_present(possible_links):
                print("Found the internal job openings URL")
                break
        return
    
    #TODO: HERE HERE HERE
    def is_internal_job_openings_URL_present(self, viable_link):
        print("\nis_internal_job_openings_URL_present()")
        if isinstance(viable_link, list):
            link_to_internal_job_openings = self.process_links(viable_link)
        #TODO: Just make this a list full of all the possible URL's utilizing each unique directory ending!!!
        elif isinstance(viable_link, str):
            link_to_internal_job_openings = self.recognized_pattern_based_url(viable_link)
            #link_to_internal_job_openings = self.test_links_if_internal_job_openings_URL(link_to_internal_job_openings)
            
        # Assign the value to the global variable and return True if found
        if link_to_internal_job_openings:
            self.companys_internal_job_openings_URL = link_to_internal_job_openings
            return True
        return False
    
    def hard_coded_link_extraction(self, url):
        print("\nhard_coded_link_extraction()")
        webpage_currently = self.browser.current_url
        self.soup_elements['soup'] = self.apply_beautifulsoup(webpage_currently, "lxml")
        if self.application_company_name == "lever":
            company_open_positions = self.soup_elements['soup'].find('a', {"class": "main-header-logo"})
            application_webpage_html = self.soup_elements['soup'].find("div", {"class": "application-page"})
            if not self.companys_internal_job_openings_URL:
                try:
                    self.soup_elements['webpage_body'] = self.soup_elements['soup'].find('body')
                    links_in_header = []
                    links_in_header.append(webpage_currently)
                    webpage_header = self.soup_elements['webpage_body'].find('div', {"class": 'main-header-content'})
                    company_open_positions_a = webpage_header.find('a', {"class": "main-header-logo"})
                    try:
                        if company_open_positions_a['href']:
                            company_open_positions_href = company_open_positions_a['href']
                            links_in_header.append(company_open_positions_href)
                    except:
                        pass
                    links_in_header.append(company_open_positions_a)
                    self.check_banner_links(links_in_header)
                except:
                    raise ConnectionError("ERROR: Companies other open positions are not present")
        elif self.application_company_name == "greenhouse":
            # webpage_currently = self.browser.current_url
            if not self.companys_internal_job_openings_URL:
                try:
                    self.soup_elements['soup'] = self.apply_beautifulsoup(webpage_currently, 'html.parser')
                    self.soup_elements['div_main'] = self.soup_elements['soup'].find("div", id="main")
                    self.soup_elements['header'] = self.soup_elements['soup'].find('header')
                    self.soup_elements['app_body'] = self.soup_elements['div_main'].find('div', id=lambda x: x in ["app-body", "app_body"])
                    
                except:
                    raise ConnectionError("ERROR: Companies other open positions are not present")
                    
            a_fragment_identifier = None
            company_other_openings_href = None
            first_child = True
            searched_all_a = False
            string_tab = '\n'
            for child in self.soup_elements['header'].children:
                if first_child:
                    first_child = False
                    continue
                elif child == string_tab:
                    pass
                elif child.name == "a" and not searched_all_a:
                    header_a_tags = self.soup_elements['header'].find_all('a')
                    for head_a_tag in header_a_tags:
                        if '/' in head_a_tag['href']:
                            company_other_openings_href = head_a_tag
                        elif '#' in head_a_tag['href']:
                            a_fragment_identifier = head_a_tag
                        elif head_a_tag == None:
                            logo_container = self.soup_elements['app_body'].find('div', class_="logo-container")
                            company_openings_a = logo_container.find('a')
                            company_other_openings_href = company_openings_a['href']
                            searched_all_a = True
            if company_other_openings_href == None:
                self.print_companies_internal_job_opening("greenhouse_io_banner()", "greenhouse", JobHREF="Couldnt Find", LinkToApplication_OnPageID=a_fragment_identifier)
            else:
                self.print_companies_internal_job_opening("greenhouse_io_banner()", "greenhouse", JobHREF=company_other_openings_href, LinkToApplication_OnPageID=a_fragment_identifier)
                
    def check_banner_links(self, links_in_header):
        print("\ncheck_banner_links()")
        first_link = True
        #list_of_other_jobs_keyword = ''
        for header_link in links_in_header[:-1]:
            if first_link == True and "lever" == self.application_company_name:
                self.try_adjusting_this_link(header_link)
                #list_of_other_jobs_keyword = 'list-page'
                first_link = False
            elif first_link == True and "greenhouse" in self.application_company_name:
                #<div id="embedded_job_board_wrapper" style="padding: 20px;">
                #<h2 id="board_title">Current Job Openings</h2>
                    #NOTE: Ex)<h1 id="board_title">Current Job Openings at Charles River Associates</h1>
                    #^NOTE: Ex)'Current Job Openings at Charles River Associates' ssoooo instead do if "Current Job Openings" in h# elements' text value!!!
                self.try_adjusting_this_link(header_link)
                #list_of_other_jobs_keyword = ''
                first_link == False
        
        #! Multithreading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            #future_to_link = {executor.submit(self.check_link, header_link, list_of_other_jobs_keyword): header_link for header_link in links_in_header[:1]}
            future_to_link = {executor.submit(self.check_link, header_link): header_link for header_link in links_in_header[:1]}
            for future in concurrent.futures.as_completed(future_to_link):
                link = future_to_link[future]
                try:
                    result = future.result()
                    if result is not None:
                        self.company_open_positions_link = result
                        return
                except Exception as exc:
                    print(f'{link} generated an exception: {exc}')
        
        if (self.company_open_positions_link == None):
            #TODO: Make this a method
            links_in_header[-1].click()
            time.sleep(3)
            current_url = self.browser.current_url
            result = self.check_link(current_url)
            if result is not None:
                self.company_open_positions_link = result
        return
    
    def process_links(self, possible_links):
        print("\nprocess_links()")
        all_links = []
        for link in possible_links:
            href = link.get('href')
            # Skip if href is None
            if href is None:
                continue
            # Construct the full URL
            job_url = self.construct_url_to_job(self.current_url, href)
            # Adjust the URL if necessary
            adjusted_url = self.try_adjusting_this_link(job_url)
            all_links.append(adjusted_url)
        # Ensure no duplicates
        unique_possible_links = self.remove_duplicates_from_list(all_links)
        # Check if links are internal job openings URL
        link = self.test_links_if_internal_job_openings_URL(unique_possible_links)
        return link if self.test_links_if_internal_job_openings_URL(link) else None
    
    def construct_url_to_job(self, current_url, job_opening_href):
        print("\nconstruct_url_to_job()")
        
        print(f'current_url = {current_url}\njob_opening_href = {job_opening_href}')
        
        button_to_job_description = job_opening_href
        print(f'button_to_job_description = {button_to_job_description}') #True
        # job_link = job_opening_href.get('href')
        job_link = job_opening_href
        print(f'job_link = {job_link}')
        domain_name = self.try_adjusting_this_link(current_url)
        print(f'domain_name = {domain_name}')
        # job_path = job_opening_href.get('href')
        job_path = job_opening_href
        print(f'job_path = {job_path}')
        job_url = domain_name + job_path
        return job_url
    
    #TODO: jobs.lever.co/  <-this is hard coded > so need to change that!!
    def try_adjusting_this_link(self, adjust_this_link):
        print(f"\ntry_adjusting_this_link()")
        print(f" adjust_this_link = {adjust_this_link}")
        if self.application_company_name == 'lever':
            adjusting_link = adjust_this_link.find('jobs.lever.co/') + len('jobs.lever.co/')
            still_adjusting = adjust_this_link.find('/', adjusting_link) + 1
            link_adjusted = adjust_this_link[:still_adjusting]
            adjust_this_link = link_adjusted
        if self.application_company_name == 'greenhouse':
            adjusting_link = adjust_this_link.find('greenhouse.io/') + len('greenhouse.io/')
            still_adjusting = adjust_this_link.find('/', adjusting_link) + 1
            link_adjusted = adjust_this_link[:still_adjusting]
            print(f"    ----> {link_adjusted}")
            adjust_this_link = link_adjusted
        #time.sleep(1)
        print(f"    ----> {adjust_this_link}")
        return adjust_this_link
    
    def test_links_if_internal_job_openings_URL(self, unique_possible_links):
        print("\ncheck_banner_links()")
        # Multithreading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_link = {executor.submit(self.check_if_internal_job_openings_URL, possible_link): possible_link for possible_link in unique_possible_links}
            for future in concurrent.futures.as_completed(future_to_link):
                link = future_to_link[future]
                try:
                    result = future.result()
                    if result is True:
                        return link
                except Exception as exc:
                    print(f'{link} generated an exception: {exc}')
        return None

    def check_if_internal_job_openings_URL(self, possible_link):
        print("\ncheck_link()")
        # Check if the link is the "Internal-Job-Listings" webpage
        if self.determine_current_page(possible_link) == 0:
            return True
        return False
#!==============================================


#!=========== filter list of links =============
    def filter_list_of_links(self):
        print("\nfilter_list_of_links()")
        self.list_of_links = self.remove_duplicates_from_list(self.list_of_links)
        if not self.list_of_links:
            print(" self.list_of_links is empty!")
            return
        self.list_of_links = self.remove_allocated_links()
        self.list_of_links = self.JobSearchWorkflow_instance.filter_out_jobs_user_previously_applied_to(self.list_of_links, self.JobSearchWorkflow_instance.previously_applied_to_job_links)

    def remove_duplicates_from_list(self, list_to_filter):
        print("\n remove_duplicates_from_list()")
        return list(dict.fromkeys(list_to_filter))
    
    def remove_allocated_links(self):
        print("\n remove_allocated_links()")
        if self.companys_internal_job_openings_URL in self.list_of_links:
            self.list_of_links.remove(self.companys_internal_job_openings_URL)
        return self.list_of_links
#!==============================================



#?????????
#*********
#TODO TODO
# Add !!! location_check!!! Make sure countries are equal!!
#!=========== filter by requirements ===========
    #TODO: ?? DELETE ??  I think this might have been how I originally checked experience in the job_title?!?!?!
    def fits_users_criteria(self, test_elements_uniqueness, *args):
        print("\nfits_users_criteria()")
        ultimate_lists_checker = []
        for arg in args:
            ultimate_lists_checker.extend(arg)
        for unacceptable_element in ultimate_lists_checker:
            if unacceptable_element in test_elements_uniqueness:
                return False
        return True



    #! safe_print()
    def users_basic_requirements_job_title(self, job_title):
        print("\nusers_basic_requirements_job_title()")
        print(f"   {self.users_job_search_requirements['user_desired_job_titles']}")
        safe_print(f"              vs.\n   {job_title}\n")
        
        #Split the job_title on common delimiters
        job_title_parts = [part.lower().strip() for part in re.split(r'[\/,;] | or | and ', job_title)]
        safe_print(f"job_title_parts = {job_title_parts}")
        
        for part in job_title_parts:
            # best_match = self.find_the_bestest_match(part.strip())
            # if best_match is not None:
            for desired_job in self.users_job_search_requirements['user_desired_job_titles']:
                if desired_job in part:
                    #print(f"Job PASSED for part: {part}")
                    print(f"{part}")
                    return True
       # print("Job FAILED!!")
        return False
    
    def get_experience_level(self, job_title):
        print("\nget_experience_level()")
        for experience_keyword in self.prior_experience_keywords:
            if experience_keyword in job_title:
                return experience_keyword
    
    
    def check_users_basic_requirements(self, job_title, job_location, job_workplaceType):
        print("\ncheck_users_basic_requirements()")
        
        safe_print(f" self.current_jobs_details = {self.current_jobs_details}\n")
        safe_print(f" job_title = {job_title}\n job_location = {job_location}\n job_workplaceType = {job_workplaceType}\n")
        safe_print(f"self.users_job_search_requirements['entry_level'] = {self.users_job_search_requirements['entry_level']}")
        
        #if self.users_job_search_requirements['entry_level'] == True and self.users_basic_requirements_experience_level(job_title) == False:
        if self.users_job_search_requirements['entry_level'] == False or self.users_basic_requirements_experience_level(job_title) == True:
            return False
        location_and_workplaceType_check_out = self.user_basic_requirements_location_workplaceType(job_location, job_workplaceType)
        if location_and_workplaceType_check_out == True:
            pass
        else:
            return False
        return True

    def users_basic_requirements_experience_level(self, job_title):
        print("users_basic_requirements_experience_level()")
        print(" ", end="")
        # print(any(experience_keyword in job_title for experience_keyword in self.prior_experience_keywords), end="")
        # print("  --  No experience keywords found in the Job Title!")
        # return any(experience_keyword in job_title for experience_keyword in self.prior_experience_keywords)
        # ^ KEEP ALL THIS AND ERASE BELOW WHEN READY!!!!! (Below is only for testing)
        experience_found = any(experience_keyword in job_title for experience_keyword in self.prior_experience_keywords)
        print(" ", end="")
        print(experience_found, end="")
        if experience_found:
            print("  --  Experience keywords found in the Job Title!")
        else:
            print("  --  No experience keywords found in the Job Title!")
        return experience_found

    #TODO: A lot of work boy!!!
    def user_basic_requirements_location_workplaceType(self, job_location, job_workplaceType):
        print("\nuser_basic_requirements_location_workplaceType()")
        # if not job_location or job_location.lower().country() not in self.users_job_search_requirements['user_preferred_locations']:
        #     return False
        # if job_location not in self.users_job_search_requirements['user_preferred_locations']:
        #     return False
        
        
        if self.users_job_search_requirements['user_preferred_locations'] and job_location not in self.users_job_search_requirements['user_preferred_locations']:
            print("       USER has or doesn't something workplaceType...  idk?")
            return False
        
        
        if not job_workplaceType or job_workplaceType.lower() == "unknown":
            print("       workplaceType unknown")
            return False
        if job_workplaceType.lower() == 'in-office with occasional remote':
            if 'in-office' in self.users_job_search_requirements['user_preferred_workplaceType'] or 'remote' in self.users_job_search_requirements['user_preferred_workplaceType']:
                print("       workplaceType  ->  in-office with occasional remote")
                return True
            else:
                return False
        if job_workplaceType.lower() == 'hybrid with rare in-office':
            if 'hybrid' in self.users_job_search_requirements['user_preferred_workplaceType'] or 'remote' in self.users_job_search_requirements['user_preferred_workplaceType']:
                print("       workplaceType  ->  hybrid with rare in-office")
                return True
            else:
                return False
        if job_workplaceType.lower() == 'remote':
            print("       workplaceType  ->  remote")
            return True
        if job_workplaceType.lower() == 'hybrid':
            if 'hybrid' in self.users_job_search_requirements['user_preferred_workplaceType'] and 'in-office' in self.users_job_search_requirements['user_preferred_workplaceType']:
                print("       workplaceType  ->  hybrid")
                return True
            else:
                return False
        if job_workplaceType.lower() == 'in-office':
            if 'in-office' in self.users_job_search_requirements['user_preferred_workplaceType']:
                print("       workplaceType  ->  in-office")
                return True
            else:
                return False
        print("       workplaceType didn't work correctly")
        return False
#!==============================================







    # print(f"------\n {}\n------")
    #TODO: Please get rid of -> (self, job_link) ? 
    def determine_current_page(self, job_link):
        print("\ndetermine_current_page()")
        print(f"       job_link = {job_link}")
        soup = self.apply_beautifulsoup(job_link, "lxml")
        #print(f"------ soup:\n {soup}\n------")
        print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        if self.application_company_name == "lever":
            webpage_body = soup.find('body')
            opening_link_application = soup.find('div', {"class": 'application-page'})
            opening_link_description = soup.find('div', {"class": 'posting-page'})
            opening_link_company_jobs = soup.find('div', {"class": "list-page"})
            if opening_link_application:
                print('-Application Page')
                self.update_soup_elements(soup, webpage_body=webpage_body, opening_link_application=opening_link_application)
                return 2
            elif opening_link_description:
                print("-Job Description Page")
                self.update_soup_elements(soup, webpage_body=webpage_body, opening_link_description=opening_link_description)
                return 1
            elif opening_link_company_jobs:
                print('-Job Listings Page')
                self.update_soup_elements(soup, webpage_body=webpage_body, opening_link_company_jobs=opening_link_company_jobs)
                return 0
            #TODO: elif - check for 'special' job expired webpage!
            #TODO: else - blacklist_this_url(job_link)
            #return self.application_company_name, job_link
            #TODO: ^ ^ ^ Maybe you need to remove that link or something!! Check this out and figure it out!
            else:
                return None
        elif self.application_company_name == "greenhouse":
            div_main = soup.find("div", id="main")
            #print(f"------ div_main:\n {div_main}\n------")
            next_elem = div_main.find_next()
            while next_elem:
                # if next_elem.name == "div" and (next_elem.get("id") == "flash-wrapper" or next_elem.get("id") == "flash_wrapper"):
                if next_elem.name == "div" and next_elem.get("id") in ["flash-wrapper", "flash_wrapper"]:
                    print('-Job Listings Page V.1')
                    return 0
                elif (next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper"):
                    print('-Job Listings Page V.2')
                    return 0
                elif (next_elem.name == "section" and next_elem.get("class") == "level-0"):
                    print('-Company Job Openings Page')
                    print("A while loop for this is perfect for this because there can be multiple <section class='level-0'>")
                    return 0
                elif next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"]:
                    app_body = next_elem
                    header = next_elem.find("div", id="header")
                    content = next_elem.find("div", id="content")
                    if header and content:
                        print("-Job Description Page")
                        self.update_soup_elements(soup, div_main=div_main, app_body=app_body, header=header, content=content)
                        return 1
                    break
                else:
                    next_elem = next_elem.find_next()
            #return self.application_company_name, job_link
            #TODO: ^ ^ ^ Maybe you need to remove that link or something!! Check this out and figure it out!
            return None
        print("\t -The Plymouth Conjecture!")
        return None
    
    #!=========== Internal-Job-Listings ============
    def check_companies_other_job_openings(self, link):
        print("\ncheck_companies_other_job_openings()")
        #TODO: change webpage --> self.companys_internal_job_openings_URL
         #??? What if already on this page??? Like what if it is the initial link!?!?!?
        if self.browser.current_url != self.companys_internal_job_openings_URL:
            self.change_page(self.companys_internal_job_openings_URL)
        self.soup_elements['soup'] = self.apply_beautifulsoup(self.current_url, "lxml")
        list_of_job_urls = self.collect_companies_current_job_openings(self.soup_elements['soup'])
        
        print(f"Internal-Job-Listings\n   BRAND NEW list_of_job_urls = {list_of_job_urls}\n")
        print(f"Internal-Job-Listings\n   ORIGINAL self.list_of_links = {self.list_of_links}\n")
        self.print_matching_job_details(list_of_job_urls)
        
        self.update_list_of_links(list_of_job_urls)
        self.filter_list_of_links()
        
        print(f"\nInternal-Job-Listings\n   NEW self.list_of_links = {self.list_of_links}\n")
        self.print_current_jobs_details()
        
        self.change_page(link)
    
    def get_absolute_url(self, url1, url2):
        print("\nget_absolute_url()")
        parsed_url1 = urlparse(url1)
        parsed_url2 = urlparse(url2)

        # Check if url1 is absolute (has a scheme like "http" or "https")
        if parsed_url1.scheme:
            base_url = f"{parsed_url1.scheme}://{parsed_url1.netloc}/"
            absolute_url2 = urljoin(base_url, url2)
            return url1, absolute_url2
        # Check if url2 is absolute
        elif parsed_url2.scheme:
            base_url = f"{parsed_url2.scheme}://{parsed_url2.netloc}/"
            absolute_url1 = urljoin(base_url, url1)
            return absolute_url1, url2
        else:
            raise ValueError("At least one URL must be absolute")
    
    #! safe_print()
    def print_current_jobs_details(self):
        print("\nprint_current_jobs_details()")
        for key, value in self.current_jobs_details.items():
            safe_print(f"{key}: {value}")
    
    #! safe_print()
    def print_matching_job_details(self, list_of_job_urls):
        print("\nprint_matching_job_details()")
        for url in list_of_job_urls:
            # Check if the URL exists in self.current_jobs_details
            if url == self.current_jobs_details.get("job_url"):
                print("**" + url + "**\n") # Print the matching URL
                # Print all the key-value pairs in the dictionary
                for key, value in self.current_jobs_details.items():
                    safe_print(f"{key}: {value}")
                print("\n") # Print a newline for separation
    
    #NOTE: Maybe you can do a while loop as confirmation and setting variables!! Like in job_description_webpage_navigation()
    #NOTE: OR...  or 2 methods with whiles where the 1st methods' while checks and confirms variables and the 2nd methods' while sets variables if present -> exactly like in job_description_webpage_navigation()!!! (The 2nd method can utilize the next_elem thing!?)
    #! GET RID OF ALL --- filter by requirements --- {except for get_experience_level()}
    #? JK JK  "if self.users_basic_requirements_job_title(job_title) == False:" just checks if job_title matches users_job_title!! {This checks and confirms user should not add 'accountant' job details to current_jobs_details!!!}
        #! THIS METHOD IS ALL ABOUT COLLECTING ALL MATCHING job_title STRINGS !!REGARDLESS!! OF EXPERIENCE!!!!
        #! CHECK ALL THAT STUFF AFTER THIS METHOD -> IF THEY FIT ADD current_jobs_details TO  
            #! total_company_jobs_available  <= add all 
            #! possibly_qualified_for_jobs   <= 
            #! jobs_applied_to_this_session  <= submitted application
    #! safe_print()
    def collect_companies_current_job_openings(self, soup):
        # print("\ncollect_companies_current_job_openings()")
        print("\n*")
        print("* *")
        print("* * *")
        print("* * * *")
        print("* * * * *")
        print("collect_companies_current_job_openings()")
        current_url = self.browser.current_url
        list_of_job_urls = []
        if self.application_company_name == 'lever':
            self.soup_elements["postings_wrapper"] = soup.find('div', class_="postings-wrapper")
            self.soup_elements["postings_groups"] = self.soup_elements["postings_wrapper"].find_all('div', class_="postings-group")
            for postings_group in self.soup_elements["postings_groups"]:
                print(":-----------------------------------------------------------------------")
                # Extracting large-category-header if present
                #TODO - company_department[Design]
                department = postings_group.find('div', class_="large-category-header")
                if department:
                    print(f"Large Category Header:{department.text}")
                # Extracting posting-category-title if present
                #TODO - company_department[App-Design]
                specialization = postings_group.find('div', class_="posting-category-title large-category-label")
                if specialization:
                    print(f"Posting Category Title:{specialization.text}")

                # Extracting all posting elements
                postings = postings_group.find_all('div', class_="posting")
                for posting in postings:
                    print(":-----------------------------------------------------------------------")
                    # Confirming the 'Apply' button
                    #TODO: Pick one!
                    # job_opening_href = apply_button
                    apply_button = posting.find('a', text='Apply')
                    if apply_button:
                        print(f"Apply Button URL: {apply_button['href']}")

                    # Finding the title button and extracting job title
                    #TODO: Pick one!
                    # button_to_job_description = title_button
                    title_button = posting.find('a', class_="posting-title")
                    if title_button:
                        job_title = title_button.find('h5', {'data-qa': 'posting-name'}).get_text().strip()
                        if self.users_basic_requirements_job_title(job_title) == False:
                            print("          Job FAILED!!")
                            continue
                        print("          Job PASSED!!")
                        experience_level = self.get_experience_level(job_title)
                            
                    #TODO:-----------------------------------------------------------------------
                    #Error Handling: Confirm apply_button and title_button links are = !!!
                    apply_href = apply_button['href']
                    title_href = title_button['href']
                    
                    absolute_apply_href, absolute_title_href = self.get_absolute_url(apply_href, title_href)
                    
                    if absolute_apply_href == absolute_title_href:
                        job_url = absolute_apply_href
                    else:
                        job_url = absolute_apply_href
                    #TODO:-----------------------------------------------------------------------    

                    # Extracting other details
                    posting_categories = posting.find('div', class_="posting-categories")
                    if posting_categories:
                        job_location = posting_categories.find('span', class_='location').get_text().strip() if posting_categories.find('span', class_='location') else None
                        company_department = posting_categories.find('span', class_='department').get_text().strip() if posting_categories.find('span', class_='department') else None
                        employment_type = posting_categories.find('span', class_='commitment').get_text().strip() if posting_categories.find('span', class_='commitment') else None
                        job_workplaceType = posting_categories.find('span', class_='workplaceTypes').get_text().strip() if posting_categories.find('span', class_='workplaceTypes') else None

                    
                    #***
                    self.print_job_details(job_url, job_title, job_location, company_department, employment_type, job_workplaceType, experience_level)
                    #***
                    
                    
                    #if self.check_users_basic_requirements(job_title, job_location, job_workplaceType):
                    michaels_secret_stuff = self.check_users_basic_requirements(job_title, job_location, job_workplaceType)
                    if michaels_secret_stuff == True:
                        #TODO: company_name
                            #! ^  ^  ^  ^ b/c I organize links in JobSearchWorkflow.py that variable only needs to be set once!!!
                        self.current_jobs_details.update({
                            'job_url': job_url,
                            'job_title': job_title,
                            'job_location': job_location,
                            'job_workplaceType': job_workplaceType,
                            'company_department': company_department,
                            'employment_type': employment_type,
                            'experience_level': experience_level
                        })
                        print("STEP 1:")
                        print(f"experience_level = {experience_level}")
                        print(f"if not experience = ", end="")
                        print(not experience_level)
                        if not experience_level:
                            
                            
                            #! HERE TESTING HERE TESTING HERE TESTING HERE TESTING
                            print("\nSTEP 2:")
                            print("\nv v v v v v v v v v v v v v v v v v v ")
                            print(f"self.current_jobs_details = {self.current_jobs_details}")
                            print(f"job_url = {job_url}")
                            print(f"list_of_job_urls = {list_of_job_urls}")
                            
                            list_of_job_urls.append(job_url)
                            
                            print(f"list_of_job_urls = {list_of_job_urls}")
                            print("^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^")
                    
                    print("\nSTEP 3:")    
                    # v was here
                    self.print_companies_internal_job_opening("company_job_openings", self.application_company_name, JobTitle=job_title, JobLocation=job_location, WorkPlaceTypes=job_workplaceType, CompanyDepartment=company_department, JobTeamInCompany=specialization, JobHREF=job_url, ButtonToJob=apply_href)
                    print("::----------------------------------------------------------------------")
        elif self.application_company_name == 'greenhouse':
        #         div_main = soup.find("div", id="main")
        #         # Find all heading elements
        #         headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        #         # Sort headings by their level, starting with the highest
        #         sorted_headings = sorted(headings, key=lambda x: int(x.name[1]), reverse=True)
        #         print(":-----------------------------------------------------------------------")
        #         # Traverse through sorted headings and find the one without a parent 'section' element
        #         for heading in sorted_headings:
        #             if heading.find_parent('section') is None:
        #                 company_department = heading.text.strip()
        #                 print(f"company_department = {company_department}")
                        
        #         # Find sections containing company departments and job openings
        #         sections = div_main.find_all('section', class_=lambda x: x and 'level' in x)
        #         for section in sections:
        #             job_openings = section.find_all('div', {'class': 'opening'})
        #             number_of_elements = len(job_openings)
        #             print("Number of elements with class 'opening':", number_of_elements)
        #             for job_opening in job_openings:
        #                 print(":-----------------------------------------------------------------------")
        #                 job_opening_href = job_opening.find('a')
        #                 if job_opening_href:
        #                     job_title = job_opening_href.text
        #                     if self.users_basic_requirements_job_title(job_title) == False:
        #                         print("          Job FAILED!!")
        #                         continue
        #                     print("          Job PASSED!!")
        #                     experience_level = self.get_experience_level(job_title)
        #                     job_url = self.alter_url_to_job(current_url, job_opening_href)
        #                     span_tag_location = job_opening.find('span', {'class', 'location'})
        #                     job_location = span_tag_location.text if span_tag_location else None
                            
        #                     employment_type = "Testing Tests"
                            
        #                     self.print_job_details(job_url, job_title, job_location, company_department, employment_type, job_workplaceType, experience_level)
                            
        #                     if self.check_users_basic_requirements(job_title, job_location, job_workplaceType):
        #                         self.current_jobs_details.update({
        #                             'job_url': job_url,
        #                             'job_title': job_title,
        #                             'experience_level': experience_level,
        #                             'job_location': job_location,
        #                             'job_workplaceType': job_workplaceType,
        #                             'company_department': company_department,
        #                             'employment_type': employment_type
        #                         })
        #                         if experience_level == None:
        #                             print(f"This link {job_url} has been added to list_of_job_urls!")
        #                             list_of_job_urls.append(job_url)
        #                     self.print_companies_internal_job_opening("company_job_openings", self.application_company_name, JobTitle=job_title, JobLocation=job_location, ButtonToJob=job_opening_href)
        #                     print(":-----------------------------------------------------------------------")
        # print("* * * * *")
        # print("* * * *")
        # print("* * *")
        # print("* *")
        # print("*\n\n")
        # return list_of_job_urls
        
        # ----------------------------------------------------------------------------------------------------------------------------------------------
        
        # if self.application_company_name == 'greenhouse':
        #     # Find the main content div
        #     div_main = soup.find("div", id="main")
        #     # Find the section containing "Current Job Openings" or similar text
        #     job_openings_section = div_main.find(string=re.compile("Current Job Openings", re.IGNORECASE)).find_parent('section')
        #     # Find all headings within the job openings section
        #     headings = job_openings_section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        #     # Initialize company_department variable
        #     company_department = None
        #     # Iterate through headings and divs with class 'opening' to extract job details
        #     for element in job_openings_section.children:
        #         if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        #             company_department = element.text.strip()
        #             print(f"company_department = {company_department}")
        #         elif element.name == 'div' and 'opening' in element.get('class', []):
        #             job_opening_href = element.find('a')
        #             if job_opening_href:
        #                 job_title = job_opening_href.text
        #                 if self.users_basic_requirements_job_title(job_title) == False:
        #                     print("          Job FAILED!!")
        #                     continue
        #                 print("          Job PASSED!!")
        #                 experience_level = self.get_experience_level(job_title)
        #                 job_url = self.alter_url_to_job(current_url, job_opening_href)
        #                 span_tag_location = element.find('span', {'class', 'location'})
        #                 job_location = span_tag_location.text if span_tag_location else None
                        
        #                 employment_type = "Testing Tests" # Adjust as needed
                        
        #                 self.print_job_details(job_url, job_title, job_location, company_department, employment_type, None, experience_level)
                        
        #                 if self.check_users_basic_requirements(job_title, job_location, None):
        #                     self.current_jobs_details.update({
        #                         'job_url': job_url,
        #                         'job_title': job_title,
        #                         'experience_level': experience_level,
        #                         'job_location': job_location,
        #                         'job_workplaceType': None,
        #                         'company_department': company_department,
        #                         'employment_type': employment_type
        #                     })
        #                     if experience_level == None:
        #                         print(f"This link {job_url} has been added to list_of_job_urls!")
        #                         list_of_job_urls.append(job_url)
        #                 self.print_companies_internal_job_opening("company_job_openings", self.application_company_name, JobTitle=job_title, JobLocation=job_location, ButtonToJob=job_opening_href)
        #                 print(":-----------------------------------------------------------------------")
        # print("* * * * *")
        # print("* * * *")
        # print("* * *")
        # print("* *")
        # print("*\n\n")
        # return list_of_job_urls
        
        # ----------------------------------------------------------------------------------------------------------------------------------------------
        
            # Find the main div containing job details
            div_main = soup.find("div", id="main")
            
            
            # NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW
            if div_main is not None:
                sections = div_main.find_all('section', class_=lambda x: x and 'level' in x)
            else:
                print("div_main not found")
                sections = []
            # NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW
            
            
            # Find all heading elements
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            #NOTE: ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL
            # # Sort headings by their level, starting with the highest
            # sorted_headings = sorted(headings, key=lambda x: int(x.name[1]), reverse=True)
            
            # # Traverse through sorted headings and find the one without a parent 'section' element
            # for heading in sorted_headings:
            #     if heading.find_parent('section') is None:
            #         company_department = heading.text.strip()
            #         break
            #NOTE: ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL ORIGINAL
            
            #NEW NEW NEW NEW NEW
            # # Traverse through headings and find the one with an id consisting only of numbers
            # for heading in headings:
            #     heading_id = heading.get('id')
            #     if heading_id and heading_id.isdigit():
            #         # Check if there are sibling or child elements with a department_id attribute containing the same number
            #         siblings_with_department_id = heading.find_next_siblings(attrs={'department_id': heading_id})
            #         children_with_department_id = heading.find_all(attrs={'department_id': heading_id})
            #         if siblings_with_department_id or children_with_department_id:
            #             company_department = heading.text.strip()
            #             break
                    
            # Find sections containing company departments and job openings
            #TODO: OG sections = div_main.find_all('section', class_=lambda x: x and 'level' in x)
            for section in sections:
                job_openings = section.find_all('div', {'class': 'opening'})
                for job_opening in job_openings:
                    print(":-----------------------------------------------------------------------")
                    job_opening_href = job_opening.find('a')
                    if job_opening_href:
                        job_title = job_opening_href.text
                        if self.users_basic_requirements_job_title(job_title) == False:
                            print("          Job FAILED!!")
                            print(":-----------------------------------------------------------------------")
                            continue
                        print("          Job PASSED!!")
                        experience_level = self.get_experience_level(job_title)
                        
                        
                        
                        
                        
                        
                        
                        #NEW NEW NEW NEW NEW
                        # for heading in headings:
                        #     heading_id = heading.get('id')
                        #     if heading_id and heading_id.isdigit():
                        #         # Check if there are sibling or child elements with a department_id attribute containing the same number
                        #         siblings_with_department_id = heading.find_next_siblings(attrs={'department_id': heading_id})
                        #         children_with_department_id = heading.find_all(attrs={'department_id': heading_id})
                        #         if siblings_with_department_id or children_with_department_id:
                        #             company_department = heading.text.strip()
                        #             break
                        department_ids = job_opening.get('department_id', '').split(',')
                        company_department = None

                        for dept_id in department_ids:
                            for heading in headings:
                                if heading.get('id') == dept_id and heading.text.strip():
                                    company_department = heading.text.strip()
                                    break  # Break the loop once the first non-empty heading is found
                            if company_department:
                                break  # Break the outer loop if company_department is set
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        job_url = job_opening_href.get('href')
                        # span_tag_location = job_opening.find('span', {'class', 'location'})
                        # job_location = span_tag_location.text if span_tag_location else None
                        # if not job_location:
                        #     span_tag_location = job_opening.find('div', {'class', 'location'})
                        #     job_location = span_tag_location.text if span_tag_location else None
                        for tag_name, class_name in [('span', 'location'), ('div', 'location')]:
                            tag_location = job_opening.find(tag_name, {'class': class_name})
                            if tag_location:
                                job_location = tag_location.text
                                break
                            
                        job_workplaceType = self.current_jobs_details.get('job_workplaceType', 'full-time')
                        
                        # Print or store the details as required
                        print("\n")
                        safe_print(f"Job Title: {job_title}")
                        safe_print(f"Job URL: {job_url}")
                        safe_print(f"Job Location: {job_location}")
                        safe_print(f"Company Department: {company_department}")
                        print(":-----------------------------------------------------------------------")
                        
                    if self.check_users_basic_requirements(job_title, job_location, job_workplaceType):
                        self.current_jobs_details.update({
                            'job_url': job_url,
                            'job_title': job_title,
                            'job_location': job_location,
                            'job_workplaceType': job_workplaceType,
                            'company_department': company_department,
                            'employment_type': employment_type,
                            'experience_level': experience_level
                        })
                        print("STEP 1:")
                        print(f"experience_level = {experience_level}")
                        print(f"if not experience = ", end="")
                        print(not experience_level)
                        if not experience_level:
                        
                        
                            #! HERE TESTING HERE TESTING HERE TESTING HERE TESTING
                            print("STEP 2:")
                            print("\nv v v v v v v v v v v v v v v v v v v")
                            safe_print(f"self.current_jobs_details = {self.current_jobs_details}")
                            safe_print(f"job_url = {job_url}")
                            safe_print(f"list_of_job_urls = {list_of_job_urls}")
                            
                            list_of_job_urls.append(job_url)
                            
                            print(f"list_of_job_urls = {list_of_job_urls}")
                            print("^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^")
                
                    print("\nSTEP 3:")   
                # v was here
                    self.print_companies_internal_job_opening("company_job_openings", self.application_company_name, JobTitle=job_title, JobLocation=job_location, WorkPlaceTypes=job_workplaceType, CompanyDepartment=company_department, JobHREF=job_url)
                    print("::----------------------------------------------------------------------")
                        
                        
        print("* * * * *")
        print("* * * *")
        print("* * *")
        print("* *")
        print("*\n\n")
        return list_of_job_urls

    
    #! safe_print()
    def print_job_details(self, job_url, job_title, job_location, company_department, employment_type, job_workplaceType, experience_level=None):
        print("\nprint_job_details()")
        print("       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        safe_print(f"       Job URL:{job_url}")
        safe_print(f"       Job Title:{job_title}")
        safe_print(f"       Job Location:{job_location}")
        safe_print(f"       Company Department:{company_department}")
        safe_print(f"       Employment Type:{employment_type}")
        safe_print(f"       Job Workplace Type:{job_workplaceType}")
        if experience_level is not None:
            print(f"       Experience Level:{experience_level}")
        print("       <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("\n") # Print a newline for separation

    
    
    

    #TODO: def print_companys_internal_job_opening(self, *args, **kwargs):
    #NOTE: I think this is only supposed to print 1 job at a time!! (??The **kwargs is inside the *args and the *args is A SINGLE jobs' details??)
    #! safe_print()
    def print_companies_internal_job_opening(self, *args, **kwargs):
        print('----------------------------------------------------------------------------------------------------')
        print("print_company_job_openings()")
        method_name = None
        for arg in args:
            if arg == 'greenhouse':
                print(method_name)
                print(arg)
                for key, value in kwargs.items():
                    safe_print(key + ": " + str(value))
            elif arg == 'lever':
                print(method_name)
                print(arg)
                for key, value in kwargs.items():
                    safe_print(key + ": " + str(value))
            else:
                method_name = arg
        print('----------------------------------------------------------------------------------------------------')
        print('\n\n\n')
    #!==============================================
    
    #!============= Job-Description ================
    #! safe_print
    def analyze_job_suitabililty(self):
        #print("\n    ---- Job-Description ----    \n")
        print("\nanalyze_job_suitabililty()")
        #This part is about collecting info
        self.current_jobs_details["job_url"] = self.current_url
        
        if self.application_company_name == "lever":
            parser = 'lxml'
        elif self.application_company_name == "greenhouse":
            parser = 'html'
        
        self.fetch_and_fill_variables(self.job_application_webpage[1], parser)
        self.job_description_webpage_navigation()
        
        
        
        #This part determines if user is fit for the job
        #user_fits_jobs_criteria = self.should_user_apply(self.soup_elements['opening_link_description'])
        user_fits_jobs_criteria = self.should_user_apply(self.soup_elements['content'])
        safe_print(f"content = \n{self.soup_elements['content'].get_text()}")
        #job_fits_users_criteria = self.fits_users_criteria()
        
        #????????????????????????????????????????????????????????????????????????????????????????
        # Get the value of 'job_workplaceType' from the dictionary, and if it's not found, use 'in-office' as the default value
        job_workplaceType = self.current_jobs_details.get('job_workplaceType', 'in-office')
        
        # job_fits_users_criteria = self.check_users_basic_requirements(self.current_jobs_details['job_title'], self.current_jobs_details['job_location'], self.current_jobs_details['job_workplaceType'])
        job_fits_users_criteria = self.check_users_basic_requirements(self.current_jobs_details['job_title'], self.current_jobs_details['job_location'], job_workplaceType)
        #print(f"  user_fits_jobs_criteria = {user_fits_jobs_criteria}\n  job_fits_users_criteria = {job_fits_users_criteria}")
        if user_fits_jobs_criteria and job_fits_users_criteria:
            print("\tUser is applying to this job!!    <-----------------------")
            #TODO: Refactor this  v  by making a method called ?transfer_webpages() => {self.bottom_has_application_or_button() | self.click_this_button_or_scroll() | self.change_webpage()}?
            self.bottom_has_application_or_button(self.application_company_name)
            return 2
        else:
            print("\tUser is NOT going to apply to this job!!")
            if user_fits_jobs_criteria == False and job_fits_users_criteria == False:
                print(f"\t user_fits_jobs_criteria = {user_fits_jobs_criteria}\n\t job_fits_users_criteria = {job_fits_users_criteria}")
            else:
                if user_fits_jobs_criteria == False:
                    print(f"\t user_fits_jobs_criteria = {user_fits_jobs_criteria}")
                if job_fits_users_criteria == False:
                    print(f"\t job_fits_users_criteria = {job_fits_users_criteria}")
            #print("\tHmmm that's weird ? it's neither button nor application")
            return 1


    def should_user_apply(self, job_description):
        everything_about_job = job_description.get_text()
        #TODO: ADD SpaCy coding-formatting here!!!
        experience_needed = "You must be a diety! Being a demigod or demigoddess is literally embarrassing... just go back to coloring if this is you. Literally useless & pathetic ewww"
        if re.search(experience_needed, everything_about_job):
            return False
        else:
            return True
    
    #TODO: call self.click_this_button(button)
    #NOTE: ^  ^  ^ Maybe rename to  self.click_this_button_or_scroll() {Better encapsulates all scenarios here}
    def bottom_has_application_or_button(self, application_company_name):
        soup = self.apply_beautifulsoup(self.browser.current_url, "html")
        if application_company_name == "lever":
            a_tag_butt = soup.find('a', {'data-qa': ['btn-apply-bottom', 'show-page-apply']})
            div_tag_butt = soup.find('div', {'data-qa': 'btn-apply-bottom'})
            application_at_bottom = soup.find("div", id="application")
            if a_tag_butt:
                xpath_selector = f"//a[@data-qa='{a_tag_butt['data-qa']}']"
                apply_button = self.browser.find_element(By.XPATH, xpath_selector)
                self.scroll_to_element(apply_button)
                apply_button.click()
                time.sleep(2)
            elif div_tag_butt:
                apply_button = self.browser.find_element(By.XPATH, f"//div[@data-qa='{a_tag_butt['data-qa'][0]}']")
                self.scroll_to_element(apply_button)
                apply_button.click()
                time.sleep(3)
            elif application_at_bottom:
                self.scroll_to_element(application_at_bottom)
            return
        elif application_company_name == "greenhouse":
            application = soup.find("div", id="application")
            apply_button_list = None
            try:
                apply_button_list = self.browser.find_element(By.XPATH, "//button[text()='Apply Here' or text()='Apply Now' or text()='Apply for this job']")
            except NoSuchElementException:
                pass
            if application:
                self.scroll_to_element(application)
                time.sleep(1)
            elif apply_button_list:
                apply_button = apply_button_list
                self.scroll_to_element(apply_button)
                apply_button.click()
                time.sleep(3)
            return
    #!==============================================
    
    #!============= Job-Application ================
    def apply_to_job(self):
        print("\napply_to_job()")
        time.sleep(3)
        current_url = self.browser.current_url
        if self.application_company_name == "lever":
            self.reset_webpages_soup_elements()
        self.soup_elements['soup'] = self.apply_beautifulsoup(current_url, "html")
        self.form_input_details = self.get_form_input_details(current_url)
        self.insert_resume()
        self.process_form_inputs(self.form_input_details)
        return 3
    #!==============================================
    
    #!=========== Submitted-Application ============
    #TODO: Figure out what needs to be returned here!?!?!?
    #TODO: add variable => self.soup_elements
    def confirmation_webpage_proves_application_submitted(self):
        print("\nconfirmation_webpage_proves_application_submitted()")
        self.current_url = self.browser.current_url
        if self.application_company_name == "lever":            
            #Check if the string "Application submitted!" is present
            soup = self.apply_beautifulsoup(self.current_url, 'html')  # or 'lxml', depending on your preference
            if 'Application submitted!' in soup.text:
                print("Text 'Application submitted!' is present.")
            else:
                print("Text 'Application submitted!' is not present.")
            
            #Check if body element's class attribute has a 'thanks' value
            if body := soup.find('body', class_='thanks'):
                print("Body element with class 'thanks' is present.")
            else:
                print("Body element with class 'thanks' is not present.")
            
            #Check that the value 'thanks' is at the end of the URL
            if self.current_url.endswith('thanks'):
                print("URL ends with 'thanks'.")
            else:
                print("URL does not end with 'thanks'.")
        elif self.application_company_name == "greenhouse":
            #Check if the string "Thank you for applying." is present
            soup = self.apply_beautifulsoup(self.current_url, 'html')  # or 'lxml', depending on your preference
            if 'Thank you for applying.' in soup.text:
                print("Text 'Thank you for applying.' is present.")
            else:
                print("Text 'Thank you for applying.' is not present.")
                        
            #Check if div element's id attribute has a 'application_confirmation' value
            if div := soup.find('div', id='application_confirmation'):
                print("div element with id 'application_confirmation' is present.")
            else:
                print("div element with id 'application_confirmation' is not present.")
            
            #Check that the value 'thanks' is at the end of the URL
            if self.current_url.endswith('confirmation'):
                print("URL ends with 'confirmation'.")
            else:
                print("URL does not end with 'confirmation'.")
    #!==============================================
    

    
    
    
    #print("\n()")
    
    # ':=' (walrus operator)
    # if body := soup.find('body', class_='thanks'):
    
    #"Internal-Job-Listings", "Job-Description", "Job-Application", "Submitted-Application"
    
    #TODO: Confirm this & maybe just get these with soup?!?!?!
    # "greenhouse" = soup.find("div", id="main")
    #   "lever"    = soup.find('body')
    #TODO:              ^ body doesn't need attrName-attrVal in JSON plus we ONLY NEED the 1st OCCURANCE!!!
    #NOTE: "lever" -> logo element = <a>{aka: button too} + <a href=''> + logo{duhh}
    
    
    
    def fetch_and_fill_variables(self, job_application_webpage, parser):
        print(f"\nfetch_and_fill_variables()")
        self.soup_elements['soup'] = self.apply_beautifulsoup(self.current_url, parser)
        self.process_webpage(job_application_webpage, self.soup_elements['soup'])
        self.print_soup_elements(job_application_webpage)
    
    #! safe_print()    
    def print_soup_elements(self, job_application_webpage):
        print("\nprint_soup_elements()")
        print(f" >>>   self.application_company_name:  {self.application_company_name}")
        print(f" >>>   job_application_webpage:        {job_application_webpage}")
        print("\n    soup_elements = {")
        for index, (key, value) in enumerate(self.soup_elements.items()):
            if index == 0:
                print(f"        soup: soupValue,\n")
                continue
            print(f"\n% % % % % % % % % % % % % % %             < < < < < < < < < < < <")
            safe_print(f"        {key}: {value},\n")
        print("    }")
    
    
    #Welcome to the Holy Land my child... we've been waiting for you
    #!======= Blueprints to Navigate Webpage =======
    #*These 3 methods deal with getting the json file stuff!!
    def get_website_data(self):
        # with open(self.website_elements_relative_path) as websites_data_json_file:
        with open(self.website_elements_relative_path, encoding='utf-8') as websites_data_json_file:
            data = json.load(websites_data_json_file)
            self.website_data = data.get(self.application_company_name, None)
            return

    def get_webpage_data(self, job_application_webpage):
        return self.website_data.get(job_application_webpage, None)
    
    '''
    def process_webpage(self, job_application_webpage, soup):
        if not self.website_data:
            self.get_website_data()
        page_info = self.get_webpage_data(job_application_webpage)

        # Process each element defined in the page info.
        for element_name, element_infos in page_info["elements"].items():
            for element_info in element_infos:
                attr_name = element_info.get("attr")
                attr_value = element_info.get("value")
                if attr_name and attr_value:
                    element = soup.find(element_info["tag"], **{attr_name: attr_value})
                else:
                    element = soup.find(element_info["tag"])
                
                if element:
                    self.update_soup_elements(soup, **{element_name: element})
                    break

        #return self.soup_elements.get('content')
        return
    '''
    
    def process_webpage(self, job_application_webpage, soup):
        print("\nprocess_webpage()")
        if not self.website_data:
            self.get_website_data()
        page_info = self.get_webpage_data(job_application_webpage)

        # Define relationships based on page_info
        relationships = self.build_relationships(page_info)

        # Extract elements based on relationships
        extracted_elements = self.extract_elements(soup, relationships)

        # Update soup elements
        self.update_extracted_soup_elements(extracted_elements)

        return
    
    #print("\n()")
    def build_relationships(self, page_info):
        print("\nbuild_relationships()")
        relationships = {}
        for element_name, element_infos in page_info["elements"].items():
            for element_info in element_infos:
                relationships[element_name] = {
                    'tag': element_info.get("tag"),
                    'class': element_info.get("class"),
                    'id': element_info.get("id"),
                    'text': element_info.get("text"),   # NEW
                    'data_attr': element_info.get("data_attr"),
                    'starts_with': element_info.get("starts_with"),
                    'ends_with': element_info.get("ends_with"),
                    'not_equal': element_info.get("not_equal"),
                    'contains_text': element_info.get("contains_text"),
                    'attribute_exists': element_info.get("attribute_exists"),
                    'relationship': element_info.get("relationship")
                }
        #print(f"{relationships}")
        print("*******************************************************\n\n")
        return relationships
    
    #Used shell thinking here as 'regex type thing'
    #NOTE:  "metacharacters"
    #! safe_print()
    def extract_elements(self, soup, relationships):
        print("\nextract_elements()")
        elements = {}
        for element_name, relationship in relationships.items():
            query = {}
            if relationship['tag']:
                query['name'] = relationship['tag']
            if relationship['class']:
                query['class_'] = relationship['class']
            if relationship['id']:
                query['id'] = relationship['id']
            
            # NEW
            if relationship['text']:
                #query['string'] = relationship['text']
                # FIGURING THIS OUT WAS THE MOST UNHOLY MISSION PEOPLE BETTER RECOGNIZE
                #vein of my existence; <- I meant to say that but forgot but straight super hero status!
                query['string'] = re.compile(r'\s*' + re.escape(relationship['text']) + r'\s*')
            
            if relationship['data_attr']:
                query['data-*'] = relationship['data_attr']
            if relationship['starts_with']:
                query['*^'] = relationship['starts_with']
            if relationship['ends_with']:
                query['*$'] = relationship['ends_with']
            if relationship['not_equal']:
                query['*!='] = relationship['not_equal']
            if relationship['contains_text']:
                query['*~'] = relationship['contains_text']
            if relationship['attribute_exists']:
                query['*'] = relationship['attribute_exists']

            element = soup.find(**query)
            # NEW
            safe_print(f"Query for {element_name}: {query}")
            safe_print(f"Result for {element_name}: {element}\n")

            if relationship['relationship'] == 'children':
                elements[element_name] = element.findChildren()
            elif relationship['relationship'] == 'ancestors':
                elements[element_name] = element.findParents()
            elif relationship['relationship'] == 'following_siblings':
                elements[element_name] = element.findNextSiblings()
            elif relationship['relationship'] == 'preceding_siblings':
                elements[element_name] = element.findPreviousSiblings()
            else:
                elements[element_name] = element

        safe_print(f"{elements}")
        print("*******************************************************\n\n")
        return elements
    
    def update_extracted_soup_elements(self, extracted_elements):
        print("\nupdate_extracted_soup_elements()")
        for key, element in extracted_elements.items():
            self.soup_elements[key] = element
        #print(f"{self.soup_elements}")
        print("*******************************************************\n\n")
    #********************************************************


    #NOTE: REMEMBER!!!! This part is basically {just get links} and basic information about the job!!!
    #TODO: FIX THIS ABSOLUTE MESS!  Good Lord Janice...
    def job_description_webpage_navigation(self):
        print("\njob_description_webpage_navigation()")
        print("Welcome fair maiden!")
        if self.application_company_name == "lever":
            next_elem = self.soup_elements['banner_job_info'].find_next()
            while next_elem:
                # .strip("/ \\") = remove leading and trailing slashes, backslashes, and spaces from the text
                # .strip() = remove leading and trailing whitespace (including spaces, tabs, and newline characters) from the text
                if next_elem.name == "h2" and (job_title := next_elem.get_text().strip("/ \\").strip()):
                    self.current_jobs_details["job_title"] = job_title
                if next_elem.name == "div" and "location" in next_elem.get("class", []) and (job_location := next_elem.get_text().strip("/ \\").strip()):
                    self.current_jobs_details["job_location"] = job_location
                if next_elem.name == "div" and "department" in next_elem.get("class", []) and (company_department := next_elem.get_text().strip("/ \\").strip()):
                    self.current_jobs_details["company_department"] = company_department
                if next_elem.name == "div" and "commitment" in next_elem.get("class", []) and (employment_type := next_elem.get_text().strip("/ \\").strip()):
                    self.current_jobs_details["employment_type"] = employment_type
                if next_elem.name == "div" and "workplaceTypes" in next_elem.get("class", []) and (job_workplaceType := next_elem.get_text().strip("/ \\").strip()):
                    self.current_jobs_details["job_workplaceType"] = job_workplaceType
                next_elem = next_elem.find_next()
        elif self.application_company_name == "greenhouse":
            next_elem = self.soup_elements['div_main'].find_next()
            while next_elem:
                #next_elem = next_elem.find_next()
                #This if statement should test the identifiable/unique element that represents that we are in fact on the "Job-Description" page!!
                  #Ex. For "greenhouse" that would be - (next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"])
                #!!! This is literally the purpose determine_current_page() !!!
                #TODO: ^ ^ ^ Look into this father...
                if self.application_company_name == "greenhouse" and self.soup_elements["app_body"]:
                    if 'header' in self.soup_elements and 'content' in self.soup_elements:
                          header = self.soup_elements['header']
                          content = self.soup_elements['content']

                          if job_title_elem := header.find("h1", class_="app-title").get_text().strip("/ \\").strip():
                              self.current_jobs_details["job_title"] = job_title_elem
                          # Extract company name
                          if company_name_elem := header.find("span", class_="company-name").get_text().strip("/ \\").strip():
                              self.current_jobs_details["company_name"] = company_name_elem
                          # Extract job location
                          if job_location_elem := header.find("div", class_="location").get_text().strip("/ \\").strip():
                              self.current_jobs_details["job_location"] = job_location_elem
                    else:
                        print("Guess the .greenhouse_io_start_page_detector() while loop doesn't work")
                next_elem = next_elem.find_next()
        return
    #!==============================================
    






    #TODO:
    # {
    # "greenhouse": {
    #     "Internal-Job-Listings": {
    #         "elements": {
    #             "content": [
    #                 {"tag": "div", "id": "flash-wrapper"},
    #                 {"tag": "div", "id": "flash_wrapper"},
    #                 {"tag": "div", "id": "embedded_job_board_wrapper"},
    #                 {"tag": "section", "class": "level-0"}
                                                    #    ^ try and see if you can do * instead of a number!!
    

#https://boards.greenhouse.io/animallogicsydneyhybridusd/jobs/3985059



#================  Only the bravest of souls look in these depths...         it works but...    you know  =================================================================================================










#!======= Welcome to the form field ==========

    def get_input_tag_elements(self):
        input_elements = self.browser.find_elements(By.TAG_NAME, 'input')
        inputs_info = []
        for input_element in input_elements:
            input_id = input_element.get_attribute('id')
            input_type = input_element.get_attribute('type')
            is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
            inputs_info.append((input_id, input_type, is_hidden))
        return inputs_info

    def find_visible_input(self, selector):
        input_element = self.browser.find_element(By.CSS_SELECTOR, selector)
        is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
        if is_hidden:
            self.browser.execute_script("arguments[0].style.display = 'block';", input_element)
            is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
        return input_element, not is_hidden

    def find_resume_upload_button(self):
        # List of potential selectors
        selectors = [
            (By.CSS_SELECTOR, 'button[aria-describedby="resume-allowable-file-types"]'),
            (By.CSS_SELECTOR, 'button.visible-resume-upload'),
            (By.CSS_SELECTOR, 'button.close-overlay'),
            (By.CSS_SELECTOR, 'input.application-file-input'),
            (By.CSS_SELECTOR, 'input#resume-upload-input'),
            (By.CSS_SELECTOR, 'input[name="resume"]')
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(self.browser, 2).until(EC.presence_of_element_located(selector))
                print(f"Found element: {element}")
                return element
            except:
                continue  # Try the next selector if the current one fails

        return None  # Return None if no matching element is found
    #lever:
    # var failure = $('.resume-upload-failure');
    # var success = $('.resume-upload-success');
    # var working = $('.resume-upload-working');
    def insert_resume(self):
        print("\ninsert_resume()")
        #resume_path = self.users_information.get('WORK_RESUME_PATH')
        resume_path = self.users_information.get('RESUME_PATH')
        print(resume_path)
        
        if self.application_company_name == 'greenhouse':
            element = self.browser.find_element(By.XPATH, "//button[text()='Attach']")
            #element = self.browser.find_element(By.XPATH, "//button[contains(text, 'ATTACH')]")
            #element = self.browser.find_elements(By.ID, "application")
            print("0.1 = ", end="")
            print(element)
            if not element:
                element = self.browser.find_element(By.CLASS_NAME, "resume")
                print("0.2 = ", end="")
                print(element)
            if not element:
                element = self.browser.find_element(By.XPATH, "//button[text()='Attach']")
                print("0.3 = ", end="")
                print(element)
            if not element:
                print("That's so silly! Can't scroll")
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(2)
        print("1")
        
        #for *lever.co* I believe
        resume_file_input = self.browser.find_elements(By.XPATH, '//input[data-qa="input-resume"]')
        print("2")
        print(resume_file_input)
        print("2.1 = ", end="")
        if resume_file_input:
            print("3")
            resume_file_input[0].send_keys(resume_path)
            print("4")
        else:
            print("5")
            self.dismiss_random_popups()
            
            
            
            
            # ---
            #             #self.browser.execute_script("arguments[0].scrollIntoView();", resume_file_input)
            # #resume_upload_button = self.browser.find_element(By.CSS_SELECTOR, 'button.visible-resume-upload')
            # #resume_upload_button = self.browser.find_element(By.CSS_SELECTOR, 'button[aria-describedby="resume-allowable-file-types"]')
            # wait = WebDriverWait(self.browser, 10)
            # #overlay_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.close-overlay')))
            # #overlay_close_button.click()
            # resume_upload_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-describedby="resume-allowable-file-types"]')))
            # vvvv
            resume_upload_button = self.find_resume_upload_button()
            # ----
            
            
            
            
            print("--------------------------------------------------------")
            print(f"resume_upload_button = {resume_upload_button}")
            print("--------------------------------------------------------")
            #print()
            print("6")
            if resume_upload_button:
                time.sleep(1)
                print("8")
                input_elements = self.get_input_tag_elements()
                input_element, is_visible = self.find_visible_input('input[type="file"]')
                print("Bargain-Mart")
                print((input_element, is_visible))
                
                upload_input = self.browser.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                upload_input.send_keys(resume_path)
                print("8.1")
                time.sleep(2)

                print("13")
            else:
                raise Exception('Could not find resume upload element')
        print("14 Holy Hole")
        return
    
    def get_label(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'
        
        if input_element.get('type') == 'radio':
            label = self.find_radio_label(input_element)
            return label
        
        if input_element.get('type') == 'checkbox':
            div_parent, parents_text = self.get_div_parent(input_element)
            if div_parent == 'None' or parents_text == 'None':
                pass
            elif div_parent and parents_text:
                #return div_parent, parents_text
                checkbox_values = [div_parent, parents_text]
                return checkbox_values

        label = None

        # Case 1: Check if the label is a direct previous sibling of the input element
        label = input_element.find_previous_sibling('label')

        # Case 2: Check if the label is inside a parent container
        if not label:
            parent = input_element.find_parent()
            if parent:
                label = parent.find('label')

        # Case 3: Check if the label is associated using the "for" attribute
        if not label:
            input_id = input_element.get('id')
            if input_id:
                label = input_element.find_previous('label', attrs={'for': input_id})

        # Case 4: Check if the input element is a child of a label element
        if not label:
            parent_label = input_element.find_parent('label')
            if parent_label:
                label = parent_label

        # Case 5: Check if a label is inside a parent container of the input element
        if not label:
            parent = input_element.find_parent()
            if parent:
                label = parent.find('label')
                
        # Case 6: Checks if the input element has an 'aria-label' meaning it's dynamic so goes & searches
        # all previous label containers to see if any have text values that are equal to the aria-label' 
        if not label:
            if 'aria-label' in input_element.attrs:
                aria_label_match = None
                parent_label = input_element.find_previous('label')
                aria_label_value = input_element["aria-label"]
                if parent_label.text.strip() == aria_label_value:
                    aria_label_match = True
                if aria_label_match:
                    dynamic_label = aria_label_value + " (dynamic " + input_element.get('type') + ")"
                    if dynamic_label:
                        return dynamic_label
                elif aria_label_match == None:
                    return aria_label_value
                        
        # Case 7: Checks if the input element's style attribute is equal to 'display: none;' meaning it's
        # dynamic so goes & searches for the most previous label container to specify its text value is dynamic
        if not label:
            if input_element.get('style') == 'display: none;':
                previous_input = input_element.find_previous('input')
                if previous_input:
                    parent_label = previous_input.find_previous('label')
                    dynamic_label = parent_label.text.strip() + " (dynamic " + input_element.get('type') + ")"
                    if dynamic_label:
                        return dynamic_label
                    
        # Case 8: Special case for Resume/CV
        if not label and self.one_resume_label == False:
            found_attach = False
            parent_label = input_element.find_previous('label')
            #print(f"----parent_label ========>>>>> {parent_label}")
            label = parent_label
            self.one_resume_label = True
            #TODO: This whole thing is pee pee poo poo
            current_element = input_element
            while current_element:
                if isinstance(current_element, NavigableString) and 'attach' in str(current_element).lower():
                    found_attach = True
                    break
                current_element = current_element.next_sibling
            # Traverse up from the specific_element and find the label tag
            if found_attach:
                label_tag = input_element.find_previous('label')
                if label_tag:
                    # Check if the immediate child is a text value
                    first_child = label_tag.contents[0]
                    if isinstance(first_child, NavigableString) and first_child.strip():
                        holey_holes = first_child.strip()
                    else:
                        # Check if it has a child element and if it does, save that child's text value
                        for child in label_tag.children:
                            if not isinstance(child, NavigableString):
                                holey_holes = child.get_text(strip=True)
                                break
                    #print(f"Text value of the label: {holey_holes}")
                    label = holey_holes
            else:
                print("No sibling found with the 'attach' keyword.")
                #print("Just to remember input_element = ")
                #print(input_element)

        # Check if the label contains a nested div element with the class "application-label" (case for Input 18)
        if label:
            app_label = label.find(lambda tag: 'class' in tag.attrs and 'application-label' in tag['class'])
            if app_label:
                label = app_label

        if label:
            label_text = label.text.strip()

            # If the standard asterisk (*) or fullwidth asterisk (✱) is present, remove everything after it
            if '*' in label_text:
                label_text = label_text.split('*')[0].strip() + ' *'
            elif '✱' in label_text:
                label_text = label_text.split('✱')[0].strip() + ' ✱'
            else:
                # If the newline character (\n) is present, remove it and everything after it
                label_text = label_text.split('\n')[0].strip()

            return label_text

        # Case 6: Check if the input_element has a placeholder attribute
        placeholder = input_element.get('placeholder')
        if placeholder:
            return f"Placeholder ~ {placeholder}"

        return None
    

    def find_radio_label(self, element, stop_level=5):
        current_level = 0
        while (current_level <= stop_level):
            print(f"Level {current_level}:")
            if current_level == 0 or current_level == 5:
                if current_level == 0:
                    print(element.prettify())
                if current_level == 5:
                    sauce = element.next_element.get_text(strip=True)
                    #print(sauce)
                    #print(sauce.encode('utf-8'))
                    return sauce
            element = element.parent
            current_level += 1

    def get_div_parent(self, input_element):
        parent_element = input_element.find_previous(lambda tag: any('question' in class_name for class_name in tag.get('class', [])))
        if parent_element:
            current_element = parent_element.next_element
            while current_element:
                print(f"current_element = {current_element} | ")
                if isinstance(current_element, NavigableString) and current_element.strip():
                    print(f"------------------->    parents_text = {parents_text}")
                    parents_text = current_element.strip()
                    break
                current_element = current_element.next_element
        else:
            print("Craig would be dissapointed in you...    tisk tisk!")
            
        input_tags = input_element.name
        correct_parent = None
        count = 0
        while correct_parent:
            correct_parent = parent_element.find_all(input_tags)     #[, {'type': }]
            if correct_parent:
                parent_element = correct_parent
                break
            parent_element = parent_element.next_sibling
            if count > 4:
                break
            print(count)
            count =+ 1
        return parent_element, parents_text

    #! Maybe include 2 parameters and check if url = None then skip beautifulsoup part!!
    def get_form_input_details(self, url):
        #TODO: GET RID OF THIS AS SOON AS POSSIBLE!!!!
        self.one_resume_label = False
        
        print("\nget_form_input_details()")
        print("      URL = " + url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        form_fields = soup.find_all(['input', 'textarea', 'button', 'select'])

        form_input_details = []
        processed_radios = set()

        for i, field in enumerate(form_fields, start=1):
            input_type = field.get('type')
            input_id = field.get('id')
            input_label = ''
            is_hidden = field.get('style') == 'display: none;' or input_type == 'hidden'
            input_html = str(field).strip()

            if field.name == 'button':
                input_type = 'button'
                # Skip captcha buttons
                if 'h-captcha' in field.get('class', []) or 'g-recaptcha' in field.get('class', []):
                    continue
            elif field.name == 'textarea':
                input_type = 'textarea'
            elif field.name == 'select':
                input_type = 'select'

            # Add a check for the input types you want to keep
            if input_type not in ['text', 'email', 'password', 'select', 'radio', 'checkbox', 'textarea', 'button', 'file'] and input_id != 'education_school_name':
                continue

            values = []
            if input_type == 'select':
                options = field.find_all('option')
                for option in options:
                    values.append(option.text.strip())

            if input_type == 'radio':
                #print("Radio button in get_form_input_details:", field)  # Debugging line
                radio_name = field.get('name')
                if radio_name in processed_radios:
                    continue
                processed_radios.add(radio_name)
                radio_group = soup.find_all('input', {'name': radio_name})
                values = [radio.get('value') for radio in radio_group]
                input_html = ''.join([str(radio).strip() for radio in radio_group])
                
                # Call get_label for the entire radio button group
                input_label = self.get_label(field)
                
            elif input_type == 'checkbox':
                if field in processed_radios:
                    continue
                
                #! values - different -> sometimes value attr or in search next element for text_value!!
                #div_parent, parents_text = self.get_label(field)
                checkbox_values = self.get_label(field)
                print("      SWEET ODIN'S RAVEN ITS A checkbox A... A checkbox I SAY... GOSH DARN YOU LISTEN TO ME ITS A checkbox!!!")
                print("      also the .get_label() appeared to work")
                print("      checkbox_values = ", checkbox_values)
                div_parent = checkbox_values[0]
                print("      div_parent = ", div_parent)
                parents_text = checkbox_values[1]
                print("      parents_text = ", parents_text)
                values = []
                input_label = parents_text
                checkbox_group = div_parent.find_all('input', {'type': [input_type, "text", "textarea"]})
                input_html = ''.join([str(checkbox).strip() for checkbox in checkbox_group])
                for index, input_element in enumerate(checkbox_group):
                    parent_label = input_element.find_previous('label')
                    if input_element.get('type') == 'text':
                        values.append(parent_label.text.strip() + "(dynamic)")
                        continue
                    values.append(parent_label.text.strip())
                    processed_radios.add(input_element)

            else:
                # Call get_label for other input types
                input_label = self.get_label(field)

            # Skip hidden fields without a label
            if is_hidden and not input_label:
                continue

            is_dynamic = False
            related_elements = []

            # Check the field's ancestors for the 'data-show-if' attribute and 'display: none;' style
            current_element = field
            while current_element:
                if current_element.has_attr('data-show-if'):
                    is_dynamic = True
                    related_elements = [
                        {
                            'related_field_id': current_element['data-show-if'].split('==')[0],
                            'trigger_value': current_element['data-show-if'].split('==')[1],
                        }
                    ]
                if current_element.get('style', '') == 'display: none;':
                    is_hidden = True
                current_element = current_element.find_parent()

            form_input_details.append({
                'label': input_label,
                'type': input_type,
                'values': values,
                'is_hidden': is_hidden,
                'html': input_html,
                'dynamic': is_dynamic,
                'related_elements': related_elements,
            })
        print("      Tyrants")
        time.sleep(6)
        self.print_form_details(form_input_details)
        return form_input_details
    
    #TODO: Ummm I don't even know where to start
    #! safe_print
    def print_form_details(self, form_inputs):
        print('\n\n\n')
        jam = "10"
            
        if jam == "1":
            print('--------------------------------------------')
            print("Form Input Details: ", end="")
            for i, detail in enumerate(form_inputs, start=1):
                safe_print(f"Input {i}:")
                safe_print(f"  Label: {detail['label']}")
                safe_print(f"  Type: {detail['type']}")
                safe_print(f"  Values: {detail['values']}")
                safe_print(f"  Is Hidden: {detail['is_hidden']}")
                safe_print(f"  HTML: {detail['html']}")
            print('--------------------------------------------')
            print("\n")
            
        else:
            print('--------------------------------------------')
            print("Form Input Details: ", end="")
            for i, detail in enumerate(form_inputs, start=1):
                print(f"Input {i}:")
                safe_print(f"  Label: {detail['label']}")
                safe_print(f"  Type: {detail['type']}")
                safe_print(f"  Values: {detail['values']}")
                safe_print(f"  Is Hidden: {detail['is_hidden']}")
                safe_print(f"  HTML: {detail['html']}")
                safe_print(f"  Dynamic: {detail['dynamic']}")
                safe_print(f"  Related Elements: {detail['related_elements']}")
            print('--------------------------------------------')
            print("\n")        
        
#********************************************************************************************************
#TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
#########################################################################################################
#NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE
#????????????????????????????????????????????????????????????????????????????????????????????????????????
    
    def print_form_input_extended(self):
        print("\n\n\ndouble_check_before_fill_in_form()")
        
        print('--------------------------------------------')
        print("Form Input Extended: ")
        for key, value in self.form_input_extended.items():
            print(f"{key}: {value}")
        print('--------------------------------------------')
        print("\n")
    
    def extract_css(self, input_data_html):
        soup = BeautifulSoup(input_data_html, 'lxml')
        print("soup = ", soup)
        body_children = soup.body.contents
        for child in body_children:
            print('element = ', child)
            if child.get('id'):
                identifier = child.get('id')
                css_selector = f'#{identifier}'
            elif child.get('class'):
                identifier = child.get('class')[0]
                css_selector = f'.{identifier}'
                
                
            #NEW
            elif child.has_attr('name'):
                name_value = child['name']
                css_selector = f'input[name="{name_value}"]'
                
                
            else:
                raise ValueError('The element does not have an id or a class')

            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

        return elemental
    #TODO: ^ ^ ^ ^ v v v v These are literally exactly the same nerd!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!GOOD LORD THEY ARE NOT!!!  ^ ^ ^ ^DO NOT TOUCH^ ^ ^ ^
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #*Scrolls to each question in the form
    def scroll_to_question(self, input_data_html):
        print("\nscroll_to_question()")
        soup = BeautifulSoup(input_data_html, 'lxml')
        print("soup = ", soup)

        body_children = soup.body.contents
        for child in body_children:
            print('element = ', child)

            if child.get('id'):
                identifier = child.get('id')
                css_selector = f'#{identifier}'
            elif child.get('class'):
                identifier = child.get('class')[0]
                css_selector = f'.{identifier}'
                
            #NEW
            elif child.has_attr('name'):
                name_value = child['name']
                css_selector = f'input[name="{name_value}"]'
                
            else:
                raise ValueError('The element does not have an id or a class')

            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemental)


    #TODO: Good Luck
    def fill_that_form(self):                                                                            #v For `select` when there's too many answers!!
        #if self.form_input_extended['mandatory'] is True and (self.form_input_extended['env_values'] or self.form_input_extended['env_html']):
        # ^ the purpose of the if is b/c...  if we don't need(['mandatory']) to do the question then we don't!!!!
        print("fill_that_form()")
        if self.form_input_extended['env_key'] and self.form_input_extended['env_values']:
            #print("fill_that_form()")
            print('\n\n')
            print(self.form_input_extended)
            print('\n\n')
            time.sleep(1)
            
            
            
            
            
            
            
            element = self.form_input_extended['env_html']
            value = self.form_input_extended['env_values'][0]
            print("element = ", element)
            print("value = ", value)
            success = self.troubleshoot_form_filling(element, value)
            if not success:
                print("Failed to fill in the form. See the error messages above for details.")
            else:
                print("Successfully filled in the form.")
            #-------------------------------------------------------------------------------------------
            #This  v  checks if the "value" is 'empty' or 'None'
            #if self.form_input_extended['bc_nick_said']:
            if 'bc_nick_said' in self.form_input_extended:
                if self.form_input_extended['bc_nick_said'] == True:
                    pass
                elif self.form_input_extended['bc_nick_said'] == False:
                    print("Release the hounds Mr. Smithers...")
                    #self.form_input_extended['bc_nick_said'] == False
                    return
            
            
            
            
            
            
            
            
            # if self.form_input_extended['env_key'] == 'PHONE_NUMBER':
            #     print("Ok at least I made it in here!")
            #     element = self.form_input_extended['env_html']
            #     value = self.form_input_extended['env_values'][0]
            #     print("element = ", element)
            #     print("value = ", value)
                
            #     success = self.troubleshoot_form_filling(element, value)
                
            #     if not success:
            #         print("Failed to fill in the form. See the error messages above for details.")
            #     else:
            #         print("Successfully filled in the form.")
            
            
            
            
            
            
            
            
            
            
            
            if self.form_input_extended['text'] is True:
                #for form_input_answer in self.form_input_extended['env_values']:
                #form_input_answer = self.form_input_extended['env_values']
                print("MADE IT INTO [TEXT] - MADE IT INTO [TEXT] - MADE IT INTO [TEXT] - MADE IT INTO [TEXT]")
                for form_input_ans in self.form_input_extended['env_values']:
                    print("form_input_ans = ", form_input_ans)
                    form_input_answer = form_input_ans
                form_input_html = self.form_input_extended['env_html']
                
                if form_input_answer:
                    #form_input_html.click()
                    #self.browser.form_input_html.send_keys(form_input_answer)
                    #self.form_input_html.send_keys(form_input_answer)
                    form_input_html.send_keys(form_input_answer)
                    print("Text should be inserted => ", form_input_answer)
                    time.sleep(3)
                    return
                
                        
            elif self.form_input_extended['select'] is True:
                #form_input_answer = self.form_input_extended['env_values']
                for form_input_ans in self.form_input_extended['env_values']:
                    print("form_input_ans = ", form_input_ans)
                    form_input_answer = form_input_ans
                
                if answer:
                    form_input_html = self.form_input_extended['env_html']
                    input_select_element = self.form_input_html.find_element(By.TAG_NAME, "input")
                    #select_button = self.form_input_extended(By.)

                    input_select_element.click()
                    answer = form_input_html.find_element(By.ID, form_input_answer)
                    answer.click()
                    return
                elif form_input_answer is None:
                    form_input_html = self.form_input_extended['env_html']
                    input_select_element = self.form_input_html.find_element(By.TAG_NAME, "input")
                    
                    input_select_element.click()
                    self.input_select_element.send_keys(By.TEXT, form_input_answer)
                    self.send_keys("ENTER")
                    if input_select_element == form_input_answer:
                        return
                    elif input_select_element is None:
                        print("Try pressing the `down-arrow` key and then click `ENTER`!!")
                        print("Otherwise click the correct school!")
                    elif input_select_element is not form_input_answer:
                        raise BreakLoopException
                        
            if self.form_input_extended['radio'] is True:
                form_input_answer = self.form_input_extended['env_values']
                form_input_html = self.form_input_extended['env_html']
                
                answer = form_input_html.find_element(By.ID, form_input_answer)
                if answer:
                    answer.click()
                    return
                elif answer is None:
                    answer = self.browser.find_element(By.TEXT, form_input_answer)
                    if answer:
                        answer.click()
                    elif answer is None:
                        print("Ummmm I have no clue about this [radio] call the police maybe??")
                        
            if self.form_input_extended['checkbox'] is True:
                #TODO: Utilize the `select_all` || `select_one` from  self.form_input_extended['']
                form_input_answer = self.form_input_extended['env_values']
                form_input_html = self.form_input_extended['env_html']
                
                answer = form_input_html.find_element(By.ID, form_input_answer)
                if answer:
                    answer.click()
                    return
                elif answer is None:
                    answer = self.browser.find_element(By.TEXT, form_input_answer)
                    if answer:
                        answer.click()
                    elif answer is None:
                        print("Ummmm I have no clue about this [checkbox] call the police maybe??")
                        
            if self.form_input_extended['button'] is True:
                form_input_answer = self.form_input_extended['env_values']
                form_input_html = self.form_input_extended['env_html']
                
                answer = form_input_html.find_element(By.ID, form_input_answer)
                if answer:
                    answer.click()
                    return
                elif answer is None:
                    answer = self.browser.find_element(By.TEXT, form_input_answer)
                    if answer:
                        answer.click()
                    elif answer is None:
                        print("Ummmm I have no clue about this [checkbox] call the police maybe??")
                        
            elif self.form_input_extended['file'] is True:
                form_input_answer = self.form_input_extended['env_values']
                form_input_html = self.form_input_extended['env_html']
                
                answer = form_input_html.find_element(By.ID, form_input_answer)
                if answer:
                    answer.click()
                    return
                elif answer is None:
                    answer = self.browser.find_element(By.TEXT, form_input_answer)
                    if answer:
                        answer.click()
                    elif answer is None:
                        print("Ummmm I have no clue about this [file] call the police maybe??")
                        
        if self.form_input_extended['mandatory'] is True and not self.form_input_extended['env_values']:
            if self.max_similarity < .25:
                print("prompt user to answer!!!")
            else:
                #Skips the form
                raise BreakLoopException
    
    def troubleshoot_form_filling(self, element, value):
        try:
            # Check if the value is not None or empty
            if not value:
                print("Error: Value is None or empty")
                return False

            # Check if the element is present
            if element is None:
                print("Error: Element is None")
                return False

            # Check if the element is an input field
            if element.tag_name.lower() != 'input':
                print(f"Error: Element is not an input field, it's a {element.tag_name}")
                return False

            # Check if the element has the correct attributes
            if element.get_attribute('name') != 'job_application[phone]':
                print("Error: Element has incorrect name attribute")
                return False

            # Check if the element is displayed (visible to the user)
            if not element.is_displayed():
                print("Error: Element is not displayed")
                return False

            # Check if the element is enabled (interactable)
            if not element.is_enabled():
                print("Error: Element is not enabled")
                return False

            # Try to fill in the form
            element.clear()
            element.send_keys(value)
            print(f"Success: Filled in the form with {value}")

            return True
        except Exception as e:
            print(f"Error: An exception occurred: {e}")
            return False

    

        
            
    #TODO: Make the weight of 'your' and 'user'/'users' EQUAL (What is you address? = USERS_ADRESS)!!!!!!
    #TODO: For 'I acknowledge' buttons check the answers for that and just skip everything!!
        #TODO: Same with 'subscribe' && '?'
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                               TESTING                                         ! [https://github.com/explosion/spaCy]
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def init_form_input_extended(self):
        self.form_input_extended = {
            "mandatory": False,
            "text": False,
            "select": False,
            "radio": False,
            "checkbox": False,
            "button": False,
            "file": False,
            "select all": False,
            "select one": False,
            "dynamic": False,
            "env_key": None,
            "env_values": [],
            "env_html": None
        }
    
    #*Analyzes the label and values along with the .env(key-value) && config.py files
    #! THIS METHOD IS WHERE WE FIND OUT IF WE HAVE AN ANSWER OR NOT!!    ssoooo if we don't then we send fill_in_form() that user_response is needed!!!
    #TODO: Make sure sure to handle N/A situations as well!!
    #! THIS SHOULDN'T HAVE return ANYWHERE OTHER THAN THE END!! This should only basically be re-directs!!!!
    #! safe_print()
    def process_form_inputs(self, form_input_details):
        print("\nprocess_form_inputs()")
        self.init_form_input_extended()

        # self.nlp_load()
        # print("nlp loaded... ")

        submit_button = None
        remove_attachment = None
        resume_attachment = None
        for i, input_data in enumerate(form_input_details):
            try:
                print("\n\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

                time.sleep(2)
                self.init_form_input_extended()
                self.is_special_case(input_data)

                #++++++++++++++++++++++++++++++ MAYBE treat like edge cases +++++++++++++++++++++++++++++++++++++++
                print(f"Input {str(i)}:")
                safe_print(f"  form_input_details = {input_data}")
                if input_data['is_hidden']:
                    continue


                #! THIS HAS TO BE 1st!!!!!!!!!  b/c if it's None or 'empty'(null) then all the other tests give erros when comparring!!
                print("This is -> None or empty")
                #Basically checks for None and empty!!
                if not input_data['label'] or input_data['label'] is None:
                    print("Dang so -> input_data['label'] is None or empty")
                    continue

                print("This is -> dynamic")
                # or input_data['label'] is None:
                if 'dynamic' in input_data['label']:
                    print("Dang so -> dynamic")
                    continue

                print("This is -> == None       ...straight-up")
                if input_data['label'] is None:
                    print("Dang so -> == None       ...straight-up")
                    continue

                print("This is -> == None       IT'S A STRING")
                if input_data['label'] == 'None':
                    print("Dang so -> == None       IT'S A STRING")
                    continue



                if 'Remove attachment' in input_data['label']:
                    print("Remove attachment: (a file of sorts)")
                    safe_print(f"input_data: {input_data}")
                    remove_attachment = input_data
                    safe_print(f"remove_attachment: {remove_attachment}")
                    continue


                if 'Resume/CV' in input_data['label']:
                    print("Resume/CV: (a file)")
                    safe_print(f"input_data: {input_data}")
                    resume_attachment = input_data
                    safe_print(f"resume_attachment: {resume_attachment}")
                    continue


                if 'Submit Application' in input_data['label']:
                    print("Submit Application")
                    safe_print(f"input_data: {input_data}")
                    submit_button = input_data
                    safe_print(f"submit_button: {submit_button}")
                    continue
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


                self.scroll_to_question(input_data['html'])
                print("  Scrolled here I guess...\n")
                safe_print(f"self.form_input_extended = {self.form_input_extended}")
                time.sleep(1)

                label = input_data['label']
                safe_print(f"unprocessed label: {label}")
                label = self.process_text(label)
                safe_print(f"processed label: {label}")
                input_type = input_data['type']
                predefined_options = input_data.get('values', None)
                safe_print(f"predefined_options = {predefined_options}")

                # If the input type in select, radio, or checkbox, handle it as a !special case!
                print("\n_____________________________________________________________________________________")
                print("TIME FOR COMPARISONS! DO YOU HEAR THAT BUTT-HEAD!!! WE ARE GONNA BE COMPARING!!")
                if input_type in ['select', 'radio', 'checkbox']:
                    print("Ahhhhhhh yes it is either one of these: 'select', 'radio', 'checkbox'")
                    matching_keys = self.get_matching_keys(label)               #! .get_matching_keys() does all the comaparing to get the right answer!!!!! ssooo there do   special case check -> .env chack -> long q>a ... a>a check!!!
                    if matching_keys:
                        #!HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE
                        safe_print(f"self.form_input_extended = {self.form_input_extended}")
                        for key in matching_keys:

                            answer = self.users_information[{key}]
                            safe_print(f"answer = {answer}")
                            if answer in predefined_options:
                                # Input the answer into the form
                                safe_print(f"Entering '{answer}' for '{label}'")
                            else:
                                safe_print(f"Stored answer '{answer}' is not a valid option for '{label}'")
                    else:
                        safe_print(f"No stored answers found for '{label}'")

                else:
                    print("This one ain't special... this one ain't even intelligent... dumb ol' question any how")
                    matching_keys = self.try_finding_match(label)
                    safe_print(f"matching_keys = {matching_keys}")

                    print("if matching_keys: ", end="")
                    print("True" if matching_keys else "False")

                    if matching_keys:
                        
                        if not self.form_input_extended['env_values']:
                            
                            self.form_input_extended['env_values'].append(matching_keys)
                        
                        
                        
                        ##############################################################
                        print("self.form_input_extended['env_values'] = ", self.form_input_extended['env_values'])
                        for key in self.form_input_extended['env_values']:
                            safe_print(f"key = {key}")
                            answer = self.users_information.get(key)
                            safe_print(f"answer = {answer}")
                            # Input the answer into the form
                            safe_print(f"Entering '{answer}' for '{label}'")
                        ##############################################################
                    else:
                        context = self.q_and_a['summary'] + " " + label
                        answer = self.generate_response(context)
                        if answer:
                            # Input the answer into the form
                            safe_print(f"Entering '{answer}' for '{label}'")
                            #self.fill_form(label, answer)
                        else:
                            safe_print(f"No stored answers found for '{label}'")
                self.form_input_extended['env_html'] = self.extract_css(input_data['html'])

                self.print_form_input_extended()     ############################### HERE VON!!!

                self.fill_that_form()


            except BreakLoopException:
                print("You know what forget that job anyways! They probably suck and would've over worked you.")
                return
        self.submit_job_application(submit_button)
        print("ALL DONE!!! The job application has been completed Counselor Mackie...")
        print("Normally Counselor Mackie would recommend pushing the 'Submit Application' button right now!")
        time.sleep(2)
    
    #def check_env_file()
    def try_finding_match(self, label):
        print("\n1)try_finding_match()")
        words_in_label = label.split()
        jacc_key = None
        if len(words_in_label) <= 2:
            print("This question has 2 words or less.")
            print(words_in_label)
        
        else:
            print("This question has more than 2 words.")
            #! => doc = self.nlp(label)
            named_entities, headword, dependants = self.spacy_extract_key_info(self.nlp(label))
            print(f"named_entities = {named_entities}")
            print(f"headword = {headword}")
            print(f"dependants = {dependants}")
            key = self.generate_key(named_entities, headword, dependants)
            jacc_key = key.lower().replace("_", " ")
            print("jacc_key = ", jacc_key)
        
        #self.JobSearchWorkflow_instance.load_custom_rules()
        print("words_in_label = ", words_in_label)
        print("label = ", label)
        #NOTE: Remember Q_AND_A is only for the summary! So we only traverse CUSTOM_RULES!!
        print("self.custom_rules = ", self.custom_rules)
        for rule_capital in self.custom_rules:
            
            
            
            
            
            
            rule = rule_capital.lower()
            if label == rule:
                print("MATCH: [ try_finding_match() ]")
                print("\tCUSTOM_RULES = ", rule)
                print("\tlabel = ", label)
                value = self.convert_custom_rule_values(label, rule_capital)
                print("\t... value = ", self.custom_rules[rule_capital])
                self.form_input_extended['env_key'] = rule_capital
                return value
            
            
            
            
            
            
            
        found_best_match = self.find_best_match(label)
        print("found_best_match = ", found_best_match)
        
        #TODO: REPLACE THIS    v!!!!!!!!!!
        # if label == config.py[key]:
        #     return config.py[key]
        if found_best_match:
            return found_best_match
        #! RECENT CHANGE RECENT CHANGE RECENT CHANGE
        # elif self.jaccard_similarity(jacc_key, label):
        #     return jacc_key
        # else:
        #     #Since `rule` was previously defined you use it as above but since `summary` wasn't {something about Python treats} so just use () with '' inside it and the variable name within the ''
        #     return self.generate_response(self.q_and_a('summary'))
       
        
        #! HERE HERE HERE HERE
               
                   
        else:
            jacc_key
    
    
    #*SpaCy's needs
    #TODO: do something !!!!
    #analyze_and_flag_question_requirements()
    def process_text(self, text):
        print("process_text()")
        #if "*" in text or "✱" in text:
        asterisk_list = ["*", "✲", "✱", "＊", "﹡", "⁎", "✻", "∗", "⃰", "✲", "✳", "꙳", "﹡", "※", "⁂", "✢", "✣", "✤", "✥", "✦", "✧", "✶", "✷", "✸", "✹", "✺", "✼", "✽", "❃", "❊", "❋"]

        if any(asterisk in text for asterisk in asterisk_list):
            self.form_input_extended['mandatory'] = True
        if 'select one' in text.lower():
            self.form_input_extended['select one'] = True
        if 'select all' in text.lower() or 'mark all' in text.lower():
            self.form_input_extended['select all'] = True
        return text.lower().strip().replace("(", "").replace(")", "").replace(".", "").replace("?", "").replace("*", "").replace("✱", "").strip()
    
    #*Answer simple question for user based off their provided summary
    def generate_response(self, context):
        print("\ngenerate_response()")
        print("context = ", context)
        input_ids = self.tokenizer.encode(context, return_tensors='pt').to("cuda" if torch.cuda.is_available() else "cpu")

        max_length = len(input_ids[0]) + 100
        output = self.model.generate(input_ids, max_length=max_length, temperature=0.7)
        response = self.tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        print("response = ", response)
        
        return response
    
    #*Checklist/Radio just transitions Yes-True && No-False
    def bool_to_str(self, value):
        print("\nbool_to_str()")
        return "Yes" if value.lower() == "true" else "No"
    
    #*SpaCy runs SpaCy methods
    def spacy_extract_key_info(self, doc):
        print("\nspacy_extract_key_info()")
        print("\n\n--------------------------------------------------------")
        print("My Way")
        print("spacy_extract_headword_and_dependants()")
        headword = ""
        dependants = []
        for token in doc:
            print(f"""
                  TOKEN: {token.text}
                  ====
                  {token.tag_ = }
                  {token.head.text = }
                  {token.dep_ = }
                  """)
            
            
            print(token.head)
            if token.dep_ == "ROOT":
                headword = token.head.text
            elif token.dep_ in {"compound", "amod", "attr"}:
                dependants.append(token.lemma_)
                #dependants.append(token.text)
        print(f"headword = {headword}")
        print(f"dependants = {dependants}")
        #return headword, dependants
        print("--------------------------------------------------------")
        
        print("\n\n--------------------------------------------------------")
        print("Their Dumb Way")
        named_entities = [ent.text for ent in doc.ents]
        headword = ""
        dependants = []
        for token in doc:
            if token.dep_ == "ROOT":
                headword = token.lemma_
            elif token.dep_ in {"compound", "amod", "attr"}:
                dependants.append(token.lemma_)
        print(f"named_entities = {named_entities}")
        print(f"headword = {headword}")
        print(f"dependants = {dependants}")
        #return named_entities, headword, dependants
        print("--------------------------------------------------------")
        return named_entities, headword, dependants
    
    #*If SpaCy special case needs to be made... ensure it!! and if still yes then do so here
    def generate_key(self, named_entities, headword, dependants):
        print("\ngenerate_key()")
        
        # Using set automatically eliminates duplicates for us!!
        tokens = set(named_entities + [headword] + dependants)
        key = "_".join(tokens).upper()
        print(f"key = {key}")
        return key
    
    #TODO: ADD NEW key-value PAIR TO FILE  &&  THE custom_rules or users_information
    #*Add !UNIQUE! key-value pair to EITHER config.py || .env
    def store_new_answer(self, question, answer):
        print("\nstore_new_answer()")
        #nlp = spacy.load("en_core_web_md")
        doc = self.nlp(question.lower())
        named_entities, headword, dependants = self.spacy_extract_key_info(doc)
        key = self.generate_key(named_entities, headword, dependants)
        #key = self.verify_key(key, question)
        
        # If key is unique, add it to the .env file
        if key not in self.users_information:
            self.users_information[key] = answer
            with open(self.env_path, "a") as file:
                file.write(f"\n{key}='{answer}")
    
    #TODO:------------------------------------------------------------------------------
    #TODO: redid the synonym method
    def handle_match(self, key, label):
        print(f"\nhandle_match()")
        print("MATCH: [ 2.1)find_best_match() -> .similarity(question{*label*} | self.users_information.key)]")
        print("\tusers_information = ", key)
        print("\tlabel = ", label)
        print("\t... value = ", self.users_information[key])
        self.form_input_extended['env_key'] = key
        self.form_input_extended['env_values'].append(self.users_information[key])
        return key
    
    #*Uses label to try and find a matching key from the users' .env
    
    def find_best_match(self, label):
        print("\n2)find_best_match()")
        
        doc1 = self.nlp(label.lower())
        print("-doc1 = ", doc1)
        max_similarity = -1
        best_match = None
        synonyms = self.get_synonyms(label)
        
        print("users_information + 1")
        for key in self.users_information.keys():
            doc2 = self.nlp(key.lower().replace("_", " "))
            print("-doc2(self.users_information.key) = ", doc2)
            similarity = doc1.similarity(doc2)
            print("similarity = ", similarity)
            print("key = ", key)
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = key    #leave as = to key so it's just easier for later!!
                print("max_similarity = ", max_similarity)
                print("best_match = ", best_match)
                
                if max_similarity == 1.0:
                    print("Before assignment:", self.form_input_extended)
                    print("Before assignment(key):", key)
                    self.form_input_extended['env_key'] = key
                    print("After assignment:", self.form_input_extended)
                    print("After assignment(key):", key)
                    
                    self.form_input_extended['env_values'].append(self.users_information[key])
                    print("MATCH: [ 2.1)find_best_match() -> .similarity(question{*label*} | self.users_information.key)]")
                    print("\tusers_information = ", key)
                    print("\tlabel = ", label)
                    print("\t... value = ", self.users_information[key])
                    #print("\t... value = ", self.users_information['{key}'])
                    return key
                elif len(synonyms) > 0:
                    for synonym in synonyms:
                        doc2_syn = self.nlp(synonym.lower().replace("_", " "))
                        similarity_syn = doc2_syn.similarity(doc2)
                        if similarity_syn > max_similarity:
                            max_similarity = similarity_syn
                            best_match = key
                            
                            if max_similarity == 1.0:
                                print("Before assignment:", self.form_input_extended)
                                print("Before assignment(key):", key)
                                self.form_input_extended['env_key'] = key
                                print("After assignment:", self.form_input_extended)
                                print("After assignment(key):", key)
                                
                                self.form_input_extended['env_values'].append(self.users_information[key])
                                print("MATCH: [ 2.1)find_best_match() -> .similarity(question{*label*} | self.users_information.key)]")
                                print("\tusers_information = ", key)
                                print("\tlabel = ", label)
                                print("\t... value = ", self.users_information[key])
                                return key
            print("\nusers_information + 1") 
        print("max_similarity = ", max_similarity)
        print("best_match = ", best_match)
        print(best_match if max_similarity > 0.90 else None)
        return best_match if max_similarity > 0.90 else None
    
    def check_similarity(self, doc1, doc2, key, label, max_similarity):
        similarity = doc1.similarity(doc2)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = key
            if max_similarity == 1.0:
                return self.handle_match(key, label), max_similarity
        return best_match, max_similarity

    def find_the_bestest_match(self, label):       #aka - "find_best_match"
        print("\n2)find_best_match()")
        doc1 = self.nlp(label.lower())
        max_similarity = -1
        best_match = None
        synonyms = self.get_synonyms(label)

        for key in self.users_information.keys():
            doc2 = self.nlp(key.lower().replace("_", " "))
            best_match, max_similarity = self.check_similarity(doc1, doc2, key, label, max_similarity)

            if len(synonyms) > 0:
                for synonym in synonyms:
                    doc2_syn = self.nlp(synonym.lower().replace("_", " "))
                    best_match, max_similarity = self.check_similarity(doc1, doc2_syn, key, label, max_similarity)

        print("max_similarity = ", max_similarity)
        print("best_match = ", best_match)
        return best_match if max_similarity > 0.90 else None
    #TODO:------------------------------------------------------------------------------
    
    #*This is the DOUBLE CHECK
    def get_synonyms(self, word):
        print("\n3)get_synonyms()")
        print(f"word = {word}")
        #TODO: Ensure this resets the list of synonyms each time
        synonyms = []

        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        #TODO: DOUBLE CHECK THIS!!!!! Your asking for the synonyms of `phone number`?!?!?!?! Do we really want the synonyms for the key and not the label?!?!?!
        if word.lower() in self.custom_synonyms:
            #for custom_syn in self.custom_synonyms[word]:
            for custom_syn in self.custom_synonyms[self.process_text(word)]:
                #synonyms.extend(custom_syn)
                print("filtered_custom_syn = ", end="")
                filtered_custom_syn = self.process_text(custom_syn)
                filtered_custom_syn = filtered_custom_syn.replace("_", " ")
                print(filtered_custom_syn)
                synonyms.append(filtered_custom_syn)

        print("self.custom_synonyms = ", end="")
        print(self.custom_synonyms)
        
        
        print("synonyms = ", end="")
        print(synonyms)
        print("\n--------------------")
        
        time.sleep(2)
        
        return synonyms
    
    #*Just for me to see what it does!!
    def jaccard_similarity(self, sentence1, sentence2):
        print("\njaccard_similarity()")
        set1 = set(sentence1.lower().split())
        set2 = set(sentence2.lower().split())
        intersection = set1.intersection(set2)
        print(f"intersection = {intersection}")
        union = set1.union(set2)
        print(f"union = {union}")
        jaccard_similarity = (len(intersection) / len(union))
        print(f"jaccard_similarity = {jaccard_similarity}")
        if jaccard_similarity > 90:
            return True
        else:
            return False
    
    def submit_job_application(self, submit_button):
        
        print("We are about to click the submit button")
        time.sleep(3)
        submit_button = self.extract_css(submit_button['HTML'])
        print("submit_button = ", submit_button)
        time.sleep(1)
        submit_element_idk = self.browser.find_element(By.CSS_SELECTOR, submit_button)
        print("submit_element_idk = ", submit_element_idk)
        time.sleep(1)
        self.keep_jobs_applied_to_info()
        #self.sessions_applied_to_info
        return
        
        
        
        
        
        #submit_button_index = self.form_input_details.get('KEY-NAME')
        #submit_button = self.extract_css(submit_button_index['HTML'])
        
        '''
        submit_button = self.extract_css(submit_button['HTML'])
        
        self.browser.find_element(By.CSS_SELECTOR, submit_button).click()
        
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".response-message")))
        
        response_message = self.browser.find_element(By.CSS_SELECTOR, ".response-message").text
        if "success" in response_message.lower():
            self.keep_jobs_applied_to_info()
            print("Form submission was successful!")
        else:
            print("Form submission failed!")
            
        error_messages = self.driver.find_elements(By.CSS_SELECTOR, ".error-message")
        for error_message in error_messages:
            print(f"Error: {error_message.text}")
        '''
            
        #TODO: Add call to oxylabs captcha!!!!! 
            
        #TODO: I believe I just return all the way to go to the next job application!!!!
        #return

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                                                               !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    #TODO: Check the wording in the question
    #*special_case() method 2
    def is_special_case(self, input_data):
        label = input_data['type']
        if label in ['select', 'radio', 'checkbox', 'file']:  #NOT 'button' b/c that's just the Submit
            if label == 'select':
                select_element = self.browser.find_element(label)
                is_multiple_choice = select_element.get_attribute('multiple') is not None
                if is_multiple_choice is True:
                    self.form_input_extended['text'] = 'is_multiple_choice'
                elif is_multiple_choice is False:
                    pass
            elif label == 'checkbox':
                self.form_input_extended['checkbox'] = True
                self.form_input_extended = 'is_multiple_choice'
            elif label == 'radio':
                self.form_input_extended['radio'] = True
            elif label == 'file':
                self.form_input_extended['file'] = True
        else:
            if label == 'text' or label == 'textarea':
                self.form_input_extended['text'] = True
            elif label == 'button':
                self.form_input_extended['text'] = True
            
            else:
                print("There has been an error father...")
                print("label = ", label)
        return
    
    
    
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # ^ All that code deals with obtaining the right answer
    # v All this code will deal with 

    #TODO: Once we submit the application confirm that here and then save everything!!!
        #? For the user or my google_sheet_stats i don't know???
    #* My vote is we leave it as it is so b/c this is the correct format for Google Sheet's!!!
    #* Then JobsThatUserHasAppliedTo.csv has the same format and we can just add the session time at the end easily!!
    #! REMEMBER: if the program crashes it has to hold/preserve values!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def keep_jobs_applied_to_info(self):
        self.sessions_applied_to_info.append({
            'Job_URL': self.current_url,
            'Company_Name': self.current_jobs_details["company_name"],
            'Job_Title': self.current_jobs_details["job_title"],
            'Company_Job_Location': self.current_jobs_details["job_location"],
            'Company_Department': self.company_job_department,
            'Job_ID_Number': self.job_id_number,
        })
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    #Design layout for Answering
    #The question ITSELF requires either 'at most 1 answer' OR 'more'!!! (Meaning if there is a question present its there for a reason so requires 'at most an answer'...  UNLESS IT STATES IT WANTS !!a specific amount!! OR...  OR at least one->and this implies the max number of options available or infinity!)                    and beyond
    #SSSSooooooo when programming the process to fill in answers for the user this is the process
      #MAIN IDEA) My program is either capable of answering the question or it isn't!!
        #1)We always try to answer everything so...  ONWARD!!!  with trying to find an answer!
        #2)Figure out if it's anything other than text input!
            #NOTE:This is because at first glance we are restricted to only being able to choose from a
            #select group of answers! IMPORTANT because this is POSSIBLY PROBLEMATIC b/c if we find an
            #exact question<=>key match that means nothing!!!...   as the keys-value ALSO has to match
            #one of the available answer options!!!!!
         #2.1)Maybe here then is when we read the question for the first time and try to figure out if
         #the question signifies {at most 1 answer|a specific amount and if so then more or less|max amount
         #available}  

    #**************************************
    # form_input_details.append({
    #     'label': input_label,
    #     'type': input_type,
    #     'values': values,
    #     'is_hidden': is_hidden,
    #     'html': input_html,
    #     'dynamic': is_dynamic,
    #     'related_elements': related_elements,
    # })
    #**************************************





    def keep_jobs_applied_to_info(self):
        self.jobs_applied_to_this_session.append(self.current_jobs_details)




    # def how_to_anwser(self):
    #     #Bubble in answers
    #     #if one ans needed do what I have above it picks the best answer overall
    #     if self.form_input_extended
    #     #else multiple ans needed
    #         #list_holding_multiple_keys = []
    #         #for specific_answer in self.form_details:
    #             #if specific_answer in self.env_values:
    #                 #list_holding_multiple_keys.append(specific_answer)
    #                 #print(self.env_values[specific_answer])  =>  the answer
        
    #     #Text filled answers
        
    #     #if Mandatory self.how_to_anwser() JUST ONCE!!!!
    #     #else skip


    def deconstruct_custom_rules_dict_smoothly(self, matching_key):
        # for key, value_list in self.custom_rules.items():
        #     if matching_key == key:
        #         return value_list
        # #No equal key found in CUSTOM_RULES
        # return None
        
        #When choosing the first item from an iterable that passes a condition, we can use the next built-in function instead of a for-loop to make our code and our intent clearer.
        # ^ [https://docs.sourcery.ai/Reference/Python/Default-Rules/use-next/#after]
        #https://www.geeksforgeeks.org/python-next-method/ (<- so next isn't faster than the for loop but it just makes our code more concise...  idk the dumb computer told me to)
        return next((value_list for key, value_list in self.custom_rules.items() if matching_key == key), None)
            

    #! 
    def convert_custom_rule_values(self, label, rule_capital):
        print(f"\nconvert_custom_rule_values()")
        final_string = ''
        # v ??This part is basically just checking if key is present otherwise skip!?!?!?
        #! I believe  v  this is for synonyms!?!?!?!?
        #custom_key_value = self.check_if_label_in_customs(self.custom_rules, label)
        print(f"      label = {label}")
        custom_key_value = self.custom_rules[rule_capital]
        print(f"      rule_capital = {rule_capital}")
        print(f"      custom_key_value = {custom_key_value}")
        
        for custom_rule_value in custom_key_value:
            print(f"      custom_rule_value = {custom_rule_value}")
            if custom_rule_value.strip():
                value = self.determine_type_of_value(custom_rule_value.strip())
            else:
                #Handles the space issue!
                value = " "
            print(f"      value = {value}")
            final_string += value
            print(f"      final_string = {final_string}\n")

        print(f"      final_string = {final_string}")
        return final_string
    
    # This determines if the value obtained from the config.py dictionary variable's key-value pair is
    # connected to the .env file | variable from the code | just regular string text  
    def determine_type_of_value(self, custom_rule_value):
        print(f"\ndetermine_type_of_value()")
        if value := self.extract_env_values(custom_rule_value):
            print("Found in the .env file")
        #TODO: Perhaps change this so that it checks if index 0=( and length-1=) signifying exec instead of running it the way you are!!!
        elif value := self.check_if_custom_rule_exec(custom_rule_value):
            print("Found out this is executable")
        else:
            #value = custom_rule_value
            print("Found out this is Normal  boooo")
        return value
        
    def check_if_custom_rule_exec(self, custom_rule_value):
        print(f"\ncheck_if_custom_rule_exec()")
        try:
            exec("result = " + custom_rule_value)
            #final_value += str(result) + ' '
            final_value += str(result)
        except Exception as e:
            print(f"Error in executing code: {e}")
        return final_value

    def extract_env_values(self, custom_values_key):
        print(f"\nextract_env_values()")
        print(f"      self.users_information = {self.users_information}")
        for env_key in self.users_information:
            print(f"      env_key = {env_key}")
            print(f"      custom_values_key = {custom_values_key}")
            if custom_values_key == env_key:
                env_value = self.users_information[env_key]
                print(f"      env_value = {env_value}")
                return env_value
        # v  This should never run
        return NameError
    
    def check_if_label_in_customs(self, specific_custom, label):
        for custom_key in specific_custom:
            if label == custom_key:
                custom_key_value = custom_key[label]
                return custom_key_value
        return None







    
    @property
    def companys_internal_job_openings_URL(self):
        return self._companys_internal_job_openings_URL

    @companys_internal_job_openings_URL.setter
    def companys_internal_job_openings_URL(self, value):
        print(f"self._companys_internal_job_openings_URL = {value}")  # Print statement here
        self._companys_internal_job_openings_URL = value
        if value not in (None, 'null', ''):
            self.method_to_execute_on_set()

    def method_to_execute_on_set(self):
        print("Method executed when companys_internal_job_openings_URL is set!")










def check_language(self):
    import fasttext
    soup = self.soup_elements['soup']
    text = soup.get_text()
    model = fasttext.load_model('lid.176.bin')
    predictions = model.predict(text)
    language_of_webpage = predictions[0][0].replace('__label__', '')
    #TODO: Determine whether this should go here or somewhere else!!
    if language_of_webpage == 'en':
        return True
    else:
        return False
    # = = = = 
    # return language_of_webpage == 'en'
    return language_of_webpage

def try_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        return False
    return True


# def safe_print(text):
#     if not try_print(text):
#         # encoded_text = text.encode('utf-8')
#         encoded_text = text.encode('utf-8', 'replace')
#         decoded_text = encoded_text.decode(sys.stdout.encoding, 'replace')
#         print(decoded_text)
def safe_print(text):
    if not try_print(text):
        try:
            # Attempt to print using a different encoding
            print(text.encode('cp1252', 'replace').decode('cp1252'))
        except Exception as e:
            # If all else fails, replace problematic characters and print
            print(text.encode('ascii', 'replace').decode('ascii'))



class BreakLoopException(Exception):
    pass

























#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------

#                Misc code stuff...  idk 

#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------









# Lever code:
#   <script type="application/ld+json">{"@context" : "http://schema.org","@type" : "JobPosting","title" : "Head of Global Program Management","hiringOrganization" : {"@type" : "Organization","name": "PayU","logo": "https://s3.eu-central-1.amazonaws.com/co.lever.eu.client-logos/c9b25872-01be-4cfc-a2bf-e00deba2faf8-1694526086320.png"},"jobLocation":{"@type" : "Place","address" : {"@type" : "PostalAddress","addressLocality" : "Pozna┼ä, Poland or Bucharest, Romania","addressRegion" : null,"addressCountry" : null,"postalCode" : null}},"employmentType" : "Full-time","datePosted" : "2023-11-22","description" : "<p><b style=\"font-size: 11pt\">About PayU</b><span style=\"font-size: 11pt\">&nbsp;</span></p><p><span style=\"font-size: 11pt\">PayU, a leading payment and Fintech company in 50+ high-growth markets throughout Asia, Central and Eastern Europe, Latin America, the Middle East and Africa, part of&nbsp;Prosus&nbs




# greenhouse code:
#   <div class="select2-search select2-search-hidden select2-offscreen">       <label for="s2id_autogen2_search" class="select2-offscreen">Are you Hispanic/Latino?</label>       <input type="text" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" class="select2-input" role="combobox" aria-expanded="true" aria-autocomplete="list" aria-owns="select2-results-2" id="s2id_autogen2_search" placeholder="">   </div>   <ul class="select2-results" role="listbox" id="select2-results-2">   </ul>

#+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + 

#(dynamic question > college name)
# This code is found in 'Inspect (Q)' at the bottom of ALL the code(even footer) AND has an 'event' button
#  to click ssooo... ya! Search for this for ?dynamic code? or perhaps just this type of ?dynamic list?
#  Lastly, 'dynamic search bar for colleges' && 'actual list of colleges' are found INSIDE this v
# <div class="select2-drop select2-display-none select2-with-searchbox select2-drop-active" style="left: 206px; width: 659px; top: 2968.8px; bottom: auto; display: none;">   <div class="select2-search">       <label for="s2id_autogen6_search" class="select2-offscreen">
#           School
#         </label>       <input type="text" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" class="select2-input" role="combobox" aria-expanded="true" aria-autocomplete="both" aria-owns="select2-results-6" id="s2id_autogen6_search" placeholder="" aria-controls="select2List1">   </div>   <ul class="select2-results" role="listbox" id="select2List1"></ul></div>
# The dynamic search bar for colleges
#        <label for="s2id_autogen6_search" class="select2-offscreen">          School        </label>       <input type="text" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" class="select2-input" role="combobox" aria-expanded="true" aria-autocomplete="both" aria-owns="select2-results-6" id="s2id_autogen6_search" placeholder="" aria-controls="select2List1" aria-activedescendant="select2-result-label-113">
# The actual list of colleges ====>>>>> NOTE: <ul role="listbox"     <-Find list using this!!!!
#!  <div class="select2-search">       <label for="s2id_autogen6_search" class="select2-offscreen">          School        </label>       <input type="text" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" class="select2-input" role="combobox" aria-expanded="true" aria-autocomplete="both" aria-owns="select2-results-6" id="s2id_autogen6_search" placeholder="" aria-controls="select2List1" aria-activedescendant="select2-result-label-114">   </div>   <ul class="select2-results" role="listbox" id="select2List1"><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-109" role="option"><span class="select2-match"></span>Abraham Baldwin Agricultural College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-110" role="option"><span class="select2-match"></span>Academy of Art University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-111" role="option"><span class="select2-match"></span>Acadia University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-112" role="option"><span class="select2-match"></span>Adams State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-113" role="option"><span class="select2-match"></span>Adelphi University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable select2-highlighted" role="option" aria-selected="true" id="selectedOption"><div class="select2-result-label" id="select2-result-label-114" role="option"><span class="select2-match"></span>Adrian College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-115" role="option"><span class="select2-match"></span>Adventist University of Health Sciences</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-116" role="option"><span class="select2-match"></span>Agnes Scott College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-117" role="option"><span class="select2-match"></span>AIB College of Business</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-118" role="option"><span class="select2-match"></span>Alaska Pacific University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-119" role="option"><span class="select2-match"></span>Albany College of Pharmacy and Health Sciences</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-120" role="option"><span class="select2-match"></span>Albany State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-121" role="option"><span class="select2-match"></span>Albertus Magnus College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-122" role="option"><span class="select2-match"></span>Albion College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-123" role="option"><span class="select2-match"></span>Albright College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-124" role="option"><span class="select2-match"></span>Alderson Broaddus University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-125" role="option"><span class="select2-match"></span>Alfred University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-126" role="option"><span class="select2-match"></span>Alice Lloyd College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-127" role="option"><span class="select2-match"></span>Allegheny College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-128" role="option"><span class="select2-match"></span>Allen College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-129" role="option"><span class="select2-match"></span>Allen University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-130" role="option"><span class="select2-match"></span>Alliant International University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-131" role="option"><span class="select2-match"></span>Alma College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-132" role="option"><span class="select2-match"></span>Alvernia University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-133" role="option"><span class="select2-match"></span>Alverno College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-134" role="option"><span class="select2-match"></span>Amberton University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-135" role="option"><span class="select2-match"></span>American Academy of Art</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-136" role="option"><span class="select2-match"></span>American Indian College of the Assemblies of God</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-137" role="option"><span class="select2-match"></span>American InterContinental University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-138" role="option"><span class="select2-match"></span>American International College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-139" role="option"><span class="select2-match"></span>American Jewish University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-140" role="option"><span class="select2-match"></span>American Public University System</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-141" role="option"><span class="select2-match"></span>American University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-142" role="option"><span class="select2-match"></span>American University in Bulgaria</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-143" role="option"><span class="select2-match"></span>American University in Cairo</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-144" role="option"><span class="select2-match"></span>American University of Beirut</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-145" role="option"><span class="select2-match"></span>American University of Paris</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-146" role="option"><span class="select2-match"></span>American University of Puerto Rico</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-147" role="option"><span class="select2-match"></span>Amherst College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-148" role="option"><span class="select2-match"></span>Amridge University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-149" role="option"><span class="select2-match"></span>Anderson University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-150" role="option"><span class="select2-match"></span>Andrews University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-151" role="option"><span class="select2-match"></span>Angelo State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-152" role="option"><span class="select2-match"></span>Anna Maria College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-153" role="option"><span class="select2-match"></span>Antioch University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-154" role="option"><span class="select2-match"></span>Appalachian Bible College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-155" role="option"><span class="select2-match"></span>Aquinas College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-156" role="option"><span class="select2-match"></span>Arcadia University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-157" role="option"><span class="select2-match"></span>Argosy University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-158" role="option"><span class="select2-match"></span>Arizona Christian University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-159" role="option"><span class="select2-match"></span>Arizona State University - West</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-160" role="option"><span class="select2-match"></span>Arkansas Baptist College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-161" role="option"><span class="select2-match"></span>Arkansas Tech University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-162" role="option"><span class="select2-match"></span>Armstrong Atlantic State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-163" role="option"><span class="select2-match"></span>Art Academy of Cincinnati</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-164" role="option"><span class="select2-match"></span>Art Center College of Design</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-165" role="option"><span class="select2-match"></span>Art Institute of Atlanta</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-166" role="option"><span class="select2-match"></span>Art Institute of Colorado</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-167" role="option"><span class="select2-match"></span>Art Institute of Houston</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-168" role="option"><span class="select2-match"></span>Art Institute of Pittsburgh</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-169" role="option"><span class="select2-match"></span>Art Institute of Portland</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-170" role="option"><span class="select2-match"></span>Art Institute of Seattle</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-171" role="option"><span class="select2-match"></span>Asbury University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-172" role="option"><span class="select2-match"></span>Ashford University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-173" role="option"><span class="select2-match"></span>Ashland University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-174" role="option"><span class="select2-match"></span>Assumption College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-175" role="option"><span class="select2-match"></span>Athens State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-176" role="option"><span class="select2-match"></span>Auburn University - Montgomery</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-177" role="option"><span class="select2-match"></span>Augsburg College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-178" role="option"><span class="select2-match"></span>Augustana College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-179" role="option"><span class="select2-match"></span>Aurora University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-180" role="option"><span class="select2-match"></span>Austin College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-181" role="option"><span class="select2-match"></span>Alcorn State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-182" role="option"><span class="select2-match"></span>Ave Maria University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-183" role="option"><span class="select2-match"></span>Averett University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-184" role="option"><span class="select2-match"></span>Avila University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-185" role="option"><span class="select2-match"></span>Azusa Pacific University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-186" role="option"><span class="select2-match"></span>Babson College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-187" role="option"><span class="select2-match"></span>Bacone College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-188" role="option"><span class="select2-match"></span>Baker College of Flint</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-189" role="option"><span class="select2-match"></span>Baker University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-190" role="option"><span class="select2-match"></span>Baldwin Wallace University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-191" role="option"><span class="select2-match"></span>Christian Brothers University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-192" role="option"><span class="select2-match"></span>Abilene Christian University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-193" role="option"><span class="select2-match"></span>Arizona State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-194" role="option"><span class="select2-match"></span>Auburn University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-195" role="option"><span class="select2-match"></span>Alabama A&amp;M University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-196" role="option"><span class="select2-match"></span>Alabama State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-197" role="option"><span class="select2-match"></span>Arkansas State University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-198" role="option"><span class="select2-match"></span>Baptist Bible College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-199" role="option"><span class="select2-match"></span>Baptist Bible College and Seminary</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-200" role="option"><span class="select2-match"></span>Baptist College of Florida</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-201" role="option"><span class="select2-match"></span>Baptist Memorial College of Health Sciences</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-202" role="option"><span class="select2-match"></span>Baptist Missionary Association Theological Seminary</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-203" role="option"><span class="select2-match"></span>Bard College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-204" role="option"><span class="select2-match"></span>Bard College at Simon's Rock</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-205" role="option"><span class="select2-match"></span>Barnard College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-206" role="option"><span class="select2-match"></span>Barry University</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-207" role="option"><span class="select2-match"></span>Barton College</div></li><li class="select2-results-dept-0 select2-result select2-result-selectable" role="option" aria-selected="false" id=""><div class="select2-result-label" id="select2-result-label-208" role="option"><span class="select2-match"></span>Bastyr University</div></li><li class="select2-more-results" role="option">Loading more results…</li></ul>
#! ^ ! ^ ! ^ ! ^ !
#! search for <ul> HTML element with attribute role and value "listbox" as a listbox is JS...  hence dynamic && pretty sure you can confirm this be checking if it's hidden!!!



