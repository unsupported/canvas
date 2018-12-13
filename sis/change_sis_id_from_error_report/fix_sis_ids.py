
import csv
import re
import string
#This is the name of the error report and is assumed to be in the same directory you are running the script in
error_report = ''
#This value is used to write a new CSV
name_of_fixed_csv = ''
#This is the the sis_id you would like to change. Values accepted are account, term, course, section, group, group_category, user
type = ''

#The read_csv function is reading the provisioning report with errors and saving it in an list
def read_csv():
    with open(error_report, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        message = []
        for line in csv_reader:
            message.append(line[2])
        return message

#The get_info function is reading the message list from the provisioning report with errors and extracting the sis_id's
def get_info(whole_string):
    while whole_string:
        try:
            split_string = re.split('\\SIS ID\\b', whole_string)[-1]
            split_string = whole_string.split('ID', 1)[1]
            temp_id = split_string.split()
            curr_id = temp_id[0]
            s = whole_string.replace("'s", '')
            temp_place_holder = s.split('claimed', 1)[1]
            temp_split = temp_place_holder.split()
            new_sis_id = temp_split[0]
            val = [curr_id, new_sis_id, type]
            return val

        except:
            print('Error at string {stri}'.format(stri=split_string))

total_val = read_csv()
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
