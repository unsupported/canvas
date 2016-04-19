#!/usr/bin/env python
# working as of 4/19/2016
import requests
import time, json, os
import re,pprint

# Change this to match your access token
token="<token>"

BASE_URI = "https://<domain>.instructure.com/api/v1/accounts/self/reports/%s" 

# This headers dictionary is used for almost every request
headers = {"Authorization":"Bearer %s" % token}


# This is the list of parameters used for the sis_export_csv report, I think I'm actually
# missing one, parameters[enrollment_term], but I'm not sure
report_parameters = { "parameters[users]": True }

# Step 1: Start the report (this one is running the SIS export CSV report)
start_report_url = BASE_URI % 'sis_export_csv'
start_report_response = requests.post(start_report_url,headers=headers,params=report_parameters)

# Use the id from that output to check the progress of the report. 
status_url = start_report_url + "/" + start_report_response.json()['id']
status_response = requests.get(status_url,headers=headers)
status_response_json = status_response.json()


# Step 2: Wait for the report to be finished
while status_response_json['progress'] < 100:
  status_response_json = requests.get(status_url,headers=headers).json()
  time.sleep(2) # Sleep 2 seconds in between requests... not strictly required


# Step 3: Download the file

file_info_url = status_response_json['attachment']['url']
file_response = requests.get(file_info_url,headers=headers,stream=True)


# Step 4: Save the file
with open(status_response_json['attachment']['filename'],'w+b') as filename:
    filename.write(file_response.content)

