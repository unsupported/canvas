#!/usr/bin/env python

import requests, json
import csv

""" Example change_users.csv file

old_user_id,new_user_id
201.bobby,2013.bobby

"""

filename = '/path/to/file/users_to_change.csv' # Change this to the file with the two columns
domain = 'yourcollege.instructure.com' # Change this
token = 'tokenhere' # Change this


 
# Read CSV file

headers = {'Authorization':'Bearer %s' % token}
user_list = csv.DictReader(open(filename,'rU'))
for user in user_list:
  # Get the logins for the user, find the one with the old SIS id, and change it
  url = 'https://%s/api/v1/users/sis_user_id:%s/logins' % (domain,user['old_user_id'])

  logins = requests.get(url,headers=headers).json()
  #logins = login_response.json()
  #print logins
  if not logins:
    print 'logins',logins
    print "the user probably wasn't found, keep going"

  else:
    for l in logins:
      try:
        if l['sis_user_id'] == user['old_user_id']:
          params = {'login[sis_user_id]':user['new_user_id']}
          url = 'https://%s/api/v1/accounts/self/logins/%s' % (domain,l['id'])
          updated_login_response = requests.put(url,headers=headers,params=params)
          print updated_login_response.json()
      except Exception, exc:
        print logins,exc
        print "The user probably wasn't found.  Keep going..."


