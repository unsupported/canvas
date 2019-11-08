/* always_record_conferences.js
 * by: Danny Wahl danny@instructure.com
 * Working as of 06/16/2016
 * automatically checks the "enable recording"
 * setting when creating a new conference
 * and hides the setting from the user so they
 * can't uncheck it.
 */

$(function(){

  console.log("always_record_conferences.js");

  console.log("  Checking current path...");
  var path = window.location.pathname.split( '/' );

  if((path[1] == "courses") && (path[3] == "conferences")) {

    console.log("  User is on conferences page.");
    console.log("  Waiting for 'New Conference' to be pressed...");

    $("button[title='New Conference']").click(function(){

      console.log("  'New Conference' pressed, hiding recording option.");
      $(".web_conference_user_settings").hide();
      console.log("  Recording option hidden from user.");

      console.log("  Setting recording to 'true'").
      $("#web_conference_user_settings_record").attr("checked", true);
      console.log("  Recording is enabled for this new conference.");

    });

  } else {
    console.log("  Not on a 'Conferences' page, won't set recording preferences.");
  }

});
