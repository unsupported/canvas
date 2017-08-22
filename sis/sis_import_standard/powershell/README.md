#Standard SIS Imports PowerShell Example

This directory contains an example of using the sis_imports Canvas API to import a collection of Canvas formatted CSVs as a standard import into Canvas.

You can get additional information on the Canvas CSV import format and sis_import API at the links below.

* [How do I format CSV text files for uploading data into Canvas?](https://guides.instructure.com/m/4214/l/164118-how-do-i-format-csv-text-files-for-uploading-data-into-canvas)
* [SIS Import CSV Format Documentation](https://canvas.instructure.com/doc/api/file.sis_csv.html)
* [SIS Imports API](https://canvas.instructure.com/doc/api/sis_imports.html)

###Pre-reqs to run this script:

* PowerShell 3 or higher
* [PowerShell Community Extensions](https://github.com/Pscx/Pscx)

###You will need to alter the following variables during the setup process:

* $sourcePath:  Source path containing the CSV files to import. (Must end in a \\)
* $outputPath: Output path for the zip file that will be imported into Canvas. (Must end in a \\)
* $account_id: Root account ID of Canvas, usually the number 1. This can also be set to "self".
* $token: [Canvas API access token](https://community.canvaslms.com/docs/DOC-3013) for a user with permission to import SIS  CSV files into Canvas.
* $domain: Full Canvas URL to your Canvas instance (without https://). Should look something like "school.instructure.com"
* $outputZip: Name of the .zip file to create. For example "output.zip".
