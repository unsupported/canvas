$(function(){
/* remote_source_loader.js
 * by: Danny Wahl dwahl@instructure.com
 * working as of 10/28/2015
 * This script loads a single remote JS and/or CSS
 * file, enabling rapid script and style development
 *
 * Warning: DO NOT use this script in a production
 * environment!  When you're finished testing, upload
 * your JS and CSS to Canvas via the theme Editor
 * so they will be stored on AWS with your Canvas
 * instance.  To use, simply add the path to your
 * remote script or style below.
 */
    var jsURL = "";
    var cssURL = "";

    console.log("remote_source_loader.js");
    console.log("  Warning: Not for use on production sites!");
    console.log("  Once you've finished customizing please upload via Theme Editor.");

    console.log("  Checking for remote JS.");
    if(jsURL != "") {
        console.log("  Remote JS found, loading...");
        console.log("  Executing JS via AJAX.");
        console.log(jsURL);
        $.ajax({
            url: jsURL,
            dataType: 'script'
        });
        console.log("  Remote JS loaded.");
        console.log("  Remote JS URL is: " + jsURL);
    } else {
        console.log("  No remote JS found.");
    }

    console.log("  Checking for remote CSS.");
    if(cssURL != "") {
        console.log("  Remote CSS found, loading...");
        console.log("  Appending CSS to document head");
        var $css = $(document.createElement("link"));
        $css.attr("rel", "stylesheet");
        $css.attr("type", "text/css");
        $css.attr("href", cssURL);
        $('head').append($css);
        console.log("  Remote CSS loaded.");
        console.log("  Remote CSS URL is: " + cssURL);
    } else {
        console.log("  No remote CSS found.");
    }

    console.log("Remote Loaded finished, all changes have been executed.");
});
