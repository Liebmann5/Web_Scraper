#TODO: THIS IS TO INITIALIZE THE USER!!!  SSOOOO FILL IN .env AND etc...
#https://stackoverflow.com/questions/71634422/how-can-i-make-reliable-multiple-choice-questions-in-python

class UntouchedUser():
    
    def __init__(self):
        self.user_data = {
            'UNTOUCHED_USER': 'False',
            'LAST_APPLIED': '',
            'LINKEDIN_USERNAME': '',
            'LINKEDIN_PASSWORD': '',
            'WINDOWS_RESUME_PATH': '',
            'MAC_RESUME_PATH': '',
            'FIRST_NAME': '',
            'MIDDLE_INITIAL': '',
            'LAST_NAME': '',
            'EMAIL': '',
            'PHONE_NUMBER': '',
            'HOME_PHONE': '',
            'LOCATION_CITY': '',
            'ZIP_CODE': '',
            'SCHOOL': '',
            'DEGREE': '',
            'DISCIPLINE': '',
            'SCHOOL_START_DATE_YEAR': '',
            'SCHOOL_END_DATE_YEAR': '',
            'GPA': '',
            'CURRENT_COMPANY': '',
            'CURRENT_TITLE': '',
            'COMPANY_START_DATE': '',
            'CURRENT_EMPLOYEE': '',
            'COMPANY_END_DATE': '',
            'LINKEDIN_PROFILE': '',
            'GITHUB_URL': '',
            'PERSONAL_URL': '',
            'US_CITIZEN': '',
            'GENDER': '',
            'PRONOUNS': '',
            'SEXUAL_ORIENTATION': '',
            'RACE': '',
            'VETERAN': '',
            'DISABILITY': '',
            'SALARY_EXPECTATIONS': '',
            'NON_COMPETE_AGREEMENT': '',
            'COME_ACROSS_HOW': 'indeed',
            'JOB_TYPE': ''
        }
        self.users_job_search_requirements = {}
        self.init_users_job_search_requirements()
        
    def init_users_job_search_requirements(self):
        self.users_job_search_requirements = {
            "user_desired_job_titles": [],
            "user_preferred_locations": [],
            "user_preferred_workplaceType": ["in-office", "hybrid", "remote"],
            "employment_type": [],
            "entry_level": True, 
        }
    
    #print(f"")
    def setup_user(self):
        self.introduction()
        self.set_user_os()
        self.set_user_exp()
        if self.users_job_search_requirements["entry_level"] == True:
            self.ohhh_helen_knows_the_owner()
                    #TODO:  v   add the rest!
            return self.users_job_search_requirements
        self.user_preferred_workplaceType()
        self.employment_type()
        self.user_preferred_locations()
        self.user_desired_job_titles()
        
    def setup_test(self):
        self.users_job_search_requirements = {
            "user_desired_job_titles": ["software engineer", "backend engineer"],
            "user_preferred_locations": [],
            "user_preferred_workplaceType": ["in-office", "hybrid", "remote"],
            "employment_type": [],
            "entry_level": True, 
        }
        return self.users_job_search_requirements
        
    def set_user_exp(self):
        print("Before we get any closer to The Gates of Valhalla, it is of the upmost importance that"
              + "we 1st take care of all this paperwork. You know how this kind of stuff goes documentation,"
              + "signatures, and jurisdiction in the court of law and all that stuff; look at my suit! SSooo"
              + "for the job you are about to search for, do you have any experience in it or absolutely not?")
        user_exp = input()
        if self.validate_user_exp(user_exp):
            self.update_users_job_search_requirements(user_exp)
        else:
            self.set_user_exp()
        return
    
    def set_user_employment_type(self):
        print("Ok now what kind of employment type are you looking for? Like Full-time, Contract, Internship, etc.")
        user_exp = input()
        if self.validate_user_exp(user_exp):
            self.update_users_job_search_requirements(user_exp)
        else:
            self.set_user_exp()
        return
    
    def set_user_preferred_workplaceType(self):
        print("ok of these 3 workplace types, which are you interested in?\n"
              + "  1) in-office\n"
              + "  2) hybrid\n"
              + "  3) remote\n")
        user_exp = input()
        if self.validate_user_exp(user_exp):
            self.update_users_job_search_requirements(user_exp)
        else:
            self.set_user_exp()
        return
    
    def set_user_preferred_locations(self):
        print("ok now pick job locations? This one should be left empty if you are able to move otherwise this\n"
              + "should kinda be treated like if you cant move then just list all the popular nearby cities you can commute too!")
        user_preferred_locations = []
        for i in range(30):
            job_locations = input(f"Enter job location #{i+1}: ")
            user_preferred_locations.append(job_locations)
            if self.validate_user_locations(job_locations):
                #while loop perhaps
                pass
            self.users_job_search_requirements['user_desired_job_titles'].copy(user_preferred_locations)
        return
    
    def set_user_desired_job_titles(self):
        print("ok now type out the job name(s) of ones you want me to search for? Now the max I set is 32,466 but\n"
              + "may I highly suggest you only pick 3 to get the best results! If you want to do more I suggest\n"
              + "you just wait till this ends and then just run it again.")
        user_desired_job_titles = []
        for i in range(32466):
            job_titles = input(f"Enter job title #{i+1}: ")
            user_desired_job_titles.append(job_titles)
            if self.validate_user_job_titles(job_titles):
                #while loop perhaps
                pass
            self.users_job_search_requirements['user_desired_job_titles'].copy(user_desired_job_titles)
        return

    def introduction(self):
        print("Well well well. Somebody needs a job... figures someone like you"
              + " is wanting more money! What a weiner your parents raised. You weiner!")
        #time.sleep(1)
        print("Any who just go ahead and type out the job title you want. "
              + " each job title press ENTER! (When you press ENTER it will probably take "
              + "you to the next line, this is normal... illiterately speaking of course)")
        #time.sleep(1)
        print("Try and keep it to around 3-4 you eager eagle. Exceling past these "
              + "numbers will yield less results, so thats why.")
        #time.sleep(1)
        print("Fianlly for the love of the Hoover Dam please spell the everything correctly! "
              + "If you're not confident then highlight the name with your mouse and click\n"
              + " COPY. When you come back here just right click. If you don't have a right"
              + " click well then huh. Life is tough but get your crap together cause idk")
        #time.sleep(1)
        #TODO       
        # print("Ok now yrs of exp?")
        # user_exp = input()
        # yrs_of_exp.append(user_exp)
        #     -> Add as global like this =>   yrs_of_exp = None  =>  b/c it's an empty string
        # print("Ok and which locations?")
        # location = input()
        # (.env).add(location)    #so it's saved on their system
        # user_location.appemd(location)
        #     ==> When printed in search do   ==>   " & near=" + user_location
        #self.search_for_jobs(self)
        return
    
    def set_user_os(self):
        print("Ok now what kind of computer are using a\n"
              + "  1) Mac\n"
              + "  2) Windows\n"
              + "  3) Linux\n")
        user_exp = input()
        if self.validate_user_exp(user_exp):
            self.update_users_job_search_requirements(user_exp)
        else:
            self.set_user_exp()
        return
    
    #TODO: Maybe write a script that confirms the user did it right!?!?!?
    def set_misc_software(self):
          print("ight loser you gotta download a few things cause God only knows I tried to do it for you but")
          print("these people must hate fun!")
          print("Any ways download python: https://www.python.org/downloads/")
          print("Right smack dab at the sorta top you should see these words 'Download the latest version' just click the yellow button and work through it till Python is downloaded")
          
          print("Then download rust: https://www.rust-lang.org/tools/install")
          print("You're on your own for this one buddy...  my bad. Have ChatGPT walk you through it!")
          
          print("And if you are on Windows then msTools: https://visualstudio.microsoft.com/downloads/")
          print("\tScroll all the way to the bottom and click 'Tools for Visual Studio'")
          print("\tand then click download 'Build Tools for Visual Studio 2022'")
          
          print("????? Maybe you gotta download pip no clue though ??")       #!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------------------------------------------
          print("")
          print("")
    
    
    def users_NLP_model(self):
          print("Are you on a desktop or laptop? Do you have access to a Desktop and does that Desktop 1) Have a 500 Gb Hard Drive")
          print("and 2) a graphics card!? If your answers weren't 100% yes then GPT-Neo-1.3B is what you should pick! Then you can pick")
          users_NLP_model = self.roulette_the_NLP()
          print("between the (sm, md, lg) models. I've been told the higher you go up this latter will provide better and more accurate")
          print("answers. ")
          print("GPT-Neo-1.3B     ~ => 22 Gb\n"
                + "  https://huggingface.co/EleutherAI/gpt-neo-1.3B/tree/main")
          print("GPT-Neo-2.7B     ~ => 45 Gb\n"
                + "  https://huggingface.co/EleutherAI/gpt-neo-2.7B/tree/main")
          
    def set_spacy(self):
        print("Alright the next big setup is SpaCy!")
        print("\t1) en_core_web_sm => 12 MB")
        print("\t2) en_core_web_md => 40 MB")
        print("\t3) en_core_web_lg => 560 MB")
        print("Type the number, and only the number, of the one you want!")
        user_exp = input()
        if self.validate_user_exp(user_exp):
            self.update_users_job_search_requirements(user_exp)
        else:
            self.set_user_exp()
        return
    
#          print("")
#          print("")

      
    def recommend_user_resume(self):
          print("This place is tight to if you need a resume go here -> ", end="")
          print("https://www.resume.lol/")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #print("\n()")
    def ohhh_helen_knows_the_owner(self):
        print("\nohhh_helen_knows_the_owner()")
        self.collect_personal_info()
        self.collect_education_info()
        self.collect_professional_info()
        self.collect_job_search_info()
        self.collect_social_info()
        self.collect_eelo_info()
        self.write_to_env_file()
        self.collect_job_search_requirements()
        
    def collect_personal_info(self):
        print("\ncollect_personal_info()")
        self.user_data['FIRST_NAME'] = input("Enter your first name: ")
        self.user_data['MIDDLE INITIAL'] = input("Enter your middle initial: ")
        self.user_data['LAST_NAME'] = input("Enter your last name: ")
        self.user_data['EMAIL'] = input("Enter your email: ")
        self.user_data['PHONE_NUMBER'] = input("Enter your phone number: ")
        self.user_data['HOME_PHONE'] = input("Enter your home phone: ")
        self.user_data['LOCATION_CITY'] = input("Enter your city: ")
        self.user_data['ZIP_CODE'] = input("Enter your zip code: ")
    
    def collect_education_info(self):
        print("\ncollect_education_info()")
        self.user_data['SCHOOL'] = input("Enter your school: ")
        self.user_data['DEGREE'] = input("Enter your degree: ")
        self.user_data['DISCIPLINE'] = input("Enter your discipline: ")
        self.user_data['SCHOOL_START_DATE_YEAR'] = input("Enter your school start date year: ")
        self.user_data['SCHOOL_END_DATE_YEAR'] = input("Enter your school end date year: ")
        self.user_data['GPA'] = input("Enter your GPA: ")
        
    def collect_professional_info(self):
        print("\ncollect_professional_info()")
        self.user_data['CURRENT_COMPANY'] = input("Enter your current company: ")
        self.user_data['CURRENT_TITLE'] = input("Enter your current title: ")
        self.user_data['COMPANY_START_DATE'] = input("Enter your company start date: ")
        self.user_data['CURRENT_EMPLOYEE'] = input("Are you a current employee? (Yes/No): ")
        self.user_data['COMPANY_END_DATE'] = input("Enter your company end date (if applicable): ")
        self.user_data['LINKEDIN_PROFILE'] = input("Enter your LinkedIn profile URL: ")
        self.user_data['GITHUB_URL'] = input("Enter your GitHub URL: ")
        self.user_data['PERSONAL_URL'] = input("Enter your personal website URL: ")
        
    def collect_job_search_info(self):
        print("\ncollect_job_search_info()")
        self.user_data['JOB_TYPE'] = input("Enter the job type you're looking for (Full-time, Contract, etc.): ")
        self.user_data['SALARY_EXPECTATIONS'] = input("Enter your salary expectations: ")
        self.user_data['NON_COMPETE_AGREEMENT'] = input("Do you have a non-compete agreement? (Yes/No): ")
        self.user_data['COME_ACROSS_HOW'] = input("How did you come across this job? (e.g., indeed): ")

    def collect_social_info(self):
        print("\ncollect_social_info()")
        self.user_data['LINKEDIN_USERNAME'] = input("Enter your LinkedIn username: ")
        self.user_data['LINKEDIN_PASSWORD'] = input("Enter your LinkedIn password: ")
        self.user_data['WINDOWS_RESUME_PATH'] = input("Enter your resume path for Windows: ")
        self.user_data['MAC_RESUME_PATH'] = input("Enter your resume path for Mac: ")
        self.user_data['LINKEDIN_PROFILE'] = input("Enter your LinkedIn profile URL: ")
        self.user_data['GITHUB_URL'] = input("Enter your GitHub URL: ")
        self.user_data['PERSONAL_URL'] = input("Enter your personal website URL: ")

    #TODO: Update these to the actual 'EELO' Questions!!!!
    def collect_eelo_info(self):
        print("\ncollect_eelo_info()")
        self.user_data['US_CITIZEN'] = input("Are you a U.S. citizen? (Yes/No): ")
        self.user_data['GENDER'] = input("Enter your gender: ")
        self.user_data['PRONOUNS'] = input("Enter your pronouns: ")
        self.user_data['SEXUAL_ORIENTATION'] = input("Enter your sexual orientation: ")
        self.user_data['RACE'] = input("Enter your race: ")
        self.user_data['VETERAN'] = input("Are you a veteran? (Yes/No): ")
        self.user_data['DISABILITY'] = input("Do you have a disability? (Yes/No): ")
        
    #TODO: Add this to module file!!
    def write_to_env_file(self):
        print("\nwrite_to_env_file()")
        with open('.env', 'r') as file:
            lines = file.readlines()
            
        updated_lines = []
        for line in lines:
            key, env_value = line.strip().split('=', 1)
            if key in self.user_data and env_value != (f"'{self.user_data[key]}'"):
                new_env_value = (f"'{self.user_data[key]}'\n")
                updated_lines.append(line.replace(env_value, new_env_value))
            else:
                updated_lines.append(line)
                
        with open('.env', 'w') as file:
            file.writelines(updated_lines)
            
        return print("User data collected and written to .env file.")
        
    def collect_job_search_requirements(self):
        print("\ncollect_job_search_requirements()")
        # Collect desired job titles
        self.users_job_search_requirements["user_desired_job_titles"] = input("Enter desired job titles (comma-separated): ").split(',')

        # Collect preferred locations
        self.users_job_search_requirements["user_preferred_locations"] = input("Enter preferred locations (comma-separated): ").split(',')

        # Collect preferred workplace type
        print("Select preferred workplace types (comma-separated):")
        print("1) in-office")
        print("2) hybrid")
        print("3) remote")
        workplace_type_choices = input("Enter your choices (e.g., 1,2,3): ").split(',')
        workplace_type_map = {
            "1": "in-office",
            "2": "hybrid",
            "3": "remote"
        }
        selected_workplace_types = [workplace_type_map[choice.strip()] for choice in workplace_type_choices if choice.strip() in workplace_type_map]
        self.users_job_search_requirements["user_preferred_workplaceType"] = selected_workplace_types

        # Collect employment type
        self.users_job_search_requirements["employment_type"] = input("Enter employment type (e.g., Full-time, Contract, Internship): ")

        # Collect entry level preference
        entry_level_choice = input("Is this an entry-level position? (Yes/No): ")
        self.users_job_search_requirements["entry_level"] = entry_level_choice.lower() == 'yes'

        print(self.users_job_search_requirements)
        return print("Job search requirements collected successfully.")
