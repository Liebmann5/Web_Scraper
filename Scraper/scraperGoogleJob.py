from urllib import request
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import csv

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
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

class scraperGoogleJob():
    
    def __init__(self, list_of_links, browser):
        self.list_of_links = list_of_links
        self.browser = browser
        self.company_job_title = None
        self.company_name = None
        self.company_job_location = None
        self.company_other_openings_href = None
        #This and apply can be temporary/method variables
        #self.a_fragment_identifier = None
        
        self.app_comp = None
        
    
    def convert_csv_data(self):
        #job_data = '../job_data.csv'
        with open ('job_data.csv', mode='r') as file:
            reader = csv.reader(file)
            csv_data = []
            for row in file:
                csv_data.append(row)
                #print(csv_data)
        return csv_data
    
    def write_to_csv(self, job_data):
        with open ('job_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            #for row in writer:
            writer.writerow(job_data)
        return "All done!"
    
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
    
    def eff_that_link(self):
        print('Coolio, waiting...')
        time.sleep(5)
        print("Eff that old website! Out with the old in with the new!!")
        #url = "https://boards.greenhouse.io/doubleverify/jobs/6622484002"
        url="https://jobs.lever.co/govini/cc5f740a-7248-4246-8b77-e28ed27dd46d/apply"
        self.browser.get(url)
        time.sleep(4)
        #form_input_details = self.get_form_input_details_jew(url)
        form_input_details = self.get_some_form_input_details(url)
        self.print_form_details(form_input_details, ".get_some_form_input_details()")
        #self.print_form_details(form_input_details, ".get_form_input_details_jew()")
        # jack = self.get_form_input_details(url)
        # self.print_form_details(jack, ".get_form_input_details()")
        # jill = self.get_some_form_input_details(url)
        # self.print_form_details(jill, ".get_some_form_input_details()")
        
        # matching_indices = self.compare_form_input_details(jack, jill)
        # print(f"Matching input elements: {matching_indices}")
        # print('\n')
        # print(len(matching_indices))
        # print(len(jack))
        # print(len(jill))
        # self.print_pairs(matching_indices, jack, jill)
        
        print("You've done it all your hard work is done! Definitely wasn't worth it but whatever. Never doin that crap again.")
        time.sleep(5)
        #form_input_details = get_form_input_details(url)
        
    def compare_form_input_details(self, jack, jill):
        matches = []
        for i, jack_element in enumerate(jack):
            for j, jill_element in enumerate(jill):
                if jack_element['HTML'] == jill_element['html']:
                    #matches.append((i, j))   # < They are backwards here!!
                    matches.append((j+1, i+1))
        matches_length = len(matches)
        print(matches_length)
        return matches
    
    def print_pairs(self, matches, jack, jill):
        matches_length = len(matches)
        print(matches_length)
        count = 0
        for x, y in matches:
            print('\n')
            print('This is the pair number: ', end="")
            print(count)
            print(x)
            print(y)
            print(jack[y])
            print(jill[x])
            count += 1
        print("All done!")
    
    def click_last_result(self, google_search_name):
        #self.list_of_links = var_job_link
        google_link_title = google_search_name
        application_company = None
        
        
        
        self.eff_that_link()
        
        
        
        
        
        for job_index in self.list_of_links[::-1]:
            print("D")
            d = "h"
            if d == "d":
                h3_element = self.browser.find_element(By.XPATH, '//h3')
                ancestor_element = h3_element.find_element(By.XPATH, './ancestor::*')
                print(ancestor_element.get_attribute('outerHTML'))
                #linky = self.browser.get(job_index)
                #print(linky)
                print("\D/")
                selenium_google_link = self.browser.find_element(By.XPATH, f'//a/h3[text()="{google_search_name}"]')
                parent_a_tag_xpath = selenium_google_link.find_element(By.XPATH, '..').get_attribute('outerHTML')
                print(parent_a_tag_xpath)
                print("Defence")
            selenium_google_link = self.browser.find_element(By.XPATH, f'//ancestor::a/h3[not(descendant::br)][contains(text(), "{google_search_name}")]')
            selenium_google_link.click()
            self.browser.implicitly_wait(5)
            time.sleep(3)
            
            
            self.eff_that_link()
            
            
            result = requests.get(job_index)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')
        
            if "jobs.lever.co" in job_index:
                application_company = "lever"
                self.app_comp = application_company
                
                #self.link_to_other_company_openings(soup, application_company)
                apply_to_job, applic = self.convert_to_bs(job_index, soup, application_company)
                if apply_to_job:
                    self.fill_out_application(applic)
                self.lever_io_data(job_index, soup)
                self.find_and_organize_inputs(applic, soup)
                
            elif "boards.greenhouse.io" in job_index:
                application_company = "greenhouse"
                self.app_comp = application_company
                
                #self.link_to_other_company_openings(soup, application_company)
                apply_to_job, applic = self.convert_to_bs(job_index, soup, application_company)
                if apply_to_job:
                    self.fill_out_application(applic, soup)
                    #self.other_job_openings(self.link_to_other_jobs)
                #applic = self.greenhouse_io_start_page_decider(soup)
                applic = soup.find('div', id="application")
                self.find_and_organize_inputs(applic)
    #! div_main ==> lever.co = job_description
    #This checks the header for other company links and then buttons to apply as well?           
    # def link_to_other_company_openings(self, soup, application_company):
    #     plethora_of_jobs = None
    #     if application_company == "lever":
    #         other_company_jobs = soup.find('div', {"class": 'page show'})
    #         company_open_positions = other_company_jobs.find('a', {"class": "main-header-logo"})
    #         if company_open_positions['href']:
    #             plethora_of_jobs = company_open_positions['href']

    #         print("Couldn't find the logo with the lick to plethora_of_jobs")
    #     elif application_company == "greenhouse":
    #         div_main = soup.find("div", id="main")
    #         a_tag = soup.find('a', text='View all jobs')
    #         if a_tag:
    #             a_tag_inner_html = a_tag.decode_contents()
    #             plethora_of_jobs = a_tag_inner_html['href']
    #     print("Here1")
    #     print(plethora_of_jobs)
    #     print("Here2")
    #     return plethora_of_jobs
    
    def convert_to_bs(self, job_index, soup, application_company):
        #! For lever.co there is no set div_main... it depends on what the opening_page is!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if application_company == "lever":
            #! I think this code goes in lever_header
            #other_company_jobs_url = self.lever_co_header(soup)
            
            #! div_main ==> lever.co = job_application
            opening_link_application = soup.find('div', {"class": 'application-page'})
            opening_link_description = soup.find('div', {"class": 'posting-page'})
            #! if it opens here IMMEDIATELY get the current url from the top!!!!!!!
            #! div_main ==> lever.co = company_job_openings
            opening_link_company_jobs = soup.find('div', {"class": "list-page"})
            
            #3 openinng page possibilities [Job Description/Application/Company Openings]
            if opening_link_application:
                
                #!!!!!!!!!!!!!!! TAKE AWAY ONLY FOR TESTS !!!!!!!!!!!!!!!!!!!!!!
                self.fill_out_application(opening_link_application, soup)
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                div_main = opening_link_application
                try:
                    company_open_positions = soup.find('a', {"class": "main-header-logo"})
                    application_webpage_html = soup.find("div", {"class": "application-page"})
                    #Can't fill out the application without filtering through the job description 1st!!!
                    #! v this needs to go through the header 1st and get the link
                    #self.lever_co_header(soup, application_webpage_html, application_company)   #! Find div_main!!!!!
                    self.lever_co_header(soup)
                    if self.company_other_openings_href:
                        company_open_positions.click()
                        self.company_job_openings(soup)
                except:
                    #TODO: Change this Error type!
                    raise ConnectionError("ERROR: Companies other open positions are not present")
            elif opening_link_description:
                div_main = opening_link_description
                try:
                    a_tag_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
                    div_tag_butt = soup.find('div', {'data-qa': 'btn-apply-bottom'})
                    application_at_bottom = soup.find("div", id="application")
                    print("Application at bottom or <button>")
                    if a_tag_butt:
                        #print("== Application at bottom of page")
                        print("== Press button to go to application")
                        has_apply_button = a_tag_butt
                        apply_to_job = self.apply_yes_or_no(opening_link_description)
                    elif div_tag_butt:
                        print("== Press button to go to application")
                        has_apply_button = div_tag_butt
                        apply_to_job = self.apply_yes_or_no(opening_link_description)    #apply_to_job = boolean | T=.click() && F=.lever_header() -> .company_job_openings()
                    if apply_to_job == True:
                        self.insert_resume()
                        self.find_and_organize_inputs(application_at_bottom)
                    elif not apply_to_job:
                        #TODO:
                        self.company_other_openings_href.click()
                        self.company_job_openings(soup, div_main, application_company)
                except:
                    raise "Something went wrong with the the greenhouse.io job_description page"
            elif opening_link_company_jobs:
                #TODO: parse through other_company_jobs for "lever"
                self.company_job_openings(soup, None, application_company)
            application = opening_link_application
                
        elif application_company == "greenhouse":
            div_main = soup.find("div", id="main")
            #I did it this way because it checks very few elements since 1 of these options are normally literally the next element
            next_elem = div_main.find_next()
            while next_elem:    #NOTE: REMEBER THIS DOESN'T INCREMENT next_elem SO IT'S THE SAME VALUE AS ABOVE!!!!
                if next_elem.name == "div" and (next_elem.get("id") == "flash-wrapper" or next_elem.get("id") == "flash_wrapper"):
                    print('-Job Page')
                    #return soup.find("div", id="flash-wrapper")
                    #break
                    flash_wrapper = soup.find("div", id=["flash-wrapper", "flash_wrapper"])
                    #Ex)https://boards.greenhouse.io/luminar
                    print("******* Flash_Wrapper = ")
                    print(flash_wrapper)
                    print("*******")
                    self.company_job_openings(soup, div_main, application_company)
                    return
                elif (next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper"):
                    print('-Job Listings Page')
                    #return soup.find("div", id="embedded_job_board_wrapper")
                    embedded_job_board = soup.find("div", id="embedded_job_board_wrapper")
                    self.company_job_openings(soup, div_main, application_company)
                    return
                elif (next_elem.name == "section" and next_elem.get("class") == "level-0"):
                    print("-Company Job Openings Page")
                    print("A while loop for this is perfect for this because there can be multiple <section class='level-0'>")
                    #TODO: for this one in the elif you have to look through all "level-0" sections!!
                    self.company_job_openings(soup, div_main, application_company)
                    return soup.find("section", {"class": "level-0"})
                elif next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"]:
                    app_body = next_elem
                    header = next_elem.find("div", id="header")
                    content = next_elem.find("div", id="content")
                    application = soup.find("div", id="application")
                    if header and content:
                        print("Job Description Page")
                        #self.link_to_other_company_openings(soup, application_company)
                        #self.company_job_openings(self, soup, div_main, application_company)
                        self.greenhouse_io_header(app_body, header, content)    #TODO: return *job_title, company, location, ???*
                    #else:
                        print("Application at bottom or <button>")
                        apply_button = div_main.find("button", text="Apply Here")
                        #TODO
 #! ^ MOVE UP 198 ^ ^ ^ ^ ^ ^ ^                       apply_button = div_main.find("button", text=["Apply Here", "Apply Now"])  #NOTE: !!!!! Maybe greenhouse doesn't have <button> ...    maybe it only has <a class="button">!?!?!?
                        #application_below_description = div_main.find("div", id="application")
                        #NOTE: I don't think greenhouse.io house <... target="_blank">
                        if apply_button:
                            print("== Press button to go to application")
                            apply_button.click()
                            time.sleep(5)
                            #self.greenhouse_io_application(application)
                            print("Application = ", end="")
                            print(application)
                            apply_to_job = self.apply_yes_or_no(application)
                            #return application
                        elif application:
                            #self.apply_yes_or_no(application)
                            print("== Application at bottom of page")
                            
                            apply_to_job = self.apply_yes_or_no(content)
                        else:
                            print("Hmmm that's weird ? it's neither button nor application")
                            
                        if apply_to_job == True:
                            self.fill_out_application(application, soup)
                            #self.insert_resume(application)
                            #self.find_and_organize_inputs(application) #! <-- Change application to application_form!!!!
                        elif apply_to_job == False:
                            self.a_href.click()
                            time.sleep(4)
                            self.company_job_openings(soup, div_main, application_company)
                            return
                    break
                else:
                    next_elem = next_elem.find_next()
            self.company_other_openings_href.click()
            time.sleep(7)
            return apply_to_job, application
            #return
    
    
    
        #everything_about_job = app_body.get_text()
        #apply_yes_or_no(everything_about_job)
    #greenhouse(job_description) => app_body
    def apply_yes_or_no(self, job_description):
        everything_about_job = job_description.get_text()
        #semen = everything_about_job.prettify()
        #print(everything_about_job)
        #experience_needed = r"\b\d+\s*(year|yr)s?\s+of\s+experience\b"
        experience_needed = "You must be a diety; being a demigod or demigoddess is literally embarrassing... just go back to coloring if this is you. Literally useless & pathetic ewww"
        if re.search(experience_needed, everything_about_job):
            print("Experience requirement found!")
            print(re.search(experience_needed, everything_about_job))
            return False
        else:
            print("No experience requirement found!")
            print(re.search(experience_needed, everything_about_job))
            return True
        #csv_data = self.convert_csv_data()
        #job_exp_needed = everything_about_job.find()
    
    def company_job_openings(self, soup, div_main, application_company):
        #greenhouse.io == <div id="main">   =>   lever.co == ??? [?postings-wrapper?] -> maybe 'page-centered'
        #greenhouse.io == <section class="level-0">   =>   lever.co == <div class="postings-group">
        #greenhouse.io == <section class="level-1">   =>   lever.co == <div class="posting">
        print("Application Company = " + application_company)
        if application_company == 'lever':
            #just getting a better(more narrowed result) filter
            postings_wrapper = soup.find('div', class_="postings-wrapper")
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
                        span_tag = job_opening_href.find('span', {'class', 'sort-by-location'})
                        span_tag_company_team = job_opening_href.find('span', {'class': 'sort-by-team'})
                        span_tag_workplaceTypes = job_opening_href.find('span', {'class': 'workplaceTypes'})
                        if span_tag:
                            job_opening_location = span_tag.text
                        #job_opening_href.click()
            self.print_to_console("company_job_openings", application_company, JobTitle=job_title, JobLocation=job_opening_location, WorkPlaceTypes=span_tag_workplaceTypes, CompanyDepartment=company_department, JobTeamInCompany=span_tag_company_team, JobHREF=job_link, ButtonToJob=button_to_job_description)
            return
        
        if application_company == 'greenhouse':
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
                        job_link = job_opening_href.get('href')
                        span_tag = job_opening.find('span', {'class', 'location'})
                        if span_tag:
                            job_opening_location = span_tag.text
                            print(job_opening_location)
                        #job_opening_href.click()
                if count == 20:
                    break
                print("-------")
            self.print_to_console("company_job_openings", application_company, JobTitle=job_title, JobLocation=job_opening_location, ButtonToJob=job_link)
        return
    
    def lever_co_header(self, soup):
        app_body = soup.find("div", id=["app_body", "app-body"])
        
        #other_company_openings = soup.find('div', {"class": 'page show'})
        other_company_openings = app_body.find('div', {"class": 'page show'})
        company_open_positions = other_company_openings.find('a', {"class": "main-header-logo"})
        try:
            if company_open_positions['href']:
                plethora_of_jobs = company_open_positions['href']
                print(plethora_of_jobs)
                other_company_jobs_url = plethora_of_jobs
        except:
            print("This company has no ALL job openings page!")
            other_company_jobs_url = "This company has no ALL job openings page!"
        return other_company_jobs_url
    
    
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
                continue
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
            else:
                print("child = ")
                print(child)
            #self.company_openings_test_link = 
        if self.company_other_openings_href == None:
            self.print_to_console("greenhous_io_header()", "greenhouse", JobTitle=self.company_job_title, CompayName=self.company_name, JobLocation=self.company_job_location, JobHREF="Couldnt Find", LinkToApplicationOnPageID=self.a_fragment_identifier)
        else:
            self.print_to_console("greenhous_io_header()", "greenhouse", JobTitle=self.company_job_title, CompayName=self.company_name, JobLocation=self.company_job_location, JobHREF=self.company_other_openings_href, LinkToApplicationOnPageID=self.a_fragment_identifier)
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
    
    def fill_out_application(self, applic, soup):
        self.insert_resume()
        form_data = self.find_and_organize_inputs(applic, soup)
    
    #! FIND AND ATTACH RESUME 1st B/C AUTOFILL SUCKS
    def insert_resume(self):
        print("=== .insert_resume()")
        
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
                print("That's some bull crap! Can't scroll")
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(2)
        print("1")
        
        #resume_path = "get from .env file"
        #resume_path = r"C:\Users\user\OneDrive\Desktop\Nicholas_Liebmann_Resume_23.pdf"
        resume_path = r"/Users/nliebmann/Downloads/Nicholas_Liebmann_Resume_23.pdf"
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
                print("7")
                #resume_upload_button[0].click()
                #resume_upload_button.click()
                #file_popup_window = self.browser.window_handles[1]
                time.sleep(1)
                print("8")
                input_elements = self.get_input_tag_elements()
                
                #NOTE: [https://dev.to/razgandeanu/how-to-upload-files-with-selenium-3gj3]
                # input_element, is_visible = self.find_visible_input('input[data-qa="input-resume"]')
                input_element, is_visible = self.find_visible_input('input[type="file"]')
                print("Bargain-Mart")
                print((input_element, is_visible))
                
                #input_elements = self.get_input_elements()
                
                upload_input = self.browser.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                upload_input.send_keys(resume_path)
                print("8.1")
                time.sleep(2)
                              
                # self.browser.switch_to.window(file_popup_window)
                # self.browser.close()
                # self.browser.switch_to.window(self.browser.window_handles[0])
                
                # print("SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX")
                # # upload_frame = self.browser.find_element(By.CSS_SELECTOR, 'iframe[src*="greenhouse.io/applications/upload"]')
                # upload_frame = self.browser.find_element(By.XPATH, 'iframe[source="attach"]')
                # print("9")
                # self.browser.switch_to.frame(upload_frame)
                # print("10")
                
                # upload_input = self.browser.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                # print("11")
                # upload_input.send_keys(resume_path)
                # print("12")
                # time.sleep(5)
                
                # self.browser.switch_to.default_content()
                print("13")
            else:
                raise Exception('Could not find resume upload element')
        print("14 Holy Crap")
        return
    
    def find_visible_input(self, selector):
        input_element = self.browser.find_element(By.CSS_SELECTOR, selector)
        is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
        if is_hidden:
            self.browser.execute_script("arguments[0].style.display = 'block';", input_element)
            is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
        return input_element, not is_hidden
    
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
       
       
    # def find_and_organize_inputs(self, applic, soup):
    #     """
    #     Finds all the input elements in a form and returns a list of dictionaries
    #     containing information about each input.
    #     """
    #     form_inputs = []
    #     input_types = ["text", "email", "password", "number", "checkbox", "radio", "date"]
    #     select_types = ["select"]
    #     textarea_types = ["textarea"]
    #     file_types = ["file"]
    #     input_elements = self.browser.find_elements(By.XPATH, "//form//input | //form//select | //form//textarea")
    #     for input_element in input_elements:
    #         input_type = input_element.get_attribute('type') or input_element.tag_name.lower()
    #         if input_type in input_types or input_type in select_types or input_type in textarea_types:
    #             input_label = ""
    #             input_values = []

    #             input_id = input_element.get_attribute('id')
    #             if input_id:
    #                 try:
    #                     input_label_element = self.browser.find_element(By.XPATH, f"//label[@for='{input_id}']")
    #                     input_label = input_label_element.text.strip()
    #                 except NoSuchElementException:
    #                     input_label = ""
    #             else:
    #                 parent_element = input_element.find_element(By.XPATH, '..')
    #                 while parent_element is not None:
    #                     try:
    #                         input_label_element = parent_element.find_element(By.XPATH, ".//label")
    #                         input_label = input_label_element.text.strip()
    #                         break
    #                     except NoSuchElementException:
    #                         parent_element = parent_element.find_element(By.XPATH, '..')
    #                 if not input_label:
    #                     input_label = parent_element.text.strip()

    #             if input_type in input_types:
    #                 if input_type == "checkbox":
    #                     if input_element.is_selected():
    #                         input_values.append(input_element.get_attribute('value'))
    #                 elif input_type == "radio":
    #                     radio_inputs = self.browser.find_elements(By.XPATH, "//form//input[@name='" + input_element.get_attribute('name') + "']")
    #                     radio_values = [radio.get_attribute('value') for radio in radio_inputs if radio.is_displayed()]
    #                     if radio_values:
    #                         input_values = radio_values
    #                 else:
    #                     input_values.append(input_element.get_attribute('value'))
    #             elif input_type in select_types:
    #                 select_options = input_element.find_elements(By.XPATH, ".//option")
    #                 input_values = [option.text.strip() for option in select_options]
    #             elif input_type in textarea_types:
    #                 input_values.append(input_element.get_attribute('value'))

    #             is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
    #             if is_hidden:
    #                 self.browser.execute_script("arguments[0].setAttribute('type', 'text');", input_element)
    #                 self.browser.execute_script("arguments[0].removeAttribute('style');", input_element)

    #             form_inputs.append({
    #                 "label": input_label,
    #                 "type": input_type,
    #                 "values": input_values,
    #                 "is_hidden": is_hidden
    #             })

    #     self.print_form_details(form_inputs)
    #     return form_inputs

    def get_form_input_detailsssssss(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        form_fields = soup.find_all(['input', 'textarea', 'button', 'select'])

        form_input_details = []

        for i, field in enumerate(form_fields, start=1):
            input_type = field.get('type')
            input_label = field.get('aria-label') or field.get('aria-labelledby') or field.get('placeholder') or field.get('title') or ""
            is_hidden = field.get('style') == 'display: none;' or input_type == 'hidden'
            input_html = str(field).strip()

            if field.name == 'button':
                input_type = 'button'
            elif field.name == 'textarea':
                input_type = 'textarea'
            elif field.name == 'select':
                input_type = 'select'

            values = []
            if input_type == 'select':
                options = field.find_all('option')
                for option in options:
                    values.append(option.text.strip())

            # Skip hidden fields without a label
            if is_hidden and not input_label:
                continue

            form_input_details.append({
                'label': input_label,
                'type': input_type,
                'values': values,
                'is_hidden': is_hidden,
                'html': input_html,
            })

        return form_input_details
    


    def get_label(self, input_element):
        # Case 1: Check if the label is a direct previous sibling of the input element
        label = input_element.find_previous_sibling('label')
        if label:
            return label.get_text(strip=True)

        # Case 2: Check if the label is inside a parent container
        parent = input_element.find_parent()
        if parent:
            label = parent.find('label')
            if label:
                return label.get_text(strip=True)
            else:
                label_text = ' '.join(label.stripped_strings)
                return label_text

        # Case 3: Check if the label is associated using the "for" attribute
        input_id = input_element.get('id')
        if input_id:
            label = input_element.find_previous('label', attrs={'for': input_id})
            if label:
                return label.get_text(strip=True)
        
        # Case 4: Check if the input_element has a placeholder attribute
        if not input_label:
            placeholder = input_element.get('placeholder')
            if placeholder:
                input_label = f"Placeholder ~ {placeholder}"

        return "SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX SEX"
    
    
    def get_labe_HERE_MF(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'
        
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

        if label:
            label_text = label.text.strip()
            return label_text

        # Case 5: Check if the input_element has a placeholder attribute
        placeholder = input_element.get('placeholder')
        if placeholder:
            return f"Placeholder ~ {placeholder}"

        return None

    def get_labemin(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'

        label_text = None
        label = input_element.find_previous_sibling('label')

        if label:
            # Get the text of the label element
            label_text = label.get_text(strip=True)

            # Check if there's an asterisk in the label text
            if '*' in label_text:
                # Remove everything after the asterisk
                label_text = label_text.split('*')[0].strip()

        # If the label text is still None, check if there's a placeholder attribute
        if not label_text:
            placeholder = input_element.get('placeholder')
            if placeholder:
                label_text = f"Placeholder ~ {placeholder}"

        return label_text
    
    def get_lab(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'
        
        
        label = None
        print('\n')
        print('-------------------------------------------------------------------')
        #print(input_element)
        # print('----------------------------')
        # print(input_id)
        # print('-------------------------------------------------------------------')
        # print('\n')

        # Case 1: Check if the label is a direct previous sibling of the input element
        label = input_element.find_previous_sibling('label')
        
        # Case 2: Check if the label is inside a parent container
        if not label:
            parent = input_element.find_parent()
            #print('----------------------------')
            #print(parent)
            if parent:
                label = parent.find('label')
                
        print('-------------------------------------------------------------------')
        
        # Case 3: Check if the label is associated using the "for" attribute
        if not label:
            input_id = input_element.get('id')
            print('----------------------------')
            #print(input_id)
            if input_id:
                label = input_element.find_previous('label', attrs={'for': input_id})
        
        # print('----------------------------')
        # print(parent)
        # print('----------------------------')
        # print(input_id)
        # print('----------------------------')
        #print(label)
        print('-------------------------------------------------------------------')
        print('\n')
        
        
        if label:
            #label_text = ' '.join(label.stripped_strings)
            label_text = label.text.strip()
            # Extract only the text content of the label, ignoring child tags
            #label_text = ' '.join(label.stripped_strings)
            label_text = label_text.split('*')[0].strip()
            label_text = ' '.join(label_text.split())
            #label_text = label_text.split('*')[0].split('\n')[0].strip()
            # Remove everything after the asterisk (*) or newline character (\n)
            #label_text = re.sub(r'(\*|\n).*', '', label_text).strip()
            #label_text = ' '.join(label_text.split())
            #label_text = label_text.split('\n')[0].strip()
            #return label_text.strip()
            # if '*' in label_text:
            #     label_text = label_text[:label_text.index('*')]
            #     input_sid = label_text[:label_text.index('*')]
            #     print('----------------------------')
            #     print(label_text)
            #     print('----------------------------')
            #     print(input_sid)
            # print('-------------------------------------------------------------------')
            # if '\n' in label_text:
            #     label_text = label_text[:label_text.index('\n')]
            #     input_sid = label_text[:label_text.index('\n')]
            #     print('----------------------------')
            #     print(label_text)
            #     print('----------------------------')
            #     print(input_sid)
            return label_text
        else:
            # Case 4: Check if the input_element has a placeholder attribute
            placeholder = input_element.get('placeholder')
            if placeholder:
                return f"Placeholder ~ {placeholder}"

        return None


    def get_form_input_details(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        input_elements = soup.find_all(['input', 'textarea', 'select'])

        input_details = []

        for i, input_element in enumerate(input_elements):
            details = {
                'Label': self.get_label(input_element),
                'Type': input_element.get('type'),
                'Values': [],
                'Is_Hidden': input_element.get('type') == 'hidden',
                'HTML': str(input_element)
            }
            if input_element.name == 'select':
                details['Values'] = [option.get_text(strip=True) for option in input_element.find_all('option')]
            input_details.append(details)

        return input_details



    # v v v v v v v v v v v v v v v v v v v v v v v v
    # def get_form_input_details(self, url):
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.content, 'html.parser')
        
    #     forms = soup.find_all('form')
    #     extracted_forms = []

    #     for form in forms:
    #         form_info = {
    #             'action': form.get('action', ''),
    #             'method': form.get('method', '').upper(),
    #             'fields': []
    #         }

    #         for field in form.find_all(['input', 'select', 'textarea']):
    #             field_info = {
    #                 'name': field.get('name', ''),
    #                 'type': field.get('type', ''),
    #                 'label': field.find_previous_sibling('label')
    #             }
    #             if field_info['label']:
    #                 field_info['label'] = field_info['label'].text.strip()
                
    #             form_info['fields'].append(field_info)

    #         extracted_forms.append(form_info)

    #     return extracted_forms


    # def find_and_organize_inputs(self, applic, soup):
    #     """
    #     Finds all the input elements in a form and returns a list of dictionaries
    #     containing information about each input.
    #     """
    #     form_inputs = []
    #     input_types = ["text", "email", "password", "number", "checkbox", "radio", "date"]
    #     select_types = ["select"]
    #     textarea_types = ["textarea"]
    #     file_types = ["file"]
    #     input_elements = self.browser.find_elements(By.XPATH, "//form//input | //form//select | //form//textarea")
    #     html_element = None

    #     for input_element in input_elements:
    #         html_element = input_element.get_attribute('outerHTML')
            
    #         #print(input_element.get_attribute('outerHTML'))  # Printing the HTML element
    #         print(html_element)
    #         input_type = input_element.get_attribute('type') or input_element.tag_name.lower()
    #         if input_type in input_types or input_type in select_types or input_type in textarea_types:
    #             input_label = ""
    #             input_values = []

    #             input_id = input_element.get_attribute('id')
    #             if input_id:
    #                 try:
    #                     input_label_element = self.browser.find_element(By.XPATH, f"//label[@for='{input_id}']")
    #                     input_label = input_label_element.text.strip()
    #                 except NoSuchElementException:
    #                     input_label = ""
    #             else:
    #                 parent_element = input_element.find_element(By.XPATH, '..')
    #                 while parent_element is not None:
    #                     try:
    #                         input_label_element = parent_element.find_element(By.XPATH, ".//label")
    #                         input_label = input_label_element.text.strip()
    #                         break
    #                     except NoSuchElementException:
    #                         parent_element = parent_element.find_element(By.XPATH, '..')

    #             if input_type in input_types:
    #                 if input_type == "checkbox":
    #                     if input_element.is_selected():
    #                         input_values.append(input_element.get_attribute('value'))
    #                 elif input_type == "radio":
    #                     radio_inputs = self.browser.find_elements(By.XPATH, "//form//input[@name='" + input_element.get_attribute('name') + "']")
    #                     radio_values = [radio.get_attribute('value') for radio in radio_inputs if radio.is_displayed()]
    #                     if radio_values:
    #                         input_values = radio_values
    #                 else:
    #                     input_values.append(input_element.get_attribute('value'))
    #             elif input_type in select_types:
    #                 select_options = input_element.find_elements(By.XPATH, ".//option")
    #                 input_values = [option.text.strip() for option in select_options]
    #             elif input_type in textarea_types:
    #                 input_values.append(input_element.get_attribute('value'))

    #             is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
    #             if is_hidden:
    #                 self.browser.execute_script("arguments[0].setAttribute('type', 'text');", input_element)
    #                 self.browser.execute_script("arguments[0].removeAttribute('style');", input_element)

    #             form_inputs.append({
    #                 "label": input_label,
    #                 "type": input_type,
    #                 "values": input_values,
    #                 "is_hidden": is_hidden,
    #                 "HTML": html_element
    #             })
    #     self.print_form_details(form_inputs)
    #     return form_inputs


      
       
    # def find_and_organize_inputs(self, applic, soup):
    #     """
    #     Finds all the input elements in a form and returns a list of dictionaries
    #     containing information about each input.
    #     """
    #     form_inputs = []
    #     input_types = ["text", "email", "password", "number", "checkbox", "radio", "date"]
    #     select_types = ["select"]
    #     textarea_types = ["textarea"]
    #     file_types = ["file"]
    #     input_elements = self.browser.find_elements(By.XPATH, "//form//input | //form//select | //form//textarea")
    #     for input_element in input_elements:
    #         input_type = input_element.get_attribute('type') or input_element.tag_name.lower()
    #         if input_type in input_types or input_type in select_types or input_type in textarea_types:
    #             input_label = ""
    #             input_values = []
                
    #         input_id = input_element.get_attribute('id')
    #         if input_id:
    #             try:
    #                 input_label_element = self.browser.find_element(By.XPATH, f"//label[@for='{input_id}']")
    #                 input_label = input_label_element.text.strip()
    #             except NoSuchElementException:
    #                 input_label = ""
    #         else:
    #             parent_element = input_element.find_element(By.XPATH, '..')
    #             while parent_element is not None:
    #                 try:
    #                     input_label_element = parent_element.find_element(By.XPATH, ".//label")
    #                     input_label = input_label_element.text.strip()
    #                     break
    #                 except NoSuchElementException:
    #                     parent_element = parent_element.find_element(By.XPATH, '..')
    #             if input_type in input_types:
    #                 if input_type == "checkbox":
    #                     if input_element.is_selected():
    #                         input_values.append(input_element.get_attribute('value'))
    #                 elif input_type == "radio":
    #                     radio_inputs = self.browser.find_elements(By.XPATH, "//form//input[@name='" + input_element.get_attribute('name') + "']")
    #                     radio_values = [radio.get_attribute('value') for radio in radio_inputs if radio.is_displayed()]
    #                     if radio_values:
    #                         input_values = radio_values
    #                 else:
    #                     input_values.append(input_element.get_attribute('value'))
    #             elif input_type in select_types:
    #                 select_options = input_element.find_elements(By.XPATH, ".//option")
    #                 input_values = [option.text.strip() for option in select_options]
    #             elif input_type in textarea_types:
    #                 input_values.append(input_element.get_attribute('value'))
                    
    #             is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
    #             if is_hidden:
    #                 self.browser.execute_script("arguments[0].setAttribute('type', 'text');", input_element)
    #                 self.browser.execute_script("arguments[0].removeAttribute('style');", input_element)
                
    #             form_inputs.append({
    #                 "label": input_label,
    #                 "type": input_type,
    #                 "values": input_values,
    #                 "is_hidden": is_hidden
    #             })
    #     self.print_form_details(form_inputs)
    #     return form_inputs
       
    def print_form_details(self, form_inputs, method_used):
        print('\n\n\n')
        # print("Form Input Details:")
        # for index, input_element in enumerate(form_inputs, start=1):
        #     print(f"Input {index}:")
        #     print(f"  Label: {input_element['label']}")
        #     print(f"  Type: {input_element['type']}")
        #     print(f"  Values: {input_element['values']}")
        #     print(f"  Is Hidden: {input_element['is_hidden']}")
        #     print(f"  HTML: {input_element['HTML']}")
        # print("\n")                       #^ HERE-go to input_elements: HTML key and get its value!!!!
        
        #print('\n\n\n')
        if method_used == ".get_some_form_input_details()":
            print("Form Input Details: ", end="")
            print(method_used)
            for i, detail in enumerate(form_inputs, start=1):
                print(f"Input {i}:")
                print(f"  Label: {detail['label']}")
                print(f"  Type: {detail['type']}")
                print(f"  Values: {detail['values']}")
                print(f"  Is Hidden: {detail['is_hidden']}")
                print(f"  HTML: {detail['html']}")
                print(f"  Dynamic: {detail['dynamic']}")
                print(f"  Related Elements: {detail['related_elements']}")
            print("\n")
            
        if method_used == ".get_form_input_details_jew()":
            print("Form Input Details: ", end="")
            print(method_used)
            for i, detail in enumerate(form_inputs, start=1):
                print(f"Input {i}:")
                print(f"  Label: {detail['label']}")
                print(f"  Type: {detail['type']}")
                print(f"  Values: {detail['values']}")
                print(f"  Is Hidden: {detail['is_hidden']}")
                print(f"  HTML: {detail['html']}")
            print("\n")
        
        # v v v v v v v v v v v v v v v v v v v v v v v v   ".get_form_input_details_jew()"
        # for i, form in enumerate(form_inputs, 1):
        #     print(f"Form {i}:")
        #     print(f"  Action: {form['action']}")
        #     print(f"  Method: {form['method']}")
        #     print("  Fields:")
        #     for j, field in enumerate(form['fields'], 1):
        #         print(f"    {j}. {field['label']} (Name: {field['name']}, Type: {field['type']})")
        
        if method_used == ".get_form_input_details()":
            print("Form Input Details: ", end="")
            print(method_used)
            for i, detail in enumerate(form_inputs, start=1):
                print(f"Input {i}:")
                print(f"  Label: {detail['Label']}")
                print(f"  Type: {detail['Type']}")
                print(f"  Values: {detail['Values']}")
                print(f"  Is Hidden: {detail['Is_Hidden']}")
                print(f"  HTML: {detail['HTML']}")
            print("\n")
        
        
    # def find_and_organize_inputs(self, applic, soup):
    #     from scraperGoogle import webdriver
    #     """
    #     Finds all the input elements in a form and returns a list of dictionaries
    #     containing information about each input.
    #     """
    #     #self.browser.get(form['url'])
    #     form_inputs = []
    #     input_types = ["text", "email", "password", "number", "checkbox", "radio"]
    #     select_types = ["select"]
    #     textarea_types = ["textarea"]
    #     file_types = ["file"]
    #     input_elements = self.browser.find_elements(By.XPATH, "//form//input | //form//select | //form//textarea")
        
        
    #     selenium_to_html = []
        
        
    #     for input_element in input_elements:
    #         self.print_input_element(selenium_to_html, (input_element.get_attribute("outerHTML")))
            
    #         input_type = input_element.get_attribute('type') or input_element.tag_name.lower()
    #         if input_type in input_types or input_type in select_types or input_type in textarea_types:
    #             input_label = ""
    #             input_values = []
    #             parent_element = input_element.find_element(By.XPATH, '..')
    #             while parent_element is not None:
    #                 try:
    #                     input_label_element = parent_element.find_element(By.XPATH, ".//label")
    #                     input_label = input_label_element.text.strip()
    #                     break
    #                 except NoSuchElementException:
    #                     parent_element = parent_element.find_element(By.XPATH, '..')
    #             if input_type in input_types:
    #                 if input_type == "checkbox":
    #                     if input_element.is_selected():
    #                         input_values.append(input_element.get_attribute('value'))
    #                 elif input_type == "radio":
    #                     radio_inputs = self.browser.find_elements(By.XPATH, "//form//input[@name='" + input_element.get_attribute('name') + "']")
    #                     radio_values = [radio.get_attribute('value') for radio in radio_inputs if radio.is_displayed()]
    #                     if radio_values:
    #                         input_values = radio_values
    #                 else:
    #                     input_values.append(input_element.get_attribute('value'))
    #             elif input_type in select_types:
    #                 select_options = input_element.find_elements(By.XPATH, ".//option")
    #                 input_values = [option.text.strip() for option in select_options]
    #             elif input_type in textarea_types:
    #                 input_values.append(input_element.get_attribute('value'))
                    
    #             is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
    #             if is_hidden:
    #                 self.browser.execute_script("arguments[0].setAttribute('type', 'text');", input_element)
    #                 self.browser.execute_script("arguments[0].removeAttribute('style');", input_element)
                
    #             form_inputs.append({
    #                 "label": input_label,
    #                 "type": input_type,
    #                 "values": input_values,
    #                 "is_hidden": is_hidden
    #             })
    #         self.print_form_inputs(form_inputs)
    #     print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #     print(len(form_inputs))
    #     self.print_input_element(selenium_to_html, "ready to party")
    #     self.print_form_inputs(form_inputs) 
    #     return form_inputs






    def print_form_inputs(self, form_inputs):
        for input in form_inputs:
            print("Label: " + input["label"])
            print("Type: " + input["type"])
            print("Values: " + str(input["values"]))
            print("Is Hidden: " + str(input["is_hidden"]))
            print("--------------------")
    
    def print_input_element(self, selenium_to_html, input_element):
        if input_element == "ready to party":
            count = 0
            for html_element in selenium_to_html:
                print((str(count)) + ": ", end="")
                print(html_element)
                count += 1
        else:
            selenium_to_html.append(input_element)

    def is_input_invisible(self, input_element):
        from scraperGoogle import webdriver
        """
        Checks if an input element is invisible to the user
        Returns True if the input is invisible, False otherwise
        """
        if input_element is None:
            return False
        
        # Check if input element itself is hidden
        if input_element.get_attribute("type") == "hidden" or input_element.get_attribute("style") == "display: none;":
            return True
        
        # Check if parent element is hidden
        print(input_element)
        print(type(input_element))
        parent_element = input_element.find_element(By.XPATH, '..')
        while parent_element is not None:
            if parent_element.get_attribute("style") == "display: none;":
                return True
            parent_element = parent_element.find_element(By.XPATH, '..')
        return False
    
    def print_form_data(self, form_data):
        for data in form_data:
            label_text = data[0]
            input_values = data[1:]
            input_tags = [input.get('name') + " (" + input.name + input.get('type') + ")" for input in data[1:]]
            print(f"label_text = {label_text}")
            print(f"input_tags = {input_tags}")
            print(f"input_values = {input_values}")
            print("-------------------")
        return print("Get Sucked Loser")
    
    def print_to_console(*args, **kwargs):
        print('\n\n\n')
        print('----------------------------------------------------------------------------------------------------')
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
    
    
    
    
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   
    
    
    
    
    
    
    
    
    
    
    
    
    
#  The O.G. idea/code   
#     def find_and_organize_inputs(self, applic, soup):
#         # selenium_soupy = self.browser.find_element(By.XPATH, "form[contains(lower-case(method), 'post')]")
#         selenium_soupy = self.browser.find_element(By.TAG_NAME, "form")
        
        
#         #label_elements = applic.find_elements(By.TAG_NAME, "label")
#         label_elements = selenium_soupy.find_elements(By.TAG_NAME, "label")
#         print(label_elements)
#         form_data = []
#         form_data_length = len(form_data)
        
#         for label_element in label_elements:
#             label_text = label_element.text.strip()
#             input_elements = []
#             input_id = label_element.get_attribute('for')
#             if input_id:
#                 input_elements.append(self.browser.find_element(By.ID, input_id))
#             else:
#                 input_elements = label_element.find_elements(By.XPATH, "./following-sibling::*[1]")
#             print("Well fudge!")
#             input_values = []
#             input_tags = []
#             for input_element in input_elements:
#                 if input_element.tag_name == "input":
#                     input_type = input_element.get_attribute('type')
#                     if input_type == "checkbox":
#                         input_values.append(input_element.get_attribute('value'))
#                     elif input_type == "radio":
#                         if input_element.get_attribute('name') not in [x[0] for x in form_data]:
#                             form_data.append([input_element.get_attribute('name'), []])
#                         form_data[[x[0] for x in form_data].index(input_element.get_attribute('name'))][1].append(input_element.get_attribute('value'))
#                     elif input_type in ["text", "email", "password", "number"]:
#                         input_values.append(input_element.get_attribute('value'))
#                     input_tags.append(input_element.get_attribute('name') + " (" + input_element.tag_name + " - " + input_type + ")")
#                 elif input_element.tag_name == "select":
#                     select_options = input_element.find_elements(By.XPATH, "./option")
#                     select_values = [option.get_attribute('value') for option in select_options]
#                     input_values.append(select_values)
#                     input_tags.append(input_element.get('name') + " (" + input_element.tag_name + ")")
#                 elif input_element.tag_name == "textarea":
#                     input_values.append(input_element.text.strip())
#                     input_tags.append(input_element.get('name') + " (" + input_element.tag_name + ")")
            
#             print(input_tags)
            
#             print("Well fudge...   wicked!")
#             form_data.append([label_text] + input_values)
#             input_tags = [""] + input_tags
#             #TODO: Don't think this is necessary to add so maybe 'comment' out later on down the road
#             form_data.append(input_tags)
#             if len(form_data) > form_data_length:
#                 form_data_length = len(form_data)
#             else:
#                 print("form_data_length = ", end="")
#                 print(form_data_length)
#                 print("len(form_data) = ", end="")
#                 print(len(form_data))
#         print("Well fudge that crap is wicked!")
#         self.print_form_data(form_data)
#         return form_data
    
    










#   This code works pretty darn well and the print statements are baller!!!!
# def find_and_organize_inputs(self, applic, soup):
#         element_is_hidden = False
#         form = self.browser.find_element(By.TAG_NAME, "form")
#         label_elements = form.find_elements(By.TAG_NAME, "label")
#         form_data = []
#         invisible_data = []
#         for label_element in label_elements:
#             label_text = label_element.text.strip()
#             input_elements = []
#             input_id = label_element.get_attribute('for')  #<label for="same"> = <input id="same">
#             print('\n')
#             print("label element text = " + label_text)
#             if(label_text == None):
#                 label_text = "Nothing"
#             print("label for && input id = ")
#             print("\t", end="")
#             print(input_id)
#             print("label element = ", end="")
#             label_xpath = f"//label[@for='{input_id}']"
#             print(self.browser.find_element(By.XPATH, label_xpath).get_attribute('outerHTML'))
#             if input_id:
#                 print("input element found by id = ")
#                 input_element = self.browser.find_element(By.ID, input_id)
#                 print(input_element.get_attribute('outerHTML'))
#                 input_elements.append(input_element)
#             else:
#                 print("input element found by sibling = ")
#                 input_element = label_element.find_elements(By.XPATH, "./following-sibling::*[1]")
#                 print(input_element.get_attribute('outerHTML'))
#                 input_elements = input_element
                
#             # Check if input element is hidden and make it visible
#             for input_element in input_elements:
#                 is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
#                 if is_hidden:
#                     element_is_hidden = True
#                     print("^^^^^HIDDEN^^^^^")
#                     print('\n')
#                     self.browser.execute_script("arguments[0].setAttribute('type', 'text');", input_element)
#                     self.browser.execute_script("arguments[0].removeAttribute('style');", input_element)
                    
#             print("Well fudge!----------------------------")
#             input_values = []
#             input_tags = []
#             for input_element in input_elements:
#                 if element_is_hidden == True:
#                     # Check if the input element is inside an invisible container.
#                     #if self.is_input_invisible(input_elements[0]):
#                     #    invisible_data.append([label_text] + input_values)
#                     #    invisible_data.append(input_tags)
#                     element_is_hidden = False
#                     break
#                 if input_element.tag_name == "input":
#                     input_type = input_element.get_attribute('type')
#                     if input_type == "checkbox":
#                         input_values.append(input_element.get_attribute('value'))
#                     elif input_type == "radio":
#                         if input_element.get_attribute('name') not in [x[0] for x in form_data]:
#                             form_data.append([input_element.get_attribute('name'), []])
#                         form_data[[x[0] for x in form_data].index(input_element.get_attribute('name'))][1].append(input_element.get_attribute('value'))
#                     elif input_type in ["text", "email", "password", "number"]:
#                         input_values.append(input_element.get_attribute('value'))
#                     input_tags.append(input_element.get_attribute('name') + " (" + input_element.tag_name + " - " + input_type + ")")
#                 elif input_element.tag_name == "select":
#                     select_options = input_element.find_elements(By.XPATH, "./option")
#                     select_values = [option.get_attribute('value') for option in select_options]
#                     input_values.append(select_values)
#                     input_tags.append(input_element.get('name') + " (" + input_element.tag_name + ")")
#                 elif input_element.tag_name == "textarea":
#                     input_values.append(input_element.text.strip())
#                     input_tags.append(input_element.get('name') + " (" + input_element.tag_name + ")")
#             print("Well fudge...   wicked!----------------")
#             form_data.append([label_text] + input_values)
#             input_tags = [""] + input_tags
#             form_data.append(input_tags)
            
#             # Check if the input element is inside an invisible container.
#             #if self.is_input_invisible(input_elements[0]):
#             #    invisible_data.append([label_text] + input_values)
#             #    invisible_data.append(input_tags)
        
#         print("----------------Well fudge that crap is wicked!----------------")
#         self.print_form_data(form_data)
#         return form_data, invisible_data






















    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #@classmethod
    def get_job_inf(self, var_job_link, browser, more_results_button):   #param == cls, job_link  |  self, var_search_results
        search_results = var_job_link
        name_of_job = more_results_button
        
        print("Search results = ")
        print(search_results)
        print("Length of search_results is ", end="")
        print(len(search_results))
        
        for job_index in search_results[::-1]:
            print("===Ballsack = name_of_job = ", end="")
            print(name_of_job)      #! ===Ballsack = more_results_button = Senior Software Developer - Tanda
            selenium_link_elemen = browser.find_element(By.XPATH, f'//ancestor::a/h3[text()="{name_of_job}"]')
            print("===Ballsack = selenium_link_element = ", end="")
            print(selenium_link_elemen)      #! ===Ballsack = link_element = <selenium.webdriver.remote.webelement.WebElement (session="8f0df2b5-f4d9-4d59-b7a0-f33cf55ee1e0", element="9f6f64fe-c0f4-41b8-8591-3e4e1ed09f05")>
            selenium_link_elemen.click()
            print("Waiting for link to load...")
            print("===Ballsack = job_index = ", end="")
            print(job_index)          #! ===Ballsack = _index = https://jobs.lever.co/Tanda/11d4cf5d-51d6-4219-89b0-a611300855ef
            browser.implicitly_wait(5)
            time.sleep(7)
            
            #get HTML from clicked webpage
            #try:
            result = requests.get(job_index)
            content = result.text
            print("1")
            soup = BeautifulSoup(content, 'lxml')
            print("2 - Extracting HTML was a success")
            #print(soup.prettify())       #! Prints the HTML -------->>>>>>> DOUBLE CHECK IT'S THE JOB_URL'S HTML!?!?!?
            
            if "jobs.lever.co" in job_index:
                print("===Ballsack = jobs.lever.co = 1")
                self.general_bs(soup)
                applic = self.lever_io_data(job_index, soup)
                self.find_and_organize_inputs(applic)
                print("===Ballsack = jobs.lever.co = 2")
                #scraperGoogleJob.lever_io_data(job_index, soup)
                # Captcha
                # <input id="hcaptchaResponseInput" type="hidden" name="h-captcha-response" value>
                # <button id="hcaptchaSubmitBtn" type="submit" class="hidden"></button>
            
            elif "boards.greenhouse.io" in job_index:
                print("===Ballsack = boards.greenhouse.io = 1")
                self.general_bs(soup)
                applic = self.greenhouse_io_start_page_decider(soup)
                applic = soup.find('div', id="application")
                self.find_and_organize_inputs(applic)
                print("===Ballsack = boards.greenhouse.io = 2")
    #--------------------------------------------------------------------------------------------------
            elif "workday" in job_index:
                print("===Ballsack = workday = 1")
                self.workday_data(soup)
                print("===Ballsack = workday = 2")
            else:
                print("get_job_info() method else statement")
            print("Well that crap didn't work out!!")
        print("Well sue me silly!")
        self.lever_io_application(self, "application_link", "application_webpage_html")
        return "ok"










    
    
    #filter out already applied jobs
    #traverse job webpage
    #?????
    def lever_io_dat(self, joby_link, soup):
        self.joby_link = joby_link
        print("===Ballsack = inside the lever.co")
        #opening_link_application = soup.find('div', class_='page-application')      #application immediate
        opening_link_application = soup.find('div', {"class": 'application-page'})
        #opening_link_description = soup.find('div', class_='page-show')             #regular description start
        opening_link_description = soup.find('div', {"class": 'posting-page'})          #NOTE: In HTML class='one two' needs 2 class calls I think!?!?!?
        print("===Ballsack = opening_link_application = ", end="")
        #print(opening_link_application)
        print("You are on the Job Application webpage")
        print("===Ballsack = opening_link_description = ", end="")
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
                print("===Ballsack = plethora_of_jobs = ", end="")
                print(plethora_of_jobs)
                application_webpage_html = soup.find("div", {"class": "application-page"})
                self.lever_io_application(joby_link, application_webpage_html)
                #return opening_link_application
            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        elif opening_link_description:
            print("===Ballsack = lever.co is working")
            try:
                print("===Ballsack = inside the try lever.co")
                position_title = soup.find('h2')
                job_title = position_title.get_text().split()
                print("===Ballsack = job_title = ", end="")
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
                    link_to__apply = a_tag_butt['href']
                
                print("===Ballsack = link_to_apply = ", end="")
                print(link_to_apply)

            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        #print("===Ballsack = leaving the lever.co")
        return soup

    def lever_io_applicatio(self, application_link, application_webpage_html):
        job_form_html = application_webpage_html.find("form", id="application-form", method="POST")
        #? Nick was here
        # application_section_html = job_form_html.find_all("h4")
        # #using ^this list .find() 1st <h4> then increment...
        # print(application_section_html)
        # for user_input in application_section_html:
        #     #loop through <input> tags and fill in using selenium!!
        #     print(user_input)
        # return 0
        for user_input in job_form_html.children:
            labels = user_input.find_all("label")
            for label in labels:
                needed_inpu = label.find("application-label")
                needed_input = needed_inpu.get_text()
                #TODO: call and retrieve the value of needed_input
                #! CLEAR !!!!!!!!! all input fields before you start typing
                for tag_type in label.find_all(True):
                    #if input_type.name in ['input', 'button', 'select', 'textarea']:
                    input_type = tag_type.name
                    if input_type == "input":
                        print("In .lever_io_application() found an <input>")
                        fill_in_input(needed_input, input_type)
                    elif input_type == "button":
                        print("In .lever_io_application() found an <button>")
                        fill_in_button(needed_input, input_type)
                    elif input_type == "select":
                        print("In .lever_io_application() found an <select>")
                        fill_in_select(needed_input, input_type)  #multiple choice
                    elif input_type == "textarea":
                        print("In .lever_io_application() found an <textarea>")
                        fill_in_textarea(needed_input, input_type)
    

#plethora_of_jobs (outter) = <meta property="og:url" content="https://jobs.lever.co/anduril/51af4cee-1380-439c-86c2-510863722099/apply">
#plethora_of_jobs (inner)  = 
    
    
    
    
    def application_or_butto(self, website):
        if(website == "greenhouse"):
            application = soup.find("div", id="application")
            
    
    
    
    
    
    
    
    
    
    
    
    
    #NOTE: These have the forms below the descriptions...       1st find "Apply for this Job" | 2nd go to each incremental <button> and <input>
    def greenhouse_io_dat(self, soup):
        print("Here")
        return 0
    
    
    #if id="app_body" and [check which page you are on]
    
    def greenhouse_io_start_page_decide(self, soup): #if (child of main is one of these)
        print("Welcome fair maiden we have gathered to make decisions based on your skin color... please after you!")
        div_main = soup.find("div", id="main")
        #print(div_main)
        next_elem = div_main.find_next()
        while next_elem:
            #print(next_elem)
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
#line 570 #elif child.name == "a"
            #if ("button" in child.get("class")) => remember !BUTTON! to click
    # def greenhouse_io_header(self, app_body, header, content): #! ^ ^ ^ ^
    #     print("===Ballsack = .greenhouse_io_header() = ")
    #     print(header)
    #     print("----------------------------------")
    #     first_child = True
    #     for child in header.children:
    #         if first_child:                 #! if child == '\n'
    #             first_child = False
    #             continue
    #         if child.name == "h1" and "app-title" in child.get("class"):
    #             company_job_name = child.get_text()
    #             print("company_job_name = ")
    #             print(company_job_name)
    #         elif child.name == "span" and  "company-name" in child.get("class"):
    #             company_name = child.get_text()    #"at Braintrust" => maybe look for 1st capital letter
    #             print("company_name = ")
    #             print(company_name)
    #         elif child.name == "a" and "button" in child.get("class"):     #as long as 'href' just exists
    #             all_jobs_available_a_href = child['href']  #! ^ ^ ^ ^ ^ ^ ^ ^ ^
    #             print("all_jobs_available_a_href 1 = ")
    #             print(all_jobs_available_a_href)
    #             #! If it opens on job_description see the bottom is 'apply_button' or 'job_application'
    #             # print("all_jobs_available_a_href 2 = ")
    #             # all_jobs_available_a_href = child.decode_contents()
    #             #print(all_jobs_available_a_href)
    #             #!since child is the <a> remember to click it!!!
    #             companies_jobs_link_a = child
    #         elif child.name == "div" and "location" in child.get("class"):
    #             company_job_location = child.get_text()
    #             print("company_job_location = ")
    #             print(company_job_location)
    #         else:
    #             print("child = ")
    #             print(child)
    #     return print("finished all over .greenhouse_io_header()")
    #     #self.greenhouse_io_content(app_body, content)
    #     return 
        
    def greenhouse_io_conten(self, app_body, content):
        for child in content.children:
            for childrens_child in child.children:
                strong_elem = childrens_child.find_next()
                while strong_elem:
                    if strong_elem.name == "stong":
                        description_title = strong_elem.get_text()
                        if description_title in "Requirements":
                            print("This is the very specific BS4 way to organize and look through job description!")
                    
        application = div_main.find("div", id="application")
        #TODO
        apply_button = div_main.find("button", text="Apply Here")
        if application:
            self.greenhouse_io_application(application)
        elif apply_button:
            apply_button.click()
            time.sleep(5)
            self.greenhouse_io_application(application)
            
    def greenhouse_io_applicatio(application):
        app_form = application.find("form", id="application_form", method="post")
        for user_input in app_form.children:
            if user_input.get_attr("type") and user_input["input"] == "hidden":
                print(user_input.prettify())
            elif user_input.name == "div" and user_input.get("id") == "main_fields":
                job_a(user_info)
            elif user_input.name == "div" and user_input.get("id") == "custom_fields":
                job_app_general(user_info)
            elif user_input.name == "div" and user_input.get("id") == "demographic_questions":
                job_app_general(user_info)
            elif user_input.name == "div" and user_input.get("id") == "eeoc_fields":
                job_app_general(user_info)
            elif user_input.name == "div" and user_input.get("id") == "submit_buttons":
                job_app_general(user_info)
            
    
            #For college start & end dates their's 2 input boxes
            #Current Employee end date skip ahead and find current employee check/button
            #Previously worked for company
    
    
    
    
    
    
    
    
            
    
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
    
    #Purpose of this method is to find all the inputs!!!
    #Goal is to make a list of lists' where the inside list .len()=3 index1=label.text(){gender} |
        #index2=input_type {<select>, <button>} | index3=empty & fill with user's value
    #maybe rather than have a .len()=3 just for input's keep appending all possible box input's{only
    #for <input> b/c sometimes multiple BUT not radio buttons} and FINALLY append user's value
    #eff it just find all the labels then all the inputs
    def find_and_organize_input(self, applic):
        print("===Ballsack = find_and_organize_inputs() = ", end="")
        print(applic)
        label_elements = applic.find_element(By.TAG_NAME, "label")
        form_data = []
        for label_element in label_elements:
            #text value of the <label>
            label_text = label_element.text.strip()
            
            #get all inputs after label
            user_input_type = []
            input_id = label_element.get_attribute('for')
            if input_id:
                input_elements.append(self.browser.find_element(By.ID, input_id))
            else:
                input_elements = label_element.find_elements(By.XPATH, "./following-sibling::*[1]")
                
            #get input types
            input_values = []
            for input_element in input_elements:
                if input_element.tag_name == "input":
                    if not input_element.get_attribute('type'):
                        print("type some crap")
                    else:
                        if input_element.get_attribute('type') == "checkbox":
                            print("CHECK FOR ALL POSSIBLE TYPES")
                elif input_element.tag_name == "select":
                    select_options = input_element.find_all(By.XPATH, "./option")
                    input_values.append(select_options.text.strip())
                elif input_element.tag_name == "button":
                    if not input_element.get_attribute('type'):
                        print("type some crap")
                    else:
                        if input_element.get_attribute('type') == "radio":
                            print("CHECK FOR ALL POSSIBLE TYPES")
                        elif input_element.get_attribute('type') == "submit":
                            print("Form Submit Button")
                elif input_element.tag_name == "textarea":
                    print("Type stuff dog")
            
            #Add the label and input types
            form_data.append([label_text] + input_values)
            
            for sublist in form_data:
                print(sublist)
            
            self.fill_in_input(form_data)
    
    
    def fill_in_inpu(form_data):
        print("user <input>")
        for user_form_question in form_data:
            print(user_form_question)
    
    #Figure out the section you are in
    #Figure out the <label>.get_text()
    #Figure out if it's a <select>/<radio>/<input>
    #if label
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #, website_root, job_url, job_name, company_name, job_location, job_style, apply_button, company_department, company_commitment
    def print_inf(self):
        print('\n\n\n')
        print('----------------------------------------------------------------------------------------------------')
        if self.website_root:
            print(f'\t-The website_root = ' + self.website_root)
        if self.job_url:
            print(f'\t-The job_url      = ' + self.job_url)
        if self.job_name:
            print(f'\t-The job_name     = ' + self.job_name)
        if self.company_name:
            print(f'\tThe company_name  = ' + self.company_name)
        if self.job_location:
            print(f'\t-The job_location = ' + self.job_location)
        if self.job_style:
            print(f'\t-The job_style    = ' + self.job_style)
        if self.apply_button:
            print(f'\t-The apply_button = ' + self.apply_button)
        if self.company_department:
            print(f'\t-The company_department = ' + self.company_department)
        if self.company_commitment:
            print(f'\t-The company_commitment = ' + self.company_commitment)
        print('----------------------------------------------------------------------------------------------------')
        print('\n\n\n')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def workday_dat(self, soup):
        print("Here")
        return 0

    def general_b(self, app_body):
        everything_about_job = app_body.get_text()
        print("===Ballsack = general_bs()... all the text in the job description = ")
        print("You'll never succeed here...")
        #print(everything_about_job)
        
        #filter the job out as needed
    
    def apply_to_jo(job_data: list):
        if (len(job_data)-1):
            return "ok"

    def get_application_value():
        if "phone" in label.lower():
            if "mobile" in label.lower() or "personal" in label.lower():
                #cell_phone_number = .env.get("PHONE_NUMBER")
                return cell_phone_number
            elif "home" in label.lower():
                #home_phone_number = .env.get("HOME_PHONE")
                return home_phone_number
            else:
                #cell_phone_number = .env.get("PHONE_NUMBER")
                return cell_phone_number







#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!       REMEMBER TO COUNT THE NUMBER OF OPEN SENIOR > ROLES AVAILABLE           !
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



#<cite class="qLRx3b tjvcx GvPZzd cHaqb" role="text" style="max-width:315px">https://jobs.lever.co<span class="dyjrff qzEoUe" role="text"> › ltaresearch</span></cite>

#<a href="/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=&amp;ved=2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB&amp;url=https%3A%2F%2Fjobs.lever.co%2Fltaresearch&amp;usg=AOvVaw1WnH3yWFh2qyF8H83db1P7" data-jsarwt="1" data-usg="AOvVaw1WnH3yWFh2qyF8H83db1P7" data-ved="2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB" data-ctbtn="0" data-cthref="/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=&amp;ved=2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB&amp;url=https%3A%2F%2Fjobs.lever.co%2Fltaresearch&amp;usg=AOvVaw1WnH3yWFh2qyF8H83db1P7" data-jrwt="1"><br><h3 class="LC20lb MBeuO DKV0Md">LTA Research</h3><div class="TbwUpd NJjxre iUh30 ojE3Fb"><span class="H9lube"><div class="eqA2re NjwKYd Vwoesf" aria-hidden="true"><img class="XNo5Ab" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAWlBMVEU+SEpvdXjIysvEx8edoaN4f4FOV1n6+vr////j5eVjamxyeXvZ2dn39/dqcXPNz9CLkJCqra7y8/PU1NRdZWfs7e7d3t5cY2ZTW12zt7hYXmKTmJp/hYe6vLweb9tYAAAAn0lEQVR4AcTPAxLAMBBA0TKszfsfs1acYf9w54XOT7meH4RA7SFEe5gonJ6OfF/vXhQBqcePR4nE3cvTaCsTPfl6lBtcXJAUp5enl8TgCefE0iPF+SavajtvFN6ynpq84rwzuNOfjlXuRIy3jnwB46FP+AWMZxAVCbvgcm/Y5xFtxfS7gPEAHcHpXVB/PUd32fPN+Sjo9oFGb906+uRTAOgAEo+qriNyAAAAAElFTkSuQmCC" style="height:18px;width:18px" alt=""></div></span><div><span class="VuuXrf">lever.co</span><div class="byrV5b"><cite class="qLRx3b tjvcx GvPZzd cHaqb" role="text" style="max-width:315px">https://jobs.lever.co<span class="dyjrff qzEoUe" role="text"> › ltaresearch</span></cite></div></div></div></a>




#<a href="/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=&amp;ved=2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB&amp;url=https%3A%2F%2Fjobs.lever.co%2Fltaresearch&amp;usg=AOvVaw1WnH3yWFh2qyF8H83db1P7" data-jsarwt="1" data-usg="AOvVaw1WnH3yWFh2qyF8H83db1P7" data-ved="2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB" data-ctbtn="0" data-cthref="/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=&amp;ved=2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB&amp;url=https%3A%2F%2Fjobs.lever.co%2Fltaresearch&amp;usg=AOvVaw1WnH3yWFh2qyF8H83db1P7" data-jrwt="1"><br><h3 class="LC20lb MBeuO DKV0Md">LTA Research</h3>









    #This is the BeautifulSoup way
    # def find_and_organize_inputs(application):
    #     app_form = application.find("form", id="application_form", method="post")
    #     application_user_input = []
    #     for count, input_needed in enumerate(app_form.children):
    #         #Find all hidden stuff
    #         if input_needed.get_attr("type") and input_needed.get("type") == "hidden":
    #             print(input_needed.prettify())
    #         if input_needed.get_attr("aria-hidden") and input_needed.get("aria-hidden") == "true":
    #             print(input_needed.prettify())
    #         for 
    
    
    
    
    































# ChatGPT:
# This accidentally might be a better option b/c all I care about is the department and then the job! So if they do have a bunch of sub-'levels'
# it's probably just like office names and then managers so not stuff we really care about!?!?!?
# from bs4 import BeautifulSoup

# html = '''
# <div id="main">
# <section class="level-0"></section>
# <section class="level-0"></section>
# <section class="level-0"></section>
#   <h3 id="4051531004">Research, Engineering, Product</h3>
#   <section class="child level-1">
#   <h4 id="4013603004">All teams (roles across multiple teams)</h4>
#   <div class="opening" department_id="4013603004,4051531004" office_id="4006308004" data-office-4006308004="true" data-department-4013603004="true" data-department-4051531004="true">
#       <a data-mapped="true" href="/openai/jobs/4050126004">Research Engineer</a>
#       <br>
#       <span class="location">San Francisco, California, United States</span>
#   </div>
#   <div class="opening" department_id="4013603004,4051531004" office_id="4006308004" data-office-4006308004="true" data-department-4013603004="true" data-department-4051531004="true">
#       <a data-mapped="true" href="/openai/jobs/4229594004">Research Scientist</a>
#       <br>
#       <span class="location">San Francisco, California, United States</span>
#   </div>
#  </section>

# <section class="child level-1">
#   <h4 id="4049554004">Applied AI Engineering</h4>

#   <div class="opening" department_id="4049554004,4051531004" office_id="4006308004" data-office-4006308004="true" data-department-4049554004="true" data-department-4051531004="true">
#   <a data-mapped="true" href="/openai/jobs/4857084004">Mobile Engineering Manager, ChatGPT</a>
#   <br>
#  </section>
#  <section class="child level-1"></section>
#  <section class="child level-1"></section>
#  <section class="child level-1"></section>
#  <section class="child level-1"></section>
#  </div>
# '''

# soup = BeautifulSoup(html, 'html.parser')
# main_div = soup.find('div', {'id': 'main'})

# sections = main_div.find_all('section', class_=lambda x: x and 'level' in x)

# for section in sections:
#     opening_div = section.find('div', {'class': 'opening'})
#     if opening_div:
#         a_tag = opening_div.find('a')
#         if a_tag:
#             job_title = a_tag.text
#             job_link = a_tag.get('href')
#             span_tag = opening_div.find('span', {'class': 'location'})
#             if span_tag:
#                 job_location = span_tag.text
#                 print(f'Title: {job_title}\nLink: {job_link}\nLocation: {job_location}\n')
#             else:
#                 print(f'Title: {job_title}\nLink: {job_link}\nLocation: N/A\n')
#             a_tag.click()
#         else:
#             print('No <a> tag found in the opening div')
#     else:
#         print('No opening div found in the section')






    # def get_form_input_details(self, url):
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.content, 'html.parser')

    #     form_fields = soup.find_all(['input', 'textarea', 'button', 'select'])

    #     form_input_details = []

    #     for i, field in enumerate(form_fields, start=1):
    #         input_type = field.get('type')
    #         input_label = field.get('aria-label') or field.get('aria-labelledby') or field.get('placeholder') or field.get('title') or ""
    #         is_hidden = field.get('style') == 'display: none;' or input_type == 'hidden'
    #         input_html = str(field).strip()

    #         if field.name == 'button':
    #             input_type = 'button'
    #         elif field.name == 'textarea':
    #             input_type = 'textarea'
    #         elif field.name == 'select':
    #             input_type = 'select'

    #         values = []
    #         if input_type == 'select':
    #             options = field.find_all('option')
    #             for option in options:
    #                 values.append(option.text.strip())

    #         # For radio buttons and checkboxes, find the ancestor element with a role of "group" or "radiogroup"
    #         if input_type in ('radio', 'checkbox') and not input_label:
    #             group = field.find_parent(attrs={"role": ["group", "radiogroup"]})
    #             if group:
    #                 input_label = group.get('aria-label') or group.get('aria-labelledby') or group.get('title') or ""

    #         # Skip hidden fields without a label
    #         if is_hidden and not input_label:
    #             continue

    #         form_input_details.append({
    #             'label': input_label,
    #             'type': input_type,
    #             'values': values,
    #             'is_hidden': is_hidden,
    #             'html': input_html,
    #         })

    #     return form_input_details














    def get_labe_ballsack(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'

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

        if label:
            label_text = label.text.strip()

            # If the asterisk (*) is present, remove everything after it
            if '*' in label_text:
                label_text = label_text.split('*')[0].strip() + '*'
            elif '✱' in label_text:
                label_text = label_text.split('✱')[0].strip() + '✱'
            else:
                # If the newline character (\n) is present, remove it and everything after it
                label_text = label_text.split('\n')[0].strip()

            return label_text

        # Case 5: Check if the input_element has a placeholder attribute
        placeholder = input_element.get('placeholder')
        if placeholder:
            return f"Placeholder ~ {placeholder}"

        return None
    
    
    
    
        
    def get_labia(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'
        
        if input_element.get('type') == 'radio':
            label = self.print_parent_hierarchy(input_element)
            return label

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
                
        # Case X: Check if the input element is a radio button inside a label element, and the desired label is the parent of all radio buttons
        # if not label:
        #     if input_element.get('type') == 'radio':
        #         radio_buttons_container = input_element.find_parent('ul')
        #         if radio_buttons_container:
        #             parent_label = radio_buttons_container.find_parent('label')
        #             if parent_label:
        #                 label_with_app_label = parent_label.find(lambda tag: 'class' in tag.attrs and 'application-label' in tag['class'])
        #                 if label_with_app_label:
        #                     label = label_with_app_label.text.strip()
        #                 else:
        #                     label = parent_label

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
    
    def get_labe_tests(self, input_element, soup):
        label = ''
        
        print("Finding label for:", input_element)  # Debugging line
        
        # 1. Check if the input element is wrapped within a label element
        parent_label = input_element.find_parent('label')
        if parent_label:
            label = parent_label.text.strip()
            print("Found label in parent:", label)  # Debugging line

        # 2. Check if there's a label element with a 'for' attribute that matches the input element's 'id'
        if not label:
            input_id = input_element.get('id')
            if input_id:
                matching_label = soup.find('label', attrs={'for': input_id})
                if matching_label:
                    label = matching_label.text.strip()
                    print("Found label by 'for' attribute:", label)  # Debugging line
        return None
    
    def get_labe(self, input_element, soup):
        parent_label = input_element.find_parent('label')
        if parent_label:
            label = ' '.join(parent_label.stripped_strings)
            return label

        if 'id' in input_element.attrs:
            label_element = soup.find('label', attrs={'for': input_element['id']})
            if label_element:
                return label_element.text.strip()

        return None

    
    # def print_parent_hierarchy(self, element, level=0):
    #     parent = element.parent
    #     if parent is None:
    #         return

    #     print(f"Level {level}: {parent.prettify()}")
    #     self.print_parent_hierarchy(parent, level + 1)
    
    def print_parent_hierarchy(self, element, stop_level=5):
        current_level = 0
        while (current_level <= stop_level):
            print(f"Level {current_level}:")
            if current_level == 0 or current_level == 5:
                if current_level == 0:
                    print(element.prettify())
                if current_level == 5:
                    sauce = element.next_element.get_text(strip=True)
                    print("EFF CHATGPT THAT THING IS GAY AND SUCKS BALLS: ", end='')
                    print(sauce)
                    return sauce
            element = element.parent
            current_level += 1

    
    def get_HERE_penis(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'
        
        # Check if the input_element is a radio button
        if input_element.get('type') == 'radio':
            # If the label is not found using the 'for' attribute, climb up the hierarchy
            element = input_element
            stop_level = 5
            current_level = 0
            top_label = None
            print('MADE IT HERE TWAT')
            print(input_element)
            while current_level <= stop_level:
                print("Current Level:")
                print(current_level)
                print("Top label found: " if element.name == 'label' else "Top label not found")
                if element.name == 'label' and not element.find('input', type='radio'):
                    top_label = element
                    print("HOMO dis da element")
                    #print(element)
                    #print(top_label)
                    multiple_choice_div = top_label.find('div', class_='application-label multiple-choice')
                    print("HOMO dis da multiple_choice_div")
                    print(multiple_choice_div)
                    child_text = multiple_choice_div.get_text(strip=True)
                    print("HOMO dis da child_text")
                    print(child_text)
                    return child_text

                    break
                print("------Element:")
                print(element)
                element = element.parent
                current_level += 1
            print("HOMO dis...")
            print("Top label found: " + top_label if top_label else "Top label not found")
            if top_label:
                print("HOMO dis da motha suckin hookers nuts")
                # Find the text inside the "application-label multiple-choice" div
                multiple_choice_div = top_label.find('div', class_='application-label multiple-choice')
                print("HOMO dis da multiple_choice_div")
                print(multiple_choice_div)
                if multiple_choice_div:
                    child_text = multiple_choice_div.get_text(strip=True)
                    print("HOMO dis da child_text")
                    print(child_text)
                    return child_text

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

        #print(f"Label for input_element: {label}")  # Debugging line

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












                                        #This is the one that works
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    #! Include checkboxes!!!!
    def get_some_form_input_details(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

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
            if input_type not in ['text', 'email', 'password', 'select', 'radio', 'checkbox', 'textarea', 'button'] and input_id != 'education_school_name':
                continue

            values = []
            if input_type == 'select':
                options = field.find_all('option')
                for option in options:
                    values.append(option.text.strip())

            if input_type == 'radio':
                #print("Radio button in get_some_form_input_details:", field)  # Debugging line
                radio_name = field.get('name')
                if radio_name in processed_radios:
                    continue
                processed_radios.add(radio_name)
                radio_group = soup.find_all('input', {'name': radio_name})
                values = [radio.get('value') for radio in radio_group]
                input_html = ''.join([str(radio).strip() for radio in radio_group])
                
                #radio_button = soup.find('input', attrs={'name': 'eeo[race]', 'type': 'radio'})
                #self.print_parent_hierarchy(radio_button)
                
                # Call get_label for the entire radio button group
                input_label = self.get_labia(field)
            else:
                # Call get_label for other input types
                input_label = self.get_labia(field)

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

        return form_input_details



#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$        
        
        
        
        
        
        
    def get_form_input_details_jew(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
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
            elif field.name == 'textarea':
                input_type = 'textarea'
            elif field.name == 'select':
                input_type = 'select'

            if input_id:
                label_element = soup.find('label', {'for': input_id})
                if label_element:
                    input_label = label_element.text.strip()

            if not input_label:
                placeholder = field.get('placeholder')
                if placeholder:
                    input_label = f"Placeholder ~ {placeholder}"

            values = []
            if input_type == 'select':
                options = field.find_all('option')
                for option in options:
                    values.append(option.text.strip())

            if input_type == 'radio':
                radio_name = field.get('name')
                if radio_name in processed_radios:
                    continue
                processed_radios.add(radio_name)
                radio_group = soup.find_all('input', {'name': radio_name})
                values = [radio.get('value') for radio in radio_group]
                label_element = field.find_previous_sibling('label')
                if label_element:
                    input_label = label_element.text.strip()
                input_html = ''.join([str(radio).strip() for radio in radio_group])

            if is_hidden and not input_label:
                continue

            form_input_details.append({
                'label': input_label,
                'type': input_type,
                'values': values,
                'is_hidden': is_hidden,
                'html': input_html,
            })

        return form_input_details

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# Input 25:
#   Label:
#   Type: button
#   Values: []
#   Is Hidden: False
#   HTML: <input class="button" id="submit_app" type="button" value="Submit Application"/>
# Input 26:
#   Label: School
#   Type: hidden
#   Values: []
#   Is Hidden: True
#   HTML: <input aria-required="false" class="school-name background-field" data-url="https://boards-api.greenhouse.io/v1/boards/doubleverify/education/schools" data-validators='[{"type":"notBlank","key":"SchoolNameRequired"}]' id="education_school_name" name="job_application[educations][][school_name_id]" placeholder="Select a School" type="hidden">
# <a class="remove-background-field" href="#"><img alt="Remove Education" src="https://boards.cdn.greenhouse.io/assets/svg/close-2388e0f798509ffdefd9fe48321955a399f62a302d4f33f96e798f2272a7b52d.svg"/></a>  
# </input>
# Input 27:
#   Label: Degree
#   Type: select
#   Values: ['', 'High School', "Associate's Degree", "Bachelor's Degree", "Master's Degree", 'Master of Business Administration (M.B.A.)', 'Juris Doctor (J.D.)', 'Doctor of Medicine (M.D.)', 'Doctor of Philosophy (Ph.D.)', "Engineer's Degree", 'Other']
#   Is Hidden: False
#   HTML: <select aria-required="false" class="degree background-field" data-placeholder="Select a Degree" data-validators='[{"type":"notBlank","key":"DegreeRequired"}]' id="education_degree" name="job_application[educations][][degree_id]"><option value=""></option>
# <option value="5387323002">High School</option>
# <option value="5387324002">Associate's Degree</option>
# <option value="5387325002">Bachelor's Degree</option>
# <option value="5387326002">Master's Degree</option>
# <option value="5387327002">Master of Business Administration (M.B.A.)</option>
# <option value="5387328002">Juris Doctor (J.D.)</option>
# <option value="5387329002">Doctor of Medicine (M.D.)</option>
# <option value="5387330002">Doctor of Philosophy (Ph.D.)</option>
# <option value="5387331002">Engineer's Degree</option>
# <option value="5387332002">Other</option></select>        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        