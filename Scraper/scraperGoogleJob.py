from urllib import request
from bs4 import BeautifulSoup
import csv

class scraperGoogleJob():
    print("Made it this far!!")
    
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
    
    
    @classmethod
    def get_job_info(cls, job_link):   #param == job_link
        print("Made it to the get_job_info method!")
        job_link = ["https://jobs.lever.co/rover/0a6bcb57-bc8b-4826-b98c-7a17cbb4a911/apply", "https://jobs.lever.co/palantir/e82b696e-a085-4bbf-8bcb-6d2c4f8cf2f7"]
        for job in job_link:
            result = request.get(job)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')
            print(soup.prettify())
            
            if "jobs.lever.co" in job:
                cls.lever_io(job, soup)
                # Captcha
                # <input id="hcaptchaResponseInput" type="hidden" name="h-captcha-response" value>
                # <button id="hcaptchaSubmitBtn" type="submit" class="hidden"></button>
            
            elif "boards.greenhouse.io" in job:
                cls.greenhouse_io(soup)

            elif "workday" in job:
                cls.workday(soup)               
        return "ok"
    
    
    #filter out already applied jobs
    #traverse job webpage
    #?????
    def lever_io_data(job_link, soup):
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

    def lever_io_apply(application_link, application_webpage_html):
        job_form_html = application_webpage_html.find("form", id="application-form", method="POST")
        application_section_html = job_form_html.find_all("h4")
        #using ^this list .find() 1st <h4> then increment...
        print(application_section_html)
        for user_input in application_section_html:
            #loop through <input> tags and fill in using selenium!!
            print(user_input)
        return 0
    
    def greenhouse_io_data(soup):
        print("Here")
        return 0
    
    def workday_data(soup):
        print("Here")
        return 0
    
    def apply_to_job(job_data: list):
        if len(job_data)-1:
            return "ok"

#if __name__ == '__main__':
#    scraper = scraperGoogleJob()


