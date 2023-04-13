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

class scraperGoogleJob():
    
    def __init__(self, list_of_links, browser):
        self.list_of_links = list_of_links
        self.browser = browser
        
    
    def convert_csv_data(job_data):
        with open ('job_data.csv', mode='r') as file:
            reader = csv.reader(file)
            csv_data = []
            for row in job_data:
                csv_data.append(row)
                #print(csv_data)
        return csv_data
    
    def write_to_csv(job_data):
        with open ('job_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            #for row in writer:
            writer.writerow(job_data)
        return "All done!"
    
    
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
        
            if "jobs.lever.co" in job_index:
                application_company = "lever"
                self.other_company_openings(soup, application_company)
                self.convert_to_bs(job_index, soup, "lever")
                applic = self.lever_io_data(job_index, soup)
                self.find_and_organize_inputs(applic)
    
            elif "boards.greenhouse.io" in job_index:
                application_company = "greenhouse"
                self.other_company_openings(soup, application_company)
                self.convert_to_bs(job_index, soup, "greenhouse")
                applic = self.greenhouse_io_start_page_decider(soup)
                applic = soup.find('div', id="application")
                self.find_and_organize_inputs(applic)
                
    def other_company_openings(self, soup, application_company):
        plethora_of_jobs = None
        if application_company == "lever":
            other_company_jobs = soup.find('div', {"class": 'page show'})
            company_open_positions = other_company_jobs.find('a', {"class": "main-header-logo"})
            if company_open_positions['href']:
                plethora_of_jobs = company_open_positions['href']

            print("Couldn't find the logo with the lick to plethora_of_jobs")
        elif application_company == "greenhouse":
            a_tag = soup.find('a', text='View all jobs')
            if a_tag:
                a_tag_inner_html = a_tag.decode_contents()
                plethora_of_jobs = a_tag_inner_html['href']
        print("Here1")
        print(plethora_of_jobs)
        print("Here2")
        return plethora_of_jobs
    
    def convert_to_bs(self, job_index, soup, application_company):
        if application_company == "lever":
            app_body = soup.find("div", id="app_body")
            
            other_company_openings = soup.find('div', {"class": 'page show'})
            company_open_positions = other_company_openings.find('a', {"class": "main-header-logo"})
            try:
                if company_open_positions['href']:
                    plethora_of_jobs = company_open_positions['href']
                    print(plethora_of_jobs)
            except:
                print("This company has no ALL job openings page!")
            opening_link_application = soup.find('div', {"class": 'application-page'})
            opening_link_description = soup.find('div', {"class": 'posting-page'})
            
            #3 openinng page possibilities [Job Description/Application/Company Openings]
            if opening_link_application:
                try:
                    company_open_positions = soup.find('a', {"class": "main-header-logo"})
                    application_webpage_html = soup.find("div", {"class": "application-page"})
                    self.lever_io_application(joby_link, application_webpage_html)
                except:
                    #TODO: Change this Error type!
                    raise ConnectionError("ERROR: Companies other open positions are not present")
            elif opening_link_description:
                try:
                    a_tag_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
                    div_tag_butt = soup.find('div', {'data-qa': 'btn-apply-bottom'})
                    application_at_bottom = soup.find("div", id="application")
                    if a_tag_butt:
                        has_apply_button = a_tag_butt
                    elif div_tag_butt:
                        has_apply_button = div_tag_butt
                    
                    if ok_to_apply():
                        fill_out_application()
                except:
                    raise "Something went wrong with the the greenhouse.io job_description page"
            return
                    
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
        
        elif application_company == "greenhouse":
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
            return
    
    
    
        everything_about_job = app_body.get_text()
        dont_apply(everything_about_job)
        
    def dont_apply(self, everything_about_job):
        job_exp_needed = everything_about_job.find()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #@classmethod
    def get_job_info(self, var_job_link, browser, google_search_button):   #param == cls, job_link  |  self, var_search_results
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
    def lever_io_data(self, joby_link, soup):
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

    def lever_io_application(self, application_link, application_webpage_html):
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
    
    
    
    
    def application_or_button(self, website):
        if(website == "greenhouse"):
            application = soup.find("div", id="application")
            
    
    
    
    
    
    
    
    
    
    
    
    
    #NOTE: These have the forms below the descriptions...       1st find "Apply for this Job" | 2nd go to each incremental <button> and <input>
    def greenhouse_io_data(self, soup):
        print("Here")
        return 0
    
    
    #if id="app_body" and [check which page you are on]
    
    def greenhouse_io_start_page_decider(self, soup): #if (child of main is one of these)
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
        
    
    def greenhouse_io_header(self, app_body, header, content):
        print("===Ballsack = .greenhouse_io_header() = ")
        print(header)
        print("----------------------------------")
        first_child = True
        for child in header.children:
            if first_child:
                first_child = False
                continue
            if child.name == "h1" and "app-title" in child.get("class"):
                company_job_name = child.get_text()
                print("company_job_name = ")
                print(company_job_name)
            elif child.name == "span" and  "company-name" in child.get("class"):
                company_name = child.get_text()    #"at Braintrust" => maybe look for 1st capital letter
                print("company_name = ")
                print(company_name)
            elif child.name == "a" and "button" in child.get("class"):     #as long as 'href' just exists
                all_jobs_available_a_href = child['href']
                print("all_jobs_available_a_href 1 = ")
                print(all_jobs_available_a_href)
                #! If it opens on job_description see the bottom is 'apply_button' or 'job_application'
                # print("all_jobs_available_a_href 2 = ")
                # all_jobs_available_a_href = child.decode_contents()
                print(all_jobs_available_a_href)
                #!since child is the <a> remember to click it!!!
                companies_jobs_link_a = child
            elif child.name == "div" and "location" in child.get("class"):
                company_job_location = child.get_text()
                print("company_job_location = ")
                print(company_job_location)
            else:
                print("child = ")
                print(child)
        return print("finished all over .greenhouse_io_header()")
        #self.greenhouse_io_content(app_body, content)
        return 
        
    def greenhouse_io_content(self, app_body, content):
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
            
    def greenhouse_io_application(application):
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
    def attach_resume(self, application):
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
    def find_and_organize_inputs(self, applic):
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
    
    
    def fill_in_input(form_data):
        print("user <input>")
        for user_form_question in form_data:
            print(user_form_question)
    
    #Figure out the section you are in
    #Figure out the <label>.get_text()
    #Figure out if it's a <select>/<radio>/<input>
    #if label
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #, website_root, job_url, job_name, company_name, job_location, job_style, apply_button, company_department, company_commitment
    def print_info(self):
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def workday_data(self, soup):
        print("Here")
        return 0

    def general_bs(self, app_body):
        everything_about_job = app_body.get_text()
        print("===Ballsack = general_bs()... all the text in the job description = ")
        print("You'll never succeed here...")
        #print(everything_about_job)
        
        #filter the job out as needed
    
    def apply_to_job(job_data: list):
        if (len(job_data)-1):
            return "ok"

    def get_application_values():
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