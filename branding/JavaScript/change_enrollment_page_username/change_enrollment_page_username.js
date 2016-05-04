//WORKING AS OF 04/29/21016
 // Only works on the self enrollment screen
 if (window.location.pathname.search('enroll')) {
     $('label[for="student_email"]').text("Variable1");
     $('p:contains("Please enter your Email:")').text("Variable2:");
 }
