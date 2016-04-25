#Bulk Update Canvas Login Passwords


##General Information

This script takes a list of Canvas usernames with their respective passwords (ostensibly, at least some of the passwords will be new), and then sets each given username to the password provided. **Why should I care about this? Can't I just upload a users.csv file with new passwords?** At the time of this writing, the users.csv file can create passwords for *brand new users*, but it will not update the password of any *existing* users.

Documentation on the Logins API endpoint: <https://canvas.instructure.com/doc/api/logins.html>

##Requests Library

This example makes use of the [Requests](http://docs.python-requests.org/) library, a Python HTTP library "written for human beings". As of this writing, Requests is supported in Python versions 2.6 to 3.3. Instructions for installing Requests can be found [here](http://docs.python-requests.org/en/latest/user/install/). If you'd like to learn more about how to use the library itself, take a look at the [Quickstart Guide](http://docs.python-requests.org/en/latest/user/quickstart/).

##Using the Script

Before running this script, you'll need to set the four variables at the beginning of the file:
	
	subdomain = '' # Example: 'myschool' in 'myschool.instructure.com
	access_token = '' # your access token
	my_file = '' # name of CSV file containing your list of usernames/passwords
	my_log = '' # name of the file you'd like to log results to

You'll also need to create a CSV with a list of usernames and the passwords you'd like to assign to them. This needs to be placed in the same directory that you're running the script from. You'll find an example CSV here on this page.

If you want to log your results to a file, you'll need to create that file (again, in the same directory as the script) prior to running update_passwords.py.