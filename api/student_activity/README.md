Exporting Student Activity to CSV
======

The `student_activity_to_csv.rb` file in this folder can be
used to generate a report of all student interactions across
all courses in an account. The report will be generated in a
CSV formatted file and will include the following learning
activities:

* All Assignments (including quizzes)
* All Discussions

Requirements
======

You will need to install [Ruby](http://ruby-lang.org) version 1.9.2.
Earlier versions (including 1.8.6) will not work.

Configuration
======

You will need to open the included ruby file:

student_activity_to_csv.rb

and adjust or input the following variables:

Account ID:

Find `$account_id = ''` and place your account ID in the quotes.

Access Token:

Find `$access_token = ''` and place your access token in the
quotes.

Canvas Domain:

Optionally, find `$canvas_domain = ''` and place your Canvas
domain in the quotes.


Usage
======

To generate the CSV report, simply run the included ruby file:
```
$ ruby student_activity_to_csv.rb [PATH TO CSV]
```
Replace `[PATH TO CSV]` with the name and, optionally, the path
where you would like to save the resulting report.

Support
======

This is an unsupported, community-created project. Keep that in
mind. Instructure won't be able to help you fix or debug this.
That said, the community will hopefully help support and keep
both the script and this documentation up-to-date.

Good luck!
