    def company_job_openings(self, soup, div_main, application_company_name):
        print("company_job_openings()")
        #greenhouse.io == <div id="main">   =>   lever.co == ??? [?postings-wrapper?] -> maybe 'filter-bar'
        #greenhouse.io == <section class="level-0">   =>   lever.co == <div class="postings-group">
        #greenhouse.io == <section class="level-1">   =>   lever.co == <div class="posting">
        print("Application Company = " + application_company_name)
        
        
        #???????????????????????????????????????????????????????????????????????
        #TODO
        #! Check out below!!! Maybe this needs to be perfect url?
        self.company_internal_job_listings_url = self.browser.current_url
        #???????????????????????????????????????????????????????????????????????
        #NOTE:Sometimes clicking the banner takes you to the company's website rather than their internal job listings on 'greenhouse' or 'lever'
        
        
        if application_company_name == 'lever':
            #just getting a better(more narrowed result) filter
            postings_wrapper = soup.find('div', class_="postings-wrapper")
            current_url = self.browser.current_url
            perfect_url = self.try_adjusting_this_link(current_url)
            
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
                        for bad_word in self.avoid_these_job_titles:
                            if bad_word not in job_title:
                                job_href = job_opening_href.get('href')
                                job_url = perfect_url + job_href
                                self.company_open_positions_url.append(job_url)
                                print(job_title)
                        span_tag = job_opening_href.find('span', {'class', 'sort-by-location'})
                        span_tag_company_team = job_opening_href.find('span', {'class': 'sort-by-team'})
                        span_tag_workplaceTypes = job_opening_href.find('span', {'class': 'workplaceTypes'})
                        if span_tag:
                            job_opening_location = span_tag.text
                        #job_opening_href.click()$%$%$%$%$%$%$%$%$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%
                if self.fits_users_criteria():
                    self.company_open_positions_url.append(job_link)
            self.print_company_job_openings("company_job_openings", application_company_name, JobTitle=job_title, JobLocation=job_opening_location, WorkPlaceTypes=span_tag_workplaceTypes, CompanyDepartment=company_department, JobTeamInCompany=span_tag_company_team, JobHREF=job_link, ButtonToJob=button_to_job_description)
            return
        
        elif application_company_name == 'greenhouse':
            current_url = self.browser.current_url
            perfect_url = self.try_adjusting_this_link(current_url)
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
                        for bad_word in self.avoid_these_job_titles:
                            if bad_word not in job_title:
                                job_href = job_opening_href.get('href')
                                job_url = perfect_url + job_href
                                self.company_open_positions_url.append(job_url)
                        span_tag = job_opening.find('span', {'class', 'location'})
                        if span_tag:
                            job_opening_location = span_tag.text
                            print(job_opening_location)
                        #job_opening_href.click()
                if count == 20:
                    break
                print("-------")
            self.print_company_job_openings("company_job_openings", application_company_name, JobTitle=job_title, JobLocation=job_opening_location, ButtonToJob=job_href)
            #%% %% %% %% %% %% %% %%
        return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


















    def company_job_openings(self, soup, div_main, application_company_name):
        print("company_job_openings()")
        #greenhouse.io == <div id="main">   =>   lever.co == ??? [?postings-wrapper?] -> maybe 'filter-bar'
        #greenhouse.io == <section class="level-0">   =>   lever.co == <div class="postings-group">
        #greenhouse.io == <section class="level-1">   =>   lever.co == <div class="posting">
        print("Application Company = " + application_company_name)
        
        
        #???????????????????????????????????????????????????????????????????????
        #TODO
        #! Check out below!!! Maybe this needs to be perfect url?
        self.company_internal_job_listings_url = self.browser.current_url
        #???????????????????????????????????????????????????????????????????????
        #NOTE:Sometimes clicking the banner takes you to the company's website rather than their internal job listings on 'greenhouse' or 'lever'
        
        
        if application_company_name == 'lever':
            #just getting a better(more narrowed result) filter
            postings_wrapper = soup.find('div', class_="postings-wrapper")
            current_url = self.browser.current_url
            perfect_url = self.try_adjusting_this_link(current_url)
            
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
                        for bad_word in self.avoid_these_job_titles:
                            if bad_word not in job_title:
                                job_href = job_opening_href.get('href')
                                job_url = perfect_url + job_href
                                self.company_open_positions_url.append(job_url)
                                print(job_title)
                        span_tag = job_opening_href.find('span', {'class', 'sort-by-location'})
                        span_tag_company_team = job_opening_href.find('span', {'class': 'sort-by-team'})
                        span_tag_workplaceTypes = job_opening_href.find('span', {'class': 'workplaceTypes'})
                        if span_tag:
                            job_opening_location = span_tag.text
                        #job_opening_href.click()$%$%$%$%$%$%$%$%$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%
                if self.fits_users_criteria():
                    self.company_open_positions_url.append(job_link)
            self.print_company_job_openings("company_job_openings", application_company_name, JobTitle=job_title, JobLocation=job_opening_location, WorkPlaceTypes=span_tag_workplaceTypes, CompanyDepartment=company_department, JobTeamInCompany=span_tag_company_team, JobHREF=job_link, ButtonToJob=button_to_job_description)
            return
        
        elif application_company_name == 'greenhouse':
            current_url = self.browser.current_url
            perfect_url = self.try_adjusting_this_link(current_url)
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
                        for bad_word in self.avoid_these_job_titles:
                            if bad_word not in job_title:
                                job_href = job_opening_href.get('href')
                                job_url = perfect_url + job_href
                                self.company_open_positions_url.append(job_url)
                        span_tag = job_opening.find('span', {'class', 'location'})
                        if span_tag:
                            job_opening_location = span_tag.text
                            print(job_opening_location)
                        #job_opening_href.click()
                if count == 20:
                    break
                print("-------")
            self.print_company_job_openings("company_job_openings", application_company_name, JobTitle=job_title, JobLocation=job_opening_location, ButtonToJob=job_href)
            #%% %% %% %% %% %% %% %%
        return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #self.company_job_title = None
    #self.company_name = None
    #self.company_job_location = None
    self.company_open_positions_url = []
    self.company_job_department = None
    self.job_id_number = None
    self.company_open_positions_link = None
    #self.job_link_url = None
    
    
    
    
    
    
    
    
    #!ADD to global variables
    job_application_webpage = ["Job-Description", "Job-Application", "Submitted-Application", "Internal-Job-Listings"]
    
    self.internal_jobs_details = []
    self.current_jobs_details = {}
    
    self.company_internal_job_listings_urls = []
    
    
    
    #TODO: In progress...
        #Incorporate checking other links if present!!!(you know besides the 1st)   Also, think about banner()!
    def find_companys_internal_job_listings_url(self):
        current_url = self.browser.current_url
        adjusted_url = self.try_adjusting_this_link(current_url)
        v1_parsed_url =  self.
        v2_parsed_url = self.is_absolute_path_v2(current_url)
        
        possible_urls = [current_url, adjusted_url, v1_parsed_url, v2_parsed_url]
        # OR OR OR...  try this way
        # urls = [
        #     self.browser.current_url
        #     self.try_adjusting_this_link(current_url),
        #     self.greenhouse_io_banner(),
        #     self.try_adjusting_this_link(current_url)
        # ]
        
        for check_this_url in possible_urls:
            #if self.validate_internal_job_listings_url(check_this_url):
            if self.determine_current_webpage(check_this_url) == job_application_webpage[3]:
                #TODO: Where ever you call this from make sure you have this...
                    #TODO:  self.company_internal_job_listings_url = self.find_companys_internal_job_listings_url()
                return check_this_url
        print("This company lowers your bonus every year anyways. Good Riddance if you ask me!")
        return None
    
    
    def is_absolute_path_v2(self, current_url):
        parsed_url = urlparse(current_url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
        company_url = '/'.join(parsed_url.path.strip('/').split('/')[:1])
        company_base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, company_url, '', '', ''))
    
    def init_users_job_search_requirements(self):
        self.users_job_search_requirements = {
            "job_title": [],
            "job_location": [],
            "job_workplaceType": [],
            "employment_type": [],  #Not really something I'm checking for
            "entry_level": True,  # < {"experience_level": False} You already have experience so any experience job is possible; shoot for the stars!
        }
    
    def init_current_jobs_details(self):
        #temp_job_details
        self.current_jobs_details = {
            "job_url": None,
            "job_title": None,
            "job_location": None,
            "company_name": None,
            "job_workplaceType": None,
            "company_department": None,
            "id_number": None,
            "job_release_date": None,
            "employment_type": None,
            "experience_level": None,
            "years_of_experience": None,
            "company_industry": None,
            #"education_requirement": None,
            #"skills": None,
            #"security_clearance": None
        }
        
    #TODO: Double check what this method does because I think it just makes the URL become the domain
        #TODO: AND...  AND if that is true then switch this dumb crap to the urlparse()!!
    def try_adjusting_this_link(self, adjust_this_link):
        print("try_adjusting_this_link()")
        if self.application_company_name == 'lever':
            adjusting_link = adjust_this_link.find('jobs.lever.co/') + len('jobs.lever.co/')
        if self.application_company_name == 'greenhouse':
            adjusting_link = adjust_this_link.find('greenhouse.io/') + len('greenhouse.io/')
            
            still_adjusting = adjust_this_link.find('/', adjusting_link) + 1
            # if self.is_absolute_path(still_adjusting):
            #     print("We know two things 1)This is in fact an href 2)This does lead somewhere")
            # else:
            #     #!IDEA: After the 'lever' and 'greenhouse' check wrap all this in a while loop && try a couple things!!
            #     print("I really have not 1 clue what to do here")
            link_adjusted = adjust_this_link[:still_adjusting]
            print(link_adjusted)
            adjust_this_link = link_adjusted
            print(adjust_this_link)
        time.sleep(2)
        return adjust_this_link
    
    # 1) Checks if at least one of users requested 'job titles' is present
    # 2) Then if it is...  checks if experience keywords are present
        # 2.1) If experience keywords are present returns google sheets
        # 2.2) If experience keywords are NOT present returns internal_jobs_details
    #! I believe using the new methods like users_basic_requirements_check() would be better than this way!!
    def users_basic_requirements_job_title_V2(self, company_job_title):
        for desired_job in self.users_job_search_requirements["job_title"]:
            #If users' requested job title isn't even present then skip this job completely|move onto the next!
            if desired_job not in company_job_title:
                return False
        #Job Titles Match so regardless return True BUT...  add a link to potentially_qualified_job_links &&
            #"job_url" in internal_jobs_details so we know to continue with this one other NO "job_url" just means add to Google Sheets!!
        if self.users_job_search_requirements['entry_level'] == True:
            for experience_keyword in self.prior_experience_keywords:
                if experience_keyword in company_job_title:
                    return experience_keyword
        return True
    
    def users_basic_requirements_check(self, company_job_title, job_location, job_workplaceType):
        if self.users_job_search_requirements['entry_level'] == True:
            if self.users_basic_requirements_experience_level(company_job_title) == False:
                return False
        
        if self.user_basic_requirements_location_workplaceType(job_location, job_workplaceType):
            return False
    
    def users_basic_requirements_job_title(self, company_job_title):
        return any(desired_job in company_job_title for desired_job in self.users_job_search_requirements['job_title'])
    
    def users_basic_requirements_experience_level(self, company_job_title):
        return any(experience_keyword in company_job_title for experience_keyword in self.prior_experience_keywords)
    
    def get_experience_level(self, company_job_title):
        for experience_keyword in self.prior_experience_keyword:
            if experience_keyword in company_job_title:
                return experience_keyword
    
    def construct_url_to_job(self, current_url, job_opening_href):
        # v Maybe for Selenium?
        button_to_job_description = job_opening_href
        print("button_to_job_description = ", button_to_job_description)
        job_link = job_opening_href.get('href')
        print("job_link = ", job_link)
        try:
            if is_absolute_path(job_link) == False:
                print("Ummm honestly I would have no idea what to do here!!")
        except ConnectionError:
            print(r"Error {e}")
        
        domain_name = self.try_adjusting_this_link(current_url)
        print("domain_name = ", domain_name)
        job_path = job_opening_href.get('href')
        print("job_path = ", job_path)
        job_url = domain_name + job_path
        print("job_url = ", job_url)
        return job_url
    
    #TODO: Make sure this works for when there are no links!! ALSO, maybe add a special case for "Don't see your job" application
    #def company_job_openings()
    def get_companies_internal_job_details(self, soup, div_main, application_company_name):
        print("get_companies_internal_job_details()")
        print("Application Company = " + application_company_name)
        #Doing this will erase all previously added job_details
        #self.internal_jobs_details = []
        current_url = self.browser.current_url
        
        if application_company_name == 'lever':
            postings_wrapper = soup.find('div', class_="postings-wrapper")
            postings_group_apply = postings_wrapper.find_all('div', class_=lambda x: x and ('postings-group' in x or 'posting-apply' in x))
            for section in postings_group_apply:
                self.init_current_jobs_details()
                print(section)
                company_department = section.find('div', class_='large-category-header').text
                if company_department:
                    print(company_department)
                if section.name == 'div' and section.get('class') == 'posting-apply':
                    job_opening_href = section.next_sibling
                    if job_opening_href.name == 'a' and job_opening_href.get('class') == 'posting-title':
                        #GET RID OF THESE???????
                        button_to_job_description = job_opening_href
                        print("button_to_job_description = ", button_to_job_description)
                        #GET RID OF THESE???????
                        job_url = self.construct_url_to_job(current_url, job_opening_href)
                        job_title = job_opening_href.find('h5').text
                        print("job_title = ", job_title)

                        if self.users_basic_requirements_job_title(job_title) == False:
                            continue
                        
                        experience_level = self.get_experience_level(job_title)

                        span_tag_location = job_opening_href.find('span', {'class', 'sort-by-location'})
                        span_tag_company_team = job_opening_href.find('span', {'class': 'sort-by-team'})
                        span_tag_workplaceType = job_opening_href.find('span', {'class': 'workplaceTypes'})
                        
                        
                        # The line span_tag_company_team = job_opening_href.find('span', {'class': 'sort-by-team'}) will not raise an error even if the element is not found. The find method returns None when it doesn't find an element that matches the criteria, but it doesn't raise an error.
                        # The error occurs when you try to access an attribute (in this case, text) of None. That's why we use the conditional operator to check if span_tag_company_team is not None before trying to access its text attribute.
                        # So, the line company_team = span_tag_company_team.text if span_tag_company_team else None will not raise an error, because it only tries to access span_tag_company_team.text if span_tag_company_team is not None. If span_tag_company_team is None, it simply assigns None to company_team.
                        
                        job_location = span_tag_location.text if span_tag_location else None
                        #TODO: Find out what the heck this team is!!!
                        #company_department = span_tag_company_team.text if span_tag_company_team else None
                        job_workplaceType = span_tag_workplaceType.text if span_tag_workplaceType else None
                            
                            
                if self.users_basic_requirements_check(job_title, job_location, job_workplaceType):
                    self.current_jobs_details.update({
                        'company_department': company_department,
                        'job_url': job_url,
                        'job_title': job_title,
                        'experience_level': experience_level,
                        'job_location': job_location,
                        'job_workplaceType': job_workplaceType
                    })
                    if not experience_level:
                        self.company_internal_job_listings_urls.append(job_url)

                self.print_companies_internal_job_opening("company_job_openings", application_company_name, JobTitle=job_title, JobLocation=job_location, WorkPlaceTypes=job_workplaceType, CompanyDepartment=company_department, JobTeamInCompany=span_tag_company_team, JobHREF=job_url, ButtonToJob=button_to_job_description)
            return
            
        elif application_company_name == 'greenhouse':
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
                    #GET RID OF THESE???????
                    button_to_job_description = job_opening_href
                    print("button_to_job_description = ", button_to_job_description)
                    #GET RID OF THESE???????
                    if job_opening_href:
                        job_title = job_opening_href.text
                        print("job_title = ", job_title)

                        if self.users_basic_requirements_job_title(job_title) == False:
                            continue
                        
                        experience_level = self.get_experience_level(job_title)

                        job_url = self.construct_url_to_job(current_url, job_opening_href)

                        span_tag_location = job_opening.find('span', {'class', 'location'})
                        
                        job_location = span_tag_location.text if span_tag_location else None
                        print("job_location = ", job_location)
                        #job_opening_href.click()
                        
                if self.users_basic_requirements_check(job_title, job_location, job_workplaceType):
                    self.current_jobs_details.update({
                        'company_department': company_department,
                        'job_url': job_url,
                        'job_title': job_title,
                        'experience_level': experience_level,
                        'job_location': job_location,
                        'job_workplaceType': job_workplaceType
                    })
                    if not experience_level:
                        self.company_internal_job_listings_urls.append(job_url)
                self.print_company_job_openings("company_job_openings", application_company_name, JobTitle=job_title, JobLocation=job_location, ButtonToJob=button_to_job_description)
        return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 
 




































































































    #!ADD to global variables
    job_application_webpage = ["Job-Description", "Job-Application", "Submitted-Application", "Internal-Job-Listings"]
    
    #This is a *SPECIAL* case b/c it's only called if the 1st link is for "lever" and it's the application page!!
    def initial_job_application_webpage(self):
        #I think just calling this is best b/c one of its MAIN JOBS is to find the correct
        self.lever_co_banner(webpage_body, soup)

    
    
    
    def determine_current_page(self, job_link, application_company_name):
        print("determine_current_page()")
        soup = self.apply_beautifulsoup(job_link, "lxml")
        print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        
        if application_company_name == "lever":
            webpage_body = soup.find('body')
            
            opening_link_application = soup.find('div', {"class": 'application-page'})
            opening_link_description = soup.find('div', {"class": 'posting-page'})
            opening_link_company_jobs = soup.find('div', {"class": "list-page"})
            
            job_application_page = opening_link_application.text if opening_link_application else None
            job_description_page = opening_link_description.text if opening_link_description else None
            internal_job_listings_page = opening_link_company_jobs.text if opening_link_company_jobs else None
            
            if job_application_page:
                print('-Application Page')
                try:
                    #TODO: This is v what we want to avoid!!!
                    company_open_positions = soup.find('a', {"class": "main-header-logo"})
                    internal_job_listings_url = company_open_positions if company_open_positions else None
                    if not internal_job_listings_url:
                        #? IDEA IDEA IDEA
                        company_open_positions.click()
                        #? IDEA IDEA IDEA
                        
                    #application_webpage_html = soup.find("div", {"class": "application-page"})
                    
                    #I think just calling this is best b/c one of its MAIN JOBS is to find the correct 
                    self.lever_co_banner(webpage_body, soup)
                    #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    self.form_input_details = self.get_form_input_details(current_url)
                    self.process_form_inputs(self.form_input_details)
                    
                    
                    #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                #     try:
                #         self.company_open_positions_a.click()
                #     except:
                #         raw_link = company_open_positions['href']
                #         self.browser.get(raw_link)
                #     time.sleep(2)
                #     return
                except:
                    #TODO: Change this Error type!
                    raise ConnectionError("ERROR: Companies other open positions are not present")
            elif job_description_page:
                print("-Job Description Page")
                self.scroll_to_element(opening_link_description)
                apply_to_job = self.should_user_apply(opening_link_description)
                if apply_to_job == True:
                    print("lever application locked and loaded")
                    self.bottom_has_application_or_button(application_company_name)
                    time.sleep(1)
                    current_url = self.browser.current_url
                    soup = self.apply_beautifulsoup(current_url, "html")
                    self.form_input_details = self.get_form_input_details(current_url)
                    self.insert_resume()
                    #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    #self.form_input_details = self.get_form_input_details(current_url)
                    self.process_form_inputs(self.form_input_details)
                    
                    
                    #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                    #self.fill_out_application(job_link, form_input_details)
                    self.keep_jobs_applied_to_info()
                elif not apply_to_job:
                    #TODO:
                    self.company_other_openings_href.click()
                    
                #TODO: If the button is present click OTHERWISE just insert the link
                if self.company_other_openings_href:
                    self.company_other_openings_href.click()
                else:
                    self.browser.get(self.company_other_openings_href)

            elif internal_job_listings_page:
                print('-Job Listings Page')
                pass
            return
            
        elif application_company_name == "greenhouse":
            div_main = soup.find("div", id="main")

            next_elem = div_main.find_next()
            while next_elem:    #NOTE: REMEBER THIS DOESN'T INCREMENT next_elem SO IT'S THE SAME VALUE AS ABOVE!!!!
                if next_elem.name == "div" and (next_elem.get("id") == "flash-wrapper" or next_elem.get("id") == "flash_wrapper"):
                    print('-Job Listings Page V.1')
                    return self.applying_process_webpage[3]
                elif (next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper"):
                    print('-Job Listings Page V.2')
                    return self.applying_process_webpage[3]
                elif (next_elem.name == "section" and next_elem.get("class") == "level-0"):
                    print("-Company Job Openings Page")
                    return self.applying_process_webpage[3]
                elif next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"]:
                    app_body = next_elem
                    header = next_elem.find("div", id="header")
                    content = next_elem.find("div", id="content")
                    
                    if header and content:
                        print("-Job Description Page")
                        #TODO: Fix this!!! I need the header link!
                        self.greenhouse_io_banner(app_body, header, content)    #TODO: return *job_title, company, location, ???*
                        current_url = self.browser.current_url
                        should_apply = self.should_user_apply(app_body)
                        if should_apply == True:
                            #This should setup the code so that it's lookin down the barrell of the application! Everything should already be setup!!!
                            self.bottom_has_application_or_button(application_company_name)
                            print("greenhouse application locked and loaded")
                            #form_input_details = self.get_form_input_details(job_link)
                            print("Meet")
                            time.sleep(8)
                            self.insert_resume()
                            print("me")
                            time.sleep(8)
                            #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            self.form_input_details = self.get_form_input_details(current_url)
                            self.process_form_inputs(self.form_input_details)
                    
                            
                            #!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            print("out back naked little Timmy....")
                            #self.fill_out_application(job_link, form_input_details)
                            self.keep_jobs_applied_to_info(job_link)
                        elif should_apply == False:
                            pass 
                        else:
                            print("\tHmmm that's weird ? it's neither button nor application")
                        
                        
                        try:
                            self.company_other_openings_href.click()
                        except:
                            self.browser.get(self.company_other_openings_href)
                            
                            
                        time.sleep(4)
                        pass
                    break
                else:
                    next_elem = next_elem.find_next()
            print("Not really sure how the heck we got here and defintiely don't have a clue about where to go from here!?!?!?")
            return





    def job_application_webpage(self, jj):
        if self.application_company_name == 'lever':
            #idk maybe do the web scraping?
        elif self.application_company_name == 'greenhouse':
            #idk maybe do the web scraping?

    def job_description_webpage(self, jj):
        if self.application_company_name == 'lever':
            #idk maybe do the web scraping?
        elif self.application_company_name == 'greenhouse':
            #idk maybe do the web scraping?
            
    def job_application_webpage(self, jj):
        if self.application_company_name == 'lever':
            #idk maybe do the web scraping?
        elif self.application_company_name == 'greenhouse':
            #idk maybe do the web scraping?






    def init_current_webpage_soup_elements(self, job_link):
        soup = self.apply_beautifulsoup(job_link, "lxml")
        if self.application_company_name == 'lever':
            webpage_body = soup.find('body')
        elif self.application_company_name == 'greenhouse':
            div_main = soup.find("div", id="main")
        self.various_bs = {
            "soup": soup,
            "div_main": div_main,
            "webpage_body": webpage_body,
        }





















-----------------------------------------------------                      -------------------------------------------------



def company_job_openings(self, soup, div_main, application_company_name):
    print("company_job_openings()")

    # Set the internal job listings URL
    self.company_internal_job_listings_url = self.browser.current_url

    # Check if the application company is Lever
    if application_company_name == 'lever':
        postings_wrapper = soup.find('div', class_="postings-wrapper")
        current_url = self.browser.current_url
        perfect_url = self.try_adjusting_this_link(current_url)
        postings_group_apply = postings_wrapper.find_all('div', class_=lambda x: x and ('postings-group' in x or 'posting-apply' in x))

        for section in postings_group_apply:
            company_department = section.find('div', class_='large-category-header').text
            if company_department:
                print(company_department)

            if section.name == 'div' and section.get('class') == 'posting-apply':
                job_opening_href = section.next_sibling
                if job_opening_href.name == 'a' and job_opening_href.get('class') == 'posting-title':
                    button_to_job_description = job_opening_href
                    job_link = job_opening_href.get('href')
                    job_title = job_opening_href.find('h5').text
                    for bad_word in self.avoid_these_job_titles:
                        if bad_word not in job_title:
                            job_href = job_opening_href.get('href')
                            job_url = perfect_url + job_href
                            self.company_open_positions_url.append(job_url)
                    span_tag = job_opening_href.find('span', {'class', 'sort-by-location'})
                    span_tag_company_team = job_opening_href.find('span', {'class': 'sort-by-team'})
                    span_tag_workplaceTypes = job_opening_href.find('span', {'class': 'workplaceTypes'})
                    if span_tag:
                        job_opening_location = span_tag.text
                if self.fits_users_criteria():
                    self.company_open_positions_url.append(job_link)

        self.print_company_job_openings(
            "company_job_openings", 
            application_company_name, 
            JobTitle=job_title, 
            JobLocation=job_opening_location, 
            WorkPlaceTypes=span_tag_workplaceTypes, 
            CompanyDepartment=company_department, 
            JobTeamInCompany=span_tag_company_team, 
            JobHREF=job_link, 
            ButtonToJob=button_to_job_description
        )

    # Check if the application company is Greenhouse
    elif application_company_name == 'greenhouse':
        current_url = self.browser.current_url
        perfect_url = self.try_adjusting_this_link(current_url)
        sections = div_main.find_all('section', class_=lambda x: x and 'level' in x)

        for section in sections:
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
                    for bad_word in self.avoid_these_job_titles:
                        if bad_word not in job_title:
                            job_href = job_opening_href.get('href')
                            job_url = perfect_url + job_href
                            self.company_open_positions_url.append(job_url)
                    span_tag = job_opening.find('span', {'class', 'location'})
                    if span_tag:
                        job_opening_location = span_tag.text
                        print(job_opening_location)

        self.print_company_job_openings(
            "company_job_openings", 
            application_company_name, 
            JobTitle=job_title, 
            JobLocation=job_opening_location, 
            ButtonToJob=job_href
        )