

# Import the following modules
import csv
import requests
import os

# -----------------------------Edit These Variables---------------------------------#

# Set api key to environmental variable "api_key" using export api_key='<< API KEY >>'
#api_key = os.environ['api_key']

api_key = ''
# Set URL to the environment you would like to create courses in. Make sure you have the last "/" on the end.
url = 'https://schoolname.instructure.com/api/v1/'
header = {'Authorization': 'Bearer ' + api_key}

# Enter File location here. It is assumed to be in the same directory you are in
file_location = ''






#Create sandbox will create a user and call the create_course function.
def create_sandbox(first_name, last_name, email):
    full_name = first_name + " " + last_name
    payload = { "user[name]": full_name, "pseudonym[unique_id]": email }
    r = requests.post(url + 'accounts/self/users', headers=header, data=payload)

    #If api call returns a 200,
    if r.ok:
        info = r.json()
        canvas_id = info['id']
        print('#--------------------------------------------#')
        print('Successfully created {name}\'s user'.format(name=full_name))
        #Create course function
        create_course(full_name, canvas_id)
    else:
        print('Failed to create {0} {1}\'s sandbox course. Response returned is {2}. Please check the create_sandbox function.'.format(first_name, last_name, r.status_code))
        pass




def create_course(course_name, user_canvas_id):
    payload = {"course[name]": course_name + 'Sandbox Course', "course[sis_course_id]": course_name + 'SIS_ID'}

    r = requests.post(url + 'accounts/self/courses', headers=header, data=payload)
    if r.ok:
        info = r.json()
        course_id = info['id']
        print('Successfully created a course for {name}'.format(name=course_name))

        enroll_user(user_canvas_id, course_id)
    else:
        print('Failed to create course with code {c}. Please check the create_course function and the corresponding csv with the values {coursename}, {course_sisid}, {user_canvasid}'.format(c=r.status_code, coursename=course_name, course_sisid=course_sis_id, user_canvasid=user_canvas_id))
        pass

def enroll_user(user_id, course_id):
    payload = {"enrollment[user_id]": user_id, "enrollment[type]": "TeacherEnrollment", "enrollment[enrollment_state]": "active"}
    r = requests.post(url + '/courses/{}/enrollments'.format(course_id), headers=header, data=payload)
    if r.ok:
        print('Successfully enrolled user')
        print('#--------------------------------------------#')
    else:
        print('Enrollment failed for the user {user}. Skipping.'.format(user=user_id))
        pass



with open(file_location, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
        create_sandbox(line[0], line[1], line[2])
