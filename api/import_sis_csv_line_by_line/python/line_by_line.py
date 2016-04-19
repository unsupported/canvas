#!/usr/bin/env python
# -*- coding: utf-8 -*-

# If you ever need to import a Canvas CSV file one line at a time this script
# could be useful.  

# NOTE: This script uses two 3rd party python modules: requests and clintui
# Use pip to install them like this
#
# pip install requests clint

# Change the DOMAIN and ACCESS_TOKEN
DOMAIN = '<schooldomain>.instructure.com'
ACCESS_TOKEN = 'token-goes-here'

'''
             _ ._  _ , _ ._
           (_ ' ( `  )_  .__)
         ( (  (    )   `)  ) _)
        (__ (_   (_ . _) _) ,__)
            `~~`\ ' . /`~~`
            ,::: ;   ; :::,
           ':::::::::::::::'
 _______________/_ __ \________________________________________________________
|                                                                              |
| Configuration is done. Only edit things after this if you know what you are  |
| doing. You might, I'm not saying you don't, but you might not.               | 
|______________________________________________________________________________|

'''

payload = {'import_type' : 'instructure_csv', 'extension' : 'csv'}
header = {'Authorization' : 'Bearer {}'.format(ACCESS_TOKEN)}
base_url = 'https://{}/api/v1/accounts/self/sis_imports{{}}'.format(DOMAIN)

import sys,csv
import requests,StringIO
from clint.textui import progress
from pprint import pprint

def checkToken(): 
  res = requests.get(base_url.format(''),headers=header)
  print 'res', res.status_code
  return res.status_code == 200


if __name__ == '__main__':

  import_url = base_url.format('')
  problems = []
  if not checkToken():
    print 'invalid access token'
    exit(1)
  with open(sys.argv[1],'rU') as _f:
    csv_r = list(csv.DictReader(_f))
    pending_imports = []
    finished_imports = []
    with progress.Bar(label='importing status',expected_size=len(csv_r)) as bar :

      # Send imports one by one
      for idx,row in enumerate(csv_r):
        bar.label='importing line '.format(idx+1,len(csv_r))
        tmp_s = StringIO.StringIO('')
        csv_wr = csv.DictWriter(tmp_s,fieldnames=row.keys())
        csv_wr.writeheader()
        csv_wr.writerow(row)
        r = requests.post(import_url, headers=header, params=payload, data=tmp_s.getvalue())
        r = r.json()
        r['row'] = idx
        bar.show(idx+1)
        if r.has_key('id'):
          pending_imports.append(r)
        else:
          pprint(r)

      # Loop through the stored import id's until they are all imported
      while pending_imports:
        for idx,pi in enumerate(pending_imports):
          pending_import = pending_imports.pop(idx)
          r = requests.get(base_url.format('/'+str(pending_import['id'])),headers=header).json()
          bar.label = 'import {} status: {} '.format(r['id'],r['workflow_state'])
          bar.show(len(csv_r) - len(pending_imports))
          if r['workflow_state'] in ('created','importing'):
            pending_imports.append(pending_import)
          else:
            finished_imports.append(pending_import)

      # print out those that are imported_with_messages and have
      # processing_errors
      for r in filter(lambda i: 'processing_errors' in i or 'processing_warnings' in i,finished_imports):
        print r
        for err in r['processing_errors']:
          problems.append({'row':r['row'],'errors':err})
        for err in r['processing_warnings']:
          problems.append({'row':r['row'],'errors':err})
  pprint(problems)

