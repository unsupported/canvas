# Change SIS ID

This ruby script allows for changing user's sis_user_id in Canvas. This type of script is often used when changing student information systems.

# Setup

Before running this script, you'll need to modify the five variables at the beginning of the file:

  ```ruby
  csv_file = ''     			# Use the full path '/Users/XXXXX/Path/To/File.csv' to source csv file
  access_token = ''				# Your API token that was generated from your account user
  domain = ''             # domain.instructure.com, use domain only
  env = '' 						    # Leave nil if pushing to Production
  output_csv = ''         # Put the full path to a blank csv file to have the errors written in.
  ```
  
## CSV Files

When creating the source CSV file, you will need to make a column named `old_user_sis_id` as one header.
The other header needs to be `new_user_sis_id` for the value you want it changed to as follows.

old_sis_user_id | new_sis_user_id
--- | ---
12345 | 23456

You will also want to provide a blank csv file for the `output_csv` file. The script will output an error report to a the `output_csv` file as provided by you. It will output users who do not have the old_sis_user_id provided in the CSV.

# Running the Script

This script is running things concurrently for increased efficiency. This means that you may have to wait for a minute for things to queue up before you'll see logging.

If you run into errors with your script running it is probably because your api token is being throttled. For more information on throttling please see <https://canvas.instructure.com/doc/api/file.throttling.html>. If you suspect this is happening to you reduce the number in this line of code:

  ```ruby
  hydra = Typhoeus::Hydra.new(max_concurrency: 10)
  ```

