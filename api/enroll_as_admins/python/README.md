#Bulk Enroll Admins


##General Information

Documentation on the "Create Account Admin" API itself: <https://canvas.instructure.com/doc/api/admins.html#method.admins.create>

##Requests Library

This example makes use of the [Requests](http://docs.python-requests.org/) library, a Python HTTP library "written for human beings". As of this writing, Requests is supported in Python versions 2.6 to 3.3. 

Instructions for installing Requests can be found [here](http://docs.python-requests.org/en/latest/user/install/). If you'd like to learn more about how to use the library itself, take a look at the [Quickstart Guide](http://docs.python-requests.org/en/latest/user/quickstart/).


##Using the Script

Use this script to assign a large number of Canvas users as admins to their respective account/sub-accounts. Simply update the `<REPLACE>` fields with your own information.  

Note that you should use the **SIS ID**, not the Canvas ID, of each user and the account/sub-account you would like to assign them to. See the `example_csv_file.csv` for an idea of what the file should look like.