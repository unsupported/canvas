#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# canvas_data_sync.py
# Author: Brandon Poulliot
# Purpose: Sync Canvas Data to a destination specified by the user
#      * Can provide most recent Canvas Data dump table files
#      * Can provide latest Canvas Data schema in file
#      * Can provide more information on Canvas Data dumps in CSV file
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
# Arguments: 1. endpoint - required and positional, must come directly after
#              script invocation
#      2. -l (--limit) - optional, invoke using -l limit=#
#                Only used with dump option, specifies a limit to
#                the number of dump entries returned (default=50)
#      3. -a (--after) - optional, invoke using -a after=#
#                Only used with dump option, specifies the ID of
#                the dump to pull data after (i.e., ID > limit)
#      4. -m (--method) - optional, invoke using
#                 -m (GET|DELETE|HEAD|OPTIONS|POST|PUT)
#                 Future-proofing this script when more methods
#                 become available (default=GET)
#
# Usage: Call from shell/cmd with preferred version and arguments
#    Examples: 1. python3 canvas_data_sync.py sync -m GET
#
#           Uses python 3.x + GET method to sync all Canvas Data
#
#          2. python canvas_data_sync.py dump -l limit=100 -a after=345
#
#           Uses default python to write a JSON file with all info on
#           the first 100 data dumps after dump ID 345
#
# NOTES: + Working as of 9/20/19
#    + Left in "future-proofing" lines, do not uncomment until useful
#    + Flat file extensions don't matter -- change at will
#    + Schema/dump extenstions - keep JSON for syntax marks in text editors

###############################################################################
################# Module Imports -- DO NOT CHANGE THESE! ######################
###############################################################################

# standard modules
import gzip
import json
import re
import sys
from datetime import datetime, timezone
from os import listdir, remove
from os.path import getsize, isfile, join

# non-standard modules
import requests
from canvasfuncs import hmacsig, candata

###############################################################################
################# User-Declared Variables -- CHANGE THESE! ####################
###############################################################################

# set local timezone abbreviation to differentiate
local_timezone = '<TZ>'
params = ''

# generate local timestamp (LT) for filenames
dt_lt = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))

# output dir *MUST* have trailing slash followed by curly braces
# Example: /home/canvas/data-dumps/{}
out_dir = '</path/to/data/goes/here/{}>'
schema_out = join(out_dir,'schema/')
# your Canvas Data API key -- do NOT use secret here
api_key = '<Canvas Data API Key>'
# now use your Canvas Data API secret!
cdata_secret = '<Canvas Data API Secret>'
# filenames -- change as appropriate
schema_fname = 'canvasdata-schema-{}.json'
dump_fname = '{}-canvasdata-dumps.json'.format(dt_lt)

# schema notification settings
body = join(schema_out, 'schema_notify')
subj = 'Canvas Data Schema Changes {}'.format(dt_lt)
msg = '''New schema version {} for Canvas Data. \n\
      Please consult https://portal.inshosteddata.com/docs/api'''
whonotify = '<optional notification email address>'


# set block size for buffer as needed
block_size = 8192

###############################################################################
################# API Call Information Gathering Section ######################
###############################################################################

# parse arguments
args = candata.parse(sys.argv)

# check that method is correct syntax
method_syntax = re.search('^GET$', args.method)

# For use only when more methods added to Canvas Data API
#method_syntax = re.search('^(GET|DELETE|HEAD|OPTIONS|POST|PUT)$',
#              args.method)

# if the method is wrong, the call won't work, exit
if method_syntax is None:
  print('HTTP method is not valid, must be GET. Exiting...')
  sys.exit('invalid method.')

#  print('''HTTP method is not valid, must be GET, DELETE, HEAD, OPTIONS,
#       POST, or PUT. Exiting...''')

cdata_uri = 'https://portal.inshosteddata.com/api/{}'
ep_all = ['dump', 'sync', 'schema', 'latest']

# check the endpoint argument
endpoints = [args.endpoint.lower()]

if len([e for e in endpoints if e not in ep_all]) > 0:
  print('''Invalid argument, must be "dump", "latest", "sync", or "schema". \
        Exiting...''')
  sys.exit('invalid request')

# add a schema file to sync
if 'sync' in endpoints:
  endpoints.append('schema')

# TODO: Add byTable endpoint and args

###############################################################################
############################# API Call Generation #############################
###############################################################################

# start the API call
for call in endpoints:
  print('Starting Canvas Data {} request...\nTimestamp: {}\n'.format(
    call, dt_lt))

# not terribly useful unless schema changes, writes schema to a file
if 'schema' in endpoints:
  call_url = cdata_uri.format('schema/latest')
  reqOpts = hmacsig.HMACopts(call_url, args.method, params, cdata_secret)
  auth_headers = hmacsig.HMACsig(reqOpts, api_key)
  start_call = requests.get(call_url, headers=auth_headers)
  call_response = start_call.json()
  file_path = join(schema_out, schema_fname.format(call_response['version'].replace('.', '-')))
  if not isfile(file_path):
    old_schema = listdir(schema_out)
    with open(file_path, 'w+') as schema_file:
      call_json = json.dump(call_response, schema_file, indent=4)
      schema_file.close()
    for schema in old_schema:
      remove(join(schema_out, schema))
    dt_complete = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))
    msg_detail = msg.format(call_response['version'])
    print('Schema file written, check output directory.\n Completed: {}'.format(dt_complete))
    schema_notify = candata.notify(subj, body, msg_detail, whonotify)

# main purpose of script -- syncs Canvas Data API files to output dir
if 'sync' in endpoints:
  sync_files = []
  call_url = cdata_uri.format('account/self/file/sync')
  reqOpts = hmacsig.HMACopts(call_url, args.method, params, cdata_secret)
  auth_headers = hmacsig.HMACsig(reqOpts, api_key)
  start_call = requests.get(call_url, headers=auth_headers)
  call_response = start_call.json()
  # get filename and download path for each table
  table_manifest = call_response['files']
  sync_files = candata.tablesync(table_manifest, out_dir, block_size)
  # catalog existing files -- to remove unnecessary files later (for sync)
  x_files = listdir(out_dir)
  # create a deletion manifest via list comprehension
  del_manifest = [f for f in x_files if f not in sync_files]
  # remove each file in the deletion manifest to complete the sync
  for file in del_manifest:
    fpath = join(out_dir, file)
    if isfile(fpath):
      remove(fpath)
      print('Removed file: {}'.format(fpath))
  dt_complete = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))
  print('Canvas Data synchronized.\nCompleted: {}'.format(dt_complete))

# download latest dump (i.e., tables from last 24 hrs), not needed w/ sync
if 'latest' in endpoints:
  call_url = cdata_uri.format('account/self/file/latest')
  reqOpts = hmacsig.HMACopts(call_url, args.method, params, cdata_secret)
  auth_headers = hmacsig.HMACsig(reqOpts, api_key)
  start_call = requests.get(call_url, headers=auth_headers)
  call_response = start_call.json()
  table_list = call_response['artifactsByTable']

  # TODO: match with sync to utilize candata.tablesync function
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
      with open(file_path, 'wb+') as latest:
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

# if you need more information on daily dumps
if 'dump' in endpoints:
  dump_uri = cdata_uri.format('account/self/dump{}{}')

  if args.limit is not None and args.after is not None:
    call_url = paramcheck(args.limit, args.after, dump_uri)
  else:
    call_url = dump_uri.strip('{}')
  reqOpts = hmacsig.HMACopts(call_url, args.method, params, cdata_secret)
  auth_headers = hmacsig.HMACsig(reqOpts, api_key)
  start_call = requests.get(call_url, headers=auth_headers)
  call_response = start_call.json()

  fname = dump_fname
  file_path = join(out_dir, fname)
  with open(file_path,'w+') as dump_file:
    call_json = json.dump(call_response, dump_file, indent=4)
  dt_complete = datetime.now().strftime('%m-%d-%Y_%H%M{}'.format(local_timezone))
  print('''Dump info file written, check output directory.
      \nCompleted: {}'''.format(dt_complete))
