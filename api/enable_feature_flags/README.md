#Bulk Enable Feature Flags

This script takes a csv file with one header canvas_course_id. The id's in this column refer to courses that should have a feature flag enabled via the API.

Best case use: If only feature flags can be enabled at the course level, this script enables (also disables) the feature flag in bulk, course by course.

Please see the 'courses.csv' as a template to structure your CSV file.