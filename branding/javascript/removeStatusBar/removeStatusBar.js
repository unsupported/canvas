function onElementRendered(selector, cb, _attempts) {
    var el = $(selector);
    _attempts = ++_attempts || 1;
    if (el.length) return cb(el);
    if (_attempts == 60) return;
    setTimeout(function() {
        onElementRendered(selector, cb, _attempts);
    }, 250);
};

// function to target the RCE status bar and remove HTML snippet
function removeStatusBar(){
    let statusBar = $('span[data-testid="whole-status-bar-path"]')
    statusBar.hide();
};

// function will wait for targetted element to load before attempting to hide
$(document).ready(function() {
    onElementRendered('span[data-testid="whole-status-bar-path"]', function(e) {
        console.log('Removing status bar....')
        removeStatusBar(); 
    });
});
