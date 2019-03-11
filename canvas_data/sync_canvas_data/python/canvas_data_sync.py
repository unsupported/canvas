#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# canvas_data_sync.py
# Author: Brandon Poulliot
# Purpose: Sync Canvas Data to a destination specified by the user
#      * Can provide most recent Canvas Data dump table files
#      * Can provide latest Canvas Data schema in file
#      * Can provide more information on Canvas Data dumps in CSV file
#
# Requirements: only non-standard library is REQUESTS
#
# Script Map:
#       1. Take in arguments and set API endpoint
#       2. Create base-64-encoded HMAC-256 signature
#       3. Download Canvas Data files
#         a. sync - downloads all tables not previously downloaded
#         b. latest - downloads only last 24 hours of tables
#         c. dump - writes a JSON file with extra dump information
#         d. schema - writes a JSON file with exhaustive schema information
#         e. byTable - COMING SOON!
#       4. Unzip (un-GZ?) the Canvas Data files (options 3a and 3b)
#       5. Remove the GZ archive files (options 3a and 3b)
#       6. Remove files not present in most recent sync (option 3a)
#
# Arguments: 
#      1. endpoint - required and positional, must come directly after
#                script invocation
#      2. -l (--limit) - optional, invoke using -l limit=#
#                Only used with dump option, specifies a limit to
#                the number of dump entries returned (default=50)
#      3. -a (--after) - optional, invoke using -a after=#
#                Only used with dump option, specifies the ID of
#                the dump to pull data after (i.e., ID > limit)
#      4. -m (--method) - optional, invoke using
#                -m (GET|DELETE|HEAD|OPTIONS|POST|PUT)
#                Future-proofing this script when more methods
#                become available (default=GET)
#
# Usage: Call from shell/cmd with preferred version and arguments
#    Examples:
#          1. python3 canvas_data_sync.py sync -m GET
#
#             Uses python 3.x + GET method to sync all Canvas Data
#
#          2. python canvas_data_sync.py dump -l limit=100 -a after=345
#
#             Uses default python to write a JSON file with all info on
#               the first 100 data dumps after dump ID 345
#         
# NOTES: + Working as of 3/4/19
#    + Left in "future-proofing" lines, do not uncomment until useful
#    + Flat file extensions don't matter -- change at will
#    + Schema/dump extenstions - keep JSON for syntax marks in text editors

###############################################################################
################# Module Imports -- DO NOT CHANGE THESE! ######################
###############################################################################

# standard modules
import argparse
import base64
import gzip
import hashlib
import hmac
import json
import re
import sys
from datetime import datetime, timezone
from os import listdir, remove
from os.path import getsize, isfile, join
from urllib import parse

# non-standard modules
import requests

###############################################################################
################# User-Declared Variables -- CHANGE THESE! ####################
###############################################################################

# set local timezone abbreviation to differentiate
local_timezone = '<your timezone abbreviation>'

# generate local timestamp (LT) for filenames
dt_lt = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))
# generate UTC timestamp for HMAC-256 signature
dt_now = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

# output dir *MUST* have trailing slash
# Example: /home/canvas/data-dumps/
out_dir = '<C:/your/output/path/>'
# your Canvas Data API key -- do NOT use secret here
api_key = '<Canvas Data API key>'
# now use your Canvas Data API secret!
cdata_secret = '<Canvas Data API secret>'
# filenames -- change as appropriate
schema_fname = '{}-canvas-data-schema.json'.format(dt_lt)
dump_fname = '{}-canvas_data_dumps.json'.format(dt_lt)
# set file extension for flat files -- recommend using default of blank
fext = ''

# set block size for buffer as needed
block_size = 8192

###############################################################################
################# API Call Information Gathering Section ######################
###############################################################################

# init variables for API call parameters
raw_params = []
params = ''

# create argument parser to allow for command line arguments
parser = argparse.ArgumentParser(description='''Separate Canvas Data API call
                 components.''')

# add arguments to parser, first is positional (must be 1st) and required
parser.add_argument('endpoint',
          help='''Specify the endpoint of your API call: dump, sync,
          latest, or schema.''')
parser.add_argument('-l', '--limit', 
          help='''Syntax is "limit=#", specifies how many records to
          return. Only works with dump.''')
parser.add_argument('-a', '--after', 
          help='''Syntax is "after=#", specifies to pull only data
          after dump number provided. Only works with dump.''')
# this one doesn't matter right now, only method available is GET
parser.add_argument('-m', '--method', default='GET',
          help='''Future-proofing for possible new methods for
          Canvas Data API. Currently, only method is GET.''')

# parse args from sys.argv into ParseResult object
args = parser.parse_args()

# check that limit, after, and method all meet syntax requirements
if args.limit is not None:
  limit_syntax = re.search('^limit\=\d+$', args.limit)
  if limit_syntax is not None:
    raw_params.append(args.limit)
  
if args.after is not None:
  after_syntax = re.search('^after\=\d+$', args.after)
  if after_syntax is not None:
    raw_params.append(args.after)

# check that the HTTP method is acceptable  
method_syntax = re.search('^GET$', args.method)
# Below for use only when more methods added to Canvas Data API
#method_syntax = re.search('^(GET|DELETE|HEAD|OPTIONS|POST|PUT)$',
#              args.method)

# if the method is wrong, the call won't work, exit
if method_syntax is None:
# Below for use only when more methods added to Canvas Data API
#  print('''HTTP method is not valid, must be GET, DELETE, HEAD, OPTIONS,
#       POST, or PUT. Exiting...''')
  print('HTTP method is not valid, must be GET. Exiting...')
  sys.exit('invalid method.')

# check the endpoint argument and set the API call URL accordingly
if args.endpoint.lower() == 'dump':
  api_url = 'https://portal.inshosteddata.com/api/account/self/dump{}{}'
elif args.endpoint.lower() == 'sync':
  api_url = 'https://portal.inshosteddata.com/api/account/self/file/sync'
elif args.endpoint.lower() == 'schema':
  api_url = 'https://portal.inshosteddata.com/api/schema/latest'
elif args.endpoint.lower() == 'latest':
  api_url = 'https://portal.inshosteddata.com/api/account/self/file/latest'
# TODO: Add byTable endpoint and args
# elif args.endpoint.lower() == 'bytable':

else:
  print('''Invalid argument, must be "dump", "latest", "sync", or "schema".
      Exiting...''')
  sys.exit('invalid request')
  
# check if params set, sort alphabetically, join them, add to end of API call
if args.endpoint.lower() == 'dump':
  if len(raw_params) > 0:
    raw_params.sort()
    params = '&'.join(raw_params)
    call_url = api_url.format('?', params)
  # remove curly braces -- although this doesn't seem to matter...
  else:
    call_url = api_url.strip('{}')
# if not using dump, don't add parameters
else:
  call_url = api_url
  
###############################################################################
###################### HMAC Signature Building Section ########################
###############################################################################

# break the call into components to build HMAC-256 signature
call_info = list(parse.urlparse(call_url))

# set components for HMAC-256 signature
reqOpts = {
  'method' : args.method.upper(),
  'host' : call_info[1],
  # intentionally blank
  'content_type' : '',
  # intentionally blank
  'content_md5' : '',
  'path' : call_info[2],
  'parameters' : params,
  'req_timestamp' : dt_now,
  'api_secret' : cdata_secret
  }

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
############### DO NOT CHANGE ANYTHING IN THIS SUBSECTION #####################
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

# build a bytes message by joining the signature components
message = bytes('\n'.join(str(x) for x in reqOpts.values()), 'utf-8')
# change the Canvas Data API secret to bytes
api_secb = bytes(reqOpts['api_secret'], 'utf-8')

# create an SHA-256 hashed HMAC object, then base 64 encode it
signed_msg = base64.b64encode(hmac.new(api_secb, message,
                     digestmod=hashlib.sha256).digest())
# must be 'decoded'to utf-8 to get rid of byte marks (^,.,^)
signature = signed_msg.decode('utf-8')

# build auth headers from Canvas Data API key, HMAC-256 sig, and timestamp
auth_headers = { 'Authorization' : 'HMACAuth {}:{}'.format(api_key, signature),
         'Date' : '{}'.format(dt_now) }

###############################################################################
############################# API Call Generation #############################
###############################################################################

# start the API call
print('Starting Canvas Data {} request...\nTimestamp: {}\n'.format(args.endpoint.lower(), dt_lt))
start_call = requests.get(call_url, headers=auth_headers)
call_response = start_call.json()

# initialize loop variables
fname = ''
file_path = ''
flat_file = ''
dl_url = ''
sync_files = []

###############################################################################
########################## CData SYNC Section #################################
###############################################################################

# main purpose of script -- syncs Canvas Data API files to output dir
if args.endpoint.lower() == 'sync':
  # get filename and download path for each table
  table_manifest = call_response['files']
  for table in table_manifest:
    fname = table['filename']
    file_path = join(out_dir, fname)
    flat_fname = fname.split('.')[0]
    print(fname)
    # add extension if desired, makes no difference but you do you
    flat_file = file_path.split('.')[0] + fext
    dl_url = table['url']
    dl_file = requests.get(dl_url)
    # is the file a full table or part of a table?
    print('Partial table? {}'.format(table['partial']))
    if isfile(file_path):
      remove(file_path)
      print('Local file fragment removed: {}'.format(file_path))
    # delete any zero-length mishap files
    if isfile(flat_file) and getsize(flat_file) == 0:
      remove(flat_file)
    # check if the flat file exists, if not, download it
    # note that this will skip incomplete files more than 0 KB
    if isfile(flat_file) and getsize(flat_file) > 0:
      print('Skipping file: {} -- already exists.\n'.format(flat_fname))
      sync_files.append(flat_fname)
      continue
    # if the thousand other scenarios aren't true, let's write the file!
    else:
      with open(file_path, 'wb') as sync:
        sync.write(dl_file.content)
        sync.close()
      print('Downloaded file: {}'.format(fname))
      # open gz file and dump contents into flat file block by block
      with gzip.open(file_path, 'rb') as zipped, \
      open(flat_file, 'wb') as unzipped:
        while True:
          block = zipped.read(block_size)
          if not block:
            break
          else:
            unzipped.write(block)
        unzipped.write(block)
        # must explicitly close both files before further manipulation
        unzipped.close()
        zipped.close()
      print('Unzipped file: {}\n'.format(flat_file))
      # after all is said and done, remove the GZ file
      remove(file_path)
      # add the downloaded file to a sync list
      sync_files.append(flat_fname)
  # catalog existing files -- to remove unnecessary files later (for sync)
  x_files = listdir(out_dir)
  # create a deletion manifest via list comprehension
  del_manifest = [f for f in x_files + sync_files if f not in sync_files]
  del_paths = []
  # add the output path to file names in deletion manifest
  for file in del_manifest:
    del_paths.append(join(out_dir, file))
  # remove each file in the deletion manifest to complete the sync
  for file in del_manifest:
    fpath = join(out_dir, file)
    if isfile(fpath):
      remove(fpath)
      print('Removed file: {}'.format(fpath))
  dt_complete = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))
  print('Canvas Data synchronized.\nCompleted: {}'.format(dt_complete))

###############################################################################
########################## CData LATEST Section ###############################
###############################################################################

# download latest dump (i.e., tables from last 24 hrs), not needed w/ sync
elif args.endpoint.lower() == 'latest':
  table_list = call_response['artifactsByTable']
  for table in table_list:
    fname = table_list[table]['files'][0]['filename']
    flat_fname = fname.split('.')[0]
    file_path = join(out_dir, fname)
    flat_file = file_path.split('.')[0]
    dl_url = table_list[table]['files'][0]['url']
    dl_file = requests.get(dl_url)
    if isfile(file_path):
      remove(file_path)
      print('File fragment removed: {}'.format(file_path))
    if isfile(flat_file) and getsize(flat_file) == 0:
      remove(flat_file)
    if isfile(flat_file) and getsize(flat_file) > 0:
      print('Skipping file: {} -- already exists.\n'.format(flat_fname))
      continue
    else:
      with open(file_path, 'wb') as latest:
        latest.write(dl_file.content)
        latest.close()
      print('Downloaded file: {}'.format(fname))
      with gzip.open(file_path, 'rb') as zipped, \
      open(flat_file, 'wb') as unzipped:
        while True:
          block = zipped.read(block_size)
          if not block:
            break
          else:
            unzipped.write(block)
        unzipped.write(block)
        unzipped.close()
        zipped.close()
      print('Unzipped file: {}\n'.format(flat_file))
      remove(file_path)
  dt_complete = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))
  print('Canvas Data latest dump downloaded.\nCompleted: {}'.format(dt_complete))

###############################################################################
########################## CData INFO Section #################################
###############################################################################

# if you need more information on daily dumps, writes a JSON file with info       
elif args.endpoint.lower() == 'dump':
  fname = dump_fname
  file_path = join(out_dir, fname)
  with open(file_path,'w') as dump_file:
    call_json = json.dump(call_response, dump_file, indent=4)
  dt_complete = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))
  print('''Dump info file written, check output directory.
      \nCompleted: {}'''.format(dt_complete))
  
# writes schema to a file, not terribly useful unless schema changes
elif args.endpoint.lower() == 'schema':
  fname = schema_fname
  file_path = join(out_dir, fname)
  with open(file_path, 'w') as schema_file:
    call_json = json.dump(call_response, schema_file, indent=4)
  dt_complete = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))
  print('Schema file written, check output directory.\n Completed: {}'.format(dt_complete))
