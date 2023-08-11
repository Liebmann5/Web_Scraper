import requests
import hashlib
# Module for signing my data
from .signature_helper import sign_data

from fastapi import FastAPI
from pydantic import BaseModel

class JobData(BaseModel):
    job_url: str
    job_title: str
    job_location: str
    company_name: str
    job_workplaceType: str
    company_department: str
    job_id_number: str
    job_release_date: str
    employment_type: str
    experience_level: str
    years_of_experience: int
    company_industry: str

class DataSender:
    def __init__(self, jobs_applied_to_this_session, raspberry_pi_address):
        self.jobs_applied_to_this_session = jobs_applied_to_this_session
        self.raspberry_pi_address = raspberry_pi_address
        self.cert_path = "path/to/your/cert.crt"
        self.key_path = "path/to/your/private.key"

    # Code to send data to the Raspberry Pis
    # This could be done using HTTP requests, sockets, or another method
    def send_data(self, data):
        # Sign the data with your private key
        signature = sign_data(data, self.key_path)

        #TODO: Doen't the 'signature' assignment in .signature_helper do this!?!?
            #TODO: Hence making this useless?? Or is everything perfect and correct???
            #NOTE: Don't think so actually! payload is just pre-emtively making a dictionary variable for JSON, which includes ?its normal variables?
        # Include the signature with the data
        payload = {
            'data': data,
            'signature': signature
        }

        # Send the request with the client certificate
        response = requests.post(
            self.raspberry_pi_address,
            json=payload,
            cert=(self.cert_path, self.key_path),
            verify="path/to/server_cert.crt"
        )
        
        # Ensure success otherwise figure out issue and try again
        if response.status_code != 200:
            self.handle_failure(response)

        return response.json()

    # Code to handle failures in sending data, possibly logging or retrying
    # This might include logging the error, retrying the request, or notifying an admin
    #def handle_failure(self, error):
    def handle_failure(self, response):
        pass




