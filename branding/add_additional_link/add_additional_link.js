/** Working as of 04/14/16
 * JQuery is the javascript library used in many places across canvas.
 *
 * Add an additional change password link to the login screen.
 **/


$(document).ready(function(){
  if(window.location.pathname.search('login')){
    var new_link = $('<br/><br/><a href="https://CHANGEME.com" title="Change Hover Title">Custom Display Title</a>');
    $('#login_forgot_password').parent().parent().append(new_link);
  }
});
