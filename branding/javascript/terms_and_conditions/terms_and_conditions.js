//working as of August 3rd, 2017
//This script changes the terms and conditions page in Canvas to
//include a second checkbox. It will not allow
//the user to click submit unless both boxes are checked.

//Change These variables for second check box
let terms = "https://example.org"; //insert URL to your terms here
let privacy = "https://example.org"; //insert URL to privacy policy

//Don't edit past here unless you know JS and are comfortable
//making changes on your own.
$(document).ready(() => {
  $('label.checkbox input[name="user[terms_of_use]"]').parent().parent().append(`<p><label class="checkbox">\
  <input type="checkbox" name="second[terms_of_use]">I agree to the <a target="_blank" href=${terms} class="external" rel="noreferrer">\
  <span>client's terms of use</span><span class="ui-icon ui-icon-extlink ui-icon-inline" title="Links to an external site.">\
  <span class="screenreader-only">Links to an external site.</span></span></a> and <a target="_blank" href=${privacy} class="external" rel="noreferrer">\
  <span>privacy policy</span><span class="ui-icon ui-icon-extlink ui-icon-inline" title="Links to an external site."><span class="screenreader-only">\
  Links to an external site.</span></span></a>.</label></p>`);
  $('.button_box.ic-Login-confirmation__actions button[type="submit"]').on('click', (e) => {
    if ($('[name="user[terms_of_use]"]').prop('checked') && $('[name="second[terms_of_use]"]').prop('checked')) {
      console.log("both terms accepted");
    } else {
      e.preventDefault();
      if (!$('#errorOnTerms').text()) {
        $('.button_box.ic-Login-confirmation__actions').append(`<p id="errorOnTerms" style="color:red">You must agree to both terms and conditions`);
      }
      return false;
    }
  });

});

/* the script currently does not capture any information
 about the second box being checked it only prevents
 the user from submitting if it isn't checked */
