//Working as of 04/19/2016
$(document).ready(function(){
  if(window.location.pathname.indexOf('/login') >= 0){
    var c = $('#content');
    var iframe = '<iframe src="https://www.instructure.com" style="width:647px; height: 400px; margin: 75px auto; display: block;"></iframe>';
    $(iframe).appendTo(c);
  }
});
