#!/usr/bin/env python
# working as of 6/8/2018
import requests
import time, json, os
import re,pprint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

### NOTES: ###
# 1. You can use an external credentials file to (slightly) increase security.
#   a. This works for both token and email credential information.
# 2. All <> angle brackets are designed to be replaced with your data. DO NOT INCLUDE THEM.

# Change this to match your access token
token = "<replace with your Canvas token>"

# Change this to match the domain you use to access Canvas
CANVAS_DOMAIN  = "<replace domain>.instructure.com"

# Change this to the full path of your desired output folder - always use / whether linux or Windows
# Always include trailing / and uncomment options to create directories

# DATE_TODAY = time.strftime("%m-%d-%y/")
# OUTPUT_FOLDER = "<C:/Users/example/output_folder/%s>" % DATE_TODAY
OUTPUT_FOLDER = "<C:/Users/example/output_folder/>"

#if not os.path.exists(OUTPUT_FOLDER):
#	os.makedirs(OUTPUT_FOLDER)

# Change this to the term ID to pull for, otherwise this will pull for all terms
# Use API call to find term IDs: https://<domain>.instructure.com/api/v1/accounts/<account_id>/terms
ENROLLMENT_TERM = False

# Change account ID - use "self" for the account attached to the token provided
# MUST BE A STR
# Change to limit scope of report being pulled (i.e., "1" pulls for root account)
ACCOUNT_ID = "1"

# Change this to set email server and FROM email address (example is O365)
smtpserver = "smtp.office365.com:587"
from_addr = "<example@domain.edu>"

# Add email addresses to this list as recipients
to_list = ["<example2@domain.edu>","<example3@domain.edu>"]

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
############# BE EXTREMELY CAREFUL CHANGING ANY INFORMATION BELOW #################

BASE_DOMAIN = "https://%s/api/v1/%%s/" % CANVAS_DOMAIN
BASE_URI = BASE_DOMAIN % "accounts/%s/reports" % ACCOUNT_ID
BASE_START_URI = BASE_DOMAIN % "accounts/%s/reports/%%s" % ACCOUNT_ID
BASE_FILE_URI =  BASE_DOMAIN % "files/%s"

# This headers dictionary is used for almost every request
headers = {"Authorization":"Bearer %s" % token}

# Use list indices to indicate report to run - default is [0]
standard_reports = (
  "proserv_student_submissions_csv", #0
  "grade_export_csv", #1
  "mgp_grade_export_csv", #2
  "last_user_access_csv", #3
  "last_enrollment_activity_csv", #4
  "provisioning_csv", #5
  "recently_deleted_courses_csv", #6
  "student_assignment_outcome_map_csv", #7
  "unpublished_courses_csv", #8
  "course_storage_csv", #9
  "unused_courses_csv", #10
  "zero_activity_csv", #11
  "lti_report_csv", #12
  "outcome_results_csv") #13

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

# CHANGE INDICES TO RUN REPORTS
reports_requested = [8,10,11]
i = 0

for report_index in reports_requested:
	# Step 1: Start the report
	start_report_url = BASE_START_URI % standard_reports[report_index]

	print("running the report...")
	start_report_response = requests.post(start_report_url,headers=headers,params=report_parameters)
	print(start_report_response.text)

	# Use the id from that output to check the progress of the report.
	status_url = start_report_url + "%s" % start_report_response.json()["id"]
	status_response = requests.get(status_url,headers=headers)
	status_response_json = status_response.json()

	# Step 2: Wait for the report to be finished
	while status_response_json["progress"] < 100:
		status_response = requests.get(status_url,headers=headers)
		status_response_json = status_response.json()
		time.sleep(4)
		print("report progress",status_response_json["progress"])

	file_url = status_response_json["file_url"]
	file_id_pattern = re.compile("files\/(\d+)\/download")

	# Once "progress" is 100 then parse out the number between "files" and "download"

	# Step 3: Download the file
	file_info_url = status_response_json["attachment"]["url"]
	file_response = requests.get(file_info_url,headers=headers,stream=True)


	# Step 4: Save the file
	with open(OUTPUT_FOLDER + status_response_json["attachment"]["filename"],"w+b") as filename:
		filename.write(file_response.content)

	i += 1

# Step 5: Send email to report requester

# Create MIME object
msg = MIMEMultipart()
msg["From"] = from_addr
msg["To"] = ", ".join(map(str, to_list))

# Edit these if necessary to customize subject and body of email
msg["Subject"] = "<ENTER SUBJECT HERE>"
body = "<ENTER EMAIL BODY MESSAGE HERE>"

# Attach body message as plain text, turn entire email into MIME string
msg.attach(MIMEText(body, "plain"))

# Setup email server for secure login
server = smtplib.SMTP(smtpserver)
server.starttls()

# Pass credentials to server, send email, and close connection
server.login(<email_username>,<email_password>)
server.send_message(msg)
server.quit()
