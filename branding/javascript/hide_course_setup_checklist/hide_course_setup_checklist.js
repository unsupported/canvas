// Working as of June 17, 2016
// Hides the Course Setup Checklist Button

$(document).ready(function(){
  if(location.pathname.match(/^\/courses\/\d+\/?$/i)){
    $('a:contains("Course Setup Checklist")').remove();
  }
});
