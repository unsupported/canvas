#!/usr/bin/env python
# working as of 4/19/2016
import requests
import time, json, os
import re,pprint

# Change this to match your access token
token="<token_here>"
# Change this to match the domain you use to access Canvas.
CANVAS_DOMAIN  = "<domain>.instructure.com"
# Change this to the full path of your desired output folder.  I've set it to the current
# directory for the sake of this script
OUTPUT_FOLDER = os.path.dirname(os.path.abspath(__file__))
# Change this to the term to pull for, otherwise this will pull for all terms.
ENROLLMENT_TERM = False

# Edit each of these to determine which to include in the report
include_deleted_items = False
do_accounts = True
do_courses = False
do_enrollments = False
do_sections = False
do_terms = False
do_users = False
do_xlist = False
do_group_membership = False
do_groups = False

###################################################################################
#### DON'T CHANGE anything after this unless you know what you are doing. #########
BASE_DOMAIN = "https://%s/api/v1/%%s/" %  CANVAS_DOMAIN
BASE_URI = BASE_DOMAIN % "accounts/self/reports" 
BASE_START_URI = BASE_DOMAIN % "accounts/self/reports/%s" 
BASE_FILE_URI =  BASE_DOMAIN % "files/%s"

# This headers dictionary is used for almost every request
headers = {"Authorization":"Bearer %s" % token}

""" These are some of the standard reports every account has access to. """
standard_reports = (
  'student_assignment_outcome_map_csv',
  'grade_export_csv',
  'sis_export_csv',
  'provisioning_csv')

# This is the list of parameters used for the sis_export_csv report, I think I'm actually
# missing one, parameters[enrollment_term], but I'm not sure
report_parameters = {
  "parameters[accounts]": do_accounts,
  "parameters[courses]": do_courses,
  "parameters[enrollments]": do_enrollments,
  "parameters[groups]": do_groups,
  "parameters[group_membership]": do_group_membership,
  "parameters[include_deleted]": include_deleted_items,
  "parameters[sections]": do_sections,
  "parameters[terms]": do_terms,
  "parameters[users]": do_users,
  "parameters[xlist]": do_xlist}

# If ENROLLMENT_TERM isn't False, add it to the parameters list
if ENROLLMENT_TERM != False:
  report_parameters["parameters[enrollment_term]"]=ENROLLMENT_TERM

# Step 1: Start the report
start_report_url = BASE_START_URI % standard_reports[3]
print "running the report..."
start_report_response = requests.post(start_report_url,headers=headers,params=report_parameters)
print start_report_response.text

# Use the id from that output to check the progress of the report. 
status_url = start_report_url + "%s" % start_report_response.json()['id']
status_response = requests.get(status_url,headers=headers)
status_response_json = status_response.json()

# Step 2: Wait for the report to be finished
while status_response_json['progress'] < 100:
  status_response = requests.get(status_url,headers=headers)
  status_response_json = status_response.json()
  time.sleep(4)
  print 'report progress',status_response_json['progress']

file_url = status_response_json['file_url']

file_id_pattern = re.compile('files\/(\d+)\/download')

# Once "progress" is 100 then parse out the number between "files" and "download",
# 22591162 in this case, and use this number to request the files 

# Step 3: Download the file

file_info_url = status_response_json['attachment']['url']
file_response = requests.get(file_info_url,headers=headers,stream=True)


# Step 4: Save the file
with open(status_response_json['attachment']['filename'],'w+b') as filename:
    filename.write(file_response.content)

