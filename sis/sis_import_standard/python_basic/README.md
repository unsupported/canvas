Using the Canvas Open API to submit SIS Imports
===============================================

Last edited:  Mon Nov 14 13:34:52 MST 2011

General Information
--------------------

Documentation on the SIS import API itself::

 https://canvas.instructure.com/doc/api/sis_imports.html

Documentation on the format of the SIS files::

 https://canvas.instructure.com/doc/api/sis_csv.html

Python Example
--------------
**First** submit the CSV file.  You will need the json and MultipartPostHandler python
modules installed.  If you use this script, you will also need to change the
following variables to fit your environment:

BASE_URL
  replace "canvas" with the subdomain for your canvas instance
access_token
  replace this with an access token you have obtained (on your profile page in Canvas)
account_id
  replace this with the account id for your canvas instance.  This number is
  visible in the URL address when accessing Canvas.

![account id](account_id.jpg "Account ID Text")


    import urllib2
    import MultipartPostHandler
    import json

    BASE_URL = "http://canvas.instructure.com/api/v1/%s"
    access_token = "8TgEIYYfJLE9snELVit4bSh7uELJVzxb2WRJI6hayGwNSbmIV3aEXo4yQ7wFai7c"
    account_id = 11111 
    endpoint = BASE_URL % '/accounts/%s/sis_imports.json' % (account_id)

    # A csv file formatted according to the documentation listed above
    sis_file = 'users.csv' 
    params = {'attachment':open(sis_file,'rb'),
        'access_token':access_token,
        'import_type':'instructure_csv',
      }

    # Because of how the CSV file needs to be posted, we need to use the
    # MultipartPostHandler module.
    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
    urllib2.install_opener(opener)
    req = urllib2.Request(endpoint,params)
    response = urllib2.urlopen(req).read().strip()
    response_data = json.loads(response)

Here is what ``response_data`` might look like.


    {
     'ended_at': None,
     'workflow_state': 'created',
     'created_at': '2011-11-04T10:12:44-06:00',
     'updated_at': '2011-11-04T10:12:45-06:00',
     'progress': 0,
     'data': {'import_type': 'instructure_csv'},
     'id': 30113
     }


**Next**, check the status of the SIS import with a second API call.

    import_id = response_data['id']
    status_endpoint = BASE_URL % '/accounts/%d/sis_imports/%d.json?access_token=%s' % (account_id,import_id,access_token)
    fh = urllib2.urlopen(status_endpoint)
    status = json.loads(response)

While the import is still processing, the value of ``status`` will look like this.
Note that ``ended_at`` is None or null, ``workflow_state`` is "created", and ``progress``
will be a number between 0 and 99 (percent).


    {
      'ended_at': None,
      'workflow_state': 'created',
      'created_at': '2011-11-04T11:10:14-06:00',
      'updated_at': '2011-11-04T11:10:15-06:00',
      'progress': 0,
      'data': {
        'import_type': 'instructure_csv'
      },
      'id': 30148
    }

When the import is completed, ``status`` is modified where 
``ended_at`` is now a timestamp, ``workflow_state`` will be 'imported' or possibly
'imported_with_messages'.  If there are errors in the import, they will be in
the ``processing_warnings`` list.  Counts of the items imported can be found in
``data['counts']``.


    {
      'ended_at': '2011-11-04T09:59:30-06:00',
      'workflow_state': 'imported_with_messages',
      'created_at': '2011-11-04T09:57:56-06:00',
      'updated_at': '2011-11-04T09:59:30-06:00',
      'processing_warnings': [
        ['csv_1st_import/enrollments.csv', 'Attempted enrolling of deleted user cc_u001 in course ccoct2011:1'],
      ],
      'progress': 100,
      'data': {
        'import_type': 'instructure_csv',
        'counts': {
          'terms': 1,
          'users': 21,
          'grade_publishing_results': 0,
          'abstract_courses': 0,
          'group_memberships': 14,
          'courses': 23,
          'accounts': 1,
          'xlists': 0,
          'groups': 4,
          'enrollments': 736,
          'sections': 46
        }
      },
      'id': 30148
    }

