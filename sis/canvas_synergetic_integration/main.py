# =============================
# Canvas to Synergetic One-way Sync
# Unsupported 
# Contributed by Community
# =============================

import requests
import csv
import zipfile
import os
import pyodbc
import datetime
from contextlib import contextmanager
import logging, logging.handlers
from dataclasses import dataclass
from typing import List
from tempfile import TemporaryDirectory
from pathlib import Path
import argparse

logger = logging.getLogger('canvas_SI')

@dataclass
class SIS_Diffing_Parameter:
    type: type
    value: str
    description: str


diffing_params = {
    'diffing_drop_status':
    SIS_Diffing_Parameter(value='inactive', type=str,
                          description='''If diffing_drop_status is passed, this SIS import will use this status for enrollments that are
not included in the sis_batch. Defaults to ‘deleted’.
Allowed values:
deleted, completed, inactive'''),
    'diffing_data_set_identifier':
    SIS_Diffing_Parameter(value='canvas_syn_integration', type=str,
                          description='''If set on a CSV import, Canvas will attempt to optimize the SIS import by comparing this set of CSVs to 
the previous set that has the same data set identifier, and only applying the difference between the two'''),
    'diffing_user_remove_status':
    SIS_Diffing_Parameter(value='suspended', type=str,
                          description='''For users removed from one batch to the next one using the same diffing_data_set_identifier, set their
status to the value of this argument.'''),
    'change_threshold_percent':
    SIS_Diffing_Parameter(value=10, type=int,
                          description='If set with diffing, diffing will not be performed if the files are greater than the threshold as a percent.'),
}


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

        # Copy the column names into results.
        results = [self.result_columns[:]]
        for row in cur.fetchall():
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

class SI_Exception(Exception):
    pass

class SIS_ImportError(SI_Exception):
    def __init__(self, message, status_code, text):
            super().__init__(message)
            self.status_code = status_code
            self.text = text


def zipdir(path, ziph):
    '''
    Helper function for zipping the directory
    '''
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def post_data(base_url, header, filename, diffing_mode=False):
    '''
    Posts data to the canvas api endpoint. Returns identifier for import 
    '''

    extension = filename.suffix[1:]
    # Setup URL parameters
    url_params = {'import_type' : 'instructure_csv', 'extension': extension}

    if diffing_mode:
        for name, param in diffing_params.items():
            url_params[name] = param.value
 
    data = open(filename, 'rb').read()

    r = requests.post(base_url + "/sis_imports/", headers=header, params=url_params, data=data)

    # Rather than just log the output, I would like to inspect the r object and check the return code. If there is an error I want to log that. If there is no error... I might log the output as well, but at a INFO level?
    if r.status_code != 200:
        raise SIS_ImportError(status_code=r.status_code, text=r.text)
    r_json = r.json()
    logger.info(f"Import upload for {filename}, import id {r_json['id']}")
    return r_json['id']

def main(arg_strs):

    ap = argparse.ArgumentParser()
    for name, param in diffing_params.items():
        ap.add_argument('--'+name, type=param.type, help=param.description, default=param.value)

    args = ap.parse_args(args=arg_strs)

    diffing_params['diffing_data_set_identifier'].value = args.diffing_data_set_identifier
    diffing_params['change_threshold_percent'].value = args.change_threshold_percent
    diffing_params['diffing_drop_status'].value = args.diffing_drop_status
    diffing_params['diffing_user_remove_status'].value = args.diffing_user_remove_status

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
        

        SERVER = os.environ['SERVER']
        DATABASE = os.environ['DATABASE']
        USERNAME = os.environ['USERNAME']
        PASSWORD = os.environ['PASSWORD']
    except KeyError as e:
        logger.critical(f"missing required environment variable {e.args[0]}")
        raise SystemExit()

    conn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

    with db_connect(conn_string) as conn, TemporaryDirectory() as working_dir:
        try:
            go(conn, working_dir, base_url, header)
        except Exception as e:
            logger.exception("Unhandled exception while running")
            raise e



def go(conn, working_dir, base_url, header, zip=False):
 
    imports_started = []
    for view in views:
        with db_cursor(conn) as cur:
            csv_filename = (Path(working_dir) / view.name).with_suffix('.csv')
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(view.run(cur))
            if not zip:
                import_id = post_data(base_url=base_url, header=header, filename=csv_filename, diffing_mode=True)
                imports_started.append(import_id)

  
    if zip:
        # =============
        # ZIP Directory
        # =============
        zipf = zipfile.ZipFile('results.zip', 'w')
        zipdir(working_dir, zipf)
        zipf.close()

        # ===================
        # Post Data to Canvas
        # ===================
        import_id = post_data(base_url=base_url, header=header, filename='results.zip')
        imports_started.append(import_id)

    # TODO: Use GET /api/v1/accounts/:account_id/sis_imports/:id for each of the imports to track the status of the imports and log the outcome.
 

if __name__ == '__main__':
    import sys
    main(arg_strs=sys.argv[1:])

