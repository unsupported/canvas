/*
Community developed script, unsupported by Canvas
Functional as of May 3, 2016
*/

//Change "test_data" to whatever data id you're using
//Modify the ns parameter to your namespace parameter
//Finally, remove the alert and do whatever you need with data.data

(function() {
  var canvasAPI = "https://example.test.instructure.com/api/v1/users/self/custom_data/test_data?ns=testing";
  $.getJSON( canvasAPI, {
    format: "json",

  })
    .done(function(data) {
      alert(data.data);
      return;
    });
})();