#!/usr/bin/python

# works as of 4/19/2016

import csv, requests, time
from pprint import pprint

#############################
###### EDIT THIS STUFF ######
#############################

access_token = '<MY_TOKEN>' # your access token
modules_csv = 'modules.csv' # name of file storing module names
log_file = 'log.txt' # a log file. it will log things
baseUrl = 'https://myschool.instructure.com/api/v1/courses/' # change to domain of your Canvas account
header = {'Authorization' : 'Bearer ' + access_token}
payload = {}

##############################################################################
## ONLY update the code below if you are experimenting with other API calls ##
##############################################################################

def main():

    # add time stamp to log file
    log_time = str(time.asctime(time.localtime(time.time())))
    write_to_log(log_time)   

    # do that updating thang
    create_modules()
    
    # add time stamp to log file
    log_time = str(time.asctime(time.localtime(time.time())))
    write_to_log(log_time)   
    write_to_log("\n--DONE--\n\n")
   

def create_modules():

    with open(modules_csv, 'rU') as csvFile:
        csvReader = csv.reader(csvFile, delimiter = ',')
        csvReader.next() # skip the header

        for row in csvReader:
             course_id = row[0]
             title = row[1]
             url = baseUrl + '%s/modules?module[name]=%s' %(course_id,title)
             write_to_log(course_id + title)
             r = requests.post(url, headers = header, data = payload)
             write_to_log(r.text)    

def write_to_log(message):

       with open(log_file, 'a') as log:
              log.write(message + "\n")
              pprint(message)



if __name__ == "__main__": main()

