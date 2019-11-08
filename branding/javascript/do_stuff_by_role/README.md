# Canvas Do Stuff By Role
This is a helper JavaScript to get the current enrollment types for the current user, and compare them to a whitelist, then execute custom functionality if the user has the whitelisted role.

## Usage
* Define whitelisted role types in the `supportedRoles[]` array.  See the [Enrollments API](https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index) for more info on role types.
* Add desired functionality for users with supported roles in the `doStuff()` function.
* Upload this script to the theme editor.
