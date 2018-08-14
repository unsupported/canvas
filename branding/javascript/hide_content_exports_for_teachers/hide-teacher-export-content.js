if (window.location.href.indexOf("/content_exports") > -1) {
	if(ENV.current_user_roles.indexOf('admin') < 0) {
	  $('#content').html('<h1>Unauthorized</h1><div>This page is only available to adminstrators.</div>');
	}
}