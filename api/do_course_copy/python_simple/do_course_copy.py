#!/usr/bin/env python
import sys,csv,json
import requests

cache_filename = './course_copy_cache.json'
template_filename = './course_copy_template.csv'
source_column_name = 'source_course_id'
destination_column_name = 'destination_course_id'

user = {
    'domain':'cwt.test.instructure.com', # Change this
    'account_id':'', # Change this
    'access_token':'' # Change this
  }


#### 
## Stop Editing after this
####
try:
  course_list_done = json.load(open(cache_filename,'r+'))
except ValueError, err:
  course_list_done = []
course_list = csv.DictReader(open(template_filename,'U'))

# CHANGE THIS
if __name__ ==  '__main__':
  auth_headers = {"Authorization":"Bearer %s" % user['access_token']}
  
  for _copy in course_list:
    key = '::'.join(_copy.values())
    if key in course_list_done:
      # Ignore the copy if it has already been done before
      print key,'already done'
    else:
      #destination,source = course
      params = {"source_course":_copy[source_column_name]}
      copy_url = 'https://%s/api/v1/courses/%s/course_copy' % (user['domain'],_copy[destination_column_name])
      res = requests.post(copy_url,headers=auth_headers,params=params)
      if res.status_code==200:
        course_list_done.append(key)

with open(cache_filename,'r+') as outfile:
  json.dump(course_list_done, outfile)
  #json.dump(course_list_done,open(cache_filename,'w+'))
