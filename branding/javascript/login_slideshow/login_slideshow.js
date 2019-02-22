/*
 * Canvas Login Slideshow
 * by: Danny Wahl (dwahl@instructure.com)
 * Working as of 10/28/2015
 * Allows you to specify up to 3 images
 * to rotate on the background of the login page
 * independently of the new theme editor
 * REQUIRES: login_slideshow.css
 */

$(function(){

    // Check if path is /login/canvas
    if(window.location.pathname == "/login/canvas") {

        console.log("login_slideshow.js")
        console.log("  WARNING: Requires login_slideshow.css to function");

        console.log("  Creating unordered list.");
        var $slideshow = $(document.createElement("ul"));
        $slideshow.addClass("slideshow");
        var $slide = "";
        for (var i = 0; i < 3; i++) {
            $slide = $(document.createElement("li"));
            $slide.addClass("slide");
            $slideshow.append($slide);
        }

        console.log("  Adding list to page.");
        $(".ic-Login-Body").append($slideshow);

        console.log("  Slideshow has been added to page.");
    }
});
