/*
 * reset_notification_preferences.js
 * by: Danny Wahl dwahl@instructure.com
 * Working as of 02/17/2016
 * Adds indicators to the notification
 * settings to show what the defaults are,
 * making it easier to reset defaults.
 */

$(function(){
    if(window.location.pathname == "/profile/communication") {
        console.log("reset_notification_preferences.js");

        var notifications = {};

        var notificationDefault = function(dataCategory, settingDefault) {
            this.dataCategory = dataCategory;
            this.default = settingDefault;
            this.selector = $('td[data-category="' + dataCategory + '"] input[data-value="' + settingDefault + '"]');
            this.selectorLabel = $('td[data-category="' + dataCategory + '"] input[data-value="' + settingDefault + '"] + label');
            this.selectorScreenReader = $('td[data-category="' + dataCategory + '"] input[data-value="' + settingDefault + '"] + label .screenreader-only');
            this.checkIfDefault = function() {
                if(this.selector.is(':checked')) {
                    return true;
                } else {
                    return false;
                }
            };
        };

        // Instantiate notification default values

        // Course Activities
        console.log("  Populating 'Course Activities' defaults.");
        notifications.due_date = new notificationDefault("due_date", "weekly");
        notifications.grading_policies = new notificationDefault("grading_policies", "weekly");
        notifications.course_content = new notificationDefault("course_content", "never");
        notifications.files = new notificationDefault("files", "never");
        notifications.announcement = new notificationDefault("announcement", "immediately");
        notifications.announcement_created_by_you = new notificationDefault("announcement_created_by_you", "never");
        notifications.grading = new notificationDefault("grading", "immediately");
        notifications.invitation = new notificationDefault("invitation", "immediately");
        notifications.submission_comment = new notificationDefault("submission_comment", "daily");

        // Discussions
        console.log("  Populating 'Discussions' defaults.");
        notifications.discussion = new notificationDefault("discussion", "never");
        notifications.discussion_entry = new notificationDefault("discussion_entry", "daily");

        // Conversations
        console.log("  Populating 'Conversations' defaults.");
        notifications.added_to_conversation = new notificationDefault("added_to_conversation", "immediately");
        notifications.conversation_message = new notificationDefault("conversation_message", "immediately");
        notifications.conversation_created = new notificationDefault("conversation_created", "never");

        // Scheduling
        console.log("  Populating 'Scheduling' defaults.");
        notifications.student_appointment_signups = new notificationDefault("student_appointment_signups", "never");
        notifications.appointment_signups = new notificationDefault("appointment_signups", "immediately");
        notifications.appointment_cancelations = new notificationDefault("appointment_cancelations", "immediately");
        notifications.appointment_availability = new notificationDefault("appointment_availability", "immediately");
        notifications.calendar = new notificationDefault("calendar", "never");

        // Groups
        console.log("  Populating 'Groups' defaults.");
        notifications.membership_update = new notificationDefault("membership_update", "daily");

        // Alerts
        console.log("  Populating 'Alerts' defaults.");
        notifications.other = new notificationDefault("other", "daily");

        // Conferences
        console.log("  Populating 'Conferences' defaults.");
        notifications.recording_ready = new notificationDefault("recording_ready", "immediately");

        // Add indicators to non-default notification settings.

        var labelTitle = "";
        var screenReaderText = "";
        var isDefault = "";
        var settingName = "";

        for(notification in notifications) {

            settingName = notifications[notification].dataCategory.toString();

            // Check if the setting is set to the default value.
            isDefault = notifications[notification].checkIfDefault();
            console.log("  Checking " + settingName + ".");

            if(!isDefault) {
                // Display a border around defaults.
                console.log("  " + settingName + " is not set to default");
                notifications[notification].selectorLabel.css("box-shadow", "0 0 2px #cccc00 inset");
                console.log("  Visual indicator has been added for " + settingName);
            } else {
                console.log("  " + settingName + " is set to default");
                console.log("  No visual indicator added.");
            }

            // Append "(default)" to label title.
            console.log("  Adding (default) to label for " + settingName);
            labelTitle = notifications[notification].selectorLabel.attr("title");
                        notifications[notification].selectorLabel.attr("title", labelTitle + " (default)");

            // Append "(default)" to screen reader text.
            console.log("  Adding (default) to screen reader for " + settingName);
            screenReaderText = notifications[notification].selectorScreenReader.html();
            notifications[notification].selectorScreenReader.html(screenReaderText + " (default)");
        }
        console.log("  Indicators have been added for all non-default settings.");
    }
});
