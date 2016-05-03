//DEPRECATED AS OF 04/19/2016

/*
* This script appends information to the warning box displayed
*  when an HTTP:// external link is used for a module item in Canvas.
*
*  Note: To replace the content instead of appending change the .append to .html
*/
$(document).ready(function(){
  $('#insecure_content_msg.alert.alert-error').append('<p>Put your html here</p>')
});
