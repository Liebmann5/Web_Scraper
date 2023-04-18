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
    
    def deal_with_links(self, google_search_name):
        #self.list_of_links = var_job_link
        google_link_title = google_search_name
        application_company = None
        
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

    #def test_form_submission(self):
    def find_and_organize_inputs(self, applic, soup):
        # Find all form elements
        form_elements = self.browser.find_elements(By.XPATH, "//form//input | //form//select | //form//textarea")
        
        # Loop through each form element and fill it out
        for form_element in form_elements:
            # Check if form element is hidden or disabled
            if not form_element.is_displayed() or form_element.is_enabled():
                continue
            
            # Get form element tag name and type
            tag_name = form_element.tag_name.lower()
            input_type = form_element.get_attribute('type') or tag_name
            
            # Fill out the form element based on its type
            if input_type == "text" or input_type == "email" or input_type == "password" or input_type == "number":
                form_element.clear()
                form_element.send_keys("Test")
            elif input_type == "checkbox":
                form_element.click()
            elif input_type == "radio":
                radio_inputs = self.browser.find_elements(By.XPATH, "//form//input[@name='" + form_element.get_attribute('name') + "']")
                for radio_input in radio_inputs:
                    if radio_input.is_displayed() and radio_input.is_enabled():
                        radio_input.click()
            elif input_type == "select":
                select_options = form_element.find_elements(By.XPATH, ".//option")
                if select_options:
                    select_options[0].click()
            elif input_type == "textarea":
                form_element.clear()
                form_element.send_keys("Test")
            else:
                continue
            
            # Click on the submit button if present
            submit_buttons = self.browser.find_elements(By.XPATH, "//form//button[@type='submit'] | //form//input[@type='submit']")
            for submit_button in submit_buttons:
                if submit_button.is_displayed() and submit_button.is_enabled():
                    submit_button.click()
                    break
            
            # Verify that the form has been submitted successfully
            success_elements = self.browser.find_elements(By.XPATH, "//*[contains(text(), 'success')]")
            if success_elements:
                print(f"Form submission successful for element: {form_element.get_attribute('name')}")
            else:
                print(f"Form submission failed for element: {form_element.get_attribute('name')}")
      
       
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
       
    def print_form_details(self, form_inputs):
        print("Form Input Details:")
        for index, input_element in enumerate(form_inputs, start=1):
            print(f"Input {index}:")
            print(f"  Label: {input_element['label']}")
            print(f"  Type: {input_element['type']}")
            print(f"  Values: {input_element['values']}")
            print(f"  Is Hidden: {input_element['is_hidden']}")
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
    def get_job_inf(self, var_job_link, browser, google_search_button):   #param == cls, job_link  |  self, var_search_results
        search_results = var_job_link
        name_of_job = google_search_button
        
        print("Search results = ")
        print(search_results)
        print("Length of search_results is ", end="")
        print(len(search_results))
        
        for job_index in search_results[::-1]:
            print("===Ballsack = name_of_job = ", end="")
            print(name_of_job)      #! ===Ballsack = google_search_button = Senior Software Developer - Tanda
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
















