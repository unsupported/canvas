# Merge Multiple Users

This script will merge duplicate accounts into a single account using the Canvas API.

# Setup
When creating the CSV file, there needs to be a column named `merged`, this is going to be the user account you want to become the primary account once merged.

Another column will need to be named `to_be_merged`, this is going to be the account that is merged into the primary account.

Please reference the `merge_users.csv` CSV file for an example of how to setup the CSV file.

*Note:* Headers are required & both columns need to be the SIS ID of the user.
