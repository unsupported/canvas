#!/usr/bin/python3
# -*- coding: utf-8 -*-

from subprocess import call
import re
from os.path import getsize, isfile, join
import requests
from os import listdir, remove
import argparse
import gzip

def parse(argv=None):
  # create argument parser to allow for command line arguments
  parser = argparse.ArgumentParser(description='''Separate Canvas Data API call
                                               components.''')

  # add arguments to parser, first is positional (must be 1st) and required
  parser.add_argument('endpoint',
                      help='''Specify the endpoint of your API call: dump,
                           sync, latest, or schema.''')
  parser.add_argument('-l', '--limit',
                      help='''Syntax is "limit=#", specifies how many records
                           to return. Only works with dump.''')
  parser.add_argument('-a', '--after',
                      help='''Syntax is "after=#", specifies to pull only data
                      after dump number provided. Only works with dump.''')
  # this one doesn't matter right now, only method available is GET
  parser.add_argument('-m', '--method', default='GET',
                      help='''Future-proofing for possible new methods for
                           Canvas Data API. Currently, only method is GET.''')
  # parse args from sys.argv into ParseResult object
  args = parser.parse_args()
  return args

def notify(subj, body, msg, whonotify):
  with open(body, 'w') as email:
    email.write(msg)
    email.close()
  send = 'mutt -s "{}" -- {} < {}'.format(subj, whonotify, body)
  call(send, shell=True)
  remove(body)

def paramcheck(limit, after, endpoint):
  limit_syntax = re.search('^limit\=\d+$', args.limit)
  if limit_syntax is not None:
    raw_params.append(args.limit)

  after_syntax = re.search('^after\=\d+$', args.after)
  if after_syntax is not None:
    raw_params.append(args.after)

  raw_params.sort()
  params = '&'.join(raw_params)
  call_url = dump_uri.format('?', params)

  return call_url

def tablesync(table_manifest, out_dir, block_size):
  sync_files = []
  for table in table_manifest:
    fname = table['filename']
    file_path = join(out_dir, fname)
    flat_fname = fname.split('.')[0]
    print(fname)
    # add extension if desired, makes no difference but you do you
    flat_file = file_path.split('.')[0] # + '<file extension>'
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
      with open(file_path, 'wb+') as sync:
        sync.write(dl_file.content)
        sync.close()
      print('Downloaded file: {}'.format(fname))
      # open gz file and dump contents into flat file block by block
      with gzip.open(file_path, 'rb') as zipped, \
      open(flat_file, 'wb+') as unzipped:
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
  return sync_files

