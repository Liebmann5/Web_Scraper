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

class scraperGoogleJob:
    
    # def __init__(self, job_link):
    #     print("Made it this far!!")
    #     self.job_link = job_link
    
    #def read_job_data(job_data):
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
        
        print(search_results)
        print("Length of search_results is ", end="")
        print(len(search_results))
        
        for job in search_results[::-1]:
            print(google_search_button)
            link_elemen = browser.find_element(By.XPATH, f'//ancestor::a/h3[text()="{google_search_button}"]')
            print(link_elemen)
            link_elemen.click()
            print("Waiting for link to load...")
            print(job)
            browser.implicitly_wait(5)
            time.sleep(15)
            
            #get HTML from clicked webpage
            #try:
            result = requests.get(job)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')
            print(soup.prettify())
            
            if "jobs.lever.co" in job:
                self.lever_io_data(job, soup)
                #scraperGoogleJob.lever_io_data(job, soup)
                # Captcha
                # <input id="hcaptchaResponseInput" type="hidden" name="h-captcha-response" value>
                # <button id="hcaptchaSubmitBtn" type="submit" class="hidden"></button>
            
            elif "boards.greenhouse.io" in job:
                self.greenhouse_io_data(soup)

            elif "workday" in job:
                self.workday_data(soup)
        print("Well sue me silly!")
        self.lever_io_apply(self, "application_link", "application_webpage_html")
        return "ok"
    
    
    #filter out already applied jobs
    #traverse job webpage
    #?????
    def lever_io_data(self, joby_link, soup):
        self.joby_link = joby_link
        
        opening_link_application = soup.find('div', class_='page-application')      #application immediate
        opening_link_description = soup.find('div', class_='page-show')             #regular description start
        
        #if soup.find('a', class_='main-header-logo'):
        if opening_link_application:
            try:
                company_open_positions = soup.find('a', class_='main-header-logo')
                plethora_of_jobs = company_open_positions['href']
                print(plethora_of_jobs)
            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        elif opening_link_application:
            try:
                position_title = soup.find('h2').get_text()
                job_title = position_title.split()
                print(job_title)
                job_info = job_title.nextSibling('div', class_="posting-categories")
                job_location = job_info.find('div', class_='location')
                job_department = job_info.find('div', class_='department')
                job_commitment = job_info.find('div', class_='commitment')
                job_style = job_info.find('div', class_='workplaceTypes')
        
        
                job_apply_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
                link_to_apply = job_apply_butt['href']
                print(link_to_apply)

            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
                
        return soup

    def lever_io_apply(self, application_link, application_webpage_html):
        job_form_html = application_webpage_html.find("form", id="application-form", method="POST")
        application_section_html = job_form_html.find_all("h4")
        #using ^this list .find() 1st <h4> then increment...
        print(application_section_html)
        for user_input in application_section_html:
            #loop through <input> tags and fill in using selenium!!
            print(user_input)
        return 0
    
    def greenhouse_io_data(self, soup):
        print("Here")
        return 0
    
    def workday_data(self, soup):
        print("Here")
        return 0
    
    def apply_to_job(job_data: list):
        if (len(job_data)-1):
            return "ok"









#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!       REMEMBER TO COUNT THE NUMBER OF OPEN SENIOR > ROLES AVAILABLE           !
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



#<cite class="qLRx3b tjvcx GvPZzd cHaqb" role="text" style="max-width:315px">https://jobs.lever.co<span class="dyjrff qzEoUe" role="text"> › ltaresearch</span></cite>

#<a href="/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=&amp;ved=2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB&amp;url=https%3A%2F%2Fjobs.lever.co%2Fltaresearch&amp;usg=AOvVaw1WnH3yWFh2qyF8H83db1P7" data-jsarwt="1" data-usg="AOvVaw1WnH3yWFh2qyF8H83db1P7" data-ved="2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB" data-ctbtn="0" data-cthref="/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=&amp;ved=2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB&amp;url=https%3A%2F%2Fjobs.lever.co%2Fltaresearch&amp;usg=AOvVaw1WnH3yWFh2qyF8H83db1P7" data-jrwt="1"><br><h3 class="LC20lb MBeuO DKV0Md">LTA Research</h3><div class="TbwUpd NJjxre iUh30 ojE3Fb"><span class="H9lube"><div class="eqA2re NjwKYd Vwoesf" aria-hidden="true"><img class="XNo5Ab" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAWlBMVEU+SEpvdXjIysvEx8edoaN4f4FOV1n6+vr////j5eVjamxyeXvZ2dn39/dqcXPNz9CLkJCqra7y8/PU1NRdZWfs7e7d3t5cY2ZTW12zt7hYXmKTmJp/hYe6vLweb9tYAAAAn0lEQVR4AcTPAxLAMBBA0TKszfsfs1acYf9w54XOT7meH4RA7SFEe5gonJ6OfF/vXhQBqcePR4nE3cvTaCsTPfl6lBtcXJAUp5enl8TgCefE0iPF+SavajtvFN6ynpq84rwzuNOfjlXuRIy3jnwB46FP+AWMZxAVCbvgcm/Y5xFtxfS7gPEAHcHpXVB/PUd32fPN+Sjo9oFGb906+uRTAOgAEo+qriNyAAAAAElFTkSuQmCC" style="height:18px;width:18px" alt=""></div></span><div><span class="VuuXrf">lever.co</span><div class="byrV5b"><cite class="qLRx3b tjvcx GvPZzd cHaqb" role="text" style="max-width:315px">https://jobs.lever.co<span class="dyjrff qzEoUe" role="text"> › ltaresearch</span></cite></div></div></div></a>




#<a href="/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=&amp;ved=2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB&amp;url=https%3A%2F%2Fjobs.lever.co%2Fltaresearch&amp;usg=AOvVaw1WnH3yWFh2qyF8H83db1P7" data-jsarwt="1" data-usg="AOvVaw1WnH3yWFh2qyF8H83db1P7" data-ved="2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB" data-ctbtn="0" data-cthref="/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=&amp;ved=2ahUKEwiJt8e-kpj-AhXdnWoFHTlfAxE4WhAWegQIBxAB&amp;url=https%3A%2F%2Fjobs.lever.co%2Fltaresearch&amp;usg=AOvVaw1WnH3yWFh2qyF8H83db1P7" data-jrwt="1"><br><h3 class="LC20lb MBeuO DKV0Md">LTA Research</h3>






