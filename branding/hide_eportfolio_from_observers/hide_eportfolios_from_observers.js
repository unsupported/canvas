// THIS IS NOT SUPPORTED BY INSTRUCTURE.
// WORKS AS OF 3.9.17
// Hide eportfolios from observers.  
// Use at your own risk.

$(document).ready(function(){
	if($.inArray('observer',ENV['current_user_roles']) > 0) {
	  $('.eportfolios').hide();
	  /* Hide eportfolios from observers */
	};
})