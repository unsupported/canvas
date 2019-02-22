/*
 * student_remove_ignore_button.js
 * by: Danny Wahl dwahl@instructure.com
 * Working as of 10/25/2015
 * Removes the ignore (X) button on the
 * TO-DO list on the User Dashboard for
 * Students in the New UI.
 */

$(function(){

    // Verify that the path is /
    if(window.location.pathname == "/") {

        console.log("student_remove_ignore_button.js");

        // Check if the user has role "Student" in ANY course
        if($.inArray("student", ENV.current_user_roles) !== -1) {

            console.log("  User " + ENV.current_user_id + " has the role \"Student\".");
            console.log("  Ignore Buttons will be removed.");

            $(".to-do-list .IgnoreButton").remove();

        } else {

            console.log("  User " + ENV.current_user_id + " does not have the role \"Student\".");
            console.log("  Ignore Buttons will not be removed.");

        }
    }
});
