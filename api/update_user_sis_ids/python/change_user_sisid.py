#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json
import multiprocessing
import csv

""" Example change_users.csv file

old_user_id,new_user_id
201.bobby,2013.bobby

"""

filename = '/Users/path/to/change_users.csv' # Change this to the file with the two columns
domain = '<domain>.instructure.com' # Change this
token = '' # Change this

headers = {'Authorization':'Bearer %s' % token}


def proc_user(user):
  # Get the logins for the user, find the one with the old SIS id, and change it
  url = 'https://%s/api/v1/users/sis_user_id:%s/logins' % (domain,user['old_user_id'])

  logins = requests.get(url,headers=headers).json()
  #logins = login_response.json()
  #print logins
  print 'attempting to change {} to {}'.format(user['old_user_id'], user['new_user_id'])

  if not logins or type(logins) == dict:
    print "{} not found, keep going".format(user['old_user_id'])
  else:
    for l in logins:
      try:
        if l['sis_user_id'] == user['old_user_id']:
          params = {'login[sis_user_id]':user['new_user_id']}
          url = 'https://%s/api/v1/accounts/self/logins/%s' % (domain,l['id'])
          updated_login_response = requests.put(url,headers=headers,params=params)
          #print updated_login_response.json()
          #print 'user updated '
          print 'changed {} to {}'.format(user['old_user_id'], user['new_user_id'])
      except Exception, exc:
        print logins,exc
        print "The login probably wasn't found.  Keep going..."

def proc_user_list(user_list):
  p = multiprocessing.Pool(4)
  p.map(proc_user, user_list)

 
# Read CSV file
if __name__ == '__main__':

  user_list = csv.DictReader(open(filename,'rU'))
  proc_user_list(user_list)

