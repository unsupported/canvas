# Enroll users using Canvas IDs for users and sections

This script allows users to be enrolled into Canvas sections without the need for the user nor the section to have an SIS ID. The script uses the [enrollments API](https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create) and requires that both Canvas User IDs and Canvas Section IDs be used.

The input CSV has 3 required columns:
```
    canvas_user_id,canvas_section_id,role
    123,456,student
```

Please reference `example.csv`

* canvas_user_id: The Canvas ID (NOT SIS ID) for the user that should be enrolled.
* canvas_section_id: The Canvas ID (NOT SIS ID) for the section into which the user should be enrolled.
* role: The name of the role to be used for the enrollment (See Notes)

## Notes

* Default Canvas roles (student, teacher, ta and designer) are not valid for the enrollment API. As a result, the script will alter these role to the appropriate values at run time if they are detected as input. Custom roles are also supported.
* This script is only designed to add enrollments. It will not delete existing enrollments.
* This script enrolls the user as an active user in the course and does not send a notification about the enrollment to the user.
