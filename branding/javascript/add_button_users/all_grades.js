///This will target any page that includes /users in the URL and then adds a button to the right margin and adds a button to display the grades of all classes for the current user
$(document).ready(function() {
    if (window.location.pathname.indexOf('/users') > -1) {
        var address = '/users/' + window.location.pathname.split('/')[4] + '/grades';
        $('.rs-margin-lr:first-of-type').append('<a href="' + address + '"class="btn button-sidebar-wide"><i class="icon-gradebook"></i> Text for Button</a>');
    }
});
