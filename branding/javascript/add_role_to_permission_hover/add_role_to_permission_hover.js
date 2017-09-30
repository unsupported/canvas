// This js adds the role to the permission hover
$(document).ready(function(){

  $('#course-roles-tab table.roles_table a.dropdown-toggle i').each(function(x, el){
    el = $(el);
    var cellIndex = $(el).closest('td').index();
    var new_title = (el.attr('title') ?  el.attr('title') : '' ) + ' [' + $($('#course-roles-tab table thead th em')[cellIndex-1]).text() + ']';
    el.attr('title', new_title);
  });
  $('#account-roles-tab table.roles_table a.dropdown-toggle i').each(function(x, el){
    el = $(el);
    var cellIndex = $(el).closest('td').index();
    var new_title = (el.attr('title') ?  el.attr('title') : '' ) + ' [' + $($('#account-roles-tab table thead th em')[cellIndex-1]).text() + ']';
    el.attr('title', new_title);
  });
});
