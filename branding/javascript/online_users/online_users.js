/*
 * online_users.js
 * by: Danny Wahl dwahl@instructure.com
 * Working as of 03/21/2016
 * Adds an indicator to the People page of
 * a course if a user has been active in
 * the course in the last 5 minutes.
 */

$(function(){

    var path = window.location.pathname.split( '/' );

    //make sure the user is on a "people" page
    if((path[1] == "courses") && (path[3] == "users")) {

        console.log("canvas-online-users.js");

        //Time to show indicator (default 5 minutes [in millisecons])
        var timeout = 300000;

        //get the current time
        console.log("  Generating current time in millisecons...");
        var now = new Date();
        var nowMS = now.getTime();
        console.log("  Current time in MS is: " + nowMS);

        //get the domain
        var domain = window.location.hostname;
        //get the current course
        var courseID = Number(ENV.course.id);
        //get the activity report from API

        console.log("  Collecting user activity...");
        var usersActivity = [];
        var jsonURL = "https://" + domain + ":443/api/v1/courses/" + courseID + "/enrollments";
        var activity = $.getJSON( jsonURL, function( data ) {
            for(var i=0; i < data.length; i++) {
                var userID = data[i].user_id;
                console.log("  Current user is: " + userID);
                var lastActivity = new Date(data[i].last_activity_at);

                console.log("  Last activity is: " + lastActivity);
                console.log("  Converting to milliseconds...");
                var lastActivityMS = lastActivity.getTime();
                console.log("  Successfully converted...");
                usersActivity[userID] = lastActivityMS;
                console.log("  user " + userID + " done");
            }
        });
        activity.done(function(){
            console.log("  Successfully received all users and activity, parsing...");
            for (var id in usersActivity) {
                if(nowMS - usersActivity[id] < timeout) {
                    console.log("  User " + id + " active in course within 5 minutes, adding indicator.");
                    $("#user_" + id + " .avatar").css({"border-color": "#3a87ad", "box-shadow": "#0081bd"});
                    console.log("  Indicator added.");
                } else {
                    console.log("  User not active in course within 5 minutes, not adding indicator.");
                }
            }
            console.log("  Indicators have been added for all active users.");
        });
        activity.error(function(){
            console.log("  Error retrieving course activity logs, try again later.");
        });
    } else {
        console.log("  User is not on a 'People' page within a course, won't get activity logs.");
    }
});
