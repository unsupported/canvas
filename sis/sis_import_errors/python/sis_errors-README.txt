SIS Import Errors Notification

PURPOSE: This script is configured to provide an error list from the most
recent Canvas SIS import in both CSV and email format (when configured
properly) to a specified location and list of recipients, respectively.

USE CASE: Run this script shortly after or as part of your SIS imports *every*
time in order to get timely notifications of errors.

Edit the following:

sis_errors_token
CANVAS_DOMAIN
output_path

Everything related to email or CSV output should be labeled as such. Comment
out anything undesired to avoid errors (e.g., you do not want to use email,
comment out all email sections).

NOTES:
* Email formatting slightly wonky, use CSV for best results
* Can alter or supply a value for recent_imp to examine a specific import