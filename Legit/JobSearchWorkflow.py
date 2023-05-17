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

                #Run "python|python3 -u Legit/JobSearchWorkflow.py"
                #!!!!!!!!!!!!!!!!!!! TEST THIS HAS  CHECKLIST !!!!!!!!!!!!!!!!!!!!!!!!!!
                #https://jobs.lever.co/hive/9461e715-9e58-4414-bc9b-13e449f92b08/apply
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #ThisFolderWasMadeAtThreeAM/setup.sh

#! EXTRACT JOB_TYPE AS LIST OD len()=3 | {DESIRED_LOCATION, HYBRID, REMOTE}
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
       
    def job_search_workflow(self):
        self.browser_setup()
        self.google_search_results_links, last_link_from_google_search, user_desired_jobs = scraperGoogle(self.browser).user_requirements()
        print("DOPE")
        print(self.google_search_results_links)
        print("DOPER")
        time.sleep(3)
        self.previous_job_applications_data = self.convert_csv_data(self.previous_job_data_csv_relative_path)
        self.google_search_results_links = self.ensure_no_duplicates(self.google_search_results_links)
        self.previously_applied_to_job_links = self.get_job_links_users_applied_to(self.previous_job_applications_data)  #and filter them out!
        self.filter_out_jobs_user_previously_applied_to(self.google_search_results_links, self.previously_applied_to_job_links)
        self.load_users_information()
        self.apply_to_jobs(last_link_from_google_search, user_desired_jobs)
        
        self.close_browser()
        
        
        
        
    #TODO: change variable name => users_browser_choice   ->   users_browser_choice_name??
    #TODO: Setup browser HERE... b/c only the 1st run of this programm should take a long time for info setup!! The 2nd
    #TODO: time they run it just ask them what browser... HERE lol then if they make any changes GoogleSearch.py takes effect!
    def users_browser_choice(self):
        #users_browser_choice, browser_name = 1, " Firefox "
        users_browser_choice, browser_name = 2, " Safari "
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
                print("Scrolled to this place...")
                time.sleep(5)
                
                
                
                
                
                # element_code_outer = last_link_from_google_search.get_attribute('outerHTML')
                # element_code_inner = last_link_from_google_search.get_attribute('innerHTML')
                # soup_outer = BeautifulSoup(element_code_outer, 'html.parser')
                # soup_inner = BeautifulSoup(element_code_inner, 'html.parser')
                # print("------------------------------------------------------")
                # print("This is the dumb selenium element outerHTML: ")
                # print(soup_outer.prettify())
                # print("------------------------------------------------------")
                # print("This is the dumb selenium element innerHTML: ")
                # print(soup_inner.prettify())
                # print("------------------------------------------------------")
                # time.sleep(15)
                    
                
                
                 
                
                last_a_tag = last_link_from_google_search.find_element(By.TAG_NAME, 'a')
                last_a_tag.click()
                clicked_link_from_google_search = True
                print("Accidently clamped my testicles b/c I needed to be punished")
                wait_fur_this = self.wait_for_element_explicitly(self.browser, 10, (By.TAG_NAME, 'a'), 'visibility')



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
    
        
        
      
    
    
    
    
    
    def write_to_csv(self, job_data):
        with open ('job_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            #for row in writer:
            writer.writerow(job_data)
        return "All done!"
    
   
   
   
   










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














