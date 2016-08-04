//Works as of 04/27/2016
/*
 * You can use this script to add some text to the login screen just below the
 * login button and other items on the screen.  There appears to be room for about
 * 3 lines of text, or so.
 *
 * Edit the variable added_text to contain the text you want to add to the screen.
 */

$(document).ready(function(){

  var added_text = 'Hello, this is some text. I really need this text to be long so I can see what it does when it gets to the end of the line and wraps. Also, what happens when the text is really long? Does it make the modal box taller?';
  var added_html_and_text = '<div style="clear:both"><p>' + added_text + '</p></div>';

  $('#login_form').append(added_html_and_text);


});
