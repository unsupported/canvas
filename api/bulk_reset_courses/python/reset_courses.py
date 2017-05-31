#!/usr/bin/env python
# working as of 1/19/2016

import json,csv,os
import requests

"""
 You will need to edit several variables here at the top of this script. 
 token = the access token from Canvas
 CSVFileName = the full path of CSV file 
 domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
"""

headers = {
    'Authorization': 'Bearer <token_here>'
} 

CSVFileName = "csvfile.csv" # The name of the course copy CSV file.  Not the full path
domain = "<schoolname_test>.instructure.com"

#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.
################ NOTE: No offense, you probably do know what you're doing.  This is for
################ those that do not.  

if __name__ == '__main__':
  with open(CSVFileName, 'r') as _f:
    course_csv = csv.DictReader(_f)
    for course in course_csv:
      course_id = course['course_id']
      uri = "https://{0}/api/v1/courses/{1}/reset_content".format(domain, course_id)
      result = requests.post(uri, headers=headers, data=data)
    print(result.json())
