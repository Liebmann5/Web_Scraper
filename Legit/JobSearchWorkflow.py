from bs4 import BeautifulSoup
from selenium import webdriver

from dotenv import load_dotenv
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
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

                #Run "python|python3 -u Legit/JobSearchWorkflow.py"
                #!!!!!!!!!!!!!!!!!!! TEST THIS HAS  CHECKLIST !!!!!!!!!!!!!!!!!!!!!!!!!!
                #https://jobs.lever.co/hive/9461e715-9e58-4414-bc9b-13e449f92b08/apply
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class Workflow():
       
    def __init__(self):
        self.browser = None
        #self.google_search_results_links = None
        self.google_search_results_links = []
        self.time_program_ran = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("This program began running at " + self.time_program_ran)
        
        #TODO: Change this name... it's all the job info a user has previously applied to!!
        self.csv_data = []
 
        self.env_path = '.env'
        self.env_other_path = '../.env'
        #self.previous_job_data_csv_relative_path = r'../Scraper/JobsThatUserHasAppliedTo.csv'
        self.previous_job_data_csv_relative_path = r'Scraper/JobsThatUserHasAppliedTo.csv'
        self.users_information = {}
        self.total_jobs_applied_to_count = 0
        self.total_jobs_applied_to_info = {} 
        self.previous_job_applications_data = []
        self.last_time_user_applied = None
       
    def job_search_workflow(self):
        self.browser_setup()
        self.google_search_results_links, last_link_from_google_search = scraperGoogle(self.browser).user_requirements()
        print("DOPE")
        print(self.google_search_results_links)
        print("DOPER")
        time.sleep(3)
        self.previous_job_applications_data = self.convert_csv_data(self.previous_job_data_csv_relative_path)
        self.ensure_no_duplicates()
        previously_applied_to_job_links = self.get_job_links_users_applied_to()  #and filter them out!
        self.filter_out_jobs_user_previously_applied_to(previously_applied_to_job_links)
        self.load_users_information()
        self.apply_to_jobs(last_link_from_google_search)
        
        self.close_browser()
        
        
        
        
          
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
        
    
    
    
    def apply_to_jobs(self, last_link_from_google_search):
        print("Begin the sex Batman... Robin... I'll need an extra set of hands in a second so hang tight")
        clicked_link_from_google_search = False
        # for job_link in self.google_search_results_links[::1]:
        for i in range(len(self.google_search_results_links) - 1, -1, -1):   #? I think this goes last to first???
            if not clicked_link_from_google_search:
                print(last_link_from_google_search)
                #self.browser.find_element(By.X_PATH, )
                last_link_from_google_search.click()
                clicked_link_from_google_search = True
                print("Accidently clamped my testicles b/c I needed to be punished")
                time.sleep(5)
            job_link = self.google_search_results_links[i]
            print(job_link)
            CompanyWorkflow(self.browser, self.users_information, senior_experience=False).company_workflow(job_link)
    


    
    
    
    #!------------- .env --------------------
    def load_users_information(self):
        self.users_information = {}
        with open(self.env_path) as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split('=', 1)
                    value = value.strip("'")  # Remove quotes around the value
                    self.users_information[key] = value
        self.print_users_information()
    
    def print_users_information(self):
        print('--------USERS .ENV INFO--------')
        for key, value in self.users_information.items():
            print(f"{key}: {value}")
        print('-------------------------------')
    #!---------------------------------------
    
    
    
    
    
    
    

    
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
    def get_job_links_users_applied_to(self):
        print("\nget_job_links_users_applied_to() =")
        
        previously_applied_to_job_links = []
        
        for row in self.previous_job_applications_data:
            links_row = row[0]
            print("If my calculations are correct this should print a link MUAH HA HA... ", end="")
            print(links_row)
            previously_applied_to_job_links.append(links_row)
            
        self.last_time_user_applied = self.previous_job_applications_data[-1][-1]
        print("These are all the links you already applied to... Tom")
        print(previously_applied_to_job_links)
        print("And this is when you last applied... Tom")
        print(self.last_time_user_applied)
        #self.filter_out_jobs_user_previously_applied_to(previously_applied_to_job_links)
        return previously_applied_to_job_links
    
    #TODO: FINISH BOTH OF THESE!!
    #Use Quick Sort to sort jobs_previously_applied_to
    #! We run this when we finish running other_company_openings()!!!!
        #! And self.google_search_results_links can stay in the method b/c nothing changes this value!! (b/c if it needed any we already applied it!)
    def filter_out_jobs_user_previously_applied_to(self, previously_applied_to_job_links):
        print("\nfilter_out_jobs_user_previously_applied_to()")
        
        Lake_Minnetonka_Purified_list = []
        
        for google_search_result_URL in self.google_search_results_links:
            found = False
            for previously_applied_URL in previously_applied_to_job_links:
                if google_search_result_URL == previously_applied_URL:
                    print("Match google_search_result_URL: ", end='')
                    print(google_search_result_URL)
                    print("Match previously_applied_URL: ", end='')
                    print(previously_applied_URL)
                    previously_applied_to_job_links.append(previously_applied_URL)
                    found = True
                    break
            if not found:
                Lake_Minnetonka_Purified_list.append(google_search_result_URL)
        
        print("These are all the links you already applied to... ")
        print(previously_applied_to_job_links)
        print("Swedish semen... yummy " + str(len(Lake_Minnetonka_Purified_list)) + " timber logs.")
        print(Lake_Minnetonka_Purified_list)
        self.google_search_results_links = Lake_Minnetonka_Purified_list
        return
    
    def ensure_no_duplicates(self):
        print("\nensure_no_duplicates() = ")
        
        unique_results = []
        for google_search_result_URL in self.google_search_results_links:
                if google_search_result_URL not in unique_results:
                    unique_results.append(google_search_result_URL)
                else:   #THIS ELSE AND 2 PRINT STATEMENTS ARE PURELY FOR TESTING!!!
                    print("Repeated Link Found: ", end="")
                    print(google_search_result_URL)
        self.google_search_results_links = unique_results
        return
    
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def write_to_csv(self, job_data):
        with open ('job_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            #for row in writer:
            writer.writerow(job_data)
        return "All done!"
    
   
   
   
   

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    def click_last_result_DONTuseTHIS(self, google_search_name):
        #self.list_of_links = var_job_link
        google_link_title = google_search_name
        application_company = None
        
        
        
        self.eff_that_link()
        
        
        
        
        # def apply_to_jo(job_data: list):
        # if (len(job_data)-1):
        #     return "ok"
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














