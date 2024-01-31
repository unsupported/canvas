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
from contextlib import contextmanager
import logging, logging.handlers
from dataclasses import dataclass
from typing import List
from tempfile import TemporaryDirectory
from pathlib import Path

logger = logging.getLogger('canvas_SI')


@contextmanager
def db_cursor(conn):
    '''
    Context manager for database cursor. Allows for
    complete cursor close on failure.
    '''
    
    cur = conn.cursor()
    yield cur
    cur.close()

@contextmanager
def db_connect(conn_string):
    '''
    Context manager for database connection. Allows for
    complete connection close on failure.
    '''
    cnxn = pyodbc.connect(conn_string)
    yield cnxn
    cnxn.close()


@dataclass
class SIS_Datatype:
    name: str
    sql_view: str
    result_columns : List[str]

    def run(self, cur):
        cur.execute(self.sql_view)

        results = self.results_columns
        for row in cur.fetch():
            results.append(row)
        return results

views = [
    SIS_Datatype(
        name="canvas_accounts",
        sql_view="select * from uvCanvasAccounts ORDER BY parent_account_id", 
        result_columns = [
            'account_id',
            'parent_account_id',
            'name',
            'status',
        ]
    ),
    SIS_Datatype(
        name="canvas_users",
        sql_view="select * from uvCanvasUsers", 
        result_columns = [
            'user_id',
            'login_id',
            'first_name',
            'last_name',
            'full_name',
            'sortable_name',
            'email',
            'declared_user_type',
            'status',
        ]
    ),
    SIS_Datatype(
        name="canvas_courses",
        sql_view="SELECT * FROM uvCanvasCourses", 
        result_columns = [
            'course_id',
            'short_name',
            'long_name',
            'account_id',
            'term_id',
            'status',
            'course_format'
        ]
    ),

    SIS_Datatype(
        name="canvas_enrolments",
        sql_view="select * from uvCanvasEnrollments", 
        result_columns = [
            'course_id',
            'start_date',
            'end_date',
            'user_id',
            'role',
            'section_id',
            'status'
        ]
    ),  

    SIS_Datatype(
        name="canvas_terms",
        sql_view="select * from uvCanvasTerms", 
        result_columns = [
        'term_id',
        'name',
        'status',
        'start_date',
        'end_date'
        ]
    ),
 
    SIS_Datatype(
        name="canvas_sections",
        sql_view="select * from uvCanvasSections", 
        result_columns = [
            'section_id',
            'course_id',
            'name',
            'status'
        ]
    ),

]

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

    logger.info(r.text)
    

def main():

    logger.setLevel(logging.INFO)

    # Setup a logging to stderr
    se = logging.StreamHandler()
    se.setLevel(logging.WARNING)
    logger.addHandler(se)

    # And logging to event viewer
    nt = logging.handlers.NTEventLogHandler(appname=__name__,)
    nt.setLevel(logging.INFO)
    nt.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(nt)

    # And logging to a local file. Might make this optional later one, when I setup some command line arguments.
    now = datetime.datetime.now()
    logging_filename = now.strftime('canvas_SI_%Y-%m.log')
    fl = logging.FileHandler(logging_filename, encoding='utf-8')
    fl.setLevel(logging.INFO)
    fl.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    logger.addHandler(fl)

    try:
        base_url = os.environ['base_url']
        token = os.environ['TOKEN']
        header = {'Authorization' : 'Bearer {token}'.format(token=token)}
        payload = {'import_type' : 'instructure_csv', 'extension' : 'zip'}

        SERVER = os.environ['SERVER']
        DATABASE = os.environ['DATABASE']
        USERNAME = os.environ['USERNAME']
        PASSWORD = os.environ['PASSWORD']
    except KeyError as e:
        logger.exception("missing required environment variable")
        raise SystemExit()

    conn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

    with db_connect(conn_string) as conn, TemporaryDirectory() as working_dir:
        try:
            go(conn, working_dir, base_url, header, payload)
        except Exception as e:
            logger.exception("Unhandled exception while running")
            raise e



def go(conn, working_dir, base_url, header, payload):
 
    for view in views:
        with db_cursor(conn) as cur:
            csv_filename = (Path(working_dir) / view.name).with_suffix('.csv')
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(view.run(cur))

  
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

if __name__ == '__main__':
    main()

