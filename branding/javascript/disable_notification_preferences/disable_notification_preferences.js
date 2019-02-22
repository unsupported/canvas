$(function(){
    /* disable_notification_preferences.js
     * Disable the changing of notification preferences
     * for the new Canvas UI (September 2015)
     * by Danny Wahl dwahl@instructure.com
     * Working as of 10/28/2015
     */
    if(window.location.pathname == "/profile/communication") {

        console.log("disable_notification_preferences.js");
        console.log("  Editing Notification Preferences will be disabled on this page.");

        // Disable form fields
        console.log("  Disabling form fields.")

        $("#notification-preferences :input").prop("disabled", true);

        // Disable hover
        console.log("  Disabling hover interaction.");

        var $style = $(document.createElement("style"));
        $style.prop("type", "text/css");
        $style.html('.notification-table-wrapper:after {position:absolute;background:transparent;content:"";display:block;height:100%;width:100%;top:0;left:0;}');
        $style.appendTo("head");

        // Show notification settings
        console.log("  Displaying active notification settings.");

        $('.comm-event-option').addClass('show-buttons');
        $('.ui-buttonset').removeClass('screenreader-only');

        // "gray out" settings to show disabled state
        console.log("  \"Gray\" out settings to look disabled.");

        $("#notification-preferences").css({'color':'#999'});
        $(".ui-state-default").css({'color':'#999'});
        $(".ui-button.ui-state-active").css({'border-color':'#ccc','background-color':'#ccc','color':'#777'});

        // Add a note saying preferences are disabled
        console.log("  Notify user that preferences are disabled.");

        $("#content h1").html("Notification Preferences have been disabled by your administrator");

        console.log("Notification Preferences have been disabled.");
    }
});
