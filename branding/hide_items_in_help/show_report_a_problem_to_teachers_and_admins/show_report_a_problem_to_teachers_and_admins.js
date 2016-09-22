//Show Report a Problem Help Link To Teachers and Admins
//Provided AS-IS with out support. Use at your own risk.
//Confirmed working as of Sept 22,2016

if($.inArray('admin',ENV['current_user_roles']) > -1 ||  $.inArray('teacher',ENV['current_user_roles']) > -1) {
    $("head").append('<style>\
    li.ic-NavMenu-list-item a[href="#create_ticket"] + div \
    { display: inline-block !important;} \
    li.ic-NavMenu-list-item a[href="#create_ticket"] \
    { display: block !important;} </style>');
  }
