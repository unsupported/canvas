This Python script will programatically do course copies.  It
requires:

- Python version 2 or above
- Requests Library (http://docs.python-requests.org/en/latest/)

Setup
======

Step 1: Copy the `do_course_copy.py` file to your system.  

Step 2: Edit `do_course_copy.py` to change the variables at the top of the file.  
You could also change the source_column_name and
destination_column_name variables.  This will allow you to
customize the script to read the columns you add to the CSV file.

Step 3: Create a CSV file to match the format of the example `csvfile.csv`.  Save this as
whatever you set the `template_filename` to. The format is simple, actually, with only two
columns:

	source_id,destination_id
	somecanvasid,someothercanvasid


This example uses SIS id's to reference the courses

	source_id,destination_id
	sis_course_id:somesisid,sis_course_id:someothersisid

This one uses one canvas id and one sis id

	source_id,destination_id
	somecanvasid,sis_course_id:someothersisid
