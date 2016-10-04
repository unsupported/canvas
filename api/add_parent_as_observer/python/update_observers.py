#!/usr/bin/python
# working as of 4/19/2016

'''
For reference column headers must be
parent_id,student_id
'''

myCsvFile = '/full/path/to/observer/csv/file.csv' # Example: 'API_Testing/users_provisioning.csv'
domain = '<yourschool>.instructure.com'
token = '<token_here>' 
action='add' # Change this to delete if you want to delete observees instead
             # of add them


#### Don't edit past this unless you know what you're doing
import csv, requests
header = {'Authorization' : 'Bearer {}'.format(token)}

with open(myCsvFile, 'rb') as csvFile:
  csvReader = csv.DictReader(csvFile)
  if action == 'add':
    rest_action = requests.put
  else:
    rest_action = request.delete
  
  for row in csvReader:
    baseUrl = 'https://{0}/api/v1/users/{1[parent_id]}/observees/{1[student_id]}'.format(domain,row) 
    
    r = rest_action(baseUrl, headers = header)
    # Output progress to the console
    print r.json()

