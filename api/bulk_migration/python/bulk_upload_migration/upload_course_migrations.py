#!/usr/bin/env python

import json,csv,os
import collections
import time,logging
import requests
from multiprocessing import Pool
from logging.handlers import RotatingFileHandler
import itertools, sys
import zipfile
from pprint import pprint

"""
 You will need to edit several variables here at the top of this script.
 token = the access token from Canvas
 workingPath = the full working path to where the csv files are created.
    This is where the logs and archive folders will be created
 CSVFileName = the name of course copy CSV file as it will be created in
    the workingPath.
 domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
"""

token = "<access_token>" # access_token
workingPath = "/path/to/working/folder/"; # Important! Make sure this ends with a backslash
CSVFileName = "csvfile.csv" # The name of the course copy CSV file.  Not the full path

source_archive_filename_column = "source"
canvas_domain = "yourdomain.test.instructure.com"  # Your Canvas domain.  Use the .test area at first

destination_course_id_column = "destination_id"
num_processes = 4 # Change this to be the number of concurrent course copies to run, with a max of 4
wait_till_done = False # Set this to false if you don't want the script to wait for each
                       # course copy to finish before doing another.

migration_type = "common_cartridge_importer" # Change this to fit your migration type
migration_url_field = 'export_url'
migration_base_url = None # This only needs to be set if linking to files to download from
                          # the web somewhere
process_type = 'upload' # options are 'upload' or 'link'

""" Recent options for migration_type include:
"type": "angel_exporter",
"name": "Angel export .zip format",

"type": "blackboard_exporter",
"name": "Blackboard 6/7/8/9 export .zip file",

"type": "webct_scraper",
"name": "Blackboard Vista/CE, WebCT 6+ Course",

"type": "canvas_cartridge_importer",
"name": "Canvas Course Export Package",

"type": "common_cartridge_importer",
"name": "Common Cartridge 1.0/1.1/1.2 Package",

"type": "d2l_exporter",
"name": "D2L export .zip format",

"type": "moodle_converter",
"name": "Moodle 1.9 .zip file",
]
"""

#######################################################################################
#######################################################################################
################ Don't edit anything past here unless you know what you are doing.
################ NOTE: No offense, you probably do know what you're doing.  This is for
################ those that do not.

# I think I should be able to read the field names from the first line
# of the file.  That is assuming the file has headers.  It should always have them.
#

spinner = itertools.cycle(['-', '/', '|', '\\'])

try:
  # NOTE - if you install the clint pypi library you will get a nice progress
  # bar during script execution.
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

# Try loading local config variables from a file called local_config.py.  This file will
# not be in the folder by default.  Rather, it will a file created by the developer.  This
# would really be a special case.
try:
  from local_config import *
except:
  print "local config file not found. That's okay, it just means you will have modified the variables at the top of this file."


headers = {"Authorization":"Bearer %s" % token}

from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler
import urllib2

def uploadFile(data,filename):

  data['upload_params']['file'] = open(filename, "rb")

  #_data = data.items()
  #_data[1] = ('upload_params',_data[1][1].items())

  handlers = [StreamingHTTPHandler, StreamingHTTPSHandler]
  opener = urllib2.build_opener(*handlers)
  urllib2.install_opener(opener)

  datagen, headers = multipart_encode(data['upload_params'])

  #print 'pp: data[file]',data['file']
  request = urllib2.Request(data['upload_url'], datagen,headers)
  result = urllib2.urlopen(request)

  response = json.load(result)
  response.update( dict(
    status=result.getcode(),
    headers=result.info()))
  return response


def massDoCopies(data):
  # data[1] is the row of data, in the form of a list

  row_data = data[1]

  # data[0] is the progress bar object  
  prog_bar = data[0]
  prog_bar.label = 'doing copy: {}'.format(row_data)

  logger_prefix = '{0[destination_id]}:{0[source_id]}'.format(row_data)
  file_path = os.path.join(workingPath,row_data['source_id'])
  rootLogger.debug(row_data)
  course_search_url = "https://{}/api/v1/courses/{}".format(canvas_domain,row_data['destination_id'])
  rootLogger.info('{} looking for course: {}'.format(logger_prefix,course_search_url))

  done_finding = False
  found_course = {}
  while not done_finding:
    try:
      found_course = requests.get(course_search_url,headers=headers).json()
      done_finding = True
    except:
      pass
  if not found_course.get('id',None):
    rootLogger.error('{} course {} {}'.format(logger_prefix,row_data['destination_id'], 'not found'))
  else:
    rootLogger.info('{} course found {}'.format(logger_prefix,found_course))
    prog_bar.label = 'course found {}'.format(row_data['destination_id'])

    params = {
      'migration_type':migration_type
    }
    if process_type == 'upload':
      # Course quota size checking
      z = zipfile.ZipFile(open(file_path,'rb'))
      uncompress_size_mb = sum((file.file_size for file in z.infolist()))/1000000.0
      # Get course quota via api
      # Get the course used quota
      #/api/v1/courses/:course_id/files/quota
      course_quota_url = "https://{}/api/v1/courses/{}/files/quota".format(canvas_domain,row_data['destination_id'])
      course_quota_info = requests.get(course_quota_url,headers=headers).json()
      # if it isn't large enough for the unzipped
      # files then increase it to current usage + uncompress_size + 50%
      if not ((course_quota_info['quota'] - course_quota_info['quota_used'])/1000000.0) > uncompress_size_mb:
        # Increase the space needed
        update_course_data = {'course[storage_quota_mb]':course_quota_info['quota']+uncompress_size_mb}
        course_quota_info = requests.put(course_search_url,data=update_course_data,headers=headers).json()

      # TODO Pre-upload content package checking according to the type.
      # TODO Get list of common errors from Tdoxey
      params['pre_attachment']={
        'name': row_data['source_id'],
        'name':row_data['source_id'],
        'size':os.path.getsize(file_path), # read the filesize
        'content_type':'application/zip',
       }
    elif process_type == 'copy':
      # set the source course field
      params['settings'] = {'source_course_id':row_data['source_id']}
    elif process_type == 'link':
      # set the url field
      params['settings'] = {'file_url':row_data['source_id']}

    rootLogger.info('{} {}'.format(logger_prefix,params))


    headers_post = {'Authorization':headers['Authorization'],'Content-type':'application/json'}
    uri = "https://{}/api/v1/courses/{}/content_migrations".format(canvas_domain,row_data['destination_id'])
    rootLogger.info('{} uri: {}'.format(logger_prefix,uri))

    migration = requests.post(uri,headers=headers_post,data=json.dumps(params))
    migration_json = migration.json()

    rootLogger.debug(migration.json())
    if process_type=='upload':
      prog_bar.label = 'done triggering course copy, now uploading'
      rootLogger.info("{} Done prepping Canvas for upload, now sending the data...".format(logger_prefix))
      json_res = json.loads(migration.text,object_pairs_hook=collections.OrderedDict)


      # Step 2:  Upload data
      files = {'file':open(file_path,'rb').read()}
      
      _data = json_res['pre_attachment'].items()
      if _data[1][0]=='error':
          rootLogger.info("{} {} - There was a problem uploading the file.  Probably a course quota problem.".format( row_data['destination_id'], row_data['source_id']))
          row_data['errors'] = _data[1][0]
          return row_data

      _data[1] = ('upload_params',_data[1][1].items())

      rootLogger.info("{} Yes! Done sending pre-emptive 'here comes data' data, now uploading the file...".format(logger_prefix))
      upload_file_response = uploadFile(json_res['pre_attachment'],file_path)

      # Step 3: Confirm upload

      rootLogger.info("{} Done uploading the file, now confirming the upload...".format(logger_prefix))
      rootLogger.info("{} upload completed...nicely done! The Course migration should be starting soon.".format(logger_prefix))
      migration_json = requests.get('https://{}/api/v1/courses/{}/content_migrations/{}'.format(canvas_domain,row_data['destination_id'],migration_json['id']),headers=headers).json()

      
    output = "\r\n" + migration.text
    rootLogger.debug(output)

    prog_url = migration_json['progress_url']
    if wait_till_done:
      status = requests.get(prog_url,headers=headers).json()
      last_progress = status['completion']
      while status['workflow_state'] in ('pre-processing','queued','running'):
        done_statusing = False
        while not done_statusing:
          try:
            status = requests.get(prog_url,headers=headers).json()
            done_statusing = True
          except Exception, err:
            rootLogger.error('{} {}'.format(logger_prefix,err))

        if status['completion']!=last_progress:
          rootLogger.debug("{} {}".format(status['workflow_state'],status['completion']))
          last_progress = status['completion']
      if status['workflow_state']=='failed':
          rootLogger.info("{} - {} - {} {}".format(canvas_domain,row_data['destination_id'],status['workflow_state'],status['completion']))
          rootLogger.info("{} - {} - migration issues: {}".format(canvas_domain,row_data['destination_id'],migration_json['migration_issues_url']))
          rootLogger.debug(requests.get(migration_json['migration_issues_url'],headers=headers).text)
      else:
          rootLogger.info("{} - {} - {} {}".format(canvas_domain,row_data['destination_id'],status['workflow_state'],status['completion']))
    #copyCache['sources'][source_id].append(csvrow[destination_course_id_column])
    rootLogger.info(last_progress)
    rootLogger.info('all done')
  return row_data

def runMigrations(copies):
    pool = Pool(processes=num_processes)
    #copies.reverse()

    bar = Bar()
    #res = pool.map(massDoCopies,((bar,x) for x in copies))
    #for x in copies:
    #  massDoCopies((bar,x))

    print 'h2'
    print 'copies',copies
    res = pool.map_async(massDoCopies, ((bar,x) for x in copies))
    stats = []
    try:
        stats.append(res.get(0xFFFF))
    except KeyboardInterrupt:
        print 'kill processes'
        #pool.terminate()
        exit()
    except TypeError, err:
        print 'err',err
        pass


def UnicodeDictReader(utf8_data, **kwargs):
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
    yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

def prep_row(row):
  print 'process_type',process_type
  if process_type == 'link' and migration_base_url:
    source_id = migration_base_url + row.get(source_archive_filename_column,None)
  else:
    source_id = row.get(source_archive_filename_column,"no source course given or column not found")
  destination_id = row.get(destination_course_id_column,None)
  return source_id,destination_id


if __name__ == '__main__':

  course_copy_queue = []
  CSVFilePath = os.path.join(workingPath, CSVFileName)
  logPath = os.path.join(workingPath, "logs")

  timestamp = time.strftime("%y_%m_%d_%h")
  # Create several paths that are needed for the script to run.
  # These paths may exist already, but this is a check
  if not os.path.exists(logPath):
      os.mkdir(logPath)

  logFilePath = os.path.join(logPath,timestamp + ".log")

  t = time.strftime("%Y%m%d_%H:%M:%S")

  # TODO There is probably a better place to put this stuff that right here
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                      datefmt='%m-%d %H:%M')
  rootLogger = logging.getLogger('upload_course_migrations')
  rootLogger.addHandler(logging.FileHandler(logFilePath))

  logging.getLogger("requests").setLevel(logging.WARNING)
  # Rotate the log files
  #handler = RotatingFileHandler(logFilePath, maxBytes=1000000, backupCount=5)
  rootLogger.info("Log File: {}".format( logFilePath))

  if CSVFileName[-1] == '/':
      rootLogger.info("The CSVFilename should not end in a forward slash.  You are warned")

  if not os.path.exists(CSVFilePath):
    print 'hh'
    rootLogger.info('CSVFilePath: {}'.format(CSVFilePath))
    rootLogger.info("`r`n " + t +":: There was no CSV file.  I won't do anything")
  else:
    times = 1
    dr = UnicodeDictReader(open(CSVFilePath,'rU'))
    for csvrow in dr:
      times+=1
      source_id,destination_id = prep_row(csvrow)

      if source_id and destination_id:
        course_copy_queue.append(dict(source_id=source_id,destination_id=destination_id))

    runMigrations(course_copy_queue)

  for h in rootLogger.handlers[:]:
      h.close()
      rootLogger.removeHandler(h)
