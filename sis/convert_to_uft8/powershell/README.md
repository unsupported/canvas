#PowerShell Example To Convert CSV Files to UTF8 Encoding

This directory contains an example of a script that converts CSV files into UTF8 encoded text files. UTF8 is the required encoding method for CSV to be imported.

You can get additional information on the Canvas CSV import format and sis_import API at the links below.

* [How do I format CSV text files for uploading data into Canvas?](https://guides.instructure.com/m/4214/l/164118-how-do-i-format-csv-text-files-for-uploading-data-into-canvas)
* [SIS Import CSV Format Documentation](https://canvas.instructure.com/doc/api/file.sis_csv.html)
* [SIS Imports API](https://canvas.instructure.com/doc/api/sis_imports.html)

###Pre-reqs to run this script:

* PowerShell

###You will need to alter the following variables during the setup process:

* $path_to_csv_input_folder: Full path to the location of the CSV files that need to be converted to UTF8 encoding. (Must end in \\)
* $path_to_csv_output_folder: Full path to the location UTF8 encoded files should be saved. (Must end in \\)
