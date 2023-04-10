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
    
    def __init__(self, browser):
        self.browser = browser
    
    def convert_csv_data(job_data):
        with open ('job_data.csv', mode='r') as file:
            reader = csv.reader(file)
            csv_data = []
            for row in job_data:
                csv_data.append(row)
                #print(csv_data)
        return 0
    
    def write_to_csv(job_data):
        with open ('job_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            #for row in writer:
            writer.writerow(job_data)
        return 0
    
    
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
            print(name_of_job)      #! ===Ballsack = google_search_buttonSenior Software Developer - Tanda
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
            soup = BeautifulSoup(content, 'lxml')
            print(soup.prettify())       #! Prints the HTML -------->>>>>>> DOUBLE CHECK IT'S THE JOB_URL'S HTML!?!?!?
            
            if "jobs.lever.co" in job_index:
                print("===Ballsack = jobs.lever.co = 1")
                self.lever_io_data(job_index, soup)
                print("===Ballsack = jobs.lever.co = 2")
                #scraperGoogleJob.lever_io_data(job_index, soup)
                # Captcha
                # <input id="hcaptchaResponseInput" type="hidden" name="h-captcha-response" value>
                # <button id="hcaptchaSubmitBtn" type="submit" class="hidden"></button>
            
            elif "boards.greenhouse.io" in job_index:
                print("===Ballsack = boards.greenhouse.io = 1")
                self.greenhouse_io_data(soup)
                print("===Ballsack = boards.greenhouse.io = 2")

            elif "workday" in job_index:
                print("===Ballsack = workday = 1")
                self.workday_data(soup)
                print("===Ballsack = workday = 2")
            else:
                print("else statement")
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
        print(opening_link_application)
        print("===Ballsack = opening_link_description = ", end="")
        print(opening_link_description)
        
        #if soup.find('a', class_='main-header-logo'):
        if opening_link_application:
            try:
                company_open_positions = soup.find('a', {"class": 'main-header-logo'})
                plethora_of_jobs = company_open_positions['href']
                print(plethora_of_jobs)
            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        elif opening_link_description:
            print("===Ballsack = lever.co is working")
            try:
                print("===Ballsack = inside the try lever.co")
                position_title = soup.find('h2')
                job_title = position_title.split()
                print("===Ballsack = job_title = ", end="")
                print(job_title.get_text())
                job_info = job_title.nextSibling('div', {"class": "posting-categories"})
                job_location = job_info.find('div', {"class": 'location'})
                job_department = job_info.find('div', {"class": 'department'})
                job_commitment = job_info.find('div', {"class": 'commitment'})
                job_style = job_info.find('div', {"class": 'workplaceTypes'})
        
        
                job_apply_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
                link_to_apply = job_apply_butt['href']
                print("===Ballsack = link_to_apply = ", end="")
                print(link_to_apply)

            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        print("===Ballsack = leaving the lever.co")
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
                        fill_in_input(needed_input, input_type)
                    elif input_type == "button":
                        fill_in_button(needed_input, input_type)
                    elif input_type == "select":
                        fill_in_select(needed_input, input_type)  #multiple choice
                    elif input_type == "textarea":
                        fill_in_textarea(needed_input, input_type)
    

#plethora_of_jobs (outter) = <meta property="og:url" content="https://jobs.lever.co/anduril/51af4cee-1380-439c-86c2-510863722099/apply">
#plethora_of_jobs (inner)  = 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #NOTE: These have the forms below the descriptions...       1st find "Apply for this Job" | 2nd go to each incremental <button> and <input>
    def greenhouse_io_data(self, soup):
        print("Here")
        return 0
    
    
    #if id="app_body" and [check which page you are on]
    
    def greenhouse_io_start_page_decider(soup): #if (child of main is one of these)
        div_main = soup.find("div", id="main")
        next_elem = div_main.find_next()
        while next_elem:
            if next_elem.name == "div" and next_elem.get("id") == "flash-wrapper":
                print('Job Listings Page')
                break
            elif next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper":
                print('Job Listings Page')
                break
            elif next_elem.name == "div" and next_elem.get("id") == "app-body":
                app_body = next_elem
                header = next_elem.find("div", id="header")
                content = next_elem.find("div", id="content")
                if header and content:
                    print("Job Description Page")
                    greenhouse_io_header(app_body, header, content)
                else:
                    print("Application at bottom or <button>")
                    application = div_main.find("div", id="application")
                    #TODO
                    apply_button = div_main.find("button", text="Apply Here")
                    if application:
                        greenhouse_io_application(application)
                    elif apply_button:
                        apply_button.click()
                        time.sleep(5)
                        greenhouse_io_application(application)
                break
            else:
                next_elem = next_elem.find_next()
        
    
    def greenhouse_io_header(app_body, header, content):
        for child in header.children:
            if child.name == "h1" and child.get("class") == "app-title":
                company_job_name = child
            elif child.name == "span" and child.get("class") == "company-name":
                company_name = child    #"at Braintrust" => maybe look for 1st capital letter
            elif child.name == "a" and child.get("href"):     #as long as 'href' just exists
                all_jobs_available_a_href = child.get("href")
                #!since child is the <a> remember to click it!!!
                companies_jobs_link_a = child
            elif child.name == "div" and child.get("class") == "location":
                company_job_location = child.get_text()
            else:
                print(child)
        greenhouse_io_content(app_body, content)
        
    def greenhouse_io_content(app_body, content):
        for child in content.children:
            for childrens_child in child.children:
                strong_elem = childrens_child.find_next()
                while strong_elem:
                    if strong_elem.name == "stong":
                        description_title = strong_elem.get_text()
                        if description_title in "Requirements":
                            print("Balls")
                    
        application = div_main.find("div", id="application")
        #TODO
        apply_button = div_main.find("button", text="Apply Here")
        if application:
            greenhouse_io_application(application)
        elif apply_button:
            apply_button.click()
            time.sleep(5)
            greenhouse_io_application(application)
            
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
    def attach_resume(application):
        resume_element = application.find_element(By.XPATH, "//*[@id[contains(@id, 'resume')]]")
        resume_path = "get from .env file"
        
        #How does the form want us to upload our resume? Button click...
        while True:
            upload_by_button = application.find_element(By.TAG_NAME, "//fieldset[@aria-describedby='resume-allowable-file-types']")
            if upload_by_button:
                ActionChains(browser).move_to_element(upload_by_button).click().perform()
                upload_by_button.send_keys(resume_path)
                break
        try:
            ActionChains(browser).send_keys(Keys.ENTER).perform()
        except:
            raise "Something went wrong meanie! Help me :("
    
    #Purpose of this method is to find all the inputs!!!
    #Goal is to make a list of lists' where the inside list .len()=3 index1=label.text(){gender} |
        #index2=input_type {<select>, <button>} | index3=empty & fill with user's value
    #maybe rather than have a .len()=3 just for input's keep appending all possible box input's{only
    #for <input> b/c sometimes multiple BUT not radio buttons} and FINALLY append user's value
    #eff it just find all the labels then all the inputs
    def find_and_organize_inputs(application):
        label_elements = application.find_element(By.TAG_NAME, "label")
        form_data = []
        for label_element in label_elements:
            #text value of the <label>
            label_text = label_element.text.strip()
            
            #get all inputs after label
            user_input_type = []
            input_id = label_element.get_attribute('for')
            if input_id:
                input_elements.append(browser.find_element(By.ID, input_id))
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
            fill_in_input(form_data)
    
    
    def fill_in_input(form_data):
        print("user <input>")
        for user_form_question in form_data:
            print(user_form_question)
    
    #Figure out the section you are in
    #Figure out the <label>.get_text()
    #Figure out if it's a <select>/<radio>/<input>
    #if label
    
    
    
    
    
    
    
    
    
    
    def print_info():
        print(website_root)
        print(job_url)
        print(job_name)
        print(company_name)
        print(job_location)
        print(apply_button)
        print(company_department)
        print(company_commitment)
        print(company_jobtType)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def workday_data(self, soup):
        print("Here")
        return 0

    def general_bs(app_body):
        everything_about_job = app_body.get_text()
        print(everything_about_job)
        
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



















