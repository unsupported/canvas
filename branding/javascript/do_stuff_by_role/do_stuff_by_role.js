/*
 * do_stuff_by_role.js
 * by: Danny Wahl dwahl@instructure.com
 * Working as of 05/19/2016
 * Grabs the current user's actual roles
 * and compares them to a list of approved
 * roles to do some stuff.
 */

$(function(){

    // Array of role types to run the doStuff() function on
    // See https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
    // and the `type` parameter for more information
    var supportedRoles = ["TeacherEnrollment", "TaEnrollment"];

    console.log("canvas-do-stuff-by-role.js");
    console.log("  Supported roles are: " + supportedRoles);
    // Ensure that doStuff is only run once for the user
    var runOnce = false;
    console.log("  Script has not run yet for this user.");

    // Add desired functionality to the doStuff() function
    var doStuff = function() {
        console.log("  Executing script for user.");

        /*
         * ADD CUSTOM CODE HERE
         */


        // Notify that functionality has been executed
        runOnce = true;
        console.log("  Script has run for user.");
    }


    // Probably don't need to change anything below here
    // This gets the user's enrollments, compares them to supportedRoles[]
    // And executes if the script hasn't run yet

    var domain = window.location.hostname;
    var courseID = Number(ENV.course.id);
    var userID = Number(ENV.current_user_id);

    var jsonURL = "https://" + domain + ":443/api/v1/courses/" + courseID + "/enrollments?user_id=" + userID;

    var userRoles = [];

    console.log("  Getting user's current enrollments...");
    var getEnrollments = $.getJSON( jsonURL, function( data ) {
        for(var i=0; i < data.length; i++) {
            userRoles.push(data[i].type);

        }
    });
    getEnrollments.done(function(){
        console.log("  Enrollments gathered, checking for supported role...");
        for(var i=0; i < userRoles.length; i++) {
            if(runOnce == false) {
                for(var j=0; j < supportedRoles.length; j++) {
                    var supportedRole = supportedRoles.indexOf(userRoles[i]);
                    if((supportedRole != -1) && (RunOnce == false)) {
                        console.log("  Script has not run, supported role found, will run script.");
                        doStuff();
                    } else {
                        console.log("  Script has already run, or user does not have supported role.");
                        break;
                    }
                }
            } else {
                console.log("  Script has already run.");
                break;
            }
        }
    });
    getEnrollments.error(function(){
        console.log("  Error getting enrollments.");
    });
});
