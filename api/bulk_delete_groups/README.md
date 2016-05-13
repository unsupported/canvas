# Bulk Delete Groups

This script is for deleting groups that were created through migrated content in course shells. As there is no
SIS ID tied to each group, you will need to create a CSV mapping file (see example) with one column containing the `canvas_group_id` (you can find this from a provisioning report).

To run the script, first you will need to plug in the variables (see script file). Once that is populated,
run the command `ruby bulk_delete_groups.rb`. Each response will be outputted to the console. 
