#Update Notification Preferences


##General Information

This script takes a list of users and updates their Canvas notification preferences as you like. Note that the notification preferences you can update through the API are more granular than what you see in the Canvas interface. New notification preferences are also being added regularly, so the "defaults" CSV file in this folder may be (probably is) out of date. They were current as of 9/18/2014.

##Using the Script

Before running this script, you'll need to create two CSV files. The first file will be for your users and have two columns:

* **user_id**: SIS ID of your user(s) 
* **email**: email address of the respective user(s) you would like to update notifications for

The second file will indicate what notification preferences you want changed and to what frequency. It has three columns:

* **notification**: name of the notification
* **frequency**: options are 'immediately', 'daily', 'weekly', and 'never'
* **category**: category that the notification belongs to

In the .py file iteself, you'll also want to update the values assigned in the first few lines of code, as indicated by the inline comments.