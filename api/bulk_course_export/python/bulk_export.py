#!/usr/bin/env python
"""
Given a csv file with a list of courses to export, this script will launch course
exports for each course.  Once they are completed, a CSV file is written with the
course_id and export_url for each export.  The export course content is not downloaded.

"""
import requests
import csv
import sys
import os
import os.path
import time
import pprint

# Change this to contain your access token
canvas_domain = "changeme.instructure.com" # i.e. something like schoolname.instructure.com
canvas_token = 'canvas_access_token'

# Set this to the full path of the file that contains the list of ocurses to migrate.
# This file should have at least one column called course_id.  This column should
# contain the canvas course id's or sis id's (prefixed with sis_course_id:)
course_input_file = '/Users/kevin/dev/canvas-contrib/API_Examples/bulk_course_export/python/courses.in.csv'

# Set this to the full path of the output CSV file that will be created after doing
# the bulk exports for the list of courses
course_output_file = '/Users/kevin/dev/canvas-contrib/API_Examples/bulk_course_export/python/courses.out.csv'

course_id_field = 'course_id'

############################################################################################################
############################################################################################################
# Don't edit after this point unless you intend to make changes to the script logic.
############################################################################################################
############################################################################################################


# If you want pretty progress bars, install the clint python module
try:
  from clint.textui.progress import Bar
except:
  class Bar(object):
    def __init__(self,*args,**kwargs):
      self.label = kwargs.get('label','')
    def show(self,idx):
      print "{0.label} {1}% done".format(self,idx)

    @property
    def label(self):
      return self._label

    @label.setter
    def label(self, value):
      print value
      self._label = value

try:
  from local_config import *
except:
  print 'local config file not found'
  pass

config =dict (
    headers = {'Authorization':'Bearer {0}'.format(canvas_token)},
    domain = canvas_domain,
    course_input_file=course_input_file,
    course_output_file=course_output_file)

def course_export(course):
  # Do Course exports for the course
  url = "https://{1[domain]}/api/v1/courses/{0}/content_exports".format(course[course_id_field],config)
  params = {
      'export_type':'common_cartridge',
      'skip_notifications':1
      }
  try:
    res = requests.post(url,data=params,headers=config['headers']).json()
  except Exception, err:
    res = False
  return (course,res)

def course_exports(course_list):
  '''Do course exports for each course in the list'''
  #pprint.pprint(course_list)
  bar = Bar(label='Exporting Courses ',expected_size=len(course_list))
  export_list = []
  for idx,course in enumerate(course_list):
    export_list.append(course_export(course))
    bar.show(idx)

  blen = len(export_list)
  bar.label = "Checking Export Statuses: "
  bar.expected_length = blen
  bar.show(1)
  while export_list:
    if len(export_list) < 10:
      time.sleep(2)
    bar.show(blen-len(export_list))
    #print export_list
    for idx,cm in enumerate(export_list):
      course,res = cm
      url = res.get('progress_url',None)
      if not url:
        del(export_list[idx])

        print 'not able to generate export for course',course
      else:
        download_progress = requests.get(url,headers=config['headers']).json()

        bar.label = "Checking Export Status: {} {}% ".format(course[course_id_field],download_progress['completion'])
        if download_progress['workflow_state'] not in ['queued','running']:
          if download_progress['workflow_state'] == 'completed':
            url = "https://{domain}/api/v1/courses/{}/content_exports/{}".format(course[course_id_field],res['id'],**config)
            export_info = requests.get(url,headers=config['headers']).json()
            #print 'export_info',export_info
            export_url = export_info['attachment']['url']
            course['export_url'] = export_url
            yield course
          else:
            course['export_url'] = None
          del(export_list[idx])
      #return course
  #return course_list

add_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),os.path.pardir))
sys.path.append(add_path)

#print sys.path
from bulk_migration.python import course_migrations

course_migrations.debug = False

def local_prep_row(row):
  source_id,destination_id = course_migrations.prep_row(row)
  destination_id = "sis_course_id:{}".format(destination_id)
  return source_id,destination_id

if __name__ == '__main__':
  course_output_fields = ('course_id','export_url')
  with open(course_input_file,'rU') as uf, open(course_output_file,'w+') as cw:
    cw = csv.DictWriter(cw,fieldnames=course_output_fields,extrasaction='ignore')
    cw.writeheader()

    #queue = (local_prep_row(x) for x in course_exports(list(csv.DictReader(uf))))
    #course_migrations.runMigrations(queue)
    for row in course_exports(list(csv.DictReader(uf))):
      cw.writerow(row)
    #  do_import(row)

  print 'all done'
