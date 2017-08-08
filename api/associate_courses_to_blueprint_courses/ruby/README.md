# Associate Courses to Blueprint Courses

Create a 2-column CSV with headers course_id and blueprint_course_id, see sample CSV.

If you don't have the bundler gem installed, run `gem install bundler`

Install dependencies with `bundle install`, run script with `ruby associate_course.rb`.
The script will then prompt you to set the Canvas domain, prod/test/beta env, your
api token, and the path to your mapping csv.

If your csv was formatted properly, you should see the http response codes for each batch of courses
being added to each blueprint course. Keep in mind these are added in batches; so the number of status codes
you see returned in your terminal could be substantially less than the total number of lines in your csv.
