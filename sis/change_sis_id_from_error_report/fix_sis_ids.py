import csv
import re
import string
#This is the name of the error report and is assumed to be in the same directory you are running the script in
#This value is used to write a new CSV
name_of_fixed_csv = ''
#This is the the sis_id you would like to change. Values accepted are account, term, course, section, group, group_category, user
type = ''

def main():
    ##Enter name of Error Report generated from Canvas
    error_report = ''
    total_val = read_csv(error_report)
    total_val.pop(0)
    final_test = []
    for item in total_val:
        try:
            final_test.append(get_info(item))
        except:
            print('Failed at {}'.format(item))
    #Write CSV
    with open(name_of_fixed_csv, 'w') as write_csv:
        csv_writer = csv.writer(write_csv)
        csv_writer.writerow(['old_id', 'new_id', 'type'])
        for data in final_test:
            with open(name_of_fixed_csv, 'a') as writ:
                csv_writ = csv.writer(writ)
                csv_writer.writerow([data[0], data[1], data[2]])

##Trying to use this with new, better code
def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""

#The read_csv function is reading the provisioning report with errors and saving it in an list
def read_csv(csv_name):
    with open(csv_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        message = []
        for line in csv_reader:
            message.append(line[2])
        return message

#The get_info function is reading the message list from the provisioning report with errors and extracting the sis_id's
def get_info(whole_string):
    while whole_string:
        try:
            curr_id = find_between_r(whole_string, 'SIS ID', 'has already')
            new_sis_id = find_between_r(whole_string, 'already claimed', '\'s user_id requested')
            val = [curr_id.strip(), new_sis_id.strip(), type]
            return val
        except:
            print('Error at string {stri}'.format(stri=split_string))

if __name__ == "__main__":
    main()