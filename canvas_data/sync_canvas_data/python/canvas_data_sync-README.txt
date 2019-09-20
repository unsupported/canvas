Words of WARNING: This will likely download a LOT of data to the output 
directory. Carefully consider if you have space (hundreds of GB most likely) 
to spare for the sync files as well as newly re-written files (e.g., data was 
added to "module_progression_fact" table, but not enough to warrant a whole new
file) before they are removed.

# canvas_data_sync.py
# Author: Brandon Poulliot
# Purpose: Sync Canvas Data to a destination specified by the user
#      * Can provide most recent Canvas Data dump table files
#      * Can provide latest Canvas Data schema in file
#      * Can provide more information on Canvas Data dumps in CSV file
#
# Requirements: only non-standard library is REQUESTS
#
# Script Map:
#       1. Take in arguments and set API endpoint
#       2. Create base-64-encoded HMAC-256 signature
#       3. Download Canvas Data files
#         a. sync - downloads all tables not previously downloaded
#         b. latest - downloads only last 24 hours of tables
#         c. dump - writes a JSON file with extra dump information
#         d. schema - writes a JSON file with exhaustive schema information
#         e. byTable - COMING SOON!
#       4. Unzip (un-GZ?) the Canvas Data files (options 3a and 3b)
#       5. Remove the GZ archive files (options 3a and 3b)
#       6. Remove files not present in most recent sync (option 3a)
#
# Arguments: 
#      1. endpoint - required and positional, must come directly after
#                script invocation
#      2. -l (--limit) - optional, invoke using -l limit=#
#                Only used with dump option, specifies a limit to
#                the number of dump entries returned (default=50)
#      3. -a (--after) - optional, invoke using -a after=#
#                Only used with dump option, specifies the ID of
#                the dump to pull data after (i.e., ID > limit)
#      4. -m (--method) - optional, invoke using
#                -m (GET|DELETE|HEAD|OPTIONS|POST|PUT)
#                Future-proofing this script when more methods
#                become available (default=GET)
#
# Usage: Call from shell/cmd with preferred version and arguments
#    Examples:
#          1. python3 canvas_data_sync.py sync -m GET
#
#             Uses python 3.x + GET method to sync all Canvas Data
#
#          2. python canvas_data_sync.py dump -l limit=100 -a after=345
#
#             Uses default python to write a JSON file with all info on
#               the first 100 data dumps after dump ID 345
#         
# NOTES: + Working as of 9/20/19
#    + Left in "future-proofing" lines, do not uncomment until useful
#    + Flat file extensions don't matter -- change at will#    + Schema/dump extenstions - keep JSON for syntax marks in text editors
#    + Schema/dump extenstions - keep JSON for syntax marks in text editors
