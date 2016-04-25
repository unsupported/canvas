#!/bin/bash


############################################################################# 
############################################################################# 
############################################################################# 
#### Don't edit anything after here unless you know what you are doing
############################################################################# 
############################################################################# 
############################################################################# 


DIVIDER_START="#############################################################"
DIVIDER="-------------------------------------------------------------"

# Specify at least one argument
if [ $# -lt 1 ] ; then
  echo "You must specify at least 1 argument."
  echo "-e production|test|beta"
  exit 1
fi

override_sis_stickiness=false
add_sis_stickiness=false
clear_sis_stickiness=false
batch_mode=false
batch_mode_term_id=0
diffing_data_set_identifier=false
diffing_remaster_data_set=""
dry_run=false
keep_files=false
batch_mode=false
CONFIG_FILE_PATH=false

function usage(){
  cat <<EOF
  sis_script.sh $Options
$*
  Usage: sis_script.sh <[options]>
  Options:
    -e  (production|beta|test)  required, set the environment to .test,.beta, or production
    -s                          set override_sis_stickiness=true
    -f                          path to config file
    -S                          set add_sis_stickiness=true
    -k                          keep the SIS Files in the new folder
    -d  <id>                    set diffing_data_set_identifier to <id>
    -D                          set diffing_remaster_data_set=true
    --dry-run                   do a dry run
EOF
}

while getopts e:f:hb:sSk-:dD:r arg; do
  case $arg in
    e ) if [ $OPTARG != "production" ]; then domain=$domain.$OPTARG; fi;;
    f ) CONFIG_FILE_PATH=$OPTARG;; 
    s ) override_sis_stickiness=true;;
    S ) add_sis_stickiness=true;;
    b ) batch_mode=true
        batch_mode_term_id=$OPTARG;;
    c ) clear_sis_stickiness=true;;
    k ) keep_files=true;;
    d ) diffing_data_set_identifier=$OPTARG;;
    D ) diffing_remaster_data_set=true;;
    - ) LONG_OPTARG="${OPTARG#*=}"
        case $OPTARG in
            dry-run   ) dry_run=true                              ;;
            help      ) usage                                     ;;
            * )  usage " Long: >>>>>>>> invalid options (long) "  ;;
        esac ;;
    h ) usage
      exit 1
      ;;
    ? )
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))

echo 'loading config from $CONFIG_FILE_PATH'
chmod +x $CONFIG_FILE_PATH
. $CONFIG_FILE_PATH

# TODO Check for required config variables
# ACCESS_TOKEN
#echo $ACCESS_TOKEN
#echo $DOMAIN
#echo $CSV_FOLDER_NAME

CUR_DIR=$BASE_DIRECTORY
CSV_FOLDER="$BASE_DIRECTORY/$CSV_FOLDER_NAME"
#echo $CUR_DIR

echo $DIVIDER_START
echo "Starting the SIS import with the following variables:"
echo " domain:$DOMAIN"
echo " BASE_DIRECTORY:$BASE_DIRECTORY"
echo " CSV_FOLDER:$CSV_FOLDER"

# If $CUR_DIR is blank, then use the current directory
if [ "$CSV_FOLDER_NAME" = "" ]; then
  echo $DIVIDER 
  echo "CSV_FOLDER_NAME was blank, defaulting to the current folder as the source of CSV files"
  CSV_FOLDER="$CUR_DIR"
fi


# This creates a zip file with all the .csv files in the source folder
_date=`date "+%Y-%m-%d_%H-%M"`
# make a folder for this run
echo "creating a folder for this import at $CUR_DIR/archive/$_date/"
mkdir -p "$CUR_DIR/archive/$_date/"
touch "$CUR_DIR/archive/$_date/log.txt"
LOGFILE="$CUR_DIR/archive/$_date/log.txt"

function echo_time() {
  echo `date +'[%Y-%m-%d %H:%M] '` "$@"
}

function _log() {
  echo_time "$1" | tee ${LOGFILE} 
}

zip_file="$CUR_DIR/$_date.zip"

# If there are no CSV files to process, exit the script
# This is based on a snippet from http://www.ducea.com/2009/03/05/bash-tips-if-e-wildcard-file-check-too-many-arguments/
files=$(ls "$CSV_FOLDER/"*.csv 2> /dev/null | wc -l)

if [ $files -eq 0 ]
then
  _log $DIVIDER
  _log "There are no csv files in $CSV_FOLDER. I hereby declare that no SIS Import shall be executed."
  exit 1
else
  _log "$files CSV files exist: do something with them"
fi

_log "creating $zip_file with $CSV_FOLDER./*.csv"
zip -q "$zip_file" "$CSV_FOLDER/"*.csv

 $json

jsonval () {
  # -r makes the read function disable interpretation of backslashes and whatnot. It had
  # me stuck for several minutes until I found that
  read -r json_string

  local myresult=$(python <<END
import json, sys
from pprint import pprint
jstring = """$json_string"""
key_to_pull = """$1"""
try:
  json_obj = json.loads(jstring)
  #pprint(json_obj)
  res = json_obj.get(str(key_to_pull),key_to_pull+' missing, there might be errors')
  print res
except Exception,e:
  print e,jstring
END
)
  #_log ${temp##*|}
  echo $myresult
}

_log $DIVIDER
_log "Starting the import...now"

if [ "$dry_run" = true ]; then
  _log "dry run only, stopping here"
  exit 1
fi

params="extension=zip&import_type=instructure_csv"
if [ "$override_sis_stickiness" = true ]; then
  params+="&override_sis_stickiness=true"
  # These two are only usefull if override_sis_stickiness is set
  if [ "$add_sis_stickiness" = true ]; then
    params+="&add_sis_stickiness=true"
  fi
  if [ "$clear_sis_stickiness" = true ]; then
    params+="&clear_sis_stickiness=true"
  fi
fi
if [ "$batch_mode" = true ]; then
  params+="&batch_mode=true"
  params+="&batch_mode_term_id=sis_term_id:$batch_mode_term_id"
fi
if [ "$diffing_data_set_identifier" = true ]; then
  params+="&diffing_data_set_identifier=$diffing_data_set_identifier"
  # This is only usefull if diffing_data_set_identifier is true
  if [ "$diffing_remaster_data_set" = true ]; then
    params+="&diffing_remaster_data_set=true"
  fi
fi
echo "params: $params"
AUTH_HEADER="Authorization: Bearer $ACCESS_TOKEN"
json=`curl -s -F attachment=@"$zip_file" -F "$params" -H "$AUTH_HEADER" "https://$DOMAIN.instructure.com/api/v1/accounts/self/sis_imports"`

_log $DIVIDER
echo $json
id=$( echo $json | jsonval id )
_log "SIS Import ID: "  "$id"

# Do a check on the ID.  It should be a number, if it isn't then stop the script now
# before anything bad :) happens
if [ -z "${id##*[!0-9]*}" ]; then
  _log "Something was wrong with the initial sis import...stopping now"
  exit 1
else
  if [ "$keep_files" = false ] ; then
    _log "Initial import was successfull, moving $CSV_FOLDER/"*.csv to "$CUR_DIR/archive/$_date/"
    mv "$CSV_FOLDER/"*.csv "$CUR_DIR/archive/$_date/"
  else
    _log "Initial import was successfull, leaving $CSV_FOLDER/*.csv in place"
  fi
fi
workflow_state=$(echo $json | jsonval workflow_state) 
progress=$(echo $json | jsonval progress) 

#echo $workflow_state
check_url="https://$DOMAIN.instructure.com/api/v1/accounts/self/sis_imports/$id"
_log "checking status at $check_url"
while [[ $progress -lt 100 && $workflow_state != "imported" ]]; do
  sleep 3
  json=`curl -s -H "$AUTH_HEADER" $check_url`
  workflow_state=$(echo $json | jsonval workflow_state) 
  progress=$(echo $json | jsonval progress) 
  _log "$workflow_state, $progress%"
done

_log $DIVIDER
_log "Results are in"
_log "The final Workflow State for this import is \"$workflow_state\""
if [[ $workflow_state = "imported_with_errors" ]];
then
  _log "Here are the errors"
  errors=$(echo $json | jsonval errors) 
  if [ "$path_to_python_parser" = "" ]; then
    _log $json
  else
    _log $errors
  fi

fi
if [[ $workflow_state = "imported_with_messages" ]];
then
  _log "Here are the messages"
  messages=$(echo $json | jsonval processing_warnings) 
  # For some reason this is truncated when not using the python processor.  Why, I don't know.  let's just print
  # out the full $json for now
  if [ "$path_to_python_parser" = "" ]; then
    _log $json
  else
    _log "warning messages: $messages"
  fi
fi

# Move the zip file to the archive folder
_log $DIVIDER
_log "All done, now moving $zip_file to $CUR_DIR/archive/$_date/$_date.zip"
mv "$zip_file" "$CUR_DIR/archive/$_date/$_date.zip"
