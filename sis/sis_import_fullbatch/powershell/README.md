#Full Batch SIS Imports PowerShell Example

This directory contains an example of using the sis_imports Canvas API to import a collection of Canvas formatted CSVs as a full batch import into Canvas. Full batch mode requires you to select a term that will be used to process the import. Sections, Courses and Enrollments not included in the uploaded CSV file(s) that were created with a prior import will be removed if they are associated with the selected term. Updates and new objects will be created in any term for any CSV file included in the .zip.

You can get additional information on the Canvas CSV import format and sis_import API at the links below.

* [How do I format CSV text files for uploading data into Canvas?](https://guides.instructure.com/m/4214/l/164118-how-do-i-format-csv-text-files-for-uploading-data-into-canvas)
* [SIS Import CSV Format Documentation](https://canvas.instructure.com/doc/api/file.sis_csv.html)
* [SIS Imports API](https://canvas.instructure.com/doc/api/sis_imports.html)

###Important Notes:

* You must compress all the CSV files into a .zip file in and place it into the $sourcePath.
* You must name the .zip file with the value used for the selected term's SIS ID in Canvas.
* The term must already exist in Canvas before attempting a full batch or it will fail.

###Pre-reqs to run this script:

* PowerShell 3 or higher

###You will need to alter the following variables during the setup process:

* $sourcePath:  Source path containing the CSV files to import. (Must end in a \\)
* $archivePath: . (Must end in a \\)
* $logPath:
* $token: [Canvas API access token](https://community.canvaslms.com/docs/DOC-3013) for a user with permission to import SIS  CSV files into Canvas.
* $domain: Full Canvas URL to your Canvas instance (without https://). Should look something like "school.instructure.com"
* $termMatchRegex: A [regular expression](http://ss64.com/ps/syntax-regex.html) that matches your term SIS ID format. The purpose of this check is to be sure that no .zips are attempted that do not match your SIS ID format.
* $checkTimeInterval: Number of seconds to delay before checking the status of the import that was started. The status is only checked once during the process.
