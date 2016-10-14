//This is not supported by Instructure
//Functional as of October 10, 2016

$(document).ready(function () {
    $('#menu a[href="http://help.instructure.com/"]').on('click', function() {
        function onElementRendered(selector, cb, _attempts) {
          var el = $(selector);
          _attempts = ++_attempts || 1;
          if (el.length) return cb(el);
          if (_attempts == 60) return;
          setTimeout(function() {
            onElementRendered(selector, cb, _attempts);
          }, 250);
        }

        onElementRendered('a[href="#create_ticket"]', function(el) {
            //Change text for "Report a Problem"
            //$('a[href="#create_ticket"]').html('Some New Text');
            
            /*
            //Hide if user isn't an admin or teacher
            if($.inArray('admin',ENV['current_user_roles']) == -1 &&  $.inArray('teacher',ENV['current_user_roles']) == -1) {
              $('a[href="#create_ticket"]').parent().hide();
            }
            */
        });
    });
});