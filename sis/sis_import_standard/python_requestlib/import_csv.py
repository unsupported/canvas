#!/usr/bin/python

import requests
import json
from pprint import pprint


# 1. Define inputs for the POST/GET request
base_url = 'https://school.instructure.com/api/v1/accounts/self/' # Example: https://ian.test.instructure.com/api/v1/accounts/'
header = {'Authorization' : 'Bearer <token>'}

# Parameters specific to the initial POST request
myfile = '<file_path>' # Example: 'SIS_Testing/users.csv'
payload = {'import_type' : 'instructure_csv', 'extension' : 'csv'}
data = open(myfile, 'rb').read()

# If you're checking the status of an import, include the sis_import_id here in quotes. For submitting an import leave at None.
import_id = None 


# 2. Create a response object from the POST request
def myrequest(base_url, header, payload, data):
	if not import_id:
		r = requests.post(base_url + "/sis_imports/", headers=header, params=payload, data=data)
	else:
		r = requests.get(base_url +  "/sis_imports/" + import_id, headers=header)
	return r

# 3. Pull JSON content from the response into a new JSON object
# 4. Place key elements into a dictionary for later reference
def parsejson(r):
	rjson = json.loads(r.text)
	return rjson

# 0. Main method	
def main():
	# Create a response object from the POST/GET request
	r = myrequest(base_url,header,payload,data)
	# Parse JSON response
	rjson = parsejson(r)
	# Print JSON response
	pprint(rjson)

if __name__ == "__main__": main()
