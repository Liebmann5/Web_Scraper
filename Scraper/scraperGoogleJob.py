from urllib import request
from bs4 import BeautifulSoup
import csv

class scraperGoogleJob():
    #def read_job_data(job_data):
    def convert_csv_data(job_data):
        with open ('job_data.csv', mode='r') as file:
            reader = csv.reader(file)
            csv_data = []
            for row in job_data:
                csv_data.append(row)
                #print(csv_data)
    
    def write_to_csv(job_data):
        with open ('job_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            #for row in writer:
            writer.writerow(job_data)
    
    def get_job_info(job_link):
        for jobs in job_link:
            result = request.get(jobs)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')
            
        if job_link == "jobs.lever.co":
            opening_link_application = soup.find('div', class_='page-application')
            opening_link_description = soup.find('div', class_='page-show')
            if opening_link_application:
            #if soup.find('a', class_='main-header-logo'):
                try:
                    company_open_positions = soup.find('a', class_='main-header-logo')
                    plethora_of_jobs = company_open_positions['href']
                    print(plethora_of_jobs)
            elif opening_link_application:
                try:
                    job_title = soup.find('h2').get_text()
                    job_info = job_title.nextSibling('div', class_="posting-categories")
                    job_location = job_info.find('div', class_='location')
                    job_department = job_info.find('div', class_='department')
                    job_commitment = job_info.find('div', class_='commitment')
                    job_style = job_info.find('div', class_='workplaceTypes')
            
            
                    job_apply_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
                    link_to_apply = job_apply_butt['href']
                    print(link_to_apply)
                    #  Captcha
                    #<input id="hcaptchaResponseInput" type="hidden" name="h-captcha-response" value>
                    #<button id="hcaptchaSubmitBtn" type="submit" class="hidden"></button>
            
        elif job_link == "boards.greenhouse.io":
            

                