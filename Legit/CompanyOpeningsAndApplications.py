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




#!!!!!!!!!!!!!!!!!!!!!!!!
# TODO
# Make a method called stamp_variable() that before going to the next iteration in the index applies the 'status' key-value input to self.current_jobs_details!!!
# Unicode - these give me ERRORS; figure out a way to either fix this or bypass it!!
    # Ex) <span class="s1">💰</span>
# Add lookout for 'Secret' keywords!!  (Ex. Top Secret Clearance, Secret Clearance, etc.)
#!!!!!!!!!!!!!!!!!!!!!!!!


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
        self.prior_experience_keywords = ["senior", "sr", "principal", "lead", "manager"]
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
        
        self.website_elements_relative_path = r'Legit/website_elements.json'
        
        
        #TODO: FIGURE THIS OUT FIGURE THIS OUT
        self.companys_every_job_detail = {}
        #TODO: FIGURE THIS OUT FIGURE THIS OUT
    
    
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
    

    def company_workflow(self, incoming_link):
        # sourcery skip: remove-redundant-pass
        print("\ncompany_workflow()")
        #! self.current_url HERE AND ONLY HERE is different becuase this link comes from google_search_results!!!!!
        if isinstance(incoming_link, list):
            self.current_url = incoming_link[0]
            self.list_of_links = incoming_link.copy()
        elif isinstance(incoming_link, str):
            self.current_url = incoming_link
            self.list_of_links.append(incoming_link)

        self.determine_application_company_name()
        webpage_num = self.determine_current_page(self.current_url)
        if webpage_num == 0:
            self.companys_internal_job_openings_URL = self.current_url
        else:
            self.is_internal_job_openings_URL_present(self.current_url)

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
                print("   >Internal-Job-Listings<")
                #TODO: change webpage --> self.companys_internal_job_openings_URL
                    #??? What if already on this page??? Like what if it is the initial link!?!?!?
                if self.browser.current_url != self.companys_internal_job_openings_URL:
                    self.change_page(self.companys_internal_job_openings_URL)
                self.soup_elements['soup'] = self.apply_beautifulsoup(self.current_url, "lxml")
                list_of_job_urls = self.collect_companies_current_job_openings(self.soup_elements['soup'])
                self.update_list_of_links(list_of_job_urls)
                self.filter_list_of_links()
                self.change_page(link)
            
            #TODO: FIGURE THIS FLOW OUT!!!!
            self.reset_webpages_soup_elements()
            if self.job_application_webpage[webpage_num] == "Job-Description":
                print("   >Job-Description<")
                webpage_num = self.analyze_job_suitabililty()
                # Did this because if determine_current_page() returns 2 it cant be accessed and the while will just skip to the next link!
                if self.job_application_webpage[webpage_num] == "Job-Application":
                    print("   >Job-Application<")
                    webpage_num = self.apply_to_job()
                if self.job_application_webpage[webpage_num] == "Submitted-Application":
                    print("   >Submitted-Application<")
                    self.confirmation_webpage_proves_application_submitted()
                    webpage_num = 1
            else:
                print("   >I honestly don't know how to even get here<")
                self.reset_every_job_variable()
                webpage_num = 1
                
            index += 1
        return print("--------------------------------------------\nTransferring power to JobSearchWorkflow")
    
    
    
    #print("\n()")
#!======= company_workflow variables ==========
    def determine_application_company_name(self):
        print("\ndetermine_application_company_name()")
        #self.set_current_url()
        
        if "jobs.lever.co" in self.current_url:
            self.application_company_name = "lever"
        elif "boards.greenhouse.io" in self.current_url:
            self.application_company_name = "greenhouse"
        else:
            print("Neither 'lever' nor 'greenhouse' ssooo...   idk")

    #TODO: add variable => self.soup_elements
    def apply_beautifulsoup(self, job_link, parser):
        print("\napply_beautifulsoup()")
        if parser == "lxml":
            result = requests.get(job_link)
            content = result.text
            soup = BeautifulSoup(content, "lxml")
        elif parser == "html":
            page = requests.get(job_link)
            result = page.content
            soup = BeautifulSoup(result, "html.parser")
            
        # Convert the soup object to a string and handle encoding issues
        return soup

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
#TODO TODO   FIX
#!===== companys_internal_job_openings_URL =====
    def url_parser(self, url):
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
    
    def try_adjusting_this_link(self, adjust_this_link):
        print(f"\ntry_adjusting_this_link()")
        if self.application_company_name == 'lever':
            adjusting_link = adjust_this_link.find('jobs.lever.co/') + len('jobs.lever.co/')
            still_adjusting = adjust_this_link.find('/', adjusting_link) + 1
            link_adjusted = adjust_this_link[:still_adjusting]
            adjust_this_link = link_adjusted
        if self.application_company_name == 'greenhouse':
            adjusting_link = adjust_this_link.find('greenhouse.io/') + len('greenhouse.io/')
            still_adjusting = adjust_this_link.find('/', adjusting_link) + 1
            link_adjusted = adjust_this_link[:still_adjusting]
            adjust_this_link = link_adjusted
        #time.sleep(1)
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
            print("self.list_of_links is empty!")
            return
        self.list_of_links = self.remove_allocated_links()
        self.list_of_links = self.JobSearchWorkflow_instance.filter_out_jobs_user_previously_applied_to(self.list_of_links, self.JobSearchWorkflow_instance.previously_applied_to_job_links)

    def remove_duplicates_from_list(self, list_to_filter):
        print("\nremove_duplicates()")
        return list(dict.fromkeys(list_to_filter))
    
    def remove_allocated_links(self):
        print("\nremove_allocated_links()")
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

    def users_basic_requirements_job_title(self, job_title):
        print("\nusers_basic_requirements_job_title()")
        return any(desired_job in job_title for desired_job in self.users_job_search_requirements['user_desired_job_titles'])
                    #TODO: ^ Check and see if these need to switched!?!?
    
    def get_experience_level(self, job_title):
        print("\nget_experience_level()")
        for experience_keyword in self.prior_experience_keywords:
            if experience_keyword in job_title:
                return experience_keyword
    
    def check_users_basic_requirements(self, job_title, job_location, job_workplaceType):
        print("\ncheck_users_basic_requirements()")
        
        print(f"self.current_jobs_details = {self.current_jobs_details}\n")
        print(f"job_title = {job_title}\njob_location = {job_location}\njob_workplaceType = {job_workplaceType}\n\n")
        
        if self.users_job_search_requirements['entry_level'] == True and self.users_basic_requirements_experience_level(job_title) == False:
            return False
        if self.user_basic_requirements_location_workplaceType(job_location, job_workplaceType):
            return False
        return True

    def users_basic_requirements_experience_level(self, job_title):
        print("\nusers_basic_requirements_experience_level()")
        print(any(experience_keyword in job_title for experience_keyword in self.prior_experience_keywords))
        return any(experience_keyword in job_title for experience_keyword in self.prior_experience_keywords)

    def user_basic_requirements_location_workplaceType(self, job_location, job_workplaceType):
        print("\nuser_basic_requirements_location_workplaceType()")
        if not job_location or job_location.lower().country() not in self.users_job_search_requirements['user_preferred_locations']:
            return False
        if job_location not in self.users_job_search_requirements['user_preferred_locations']:
            return False
        if not job_workplaceType or job_workplaceType.lower() == "unknown":
            return False
        if job_workplaceType.lower() == 'in-office with occasional remote':
            if 'in-office' in self.users_job_search_requirements['user_preferred_workplaceType'] or 'remote' in self.users_job_search_requirements['user_preferred_workplaceType']:
                return True
            else:
                return False
        if job_workplaceType.lower() == 'hybrid with rare in-office':
            if 'hybrid' in self.users_job_search_requirements['user_preferred_workplaceType'] or 'remote' in self.users_job_search_requirements['user_preferred_workplaceType']:
                return True
            else:
                return False
        if job_workplaceType.lower() == 'remote':
            return True
        if job_workplaceType.lower() == 'hybrid':
            if 'hybrid' in self.users_job_search_requirements['user_preferred_workplaceType'] and 'in-office' in self.users_job_search_requirements['user_preferred_workplaceType']:
                return True
            else:
                return False
        if job_workplaceType.lower() == 'in-office':
            if 'in-office' in self.users_job_search_requirements['user_preferred_workplaceType']:
                return True
            else:
                return False
        print("The dogs are acting strange")
        return False
#!==============================================







    # print(f"------\n {}\n------")
    #TODO: Please get rid of -> (self, job_link) ? 
    def determine_current_page(self, job_link):
        print("\ndetermine_current_page()")
        print(f" job_link = {job_link}")
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
            return self.application_company_name, job_link
        elif self.application_company_name == "greenhouse":
            div_main = soup.find("div", id="main")
            print(f"------ div_main:\n {div_main}\n------")
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
            return self.application_company_name, job_link
        print("2 possibilities for how the heck we ended up here:")
        print("\tOPTION 1) This webpage is neither a lever nor a greenhouse <best case scenario>")
        print("\tOPTION 1+1) The Plymouth Conjecture!")
        return
    
    #!=========== Internal-Job-Listings ============
    def get_absolute_url(self, url1, url2):
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
    
    #NOTE: Maybe you can do a while loop as confirmation and setting variables!! Like in job_description_webpage_navigation()
    #NOTE: OR...  or 2 methods with whiles where the 1st methods' while checks and confirms variables and the 2nd methods' while sets variables if present -> exactly like in job_description_webpage_navigation()!!! (The 2nd method can utilize the next_elem thing!?)
    #! GET RID OF ALL --- filter by requirements --- {except for get_experience_level()}
    #? JK JK  "if self.users_basic_requirements_job_title(job_title) == False:" just checks if job_title matches users_job_title!! {This checks and confirms user should not add 'accountant' job details to current_jobs_details!!!}
        #! THIS METHOD IS ALL ABOUT COLLECTING ALL MATCHING job_title STRINGS !!REGARDLESS!! OF EXPERIENCE!!!!
        #! CHECK ALL THAT STUFF AFTER THIS METHOD -> IF THEY FIT ADD current_jobs_details TO  
            #! total_company_jobs_available  <= add all 
            #! possibly_qualified_for_jobs   <= 
            #! jobs_applied_to_this_session  <= submitted application
    def collect_companies_current_job_openings(self, soup):
        print("\ncollect_companies_current_job_openings()")
        current_url = self.browser.current_url
        list_of_job_urls = []
        if self.application_company_name == 'lever':
            self.soup_elements["postings_wrapper"] = soup.find('div', class_="postings-wrapper")
            self.soup_elements["postings_groups"] = self.soup_elements["postings_wrapper"].find_all('div', class_="postings-group")
            for postings_group in self.soup_elements["postings_groups"]:
                # Extracting large-category-header if present
                #TODO - company_department[Design]
                department = postings_group.find('div', class_="large-category-header")
                if department:
                    print("Large Category Header:", department.text)
                # Extracting posting-category-title if present
                #TODO - company_department[App-Design]
                specialization = postings_group.find('div', class_="posting-category-title large-category-label")
                if specialization:
                    print("Posting Category Title:", specialization.text)

                # Extracting all posting elements
                postings = postings_group.find_all('div', class_="posting")
                for posting in postings:
                    # Confirming the 'Apply' button
                    #TODO: Pick one!
                    # job_opening_href = apply_button
                    apply_button = posting.find('a', text='Apply')
                    if apply_button:
                        print("Apply Button URL:", apply_button['href'])

                    # Finding the title button and extracting job title
                    #TODO: Pick one!
                    # button_to_job_description = title_button
                    title_button = posting.find('a', class_="posting-title")
                    if title_button:
                        job_title = title_button.find('h5', {'data-qa': 'posting-name'}).get_text().strip()
                        if self.users_basic_requirements_job_title(job_title) == False:
                            continue
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

                    if self.check_users_basic_requirements(job_title, job_location, job_workplaceType):
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
                        if not experience_level:
                            list_of_job_urls.append(job_url)
                    self.print_companies_internal_job_opening("company_job_openings", self.application_company_name, JobTitle=job_title, JobLocation=job_location, WorkPlaceTypes=job_workplaceType, CompanyDepartment=company_department, JobTeamInCompany=specialization, JobHREF=job_url, ButtonToJob=apply_href)
        elif self.application_company_name == 'greenhouse':
            div_main = soup.find("div", id="main")
            #NOTE: The lambda function takes x as an argument, where x is the value of the class_ attribute for a given <section> tag!!!
            sections = div_main.find_all('section', class_=lambda x: x and 'level' in x)
            for section in sections:
                if section.name == 'h3':
                    company_department = section.text
                if section.name == 'h4':
                    pass
                if job_opening := section.find('div', {'class': 'opening'}):
                    job_opening_href = job_opening.find('a')
                    button_to_job_description = job_opening_href
                    if job_opening_href:
                        job_title = job_opening_href.text
                        if self.users_basic_requirements_job_title(job_title) == False:
                            continue
                        experience_level = self.get_experience_level(job_title)
                        job_url = self.construct_url_to_job(current_url, job_opening_href)
                        span_tag_location = job_opening.find('span', {'class', 'location'})
                        job_location = span_tag_location.text if span_tag_location else None
                if self.check_users_basic_requirements(job_title, job_location, job_workplaceType):
                    self.current_jobs_details.update({
                        'job_url': job_url,
                        'job_title': job_title,
                        'experience_level': experience_level,
                        'job_location': job_location,
                        'job_workplaceType': job_workplaceType
                    })
                    if not experience_level:
                        list_of_job_urls.append(job_url)
                self.print_companies_internal_job_opening("company_job_openings", self.application_company_name, JobTitle=job_title, JobLocation=job_location, ButtonToJob=button_to_job_description)
        return list_of_job_urls

    #TODO: def print_companys_internal_job_opening(self, *args, **kwargs):
    def print_companies_internal_job_opening(self, *args, **kwargs):
        print('\n\n\n')
        print('----------------------------------------------------------------------------------------------------')
        print("print_company_job_openings()")
        method_name = None
        for arg in args:
            if arg == 'greenhouse':
                print(method_name)
                print(arg)
                for key, value in kwargs.items():
                    print(key + ": " + str(value))
            elif arg == 'lever':
                print(method_name)
                print(arg)
                for key, value in kwargs.items():
                    print(key + ": " + str(value))
            else:
                method_name = arg
        print('----------------------------------------------------------------------------------------------------')
        print('\n\n\n')
    #!==============================================
    
    #!============= Job-Description ================
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
        print(f"content = \n{self.soup_elements['content'].get_text()}\n")
        #job_fits_users_criteria = self.fits_users_criteria()
        job_fits_users_criteria = self.check_users_basic_requirements(self.current_jobs_details['job_title'], self.current_jobs_details['job_location'], self.current_jobs_details['job_workplaceType'])
        print(f"user_fits_jobs_criteria = {user_fits_jobs_criteria}\njob_fits_users_criteria = {job_fits_users_criteria}")
        if user_fits_jobs_criteria and job_fits_users_criteria:
            print("User is applying to this job!!")
            #TODO: Refactor this  v  by making a method called ?transfer_webpages() => {self.bottom_has_application_or_button() | self.click_this_button_or_scroll() | self.change_webpage()}?
            self.bottom_has_application_or_button(self.application_company_name)
            return 2
        else:
            print("\tHmmm that's weird ? it's neither button nor application")
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
    
    "Internal-Job-Listings", "Job-Description", "Job-Application", "Submitted-Application"
    
    #TODO: Confirm this & maybe just get these with soup?!?!?!
    # "greenhouse" = soup.find("div", id="main")
    #   "lever"    = soup.find('body')
    #TODO:              ^ body doesn't need attrName-attrVal in JSON plus we ONLY NEED the 1st OCCURANCE!!!
    #NOTE: "lever" -> logo element = <a>{aka: button too} + <a href=''> + logo{duhh}
    
    
    
    def fetch_and_fill_variables(self, job_application_webpage, parser):
        self.soup_elements['soup'] = self.apply_beautifulsoup(self.current_url, parser)
        self.process_webpage(job_application_webpage, self.soup_elements['soup'])
        self.print_soup_elements()
        
    def print_soup_elements(self):
        print("soup_elements = {")
        for key, value in self.soup_elements.items():
            print(f"    {key}: {value},\n")
        print("}")
    
    
    #Welcome to the Holy Land my child... we've been waiting for you
    #!======= Blueprints to Navigate Webpage =======
    #*These 3 methods deal with getting the json file stuff!!
    def get_website_data(self):
        with open(self.website_elements_relative_path) as websites_data_json_file:
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

        #print(f"{elements}")
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
                next_elem = next_elem.find_next()
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
                        #self.browser.execute_script("arguments[0].scrollIntoView();", resume_file_input)
            #resume_upload_button = self.browser.find_element(By.CSS_SELECTOR, 'button.visible-resume-upload')
            #resume_upload_button = self.browser.find_element(By.CSS_SELECTOR, 'button[aria-describedby="resume-allowable-file-types"]')
            wait = WebDriverWait(self.browser, 10)
            #overlay_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.close-overlay')))
            #overlay_close_button.click()
            resume_upload_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-describedby="resume-allowable-file-types"]')))
            print("--------------------------------------------------------")
            print(resume_upload_button)
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
                    print(sauce)
                    return sauce
            element = element.parent
            current_level += 1

    def get_div_parent(self, input_element):
        parent_element = input_element.find_previous(lambda tag: any('question' in class_name for class_name in tag.get('class', [])))
        if parent_element:
            current_element = parent_element.next_element
            while current_element:
                if isinstance(current_element, NavigableString) and current_element.strip():
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
        print("URL = " + url)
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
                print("SWEET ODIN'S RAVEN ITS A checkbox A... A checkbox I SAY... GOSH DARN YOU LISTEN TO ME ITS A checkbox!!!")
                print("also the .get_label() appeared to work and has been returne Woodstock man animal...     Korny poo's ewww")
                print("checkbox_values = ", checkbox_values)
                div_parent = checkbox_values[0]
                print("div_parent = ", div_parent)
                parents_text = checkbox_values[1]
                print("parents_text = ", parents_text)
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
        print("Tyrants")
        time.sleep(6)
        self.print_form_details(form_input_details)
        return form_input_details
    
    #TODO: Ummm I don't even know where to start
    def print_form_details(self, form_inputs):
        print('\n\n\n')
        jam = "10"
            
        if jam == "1":
            print('--------------------------------------------')
            print("Form Input Details: ", end="")
            for i, detail in enumerate(form_inputs, start=1):
                print(f"Input {i}:")
                print(f"  Label: {detail['label']}")
                print(f"  Type: {detail['type']}")
                print(f"  Values: {detail['values']}")
                print(f"  Is Hidden: {detail['is_hidden']}")
                print(f"  HTML: {detail['html']}")
            print('--------------------------------------------')
            print("\n")
            
        else:
            print('--------------------------------------------')
            print("Form Input Details: ", end="")
            for i, detail in enumerate(form_inputs, start=1):
                print(f"Input {i}:")
                print(f"  Label: {detail['label']}")
                print(f"  Type: {detail['type']}")
                print(f"  Values: {detail['values']}")
                print(f"  Is Hidden: {detail['is_hidden']}")
                print(f"  HTML: {detail['html']}")
                print(f"  Dynamic: {detail['dynamic']}")
                print(f"  Related Elements: {detail['related_elements']}")
            print('--------------------------------------------')
            print("\n")        
        

    
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
            else:
                raise ValueError('The element does not have an id or a class')

            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

        return elemental
    #TODO: ^ ^ ^ ^ v v v v These are literally exactly the same nerd!
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
            else:
                raise ValueError('The element does not have an id or a class')

            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

            self.browser.execute_script("arguments[0].scrollIntoView();", elemental)


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
    def process_form_inputs(self, form_input_details):
        print("\nprocess_form_inputs()")
        self.init_form_input_extended()

        # self.nlp_load()
        # print("nlp loaded... ")

        #print("self.form_input_details: ", end="")
        #print(self.form_input_details)
        #print("form_input_details: ", form_input_details)
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
                print("  form_input_details = ", input_data)
                if input_data['is_hidden']:
                    continue



                #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
                #       iMac Computer needed this for testing!!!
                # if i == [1, 2, 3, 4, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]:
                #     self.form_input_extended['bc_nick_said'] == True
                #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|




                # print("This is -> is None")         |       print("This is -> == None")         =>       print("This is -> None or empty")
                # if input_data['label'] is None:     |       if input_data['label'] == None:     =>       if not input_data['label']:
                #     print("Dang so -> is None")     |           print("Dang so -> == None")     =>           print("Dang so -> is None or empty")
                #     continue                        |           continue                        =>           continue


                #! THIS HAS TO BE 1st!!!!!!!!!  b/c if it's None or 'empty'(null) then all the other tests give erros when comparring!!
                print("This is -> None or empty")
                #Basically checks for None and empty!!
                if not input_data['label'] or input_data['label'] is None:
                    print("Dang so -> is None or empty")
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
                    print("input_data: ", input_data)
                    remove_attachment = input_data
                    print("remove_attachment: ", remove_attachment)
                    continue


                if 'Resume/CV' in input_data['label']:
                    print("Resume/CV: (a file)")
                    print("input_data: ", input_data)
                    resume_attachment = input_data
                    print("resume_attachment: ", resume_attachment)
                    continue


                if 'Submit Application' in input_data['label']:
                    print("Submit Application")
                    print("input_data: ", input_data)
                    submit_button = input_data
                    print("submit_button: ", submit_button)
                    continue
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


                self.scroll_to_question(input_data['html'])
                #self.scroll_to_element(input_data)
                print("  Scrolled here I guess...\n")
                print("self.form_input_extended = ", self.form_input_extended)
                time.sleep(3)

                label = input_data['label']
                print("unprocessed label: ", label)
                label = self.process_text(label)
                print("processed label: ", label)
                input_type = input_data['type']
                predefined_options = input_data.get('values', None)
                print("predefined_options = ", predefined_options)

                # If the input type in select, radio, or checkbox, handle it as a !special case!
                print("\n_____________________________________________________________________________________")
                print("TIME FOR COMPARISONS! DO YOU HEAR THAT BUTT-HEAD!!! WE ARE GONNA BE COMPARING BUTTS!!")
                if input_type in ['select', 'radio', 'checkbox']:
                    print("Ahhhhhhh yes it is either one of these: 'select', 'radio', 'checkbox'")
                    matching_keys = self.get_matching_keys(label)               #! .get_matching_keys() does all the comaparing to get the right answer!!!!! ssooo there do   special case check -> .env chack -> long q>a ... a>a check!!!
                    if matching_keys:
                        #!HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE
                        print("self.form_input_extended = ", self.form_input_extended)
                        for key in matching_keys:

                            answer = self.users_information[{key}]
                            print("answer = ", answer)
                            if answer in predefined_options:
                                # Input the answer into the form
                                print(f"Entering '{answer}' for '{label}'")
                            else:
                                print(f"Stored answer '{answer}' is not a valid option for '{label}'")
                    else:
                        print(f"No stored answers found for '{label}'")

                else:
                    print("This one ain't special... this one ain't even intelligent... dumb ol' question any how")
                    matching_keys = self.try_finding_match(label)
                    print("matching_keys = ", matching_keys)
                    #! MAYBE HERE MAYBE HERE MAYBE MAYBE HERE MAYBE HERE MAYBE HERE
                    #self.form_input_extended['env_key'] = key
                    #self.form_input_extended['env_values'].append(self.users_information[key])
                    print("if matching_keys: ", end="")
                    print("True" if matching_keys else "False")
                    # if matching_keys:
                    #     for key in matching_keys:
                    if matching_keys:
                        print("self.form_input_extended['env_values'] = ", self.form_input_extended['env_values'])
                        for key in self.form_input_extended['env_values']:
                            print("key = ", key)
                            answer = self.users_information.get(key)
                            print("answer = ", answer)
                            # Input the answer into the form
                            print(f"Entering '{answer}' for '{label}'")
                            #self.fill_form(label, answer)
                    else:
                        context = self.q_and_a['summary'] + " " + label
                        answer = self.generate_response(context)
                        if answer:
                            # Input the answer into the form
                            print(f"Entering '{answer}' for '{label}'")
                            #self.fill_form(label, answer)
                        else:
                            print(f"No stored answers found for '{label}'")
                self.form_input_extended['env_html'] = self.extract_css(input_data['html'])

                self.print_form_input_extended()     ############################### HERE VON!!!

                self.fill_that_form()


            except BreakLoopException:
                print("You know what eff that job anyways! They probably suck and would've over worked you.")
                return


        self.submit_job_application(submit_button)
        print("ALL DONE!!! The job application has been completed Counselor Mackie...")
        print("Normally Counselor Mackie would recommend pushing the 'Submit Application' button right now!")
        time.sleep(2)
    
    
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
        #? These might work in case that one doesn't
        #for rule in self.custom_rules.keys():
        #for rule, value in self.custom_rules.items():
        #for rule, value in self.custom_rules:
        for rule in self.custom_rules:
            if label == rule:
                print("MATCH: [ try_finding_match() ]")
                print("\tCUSTOM_RULES = ", rule)
                print("\tlabel = ", label)
                #print("\t... value = ", value)
                print("\t... value = ", self.custom_rules[rule])
                return rule
            
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
    def process_text(self, text):
        print("process_text()")
        if "*" in text or "✱" in text:
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
                                #print("\t... value = ", self.users_information['{key}'])
                                return key
                
                
            # Check for synonyms
            #! WRONG ! sometimes I have 2 so get the root or something!!!
            #synonyms = self.get_synonyms(key)
            #synonyms = self.get_synonyms(label)
            
            
            #!-------------------------------------------------------------------------------------------------------------------------
            # for synonym in synonyms:
            #     doc2 = self.nlp(synonym.lower().replace("_", " "))
            #     print("-doc2(synonyms.index) = ", doc2)
            #     #similarity = doc1.similarity(doc2)
            #     similarity = doc2.similarity(doc1)
            #     print("similarity = ", similarity)
            #     print("key = ", key)
            #     print("synonyms = ", synonyms)
            #     if similarity > max_similarity:
            #         max_similarity = similarity
            #         best_match = key
            #         print("max_similarity = ", max_similarity)
            #         print("best_match = ", best_match)
                    
            #         if max_similarity == 1.0:
            #             self.form_input_extended['env_key'] = key
            #             self.form_input_extended['env_values'].append(self.users_information[key])
            #             print("MATCH: [ 2.2)find_best_match() -> .similarity(question{*label*} | synonyms.index)]")
            #             print("\tusers_information = ", key)
            #             print("\tlabel = ", label)
            #             print("\t... synonym = ", synonym)
            #             print("\t... value = ", self.users_information[key])
            #             #print("\t... value = ", self.users_information['{key}'])
            #             return key
            #!-------------------------------------------------------------------------------------------------------------------------
            
            
            print("\nusers_information + 1")
            
        print("max_similarity = ", max_similarity)
        print("best_match = ", best_match)
        print(best_match if max_similarity > 0.90 else None)
        return best_match if max_similarity > 0.90 else None
    
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






    def keep_jobs_applied_to_info(self):
        self.jobs_applied_to_this_session.append(self.current_jobs_details)
























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
















class BreakLoopException(Exception):
    pass
















# https://stackoverflow.com/questions/13897896/unexpected-keyword-argument-when-using-kwargs-in-constructor

    '''
    # def try_finding_internal_job_openings_URL
    def find_companys_internal_job_openings_URL(self):
        print("\nfind_companys_internal_job_openings_URL()")
        self.soup_elements['soup'] = self.apply_beautifulsoup(self.current_url, "lxml")
        self.search_for_internal_jobs_link()
        return 1
    '''

    '''
    # search_for_internal_job_openings_URL() == This method looks at Header && checks the banner for URL!
    def handle_job_description_webpage(self):
        print("\nhandle_job_description_webpage()")
        if self.application_company_name == "lever":
            company_open_positions = self.soup_elements['soup'].find('a', {"class": "main-header-logo"})
            application_webpage_html = self.soup_elements['soup'].find("div", {"class": "application-page"})
            if not self.companys_internal_job_openings_URL:
                try:
                    self.lever_co_banner(self.soup_elements['webpage_body'], self.soup_elements['soup'])
                except:
                    raise ConnectionError("ERROR: Companies other open positions are not present")
            self.scroll_to_element(self.soup_elements['opening_link_description'])
            apply_to_job = self.should_user_apply(self.soup_elements['opening_link_description'])
            if apply_to_job:
                print("User is applying to this lever.co job!!")
                self.bottom_has_application_or_button(self.application_company_name)
                time.sleep(3)
                current_url = self.browser.current_url
                self.soup_elements['soup'] = self.apply_beautifulsoup(current_url, "html")
                self.form_input_details = self.get_form_input_details(current_url)
                self.insert_resume()
                self.process_form_inputs(self.form_input_details)
            else:
                print("\tHmmm that's weird ? it's neither button nor application")
        elif self.application_company_name == "greenhouse":
            if not self.companys_internal_job_openings_URL:
                try:
                    self.greenhouse_io_banner(self.soup_elements['app_body'], self.soup_elements['header'], self.soup_elements['content'])
                except:
                    raise ConnectionError("ERROR: Companies other open positions are not present")
            self.scroll_to_element(self.soup_elements['content'])
            current_url = self.browser.current_url
            should_apply = self
    '''

    '''
    #! "lever" is ONLY searching for "Internal-Job-Listings" URL
    #! "greenhouse" is doing that and getting all the basic job info!(Consider it like the title or header)
    #Click <a> elements | collect all links
    def search_for_internal_jobs_link(self):
        print("\nsearch_for_internal_jobs_link()")
        #made from methods --> lever_co_header()
        if self.application_company_name == "lever":
            links_in_header = []
            current_url = self.browser.current_url
            links_in_header.append(current_url)
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
            return

        elif self.application_company_name == "greenhouse":
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
                if child.name == "h1" and "app-title" in child.get("class"):
                    self.current_jobs_details["job_title"] = child.get_text().strip()
                elif child.name == "span" and  "company-name" in child.get("class"):
                    self.current_jobs_details["company_name"] = child.get_text().strip()
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
                elif child.name == "div" and "location" in child.get("class"):
                    self.current_jobs_details["job_location"] = child.get_text().strip()
            if company_other_openings_href == None:
                self.print_companies_internal_job_opening("greenhouse_io_banner()", "greenhouse", JobTitle=self.current_jobs_details["job_title"], CompayName=self.current_jobs_details["company_name"], JobLocation=self.current_jobs_details["job_location"], JobHREF="Couldnt Find", LinkToApplication_OnPageID=a_fragment_identifier)
            else:
                self.print_companies_internal_job_opening("greenhouse_io_banner()", "greenhouse", JobTitle=self.current_jobs_details["job_title"], CompayName=self.current_jobs_details["company_name"], JobLocation=self.current_jobs_details["job_location"], JobHREF=company_other_openings_href, LinkToApplication_OnPageID=a_fragment_identifier)
            return
    '''

    '''
    #NOTE: Only the internal job openings webpage will have a filter dropdown!! So maybe use that!
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
    '''



    '''
    def try_adjusting_this_link(self, adjust_this_link):
        if self.application_company_name == 'lever':
            adjusting_link = adjust_this_link.find('jobs.lever.co/') + len('jobs.lever.co/')
            still_adjusting = adjust_this_link.find('/', adjusting_link) + 1
            link_adjusted = adjust_this_link[:still_adjusting]
            adjust_this_link = link_adjusted
        if self.application_company_name == 'greenhouse':
            adjusting_link = adjust_this_link.find('greenhouse.io/') + len('greenhouse.io/')
            still_adjusting = adjust_this_link.find('/', adjusting_link) + 1
            link_adjusted = adjust_this_link[:still_adjusting]
            adjust_this_link = link_adjusted
        time.sleep(2)
        return adjust_this_link
    '''

    '''
    def construct_url_to_job(self, current_url, job_opening_href):
        button_to_job_description = job_opening_href
        job_link = job_opening_href.get('href')
        domain_name = self.try_adjusting_this_link(current_url)
        job_path = job_opening_href.get('href')
        job_url = domain_name + job_path
        return job_url
    '''
    
    
    
    
    '''
        "lever": {
        "Internal-Job-Listings": {
            "elements": {
                "postings_wrapper": [
                    {"tag": "div", "class_": "postings-wrapper"}
                ],
                "postings_groups": [
                    {"tag": "div", "class_": "postings-group"}
                ],
                "postings": [
                    {"tag": "div", "class_": "posting"}
                ],
                "posting_categories": [
                    {"tag": "div", "class_": "posting-categories"}
                ]
            },
            "data": {
                "html_department": [
                    {"tag": "div", "class_": "large-category-header"}
                ],
                "html_specialization": [
                    {"tag": "div", "class_": "posting-category-title"}
                ],
                "html_department_specialization": [
                    {"tag": "span", "class": "department"}
                ],
                "html_job_opening_href": [
                    {"tag": "div", "class": "posting-apply"},
                    {"tag": "a", "text": "Apply"}
                ],
                "html_button_to_job_description": [
                    {"tag": "a", "class": "posting-title"}
                ],
                "html_job_title": [
                    {"tag": "h5", "data-qa": "posting-name"},
                    {"tag": "h5"}
                ],
                "html_job_location": [
                    #!!!!  THIS HAS THIS NAME FOR THE FILTER TAB AT THE TOP !!!!!
                    {"tag": "span", "class": "sort-by-location"},
                    {"tag": "span", "class_": "location"}
                ],
                "html_job_workplaceType": [
                    {"tag": "span", "class": "workplaceType"},
                    {"tag": "span", "class_": "workplaceTypes"}
                ]
            }
        },
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #TODO: Check out this code! Has cookies, CAPTCHA's, scripts!!! Lot's of good code!
    '''
<!DOCTYPE html>
<html>
    <head prefix="og: http://ogp.me/ns#">
        <meta content="IE=edge" http-equiv="X-UA-Compatible" />
        <meta charset="utf-8" />
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        <title>PhysicsX - Principal Product Designer</title>
        <meta name="twitter:card" value="summary" />
        <meta content="PhysicsX - Principal Product Designer" name="twitter:title" />
        <meta
            content="Introduction PhysicsX is a deep-tech company of scientists and engineers, developing machine learning applications to massively accelerate physics simulations and enable a new frontier of optimization opportunities in design and engineering. Born out of numerical physics and proven in Formula One, we help our customers radically improve their concepts and designs, transform their engineering processes and drive operational product performance. We do this in some of the most advanced and important industries of our time – including Space, Aerospace, Medical Devices, Additive Manufacturing, Electric Vehicles, Motorsport, and Renewables. Our work creates positive impact for society, be it by improving the design of artificial hearts, reducing CO2 emissions from aircraft and road vehicles, and increasing the performance of wind turbines. We are a rapidly growing and profitable company but prefer to fly under the radar to protect our customers’ confidentiality. We are about to take t"
            name="twitter:description"
        />
        <meta name="twitter:label1" value="Location" />
        <meta name="twitter:data1" value="Shoreditch, London" />
        <meta name="twitter:label2" value="Team" />
        <meta name="twitter:data2" value="Product" />
        <meta content="https://lever-client-logos.s3.us-west-2.amazonaws.com/7d94404d-aac8-47b9-9f74-94368b53a325-1673458529981.png" name="twitter:image" />
        <meta content="PhysicsX - Principal Product Designer" property="og:title" />
        <meta
            content="Introduction PhysicsX is a deep-tech company of scientists and engineers, developing machine learning applications to massively accelerate physics simulations and enable a new frontier of optimization opportunities in design and engineering. Born out of numerical physics and proven in Formula One, we help our customers radically improve their concepts and designs, transform their engineering processes and drive operational product performance. We do this in some of the most advanced and important industries of our time – including Space, Aerospace, Medical Devices, Additive Manufacturing, Electric Vehicles, Motorsport, and Renewables. Our work creates positive impact for society, be it by improving the design of artificial hearts, reducing CO2 emissions from aircraft and road vehicles, and increasing the performance of wind turbines. We are a rapidly growing and profitable company but prefer to fly under the radar to protect our customers’ confidentiality. We are about to take t"
            property="og:description"
        />
        <meta content="https://jobs.lever.co/physicsx.ai/9feadb59-31c1-4634-8998-032403030736" property="og:url" />
        <meta content="https://lever-client-logos.s3.us-west-2.amazonaws.com/7d94404d-aac8-47b9-9f74-94368b53a325-1673459191848.png" property="og:image" />
        <meta content="630" property="og:image:height" />
        <meta content="1200" property="og:image:width" />
    </head>
    <body class="show header-comfortable">
        <div class="page show">
            <div class="main-header page-full-width section-wrapper">
                <div class="main-header-content page-centered narrow-section page-full-width">
                    <a class="main-header-logo" href="https://jobs.lever.co/physicsx.ai"><img alt="PhysicsX logo" src="https://lever-client-logos.s3.us-west-2.amazonaws.com/7d94404d-aac8-47b9-9f74-94368b53a325-1673459176686.png" /></a>
                </div>
            </div>
        </div>
        <div class="content-wrapper posting-page">
            <div class="content">
                <div class="section-wrapper accent-section page-full-width">
                    <div class="section page-centered posting-header">
                        <div class="posting-headline">
                            <h2>Principal Product Designer</h2>
                            <div class="posting-categories">
                                <div class="sort-by-time posting-category medium-category-label location" href="#">Shoreditch, London /</div>
                                <div class="sort-by-team posting-category medium-category-label department" href="#">Product /</div>
                                <div class="sort-by-commitment posting-category medium-category-label commitment" href="#">Full-time</div>
                                <div class="sort-by-time posting-category medium-category-label workplaceTypes" href="#">/ Hybrid</div>
                            </div>
                        </div>
                        <div class="postings-btn-wrapper"><a class="postings-btn template-btn-submit shamrock" href="https://jobs.lever.co/physicsx.ai/9feadb59-31c1-4634-8998-032403030736/apply">Apply for this job</a></div>
                    </div>
                </div>
                <div class="section-wrapper page-full-width">
                    <div class="section page-centered" data-qa="job-description">
                        <div><b style="font-size: 12pt;">Introduction</b></div>
                        <div>
                            <span style="font-size: 12pt;">
                                PhysicsX is a deep-tech company of scientists and engineers, developing machine learning applications to massively accelerate physics simulations and enable a new frontier of optimization opportunities in
                                design and engineering.
                            </span>
                        </div>
                        <div><span style="font-size: 12pt;"></span></div>
                        <div>
                            <span style="font-size: 12pt;">
                                Born out of numerical physics and proven in Formula One, we help our customers radically improve their concepts and designs, transform their engineering processes and drive operational product performance. We
                                do this in some of the most advanced and important industries of our time – including Space, Aerospace, Medical Devices, Additive Manufacturing, Electric Vehicles, Motorsport, and Renewables. Our work creates
                                positive impact for society, be it by improving the design of artificial hearts, reducing CO2 emissions from aircraft and road vehicles, and increasing the performance of wind turbines.
                            </span>
                        </div>
                        <div><span style="font-size: 12pt;"></span></div>
                        <div>
                            <span style="font-size: 12pt;">
                                We are a rapidly growing and profitable company but prefer to fly under the radar to protect our customers’ confidentiality. We are about to take the next leap in building out our technology platform and
                                product offering. In this context, we are looking for a capable and enthusiastic software engineer to join our team. If all of this sounds exciting to you, we would love to talk (even if you don't tick all
                                the boxes).
                            </span>
                        </div>
                    </div>
                    <div class="section page-centered">
                        <div>
                            <h3>What you will do</h3>
                            <ul class="posting-requirements plain-list">
                                <ul>
                                    <li>Collaborate with cross-functional teams including product management, engineering, and user research to understand product requirements and identify design challenges</li>
                                    <li>Develop user flows, wireframes, prototypes, and high-fidelity mockups to effectively communicate product concepts</li>
                                    <li>Run usability studies, gather feedback from users, and iterate on designs</li>
                                    <li>Maintain and update style guides, design systems, and component libraries</li>
                                    <li>Work closely with engineers to ensure designs are implemented accurately in the final product</li>
                                    <li>Advocate for the end-user throughout the design process to ensure product utility and usability</li>
                                </ul>
                            </ul>
                        </div>
                    </div>
                    <div class="section page-centered">
                        <div>
                            <h3>What you bring to the table</h3>
                            <ul class="posting-requirements plain-list">
                                <ul>
                                    <li>Enthusiasm about building machine learning products for science and engineering</li>
                                    <li>Degree in Design, Human-Computer Interaction, or related fields</li>
                                    <li>7+ years’ experience in a product role, with exposure to:</li>
                                    <li>Proficiency in design tools such as Sketch, Figma, Adobe XD, or similar</li>
                                    <li>Strong understanding of user-centered design principles and methodologies</li>
                                    <li>Familiarity with design systems and creating scalable UI components</li>
                                    <li>Ability to create engaging and visually appealing designs</li>
                                    <li>Excellent communication and collaboration skills</li>
                                    <li>Experience with user research techniques and usability testing</li>
                                    <li>Knowledge of front-end development technologies and their impact on design is a plus</li>
                                    <li>Experience in data science / machine learning is a plus</li>
                                    <li>Experience in CAD/CFD/FEA is a plus</li>
                                    <li>Excellent collaboration and communication skills - with teams and users</li>
                                    <li>Passion and track record of mentoring and coaching more junior colleagues</li>
                                </ul>
                            </ul>
                        </div>
                    </div>
                    <div class="section page-centered">
                        <div>
                            <h3>What we offer</h3>
                            <ul class="posting-requirements plain-list">
                                <ul>
                                    <li>Be part of something larger: Make an impact and meaningfully shape an early-stage company. Work on some of the most exciting and important topics there are. Do something you can be proud of</li>
                                    <li>
                                        Work with a fun group of colleagues that support you, challenge you and help you grow. We come from many different backgrounds, but what we have in common is the desire to operate at the very top of
                                        our fields and solve truly challenging problems in science and engineering. If you are similarly capable, caring and driven, you'll find yourself at home here
                                    </li>
                                    <li>Experience a truly flat hierarchy. Voicing your ideas is not only welcome but encouraged, especially when they challenge the status quo</li>
                                    <li>Work sustainably, striking the right balance between work and personal life. Be able to properly switch off in the evening and during weekends. What matters is the quality of our work</li>
                                    <li>Receive a competitive compensation and equity package, in addition to plenty of perks such as generous vacation and parental leave, complimentary office food, as well as fun outings and events</li>
                                    <li>
                                        Work in a flexible setting, with your choice of either our lovely London Shoreditch or Bicester Heritage offices to collaborate in, and a good proportion from home if so desired. Get the opportunity
                                        to occasionally visit our customers' engineering sites and experience first-hand how our work is transforming their ways of working
                                    </li>
                                    <li>Use first-class equipment for working in-office or remotely, including HPC</li>
                                </ul>
                            </ul>
                        </div>
                    </div>
                    <!--[2022-11-28] [GOLD-2535] Remove payTransparencyV1 when feature flag is fully removed-->
                    <div class="section page-centered" data-qa="closing-description">
                        <div><b style="font-size: 12pt;">Our stance</b></div>
                        <div>
                            <span style="font-size: 12pt;">
                                We value diversity and are committed to equal employment opportunity regardless of sex, race, religion, ethnicity, nationality, disability, age, sexual orientation or gender identity. We strongly encourage
                                individuals from groups traditionally underrepresented in tech to apply. To help make a change, we sponsor bright women from disadvantaged backgrounds through their university degrees in science and
                                mathematics.
                            </span>
                        </div>
                    </div>
                    <div class="section page-centered last-section-apply" data-qa="btn-apply-bottom">
                        <a class="postings-btn template-btn-submit shamrock" data-qa="show-page-apply" href="https://jobs.lever.co/physicsx.ai/9feadb59-31c1-4634-8998-032403030736/apply">Apply for this job</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="main-footer page-full-width">
            <div class="main-footer-text page-centered">
                <p><a href="https://www.physicsx.ai/">PhysicsX Home Page</a></p>
                <a class="image-link" href="https://lever.co/"><span>Jobs powered by </span><img alt="Lever logo" src="/img/lever-logo-full.svg" /></a>
            </div>
        </div>
        <script type="application/ld+json">
            {
                "@context": "http://schema.org",
                "@type": "JobPosting",
                "title": "Principal Product Designer",
                "hiringOrganization": { "@type": "Organization", "name": "PhysicsX", "logo": "https://lever-client-logos.s3.us-west-2.amazonaws.com/7d94404d-aac8-47b9-9f74-94368b53a325-1673459176686.png" },
                "jobLocation": { "@type": "Place", "address": { "@type": "PostalAddress", "addressLocality": "Shoreditch, London", "addressRegion": null, "addressCountry": null, "postalCode": null } },
                "employmentType": "Full-time",
                "datePosted": "2023-08-02",
                "description": "<p><b style=\"font-size: 12pt\">Introduction</b></p><p><span style=\"font-size: 12pt\">PhysicsX is a deep-tech company of scientists and engineers, developing machine learning applications to massively accelerate physics simulations and enable a new frontier of optimization opportunities in design and engineering.&nbsp;</span></p><p><span style=\"font-size: 12pt\">&nbsp;</span></p><p><span style=\"font-size: 12pt\">Born out of numerical physics and proven in Formula One, we help our customers radically improve their concepts and designs, transform their engineering processes and drive operational product performance. We do this in some of the most advanced and important industries of our time – including Space, Aerospace, Medical Devices, Additive Manufacturing, Electric Vehicles, Motorsport, and Renewables. Our work creates positive impact for society, be it by improving the design of artificial hearts, reducing CO2 emissions from aircraft and road vehicles, and increasing the performance of wind turbines.&nbsp;&nbsp;</span></p><p><span style=\"font-size: 12pt\">&nbsp;</span></p><p><span style=\"font-size: 12pt\">We are a rapidly growing and profitable company but prefer to fly under the radar to protect our customers’ confidentiality. We are about to take the next leap in building out our technology platform and product offering. In this context, we are looking for a capable and enthusiastic software engineer to join our team. If all of this sounds exciting to you, we would love to talk (even if you don't tick all the boxes).</span></p>\\n<p><p><br></p><b>What you will do</b><ul><li>Collaborate with cross-functional teams including product management, engineering, and user research to understand product requirements and identify design challenges</li><li>Develop user flows, wireframes, prototypes, and high-fidelity mockups to effectively communicate product concepts</li><li>Run usability studies, gather feedback from users, and iterate on designs</li><li>Maintain and update style guides, design systems, and component libraries</li><li>Work closely with engineers to ensure designs are implemented accurately in the final product</li><li>Advocate for the end-user throughout the design process to ensure product utility and usability</li></ul><p><br></p><b>What you bring to the table</b><ul><li>Enthusiasm about building machine learning products for science and engineering</li><li>Degree in Design, Human-Computer Interaction, or related fields</li><li>7+ years’ experience in a product role, with exposure to:</li><li>Proficiency in design tools such as Sketch, Figma, Adobe XD, or similar</li><li>Strong understanding of user-centered design principles and methodologies</li><li>Familiarity with design systems and creating scalable UI components</li><li>Ability to create engaging and visually appealing designs</li><li>Excellent communication and collaboration skills</li><li>Experience with user research techniques and usability testing</li><li>Knowledge of front-end development technologies and their impact on design is a plus</li><li>Experience in data science / machine learning is a plus</li><li>Experience in CAD/CFD/FEA is a plus</li><li>Excellent collaboration and communication skills - with teams and users</li><li>Passion and track record of mentoring and coaching more junior colleagues</li></ul><p><br></p><b>What we offer</b><ul><li>Be part of something larger: Make an impact and meaningfully shape an early-stage company. Work on some of the most exciting and important topics there are. Do something you can be proud of</li><li>Work with a fun group of colleagues that support you, challenge you and help you grow. We come from many different backgrounds, but what we have in common is the desire to operate at the very top of our fields and solve truly challenging problems in science and engineering. If you are similarly capable, caring and driven, you'll find yourself at home here</li><li>Experience a truly flat hierarchy. Voicing your ideas is not only welcome but encouraged, especially when they challenge the status quo</li><li>Work sustainably, striking the right balance between work and personal life. Be able to properly switch off in the evening and during weekends. What matters is the quality of our work</li><li>Receive a competitive compensation and equity package, in addition to plenty of perks such as generous vacation and parental leave, complimentary office food, as well as fun outings and events&nbsp;</li><li>Work in a flexible setting, with your choice of either our lovely London Shoreditch or Bicester Heritage offices to collaborate in, and a good proportion from home if so desired. Get the opportunity to occasionally visit our customers' engineering sites and experience first-hand how our work is transforming their ways of working&nbsp;&nbsp;</li><li>Use first-class equipment for working in-office or remotely, including HPC</li></ul><p><br></p></p>\\n<p><b style=\"font-size: 12pt\">Our stance</b></p><p><span style=\"font-size: 12pt\">We value diversity and are committed to equal employment opportunity regardless of sex, race, religion, ethnicity, nationality, disability, age, sexual orientation or gender identity. We strongly encourage individuals from groups traditionally underrepresented in tech to apply. To help make a change, we sponsor bright women from disadvantaged backgrounds through their university degrees in science and mathematics. &nbsp;</span></p>"
            }
        </script>
        <script type="text/javascript">
            var subDomain = document.location.hostname;
            var rootDomain = subDomain.split(".").reverse().splice(0, 2).reverse().join(".");
            function removeCookie(cookieName) {
                document.cookie = cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=" + subDomain + ";";
                document.cookie = cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=" + rootDomain + ";";
            }
            var GA_COOKIES = ["_gid", "_ga", "_gat_customer"];
            GA_COOKIES.forEach(function (cookie) {
                removeCookie(cookie);
            });
        </script>
        <script data-apikey="6a247c6ff13012d02fde17377f0b857b" data-appversion="0.0.1690834621" data-endpoint="https://bugs.lever.co/js" data-releasestage="production" src="/js/bug-snag.js"></script>
        <script>
            var gaCode = "";
        </script>
        <script>
            var gaAllowLinker = false;
        </script>
        <script async="" src="https://www.googletagmanager.com/gtag/js?id="></script>
        <script>
            if (gaCode.startsWith("UA")) {
                window.initializeGoogleAnalytics = function () {
                    (function (i, s, o, g, r, a, m) {
                        i["GoogleAnalyticsObject"] = r;
                        (i[r] =
                            i[r] ||
                            function () {
                                (i[r].q = i[r].q || []).push(arguments);
                            }),
                            (i[r].l = 1 * new Date());
                        (a = s.createElement(o)), (m = s.getElementsByTagName(o)[0]);
                        a.async = 1;
                        a.src = g;
                        m.parentNode.insertBefore(a, m);
                    })(window, document, "script", "//www.google-analytics.com/analytics.js", "ga");
                    ga("create", gaCode, { name: "customer", allowLinker: gaAllowLinker });
                    ga("customer.send", "pageview");
                };
            } else {
                window.initializeGoogleAnalytics = function () {
                    window.dataLayer = window.dataLayer || [];
                    function gtag() {
                        dataLayer.push(arguments);
                    }
                    gtag("js", new Date());
                    gtag("config", gaCode);
                    if (gaAllowLinker) {
                        gtag("set", "linker", "lever.co");
                    }
                };
            }
        </script>
        <script type="text/javascript">
            /*We only want to not initialize Google Analytics and Segment on load if the following is true:- `gdpr` is enabled for the account- the account has the `cookieBanner` enabled- the account has the `optIn` cookieBanner typeThis is the only case where an applicant has to explicitly opt-in to the cookie consent before we can load GA/Segment*/
        </script>
        <script src="/js/cookieconsent.min.js"></script>
        <script>
            window.addEventListener("load", () => {
                window.cookieconsent.initialise({
                    enabled: true,
                    content: {
                        allow: "Accept",
                        deny: "Deny",
                        dismiss: "Dismiss",
                        message: "This website uses cookies to improve your web experience. By using the site, you agree to the use of cookies.",
                        link: " PhysicsX Cookie Policy",
                        href: "",
                        target: "_blank",
                    },
                    cookie: { path: "/physicsx.ai" },
                    type: "info",
                    layout: "lever-layout",
                    layouts: {
                        "lever-layout": `<div class="momentum-body"><div class="message message-inverse flex-column"><div class="icon">&#127850;</div><div class="message-buttons cc-desktop"><button class="button button-sm cc-btn cc-dismiss" href="#">Dismiss</button></div><h4 class='text-white'>Privacy Notice</h4><p>This website uses cookies to improve your web experience. By using the site, you agree to the use of cookies.</p><div class="self-end cc-mobile m1"><button class="button button-sm cc-btn cc-dismiss" href="#" >Dismiss</button></div></div></div>`,
                    },
                    showLink: false,
                    onInitialise: function (status) {
                        /* `onInitialise` is *only* called when cookie consent is set to `allow`/`deny`/`dismiss`,but not when the user has not indicated any consent. Thus, we cannot expect this to be calledon every page load.We check if `window.hasInitializedAnalytics` is true (which means analytics has already been initialized on page load)because double-loading Segment throws errors in the console (and potentially double-counts tracking visits).*/ var hasConsentedToCookie = this.hasConsented();
                        if (hasConsentedToCookie && !window.hasInitializedAnalytics) {
                            /* 2022-03-08 Disabling segment tracking due to an explosion in MAU after removing identify call */
                        }
                    },
                    onStatusChange: function (status) {
                        var hasConsentedToCookie = this.hasConsented();
                        var trackCookieBannerDismissed = function () {
                            var segmentProperties = { status: "accepted", bannerType: "info", service: "postings2", accountId: "7d94404d-aac8-47b9-9f74-94368b53a325" };
                            ("");
                            segmentProperties.postingId = "9feadb59-31c1-4634-8998-032403030736";
                            (""); /* 2022-03-08 Disabling segment tracking due to an explosion in MAU after removing identify call. */
                        };
                        if (hasConsentedToCookie) {
                            /* 2022-03-08: Disabling segment tracking due to an explosion in MAU after removing identify call */
                        } else {
                            var subDomain = document.location.hostname;
                            /* We want to also get the rootDomain because some of the cookies (e.g. Segment cookies) setthe cookie on the rootDomain instead of the subdomain (lever.co instead of jobs.lever.co),so we have to be more specific in order to delete it.*/ var rootDomain = subDomain
                                .split(".")
                                .reverse()
                                .splice(0, 2)
                                .reverse()
                                .join(".");
                            function removeCookie(cookieName) {
                                document.cookie = cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=" + subDomain + ";";
                                document.cookie = cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=" + rootDomain + ";";
                            }
                            var GA_COOKIES = ["_gid", "_ga", "_gat_customer"];
                            var SEGMENT_COOKIES = ["ajs_user_id", "ajs_anonymous_id", "ajs_group_id"];
                            GA_COOKIES.forEach(function (cookie) {
                                removeCookie(cookie);
                            });
                            SEGMENT_COOKIES.forEach(function (cookie) {
                                removeCookie(cookie);
                            });
                        }
                    },
                });
            });
        </script>
    </body>
</html>

    '''
    
    
    