# Bulk Delete Courses

These scripts allow for the deletion of courses in bulk, using either a course's SIS ID or Canvas Course ID (`<domain>.instructure.com/courses/<canvas_course_id>`) for those manually created courses.  In order to find a list of course SIS IDs or Canvas Course IDs, you'll need to run a provisioning report and include "courses" as an option.

To run the script(s), you will need to edit the value of the variables (see script file(s)) to be specific to your Canvas domain and access token.  The second part of the script setup is to edit the CSV files with the necessary data, whether that be `sis_course_id` or `canvas_course_id`.  Once the script file and CSV file have been updated and saved, run the command `ruby <name_of_ruby_file>.rb`.  Each response should be seen as an output in the console.
