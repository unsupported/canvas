#!/usr/bin/env python
# Working as of 2021-28-01

import json,csv,os
import requests

"""
 You will need to edit several variables here at the top of this script. 
 token = the access token from Canvas
 CSVFileName = the full path of CSV file 
 domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
"""

headers = {
    'Authorization': 'Bearer <your token here>'
} 

CSVFileName = "courseList.csv" # The name of the course copy CSV file.  Not the full path
domain = "<institution-domain>.instructure.com"

#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.

if __name__ == '__main__':
  with open(CSVFileName, 'r') as _f:
    course_csv = csv.DictReader(_f)
    for course in course_csv:
      canvas_id = course['canvas_id']
      sis_id = course['sis_id']
      uri = "https://{0}/api/v1/courses/{1}?course[sis_course_id]={2}".format(domain, canvas_id, sis_id)
      result = requests.put(uri, headers=headers)
      print(result.json())
