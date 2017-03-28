//Show Feature Request Help Link To Teachers and Admins
//Provided AS-IS with out support. Use at your own risk.
//Confirmed working as of Sept 19,2016

if($.inArray('admin',ENV['current_user_roles']) > -1 ||  $.inArray('teacher',ENV['current_user_roles']) > -1) {
    $("head").append('<style>\
    li.ic-NavMenu-list-item a[href="https://community.canvaslms.com/community/ideas/feature-ideas"] + div \
    { display: inline-block !important;} \
    li.ic-NavMenu-list-item a[href="https://community.canvaslms.com/community/ideas/feature-ideas"] \
    { display: block !important;} </style>');
  }
