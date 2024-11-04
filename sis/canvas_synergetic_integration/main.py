# =============================
# Canvas to Synergetic One-way Sync
# Unsupported 
# Contributed by Community
# =============================

import requests
import csv
import zipfile
import os
import time
import pprint
import datetime
import shutil
import contextlib
import logging, logging.handlers
import dataclasses
import typing
import tempfile 
import pathlib 
import argparse

import pyodbc

logger = logging.getLogger('canvas_SI')

@dataclasses.dataclass
class SIS_Diffing_Parameter:
    value: str
    description: str
    type: typing.Optional[type] = None
    action: typing.Optional[str] = None


# Various URL parameters we can use in the Canvas SI Import API. This
# dictionary both documents which ones we are using, and the default value. 
# This script uses this as a global variable so that the main() method can
# setup options for the CLI, and store the chosen values back in after the CLI
# arguments are parsed. Then this dictionary is referred to when building up
# the URL parameters.
diffing_params = {
    'diffing_drop_status':
    SIS_Diffing_Parameter(value='inactive', type=str,
                          description='''If this script is in diffing mode then this script will pass diffing_drop_status as a URL parameter to the POST. Hence the CANVAS SIS import will use this status for enrollments that are
not included in the sis_batch. Defaults to ‘deleted’.
Allowed values:
deleted, completed, inactive'''),
    'diffing_data_set_identifier':
    SIS_Diffing_Parameter(value='canvas_syn_integration', type=str,
                          description='''If this scrip is running in diffing mode then diffing_data_set_identifier is used as a URL parameter in the POST to CANVAS. Hence Canvas will attempt to optimize the SIS import by comparing this set of CSVs to 
the previous set that has the same data set identifier, and only applying the difference between the two'''),
    'diffing_user_remove_status':
    SIS_Diffing_Parameter(value='suspended', type=str,
                          description='''If this script is running in diffing mode then this is used as a URL parameter in the POST to Canvas as a parameter. For users removed from one batch to the next one using the same diffing_data_set_identifier, set their
status to the value of this argument.'''),
    'change_threshold_percent':
    SIS_Diffing_Parameter(value=10, type=int,
                          description='If this script is running in diffing mode then this parameter is used as a URL parameter in the POST to Canvas as a parameter. Canvas diffing will not be performed if the files are greater than the threshold as a percent.'),
    'diffing-remaster-dataset':
    SIS_Diffing_Parameter(value=False, action='store_true',
                          description='''If changes are made to SIS-managed objects outside of the normal import process, it may be necessary to process a SIS import with the same data set identifier, but apply the entire import rather than applying just the diff. To enable this mode, set the diffing_remaster_data_set=true option when creating the import, and it will be applied without diffing. The next import for the same data set will still diff against that import.
                          When scheduling this script to run frequently you should not set this option.
                          ''')
}


@contextlib.contextmanager
def db_cursor(conn):
    '''
    Context manager for database cursor. Allows for
    complete cursor close on failure.
    '''
    
    cur = conn.cursor()
    yield cur
    cur.close()

@contextlib.contextmanager
def db_connect(conn_string):
    '''
    Context manager for database connection. Allows for
    complete connection close on failure.
    '''
    cnxn = pyodbc.connect(conn_string)
    yield cnxn
    cnxn.close()


@dataclasses.dataclass
class SIS_Datatype:
    name: str
    sql_view: str
    result_columns : typing.List[str]

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

class SIS_ImportStatusError(SI_Exception):
    def __init__(self, message, status_code, text):
            super().__init__(message)
            self.status_code = status_code
            self.text = text


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
        raise SIS_ImportError(status_code=r.status_code, message="SIS Import post failed", text=r.text)
    r_json = r.json()
    return r_json['id']

def get_status(base_url, header, import_id):
    '''
    Returns a dictionary showing the result of an import
    '''
    url = base_url + f"/sis_imports/{import_id}"
    resp = requests.get(url, headers=header)
    if resp.status_code != 200:
        raise SIS_ImportStatusError(status_code=resp.status_code, message="Failed to get status", text=resp.text)
    return resp.json()


def main(arg_strs):

    ap = argparse.ArgumentParser()
    views_help = ' '.join([i.name for i in views])
    ap.add_argument('views', nargs='*', help=f'Names of views to process in this execution. One of {views_help}')
    ap.add_argument('--diffing-mode', action='store_true', help='Instead of building a zip file of all the views upload individual synergetic views as CSV files and enable diffing mode. See Canvas documentation for more details on diffing mode')
    ap.add_argument('--no-upload', action='store_true', help='Do not POST to canvas, instead only pull the data from Synergetic and save the relevant csv or zip files and save them to the local directory')
    ap.add_argument('--output-dir', help='If running with --no-upload use the named directory instead of the current directory')
    
    # Add all of the diffing parameters to the scripts arguments/options.
    for name, param in diffing_params.items():
        kwargs = {
            'help': param.description,
            'default': param.value,
        }
        if param.action:
            kwargs['action'] = param.action
        if param.type:
            kwargs['type'] = param.type
        ap.add_argument('--'+name, **kwargs)

    args = ap.parse_args(args=arg_strs)

    diffing_params['change_threshold_percent'].value = args.change_threshold_percent
    diffing_params['diffing_drop_status'].value = args.diffing_drop_status
    diffing_params['diffing_user_remove_status'].value = args.diffing_user_remove_status

    logger.setLevel(logging.DEBUG)

    # Setup a logging to stderr
    se = logging.StreamHandler()
    se.setLevel(logging.INFO)
    logger.addHandler(se)

    # And logging to event viewer
    nt = logging.handlers.NTEventLogHandler(appname=__name__,)
    nt.setLevel(logging.DEBUG)
    nt.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(nt)

    # And logging to a local file. Might make this optional later one, when I setup some command line arguments.
    now = datetime.datetime.now()
    logging_filename = now.strftime('canvas_SI_%Y-%m.log')
    fl = logging.FileHandler(logging_filename, encoding='utf-8')
    fl.setLevel(logging.DEBUG)
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

    with db_connect(conn_string) as conn, tempfile.TemporaryDirectory() as working_dir_name:
        working_dir = pathlib.Path(working_dir_name)

        try:
            go(conn, working_dir, base_url, header, args.views, diffing_mode=args.diffing_mode, no_upload=args.no_upload)
        except SI_Exception as e:
            logger.exception(f"Unhandled SI exception while running: {e}")
        finally:

            # If the operator said to not upload, then we will copy all the generated files out of the temporary directory before they are deleted.
            if args.no_upload:
                if args.output_dir:
                    output_dir = pathlib.Path(args.output_dir)
                else:
                    output_dir = pathlib.Path(".")
                for filename in working_dir.iterdir():
                    shutil.copy(filename, output_dir)
                    


def go(conn, working_dir, base_url, header, arg_views, diffing_mode=False, no_upload=False):
 
    imports_started = []
    for view in views:

        # If the operator has named a view, but this view is not one of them, skip it.
        if len(arg_views) > 0 and view.name not in arg_views:
            continue

        with db_cursor(conn) as cur:
            csv_filename = (working_dir / view.name).with_suffix('.csv')
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(view.run(cur))
            
            # If in diffing mode upload these CSV files individually
            if diffing_mode and not no_upload:

                # But first, set the identifier to be specific to this view.
                diffing_params['diffing_data_set_identifier'].value = view.name

                import_id = post_data(base_url=base_url, header=header, filename=csv_filename, diffing_mode=True)
                logger.debug(f"SI Import for {view.name} started, import ID {import_id}")
                imports_started.append( (import_id, view.name) )

  
    # If we are not running in diffing mode create a zip file of all the CSV files created.
    if not diffing_mode:
        zip_filename = working_dir / 'results.zip'
        zipf = zipfile.ZipFile(zip_filename, 'w')
        
        # zip the directory
        for obj in working_dir.rglob('*.csv'):
            if obj.is_file():
                zipf.write(obj)
        zipf.close()
        if not no_upload:
            import_id = post_data(base_url=base_url, header=header, filename=zip_filename, diffing_mode=False)
            imports_started.append((import_id, 'results.zip'))


    # Get the status of the imports we have started. These may not be
    # immediately available, so the script will loop until we've successfully
    # retrieved those statuses. But not loop forever.
    pp = pprint.PrettyPrinter(sort_dicts=False)
    status_loop_count = 0
    while len(imports_started) > 0:
        status_loop_count += 1
        tmp_list_imports = imports_started[:]
        imports_started = []
        for import_id, view_name in tmp_list_imports:
            status = get_status(base_url=base_url, header=header, import_id=import_id)
            if status is None:
                imports_started.append( (import_id, view_name) )
                continue

            progress = status['progress']
            if progress != 100:
                logger.info(f"Import for {view_name} in progress, progress = {progress}")
                imports_started.append( (import_id, view_name) )
                continue

            workflow_state = status['workflow_state']
            logger.warning(f"Import for {view_name} finished, result: {workflow_state}")
            logger.debug(f"Import for {view_name} details: {pp.pformat(status)}")

        # Don't loop forever
        if status_loop_count > 1000:
            logger.warning(f"Import status has taken to long, quiting")
            break

        if len(imports_started) > 0:
            time.sleep(2)

 

if __name__ == '__main__':
    import sys
    main(arg_strs=sys.argv[1:])

