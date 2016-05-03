<?php
/**
 * This script will fetch the current final graes for all students in a specific course. 
 * In order for this to work, you need to be either a teacher in the course or an account 
 * admin.  Please take a moment to customize the variables in the top part of this script 
 * to fit your situation.  Specifically, adjust BASE_URL, ACCESS_TOKEN, and $course_id.
 *
 **/

// Variables you should adjust
define('BASE_URL',"https://<subdomain>.instructure.com/api/v1%s"); # Set this to your account's sub-domain or url.  This is the 
                                                                     # url you use to access canvas.  
                                                                     # The %s part is used to plug in the endpoints 
                                                                     # later in the script.

define('ACCESS_TOKEN', "<your_access_token>"); # Replace this with your user's access token

$course_id = <course_id>;  # not the sis_id but the canvas internal id

// End of settings that would be changed

$request_headers = array('Authorization: Bearer ' . ACCESS_TOKEN);


# First, get the list of students in the course
#
# Build the API endpoint for fetching the list of students
$students_endpoint = sprintf(BASE_URL,sprintf('/courses/%d/students', $course_id));

# Initiate cURL, adding the REQUEST_HEADERS to it for authentication
$ch = curl_init();

// Set headers
curl_setopt($ch,CURLOPT_HTTPHEADER,$request_headers);

// Set url
curl_setopt($ch, CURLOPT_URL,$students_endpoint);
// Tell cURL to return the results of the request. 
curl_setopt($ch,CURLOPT_RETURNTRANSFER,True);
//
# Execute the request
# Fetch the response, 
$student_list = curl_exec($ch);

$grades = False;
if(!$student_list){
  print 'error fetching student list';
}else{
  # Strip extra whitespace from the beginning and end then parse response into JSON
  $student_list = json_decode(trim($student_list));

  # Build the query parameters, creating a student_ids[]=<id> for each student id
  $submission_params = array('include[]=total_scores','grouped=1');
  foreach($student_list as $key=>$value){
    $submission_params[] = 'student_ids[]='.$value->id;
  }
  # implode the string, joining it with '&'
  $submission_params_string = implode('&',$submission_params);

  # Build a request url 
  $submissions_endpoint = sprintf(BASE_URL,sprintf('/courses/%d/students/submissions', $course_id));
  # add the query parameters to the url, and set the curl url destination
  curl_setopt($ch, CURLOPT_URL, $submissions_endpoint . '?' . $submission_params_string);

  # Fetch the response
  # Get the resutls
  $grades = curl_exec($ch);

  if(!$grades){
    print "problem fetching submissions\n";
  }else{
    # strip extra whitespace from the beginning and end
    $grades = trim($grades);
    # Load the response as JSON
    $grades = json_decode($grades);
  }
}

# Please close the curl handler
curl_close($ch);

// Do something with the $grades array, which now contains the grades
var_dump($grades);
