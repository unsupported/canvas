/*
 * style_by_domain.js
 * by: Danny Wahl danny@instructure.com
 * Working as of 05/26/2016
 * Style a Canvas instance based on the
 * domain it's being accessed from.
 * Add your desired domains to the switch
 * below, and designate a CSS class to added
 * to the body when that domain is detected.
 */

$(function(){

  console.log("style_by_domain.js");

  var class = "";

  console.log("  Checking domain...");
  switch(window.location.hostname) {

    case "a.instructure.com":
      class = "domain-a";
      console.log("  Domain " + window.location.hostname + " found, using class " + class);
      break;

    case "b.instructure.com":
      class = "domain-b";
      console.log("  Domain " + window.location.hostname + " found, using class " + class);
      break;

    default:
      class = "default";
      console.log("  Domain " + window.location.hostname + " not found in list of options, using class " + class);
  }

  // Append the appropriate class to the body element
  console.log("  Adding Class " + class " to body element.");
  $("body").addClass(class);

});
