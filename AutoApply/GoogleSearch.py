import time
import contextlib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException


from UsersFirstUse import UntouchedUser

class scraperGoogle():
    """
    This class is in charge of just doing the google search with any and all specific considerations needed by the user!
    Have the headless mode to work faster but stuck with this slower version to make sure my code is perfect before
    making that switch. However, and most likely just for now but the security seems to like this slow version better!
    """
    
    def __init__(self, browser):
        """
        Initializes the scraperGoogle class with the browser instance and default search criteria.
        
        Sets up the initial state for a new Google scraper object, including empty lists for job search criteria, links, and results, as well as default values for search parameters.
        
        Parameters:
        - browser (WebDriver): The Selenium WebDriver instance to use for web scraping.
        
        Returns:
        - None
        """
        self.browser = browser
        self.user_desired_jobs = []
        self.good_locations = None
        self.bad_locations = None
        self.list_first_index = 0
        self.list_last_index = 0
        self.links_to_jobs = []
        self.previous_results_count = 0
        self.job_links_counter = 0
        self.results_from_search = []
        self.google_search_results_links = []
        #TODO: No longer needed so get rid of this
        self.last_link_from_google_search = None
        
        
        self.users_job_search_requirements = {}
        self.google_search_banner_titles = []
        
        
        
        #! NEW  NEW  NEW  NEW  NEW  NEW  NEW  NEW  NEW
        self.user_preferred_workplaceType = ["in-office", "hybrid", "remote"]
        self.user_preferred_locations = []
        #NOTE: if senior_experience is true then everything is fair game but...  if it's False create this new variable!!!!
        # if senior_experience == False:
        #     self.avoid_these_job_titles = ["senior", "sr", "principal", "lead", "manager"]
        #self.senior_experience = senior_experience
        self.avoid_these_job_titles = ["senior", "sr", "principal", "lead", "manager"]
        
        
        
        
#!============== initialize variables ====================
    #TODO: Uhhhhh?  Maybe this should be added to ManageUserJobSearch.py?!?!?!
    def fill_users_job_search_requirements(self, *args):
        """
        Fills the user's job search requirements with additional criteria.
        
        This method is intended to dynamically add job search criteria (e.g., desired job titles) provided as arguments. Note: Implementation needs to be corrected to properly update the 'users_job_search_requirements' dictionary.
        
        Parameters:
        - *args (str): Variable length argument list representing additional job search criteria.
        
        Returns:
        - None
        
        Note:
        - Current implementation does not accurately update the 'users_job_search_requirements'. Needs revision.
        """
        for arg in args:
            #Fairly certain this is absolutely wrong but it's just here as a Note...
            self.users_job_search_requirements('user_desired_job_title').append(arg)
        
    #TODO: ENSURE THIS IS CORRECT !!!!!
        #TODO: Add variable  user_blacklisted_locations == self.bad_locations
    def init_users_job_search_requirements(self):
        """
        Initializes the user's job search requirements with the current state of search criteria.
        
        Sets up or resets the 'users_job_search_requirements' dictionary with the current lists of desired job titles, preferred locations, workplace types, and additional flags for employment type and entry-level positions.
        
        Parameters:
        - None
        
        Returns:
        - None
        
        Note:
        - 'employment_type' is currently not utilized for filtering search results but is reserved for future use.
        - Assumes 'entry_level' is True for all searches, which may need adjustment for broader use cases.
        """
        self.users_job_search_requirements = {
            "user_desired_job_titles": self.user_desired_jobs,
            "user_preferred_locations": self.user_preferred_locations,
            "user_preferred_workplaceType": self.user_preferred_workplaceType,
            "employment_type": [],  #Not really something I'm checking for
            "entry_level": True, 
        }
#!========================================================
    
    
    
#!============== testing methods ====================
    #TODO: LAST_APPLIED => If anything less than 3 days -> 24 hrs | If anything > 3 days filter by -> Past Week | If anything > 2 weeks just do -> anytime
        #TODO: But show the user LAST_APPLIED and let them pick
    def ludacris_speed(self):
        """
        Initiates a basic job search flow focused on the role of a "software engineer".
        
        This method is designed to demonstrate a simplified version of the job search process,
        quickly adding a single job title ("software engineer") to the user's desired job list.
        It's part of a suite of methods showcasing different search intensities and workflows.
        
        Parameters:
        - None

        Returns:
        - None
        """
        self.user_desired_jobs.append("software engineer")
        return
    
    def plaid_speed(self):
        """
        Conducts a comprehensive job search workflow, adding multiple engineering roles to the user's desired jobs list.
        
        This method demonstrates an extensive job search process by including a variety of engineering positions,
        such as "software engineer", "backend engineer", and "full-stack engineer", into the search criteria.
        It's designed to showcase a more detailed and thorough demonstration compared to simpler workflows.
        
        The method also initiates a search process, illustrating how the application processes multiple job queries.
        
        Parameters:
        - None

        Returns:
        - None
        Note: The search for "frontend engineer" and a generic "engineer" role is currently commented out to focus the demonstration on specific backend and full-stack roles.
        """
        self.user_desired_jobs.append("software engineer")
        self.user_desired_jobs.append("backend engineer")
        self.user_desired_jobs.append("full-stack engineer")
        # self.user_desired_jobs.append("frontend engineer")
        # self.user_desired_jobs.append("engineer")
        self.search_for_jobs()
        return
    
    def purely_for_testing_and_examples(self, walkthrough_choice):
        """
        Executes the specified job search workflow to demonstrate the application's functionality.
        
        This method supports different speeds of workflow demonstration, including 'ludacris' and 'plaid',
        to show various aspects of the job search process. 'Ludacris' speed focuses on a quick demonstration,
        while 'plaid' speed provides a more thorough walkthrough with additional job roles.
        
        Parameters:
        - walkthrough_choice (str): The method name of the requested speed workflow. 
        Acceptable values include 'ludacris' and 'plaid'.
        
        Returns:
        - tuple: A tuple containing the following elements:
            - google_search_results_links (list[str]): A list of URLs from the job search results.
            - last_link_from_google_search (str): The URL to start from in the list of search results.
            - user_desired_jobs (list[str]): A list of job titles that the user is interested in searching for.
        """
        if walkthrough_choice == 'ludacris':
            self.ludacris_speed()
        elif walkthrough_choice == 'plaid':
            self.plaid_speed()
        self.new_new_print_google_search_results()
        print("Returning back to JobSearchWorkflow")
        time.sleep(2)
        return self.google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs
#!==================================================
    
    
    
#!============== query configs ====================
    def user_requirements(self):
        """
        Initializes the user's job search requirements by setting up test data and starting the job search process.
        
        This method retrieves initial job search criteria, including desired job titles, from a test setup and initiates the search process. It also prints the search results and returns various search parameters and results for further processing.
        
        Parameters:
        - None
        
        Returns:
        - tuple: Contains the following elements:
            - google_search_results_links (list[str]): A list of URLs from the job search results.
            - last_link_from_google_search (str): The URL to start from in the list of search results.
            - user_desired_jobs (list[str]): A list of job titles that the user is interested in searching for.
            - user_preferred_locations (list[str]): A list of preferred job locations by the user.
            - user_preferred_workplaceType (list[str]): A list of preferred workplace types by the user.
            - users_job_search_requirements (dict): A dictionary containing all job search requirements as set up by the test.
        """
        #self.ludacris_speed()
        self.users_job_search_requirements = UntouchedUser().setup_test()
        self.user_desired_jobs = self.users_job_search_requirements["user_desired_job_titles"]
        #self.bad_locations = self.users_job_search_requirements["user_preferred_locations"]
        
        self.search_for_jobs()
        self.new_new_print_google_search_results()
        print("Returning back to JobSearchWorkflow\n\n")
        time.sleep(2)
        #return self.google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs, self.user_preferred_locations, self.user_preferred_workplaceType
        #self.init_users_job_search_requirements()
        return self.google_search_results_links, self.last_link_from_google_search, self.user_desired_jobs, self.user_preferred_locations, self.user_preferred_workplaceType, self.users_job_search_requirements

    def search_for_jobs(self):
        """
        Conducts a job search based on the user's desired job titles and prints the search progress.
        
        This method forms a search query using the desired job titles stored in the user's job search requirements. It also handles the setup for further refining the search based on location and prints intermediary search steps to the console.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        job_titles = self.user_desired_jobs  #TODO: < Ummmm does that work

        print('Searching for ' + ", ".join(job_titles) + ' jobs...')
        search_bar = self.browser.find_element(By.NAME, "q")
        search_bar.clear()
        search_bar.send_keys('site:lever.co | site:greenhouse.io')     #('site:lever.co | site:greenhouse.io | site:workday.com')
        print('1/2')
        time.sleep(1)
        job_titles_string = ' ("'
        for i, job in enumerate(job_titles):
            if i == len(job_titles)-1 or len(job_titles) == 0:
                job_titles_string += f'{job}")'
            else:
                job_titles_string += f'{job}" | "'
        search_bar.send_keys(job_titles_string)
        print('2/2')
        print("Searching google for...       adult films?")
        time.sleep(1)

        self.search_locations(search_bar)
        return
    
    '''
    #NOTE: google already returns too few jobs AND since time is not of the essance... this will hopefully lead the users to find some hidden gems!!!
    # def filter_out_experience(self, search_bar):
    #     if self.senior_experience == False:
    #         search_bar.send_keys(('-'.join(self.avoid_these_job_titles) + ' '))
    '''
    
    #TODO       -   -   -   -   - > user_preferred_locations
    def search_locations(self, search_bar):
        """
        Refines the job search based on the user's preferred locations.
        
        This method adds location preferences to the job search query if specified. It then proceeds to filter the search results based on the specified time frame and prints intermediary steps to the console.
        
        Parameters:
        - search_bar (WebElement): The web element for the search input field.
        
        Returns:
        - None
        """
        requested_job_locations = None
        if not self.user_preferred_locations:
            self.filter_search_time_frame(search_bar)
            #TODO: remove this 'return' when ready Forest
            return
        else:
            requested_job_locations = self.user_preferred_locations

        print("Specifying search to only return job's within the " + ", ".join(requested_job_locations) + " area...  maybe")
        print("1/2")
        time.sleep(1)
        print("most likely not though")
        job_locations_string = ' ("'
        for i, location in enumerate(requested_job_locations):
            if i == len(requested_job_locations):
                job_locations_string += f'{location}") '
            else:
                job_locations_string += f'{location}" | "'
        search_bar.send_keys(job_locations_string)
        print("2/2")
        self.filter_search_time_frame(search_bar)
        return
    
    def filter_search_time_frame(self, search_bar):
        """
        Filters the job search results based on a specified time frame.
        
        Applies filters to the job search results to limit them to a specific time frame, such as the past 24 hours. It adjusts the viewport for better visibility of the results and processes the filtered search results.
        
        Parameters:
        - search_bar (WebElement): The web element for the search input field.
        
        Returns:
        - None
        """
        search_bar.send_keys(Keys.RETURN)
        print("TAAAA DDDAAAAAA")
        time.sleep(1)
        self.adjust_viewport()
        print("GET LOST WIZARD!")
        time.sleep(1)

        tools_butt = self.browser.find_element(By.XPATH, "//div[text()='Tools']")
        tools_butt.click()

        any_time_butt = self.browser.find_element(By.XPATH, "//div[text()='Any time']")
        any_time_butt.click()
        decisi = "24"

        if decisi == "24":
            past_24 = self.browser.find_element(By.XPATH, "//a[text()='Past 24 hours']")
            past_24.click()
        elif decisi == "7":
            past_week = self.browser.find_element(By.XPATH, "//a[text()='Past week']")
            past_week.click()
        else:
            raise TypeError('ERROR: Didnt pick a registered time!')
        print(f"Filtering by past {decisi}")
        time.sleep(1)
        #self.search_results(self.list_first_index, self.list_last_index)
        #self.job_search_workflow()
        #self.search_results(self.list_first_index)
        self.process_search_results()
        return
    
    def adjust_viewport(self):
        """
        Adjusts the browser viewport to match the window size for optimal visibility of search results.
        
        This method sets the viewport dimensions to ensure all search results are visible within the current window size. It's utilized during the job search process to facilitate result review.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        # Get the current window size
        window_width = self.browser.execute_script("return window.innerWidth;")
        window_height = self.browser.execute_script("return window.innerHeight;")

        # Set the viewport to match the window size
        self.browser.execute_script(f"document.documentElement.style.setProperty('width', '{window_width}px');")
        self.browser.execute_script(f"document.documentElement.style.setProperty('height', '{window_height}px');")
        self.browser.execute_script("document.documentElement.style.setProperty('overflow', 'hidden');")
#!=================================================



#!============== collect links ====================
    def scroll_to_bottom(self):
        """
        Scrolls the browser window to the bottom of the search results page.
        
        Executes a script to scroll down to the bottom of the page, allowing for the loading of additional search results. It checks if the page height has changed as an indicator of new results being loaded.
        
        Parameters:
        - None
        
        Returns:
        - bool: True if new results were loaded (indicated by a change in page height), False otherwise.
        """
        prev_height = self.browser.execute_script("return document.body.scrollHeight")
        print('\n\n\n')
        print("increment_search_results")
        print("****************************************************************")
        print(f"Current Height == {str(prev_height)}")

        #! This is what does the actual scrolling!!!
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        print("Scrolled...")

        new_height = self.browser.execute_script("return document.body.scrollHeight")
        print(f"New Height == {str(new_height)}")
        return new_height != prev_height

    def process_search_results(self):
        """
        Processes the loaded search results, handling pagination and scrolling through search pages.
        
        Iteratively processes search results, scrolls through pages, and manages pagination to capture all relevant job links until the end of search results is reached or no more results can be loaded.
        
        Parameters:
        - None
        
        Returns:
        - None
        """
        list_first_index = 0
        list_last_index = 0
        while True:
            list_last_index = self.search_results(list_first_index, list_last_index)
            
            if not self.scroll_to_bottom():
                if self.end_of_search():
                    print("I'm the issue 2")
                    break
                
                if not self.get_more_results():
                    print("I'm the issue 3")
                    break
        print("I'm the issue 4")
            
    def search_results(self, list_first_index, list_last_index):
        """
        Captures search results from the current view and stores job links and titles.
        
        This method captures and processes job links and titles from the visible part of the search results. It updates indices for pagination and prepares for the next batch of results loading.
        
        Parameters:
        - list_first_index (int): The starting index for capturing results in the current view.
        - list_last_index (int): The last index processed from the previous batch of search results.
        
        Returns:
        - int: The updated last index after processing the current batch of search results.
        """
        #TODO: I forgot where this was supposed to be applied?!?!?!?!
        # Wait for the last result from the previous search to appear on the page
        # if self.results_from_search:
        #     last_result = self.results_from_search[-1]
        #     WebDriverWait(self.browser, 10).until(
        #         EC.visibility_of(last_result)
        #     )
        initial_length = len(self.results_from_search)

        if list_first_index == 0:
            self.results_from_search = self.browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index})")
            list_last_index = len(self.results_from_search)
        else:
            self.results_from_search = self.browser.find_elements(By.CSS_SELECTOR, f"div.g:nth-child(n+{list_first_index+1})")
            list_last_index = list_first_index + len(self.results_from_search)

        for count, results_link in enumerate(self.results_from_search[initial_length:], initial_length):
            print('--------------------------------')
            print(f"{str(count + 1)}/{str(list_last_index)}")
            print(results_link)
            link = results_link.find_element(By.CSS_SELECTOR, "a")  #"h3.LC201b > a"
            print(f"Here is link #{count+1}: ", end="")
            job_link = link.get_attribute("href")
            print(job_link)
            self.google_search_results_links.append(job_link)

            if (count+1) == list_last_index:
                self.last_link_from_google_search = results_link
                print("\nvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
                print(self.last_link_from_google_search)
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")

            #TODO: I believe I got rid of this
            if count == list_last_index:
                list_first_index = list_last_index
                break
            self.google_search_banner_titles.append(results_link.find_element(By.XPATH, ".//h3").text)
        print("\nI am at end of search_results()...")
        print(
            f"First Index = {str(list_first_index)} && Last Index = {str(list_last_index)}"
        )
        return list_last_index
    
    def get_more_results(self):
        """
        Attempts to load more search results by clicking the 'More results' button, if available.
        
        This method checks for the presence of a 'More results' button and attempts to click it to load additional job listings. It handles cases where the button is hidden or not present.
        
        Parameters:
        - None
        
        Returns:
        - bool: True if additional results are successfully loaded, False if the button is not found or is hidden.
        """
        try:
            if more_results := self.browser.find_element(By.XPATH, "//span[text()='More results']"):
                parent_a_element = more_results.find_element(By.XPATH, "./ancestor::a")
                is_hidden = False
                
                if parent_a_element.get_attribute('data-ve-view') != "":
                    print("Warning: 'More results' button found in the code but...   is HIDDEN")
                    is_hidden = True

                # aria_hidden_elements = parent_a_element.find_elements(By.XPATH, ".//*[@aria-hidden='true']")
                # if aria_hidden_elements:
                #     print("Warning: 'More results' button found in the code but...   is HIDDEN")
                #     is_hidden = True

                if not is_hidden:
                    print("Found the more_results button")
                    more_results.click()
                    print("Clicked 'More results' button")
                    time.sleep(2)
                    return True

            print("No 'More results' button found or button is hidden")
            print("THIS COULD BE THE REASON FOR ERRORS!! idk though dog... soundproof spectacles")
            return False
        except NoSuchElementException:
            print("No 'More results' button found")
            return False

    def end_of_search(self):
        """
        Checks if the end of the search results has been reached.
        
        Determines if a message indicating no more search results are available is present on the page, signifying the end of the search process.
        
        Parameters:
        - None
        
        Returns:
        - bool: True if the end of search results message is found, False otherwise.
        """
        #TODO: I forgot what this does??
        with contextlib.suppress(NoSuchElementException):
            if no_more_results := self.browser.find_element(By.XPATH, "//a[text()='repeat the search with the omitted results included']"):
                print("No more search results")
                time.sleep(2)
                return True
        return False 
#!================================================
    
    
    
    
    
#!============== print methods ====================
    def print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.results_from_search):
            self.job_links_counter += 1
            print("Result #" + str(self.job_links_counter) + " from Google Seaech")
            print("\tJob Title: ", end="")
            print(job)
            print("\tLink to Job: ", end="")
            print(self.links_to_jobs[i])
        print('--------------------------------------------')
        return
    
    def new_print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.results_from_search):
            self.job_links_counter += 1
            print("Result #" + str(i+1) + " from Google Seaech")
            print("\tJob Title: ", end="")
            print(job)
            print("\tLink to Job: ", end="")
            print(self.links_to_jobs[i])
        print('--------------------------------------------')
        return
    
    def new_new_print_google_search_results(self):
        print('--------------------------------------------')
        print("Results from this Google Search: ")
        for i, job in enumerate(self.google_search_results_links):
            self.job_links_counter += 1
            print("Result #" + str(i+1) + " from Google Seaech")
            print("\tJob Title: ", end="")
            print(self.google_search_banner_titles[i])
            print("\tLink to Job: ", end="")
            print(self.google_search_results_links[i])
        print('--------------------------------------------')
        return
#!=================================================
