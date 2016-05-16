This Python script will programatically set the tab sequence (course navigation) for a
list of courses.  

This script requires:

- Python version 2 or above
- Requests Library (http://docs.python-requests.org/en/latest/)

This script also multiprocessing to send multiple tab update API requests at a time.
This will make it run faster when there are hundred or thousands of tabs to set.

Setup
======

Step 1: Copy the `set_tabs.py` file to your system.  

Step 2: Edit `set_tabs.py` to change the variables at the top of the file.  
You could also change the source_course_id_column.  This will allow you to
customize the script to read the column you add to the CSV file.

Step 3: Create a CSV file to match the format of the example `csvfile.csv`.  Save this as
whatever you set the `template_filename` to. The format is simple, actually, with only one
column:


.. csv-table:: Course List
   :header: "course_id"
	 somecanvasid


This example uses SIS id's to reference the courses

.. csv-table:: Course List
   :header: "course_id"
	
   sis_course_id:somesisid
   sis_course_id:anothersisid

This one uses one canvas id and one sis id

.. csv-table:: Course List
   :header: "course_id"

	 somecanvasid
   sis_course_id:someothersisid
