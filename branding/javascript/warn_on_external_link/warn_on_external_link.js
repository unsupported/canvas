/* canvas-warn-on-external-link.js
 * by: Danny Wahl dwahl@instructure.com
 * Working as of 11/12/2015
 * Adds an interstitial forcing the user
 * to confirm that they want to follow
 * an external link
 */


$(function(){

    console.log("warn_on_external_link.js");

    // Bind to anchors with the "external" class selector
    $(".external").click(function(e){

        // Check with the user if they want to leave
        console.log("  'external' link clicked.");
        console.log("  Confirming if the user wants to leave.");

        var goExternal = confirm("Are you sure you want to leave " + window.location.host + "?");

        console.log("  User selected: " + goExternal);

        if(!goExternal) {
            console.log("  Action cancelled.");
            e.preventDefault();
        }

    });
});
