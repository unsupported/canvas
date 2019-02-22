/*
 * enroll_in_ta_sections_only.js
 * by: Danny Wahl dwahl@instructure.com
 * Working as of 10/26/2015
 * By default TAs can enroll users into a sections
 * that the TA themselves are not enrolled into
 * This script checks the section enrollments of
 * the current user and removes sections that they
 * are not enrolled in from the "Add People" dialog
 */

$(function(){

    // Verify that the path is /courses/##/users
    var path = window.location.pathname.split( '/' );

    if((path[1] == "courses") && (path[3] == "users")) {

        console.log("enroll_in_ta_sections_only.js");

        // Don't disable for admin role.
        if($.inArray("admin", ENV.current_user_roles) == -1) {

            console.log("  User " + ENV.current_user_id + " does not have the role \"Admin\".");
            console.log("  Sections will be filtered.");

            $(document.body).on('click', '#addUsers', function() {

                //Disable the select while we verify
                console.log("  Disabling the section dropdown menu while enrollments are checked.");

                $("#course_section_id").prop("disabled", true);

                var domain = window.location.hostname;
                var currentCourse = ENV.course.id;
                var userID = ENV.current_user_id;
                var sections = [];
                var jsonURL = "https://" + domain + ":443/api/v1/courses/" + currentCourse + "/enrollments?user_id=" + userID + "&type=TaEnrollment";

                console.log("  Checking course enrollments.");

                var enrollments = $.getJSON( jsonURL, function( data ) {
                    for(var i=0; i < data.length; i++) {
                        sections.push(data[i].course_section_id);
                    }
                });

                enrollments.done(function(){

                    var courseSections = document.getElementById('course_section_id');
                    var totalSections = courseSections.options.length;
                    var removeSections = totalSections - sections.length;

                    console.log("  There are " + totalSections + " sections in course " + currentCourse + ".");
                    console.log("  User " + userID + " is a TA in " + sections.length + " sections.");
                    console.log("  User " + userID + "'s sections are: ");
                    console.log("  " + sections);
                    console.log("  " + removeSections + " section(s) will be removed.");

                    var section;
                    var optval = {};
                    var newOpts = "";
                    for(section of sections) {
                        optval = $("#course_section_id option[value='" + section + "']").text();
                        newOpts += "<option value=\"" + section + "\">" + optval + "</option>";
                    }

                    // Replace the old list of options with the user's list
                    $("#course_section_id").html(newOpts);

                    console.log("  " + removeSections + " section(s) have been removed.");

                    // Enable the select on complete
                    console.log("  Enabling section dropdown menu.");

                    // Options removed, re-enable form
                    $( "#course_section_id" ).prop( "disabled", false );
                });

                enrollments.fail(function() {
                    console.log("JSON error.");

                    //Enable the select due to error
                    console.log("  Enabling section dropdown menu.");

                    // Errored out, re-enable form
                    $( "#course_section_id" ).prop( "disabled", false );
                });

            });

        } else {
            console.log("  User " + ENV.current_user_id + " has the role \"Admin\".");
            console.log("  Sections will not be filtered.");
        }

    }

});
