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


class greehouse_io():
    greenhouse_io = ['', 'https://boards.greenhouse.io/airbase/jobs/4377585004?t=0844c1174us', 'https://boards.greenhouse.io/grindr/jobs/4982568', 'https://boards.greenhouse.io/openai']
    
    def __init__(self, list_of_links, browser):
        self.list_of_links = list_of_links
        self.browser = browser
        #No buttons
        job_description_button = self.greenhouse_io[0]
        #No only applications
        job_description_app = self.greenhouse_io[1]
        job_application = self.greenhouse_io[2]
        company_job_openings = self.greenhouse_io[3]
        
    def deal_with_links(self, google_search_name):
        #self.list_of_links = var_job_link
        google_link_title = google_search_name
        application_company = None
        
        for job_index in self.list_of_links[::-1]:
            selenium_google_link = self.browser.find_element(By.XPATH, f'//ancestor::a/h3[text()="{google_link_title}"]')
            selenium_google_link.click()
            self.browser.implicitly_wait(5)
            time.sleep(3)
            
            result = requests.get(job_index)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')
            
            if "boards.greenhouse.io" in job_index:
                application_company = "greenhouse"
                self.link_to_other_company_openings(soup, application_company)
                self.convert_to_bs(job_index, soup, "greenhouse")
                applic = self.greenhouse_io_start_page_decider(soup)
                applic = soup.find('div', id="application")
                self.find_and_organize_inputs(applic)
    
    def convert_to_bs(self, job_index, soup, application_company):
        if application_company == "greenhouse":
            div_main = soup.find("div", id="main")

            next_elem = div_main.find_next()
            while next_elem:
                if next_elem.name == "div" and (next_elem.get("id") == "flash-wrapper" or next_elem.get("id") == "flash_wrapper"):
                    print('-Job Page')
                    return soup.find("div", id="flash-wrapper")
                    break
                elif (next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper"):
                    print('-Job Listings Page')
                    return soup.find("div", id="embedded_job_board_wrapper")
                    break
                elif (next_elem.name == "section" and next_elem.get("class") == "level-0"):
                    print("-Company Job Openings Page")
                    print("A while loop for this is perfect for this because there can be multiple <section class='level-0'>")
                    #TODO: for this one in the elif you have to look through all "level-0" sections!!
                    self.company_job_openings(div_main)
                    return soup.find("section", {"class": "level-0"})
                elif next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"]:
                    app_body = next_elem
                    header = next_elem.find("div", id="header")
                    content = next_elem.find("div", id="content")
                    application = soup.find("div", id="application")
                    if header and content:
                        print("Job Description Page")
                        self.link_to_other_company_openings(soup, application_company)
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
            return
        
    def link_to_other_company_openings(self, soup, application_company):
        plethora_of_jobs = None

        if application_company == "greenhouse":
            sections = div_main.find_all('section', class_=lambda x: x and 'level' in x)
            
            for section in sections:
                #if section.name == "class" and section.get("class") == 'level-0':
                if section.name == 'h3':
                    company_department = section.text
                if section.name == 'h4':
                    print('This is most likely just a SUB-category so not really important otber than making sure we go through EVERY job it contains!')
                    
                job_opening = section.find('div', {'class': 'opening'})
                if job_opening:
                    job_opening_href = job_opening.find('a')
                    if job_opening_href:
                        job_title = job_opening_href.text
                        job_link = job_opening_href.get('href')
                        span_tag = job_opening.find('span', {'class', 'location'})
                        if span_tag:
                            job_opening_location = span_tag.text
                        job_opening_href.click()
            return
            # div_main = soup.find("div", id="main")
            # a_tag = soup.find('a', text='View all jobs')
            # if a_tag:
            #     a_tag_inner_html = a_tag.decode_contents()
            #     plethora_of_jobs = a_tag_inner_html['href']
        print("Here1")
        print(plethora_of_jobs)
        print("Here2")
        return plethora_of_jobs
        