Change Enrollment Text
======

Changes the text on the self-enrollment page from "Please enter your email address:" to anything you specify.

- Replace 'Variable1' with what you wish to title the field (Email Address, Username, Student ID).
- Replace 'Variable2' with the sentence you wish to display to to the user.  

- Example:
if (window.location.pathname.search('enroll')) {
    $('label[for="student_email"]').text("Username");
    $('p:contains("Please enter your email address:")').text("Please enter your Username:");
}

Support
======

This is an unsupported, community-created project. Keep that in mind.
Instructure won't be able to help you fix or debug this. That said, the
community will hopefully help support and keep both the script and this
documentation up-to-date.

Good luck!
