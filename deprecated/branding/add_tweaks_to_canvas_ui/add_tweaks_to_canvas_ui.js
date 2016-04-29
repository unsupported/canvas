//DEPRECATED AS OF 04/29/2016
$(document).ready(function () {

	/***********************************************
	 ** Customize UI: LOGIN PAGE
	 ***********************************************/
	if (window.location.href.match(/\/login/ig)) {

		// add tabindex attributes
		$("#login_form INPUT#pseudonym_session_unique_id").prop('tabindex', '1');
		$("#login_form INPUT#pseudonym_session_password").prop('tabindex', '2');
		$("#login_form BUTTON.btn-primary").prop('tabindex', '3');

		// MOBILE HACKS
		// Add type=text to username input field (so that default styles apply to it same as to password field)
		$("#login_form.front.face INPUT.input-block-level[name='pseudonym_session[unique_id]']").prop('type','text');
	}


}); // END OF: (document).ready
