This script is an update of a script provided by kajigga at: https://github.com/unsupported/canvas/blob/master/api/run_reports/provisioning_report/python/pull_provisioning_report.py.

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
*Added ability to run multiple reports consecutively, only sends one notification
*Added section to create folder structure based on current date [COMMENTED OUT]
*Added section to check for already existing folder, create folder if doesn't exist [COMMENTED OUT]
*Added more information on ENROLLMENT_TERM paramter (must be TERM ID, find via API)
