Pull the SIS Export Report programmatically
===========================================
This file will start a report, track the status of the report, then save the file to
the local system.

These are the steps the script follows::

Step 1: Start the report
Step 2: Wait for the report to be finished
Step 3: Pull out the file number
Step 4: Pull out the Canvas file info from the files API
Step 5: Finally fetch the file and save it to the output directory

The requests library is the only non-standard python libary used.  It just makes things so
much easier.

Setup/Usage
===========
First, edit the following variables::
  - token
  - ACCOUNT_ID
  - CANVAS_DOMAIN
  - OUTPUT_FOLDER
  - ENROLLMENT_TERM
  - include_deleted_items
  - do_accounts
  - do_courses
  - do_enrollments
  - do_sections
  - do_terms
  - do_users
  - do_xlist
  - do_group_membership
  - do_groups

Then run the script.
