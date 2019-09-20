#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pullexams_bycourse.py
#
# Usage: python3 pullexams_bycourse.py <environment> <semester_code>
#
# Outputs: CSV of exam info with course info to cross-reference
#
# Args: Requires a target (test or prod) and any amount of terms
#       Note that terms must match the SIS ID for term in Canvas
#       See: https://canvas.instructure.com/doc/api/enrollment_terms.html
#
# Outline: 1. Request and document all courses matching criteria specified
#          2. Request and document all quiz info for courses from 1
#          3. Check quiz due dates against current date to filter further
#          4. Write remaining available quizzes to file
#
# General advice: * Most replacement should happen between <>
#                 * When you see {} do not remove w/o removing matching .format
#                 * Careful changing things, infinite loops are possible
#
# Author: Brandon Poulliot
# 
# Works as of 9/20/19

# standard libraries
from datetime import datetime
import json
from os.path import join
from sys import argv, exit
import csv
import re

# non-standard libraries
import requests

###############################################################################
##############################   CHANGE THESE   ###############################
###############################################################################

# set datetime info -- change format to suit
print('Starting exam pull now {:%Y-%m-%dT%H:%M:%S}'.format(
      datetime.now()))

# set a regex expression to verify your terms passed in -- see examples
# also https://regexr.com/ can help building regex to match
# MUST UNCOMMENT THESE TO VERIFY TERMS ARGS PASSED IN

#term_regex = '^(SP|SU|FA)2[0-9]{3}$' # match format of SP2020 or FA2030
                                     # case sensitive -- thru 2999

#term_regex = '^2[0-9]{2}(1|4|7)$' # match 4-digit term starting w/ 2, middle
                                  # digits are 0-9, last digit is 1, 4, or 7

#term_regex = '^2[0-9]{3}\/(SP|SU|FA)$' # match year '/' term format thru 2999
                                       # e.g., 2020/FA or 2031/SU thru 2999

# Canvas and auth info
canvas_domain = '<domain>{}.instructure.com'
token = '<canvas_prod_token>'
test_token = '<canvas_test_token>'

# set the output path for quiz file
prod_out = '<production_output_path>'
test_out = '<test_output_path>'

# change the name of the quiz file to suit
quiz_fname = '<desired_quiz_filename>-{}.csv'
quiz_headers = 'course_name,course_code,quiz_name,unlock_date,due_date,lock_date\n'

# courses request parameters -- default: active w/ enrollments & not completed
account = 1                 # subaccount ID
per_page = 100              # results per page, most cases limit is 100
do_enrollments = 'true'     # exclude courses w/o enrollments
do_published = 'true'       # exclude unpublished courses
do_completed = 'false'      # exclude completed courses
do_term = 'sis_term_id:{}'  # search by semester -- use your SIS term ID
# if using, uncomment here and in params manifest (see line XXX)
#do_etype = ''        # teacher, student, ta, observer, or designer
#do_blueprint = ''    # t/f only include blueprint parents
#do_associated = ''   # t/f only include blueprint children
#do_teachers =        # int list of teacher user IDs to filter by
#do_subaccounts = ''  # int list of subaccount IDs to filter by
#do_state = ''        # created, claimed, available, completed, deleted, all
#do_search = ''       # partial course name, code, or full ID
#do_include = ''      # list of includes, see API docs
#do_sort = ''         # by course_name, sis_course_id, teacher, account_name
#do_order = ''        # sort 'asc' or 'desc' order
#do_filter = ''       # by course or teacher, see API docs


###############################################################################
##########################   DO NOT CHANGE THESE   ############################
###############################################################################

# separate the args
args = []
total_args = len(argv)

i = 1
while i < total_args:
  print('Argument {}: {}'.format(i, argv[i]))
  args.append(argv[i])
  i += 1

passed_args = len(args)

if passed_args < 2:
  print('''Not enough arguments supplied. \
           Syntax is: python3 pullexams_bycourse.py [prod|test] [2xxx].''')
  exit('invalid arguments')

# set environment variables based on first arg
if args[0] == 'prod':
  target = 'prod'
  env = ''
  out_path = prod_out
elif args[0] == 'test':
  target = 'test'
  env = '.test'
  token = test_token
  out_path = test_out
else:
  # will fail if no environment provided or not provided in correct order
  target = None
  print('Env arg invalid, exiting (should be prod/test), arg was: {}'.format(
         args[0]))
  exit('invalid argument')

# set new quiz file path based on env out path and filename supplied
quizf = join(out_path, quiz_fname)

# set request header info
headers = {'Authorization': 'Bearer {}'.format(token)}

# set endpoint info
base_domain = 'https://{}/api/v1/{}'.format(canvas_domain.format(env), '{}')
course_uri = base_domain.format('accounts/{}/courses')
quiz_uri = base_domain.format('courses/{}/quizzes')

# semesters check
terms = []
i = 1
while i < passed_args:
  terms.append(args[i])
  i += 1
print('Terms provided: {}'.format(terms))

for term in terms:

  # double-check quiz count
  iq = 0

  # verify that the terms provided are valid using regex
  # comment out if term_regex is not set above or utilized
  try:
    term_regex
  except NameError:
    print('Terms not being verified, proceeding...')
  else:
    verify_term = bool(re.match(term_regex, term))
    if not verify_term:
      print('Terms must be in {} format, please try again.'.format(term_regex))
      exit('invalid term format')
  
  # storage arrays
  courses_a = []  
  quiz_a = []
  quizzes_open = []

  # params manifest, ensure all params specified are uncommented here too!
  params = {
    'with_enrollments': do_enrollments,
    'published': do_published,
    'completed': do_completed,
    'enrollment_term_id': do_term.format(term)#,
    #'enrollment_type[]': do_etype,
    #'blueprint': do_blueprint,
    #'blueprint_associated': do_associated,
    #'by_teacher[]': do_teachers,
    #'by_subaccounts': do_subaccounts,
    #'state[]': do_state,
    #'search_term': do_search,
    #'include[]': do_include,
    #'sort': do_sort,
    #'order': do_order,
    #'search_by': do_filter
    }


  # get course IDs w/ criteria spec'd above
  # default: published, not completed, has enrollments
  pubcourse_r = requests.get(course_uri.format(account), headers=headers, 
                             params=params, timeout=10)
  # grab the json response
  pubcourses = pubcourse_r.json()

  # for each course, add it to the courses array
  ic = 0
  for course in pubcourses:
    courses_a.append(course)
    ic += 1
  # handle pagination, keep going until the last page
  while pubcourse_r.links['current']['url'] != pubcourse_r.links['last']['url']:  
    pubcourse_r = requests.get(pubcourse_r.links['next']['url'], headers=headers,
                               params=params, timeout=10)
    pubcourses = pubcourse_r.json()

    for course in pubcourses:
      courses_a.append(course)
      ic += 1
  print('Course count for {}: {}'.format(term, ic))
  print('Completed course manifest, pulling exams...')

  # send the biorobots to the roof, radiation limit 10s
  for course in courses_a:
    quiz_r =  requests.get(quiz_uri.format(course['id']), headers=headers, 
                           timeout=10)
    # get the response of quizzes in spec'd course
    quizzes = quiz_r.json()

    # add each quiz to the quizzes array
    for quiz in quizzes:
      quiz_a.append(quiz)

    while quiz_r.links['current']['url'] != quiz_r.links['last']['url']:
      quiz_r = requests.get(quiz_r.links['next']['url'], headers=headers, 
                            timeout=10)
      quizzes = quiz_r.json()
      for quiz in quizzes:
        quiz_a.append(quiz)

  # check due date, lock date, unlock date (availability), add to quiz array
  for quiz in quiz_a:
    name = quiz['title']
    due = quiz['due_at']
    lock = quiz['lock_at']
    unlock = quiz['unlock_at']
    if due is not None:
      due_date = datetime.strptime(due, '%Y-%m-%dT%H:%M:%SZ')
      dt_check = datetime.utcnow()
      available = due_date > dt_check
    elif unlock is not None:
      unlock_date = datetime.strptime(unlock, '%Y-%m-%dT%H:%M:%SZ')
      available = unlock_date < dt_check
    elif lock is not None:
      lock_date = datetime.strptime(lock, '%Y-%m-%dT%H:%M:%SZ')
      available = lock_date < dt_check
    elif lock is None and unlock is None and due is None:
      available = True
    else:
      available = False
    if available:
      row = '{},{},{}\n'.format(course['name'], course['sis_course_id'],
                                name, unlock, due, lock)

      quizzes_open.append(row)
      iq += 1
  print('Quizzes added to manifest for {}: {}'.format(term, iq))
  print('Completed exams manifest, writing to file...')

  # open the quiz file, write each row, close it up
  with open(quizf.format(term), 'w+') as qfile:
    qfile.write(quiz_headers)
    qrow = 0
    for row in quizzes_open:
      qfile.write(row)
      qrow += 1
    qfile.close()
  print('Quizzes Written to File: {}'.format(qrow))

