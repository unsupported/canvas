#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os # Used to access environmental variables
from canvas_api import Canvas
import requests # makes web requests
import csv # csv processing
import time # used to create a delay between subsequent checks of report status
from contextlib import closing
from pprint import pprint


######### Start - Edit these values ###########

hostname = '<canvas_hostname>.instructure.com' # Change this

# Put your access token in an environmental variable called ACCESS_TOKEN.
canvas = Canvas(hostname, CANVAS_ACCESS_TOKEN=os.getenv('ACCESS_TOKEN'))

######### End - Edit these values ###########

########################################################################
########################################################################
########################################################################
##################### Make no Changes after this         ###############
##################### unless you know what you are doing.###############
########################################################################
########################################################################
########################################################################
########################################################################







# Step 1: run provisioning report to get all accounts
report_data = {
  'parameters': {
    'accounts': True,
    'created_by_sis':True
  }
}
report_data2 = {
  'parameters': { 'accounts': True }
}

# Start the reports and stores the initial responses in a list
reports_started = [
    canvas.accounts('self').reports.provisioning_csv.post(data=report_data).json(),
    canvas.accounts('self').reports.provisioning_csv.post(data=report_data2).json()
]

# Container to hold completed report responses when they are done
reports_done = []


# wait til the report is done, loop while there are still reports in the
# reports_started list
while reports_started:
  tmp_list = [] # tmp_list to hold reports while checking status
  for x in range(len(reports_started)):
    # Pull a report from the list of started_reports
    r = canvas.accounts('self').reports.provisioning_csv(reports_started.pop()['id']).get().json()
    print('report [{0[id]}] progress {0[progress]}'.format(r)) #r['progress'])
    # If the progress is less than 100, put it into the tmp_list 
    if r['progress'] < 100:
      tmp_list.append(r)
    else:
      # Otherwise, put it in the reports_done list
      reports_done.append(r)

  # Set the reports_started list to tmp_list
  reports_started = tmp_list
  time.sleep(2)

def get_admins_for_account(account):
    for admin in canvas.accounts(account['canvas_account_id']).admins.get_paginated():
        try:
          yield {
              'canvas_user_id': admin['user']['id'],
              'sis_user_id': admin['user'].get('sis_user_id',''),
              'user_name': admin['user']['name'],
              'canvas_account_id': account['canvas_account_id'],
              'sis_account_id': account.get('account_id',''),
              'account_name': account['name'],
              'role': admin['role'],
              'role_id': admin['role_id']
          }
        except:
          return None

with open('./admins_list.csv', 'w+') as _f:
  fieldnames=('canvas_user_id', 'role', 'role_id', 'sis_user_id', 'user_name', 'canvas_account_id', 'sis_account_id', 'account_name')
  output_file = csv.DictWriter(_f, fieldnames=fieldnames, extrasaction='ignore')
  output_file.writeheader()
  
  # Get all admins for the root account
  output_file.writerows(get_admins_for_account({'canvas_account_id':'self', 'name': 'main'}))

  for report_resp in reports_done:
    # This downloads the csv file and registers it as a self-closing stream
    with closing(requests.get(report_resp['attachment']['url'], stream=True)) as r:
      # Step 2: iterate over accounts
      for account in csv.DictReader((rd.decode('utf-8') for rd in r.iter_lines())):
        # Step 3: for each account, make api request to list admins, add each admin to
        # the list of admins
        # Step 4: Output the list of admins

        if account['canvas_account_id'] != 'canvas_account_id':
          # Get all admins for this account
          admin_output = get_admins_for_account(account)
          output_file.writerows(admin_output)


