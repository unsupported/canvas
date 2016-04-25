#!/usr/bin/python
# working as of 4/19/2016

'''
For reference column headers must be
parent_id,student_id
'''

myCsvFile = '/full/path/to/observer/csv/file.csv' # Example: 'API_Testing/users_provisioning.csv'
domain = '<yourschool>.instructure.com'
token = '<token_here>' 


#### Don't edit past this unless you know what you're doing
import csv, requests
header = {'Authorization' : 'Bearer {}'.format(token)}

with open(myCsvFile, 'rb') as csvFile:
  csvReader = csv.DictReader(csvFile)
  
  for row in csvReader:
    baseUrl = 'https://{0}/api/v1/users/{1[parent_id]}/observees/{1[student_id]}'.format(domain,row) 
    r = requests.put(baseUrl, headers = header)
    # Output progress to the console
    print r.json()

