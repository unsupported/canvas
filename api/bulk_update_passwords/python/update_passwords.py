#!/usr/bin/env python
# works as of 2/10/2016
import csv, requests, json, time

subdomain = '' # Example: 'myschool' in 'myschool.instructure.com
access_token = '' # your access token
my_file = '' # name of CSV file containing your list of usernames/passwords
my_log = '' # name of the file you'd like to log results to

###################################
## DO NOT EDIT BEYOND THIS POINT ##
###################################

base_url_user = 'https://' + subdomain + 'instructure.com/api/v1/users/sis_user_id:'
base_url_login = 'https://' + subdomain + 'instructure.com/api/v1/accounts/self/logins/'
headers = { 'Authorization' : 'Bearer ' + access_token }
log = open(my_log, 'a')

def fetch_logins(user_id):

	r = requests.get(base_url_user + user_id + '/logins', headers = headers)
	logins = json.loads(r.text)
	#print logins

	for login in logins:
		if 'error' in login:
			logins = False
			exit
	return logins

def lookup_pseudonym(logins, user_id):

	for login in logins:
		if login['sis_user_id'] == user_id:
			login_id = str(login['id'])
			exit
	return login_id

def update_password(login_id, password, user_id):
	error = False
	r = requests.put(base_url_login + login_id, headers = headers, params = { 'login[password]' : password })
	rjson = json.loads(r.text)
	#print rjson

	for key in rjson:
		if key == 'errors':
			update_failed(rjson, user_id)
			error = True
			exit
	if not error:
		print('Updated: ' + user_id)
		log.write('Updated:       ' + user_id + '\n')

def lookup_failed(user_id):
	print('Failed Lookup: ' + user_id)
	log.write('Failed Lookup: ' + user_id +'\n')	


def update_failed(rjson, user_id):
	print('Failed Update: ' + user_id + '\n' +
		  '       Error: ' + str(rjson))
	log.write('Failed Update: ' + user_id + '\n' +
		  	  '       Error: ' + str(rjson) + '\n')

def main():

	with open(my_file,'rb') as csvfile:
		
		log.write(time.strftime('\n%Y-%m-%d %H:%M:%S\n'))
		emailreader = csv.reader(csvfile, delimiter = ",")
		emailreader.next() # skip the header

		for row in emailreader:
			
			user_id = row[0]
			password = str(row[1])

			# look up the user's logins
			logins = fetch_logins(user_id)

			# if the lookup failed
			if not logins:
				lookup_failed(user_id)
				continue

      # find the canvas id for the login matching the sis_user_id provided. This
      # id is not the same thing as the login_id in the CSV files. It is an
      # internal Canvas identifier for that particular username/password.
      # Inside Canvas, these are called pseudonyms.
			pseudonym_id = lookup_pseudonym(logins, user_id)

			# update password on target login
			update_password(pseudonym_id, password, user_id)
		
		print 'END OF FILE'

if __name__ == "__main__": main()

