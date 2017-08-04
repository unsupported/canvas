//working as of August 4th, 2017
/*This script automatically selects the "open in new tab" checkbox
on a new module item if it is an external url or external tool*/

//Don't edit past here unless you know JS and are comfortable
//making changes on your own.
$(document).ready(() => {
  //adds a function on the #add_module_item_select when it's value changes
  $('#add_module_item_select').change(() => {
    if ($('#add_module_item_select').val().indexOf('external') > -1) {
      $('#external_url_create_new_tab').prop("checked", true);
      $('#external_tool_create_new_tab').prop("checked", true);
    }
  });
});
