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
import datetime

now = datetime.datetime.now()

from contextlib import contextmanager

working_dir = './canvas/'

base_url = os.environ['base_url']
token = os.environ['TOKEN']
header = {'Authorization' : 'Bearer {token}'.format(token=token)}
payload = {'import_type' : 'instructure_csv', 'extension' : 'zip'}

SERVER = os.environ['SERVER']
DATABASE = os.environ['DATABASE']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

conn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'


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
          'login_id',
          'first_name',
          'last_name',
          'full_name',
          'sortable_name',
          'email',
	  'declared_user_type',
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
      cur.execute("SELECT * FROM uvCanvasCourses")
      canvas_accounts = cur.fetchall()

      results = [[
          'course_id',
          'short_name',
          'long_name',
          'account_id',
          'term_id',
          'status',
          'course_format'
      ]]

      for row in canvas_accounts:
          results.append(row)

      return results

def get_canvas_enrolments():
    '''
    Selects canvas enrolments from uvCanvasEnrollments
    '''
    with db_connect(conn_string) as cur:
      cur.execute("select * from uvCanvasEnrollments")
      canvas_accounts = cur.fetchall()

      results = [[
          'course_id',
	  'start_date',
	  'end_date',
          'user_id',
          'role',
          'section_id',
          'status'
        ]]

      for row in canvas_accounts:
          results.append(row)

      return results

def get_canvas_terms():
    '''
    Selects canvas enrolments from uvCanvasTerms
    '''
    with db_connect(conn_string) as cur:
      cur.execute("select * from uvCanvasTerms")
      canvas_terms = cur.fetchall()

      results = [[
          'term_id',
	  'name',
	  'status',
	  'start_date',
	  'end_date'
         
        ]]

      for row in canvas_terms:
          results.append(row)

      return results

def get_canvas_sections():
    '''
    Selects canvas enrolments from uvCanvasSections
    '''
    with db_connect(conn_string) as cur:
      cur.execute("select * from uvCanvasSections")
      canvas_sections = cur.fetchall()

      results = [[
          'section_id',
	  'course_id',
	  'name',
          'status'
         
        ]]

      for row in canvas_sections:
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

    print(now.strftime("%Y-%m-%d %H:%M:%S"), r.text)
    

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

    with open(working_dir + "terms.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(get_canvas_terms())

    with open(working_dir + "sections.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(get_canvas_sections())
  
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

