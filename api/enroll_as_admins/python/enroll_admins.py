#!/usr/bin/env python
# works as of 1/15/2016
import csv, json, requests

log_filename = '<REPLACE>'			# File to write log to. Example: my_log.txt
csv_filename = '<REPLACE'			# File to pull the CSV data from. Example: my_data.csv
user = {
	'domain':'<REPLACE>',			# Your domain. Example: https://myschool.instructure.com
	'access_token':'<REPLACE>' 		# Example: 1~13eoncw39f32080234hnv230850KLJ823n8H
}

####################################################
### no need to change anything beyond this point ###
####################################################

api_path = ['/api/v1/accounts/', '/admins']
header = {"Authorization" : "Bearer " + user['access_token']}

if __name__ ==  '__main__':
	with open(csv_filename, 'U') as csv_file:
		reader = csv.reader(csv_file)
		for rows in reader:
			account = 'sis_account_id:' + rows[0]			
			adminId = 'sis_user_id:' + rows[1]
			role = rows[2]
			print adminId + ", " + account
			print api_path[0] + account + api_path[1]
			payload = {'user_id' : adminId, 'send_confirmation' : 0, 'role' : role}
			r = requests.post(user['domain'] + api_path[0] + account + api_path[1], headers=header, params=payload)
			rjson = json.loads(r.text)
			print rjson
			print "Added " + rjson['user']['name']
			log = open(log_filename, 'a')
			log.write('Added ' + rjson['user']['name'] + ' (' + adminId + ')\n' )
			log.close()
