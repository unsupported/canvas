$(document).ready(function() {
	// This hides both the "+Email Address" and the modal "Email" tab
	$('a#ui-id-1.ui-tabs-anchor[href*="register_email_address"]').hide();
	$('a.add_email_link').replaceWith('<p></p>');

	// This hides both the "+Contact Method" and modal "Text (SMS)" tab
	$('a#ui-id-1.ui-tabs-anchor[href*="register_sms_number"]').hide();
	$('a.add_contact_link.icon-add').replaceWith('<p></p>');
});
