#!/usr/bin/python
#Working as of 11/19

import csv, requests, time, os
import json, collections
#import re
import mimetypes
import pprint

#working_path = '/path/to/the/folder/housing/the/bulk_assign_avatars/script/' # Base working path of this script, where everything will be housed
working_path = './' # Base working path of this script, where everything will be housed

csv_filename = 'sample.csv' # Example: 'API_Testing/users_provisioning.csv', relative to
                            # working_path.  This file contains the three  columns needed
                            # by this script.  Those columns are 
                            #   - user_id 
                            #     This is the SIS user_id.
                            #   - image_filename
                            #     the name of the image file, relative to the working path folder
                            #   - image_filetype 
                            #     the filetype of the image.  This will be something like
                            #     jpeg, png, gif. This field is needed right now because
                            #     the script does not auto-detect the filetype
"""
user_id,image_filename,image_filetype
4098275,DogHouse1.jpg,jpeg
"""
                            
images_path = 'images/'  # This is the name of the folder than houses the images.  It
                         # should be relative to the working_path
                            # script output
                            # relative to working_path

domain = 'domain.instructure.com' #Replace domain
access_token = os.environ['ACCESS_TOKEN']
#access_token = ""

##############################################################################
##############################################################################
################ Don't edit anything past here unless you know what you are doing.
################ NOTE: No offense, you probably do know what you're doing.  This is for
################ those that do not.  


header = {'Authorization' : 'Bearer {0}'.format(access_token)}
valid_mimetypes = ('image/jpeg','image/png','image/gif')

with open(f"{working_path}/{csv_filename}") as csv_file:
    read_csv = csv.DictReader(csv_file)
    for row in read_csv:
        # Step 1: Start upload file to user's file storage in Canvas
        inform_api_url = f"https://{domain}/api/v1/users/self/files"
        image_path = f"{working_path}{images_path}{row['image_filename']}"
        mime_type = mimetypes.guess_type(image_path)
        inform_parameters = {
            'name': row['image_filename'],
            'content_type': mime_type,
            'size': os.path.getsize(image_path),
            'parent_folder_path': 'profile pictures', 
            'as_user_id': f"sis_user_id:{row['user_id']}"
        }
        res = requests.post(inform_api_url,headers=header,data=inform_parameters)
        print("Done prepping Canvas for upload, now sending the data...")
        data = res.json()
        # Step 2:  Upload data
        files = {'file':open(image_path,'rb').read()}
        upload_params = data.get('upload_params')
        upload_url = data.get('upload_url')
        upload_file_res = requests.post(upload_url, data=upload_params, files=files, allow_redirects=False)
        # Step 3: Confirm upload
        confirmation_url = upload_file_res.headers['location']
        confirmation = requests.post(confirmation_url,headers=header)
        if 'id' in confirmation.json():
            file_id = confirmation.json()['id']
        else:
            print('no id here')
        params = {'as_user_id': f"sis_user_id:{row['user_id']}"}
        # Step 4: Find recently uploaded image and get the user token
        avatar_options = requests.get(f"https://{domain}/api/v1/users/sis_user_id:{row['user_id']}/avatars", headers=header, params=params)
        
        for ao in avatar_options.json():
            if ao.get('display_name') == row['image_filename']:
                print('found')
                token = ao.get('token')
                params['user[avatar][token]'] = token
                set_avatar_user = requests.put(f"https://{domain}/api/v1/users/sis_user_id:{row['user_id']}", headers=header, params=params)
                print(set_avatar_user)
                if set_avatar_user.status_code == 200:
                    print(f'Profile image set for user - {row["user_id"]}')
                else:
                    print('Failed to set profile image for user - {row["user_id"]}')