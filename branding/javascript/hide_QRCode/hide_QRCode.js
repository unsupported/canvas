function onElementRendered(selector, cb, _attempts) {
  var el = $(selector);
  _attempts = ++_attempts || 1;
  if (el.length) return cb(el);
  if (_attempts == 60) return;
  setTimeout(function() {
    onElementRendered(selector, cb, _attempts);
  }, 250);
};

onElementRendered("#global_nav_profile_link", function(e) {
  	//code goes here to wait for all elements to load
	
	$('#global_nav_profile_link').click(hideQR); //run hideQR function when user clicks on Account link

});

function hideQR() {
	onElementRendered("button:contains('QR for Mobile Login')", function(e) {
		// Wait for slide out tray to fully load
		let btnparents = $( "button:contains('QR for Mobile Login')" ).parents('li'); // select list item based on button with QR text
		btnparents.remove(); // remove selected list item
	});
	

}
