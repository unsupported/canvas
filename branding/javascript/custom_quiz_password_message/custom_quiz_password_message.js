/* custom_quiz_password_message.js
 * by: Danny Wahl danny@instructure.com
 * Working as of 05/11/2016
 * allows adding a custom message to the text
 * displayed above the password form on
 * a canvas quiz.
 */

$(function(){

    console.log("custom_quiz_password_message.js");

    // Make sure the user is actually on a quiz before we start checking stuff
    console.log("  Checking current path...");
    var path = window.location.pathname.split( '/' );
    if((path[3] == "quizzes") && (path[5] == "take")) {

        console.log("  user is on a quiz page.");
        console.log("  Checking for query parameters.");

        /* https://github.com/youbastard/jquery.getQueryParameters */
        // store all query params in an object
        jQuery.extend({
            getQueryParameters : function(str) {
               return (str || document.location.search).replace(/(^\?)/,'').split("&").map(function(n){return n = n.split("="),this[n[0]] = n[1],this}.bind({}))[0];
            }
        });

        // Check if there are any query params on /take (preview, masquerade, etc...)
        var queryParams = $.getQueryParameters();
        if((Object.keys(queryParams).length == 1) && (queryParams.user_id == ENV.current_user_id)) {
            console.log("  Student taking a quiz, will display custom message.");
            var message = "<p>who watches the watchers?</p>";
            $("#quiz_access_code").parent().before(message);
        } else {
            console.log("  Not a student taking a test, won't display custom message.");
        }
    } else {
        console.log("  Not on quiz page, won't display custom mesage.");
    }
});
