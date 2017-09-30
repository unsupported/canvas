//This will wait until the element is rendered before running our code
function onElementRendered(selector, cb, _attempts) {
    var el = $(selector);
    _attempts = ++_attempts || 1;
    if (el.length) return cb(el);
    if (_attempts == 60) return;
    setTimeout(function() {
        onElementRendered(selector, cb, _attempts);
    }, 250);
};


//This code will pull the Canvas IDs for users and courses and change the link for the survey
// onElementRendered('a[href*="showSurvey.aspx', function(e) {
//     var userSISID = ENV.current_user_id;
//     var courseID = window.location.pathname.split('/')[2];
//     $('a[href*="showSurvey.aspx"]').attr('href', 'http://enterprise.principals.ca/Survey/showSurvey.aspx' + '?evalID=232&userID=' + userSISID + "&eelD=" + courseID);
// });

//When element is rendered it will run api call to fill the necessary variables so the survey link changes
onElementRendered('.reset_course_content_button', function(e) {
    $('.reset_course_content_button').hide();
});
