# =============================
# Canvas to Synergetic One-way Sync
# Unsupported 
# Contributed by Community
# =============================

import requests
import json
import csv
import zipfile
import os
import time
import pyodbc
from contextlib import contextmanager

working_dir = './canvas/'

base_url = 'https://******.instructure.com/api/v1/accounts/self/'
token = os.environ['TOKEN']
header = {'Authorization' : 'Bearer {token}'.format(token=token)}
payload = {'import_type' : 'instructure_csv', 'extension' : 'zip'}

DB_URL = os.environ['DB_URL']
DB = os.environ['DB']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DRIVER = os.environ['DRIVER']

conn_string = 'DRIVER={DRIVER};SERVER={DB_URL};DATABASE={DB};UID={DB_USER};PWD={DB_PASSWORD}'.format(DRIVER=DRIVER, DB_URL=DB_URL, DB=DB, DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD)


@contextmanager
def db_connect(conn_string):
    '''
    Context manager for database connection. Allows for
    complete connection close on failure.
    '''
    cnxn = pyodbc.connect(conn_string)
    cur = cnxn.cursor()
    yield cur
    cnxn.close()

def get_canvas_accounts():
    '''
    Selects canvas accounts from uvCanvasAccounts
    '''
    with db_connect(conn_string) as cur:
      cur.execute("select * from uvCanvasAccounts ORDER BY parent_account_id")
      canvas_accounts = cur.fetchall()

      results = [[
          'account_id',
          'parent_account_id',
          'name',
          'status'
      ]]

      for row in canvas_accounts:
          results.append(row)

      return results

def get_canvas_users():
    '''
    Selects canvas users from uvCanvasUsers
    '''
    with db_connect(conn_string) as cur:
      cur.execute("select * from uvCanvasUsers")
      canvas_accounts = cur.fetchall()

      results = [[
          'user_id',
          'integration_id',
          'login_id',
          'password',
          'ssha_password',
          'first_name',
          'last_name',
          'full_name',
          'sortable_name',
          'short_name',
          'email',
          'status'
      ]]

      for row in canvas_accounts:
          results.append(row)

      return results

def get_canvas_courses():
    '''
    Selects canvas courses from uvCanvasCourses
    '''
    with db_connect(conn_string) as cur:
      cur.execute("select * from uvCanvasCourses")
      canvas_accounts = cur.fetchall()

      results = [[
          'course_id',
          'short_name',
          'long_name',
          'account_id',
          'term_id',
          'status',
          'integration_id',
          'start_date',
          'end_date',
          'course_format',
          'blueprint_course_id'
      ]]

      for row in canvas_accounts:
          results.append(row)

      return results

def get_canvas_enrolments():
    '''
    Selects canvas enrolments from uvCanvasEnrolments
    '''
    with db_connect(conn_string) as cur:
      cur.execute("select * from uvCanvasEnrolments")
      canvas_accounts = cur.fetchall()

      results = [[
          'course_id',
          'root_account',
          'user_id',
          'user_integration_id',
          'role',
          'role_id',
          'section_id',
          'status',
          'associated_user_id',
          'limit_section_priviledges'
        ]]

      for row in canvas_accounts:
          results.append(row)

      return results

def zipdir(path, ziph):
    '''
    Helper function for zipping the directory
    '''
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def post_data(base_url, header, payload):
    '''
    Posts data to the canvas api endpoint
    '''
    data = open('results.zip', 'rb').read()

    r = requests.post(base_url + "/sis_imports/", headers=header, params=payload, data=data)

    print(r.text)
    

if __name__ == '__main__':

    # ===========
    # Create CSVs
    # ===========
    with open(working_dir + "accounts.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(get_canvas_accounts())

    with open(working_dir + "users.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(get_canvas_users())

    with open(working_dir + "courses.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(get_canvas_courses())

    with open(working_dir + "enrolments.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(get_canvas_enrolments())

    # =============
    # ZIP Directory
    # =============
    zipf = zipfile.ZipFile('results.zip', 'w')
    zipdir(working_dir, zipf)
    zipf.close()

    # ===================
    # Post Data to Canvas
    # ===================
    post_data(base_url, header, payload)