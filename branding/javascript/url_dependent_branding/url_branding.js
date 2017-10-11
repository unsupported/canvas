// Loads styling dependent on the URL used to access Canvas.  Each URL will need its own "case".
$(document).ready(function() {
	var URL = window.location.hostname;
	switch(URL) {
		case "YOUR_DOMAIN.instructure.com OR yourVanity_URL": // Only add one URL for each 'case'
		var sheet = document.createElement('style');
			sheet.innerHTML = "{}"; // Add your styling here
			document.body.appendChild(sheet);
			break;

		case "YOUR_ADDITIONAL_DOMAIN.instructure.com OR yourVanity_URL": // Only add one URL for each 'case'
		var sheet = document.createElement('style');
			sheet.innerHTML = "{}"; // Add your styling here
			document.body.appendChild(sheet);
			break;
		}
	});