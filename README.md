# Web_Scraper


Just copy & paste this
pip install -r requirements.txt

Then run this
python -u AutoApply/JobSearchWorkflow.py

and... BOOM! That's how it's done.


# Summary:
This project is designed to automate the job application process, making it easier and more efficient for users. The only time they insert info is their first time which collects their resume, basic info, and lastly a unqiue summary about their career. The project utilizes ML and SpaCy AI to find and apply to specific jobs the user qualifies for and is interested in. The security is bypassed using OxyLabs(for now) which provides everything from rotational residential IP addesses to CAPTCHA's. The ML adds different answers to every miscellaneous question it comes across while also avoiding security as well by making each answered question unique to each user.

I also built a server that incorporates a FastAPI, MariaDB, data analysis, and output of data to Google Sheets in the form of many useful graphs that provide current insight into the job market in real-time!


AutoApply:
 JobSearchWorkflow.py   - The main program which controls the workflow of everything
 UsersFirstUse.py       - The purpose of this program is to collect all the info from the user in relation to their job search & is also only meant to be run once
 ManageUserJobSearch.py - Part two of aboves file but deals with users technology preferences utilized
 GoogleSearch.py        - The program responsible for opening the users browser to search for job openings, resulting in a list of current roles that meet the users requirements
 CompanyOpeningsAndApplications.py - the file responsible for the entire job application process and is still in 'Under Construction' as it will be broken down into 3 parts which I'll list below
    I. Search for companies other job openings webpage and consider up to 5 other roles(if available)
    II. Read Job description and see if it meets the users requirements AS WELL AS vice versa
    III. Fill out job application to apply
 website_elements.json  - JSON file used to quickly identify and retrieve necessary info WHICH ALSO allows for this program to be extremely adaptable and work with & for more online forms over time

