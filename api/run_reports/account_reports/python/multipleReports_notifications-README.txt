This script is an update and expansion of a script provided at: https://github.com/unsupported/canvas/blob/master/api/run_reports/provisioning_report/python/pull_provisioning_report.py.

PURPOSE: This script allows you to set one or multiple account reports in Canvas to be run, downloaded, and moved to a specified location (local, network, and even Samba destinations all work). The script is then setup to send out an email from a specified account (you must have permission to send from this address) to a one or more recipients.

USE CASE: Use a BATCH script to run daily, weekly, and monthly reports and deliver them to a shared destination like a network drive or mapped SharePoint folder via Windows Task Scheduler. Can also run as BASH script or simple cronjob in Linux - more flexibility in scheduling with crontab.

Most information for what to replace is contained within the Python file.

*Modified to be Python 3.6 compatible
*Modified to be Windows compatible
*Modified to actually send the downloaded file to output directory
  *Previously files were saved to the directory where the script was run
*Modified to allow for setting account ID (previously only SELF)
*Added portion to notify report requester of report availability via email

NOTE: I have not tested all reports and cannot verify they will all run successfully.
*Verified working as of 6/11/18:
 -proserv_student_submissions_csv
 -unpublished_courses_csv
 -unused_courses_csv
 -zero_activity_csv
 -outcome_results_csv

6/11/18
*Added ability to run multiple reports consecutively, only sends one notification (could be altered)
*Added section to create folder structure based on current date [COMMENTED OUT]
*Added section to check for already existing folder, create folder if doesn't exist [COMMENTED OUT]
*Added more information on ENROLLMENT_TERM parameter (must be TERM ID, find via API link)
