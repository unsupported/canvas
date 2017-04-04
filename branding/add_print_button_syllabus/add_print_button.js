//This is unsupported by Canvas
//Working 4/4/2017

$(document).ready(function() {
    if (window.location.href.indexOf("syllabus") > -1) {
        var new_link = $('<div class="grid-row middle-xs between-xs" style="margin-bottom: 10px"><div class="col-xs-6"></div><div class="col-md-6 col-lg-3"><a class="btn print-grades icon-printer" href="javascript:window.print()">Print Syllabus</a></div></div>');
        $('#content').prepend(new_link);
    }
});
