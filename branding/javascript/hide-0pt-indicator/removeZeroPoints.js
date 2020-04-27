// Written by A. Carey, Instructure Inc
// 2020.04.27
// If you put this in your Theme's JS - 
// It will hide any module point indicators with '0 pts'



function onElementRendered(selector, cb, _attempts) {
  var el = $(selector);
  _attempts = ++_attempts || 1;
  if (el.length) return cb(el);
  if (_attempts == 60) return;
  setTimeout(function() {
    onElementRendered(selector, cb, _attempts);
  }, 250);
};

function removeZeroPoints(){

	let zeropoints = $('.points_possible_display:contains("0 pts")'); // select all points indicators that have 0 pts
	zeropoints.parent('div').remove(); // remove the parent divs of selected points indicators

}

onElementRendered(".points_possible_display:contains('0 pts')", function(e) {
  	// code goes here to wait for all elements to load
  	// function will run if currently on modules page

	if(window.location.href.indexOf("/modules") > -1){
		removeZeroPoints(); //run removeZeroPoints function
	}	
	
});


