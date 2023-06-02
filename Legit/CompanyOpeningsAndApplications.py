from urllib import request
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import csv

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
import time

import re
from selenium.common.exceptions import NoSuchElementException
#from scraperGoogle import webdriver
import bs4
from bs4 import Tag
from bs4.element import NavigableString
import spacy
from fuzzywuzzy import fuzz
# import Legit.config as config
# ^ handle_custom_rules()
import config

import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from transformers import GPTNeoForCausalLM, GPT2Tokenizer


#! Filter out string "professional experience is a must"


import torch

class CompanyWorkflow():
                                                #TODO: v INCLUDE THIS EVERYWHERE!!!!!
    def __init__(self, JobSearchWorkflow_instance, browser, users_information, user_desired_jobs, todays_jobs_applied_to_info, tokenizer, model, nlp, lemmatizer, custom_rules, q_and_a, senior_experience):
        self.JobSearchWorkflow_instance = JobSearchWorkflow_instance
        #self.list_of_links = list_of_links
        self.browser = browser
        self.company_job_title = None
        self.company_name = None
        self.company_job_location = None
        self.company_open_positions_urls = []
        #This and apply can be temporary/method variables
        #self.a_fragment_identifier = None
        self.company_job_department = None
        self.job_id_number = None
        
        self.app_comp = None
        
        self.users_information = users_information  #{}
        self.application_company_name = None
        self.company_open_positions_link = None
        if senior_experience == False:
            self.avoid_these_job_titles = ["senior", "sr", "principal", "lead", "manager"]
        self.soup = None
        self.company_open_positions_a = None    #For selenium to click
        self.application_company_name = None
        self.todays_jobs_applied_to_info = todays_jobs_applied_to_info  #{}
        self.company_other_openings_href = None
        self.job_link_url = None
        self.user_desired_jobs = user_desired_jobs  #[]
        self.one_resume_label = False
    
        self.form_input_details = {}
    
    
        
        #init_gpt_neo()
        self.tokenizer = tokenizer
        self.model = model
        #load_nlp()
        self.nlp = nlp
        #load_company_resources()
        self.lemmatizer = lemmatizer
        
        
        
        self.custom_rules = custom_rules
        self.q_and_a = q_and_a
        
        self.env_path = '.env'
        
        
        self.form_input_extended = None
        
        
    # from transformers import pipeline

    # generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
    # print(generator("Once upon a time", max_length=100))

    
    
        

    
    #! Run determine_current_page and .header ONCE!!!!
    #! Once you get the list for all the open positions...
    #! Run a loop here .job_description => .should_apply() => .apply(.get_form_input_details(), .insert_resume(), .fill_in_form(), captcha_stuff()) 
    #!                                                  ^.get_job_data()
    #NOTE: For the 1st iteration let .determine_current_page() do all the work
    def company_workflow(self, job_link):
        print("company_workflow()")
        #ALSO use this to get NEW... input Headers and their anwsers!!!!!! 
        #self.lets_run_some_tests()
        self.job_link_url = job_link       #!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------------------------------------------
        #self.lets_run_some_tests()
        #self.full_company_test()
        
        if "jobs.lever.co" in job_link:
            self.application_company_name = "lever"
        elif "boards.greenhouse.io" in job_link:
            self.application_company_name = "greenhouse"
            # self.determine_current_page(job_link, self.application_company_name)
            # self.company_job_openings(soup)
            
            # for job_opening in self.company_job_openings:
            #     soup = self.apply_beautifulsoup(job_opening, "lxml")
            #     webpage_body = soup.find('body')
            #     if self.should_user_apply(webpage_body) == True:
            #         self.lever_io_data(job_opening, webpage_body)
            #         soup = self.apply_beautifulsoup(job_link, "html")
            #         form_input_details = self.get_form_input_details()
            #         self.insert_resume()
            #         self.fill_out_application(form_input_details)
            #         self.keep_jobs_applied_to_info(job_link)
            #     self.reset_job_variables()
            
        # elif "boards.greenhouse.io" in job_link:
        #     self.application_company_name = "greenhouse"
        self.determine_current_page(job_link, self.application_company_name)
        #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        print("GOOOOODDDD LORD!!!! Do you know what this means Mr. McCalister...")
        
        
        
        
        
        #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        soup = self.apply_beautifulsoup(job_link, "lxml")
        self.company_job_openings(soup)
        
        for job_opening in self.company_job_openings:
            soup = self.apply_beautifulsoup(job_opening, "lxml")
            webpage_body = soup.find('body')
            if self.should_user_apply(webpage_body) == True:
                self.lever_io_data(job_opening, webpage_body)
                soup = self.apply_beautifulsoup(job_link, "html")
                form_input_details = self.get_form_input_details()
                self.insert_resume()
                self.fill_out_application(job_link, form_input_details)
                self.keep_jobs_applied_to_info(job_link)
            self.reset_job_variables()
        #! div_main ==> lever.co = job_description
        return
        
    
    def determine_current_page(self, job_link, application_company_name):
        print("determine_current_page()")
        soup = self.apply_beautifulsoup(job_link, "lxml")
        print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        if application_company_name == "lever":
            webpage_body = soup.find('body')
            opening_link_application = soup.find('div', {"class": 'application-page'})
            opening_link_description = soup.find('div', {"class": 'posting-page'})
            opening_link_company_jobs = soup.find('div', {"class": "list-page"})
            if opening_link_application:
                print('-Application Page')
                try:
                    #TODO: This is v what we want to avoid!!!
                    company_open_positions = soup.find('a', {"class": "main-header-logo"})
                    application_webpage_html = soup.find("div", {"class": "application-page"})
                    self.lever_co_header(webpage_body, soup)
                    #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    self.form_input_details = self.get_form_input_details(current_url)
                    self.process_form_inputs(self.form_input_details)
                    
                    
                    #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                #     try:
                #         self.company_open_positions_a.click()
                #     except:
                #         raw_link = company_open_positions['href']
                #         self.browser.get(raw_link)
                #     time.sleep(2)
                #     return
                except:
                    #TODO: Change this Error type!
                    raise ConnectionError("ERROR: Companies other open positions are not present")
            elif opening_link_description:
                print("-Job Description Page")
                self.scroll_to_element(opening_link_description)
                apply_to_job = self.should_user_apply(opening_link_description)
                if apply_to_job == True:
                    print("lever application locked and loaded")
                    self.bottom_has_application_or_button(application_company_name)
                    time.sleep(3)
                    current_url = self.browser.current_url
                    soup = self.apply_beautifulsoup(current_url, "html")
                    self.form_input_details = self.get_form_input_details(current_url)
                    self.insert_resume()
                    #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    #self.form_input_details = self.get_form_input_details(current_url)
                    self.process_form_inputs(self.form_input_details)
                    
                    
                    #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    #self.fill_out_application(job_link, form_input_details)
                    self.keep_jobs_applied_to_info()
                elif not apply_to_job:
                    #TODO:
                    self.company_other_openings_href.click()
                    
                #TODO: If the button is present click OTHERWISE just insert the link
                if self.company_other_openings_href:
                    self.company_other_openings_href.click()
                else:
                    self.browser.get(self.company_other_openings_href)

            elif opening_link_company_jobs:
                print('-Job Listings Page')
                pass
            return
        
            
        elif application_company_name == "greenhouse":
            div_main = soup.find("div", id="main")
            job_description_element = self.browser.find_element(By.ID, "content")
            
            #I did it this way because it checks very few elements since 1 of these options are normally literally the next element
            next_elem = div_main.find_next()
            while next_elem:    #NOTE: REMEBER THIS DOESN'T INCREMENT next_elem SO IT'S THE SAME VALUE AS ABOVE!!!!
                if next_elem.name == "div" and (next_elem.get("id") == "flash-wrapper" or next_elem.get("id") == "flash_wrapper"):
                    print('-Job Listings Page')
                    pass
                elif (next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper"):
                    print('-Job Listings Page')
                    pass
                elif (next_elem.name == "section" and next_elem.get("class") == "level-0"):
                    print("-Company Job Openings Page")
                    print("A while loop for this is perfect for this because there can be multiple <section class='level-0'>")
                    #TODO: for this one in the elif you have to look through all "level-0" sections!!
                    return
                elif next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"]:
                    app_body = next_elem
                    header = next_elem.find("div", id="header")
                    content = next_elem.find("div", id="content")
                    
                    if header and content:
                        print("-Job Description Page")
                        #TODO: Fix this!!! I need the header link!
                        self.greenhouse_io_header(app_body, header, content)    #TODO: return *job_title, company, location, ???*
                        current_url = self.browser.current_url
                        should_apply = self.should_user_apply(app_body)
                        if should_apply == True:
                            #This should setup the code so that it's lookin down the barrell of the application! Everything should already be setup!!!
                            self.bottom_has_application_or_button(application_company_name)
                            print("greenhouse application locked and loaded")
                            #form_input_details = self.get_form_input_details(job_link)
                            print("Meet")
                            time.sleep(8)
                            self.insert_resume()
                            print("me")
                            time.sleep(8)
                            #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            self.form_input_details = self.get_form_input_details(current_url)
                            self.process_form_inputs(self.form_input_details)
                    
                            
                            #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            print("out back naked little Timmy....")
                            #self.fill_out_application(job_link, form_input_details)
                            self.keep_jobs_applied_to_info(job_link)
                        elif should_apply == False:
                            pass 
                        else:
                            print("\tHmmm that's weird ? it's neither button nor application")
                        
                        
                        try:
                            self.company_other_openings_href.click()
                        except:
                            self.browser.get(self.company_other_openings_href)
                            
                            
                        time.sleep(4)
                        pass
                    break
                else:
                    next_elem = next_elem.find_next()
            print("Not really sure how the heck we got here and defintiely don't have a clue about where to go from here!?!?!?")
            return
    
    
    
    
    
    
    
    
    
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                TOOLS                                          !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def apply_beautifulsoup(self, job_link, parser):
        print("apply_beautifulsoup()")
        #the way I learned how to do it
        if parser == "lxml":
            result = requests.get(job_link)
            content = result.text
            soup = BeautifulSoup(content, "lxml")
        #used for form_input_details()
        if parser == "html":
            page = requests.get(job_link)
            result = page.content
            soup = BeautifulSoup(result, "html.parser")           
        return soup
    
    def scroll_to_element(self, element):
        print("scroll_to_element()")
        # Check if the input element is a BeautifulSoup element
        if isinstance(element, Tag):
            # Extract the tag name
            tag_name = element.name
            print("  ", {tag_name})
            
            # Extract the attributes
            attrs = element.attrs
            css_selectors = [f"{tag_name}"]
            
            # Convert attributes to CSS selectors
            for attr, value in attrs.items():
                if isinstance(value, list):
                    value = " ".join(value)
                    css_selectors.append(f"[{attr}='{value}']")
                    
                css_selector = "".join(css_selectors)
                print("  ", end="")
                print(css_selector)
                
                # Find the same element using Selenium
                element = self.browser.find_element(By.CSS_SELECTOR, css_selector)
                
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        print("  Scrolled to this place...")
        time.sleep(3)
        return
    
    #These set of methods are a bit different because... although they do filter; their purpose is for my Google Sheets Data!!
    def users_basic_requirements(self):
        basic_requirements_met = True
        while basic_requirements_met == True:
            #? READ IT LIKE THIS: naturally if True => run the inside | if not True <-(!so say with expected answer!) sssoooooo...
            #? to run the inside we need {something that's} "not True" LITERALLY which is False which is needed to => run the inside
            if not self.users_basic_requirements_job_title():
                basic_requirements_met = False
            if not self.users_basic_requirements_job_location():
                basic_requirements_met = False
            if basic_requirements_met == True:
                break
        if basic_requirements_met == False:
            self.found_senior_job_insert()
        elif basic_requirements_met == True:
            self.found_entry_job_insert()
        return
        
    def users_basic_requirements_company_openings(self):
        #This filters company_job_openings BUT only removes duplicates && everything previously already looked at!!
        self.company_job_openings = self.JobSearchWorkflow_instance.ensure_no_duplicates(self.company_job_openings)
        todays_jobs_applied_to_URLs = self.JobSearchWorkflow_instance.get_job_links_users_applied_to(self.todays_jobs_applied_to_info)
        self.company_job_openings = self.JobSearchWorkflow_instance.filter_out_jobs_user_previously_applied_to(self.company_job_openings, todays_jobs_applied_to_URLs)
        self.company_job_openings = self.JobSearchWorkflow_instance.filter_out_jobs_user_previously_applied_to(self.company_job_openings, self.JobSearchWorkflow_instance.google_search_results_links)
    
    def users_basic_requirements_job_title(self):
        for desired_job in self.user_desired_jobs:
            if desired_job not in self.company_job_title:
                return False
            if self.avoid_these_job_titles:
                for avoid_title in self.avoid_these_job_titles:
                    if avoid_title in desired_job:
                        return False
        return True
    
    def user_basic_requirements(self, company_job_location, company_job_workplaceType):
        if not company_job_location or company_job_location.lower() is None:
            return True
        
        if company_job_location not in self.user_preferred_locations:
            return False
        
        if not company_job_workplaceType or company_job_workplaceType:
            return False
        
        # edge cases
        if company_job_workplaceType.lower() == 'in-office with occasional remote':     #could just refer to this as travel
            if 'in-office' in self.user_preferred_workplaceType or 'remote' in self.user_preferred_workplaceType:
                return True
            else:
                return False
            
        if company_job_workplaceType.lower() == 'hybrid with rare in-office':
            if 'hybrid' in self.user_preferred_workplaceType or 'remote' in self.user_preferred_workplaceType:
                return True
            else:
                return False
        
        #standard scenario    
        if company_job_workplaceType.lower() == 'remote':
            return True
        
        if company_job_workplaceType.lower() == 'hybrid':
            if 'hybrid' in self.user_preferred_workplaceType and 'in-office' in self.user_preferred_workplaceType:
                return True
            else:
                return False
            
        if company_job_workplaceType.lower() == 'in-office':
            if 'in-office' in self.user_preferred_workplaceType:
                return True
            else:
                return False
            
        print("Yo some crap went wrong or somethin dog")
        return False
    

    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                                                               !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
    #TODO: This goes to all the links!!
    # def troubleshoot_xpath(self):
    #     for link in self.list_of_links:
    #         try:
    #             self.browser.get(link)
    #             time.sleep(2)
    #             job_title = self.browser.title
    #             print(f"Scraping job: {job_title}")

    #             # Search for the Google search name in the page
    #             google_search_name = job_title.split("-")[0].strip()
    #             print(f"Searching for: {google_search_name}")
    #             selenium_google_link = self.browser.find_element(By.XPATH, f'//ancestor::a/h3[not(descendant::br)][text()="{google_search_name}"]')
    #             print("Found search result")

    #             # Click on the Google search result link
    #             selenium_google_link.click()
    #             print("Clicked on the search result link")

    #             # Wait for the page to load and switch to the new tab
    #             WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
    #             self.browser.switch_to.window(self.browser.window_handles[-1])
    #             print("Switched to new tab")

    #             # Perform actions on the job page
    #             self.scrape_job_page()

    #             # Close the new tab and switch back to the search results tab
    #             self.browser.close()
    #             self.browser.switch_to.window(self.browser.window_handles[0])
    #             print("Closed new tab and switched back to search results tab")

    #         except NoSuchElementException:
    #             print(f"No search result found for: {google_search_name}")
    #             continue
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                               TESTING                                         !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    #PURPOSE: To test methods
    def lets_run_some_tests(self):
        print('Coolio, waiting...')
        time.sleep(5)
        print("Eff that old website! Let's test this new one heard J.Cole said he heard Jonah Hill said it was tight! Out with the old in with the new!!")
        #url = "https://boards.greenhouse.io/doubleverify/jobs/6622484002"
        #url = "https://boards.greenhouse.io/zealcareers/jobs/4873035004"
        url = "https://jobs.lever.co/younited/6c000bb3-c2e4-490c-a02d-48cd3b2df908/apply"
        self.browser.get(url)
        time.sleep(4)
        #Run any tests you want here!
        form_input_details = self.get_form_input_details(url)
        self.print_form_details(form_input_details)
        time.sleep(20)
        #url="https://jobs.lever.co/govini/cc5f740a-7248-4246-8b77-e28ed27dd46d/apply"
        url="https://jobs.lever.co/mainstreet/c09d4403-97be-4ffd-b886-e5df9b6e1f88/apply"
        self.browser.get(url)
        time.sleep(4)
        #Run any tests you want here!
        form_input_details = self.get_form_input_details(url)
        self.print_form_details(form_input_details)
        time.sleep(20)
        
        print("You've done it all your hard work is done! Definitely wasn't worth it but whatever. Never doin that crap again.")
        time.sleep(5)
        return
    
    #PURPOSE: To test full walkthroughs
    def full_company_test(self):
        print("OOOOOOOOOOOHHHHHHHHHH SSSSShhhhhiiiiiiii we goin full-auto!!")
        url = "https://jobs.lever.co/younited/6c000bb3-c2e4-490c-a02d-48cd3b2df908"
        self.browser.get(url)
        self.job_link_url = url
        time.sleep(3)
        return
        
    def delete_maybe(self, job_link):
        application_company_name = None
        
        #ALSO use this to get NEW... input Headers and their anwsers!!!!!! 
        self.lets_run_some_tests()

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                                                               !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 







 


    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                   INDIVIDUAL COMPANY-WORKFLOW STEPS                           !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    #everything_about_job = app_body.get_text()
    #should_user_apply(everything_about_job)
    #greenhouse(job_description) => app_body
    def should_user_apply(self, job_description):
        print("should_user_apply()")
        #FILTER: keywords (industry experience//////)
        everything_about_job = job_description.get_text()

        #print(everything_about_job)
        #experience_needed = r"\b\d+\s*(year|yr)s?\s+of\s+experience\b"
        experience_needed = "You must be a diety! Being a demigod or demigoddess is literally embarrassing... just go back to coloring if this is you. Literally useless & pathetic ewww"
        if re.search(experience_needed, everything_about_job):
            print("Experience requirement found!")
            #print(re.search(experience_needed, everything_about_job))
            return False
        else:
            print("No experience requirement found!")
            #print(re.search(experience_needed, everything_about_job))
            return True
        
    def bottom_has_application_or_button(self, application_company_name):
        print("bottom_has_application_or_button()")
        soup = self.apply_beautifulsoup(self.browser.current_url, "html")
        if application_company_name == "lever":
            a_tag_butt = soup.find('a', {'data-qa': ['btn-apply-bottom', 'show-page-apply']})
            div_tag_butt = soup.find('div', {'data-qa': 'btn-apply-bottom'})
            application_at_bottom = soup.find("div", id="application")
            print("\nLever: Application at bottom or <button>")
            if a_tag_butt:
                print("\tPress button to go to application")
                xpath_selector = f"//a[@data-qa='{a_tag_butt['data-qa']}']"
                print(f"xpath_selector: {xpath_selector}")
                apply_button = self.browser.find_element(By.XPATH, xpath_selector)
                self.scroll_to_element(apply_button)
                time.sleep(1)
                print("apply_button: ", end="")
                print(apply_button)
                apply_button.click()
                time.sleep(2)
            elif div_tag_butt:
                print("\tlever: Press button to go to application")
                apply_button = self.browser.find_element(By.XPATH, f"//div[@data-qa='{a_tag_butt['data-qa'][0]}']")
                self.scroll_to_element(apply_button)
                time.sleep(1)
                apply_button.click()
                time.sleep(2)
            elif application_at_bottom:
                print("\tApplication at bottom of page")
                self.scroll_to_element(application_at_bottom)
            return
            
        elif application_company_name == "greenhouse":
            application = soup.find("div", id="application")
            apply_button_list = None
            try:
                apply_button_list = self.browser.find_element(By.XPATH, "//button[text()='Apply Here' or text()='Apply Now' or text()='Apply for this job']")
            except NoSuchElementException:
                pass
            print("\nGreenhouse: Application at bottom or <button>")
            if application:
                self.scroll_to_element(application)
                print("\tApplication at bottom of page")
                time.sleep(1)
            elif apply_button:
                #print("apply_button options:", ", ".join(str(button) for button in apply_button_list))
                #apply_button = apply_button_list[0]
                apply_button = apply_button_list
                print("apply_button options:", end="") 
                print(apply_button)

                self.scroll_to_element(apply_button)
                print("\tPress button to go to application")
                time.sleep(1)
                apply_button.click()
                time.sleep(3)
            return
    
    
    
    def company_job_openings(self, soup, div_main, application_company_name):
        print("company_job_openings()")
        #greenhouse.io == <div id="main">   =>   lever.co == ??? [?postings-wrapper?] -> maybe 'filter-bar'
        #greenhouse.io == <section class="level-0">   =>   lever.co == <div class="postings-group">
        #greenhouse.io == <section class="level-1">   =>   lever.co == <div class="posting">
        print("Application Company = " + application_company_name)
        
        
        if application_company_name == 'lever':
            #just getting a better(more narrowed result) filter
            postings_wrapper = soup.find('div', class_="postings-wrapper")
            current_url = self.browser.current_url
            perfect_url = self.try_adjusting_job_link(current_url)
            postings_group_apply = postings_wrapper.find_all('div', class_=lambda x: x and ('postings-group' in x or 'posting-apply' in x))
            
            
            #department_name_empty = True
            for section in postings_group_apply:
                print(section)
                company_department = section.find('div', class_='large-category-header').text
                #if company_department and department_name_empty:
                if company_department:
                    print(company_department)
                    #department_name_empty = False
                
                # if section.name == 'h3':
                #     company_department = section.text
                # if section.name == 'h4':
                #     print('This is most likely just a SUB-category so not really important otber than making sure we go through EVERY job it contains!')
                    
                #job_opening = section.find('div', {'class': 'opening'})
                if section.name == 'div' and section.get('class') == 'posting-apply':
                    job_opening_href = section.next_sibling
                    if job_opening_href.name == 'a' and job_opening_href.get('class') == 'posting-title':
                        button_to_job_description = job_opening_href
                        job_link = job_opening_href.get('href')
                        job_title = job_opening_href.find('h5').text
                        for bad_word in self.avoid_these_job_titles:
                            if bad_word not in job_title:
                                job_href = job_opening_href.get('href')
                                job_url = perfect_url + job_href
                                self.company_open_positions_url.append(job_url)
                                print(job_title)
                        span_tag = job_opening_href.find('span', {'class', 'sort-by-location'})
                        span_tag_company_team = job_opening_href.find('span', {'class': 'sort-by-team'})
                        span_tag_workplaceTypes = job_opening_href.find('span', {'class': 'workplaceTypes'})
                        if span_tag:
                            job_opening_location = span_tag.text
                        #job_opening_href.click()$%$%$%$%$%$%$%$%$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%
                if self.fits_users_criteria():
                    self.company_open_positions_url.append(job_link)
            self.print_company_job_openings("company_job_openings", application_company_name, JobTitle=job_title, JobLocation=job_opening_location, WorkPlaceTypes=span_tag_workplaceTypes, CompanyDepartment=company_department, JobTeamInCompany=span_tag_company_team, JobHREF=job_link, ButtonToJob=button_to_job_description)
            return
        
        elif application_company_name == 'greenhouse':
            current_url = self.browser.current_url
            perfect_url = self.try_adjusting_job_link(current_url)
            sections = div_main.find_all('section', class_=lambda x: x and 'level' in x)
            #print(sections) #TODO: Make sure this list includes all 'level-0' and 'level-1' THEN the for loop below should parse through both 'levels'!!
            count = 0
            for section in sections:
                count += 1
                #if section.name == "class" and section.get("class") == 'level-0':
                if section.name == 'h3':
                    company_department = section.text
                    print(company_department)
                if section.name == 'h4':
                    print('This is most likely just a SUB-category so not really important other than making sure we go through EVERY job it contains!')
                    
                job_opening = section.find('div', {'class': 'opening'})
                if job_opening:
                    job_opening_href = job_opening.find('a')
                    if job_opening_href:
                        job_title = job_opening_href.text
                        print(job_title)
                        for bad_word in self.avoid_these_job_titles:
                            if bad_word not in job_title:
                                job_href = job_opening_href.get('href')
                                job_url = perfect_url + job_href
                                self.company_open_positions_url.append(job_url)
                        span_tag = job_opening.find('span', {'class', 'location'})
                        if span_tag:
                            job_opening_location = span_tag.text
                            print(job_opening_location)
                        #job_opening_href.click()
                if count == 20:
                    break
                print("-------")
            self.print_company_job_openings("company_job_openings", application_company_name, JobTitle=job_title, JobLocation=job_opening_location, ButtonToJob=job_href)
        return
    
    def print_company_job_openings(*args, **kwargs):
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
    
    
    
    
    #The purpose of this method is pretty much only finding and retrieving the companies other open positions url!!!
    def lever_co_header(self, webpage_body):
        links_in_header = []
        print("\nThese are the links/elements that lead to this companies other available Job Openings:")
        current_url = self.browser.current_url
        print("Current URL: " + current_url)
        links_in_header.append(current_url)
        webpage_header = webpage_body.find('div', {"class": 'main-header-content'})
        self.company_open_positions_a = webpage_header.find('a', {"class": "main-header-logo"})
        print("Selenium Click => Companies other Job Openings: " + self.company_open_positions_a)
        #links_in_header.append(self.company_open_positions_a)
        try:
            if self.company_open_positions_a['href']:
                company_open_positions_href = self.company_open_positions_a['href']
                print("Webpage's Header link: " + company_open_positions_href)
                company_open_positions_url = company_open_positions_href
                links_in_header.append(company_open_positions_url)
        except:
            print("This company's webpage is dumb anyways! Trust me they would've probably overworked you anyways.")
        self.check_header_links(links_in_header)
        return
    
    #line 570 #elif child.name == "a"
    #if ("button" in child.get("class")) => remember !BUTTON! to click
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!         greenhouse_io_BANNER  [not header]           !!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def greenhouse_io_header(self, app_body, header, content): #! ^ ^ ^ ^
        first_child = True
        searched_all_a = False
        string_tab = '\n'
        for child in header.children:
            if first_child:                 #! if child == '\n'     CHECK ||||||||||
                first_child = False
                continue
            elif child == string_tab:
                #? continue
                pass
            if child.name == "h1" and "app-title" in child.get("class"):
                self.company_job_title = child.get_text().strip()
            elif child.name == "span" and  "company-name" in child.get("class"):
                self.company_name = child.get_text().strip()    #"at Braintrust" => maybe look for 1st capital letter
            elif child.name == "a" and not searched_all_a:  #TODO: v only captured the 1st <a>
                # has_hash = header.find_all('a', href=(lambda value: value and '#' in value))
                # for a_tag in has_hash:
                #     if '/' in a_tag['href']:
                #         self.a_href = a_tag
                #     #! HTML <a href='#ANYTHINGH'> -> REMEMBER *#* means redirect to that part of the webpage
                #     elif '#' in a_tag['href']:
                #         self.a_fragment_identifier = a_tag
                # if self.company_other_openings_href == None:
                #     logo_container = app_body.find('div', class_="logo-container")
                #     company_openings_a = logo_container.find('a')
                #     self.company_other_openings_href = company_openings_a['href']
                # searched_all_a = True
                header_a_tags = header.find_all('a')
                for head_a_tag in header_a_tags:
                    if '/' in head_a_tag['href']:
                        self.company_other_openings_href = head_a_tag
                    elif '#' in head_a_tag['href']:
                        self.a_fragment_identifier = head_a_tag
                    elif head_a_tag == None:
                        logo_container = app_body.find('div', class_="logo-container")
                        company_openings_a = logo_container.find('a')
                        self.company_other_openings_href = company_openings_a['href']
                        searched_all_a = True
                #all_jobs_available_a_href = child['href']  #! ^ ^ ^ ^ ^ ^ ^ ^ ^
                #print("all_jobs_available_a_href 1 = ")
                #print(all_jobs_available_a_href)
                #! If it opens on job_description see the bottom is 'apply_button' or 'job_application'
                # print("all_jobs_available_a_href 2 = ")
                # all_jobs_available_a_href = child.decode_contents()
                #print(all_jobs_available_a_href)
                #!since child is the <a> remember to click it!!!
                #companies_jobs_link_a = child
            elif child.name == "div" and "location" in child.get("class"):
                self.company_job_location = child.get_text().strip()
            #? else:
            #?     print("child = ")
            #?     print(child)
            #self.company_openings_test_link = 
        if self.company_other_openings_href == None:
            self.print_company_job_openings("greenhouse_io_header()", "greenhouse", JobTitle=self.company_job_title, CompayName=self.company_name, JobLocation=self.company_job_location, JobHREF="Couldnt Find", LinkToApplication_OnPageID=self.a_fragment_identifier)
        else:
            self.print_company_job_openings("greenhouse_io_header()", "greenhouse", JobTitle=self.company_job_title, CompayName=self.company_name, JobLocation=self.company_job_location, JobHREF=self.company_other_openings_href, LinkToApplication_OnPageID=self.a_fragment_identifier)
        return
        #self.greenhouse_io_content(app_body, content)
        # if self.a_fragment_identifier == None:
        #     return self.company_job_title, self.company_name, self.company_job_location, self.company_other_openings_href
        # else:
        #     return self.company_job_title, self.company_name, self.company_job_location, self.company_other_openings_href, self.a_fragment_identifier
    
    
            #         position_title = soup.find('h2')
            #         job_title = position_title.get_text().split()
            #         job_info = soup.find('div', {"class": "posting-categories"})
            #         job_location = job_info.find('div', {"class": 'location'}).get_text().strip()
            #         job_department = job_info.find('div', {"class": 'department'}).get_text().strip()
            #         job_commitment = job_info.find('div', {"class": 'commitment'}).get_text().strip()
            #         job_style = job_info.find('div', {"class": 'workplaceTypes'}).get_text().strip()
            #         print("HERE------------------------------------")
                    
            #         a_tag_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
            #         div_tag_butt = soup.find('div', {'data-qa': 'btn-apply-bottom'})
            #         job_apply_butt = None
            #         link_to_apply = None
            #         #job_apply_butt = soup.select_one('a.btn-apply-bottom, div.btn-apply-bottom')
            #         #if job_apply_butt.name == 'div':
            #         if div_tag_butt:
            #             job_apply_butt = job_apply_butt.find('a')
            #             link_to_apply = job_apply_butt['href']
            #         elif a_tag_butt:
            #             link_to__apply = a_tag_butt['href']
            #     except:
            #         #TODO: Change this Error type!
            #         raise ConnectionError("ERROR: Companies other open positions are not present")
            # return
    
    
    
    def check_header_links(self, links_in_header):
        print("check_header_links()")
        #! CANT SET VALUES TO LOCAL VARIABLES  REMEMBER!!!!!...  except for booleans I guess?
        first_link = True
        list_of_other_jobs_keyword
        for header_link in links_in_header:
            if first_link == True and "lever" == self.application_company_name:
                self.try_adjusting_job_link(header_link)
                list_of_other_jobs_keyword = 'list-page'
                first_link = False
            elif first_link == True and "greenhouse" in self.application_company_name:
                
                list_of_other_jobs_keywords = ''
                first_link == False
            self.browser.execute_script("window.open('{}', '_blank');".format(header_link))
            for handle in self.browser.window_handles:
                self.browser.switch_to.window(handle)
                if list_of_other_jobs_keyword in self.browser.page_source:
                    self.company_open_positions_link = header_link
                    return
        print("Hmmmm this is unexpected. I must be dumb...")
        time.sleep(1)
        print("Not you the user; I mean me the programmer...      hmmmm...")
        time.sleep(2)
        print("You probably suck too though, don't think you dont't :)")
        time.sleep(1)
        if (self.company_open_positions_link == None):
            self.company_open_positions_a.click()
            time.sleep(5)
    
    def try_adjusting_job_link(self, job_link):
        print("try_adjusting_job_link()")
        if self.application_company_name == 'lever':
            adjusting_link = job_link.find('jobs.lever.co/') + len('jobs.lever.co/')
            still_adjusting = job_link.find('/', adjusting_link) + 1
            link_adjusted = job_link[:still_adjusting]
            print(link_adjusted)
            job_link = link_adjusted
            print(job_link)
        if self.application_company_name == 'greenhouse':
            adjusting_link = job_link.find('greenhouse.io/') + len('greenhouse.io/')
            still_adjusting = job_link.find('/', adjusting_link) + 1
            link_adjusted = job_link[:still_adjusting]
            print(link_adjusted)
            job_link = link_adjusted
            print(job_link)
        time.sleep(8)
        return job_link
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                                                               !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
    
    
    
    
    
    
    
    
    
    
    
    
    def is_absolute_path(href):
        print("is_absolute_path()")
        parsed_url = urlparse(href)
        print("The href value is: ", end="")
        print(parsed_url)
        return bool(parsed_url.netloc)

    #! HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE
    def fits_users_criteria(test_elements_uniqueness, *args):
        ultimate_lists_checker = []
        for arg in args:
            ultimate_lists_checker.extend(arg)                      #WORKS for job_title && links
        for unacceptable_element in ultimate_lists_checker:
            if unacceptable_element in test_elements_uniqueness:
                return False
        return True

    def get_input_tag_elements(self):
        """
        Returns a list of tuples with input element ID, type and visibility status
        """
        input_elements = self.browser.find_elements(By.TAG_NAME, 'input')
        inputs_info = []
        for input_element in input_elements:
            input_id = input_element.get_attribute('id')
            input_type = input_element.get_attribute('type')
            is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
            inputs_info.append((input_id, input_type, is_hidden))
        return inputs_info



    

    
    #filter out already applied jobs
    #traverse job webpage
    #?????
    def lever_io_data(self, joby_link, soup):
        self.joby_link = joby_link
        print("===Ball = inside the lever.co")
        #opening_link_application = soup.find('div', class_='page-application')      #application immediate
        opening_link_application = soup.find('div', {"class": 'application-page'})
        #opening_link_description = soup.find('div', class_='page-show')             #regular description start
        opening_link_description = soup.find('div', {"class": 'posting-page'})          #NOTE: In HTML class='one two' needs 2 class calls I think!?!?!?
        print("===Ball = opening_link_application = ", end="")
        #print(opening_link_application)
        print("You are on the Job Application webpage")
        print("===Ball = opening_link_description = ", end="")
        #print(opening_link_description)
        print("You are on the Job Description webpage")
        try:
            other_company_jobs = soup.find('div', {"class": 'page show'})
            company_open_positions = other_company_jobs.find('a', {"class": "main-header-logo"})
            if company_open_positions['href']:
                plethora_of_jobs = company_open_positions['href']
                print(plethora_of_jobs)
        except:
            print("Couldn't find the logo with the lick to plethora_of_jobs")
        
        #if soup.find('a', class_='main-header-logo'):
        if opening_link_application:
            try:
                company_open_positions = soup.find('a', {"class": "main-header-logo"})
                #company_open_positions = soup.find('a', class_=['main-header-logo', 'main-header'])
                plethora_of_jobs = company_open_positions['href']
                print("===Ball = plethora_of_jobs = ", end="")
                print(plethora_of_jobs)
                application_webpage_html = soup.find("div", {"class": "application-page"})
                self.lever_io_application(joby_link, application_webpage_html)
                #return opening_link_application
            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        elif opening_link_description:
            print("===Ball = lever.co is working")
            try:
                print("===Ball = inside the try lever.co")
                position_title = soup.find('h2')
                job_title = position_title.get_text().split()
                print("===Ball = job_title = ", end="")
                #print(job_title.get_text())
                print(job_title)
                #? .position_title.find() doesn't work b/c the <h2> and <div> are siblings!!
                # job_info = position_title.find('div', {"class": "posting-categories"})
                job_info = soup.find('div', {"class": "posting-categories"})
                job_location = job_info.find('div', {"class": 'location'}).get_text().strip()
                job_department = job_info.find('div', {"class": 'department'}).get_text().strip()
                job_commitment = job_info.find('div', {"class": 'commitment'}).get_text().strip()
                job_style = job_info.find('div', {"class": 'workplaceTypes'}).get_text().strip()
                print("HERE------------------------------------")
                print(job_location)
        
                a_tag_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
                div_tag_butt = soup.find('div', {'data-qa': 'btn-apply-bottom'})
                job_apply_butt = None
                link_to_apply = None
                #job_apply_butt = soup.select_one('a.btn-apply-bottom, div.btn-apply-bottom')
                #if job_apply_butt.name == 'div':
                if div_tag_butt:
                    job_apply_butt = job_apply_butt.find('a')
                    link_to_apply = job_apply_butt['href']
                elif a_tag_butt:
                    link_to_apply = a_tag_butt['href']
                
                print("===Ball = link_to_apply = ", end="")
                print(link_to_apply)

            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        #print("===Ball = leaving the lever.co")
        return soup

    #if id="app_body" and [check which page you are on]
    
    def greenhouse_io_start_page_decide(self, soup): #if (child of main is one of these)
        print("Welcome fair maiden this company has gathered to make decisions based on your skin color... please after you!")
        div_main = soup.find("div", id="main")
        next_elem = div_main.find_next()
        while next_elem:
            if next_elem.name == "div" and next_elem.get("id") == "flash-wrapper":
                print('-Job Page')
                return soup.find("div", id="flash-wrapper")
                break
            elif (next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper"):
                print('-Job Listings Page')
                return soup.find("div", id="embedded_job_board_wrapper")
                break
            elif (next_elem.name == "section" and next_elem.get("class") == "level-0"):
                print("-Job Listings Page")
                print("A while loop for this is perfect for this because there can be multiple <section class='level-0'>")
                #TODO: for this one in the elif you have to look through all "level-0" sections!!
                return soup.find("section", {"class": "level-0"})
            elif next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"]:
                app_body = next_elem
                header = next_elem.find("div", id="header")
                content = next_elem.find("div", id="content")
                application = soup.find("div", id="application")
                if header and content:
                    print("Job Description Page")
                    self.greenhouse_io_header(app_body, header, content)
                else:
                    print("Application at bottom or <button>")
                    #TODO
                    apply_button = div_main.find("button", text="Apply Here")
                    if application:
                        self.greenhouse_io_application(application)
                    elif apply_button:
                        apply_button.click()
                        time.sleep(5)
                        self.greenhouse_io_application(application)
                        print("Application = ", end="")
                        print(application)
                        return application
                break
            else:
                next_elem = next_elem.find_next()
        print("Guess the .greenhouse_io_start_page_detector() while loop doesn't work")

    #! FIND AND ATTACH RESUME 1st B/C AUTOFILL SUCKS
    def attach_resum(self, application):
        resume_element = application.find_element(By.XPATH, "//*[@id[contains(@id, 'resume')]]")
        resume_path = "get from .env file"
        
        #How does the form want us to upload our resume? Button click...
        while True:
            upload_by_button = application.find_element(By.TAG_NAME, "//fieldset[@aria-describedby='resume-allowable-file-types']")
            if upload_by_button:
                ActionChains(self.browser).move_to_element(upload_by_button).click().perform()
                upload_by_button.send_keys(resume_path)
                break
        try:
            ActionChains(self.browser).send_keys(Keys.ENTER).perform()
        except:
            raise "Something went wrong meanie! Help me :("






    def find_visible_input(self, selector):
        input_element = self.browser.find_element(By.CSS_SELECTOR, selector)
        is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
        if is_hidden:
            self.browser.execute_script("arguments[0].style.display = 'block';", input_element)
            is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
        return input_element, not is_hidden

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!       REMEMBER TO COUNT THE NUMBER OF OPEN SENIOR > ROLES AVAILABLE           !
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #! FIND AND ATTACH RESUME 1st B/C AUTOFILL SUCKS
    def insert_resume(self):
        print(".insert_resume()")
        #resume_path = self.users_information.get('WORK_RESUME_PATH')
        resume_path = self.users_information.get('RESUME_PATH')
        print(resume_path)
        
        if self.app_comp == 'greenhouse':
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
            #resume_upload_button = self.browser.find_element(By.CSS_SELECTOR, 'button.visible-resume-upload')
            resume_upload_button = self.browser.find_element(By.CSS_SELECTOR, 'button[aria-describedby="resume-allowable-file-types"]')
            print("--------------------------------------------------------")
            print(resume_upload_button)
            print("--------------------------------------------------------")
            #print()
            print("6")
            if resume_upload_button:
                time.sleep(1)
                print("8")
                input_elements = self.get_input_tag_elements()
                
                #NOTE: [https://dev.to/razgandeanu/how-to-upload-files-with-selenium-3gj3]
                # input_element, is_visible = self.find_visible_input('input[data-qa="input-resume"]')
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
                return div_parent, parents_text

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
    
    #OG: print_form_heirarchy()
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
            print("Craig would be dissapointed in you...    you maget!")
            
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

    #! Include checkboxes!!!!
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
                div_parent, parents_text = self.get_label(field)
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
        
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!                                                                               !
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    
    #https://boards.greenhouse.io/blend/jobs/4870154004
    #https://boards.greenhouse.io/dice/jobs/6594742002
    #https://jobs.lever.co/atlassian/013b099b-85b2-4527-a2d4-18179b0a1247/apply
    #https://jobs.lever.co/gametime/58aef93e-7799-4ba0-bea9-e848520db151/apply
    #https://boards.greenhouse.io/zealcareers/jobs/4873035004
    
    
    
    
    
    
    
    
        
    def keep_jobs_applied_to_info(self, job_link):
        self.todays_jobs_applied_to_info.append({
            'Job_URL': job_link,
            'Company_Name': self.company_name,
            'Job_Title': self.company_job_title,
            'Company_Job_Location': self.company_job_location,
            'Company_Department': self.company_job_department,
            'Job_ID_Number': self.job_id_number,
        })  
        

    #*This is what I used before config.py            
    def get_value_for_label(self, label):
        label_to_key_mapping = {
            'Full Name': 'FULL_NAME',
            # Add other custom mappings here
        }

        if label in label_to_key_mapping:
            key = label_to_key_mapping[label]
            if key == 'FULL_NAME':
                first_name = self.users_information.get('FIRST_NAME', '')
                middle_initial = self.users_information.get('MIDDLE_INITIAL', '')
                last_name = self.users_information.get('LAST_NAME', '')
                return f"{first_name} {middle_initial} {last_name}".strip()

        # If there's no custom mapping for the label, return the value associated with the label as the key
        return self.users_information.get(label, None)
        
        
        
    
        
    def fill_form_fields(self, form_input_details):
        # Start the Selenium browser
        browser = webdriver.Firefox()
        browser.get(self.url)

        for input_detail in form_input_details:
            env_key = self.get_env_key_for_label(input_detail['label'])
            env_value = self.users_information.get(env_key)

            if env_value is None:
                print(f"New question not found in the .env file: {input_detail['label']}")
                if input_detail['values']:
                    print("Possible answers:")
                    for value in input_detail['values']:
                        print(f" - {value}")
                env_value = input("Please enter your answer: ")
                # Save the new value to the .env file here, if needed

            if env_value is not None:
                # Fill in the form field based on its type
                if input_detail['type'] == 'textarea':
                    textarea = input_detail['html']
                    textarea_element = browser.find_element_by_name(textarea['name'])
                    textarea_element.send_keys(env_value)
                elif input_detail['type'] == 'select':
                    select = input_detail['html']
                    select_element = Select(browser.find_element_by_name(select['name']))
                    select_element.select_by_visible_text(env_value)
                elif input_detail['type'] == 'text':
                    text_element = browser.find_element_by_name(input_detail['html']['name'])
                    text_element.send_keys(env_value)
                elif input_detail['type'] == 'email':
                    email_element = browser.find_element_by_name(input_detail['html']['name'])
                    email_element.send_keys(env_value)
                elif input_detail['type'] == 'password':
                    password_element = browser.find_element_by_name(input_detail['html']['name'])
                    password_element.send_keys(env_value)
                elif input_detail['type'] == 'checkbox':
                    checkbox_element = browser.find_element_by_name(input_detail['html']['name'])
                    if env_value.lower() in ['true', 'yes']:
                        checkbox_element.click()
                elif input_detail['type'] == 'radio':
                    radio_elements = browser.find_elements_by_name(input_detail['html']['name'])
                    for radio_element in radio_elements:
                        if radio_element.get_attribute('value') == env_value:
                            radio_element.click()
                            break

        # Click the submit button
        submit_button = browser.find_element_by_css_selector("input[type='submit'], button[type='submit']")
        submit_button.click()
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#Fiesty
        # def fill_form(self, form_input_details):
        # print("\nfill_form()")
        # for i, input_data in enumerate(form_input_details):
        #     print(f"Processing Input {i}: ...")

        #     # Check if it's a special case
        #     special_expected_user_input = self.is_special_case(input_data)
        #     if special_expected_user_input:
        #         print(f"Input {i}: a special case -> {special_expected_user_input}")

        #     # Extract label from the input_data
        #     label = input_data['label']

        #     # Handle custom rules or get matching key if present
        #     key = self.get_matching_key_if_present(label, special_expected_user_input)

        #     if key:
        #         # Get value from the users_information dictionary
        #         value = self.users_information[key]

        #         if special_expected_user_input == 'is_multiple_choice':
        #             # if multiple values are expected, we'll assume value is a list
        #             for v in value:
        #                 self.browser.find_element(label).send_keys(v)
        #                 # Add additional logic here to handle multiple choice selections
        #         elif special_expected_user_input == 'is_file':
        #             # handle file upload
        #             self.browser.find_element(label).send_keys(value)  # assuming value is file path
        #         else:
        #             # Fill in the form
        #             self.browser.find_element(label).send_keys(value)
        #     else:
        #         print(f"No matching key found for label {label}")
        # print("eff that question")
        # time.sleep(5)
#Kittens 
    # print("\n\n--------------------------------------------------------")
    # print("My Way")
    # print("spacy_extract_headword_and_dependants()")
    # headword = ""
    # dependants = []
    # for token in doc:
    #     print(f"""
    #           TOKEN: {token.text}
    #           ====
    #           {token.tag_ = }
    #           {token.head.text = }
    #           {token.dep_ = }
    #           """)
        
        
        
    #     if token.head == "ROOT":
    #         headword = token.head.text
    #     elif token.dep_ in {"compund", "amoud", "attr"}:
    #         dependants.append(token.lemma_)
    #         #dependants.append(token.text)
    # print(f"headword = {headword}")
    # print(f"dependants = {dependants}")
    # #return headword, dependants
    # print("--------------------------------------------------------")
    
    
    
    
    #*Testing Method
    def test_this_pile_of_lard(self, job_link):
        print("test_this_pile_of_lard()")
        print(job_link)
        urls = ['https://boards.greenhouse.io/latitude/jobs/5028220',
                'https://boards.greenhouse.io/earnin/jobs/4860753',
                'https://jobs.lever.co/instructure/804e2e79-89dc-4d5a-b247-aee377435f7c/apply',
                'https://jobs.lever.co/relativity/ac76f210-0070-45d2-ba68-440907de4411/apply']
        # for i, url in enumerate(urls):
        #     try:
        #         print(f"Processing URL {i+1}...")
        #         self.browser.get(url)
        #         time.sleep(6)
        #         self.company_workflow(url)
        #         print(f"URL({url}) {i+1} company_workflow() complete...")
        #         time.sleep(20)
        #     except Exception as e:
        #         print(f"An error occurred while processing URL {i+1}: {url}")
        #         print(str(e))
        #     finally:
        #         print(f"Finished processing URL {i+1}")
        for i, url in enumerate(urls):
            print(f"Processing URL {i+1}...")
            self.browser.get(url)
            time.sleep(6)
            self.company_workflow(url)
            print(f"URL({url}) {i+1} company_workflow() complete...")
            time.sleep(20)

                
        #self.process_urls(urls)
    
    #*Old Test Method
    def process_urls(self, urls):
        print("process_urls()")
        for i, url in enumerate(urls):
            try:
                print(f"Processing URL {i+1}...")
                self.browser.get(url)  # assuming self.browser is an instance of a webdriver
                
                
                
                
                time.sleep(5)
                self.scroll_to_element("form")





                form_input_details = self.get_form_input_details()  # assuming a function to extract form details
                self.fill_form(form_input_details)

            except Exception as e:
                print(f"An error occurred while processing URL {i+1}: {url}")
                print(str(e))

            finally:
                print(f"Finished processing URL {i+1}")
    
    def double_check_before_fill_in_form(self):
        print("double_check_before_fill_in_form()")
        print("Nepotism")
    
    #*Sends values to form
    #TODO: NOTE -> if process_form_input sends nothing then check if there was a * in the label!! or if it's a text/textarea!!
    # def fill_form(self, form_input_details):
    def fill_form(self, label, key):
        print("\nfill_form()")
        # for i, input_data in enumerate(form_input_details):
        #     print(f"Processing Input {i}: ...")

        #     # Check if it's a special case
        #     special_expected_user_input = self.is_special_case(input_data)
        #     if special_expected_user_input:
        #         print(f"Input {i}: a special case -> {special_expected_user_input}")

        #     # Extract label from the input_data
        #     label = input_data['label']

        #     # Handle custom rules or get matching key if present
        #     key = self.get_matching_key_if_present(label, special_expected_user_input)

        if key:
            # Get value from the users_information dictionary
            value = self.users_information[key]
            
            
            
            
            for input in self.form_input_details:
                if label == input['label']:
                    input_data = input
                    
                    
            
                    
            special_expected_user_input = self.is_special_case(input_data)

            #self.form_input_details
            if special_expected_user_input == 'is_multiple_choice':
                # if multiple values are expected, we'll assume value is a list
                for v in value:
                    self.browser.find_element(label).send_keys(v)
                    # Add additional logic here to handle multiple choice selections
            elif special_expected_user_input == 'is_file':
                # handle file upload
                self.browser.find_element(label).send_keys(value)  # assuming value is file path
            else:
                # Fill in the form
                self.browser.find_element(label).send_keys(value)
        else:
            print(f"No matching key found for label {label}")
        print("inserted that question")
        print("but eff that question")
        time.sleep(5)
    
    #*Scrolls to each question in the form
    def scroll_to_question(self, input_data_html):
        print("\nscroll_to_question()")
        soup = BeautifulSoup(input_data_html, 'lxml')
        print("soup = ", soup)
        # element = soup.find()
        # print('element = ', element)
        
        # print(soup.get('id'))  # Prints: "mydiv"
        # print(soup.get('class'))  # Prints: ["myclass"]
        
        body_children = soup.body.contents
        for child in body_children:
            print('element = ', child)
            
            if child.get('id'):
                identifier = child.get('id')
                css_selector = '#' + identifier
            elif child.get('class'):
                identifier = child.get('class')[0]
                css_selector = '.' + identifier
            else:
                raise ValueError('The element does not have an id or a class')
        
            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        
            self.browser.execute_script("arguments[0].scrollIntoView();", elemental)
    
    # def form_fields_requirement(self, form_input_answers, label):
    #     #TODO: Make sure to remove the % %
    #     NA_option = True if "Not Applicable" in label or "N/A" in label else False
    #     #TODO: Make sure to remove the | |
    #     SELECT_ONE = True if "select one" in label else False
    #     SELECT_ALL = True if "select all" in label or "N/A" in label else False
    #     MARK_ALL = True if "select all" in label else False
        

        
        
    #     if "*" in label or "✱" in label:
    #         #look through .env for a matching key
    #             #if match_found -> look at key's value
    #                 #if value wrapped in between %% remove them
    #                 #elif value wrapped in between || remove them
    #                 #else return value
    #             #else
        
    #     if "Not Applicable" in label or 'N/A' in label:
    #         #look through .env for a matching key
    #             #if match_found -> look at key's value
    #                 #if value wrapped in between %% user prefers N/A
    #                 #elif value wrapped in between || user prefers 'skip question'
    #                 #else return value
    #             #else
                
    # def job_type_preferences(self, requested_job_type):
        
            
    #TODO: Make the weight of 'your' and 'user'/'users' EQUAL (What is you address? = USERS_ADRESS)!!!!!!
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
        for i, input_data in enumerate(form_input_details):
            time.sleep(5)
            self.init_form_input_extended()
            
            #++++++++++++++++++++++++++++++ MAYBE treat like edge cases +++++++++++++++++++++++++++++++++++++++
            print("Input " + str(i) + ":")
            print("  form_input_details = ", input_data)
            if input_data['is_hidden']:
                continue
            
            print("This is -> is None")
            if input_data['label'] is None:
                print("Dang so -> is None")
                continue
            
            print("This is -> dynamic")
            if 'dynamic' in input_data['label']: #or input_data['label'] is None:
                print("Dang so -> dynamic")
                continue
            
            print("This is -> == None")
            if input_data['label'] == None:
                print("Dang so -> == None")
                continue
            

            if 'Submit Application' in input_data['label']:
                print("Submit Application")
                print("input_data: ", input_data)
                submit_button = input_data
                print("submit_button: ", submit_button)    
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
                print("Ahhhhhhh yes a very sexual we have come across as it is either one of these: 'select', 'radio', 'checkbox'")
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
                            self.fill_form(label, answer)
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
                        self.fill_form(label, answer)
                else:
                    context = self.q_and_a['summary'] + " " + label
                    answer = self.generate_response(context)
                    if answer:
                        # Input the answer into the form
                        print(f"Entering '{answer}' for '{label}'")
                        self.fill_form(label, answer)
                    else:
                        print(f"No stored answers found for '{label}'")
        print("ALL DONE!!! The job application has been completed Reverand Mackie...")
        print("Normally Germans would push the 'Submit Application' button right now!")
        time.sleep(20)
    
    
    def try_finding_match(self, label):
        print("\n1)try_finding_match()")
        words_in_label = label.split()
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
        elif self.jaccard_similarity(jacc_key, label):
            return jacc_key
        else:
            #Since `rule` was previously defined you use it as above but since `summary` wasn't {something about Python treats} so just use () with '' inside it and the variable name within the ''
            return self.generate_response(self.q_and_a('summary'))
    
    
    #*SpaCy's needs and dumb stuff gone
    #TODO: do something with the dumb *!!!!
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
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #TODO: Make sure key isn't = to an already set key!!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        key = "_".join(tokens).upper()
        print(f"key = {key}")
        return key
    
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
                
            # Check for synonyms
            #! WRONG ! sometimes I have 2 so get the root or something!!!
            #synonyms = self.get_synonyms(key)
            #synonyms = self.get_synonyms(label)
            for synonym in synonyms:
                doc2 = self.nlp(synonym.lower().replace("_", " "))
                print("-doc2(synonyms.index) = ", doc2)
                #similarity = doc1.similarity(doc2)
                similarity = doc2.similarity(doc1)
                print("similarity = ", similarity)
                print("key = ", key)
                print("synonyms = ", synonyms)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = key
                    print("max_similarity = ", max_similarity)
                    print("best_match = ", best_match)
                    
                    if max_similarity == 1.0:
                        self.form_input_extended['env_key'] = key
                        self.form_input_extended['env_values'].append(self.users_information[key])
                        print("MATCH: [ 2.2)find_best_match() -> .similarity(question{*label*} | synonyms.index)]")
                        print("\tusers_information = ", key)
                        print("\tlabel = ", label)
                        print("\t... synonym = ", synonym)
                        print("\t... value = ", self.users_information[key])
                        #print("\t... value = ", self.users_information['{key}'])
                        return key
            
            print("\nusers_information + 1")
            
        print("max_similarity = ", max_similarity)
        print("best_match = ", best_match)
        print(best_match if max_similarity > 0.75 else None)
        return best_match if max_similarity > 0.75 else None
    
    #*This is the DOUBLE CHECK
    def get_synonyms(self, word):
        print("\n3)get_synonyms()")
        print(f"word = {word}")
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        print("synonyms = ", end="")
        print(synonyms)
        return synonyms
    
    #*special_case() method 1
    def get_input_type(self, input_data):
        print("get_input_type()")
        label = input_data['type']
        if label == 'select':
            select_element = self.browser.find_element(label)
            is_multiple_choice = select_element.get_attribute('multiple') is not None
            return 'is_multiple_choice' if is_multiple_choice else None
        elif label == 'checkbox':
            return 'is_multiple_choice'
        elif label == 'file':
            return 'is_file'
        return None
    
    #*Just for me to see what it does!! Crap looks haaatt!
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
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                                                               !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    # print("Form Input Details: ", end="")
    # print(f"Input {i}:")
    # print(f"  Label: {detail['label']}")
    # print(f"  Type: {detail['type']}")
    # print(f"  Values: {detail['values']}")
    # print(f"  Is Hidden: {detail['is_hidden']}")
    # print(f"  HTML: {detail['html']}")
    # print(f"  Dynamic: {detail['dynamic']}")
    # print(f"  Related Elements: {detail['related_elements']}")
    #------------------------------------------------------------------------------
    # ['text', 'email', 'password', 'select', 'radio', 'checkbox', 'textarea', 'button', 'file']
    #TODO: Compare label->key/label->value/values->key/values->value
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
    
    
    
    
    
    
    
    
    
    
    
    #FILTER OUT: Two (2) years of hands-on experience writing professional software code.
    #BIRTHDAY: Calculate their age using YYYY
    
    
    #NOTE: q_considerations -> 
        # https://boards.greenhouse.io/affirm/jobs/5600147003 -> checklist's say (select one)
        
    
    
    
    #dictionary variable = {
    #     question: 'How fat are your nuts hangin? (select one)'
    #     q_considerations: ''
    # }
    
    
    
    
    
    
    #ADD TO process_form_inputs()
            #     print("Looking for dynamic answers")
            # for predefined_answer in form_input_details.get('values'):
            #     if "(dynamic)" not in predefined_answer:
            #         #current index + 1   ->    is dynamic {SSSOOOOO if we pick that to be the answer THEN prepare & take special care of the next question}
            #         #answer_results_dynamic = predefined_answer          #Save the answer that will lead to a pop-up dynamic question
            #         self.form_input_extended['dynamic'] = True
                    
            # print("Looking for dynamic questions")
            # for j in reversed(range(i)):
            #     #label = form_input_details[j]['label']         #if the 'label' keys' value is empty this action will prompt a KeyError BUT...  using .get() won't!!!
            #     if input_data.get('label') == form_input_details[j].get('label'):
            #         #TODO:Figure out how to get access to the previous input ALSO  !ALSO! REMEMBER the questions in form_input_details are sometimes out of order
            #         self.form_input_extended['dynamic'] = True
            #         continue
            #     #!RECENT CHANGE sssoooooo if anything happens it's cause of this
            #     # else:
            #     #     if duplicate_label == current_label:
            #     #         has_dynamic_question = duplicate_label          #NOT current_label becuase THAT IS the duplicate and we're looking for the O.G., which is everything that came before it!!!!
            #     # OR OR OOOORRRRRRRR just as Chat-GPT did in fill_out_form() is any of these dynamic things are ran into handle them immediately and then just do `continue` so it skips it on the next iteration!!!!
            
    
    
    
    
    
    
    
    
    
    
    
    
   



#! Important Notes

# bs4
# app_body = soup.find("div", id=["app_body", "app-body"])   <---greenhouse.io

# python
# if label in ['select', 'radio', 'checkbox', 'file']:


#.replace("*", "").replace("✱", "")
#print("True" if matching_keys else "False")





    
        
        





















# Input 18:
#   Label: What gender pronoun(s) do you identify with?
#   Type: checkbox
#   Values: ['He / Him / His', 'She / Her / Hers', 'They / Them / Theirs', 'Decline To Self Identify']
#   Is Hidden: False
#   HTML: <label>What gender pronoun(s) do you identify with?<br><input type="hidden" name="job_application[answers_attributes][4][question_id]" id="job_application_answers_attributes_4_question_id" value="23367632002"><input type="hidden" name="job_application[answers_attributes][4][priority]" id="job_application_answers_attributes_4_priority" value="4"><div><div class="msg-container" set="23367632002"></div></div><label><input type="checkbox" name="job_application[answers_attributes][4][answer_selected_options_attributes][0][question_option_id]" id="job_application_answers_attributes_4_answer_selected_options_attributes_0_question_option_id" value="110843031002" set="23367632002" aria-required="false">&nbsp;&nbsp;He / Him / His</label><br><label><input type="checkbox" name="job_application[answers_attributes][4][answer_selected_options_attributes][1][question_option_id]" id="job_application_answers_attributes_4_answer_selected_options_attributes_1_question_option_id" value="110843032002" set="23367632002" aria-required="false">&nbsp;&nbsp;She / Her / Hers</label><br><label><input type="checkbox" name="job_application[answers_attributes][4][answer_selected_options_attributes][2][question_option_id]" id="job_application_answers_attributes_4_answer_selected_options_attributes_2_question_option_id" value="110843033002" set="23367632002" aria-required="false">&nbsp;&nbsp;They / Them / Theirs</label><br><label><input type="checkbox" name="job_application[answers_attributes][4][answer_selected_options_attributes][3][question_option_id]" id="job_application_answers_attributes_4_answer_selected_options_attributes_3_question_option_id" value="110843034002" set="23367632002" aria-required="false">&nbsp;&nbsp;Decline To Self Identify</label><br></label>
#   Dynamic: False
#   Related Elements: []








# Input 00: -The number in which this input tag appears in the form
#   Label: -The string value that informs the user what information is needed for this specific input
#   Type: -How my code will insert the users value so Ex. checkbox input, radio input, button, etc.
#   Values: -A list of predefined values that the user has to choose from; if any
#   Is Hidden: -Determines whether this input field is hidden or not
#   HTML: -All the HTML code that contains the Label and Values value so inserting users values are quicker
#   Dynamic: -Whether this input field contains anything dynamic
#   Related Elements: -If Dynamic's value is True then this is where we store that dynamic code
  
# Input 18:
#   Label: How would you describe your gender identity? (mark all that apply)
#   Type: checkbox
#   Values: ["Man", "Non-binary", "Woman", "I prefer to self-describe", "I don't wish to answer"]
#   Is Hidden: False
#   HTML: 
#   Dynamic: False
#   Related Elements: []

  

  

  

  

  

# Input 16:
#   Label: How would you describe your racial/ethnic background? (mark all that apply)
#   Type: checkbox
#   Values: ["Black or of African descent", "East Asian", "Hispanic, Latinx or of Spanish Origin", "Indigenous, American Indian or Alaska Native", "Middle Eastern or North African", "Native Hawaiian or Pacific Islander", "South Asian", "Southeast Asian", "White or European", "I prefer to self-describe", "I don't wish to answer"]
#   Is Hidden: False
#   HTML: 
#   Dynamic: False
#   Related Elements: []
# Input 17:
#   Label: How would you describe your sexual orientation? (mark all that apply)
#   Type: checkbox
#   Values: ["Asexual", "Bisexual and/or pansexual", "Gay", "Heterosexual", "Lesbian", "Queer", "I prefer to self-describe", "I don't wish to answer"]
#   Is Hidden: False
#   HTML: 
#   Dynamic: False
#   Related Elements: []
# Input 18:
#   Label: Do you identify as transgender? (Select one)
#   Type: checkbox
#   Values: ["Yes", "No", "I prefer to self-describe", "I don't wish to answer"]
#   Is Hidden: False
#   HTML: 
#   Dynamic: False
#   Related Elements: []
# Input 19:
#   Label: Do you have a disability or chronic condition (physical, visual, auditory, cognitive, mental, emotional, or other) that substantially limits one or more of your major life activities, including mobility, communication (seeing, hearing, speaking), and learning? (Select one)
#   Type: checkbox
#   Values: ["Yes", "No", "I prefer to self-describe", "I don't wish to answer"]
#   Is Hidden: False
#   HTML: 
#   Dynamic: False
#   Related Elements: []
# Input 20:
#   Label: Are you a veteran or active member of the United States Armed Forces? (Select one)
#   Type: checkbox
#   Values: ["Yes, I am a veteran or active member", "No, I am not a veteran or active member", "I prefer to self-describe", "I don't wish to answer"]
#   Is Hidden: False
#   HTML: 
#   Dynamic: False
#   Related Elements: []









































#     def determine_current_page(self, job_link, application_company_name):
#         soup = self.apply_beautifulsoup(job_link, "lxml")
        
#         if application_company_name == "lever":
#             webpage_body = soup.find('body')

#             opening_link_application = soup.find('div', {"class": 'application-page'})
#             opening_link_description = soup.find('div', {"class": 'posting-page'})
#             opening_link_company_jobs = soup.find('div', {"class": "list-page"})

#             #opening_link_application = soup.find('div', {"class": 'application-page'})
#             if opening_link_application:
#                 try:
#                     self.lever_co_header(webpage_body, soup)

#                     try:
#                         self.company_open_positions_a.click()
#                     except:
#                         raw_link = company_open_positions['href']
#                         self.browser.get(raw_link)
#                     time.sleep(2)
#                     return
#                 except:
#                     #TODO: Change this Error type!
#                     raise ConnectionError("ERROR: Companies other open positions are not present")
                
#             elif opening_link_description:
#                 #try:
#                 apply_button = None
                
#                 a_tag_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
#                 div_tag_butt = soup.find('div', {'data-qa': 'btn-apply-bottom'})
#                 application_at_bottom = soup.find("div", id="application")
#                 print("Application at bottom or <button>")
#                 if a_tag_butt:
#                     #print("== Application at bottom of page")
#                     print("\tPress button to go to application")
#                     apply_button = a_tag_butt
#                     apply_to_job = self.should_user_apply(opening_link_description)
#                 elif div_tag_butt:
#                     print("\tPress button to go to application")
#                     apply_button = div_tag_butt
#                     apply_to_job = self.should_user_apply(opening_link_description)    #apply_to_job = boolean | T=.click() && F=.lever_header() -> .company_job_openings()
#                 if apply_to_job == True:
#                     print("1st lever application locked and loaded")
#                     apply_button.click()
#                     time.sleep(5)
#                     current_url = self.browser.current_url
#                     soup = self.apply_beautifulsoup(current_url, "html")
#                     form_input_details = self.get_form_input_details(current_url)
#                     self.insert_resume()
#                     self.fill_out_application(form_input_details)
#                     self.keep_jobs_applied_to_info()
#                     #TODO: If the button is present click OTHERWISE just insert the link
#                     if self.company_other_openings_href:
#                         self.company_other_openings_href.click()
#                     else:
#                         self.browser.get(self.company_other_openings_href)
#                     return
#                 elif not apply_to_job:
#                     #TODO:
#                     self.company_other_openings_href.click()
#                     return
#                 # except:
#                 #     raise ("Something went wrong with the the greenhouse.io job_description page")
#             elif opening_link_company_jobs:
#                 #TODO: parse through other_company_jobs for "lever"
#                 #self.company_job_openings(soup, None, application_company_name)
#                 return
#             application = opening_link_application
        













#         elif application_company_name == "greenhouse":
#             div_main = soup.find("div", id="main")
#             job_description_element = self.browser.find_element(By.ID, "content")
            
#             #I did it this way because it checks very few elements since 1 of these options are normally literally the next element
#             next_elem = div_main.find_next()
#             while next_elem:    #NOTE: REMEBER THIS DOESN'T INCREMENT next_elem SO IT'S THE SAME VALUE AS ABOVE!!!!
#                 if next_elem.name == "div" and (next_elem.get("id") == "flash-wrapper" or next_elem.get("id") == "flash_wrapper"):
#                     print('-Job Listings Page')
#                     return
#                 elif (next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper"):
#                     print('-Job Listings Page')
#                     return
#                 elif (next_elem.name == "section" and next_elem.get("class") == "level-0"):
#                     print("-Company Job Openings Page")
#                     print("A while loop for this is perfect for this because there can be multiple <section class='level-0'>")
#                     #TODO: for this one in the elif you have to look through all "level-0" sections!!
#                     return
#                 elif next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"]:
#                     app_body = next_elem
#                     header = next_elem.find("div", id="header")
#                     content = next_elem.find("div", id="content")
                    
#                     if header and content:
#                         print("Job Description Page")
#                         #TODO: Fix this!!! I need the header link!
#                         self.greenhouse_io_header(app_body, header, content)    #TODO: return *job_title, company, location, ???*
#                         should_apply = self.should_user_apply()
#                         if should_apply == True:
#                             #This should setup the code so that it's lookin down the barrell of the application! Everything should already be setup!!!
#                             self.bottom_has_application_or_button()
#                         elif should_apply == False:
#                             try:
#                                 self.company_other_openings_href.click()
#                             except:
#                                 self.browser.get(self.company_other_openings_href)
#                             time.sleep(2)
#                             return
                            
#                         #TODO
#  #! ^ MOVE UP 198 ^ ^ ^ ^ ^ ^ ^                       apply_button = div_main.find("button", text=["Apply Here", "Apply Now"])  #NOTE: !!!!! Maybe greenhouse doesn't have <button> ...    maybe it only has <a class="button">!?!?!?
#                         #application_below_description = div_main.find("div", id="application")
#                         #NOTE: I don't think greenhouse.io house <... target="_blank">
#                         #if apply_button:
#                             #print("\tPress button to go to application")
#                             #should_apply = self.should_user_apply()
#                             #print("\t\tApply button: ", end="")
#                             #print(apply_button)
#                             #if should_apply == True:
#                                 #apply_button.click()
#                                 #time.sleep(5)
#                                 #self.greenhouse_io_application(application)
#                             #print("\t\tApplication = ", end="")
#                             #print(application)
#                             #apply_to_job = self.should_user_apply(application)
#                             #return application
#                         #elif application:
#                             #self.should_user_apply(application)
#                             #print("\tApplication at bottom of page")
                            
#                         else:
#                             print("\tHmmm that's weird ? it's neither button nor application")
                        
#                         # self.scroll_to_element(job_description_element)
#                         # if apply_to_job == True:
#                         print("1st greenhouse application locked and loaded")
#                         form_input_details = self.get_form_input_details(job_link)
#                         print("Meet")
#                         time.sleep(8)
#                         self.insert_resume()
#                         print("me")
#                         time.sleep(8)
#                         self.fill_out_application(form_input_details)
#                         self.keep_jobs_applied_to_info(job_link)
#                         # elif apply_to_job == False:
#                         #     self.a_href.click()
#                         #     time.sleep(4)
#                         #     return
#                     break
#                 else:
#                     next_elem = next_elem.find_next()
#             print("Not really sure how the heck we got here and defintiely don't have a clue about where to go from here!?!?!?")
#             return
























    #TODO
    # user_desired_worplaceType = [ 1 || 2 || 3 || 4 || 5 || 6 || 7 || 8 || 9 || 2 || 1 || 2 || 1 || 2]
    # 1 = ONLY remote (under no circumstances will you ever go in)
    # 2 = ONLY in-office (under no circumstances are you trusted with work getting done at home) | check locations match
    # 3 = 
    # 4 = 
    # 5 = 
    # 6 = 
    # 7 = 
    # 8 = 
    # 9 = 
    # def users_basic_requirements_job_location(self, company_job_workplaceType, company_job_location):
    #     if company_job_workplaceType == None:
    #         for desired_location in self.user_desired_location:
    #             if desired_location not in company_job_location:
    #                 if 'hybrid' in company_job_location:
    #                     if user_desired_state not in self.get_state(company_job_location):
    #                         return False
    #                 if 'remote' in company_job_location:
                        
    #     elif company_job_workplaceType == 'hybrid':
    #         if self.user_desired_location is not None:
    #             for desired_location in self.user_desired_location:
    #                 if desired_location not in company_job_location:
    #                     re
        
    #     elif company_job_workplaceType == ""

















