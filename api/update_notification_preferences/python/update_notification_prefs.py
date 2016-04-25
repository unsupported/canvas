#!/usr/bin/python

# working as of 4/19/2016

import csv, requests, time
from pprint import pprint

#############################
###### EDIT THIS STUFF ######
#############################

users_csv = 'users.csv' # name of file storing users/emails that will get notifications updated
notifications_csv = 'notifications.csv' # name of file storing your new notification settings
log_file = 'log.txt' # a log file. it will log things.
canvasDomain = 'myschool.instructure.com' # domain of your Canvas account
access_token = '<MY_TOKEN>' # your access token

#############################
## DON'T UPDATE CODE BELOW ##
#############################

baseUrl = 'https://%s/api/v1/users/self/communication_channels/email/' %(canvasDomain)
header = {'Authorization' : 'Bearer ' + access_token}
payload = {}

def main():

    # build payload dictionary
    build_notification_payload()

    # add time stamp to log file
    log_time = str(time.asctime(time.localtime(time.time())))
    write_to_log(log_time)   

    # do that updating thang
    update_prefs()
    
    # add time stamp to log file
    log_time = str(time.asctime(time.localtime(time.time())))
    write_to_log(log_time)   
    write_to_log("\n--DONE--\n\n")
   

def build_notification_payload():

    with open(notifications_csv, 'rU') as csvFile:
        csvReader = csv.reader(csvFile, delimiter = ',')
        csvReader.next() # Skip the header

        for row in csvReader:
            # row[0] = notification name, row[1] = notification frequency
            payload['notification_preferences[' + row[0] + '][frequency]'] = row[1]

def update_prefs():

    with open(users_csv, 'rU') as csvFile:
        csvReader = csv.reader(csvFile, delimiter = ',')
        csvReader.next() # skip the header

        for row in csvReader:
             user_id = row[0]
             cc = row[1]
             url = baseUrl + '%s/notification_preferences?as_user_id=sis_user_id:%s' %(cc,user_id)
             write_to_log(user_id + ": " + cc)
             r = requests.put(url, headers = header, data = payload)
             write_to_log(r.text)    

def write_to_log(message):

       with open(log_file, 'a') as log:
              log.write(message + "\n")
              pprint(message)



if __name__ == "__main__": main()

