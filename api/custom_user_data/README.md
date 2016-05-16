##Custom User Data Automation

###Ruby

This script is used to add user defined custom data for user accounts. The script utilizes the Canvas API: https://canvas.instructure.com/doc/api/all_resources.html#method.custom_data.set_data

Modify lines 9-13 with data for your institution / Canvas instance. Do not modify anything else unless you're familiar with Ruby. If you encounter an error it most likely due to an error with your configuration (lines 9-13).

You will also need to modify the custom_data csv file.

1. Column 1 - Canvas user ID. Currently this script doesn't allow sis user ids.
2. Column 2 - This is the name of the data (i.e. phone number, address, etc...). This is labelled as "scope" in the api documentation.
3. Column 3 - Namespace. Canvas requires a namespace to prevent collisions between different applications using the same data id.
4. Column 4 - Data. Input the custom data in this column.


This is a relatively new script. There are known limitations:

1. The Custom Data Canvas API endpoint allows data to be uploaded in an array format. This script does not.
2. This script requires the Canvas user id, you cannot use the user sis id.
3. This script utilizes a beta API endpoint. It's possible Canvas may make changes that break this script.


###JavaScript

The JavaScript file inlcuded is used to display the custom data. Add this JS script to your Canvas instance and the added custom data field will display for each user you have added data.

1. Modify the data id "test_data" to your data
2. Change the namespace parameter
3. Remove alert and use the data.data parameter

I'm not aware of any limitation with the JS file.

Any ideas, errors, etc... submit an issue referencing this directory path (api > bulk_custom_user_data).