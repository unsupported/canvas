This Python script will programatically do course migrations.  It assumes that you have
hosted the course migration files on a publicly visible web server where Canvas can
download them from. 

It requires:

- Python version 2 or above
- Requests Library (http://docs.python-requests.org/en/latest/)

This script also multiprocessing to send multiple course copy API requests at a time.
This will make it run faster when there are hundred or thousands of copies to trigger.

Setup
======

Step 1: Copy the `course_migrations.py` file to your system.  

Step 2: Edit `course_migrations.py` to change the variables at the top of the file.  
You could also change the source_archive_filename_column and
destination_course_id_column variables.  This will allow you to
customize the script to read the columns you add to the CSV file.

Step 3: Create a CSV file to match the format of the example `csvfile.csv`.  Save this as
whatever you set the `template_filename` to. The format is simple, actually, with only two
columns. *source_filename* is the filename of the course archive on the web.
*destination_id* is the id of the course to receive the content.

	source_filename,destination_id
	some_archive_filename,somecanvasid


This example uses an SIS id to reference the destination course:

	source_filename,destination_id
	somecanvasid,sis_course_id:someothersisid


Alternative
===========
As an alternative, you can use the script in the bulk_upload_migration folder to
upload the migration files to Canvas then run the migration from there. If you do
that, you do not use this course_migrations.py file.
