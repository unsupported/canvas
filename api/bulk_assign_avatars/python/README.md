# Bulk assign avatars to users

This script utilizes Canvas' API to assign an avatar to your users in bulk. It
makes the following assumptions:

1. You have all of the user images hosted somewhere that can be accessed publicly
2. Each user image is named according to the user it applies to, in a predictable format
3. More specifically, each user image is named according to each user's SIS ID (or `user_id`).This can be changed if necessary, but #2 will still apply regardless.

Also note that this script does not *upload* your images to Canvas in any way, it simply links each user to an image you're already hosting.

## Generate a Users CSV

Use the Provisioning Report to create a CSV file of all users in your account. You can find this report by going to your Account settings and selecting the "Reports" tab. Click "Configure" and in the dialogue that pops up just select "Users CSV" and then "Run Report".

## Update code in the script

Before you can run the script, you'll need to replace the code enclosed in angle brackets with your own data.

	myCsvFile = '<MY_CSV_FILE>' # Example: 'API_Testing/users_provisioning.csv'
	myLogFile = '<MY_LOG_FILE>' # Example: '/Users/ianm/Documents/Schools/IMU/log.txt'
	baseUrl = '<MY_BASE_URL>' # Example: 'https://ian.test.instructure.com/api/v1/users/'
	header = {'Authorization' : 'Bearer <MY_ACCESS_TOKEN>'}
	imagesUrl = '<MY_IMAGES_URL>' # Example: 'https://s3.amazonaws.com/canvas_ianm/avatars/'
	fileExt = '<FILE_EXTENSION>' # .png, .jpg, etc.

* `<MY_CSV_FILE>`: Filepath to the Users CSV you'll be importing
* `<MY_LOG_FILE>`: Filepath to a log file you'll output results to, if you'd like to do this
* `<MY_BASE_URL>`: From the example, replace "canvas" with the subdomain for your Canvas instance.
* `<MY_ACCESS_TOKEN>`: If you're unsure of how to generate this, review [this](https://canvas.instructure.com/doc/api/file.oauth.html) page of the Canvas API, under "Manual Token Generation".
* `<MY_IMAGES_URL`: URL of the folder containing all of your user images.
* `<FILE_EXTENSION>`: Format of your image files (.png, .jpg, etc.)
