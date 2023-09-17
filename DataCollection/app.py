from flask import Flask, request, jsonify
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

app = Flask(__name__)

# Load Google Sheets API credentials
credentials = service_account.Credentials.from_service_account_file('path/to/your/credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
spreadsheet_id = 'spreadsheet_id'

sheets_api = build('sheet', 'v4', credentials=credentials)

#Pick things you can make a joke out of!! or things you can use to make a joke out of!!
expected_data = ['Data', 'Job Title', 'Job Location', 'Company', 'Industry', 'Employment Type', 'Education', 'Skills', 'Experience Level', 'Years of Experience', 'Senior Jobs', 'Qualified Jobs']

allowed_employment_types = ['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship']
allowed_experience_levels = ['Entry', '', 'Staff', 'Senior', 'Lead', 'Principal']

def validate_job_data(data):
    if any(field not in data for field in expected_data):
        return False, 'Invalid data format'

    if data['Employment Type'] not in allowed_employment_types:
        return False, 'Invalid Employment Type'

    if data['Experience Level'] not in allowed_experience_levels:
        return False, 'Invalid Experience Level'

    #TODO: Add more checks like insurance it's within users country!!!

    return True, ''

#TODO: REMEMBER IT'S NOT A DB!! So create a method that adds things together if `Industry=Employment Type= Location=Experience Level`

@app.route('/add_job_data', methods=['POST'])
def add_data_to_google():
    data = request.get_json()
    
    is_valid, error_message = validate_job_data(data)
    if not is_valid:
        return jsonify({'message': error_message}), 400
    
    sheet_range = 'Sheet1!A1'
    body = {'values': [data[field] for field in expected_data]}
    sheets_api.spreadsheets().values().append(
        spreadsheetID=spreadsheet_id,
        range=sheet_range,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    
    return jsonify({'message': 'Job data added successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)