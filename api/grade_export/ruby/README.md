# Grade Export Script

## About ##
This script generates a grade export report using the Canvas enrollments API. It traverses a provisioning report for a given term, and reports a Letter Grade.

#Technical Specs
  - Ruby Version 2.2.3+
  - External Gems you may need to install:
       - [Typhoeus](https://github.com/typhoeus/typhoeus) - Request client
       - [Net-sftp](https://github.com/net-ssh/net-sftp) - SFTP client


 #Requirements
  - This script will pull grades for a given term and assumes your courses are associated with a `term_id`
  - section_ids and course_ids should also be included with every course and section
  - A grading scheme must be enabled in a course as this will *only* export final letter grades
  - There needs to be a directory in the SFTP root called "Grades" (this can be modified around line 156 `sftp.upload!(file_path, "Grades/#{file_name}")`)

## Installation: ##

1. Ensure Ruby is installed on your machine (preferably on mac or linux)

2. Generate an API access token for the proper Canvas environment

3. You may need to install a few ruby gems. They are all listed above.

4. Configure the additional variables in the top section of the script:

      - school_domain

      - auth_token: API access token

      - term_id: the SIS ID of the term to pull from

      - sftp_host

      - sftp_username

      - sftp_password

5. Editing report format

     - If you want to adjust the format for the report, you can do so by modifying these lines around line 100:

      -  ```  csv << ["Student Number", "Course Number", "Section Number", "Term", "Final Grade", "Final Approved", "Certificate Requirements Met", "Completion Date"] ```

     These are the column headers for the report. You will then need to adjust the lines around line 144 to adjust the values to match:

    - ``` csv << [sis_user_id, sis_user_id, sis_course_id, sis_section_id, "", $term_id, grade, "Final Approved",completion_date ] ```


6. In terminal, run `ruby grade_export.rb`


# Support
As always this is AS-IS and is not supported by Instructure! It is up to you and any kind Canvas Community Members to own, maintain, and troubleshoot any issues with this script.
