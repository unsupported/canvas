# Update Users Timezones

This script will allow you to update users time zones en masse for a set of users.

# Setup

Please see the example CSV `example.csv` for construction of the CSV file.
The CSV file will need to contain two columns, a column that has the header as `user_sis_id`, where the users SIS ID is added.
The second column will need to be named `timezone` and have the timezone in the [IANA time zones](http://www.iana.org/time-zones) or the [Rails](http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html) version.

You can use `America/Denver` to set the timezone to Mountain Time (US & Canada), or `America/New_York` for Eastern Time (US & Canada).

Update the values above the specified line to run the script.

# Run

You will need to run `ruby update_users_timezone.rb` once the variables are set in the file.
