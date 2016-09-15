#Creating a Canvas Users.csv from Active Directory PowerShell Example

This directory contains an example script that shows how to build a Canvas users.csv using data from Active Directory.

You can get additional information on the Canvas CSV import format and sis_import API at the links below.

* [How do I format CSV text files for uploading data into Canvas?](https://guides.instructure.com/m/4214/l/164118-how-do-i-format-csv-text-files-for-uploading-data-into-canvas)
* [SIS Import CSV Format Documentation](https://canvas.instructure.com/doc/api/file.sis_csv.html)
* [SIS Imports API](https://canvas.instructure.com/doc/api/sis_imports.html)

###Important Notes:

* This script does NOT import the file. It only creates the file.
* All information for the user.csv file must be in your Active Directory.
* If you would like to use different values for different user types you will need to make multiple copies of the script with different ADSearchBase or ADSearchFilter to limit the users in each script.

###Pre-reqs to run this script:

* PowerShell 3 or higher
* AD Admin Tools

###You will need to alter the following variables during the setup process:

* $ADSearchBase: The LDAP Base from which to pull all users. Ex: ou=school1,dc=school,dc=local
* $ADSearchFilter: The LDAP search filter to use. Use "\*" for all users.
* $outputFile: Full path to the output file. Ex: e:\\scripts\\users.csv
* FieldMap: Map the AD attribute to the CSV export file column ("canvas_header" = "AD_attribute_name")
* $AppendTo: Append the various static strings to the end of each value in the specified column ("canvas_header" = "string_you_want_to_append"). Leave hash empty if you do not want to append to any columns.
* $PrependTo: Prepend the various static strings to the beginning of each value in the specified column ("canvas_header" = "string_you_want_to_append"). Leave hash empty if you do not want to prepend to any columns.
* $StaticFieldMap: Add a static value to the export file column. Leave hash blank if you do not want to use any static values for any columns.

Support
======

This is an unsupported, community-created project. Keep that in mind.
Instructure won't be able to help you fix or debug this. That said, the
community will hopefully help support and keep both the script and this
documentation up-to-date.

Good luck!
