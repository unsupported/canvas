#Bulk Update Canvas Login Passwords


##General Information

This script takes a list of Canvas usernames with their respective passwords (ostensibly, at least some of the passwords will be new), and then sets each given username to the password provided. **Why should I care about this? Can't I just upload a users.csv file with new passwords?** At the time of this writing, the users.csv file can create passwords for *brand new users*, but it will not update the password of any *existing* users.

Documentation on the Logins API endpoint: <https://canvas.instructure.com/doc/api/logins.html>

##Required Ruby Gems

There are several ruby gems that you will need to have installed in order to run this script. Instructions to install are as follows:

  gem install typhoeus      # Helps with making the API calls and concurrency
  gem install json          # Assists in parsing the data from the API call

##Using the Script

Before running this script, you'll need to modify the five variables at the beginning of the file:

  ```ruby
  csv_file = ''     			# Use the full path '/Users/XXXXX/Path/To/File.csv' to source csv file
  access_token = ''				# Your API token that was generated from your account user
  domain = '' 						# domain.instructure.com, use domain only
  env = '' 						  	# Leave nil if pushing to Production
  output_csv = ''         # Put the full path to a blank csv file to have the errors written in.
  ```
##CSV Files

The csv_file should follow the format of the provided csv example file:

sis_user_id | sis_login_id | new_password
--- | --- | ---
12345 | example@example.com | asdfasdf

The first two columns can be obtained by running an [SIS Export Report](https://community.canvaslms.com/docs/DOC-3050) and copying the user_id and login_id columns.

In case your import file contains any users that are not in Canvas or other errors, the output_csv file will populate a csv file for you with the errors. The following errors are as follows:

  1. User sis_user_id does not exist in Canvas
  2. The sis_login_id provided in the csv_file does not match an existing login_id for the user in Canvas

The first column of the output_csv will be either 1 or 2 so you can filter in excel to sort the error data by type.

##Errors While Running script

If you run into errors with your script running it is probably because your api token is being throttled. For more information on throttling please see <https://canvas.instructure.com/doc/api/file.throttling.html>. If you suspect this is happening to you reduce the number in this line of code:

  ```ruby
  hydra = Typhoeus::Hydra.new(max_concurrency: 10)
  ```
