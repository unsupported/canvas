/*
 * grades_on_profile.js
 * by: Danny Wahl danny@instructure.com
 * Working as of 03/28/2016
 * Adds a link to the user's grades page
 * on their profile page and account profile.
 */

$(function(){
    console.log("grades_on_profile.js");
    console.log("  Getting current path...");
    var path = window.location.pathname.split( '/' );
    var makeLink = function(id, un) {
        var icon = '<img src="https://du11hjcvx0uqb.cloudfront.net/dist/images/grading_icon-16e9e323ad.png" alt="Grading icon 16e9e323ad">';
        console.log("  Building link.");
        var link = '<a href="/users/' + id + '/grades" class="btn button-sidebar-wide">' + icon + ' Grades for ' + un + '</a>';
        $("#right-side > div").prepend(link);
        console.log("  Link added.");
    }

    // Check if the path is /accounts/n/users/id
    if((path[1] == "accounts") && (path[3] == "users")) {
        console.log("  Adding grades link to " + window.location.pathname);
        var userID = path[4];
        console.log("  UserID is " + userID);
        var name = document.title;
        console.log("  User name is " + name);
        console.log(  "  adding link...");
        makeLink(userID, name);
        console.log("  Grades link has been added.");
    // Check if the path is /profile
    } else if(path[1] == "profile") {
        console.log("  Adding grades link to " + window.location.pathname);
        var userID = ENV.current_user_id;
        console.log("  UserID is " + userID);
        var name = ENV.PROFILE.name;
        console.log("  User name is " + name);
        console.log(  "  adding link...");
        makeLink(userID, name);
        console.log("  Grades link has been added.");
    // We don't check for /course/n/users/id b/c it already has a grades link
    } else {
        console.log("  Not on a profile page, grades link will not be added.");
    }
});
