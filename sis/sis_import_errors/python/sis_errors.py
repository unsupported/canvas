#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# written by Brandon Poulliot @ UCCS
# working as of 12/13/18

import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
    
# Change this to match your access token
sis_errors_token = '<insert token here>'

# Change this to match the domain you use to access Canvas
CANVAS_DOMAIN = '<yourdomain>.instructure.com'
ACCOUNT_ID = '1'

############################ CHANGE FILE SETTINGS #############################

# must include directory and file -- can customize with variables if desired
# will be overwritten unless unique name used
# example: '/home/user1/sis/errors/sis-import-errors-{}.csv' could be used as
#          output_path.format(recent_imp) to give filename with sis import id
output_path = '<your path here>'

############################ CHANGE EMAIL SETTINGS ############################

# Set email server and FROM email address (example is O365)
smtpserver = 'smtp.office365.com:587'
from_addr = '<email1@address.edu>'

# Add email addresses to list as recipients
to_list = ['<email2@address.edu>','<email3@address.edu>']

###############################################################################
############# BE EXTREMELY CAREFUL CHANGING ANY INFORMATION BELOW #############
###############################################################################

BASE_DOMAIN = 'https://{}/api/v1/{}/'.format(CANVAS_DOMAIN,{})
BASE_START_URI = BASE_DOMAIN.format('accounts/{}/{}'.format(ACCOUNT_ID,{}))
IMP_LIST = 'sis_imports{}'
ERR_LIST = IMP_LIST.format('/{}/errors')

# This headers dictionary is used for almost every request
headers = {'Authorization':'Bearer {}'.format(sis_errors_token)}

get_sis_imp = BASE_START_URI.format(IMP_LIST.format('?per_page=1'))
get_err_list = BASE_START_URI.format(ERR_LIST)

# get the most recent SIS import ID
fetch_sis = requests.get(get_sis_imp,headers=headers)
sis_imp_list = json.loads(fetch_sis.text)
# specify sis import id below instead of auto-populating for info on one import
recent_imp = sis_imp_list['sis_imports'][0]['id']

# get error list from most recent import
fetch_err = requests.get(get_err_list.format(recent_imp),headers=headers)
err_json = json.loads(fetch_err.text)
err_comps = err_json['sis_import_errors']
err_count = len(err_comps)
err_report = []

# build error list if there are any errors in the list
if err_count > 0:
    err_summary = '''The most recent SIS Import (ID: {})
    resulted in {} errors. Locate {} for more information.\n'''.format(
        recent_imp,err_count,output_path)
    # CSV output headers
    err_headers = 'error_file,error_row,error_message\n'
    # EMAIL body
    msg_body = '<p>{}</p>'.format(err_summary)
    
    print(err_summary)

    # build a row or paragraph for each error, write or append it
    err_index = 0
    for error in err_comps:
        # building CSV row
        err_row = ('{},{},{}'.format(err_comps[err_index]['file'],
                                        str(err_comps[err_index]['row']),
                                        '"{}"'.format(
                                            err_comps[err_index]['message'])
                                        )
                  )
        # building EMAIL message
        msg_body += '<p>{}</p>'.format(err_row.replace(',','<br />'))
        err_report.append(err_row)
        err_index += 1
    
################################# CSV OUTPUT ##################################
    # write the CSV file specified in output path above    
    with open(output_path, 'w') as err_file:
        err_file.write(err_headers)
        
        err_index = 0
        for row in err_report:
            err_file.write(err_report[err_index] + '\n')
            err_index += 1
    # end CSV
    
################################ EMAIL OUTPUT #################################
    # build and send the email as high priority
    # Create MIME object
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(map(str, to_list))
    msg['X-Priority'] = '2'
    
    # Edit these if necessary to customize subject and body of email
    msg['Subject'] = 'SIS Import Errors Alert'
    
    # Attach body message as HTML, turn entire email into MIME string
    msg.attach(MIMEText(msg_body, 'html'))
    
    # Setup email server for secure login
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    
    # Pass credentials to server, send email, and close connection
    # Use app password/token if possible
    server.login('<email username>','<email password>')
    server.send_message(msg)
    server.quit()
    # end EMAIL
        
else:
    print('''The most recent SIS Import (ID: {})
          resulted in zero errors.'''.format(recent_imp))
