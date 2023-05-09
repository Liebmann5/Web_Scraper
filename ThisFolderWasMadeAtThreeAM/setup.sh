@!/bin/bash

#Create a virtual environment
python3 -m venv awesome_i_can_name_this_anything_uhhhh_apple_sucks

#Create the virtual environment
source awesome_i_can_name_this_anything_uhhhh_apple_sucks/bin/activate

#Install dependencies
pip install -r requirements.txt

#Run my Thing that does stuff....   hopefully
python ../Legit/JobSearchWorkflow.py

#Deactivate the virtual environment
deactivate