// Working as of 7/28/2020

function onElementRendered(selector, cb, _attempts) {
  var el = $(selector);
  _attempts = ++_attempts || 1;
  if (el.length) return cb(el);
  if (_attempts == 60) return;
  setTimeout(function () {
    onElementRendered(selector, cb, _attempts);
  }, 250);
}

// When element is rendered, the targeted element will be hidden
onElementRendered(".conferences", function (e) {
  $(".conferences").hide();
});

onElementRendered("[aria-label='Conferences']", function (e) {
  $("[aria-label='Conferences']").hide();
});
