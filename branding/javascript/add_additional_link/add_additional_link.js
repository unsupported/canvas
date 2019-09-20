/*
  Working as of 03/5/19
  
  - Adds an additional link to the login screen.
  - Replace the "href", "title", and "Custom Display Title" text below

*/

$(document).ready(function () {
  if (window.location.pathname.search('login')) {
    var new_link = $('<br/><br/><a href="#" title="Change Hover Title">Custom Display Title</a>');
    $('#login_forgot_password').parent().parent().append(new_link);
  }
});