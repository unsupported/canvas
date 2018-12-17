This script is an update and expansion of a script provided by kajigga in the
same repository (/run_reports/provisioning_report/).

PURPOSE: This script allows you to set one or multiple account reports in
Canvas to be run, downloaded, and moved to a specified location (local,
network, and even Samba destinations all work). The script is then setup to
send out an email from a specified account (you must have permission to send
from this address) to a one or more recipients.

USE CASE: Use a BATCH script to run daily, weekly, and monthly reports and
deliver them to a shared destination like a network drive or mapped SharePoint
folder via Windows Task Scheduler. Can also run as BASH script or simple
cronjob in Linux - more flexibility in scheduling with crontab.

Most information for what to replace is contained within the Python file.

NOTES:
* Reports verified working as of 6/11/18:
  - proserv_student_submissions_csv
  - unpublished_courses_csv
  - unused_courses_csv
  - zero_activity_csv
  - outcome_results_csv
* Match your SIS ID for term exactly -- there is no way to validate universally
  - Script will fail if your term argument doesn't match a term in Canvas
* Note that include_ or do_ variables set this option for ALL reports in run
  - Check report configurations in UI to understand which reports these
    variables apply to (e.g., provisioning report)
  - TODO: add another variable check for which options to run (in progress)

################################# Changelog ###################################

Initial commit:
* Modified to be Python 3.6 compatible
* Modified to be Windows compatible
* Modified to actually send the downloaded file to output directory
  - Previously files were saved to the directory where the script was run
* Modified to allow for setting account ID (previously only SELF)
* Added portion to notify report requester of report availability via email

6/11/18
* Added ability to run multiple reports consecutively, sends one notification
* Ability to create folder structure based on current date [OFF]
* Ability to check for existing folder, create folder if not [OFF]
* Information on ENROLLMENT_TERM parameter (must be TERM ID, find via API link)

12/13/18
* Replaced deprecated string formatting
* Added sys library to utilize optional variable
  - Optional variable of semester SIS ID can be passed (e.g., 'FA18')
  - Limits reports to specific semester without Canvas semester ID
  - If no variable specified, semester is set to false (all semesters)
* Removed unused BASE_FILE_URI
* Modified comments for clarity