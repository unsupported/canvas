/* report_discussion_post.js
 * by: Danny Wahl danny@instructure.com
 * working as of 12/22/2016
 * Adds a "report" button to each entry in a discussion
 * Clicking "report" will send an inbox message to the
 * discussion author and hide the entry content from the
 * reporter.
 */

$(function(){

  console.log("report_discussion_post.js");
  console.log("  Checking if user is viewing a discussion...");

  var path = window.location.pathname.split( '/' );

  if((path[3] == "discussion_topics") && (path.length > 4)) {

    console.log("  User is viewing a discussion.");
    console.log("  Checking if inbox is enabled for the user.");

    if(ENV.current_user_disabled_inbox == false) {

      console.log("  Inbox is enabled for the user.");
      console.log("  Configuring 'report' settings...");

      var domain = window.location.hostname;

      var reporter = ENV.current_user.display_name;

      var courseName = $("#breadcrumbs li:nth-child(2) .ellipsible").text();

      var discussionTopic = $("#discussion_topic h1.discussion-title").text();
      var discussionCreator = $("#discussion_topic .author").text();
      var discussionCreatorID = $("#discussion_topic .author").attr('href').split( '/' );
      discussionCreatorID = Number(discussionCreatorID[discussionCreatorID.length - 1]);
      var discussionURL = window.location.href;

      var reportLink = '<a class="icon-flag report-post" href="#" style="margin-left:12px;">Report</a>';
      var successReportedLink = '<p><div class="ic-flash-info"><div class="ic-flash__icon" aria-hidden="true"><i class="icon-info"></i></div>This entry has been reported.</div></p>';
      var failReportedLink = '<p><div class="ic-flash-error"><div class="ic-flash__icon" aria-hidden="true"><i class="icon-warning"></i></div>Oops! This entry has <strong>NOT</strong> been reported. Go find an adult.</div></p>';

      console.log("  Adding 'report' button to entries...");

      $('.entry-controls').append(reportLink);

      console.log("  Report button added to entries.");

      var hidePost = function(success, entry) {
        var success = success;
        var entry = entry;
        var userNotice = "";
        if(success == true) {
          userNotice = successReportedLink;
          console.log("  Post was successfully reported.");
        } else {
          userNotice = failReportedLink;
          console.log("  Failed to report post.");
        }
        console.log("  Removing entry from view, and notifying user of report status...");
        $('#' + entry  + ' > article .message').html(userNotice);
        console.log("  Removed " + entry + " content from view.");
        console.log("  Removing entry controls from post.");
        $('#' + entry + ' > article .entry-controls').remove();

        console.log("  Finished.");
      }

      var reportPost = function(entry) {
        var entry = entry;

        console.log("  Gathering info of reported post...");

        var entryURL = discussionURL + "#" + entry;
        var entryAuthor = $('#' + entry + ' > article .author').text().trim();
        var messageContent = reporter + ' has reported a post by ' + entryAuthor + ' in your discussion "' + discussionTopic + '" in the course "' + courseName + '". The URL to the reported post is:' + "\r\n" + entryURL;

        var postURL = "https://" + domain + ":443/api/v1/conversations/";
        var params = {
          "recipients[]": discussionCreatorID,
          "subject": "Reported Discussion Post",
          "body": messageContent,
        }

        console.log("  Sending notification to Discussion author.");

        $.post( postURL, params, function( data ) {
            console.log(data);
        })
        .done(function(){
          hidePost(true, entry);
        })
        .fail(function(){
          hidePost(false, entry);
        });
      }

      $('.report-post').click(function(event) {
        console.log("  user clicked 'report', beginning report process...");
        event.preventDefault();
        var entry = $(this).closest(".entry").attr('id');
        reportPost(entry);
      });

    } else {
      console.log("  Inbox is disabled for current user, will not add 'report' button to posts.");
    }

  } else {
    console.log("  User is not currently viewing a discussion, will not add 'report' button to posts.");
  }
});
