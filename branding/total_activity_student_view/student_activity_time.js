/*working as of July 26th, 2017*/
//Script to add the total activity time for the course a student is on

$(document).ready(function() {
  function convertSeconds(totalSeconds) {
    totalSeconds = Number(totalSeconds);

    let d = Math.floor(totalSeconds / 86400);
    let h = Math.floor(totalSeconds % 86400 / 3600);
    let m = Math.floor(totalSeconds % 86400 % 3600 / 60);
    let s = Math.floor(totalSeconds % 86400 % 3600 % 60);

    return (' ' + d).slice(d.length) + ' day(s) ' + ('0' + h).slice(-2) + ":" + ('0' + m).slice(-2) + ":" + ('0' + s).slice(-2);
  }

  if (window.location.pathname.indexOf('courses') > -1 && $.inArray('student', ENV.current_user_roles) > -1) {
    let userId = ENV.current_user_id;
    let courseId = ENV.context_asset_string.split('_')[1];
    let jsonUrl = `https://${window.location.hostname}/api/v1/users/${userId}/enrollments`;
    let time = "";

    $.getJSON(jsonUrl, (data) => {
      let currentCourse = data.filter((course) => {
        return course.course_id == courseId;
      });
      time = currentCourse[0].total_activity_time;
      time = convertSeconds(time);
      $('#right-side').prepend("<div class='events_list time_active'><h2>Time Activity</h2></div>");
      $(".events_list.time_active").append(time + " (hrs/mins/secs)");
    });

  }

});
