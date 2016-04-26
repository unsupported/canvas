//working as of 04/25/2016
function onElementRendered(selector, cb, _attempts) {
  var el = $(selector);
  _attempts = ++_attempts || 1;
  if (el.length) return cb(el);
  if (_attempts == 60) return;
  setTimeout(function() {
    onElementRendered(selector, cb, _attempts);
  }, 250);
};

onElementRendered('#element_id_or_.class', function(e) {
  //code goes here to wait for all elements to load
});
