// Working as of 2/28/2019

/*

  **INSTRUCTIONS**
  
  This can be used to allow your users to be redirected to a specific URL by
  replacing the "YOUR REDIRECT URL HERE" below with a URL of your choice.
  
  To simply redirect users back to the base <domain>.instructure.com URL for
  your domain, replace the YOUR REDIRECT URL HERE with:
  
  `window.location.origin`
  
  Make sure to remove the backticks so as to appear like a typical variable
*/

$(function () {
  if (window.location.pathname == "/login/canvas") {
    window.location.href = // YOUR REDIRECT URL HERE;
  } else {
    console.log("All good. We're in the right place.");
  }
});
