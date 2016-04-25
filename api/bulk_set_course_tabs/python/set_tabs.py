#!/usr/bin/env python
# working as of 1/19/2016

import json,csv,os
import time
import requests
import multiprocessing

"""
 You will need to edit several variables here at the top of this script. 
 token = the access token from Canvas
 workingPath = the full working path to where the csv files are created.  
    This is where the logs and archive folders will be created
 CSVFileName = the name of CSV file as it will be created in
    the workingPath.
 domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
"""

token = "<access_token>" # access_token
workingPath = "/path/to/working/folder/"; # Important! Make sure this ends with a backslash
CSVFileName = "csvfile.csv" # The name of the course copy CSV file.  Not the full path
domain = "<schoolname_test>.instructure.com"
source_course_id_column = "course_id"
num_processes = 4 # Change this to be the number of concurrent course tab changes to run at once.  
# Set the tab order here. Each item is composed of two pieces.  The first is the tab_id of
# the navigation element.  The second is whether the tab is hidden.
# Note: the home and settings tabs are fixed at the start and end of the list respectively
# and cannot be moved.
course_tab_order = ( 
    ('announcements',False),
    ('collaborations',True),
    ('files',False),
    ('grades',True),
    ('discussions',True),
    ('syllabus',False),
    ('quizzes',False),
    ('modules',False),
    ('people',False),
    ('conferences',True),
    ('outcomes',False),
    ('pages',True),
    ('assignments',False),
)

##############################################################################
##############################################################################
################ Don't edit anything past here unless you know what you are doing.
################ NOTE: No offense, you probably do know what you're doing.  This is for
################ those that do not.  

# I think I should be able to read the field names from the first line
# of the file.  That is assuming the file has headers.  It should always have them.
# fieldnames that will exist in the csv file
#fieldnames = (destination_course_id_column,source_course_id_column)


debug=False
# Try loading local config variables from a file called local_config.py.  This file will
# not be in the folder by default.  Rather, it will a file created by the developer.  This
# would really be a special case.
try:
  from local_config import *
except:
  print 'local config file not found'
  pass

if "/" in CSVFileName:
    print "The CSVFilename should not contain forwardslashed.  You are warned"

tabchanges_queue = []
headers = {"Authorization":"Bearer %s" % token}

def massDoTabUpdates(data):


  course_id = data.get(source_course_id_column,None)

  for position,item in enumerate(course_tab_order):
    #print dict(course_id=course_id,position=position,item=item)
    params = {'position': position+2,'hidden': item[1]}
    uri = "https://{0}/api/v1/courses/{1}/tabs/{2}".format(domain,course_id, item[0])
    done_putting = False
    while not done_putting:
      try:
        result = requests.put(uri,headers=headers,params=params)
        done_putting = True
      except:
        pass

    #print $result
    output = "\r\n" + result.text
    #print 'done tab change of {0}(position:{3},hidden:{2}) for course {1}'.format(item[0],course_id,item[1],position)
    #print output
    logfile.write(output)
  return True,'done tab change of for course {0}'.format(course_id)

CSVFilePath = os.path.join(workingPath, CSVFileName)
logPath = os.path.join(workingPath, "logs")

timestamp = time.strftime("%y_%m_%d_%h")
logFilePath = os.path.join(logPath,timestamp + ".log")
# Create several paths that are needed for the script to run.
# These paths may exist already, but this is a check
if not os.path.exists(logPath):
    os.mkdir(logPath)
 
print "Log File: ", logFilePath
t = time.strftime("%Y%m%d_%H:%M:%S")

def UnicodeDictReader(utf8_data, **kwargs):
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
    #print row
    yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

logfile = open(logFilePath,'ab+')
if not os.path.exists(CSVFilePath):
  print CSVFilePath
  print "There was no csv file.  I won't do anything"
  output = "\r\n " + t +":: There was no CSV file.  I won't do anything"
  logfile.write(output)
else:
  pool = multiprocessing.Pool(processes=num_processes)
  res = pool.map(massDoTabUpdates,UnicodeDictReader(open(CSVFilePath,'rb')))
  print res
