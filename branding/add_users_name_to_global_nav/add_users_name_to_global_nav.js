/*
 * Adds the user's display name in place of the word "Account" on the Canvas Global Navigation Menu.
 *
 * This script is provided AS-IS with no support nor warranty.
 * Confirmed working Aug 25, 2016
 *
 */
$('window').ready(function(){$('#global_nav_profile_link div.menu-item__text').text(ENV.current_user.display_name);});
