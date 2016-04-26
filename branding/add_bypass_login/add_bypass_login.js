//Working as of 04/19/2016
$(document).ready(function(){
  if(window.location.pathname.search('login')){
    //$('#login_forgot_password').text(internal_link_text);
    var new_link = $('<br/><a href="/login/canvas" title="Canvas Login">Canvas Login</a><br/><br/>');
    //$('#login_forgot_password').parent().parent().prepend(new_link);
    //$('label[for=pseudonym_session_remember_me]').after(new_link);
    $('label[for=pseudonym_session_remember_me]').after("<br/><br/>");
    $('#login_forgot_password').after(new_link);
  }
});
