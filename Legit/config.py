#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# When coming up with custom names -> figure out how ChatGPT does it!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CUSTOM_RULES = {
    "Full name": ["FIRST_NAME", " ", "MIDDLE_NAME", " ", "LAST_NAME"],
    "Signature": ["FIRST_NAME", " ", "LAST_NAME"],
    "Address": ["91293 Reje Ct.", " ", "USERS_CITY", ", ", "USERS_STATE", " ", "USERS_ZIP_CODE"],
    "Start Availability": ["self.time_program_ran" + " " + "add 2 weeks(self.time_program_ran+336hrs)"],
    "Name and Date": ["FIRST_NAME", " ", "LAST_NAME", " ", "self.time_program_ran"],
    "Software Engineer": ["Software Developer"],
    "Location (City)": ["LOCATION_CITY", ", ", "LOCATION_STATE"],
},
#TODO: I'm fairly certain I'd want these switched!?!?!?
#TODO: Add degrees!! So  B.S. = Bachelors of Science
CUSTOM_SYNONYMS = {
    "phone": ["PHONE_NUMBER", "PERSONAL_CELL", "CELLPHONE", "PHONE"],
    "linkedIn profile": ["LINKEDIN_PROFILE"],
    "website": ["GITHUB_URL"],
    "github": ["GITHUB_URL"],
    "portfolio": ["GITHUB_URL"],
    "require immigration sponsorship": ["US_CITIZEN"],
    "require visa sponsorship": ["US_CITIZEN"],
    "hear about job": ["COME_ACROSS_HOW"],
    # "website": ["GITHUB_URL"],
    # "website": ["GITHUB_URL"],
},
Q_AND_A = {
    "summary": ["I'm a to do it all! The movie Dodgeball was about me."],
}
