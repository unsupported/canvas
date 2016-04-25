Line by Line CSV Importer
--------------------------

If you ever need to import a Canvas CSV file one line at a time this script could be useful.  

NOTE: This script uses two 3rd party python modules: requests and clintui
Use pip to install them like this

  pip install requests clint

Edit the file, setting the DOMAIN and ACCESS_TOKEN.

Run the script like this:

  ./import_sis_csv_line_by_line.py path/to/csv/file.csv
