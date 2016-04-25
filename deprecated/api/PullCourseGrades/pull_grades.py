# This script is only a draft
import requests
import json
import pprint

# API reference https://canvas.instructure.com/doc/api/submissions.html

BASE_URL = "https://school.instructure.com/api/v1%s"
access_token = 'token_here'
course_id = 'change_me'  # not the sis_id but the canvas internal id

REQUEST_HEADERS = {'Authorization':'Bearer %s' % access_token}

# First, get the list of students in the course

students_endpoint = BASE_URL % '/courses/%s/students' % (course_id)

# Create a request, adding the REQUEST_HEADERS to it for authentication
not_done = True
students = []
url = students_endpoint
while not_done:
  student_request = requests.get(url,headers=REQUEST_HEADERS)
  students+=student_request.json()
  if 'next' in student_request.links.keys():
    url = student.request.links['next']['href']
  else:
    not_done = False

print 'done gettign students',len(students),'students'
# Load the response as JSON
response_data = student_request.json()

# Exit if there were no students in the returned data
if not response_data:
  print 'Sorry, there were no students registered in the course.'
  exit(0)

# Loop through the students, populating the student_ids list with their canvas ids
student_ids = [s['id'] for s in response_data]


# Build the endpoint for requesting submissions
submissions_endpoint = BASE_URL % '/courses/%s/students/submissions' % (course_id)

# Build the GET request parameters that are needed to fetch the submissions along with the
# total scores (grades)
submission_params = {'include[]':'total_scores','grouped':1}
submission_params['student_ids[]'] = student_ids

#submission_params = urllib.urlencode(submission_params)


# Build a request, adding the REQUEST_HEADERS to it for authentication
req = requests.get(submissions_endpoint, params=submission_params, headers=REQUEST_HEADERS)

# Load the response as JSON
grades = req.json()

pprint.pprint(grades)
