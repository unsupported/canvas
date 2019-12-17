# Update Users Timezones

Allows you to update users time zones in bulk for a set of users.

## Setup

- Please see the [example CSV](./example.csv) as an example of the required CSV headers.
- Required Headers:
  - `user_sis_id` - The user's SIS ID as it appears in Canvas
  - `timezone` - The desired timezone formatted either as a [IANA time zone](http://www.iana.org/time-zones) or [Rails](http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html) timezone.
    - `America/Denver` is an example a timezone equivalent to `Mountain Time (US & Canada)`
    - `America/New_York` is an example a timezone equivalent to `Eastern Time (US & Canada)`

## Run

1. Ensure your CSV file has the required `user_sis_id` and `timezone` headers.
2. In a terminal window: `ruby update_users_timezone.rb`.
3. Prompts will ask you to separately enter a `token` (valid for domain and environment for which the script will run), `domain`, `environment`, and `source file` in order to set variables within the script.
4. Terminal output should show `Updated user <user_sis_id> with new time zone settings` for each user in your CSV file.
5. Last output line should read `Completely Done`.
