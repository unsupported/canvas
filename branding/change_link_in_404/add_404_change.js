$(document).ready(function() {
    function onElementRendered(selector, cb, _attempts) {
        var el = $(selector);
        _attempts = ++_attempts || 1;
        if (el.length) return cb(el);
        if (_attempts == 60) return;
        setTimeout(function() {
            onElementRendered(selector, cb, _attempts);
        }, 250);
    }

    //This will check to see that an h2 tag has loaded, then it will check the text
    //inside the h2 tag to make sure it has "Not Found". Then it will hide the submit_error_link
    //and add a link that you can edit on line 19 to your liking.
    onElementRendered('h2', function(e) {
        //code goes here to wait for all elements to load
        if ($('h2').text().indexOf('Not Found') > -1) {
            $('.submit_error_link').hide();
            $('p').append('<h3><a href="#LinkGoesHere" id="new-link-id">Text for link goes here</a></h3>');
            console.log('Did it!');
        }
    });
});
