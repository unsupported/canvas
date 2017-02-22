$(document).ready(function() {
    var adminOnly = true; // change this if you don't want admins to see the options either.

    //The function below checks to see that an element has rendered. When called
    //the function will look for a particular selector. Do not remove.
    function onElementRendered(selector, cb, _attempts) {
        var el = $(selector);
        _attempts = ++_attempts || 1;
        if (el.length) return cb(el);
        if (_attempts == 60) return;
        setTimeout(function() {
            onElementRendered(selector, cb, _attempts);
        }, 250);
    }

    onElementRendered('#addUsers', function() {
        $('#addUsers').on('click', function() {

            if (adminOnly) {
                if (window.location.pathname.indexOf('courses') > -1 && ENV.current_user_roles.indexOf('admin') == -1) {
                    //Line below will hide the "Login ID" on the "Add People" screen on the people page within a course
                    // $('[for="peoplesearch_radio_unique_id"]').hide();
                    //Line below will change the test for "Login ID" on the "Add People" screen on the people page within a course
                    $('[for="peoplesearch_radio_unique_id"] span:nth-child(2) span:nth-child(2)').text('text you want');
                    //Line below will remove the student in the dropdown for "Add People" on the people page in Canvas
                    $('[for="peoplesearch_select_role"] option[value=3]').remove(); // if you want to change which role is removed change the "value=3"
                }
            } else if (window.location.pathname.indexOf('courses') > -1) {
                //Line below will hide the "Login ID" on the "Add People" screen on the people page within a course
                // $('[for="peoplesearch_radio_unique_id"]').hide();
                //Line below will change the test for "Login ID" on the "Add People" screen on the people page within a course
                $('[for="peoplesearch_radio_unique_id"] span:nth-child(2) span:nth-child(2)').text('text you want');
                //Line below will remove the student in the dropdown for "Add People" on the people page in Canvas
                $('[for="peoplesearch_select_role"] option[value=3]').remove();
            }
        });

    });
});
