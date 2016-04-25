#SIS Import Example using Python Requests Library


##General Information

Documentation on the SIS import API itself: <https://canvas.instructure.com/doc/api/sis_imports.html>

Documentation on the required format for the files you import: <https://canvas.instructure.com/doc/api/sis_csv.html>

##Requests Library

This example makes use of the [Requests](http://docs.python-requests.org/) library, a Python HTTP library "written for human beings". As of this writing, Requests is supported in Python versions 2.6 to 3.3. 

Instructions for installing Requests can be found [here](http://docs.python-requests.org/en/latest/user/install/). If you'd like to learn more about how to use the library itself, take a look at the [Quickstart Guide](http://docs.python-requests.org/en/latest/user/quickstart/).

##Using the Script

This script allows you to both submit an SIS import and check the status of imports that you've already run. Before you can submit an initial request, you'll need to replace the code enclosed in angle brackets with your own data.

	# 1. Define inputs for the POST/GET request
	base_url = '<MY_BASE_URL>' # Example: https://canvas.instructure.com/api/v1/accounts/'
	account_id = '<MY_ACCOUNT_ID>' # Example: 95298
	header = {'Authorization' : 'Bearer <MY_ACCESS_TOKEN>'}

	# Parameters specific to the initial POST request
	myfile = '<MY_FILE>' # Example: 'SIS_Testing/users.csv'
	payload = {'import_type' : 'instructure_csv', 'extension' : 'csv'}
	data = open(myfile, 'rb').read()

* `<MY_BASE_URL>`: From the example, replace "canvas" with the subdomain for your Canvas instance.
* `<MY_ACCOUNT_ID>`: The account ID for your Canvas instance. This number is visible in the URL address when accessing Canvas, immediately following "accounts/".
* `<MY_ACCESS_TOKEN>`: If you're unsure of how to generate this, review [this](https://canvas.instructure.com/doc/api/file.oauth.html) page of the Canvas API, under "Manual Token Generation".
* `<MY_FILE>`: Filepath to the CSV you'll be importing.

###Submit CSV
When you run the script, you should get a response that looks something like this: 

	{
		'created_at': '2013-03-13T11:14:14-06:00',
		'data': {'import_type': 'instructure_csv'},
		 'ended_at': None,
		 'id': 5467052,
		 'progress': 0,
		 'updated_at': '2013-03-13T11:14:14-06:00',
		 'workflow_state': 'created'
	}

Notice that `workflow_state` is set to 'created' and the current import progress is at 0%. Take note of the `id` value, as you'll need that to check the status of the import.

###Check import status
You can now take the id from the response to check the status of the import. On the line in the script that reads `import_id = None`, replace `None` with the id, surrounded by quotes.

Running the script again, the response will look something like this:

	{
		'created_at': '2013-03-13T11:14:14-06:00',
		'data': {'import_type' : 'instructure_csv'},
		'ended_at': None,
		'id': 5467052,
		'progress': 10,
		'updated_at': '2013-03-13T11:14:22-06:00',
		'workflow_state': 'importing'
	}

Notice how in the above response, `progress` is now 10 and `workflow_state` has changed from 'created' to 'importing'. As you continue to check the status of the import, `progress` will be a number between 0 and 100.

When the import has completed, `progress` will be at 100 (unless there was a failure during the import), and `workflow_state` will be 'imported', 'imported\_with\_messages', 'failed', or 'failed\_with\_messages'. Here's an example response:

	{
		'created_at': '2013-03-13T11:14:14-06:00',
		'data': {
			'counts': {
				'abstract_courses': 0,
				'accounts': 0,
				'courses': 0,
				'enrollments': 0,
				'grade_publishing_results': 0,
				'group_memberships': 0,
				'groups': 0,
				'sections': 0,
				'terms': 0,
				'users': 149,
				'xlists': 0
				},
			'import_type': 'instructure_csv',
			'supplied_batches': ['user']
			},
		'ended_at': '2013-03-13T11:14:23-06:00',
		'id': 5467052,
		'progress': 100,
		'updated_at': '2013-03-13T11:14:23-06:00',
		'workflow_state': 'imported'
	}

