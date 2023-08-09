#TODO: THIS IS TO INITIALIZE THE USER!!!  SSOOOO FILL IN .env AND etc...

class UntouchedUser():
    
    def __init__(self):
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
        print(f"Alright the next big setup is SpaCy!")
        print("\t1) en_core_web_sm => 12 MB")
        print("\t2) en_core_web_md => 40 MB")
        print("\t3) en_core_web_lg => 560 MB")
            #If this is chosen you want to run => 'python -m spacy download en_core_web_lg'
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
    
    
    
    