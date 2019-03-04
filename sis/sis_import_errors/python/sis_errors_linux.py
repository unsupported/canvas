#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Brandon Poulliot
# Working as of 3/4/19
# currently uses mutt utility to send mail w/ attachment

# standard libraries
import json
import time
import subprocess
from os import remove

# non-standard libraries
import requests

# token w/ access to get SIS import errors
sis_errors_token = '<set token here>'

# canvas config info
CANVAS_DOMAIN = '<CANVAS DOMAIN>'
ACCOUNT_ID = '1'

# set output folder, leave curly braces e.g.:
#     /home/user/downloads/{}
output_path = '/home/user/folder/{}'

# mail info
err_date = time.strftime('%m-%d-%Y %H:%M:%S')
recipient = '<EMAIL ADDRESS>'
subject = 'Canvas SIS Import Errors {}'.format(err_date)
body = output_path.format('err_mailbody.txt')

###############################################################################
############# BE EXTREMELY CAREFUL CHANGING ANY INFORMATION BELOW #############
###############################################################################

BASE_DOMAIN = 'https://{}/api/v1/{}/'.format(CANVAS_DOMAIN,{})
BASE_START_URI = BASE_DOMAIN.format('accounts/{}/{}'.format(ACCOUNT_ID,{}))
IMP_LIST = 'sis_imports{}'

# This headers dictionary is used for almost every request
headers = {'Authorization':'Bearer {}'.format(sis_errors_token)}

# NOTE: This is the main change -- other script read out each piece of info
#       while this one simply snags the file, downloads it, 

# define API call for single most recent SIS import
# NOTE: If you do back-to-back uploads, this may grab the wrong one
get_sis_imp = BASE_START_URI.format(IMP_LIST.format('?per_page=1'))

# get the most recent SIS import info
fetch_sis = requests.get(get_sis_imp,headers=headers)
imp_list = json.loads(fetch_sis.text)
imp_info = imp_list['sis_imports'][0]
imp_id = imp_info['id']
imp_status = imp_info['workflow_state']
print('SIS Import {} completed with a status of: {}.'.format(imp_id, imp_status))

# if the SIS import broke, generate a message
if (
    imp_status == 'imported_with_messages' or
    imp_status == 'failed_with_messages'
    ):
    imp_errors = imp_info['errors_attachment']
    err_file_info = imp_errors['url']
    err_file_dl = requests.get(err_file_info,headers=headers,stream=True)
    err_file_local = output_path.format(imp_errors['display_name'])
    with open(err_file_local, 'w+b') as errfile:
        errfile.write(err_file_dl.content)
        errfile.close()
    with open(body, 'w+') as mailbody:
        mailbody.write('The last SIS import (ID: {}) resulted in errors.'.format(imp_id))
        mailbody.close()
    
    # send it with mutt
    err_notify = 'mutt -s "{}" -a {} -- {} < {}'.format(subject, err_file_local, recipient, body)
    subprocess.call(err_notify, shell=True)
    
    # remove local files
    remove(err_file_local)
    remove(body)

else:
    print('No errors detected...')
