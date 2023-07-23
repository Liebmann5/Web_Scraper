
    def check_banner_links(self, links_in_header):
        print("\ncheck_banner_links()")
        first_link = True
        for header_link in links_in_header[:-1]:
            if first_link == True and "lever" == self.application_company_name:
                self.try_adjusting_this_link(header_link)
                first_link = False
            elif first_link == True and "greenhouse" in self.application_company_name:
                self.try_adjusting_this_link(header_link)
                first_link == False
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_link = {executor.submit(self.check_link, header_link): header_link for header_link in links_in_header[:1]}
            for future in concurrent.futures.as_completed(future_to_link):
                link = future_to_link[future]
                try:
                    result = future.result()
                    if result is not None:
                        self.company_open_positions_link = result
                        return
                except Exception as exc:
                    print(f'{link} generated an exception: {exc}')
        
        if (self.company_open_positions_link == None):
            #TODO: Make this a method
            links_in_header[-1].click()
            time.sleep(3)
            current_url = self.browser.current_url
            result = self.check_link(current_url)
            if result is not None:
                self.company_open_positions_link = result
        return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def determine_current_page(self, job_link, application_company_name):
        soup = self.apply_beautifulsoup(job_link, "lxml")
        
        if application_company_name == "lever":
            webpage_body = soup.find('body')

            opening_link_application = soup.find('div', {"class": 'application-page'})
            opening_link_description = soup.find('div', {"class": 'posting-page'})
            opening_link_company_jobs = soup.find('div', {"class": "list-page"})

            if opening_link_application:
                try:
                    #TODO: This is v what we want to avoid!!!
                    company_open_positions = soup.find('a', {"class": "main-header-logo"})
                    application_webpage_html = soup.find("div", {"class": "application-page"})
                    
                    self.lever_co_header(webpage_body, soup)

                    self.company_open_positions_a.click()
                    return
                except:
                    #TODO: Change this Error type!
                    raise ConnectionError("ERROR: Companies other open positions are not present")
                
            elif opening_link_description:
                #try:
                apply_button = None
                
                a_tag_butt = soup.find('a', {'data-qa': 'btn-apply-bottom'})
                div_tag_butt = soup.find('div', {'data-qa': 'btn-apply-bottom'})
                application_at_bottom = soup.find("div", id="application")
                print("Application at bottom or <button>")
                if a_tag_butt:
                    #print("== Application at bottom of page")
                    print("\tPress button to go to application")
                    apply_button = a_tag_butt
                    apply_to_job = self.should_user_apply(opening_link_description)
                elif div_tag_butt:
                    print("\tPress button to go to application")
                    apply_button = div_tag_butt
                    apply_to_job = self.should_user_apply(opening_link_description)    #apply_to_job = boolean | T=.click() && F=.lever_header() -> .company_job_openings()
                if apply_to_job == True:
                    print("1st lever application locked and loaded")
                    apply_button.click()
                    time.sleep(5)
                    current_url = self.browser.current_url
                    soup = self.apply_beautifulsoup(current_url, "html.parser")
                    form_input_details = self.get_form_input_details(current_url)
                    self.insert_resume()
                    self.fill_out_application(form_input_details)
                    self.keep_jobs_applied_to_info()
                    #TODO: If the button is present click OTHERWISE just insert the link
                    #! v v v v vv v v v v v v v v v v v v vv v v v v v v v v v v v v vv v v v v v v v v
                    if self.company_other_openings_href:
                        self.company_other_openings_href.click()
                    else:
                        self.browser.get(self.company_other_openings_href)
                    return
                elif not apply_to_job:
                    #TODO:
                    self.company_other_openings_href.click()
                    return
                #! ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 
                # except:
                #     raise ("Something went wrong with the the greenhouse.io job_description page")
            elif opening_link_company_jobs:
                #TODO: parse through other_company_jobs for "lever"
                self.company_job_openings(soup, None, application_company_name)
            application = opening_link_application
        
               

        
        
        
        
    def lever_co_header(self, webpage_body):
        print("\nlever_co_header()")
        links_in_header = []
        print("\nThese are the links/elements that lead to this companies other available Job Openings:")
        current_url = self.browser.current_url
        print("Current URL: " + current_url)
        links_in_header.append(current_url)
        webpage_header = webpage_body.find('div', {"class": 'main-header-content'})
        self.company_open_positions_a = webpage_header.find('a', {"class": "main-header-logo"})
        print("Selenium Click => Companies other Job Openings: " + self.company_open_positions_a)
        #links_in_header.append(self.company_open_positions_a)
        try:
            if self.company_open_positions_a['href']:
                company_open_positions_href = self.company_open_positions_a['href']
                print("Webpage's Header link: " + company_open_positions_href)
                company_open_positions_url = company_open_positions_href
                links_in_header.append(company_open_positions_url)
        except:
            print("This company's webpage is dumb anyways! Trust me they would've probably overworked you anyways.")
        self.check_header_links(links_in_header)
        return
            
        
        
    def lever_io_dat(self, joby_link, soup):
        self.joby_link = joby_link
        print("=== inside the lever.co")
        #opening_link_application = soup.find('div', class_='page-application')      #application immediate
        opening_link_application = soup.find('div', {"class": 'application-page'})
        #opening_link_description = soup.find('div', class_='page-show')             #regular description start
        opening_link_description = soup.find('div', {"class": 'posting-page'})          #NOTE: In HTML class='one two' needs 2 class calls I think!?!?!?
        print("=== opening_link_application = ", end="")
        #print(opening_link_application)
        print("You are on the Job Application webpage")
        print("=== opening_link_description = ", end="")
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
                print("=== plethora_of_jobs = ", end="")
                print(plethora_of_jobs)
                application_webpage_html = soup.find("div", {"class": "application-page"})
                self.lever_io_application(joby_link, application_webpage_html)
                #return opening_link_application
            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        elif opening_link_description:
            print("=== lever.co is working")
            try:
                print("=== inside the try lever.co")
                position_title = soup.find('h2')
                job_title = position_title.get_text().split()
                print("=== job_title = ", end="")
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
                
                print("=== link_to_apply = ", end="")
                print(link_to_apply)

            except:
                #TODO: Change this Error type!
                raise ConnectionError("ERROR: Companies other open positions are not present")
        #print("=== leaving the lever.co")
        return soup
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    def determine_current_page(self, job_link, application_company_name):
        elif application_company_name == "greenhouse":
            div_main = soup.find("div", id="main")
            job_description_element = self.browser.find_element(By.ID, "content")
            
            #I did it this way because it checks very few elements since 1 of these options are normally literally the next element
            next_elem = div_main.find_next()
            while next_elem:    #NOTE: REMEBER THIS DOESN'T INCREMENT next_elem SO IT'S THE SAME VALUE AS ABOVE!!!!
                if next_elem.name == "div" and (next_elem.get("id") == "flash-wrapper" or next_elem.get("id") == "flash_wrapper"):
                    print('-Job Listings Page')
                    return
                elif (next_elem.name == "div" and next_elem.get("id") == "embedded_job_board_wrapper"):
                    print('-Job Listings Page')
                    return
                elif (next_elem.name == "section" and next_elem.get("class") == "level-0"):
                    print("-Company Job Openings Page")
                    print("A while loop for this is perfect for this because there can be multiple <section class='level-0'>")
                    #TODO: for this one in the elif you have to look through all "level-0" sections!!
                    return
                elif next_elem.name == "div" and next_elem.get("id") in ["app-body", "app_body"]:
                    app_body = next_elem
                    header = next_elem.find("div", id="header")
                    content = next_elem.find("div", id="content")
                    application = soup.find("div", id="application")
                    if header and content:
                        print("Job Description Page")
                        self.greenhouse_io_header(app_body, header, content)    #TODO: return *job_title, company, location, ???*

                        print("Application at bottom or <button>")
                        apply_button = div_main.find("button", text=["Apply Here", "Apply Now", "Apply for this job"])
                        #TODO
 #! ^ MOVE UP 198 ^ ^ ^ ^ ^ ^ ^                       apply_button = div_main.find("button", text=["Apply Here", "Apply Now"])  #NOTE: !!!!! Maybe greenhouse doesn't have <button> ...    maybe it only has <a class="button">!?!?!?
                        #application_below_description = div_main.find("div", id="application")
                        #NOTE: I don't think greenhouse.io house <... target="_blank">
                        if apply_button:
                            print("\tPress button to go to application")
                            should_apply = self.should_user_apply()
                            print("\t\tApply button: ", end="")
                            print(apply_button)
                            if should_apply == True:
                                apply_button.click()
                                time.sleep(5)
                                self.greenhouse_io_application(application)
                            print("\t\tApplication = ", end="")
                            print(application)
                            apply_to_job = self.should_user_apply(application)
                            #return application
                        elif application:
                            #self.should_user_apply(application)
                            print("\tApplication at bottom of page")
                            
                            apply_to_job = self.should_user_apply(content)
                        else:
                            print("\tHmmm that's weird ? it's neither button nor application")
                        
                        self.scroll_to_element(job_description_element)
                        if apply_to_job == True:
                            print("1st greenhouse application locked and loaded")
                            form_input_details = self.get_form_input_details(job_link)
                            print("Meet")
                            time.sleep(8)
                            self.insert_resume()
                            print("me")
                            time.sleep(8)
                            self.fill_out_application(form_input_details)
                            self.keep_jobs_applied_to_info(job_link)
                        elif apply_to_job == False:
                            self.a_href.click()
                            time.sleep(4)
                            return
                    break
                else:
                    next_elem = next_elem.find_next()
            print("Not really sure how the heck we got here and defintiely don't have a clue about where to go from here!?!?!?")
            return
    
    
    
    def greenhouse_io_start_page_decide(self, soup): #if (child of main is one of these)
        print("Welcome fair maiden this company has gathered to make decisions based on your skin color... please after you!")
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
        print("Guess the .greenhouse_io_start_page_detector() while loop doesn't work")
    
    
    
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
            self.print_company_job_openings("greenhouse_io_header()", "greenhouse", JobTitle=self.company_job_title, CompayName=self.company_name, JobLocation=self.company_job_location, JobHREF="Couldnt Find", LinkToApplication_OnPageID=self.a_fragment_identifier)
        else:
            self.print_company_job_openings("greenhouse_io_header()", "greenhouse", JobTitle=self.company_job_title, CompayName=self.company_name, JobLocation=self.company_job_location, JobHREF=self.company_other_openings_href, LinkToApplication_OnPageID=self.a_fragment_identifier)
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
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    