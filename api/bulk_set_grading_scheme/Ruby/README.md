## Update Course Grading Scheme

This script uses course SIS IDs to target a list of courses and set their grading scheme. Course SIS IDs should be supplied within a CSV file (see the `course_ids.csv` as a template).

#### Setup & Variables
Variables for `access_token`, `domain`, `env` (production, beta, test), `csv_file` (file path), and `grading_standard_id` will all be set via prompts within the Ruby script.

*NOTE* The `grading_standard_id` can be found via the [API endpoint for available grading standards](https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index "List the grading standards available in a context.").
