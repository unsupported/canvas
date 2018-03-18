# Update Blank Course SIS Ids

Last working as of 3/18/2018

## Installation

Ensure the Elixir programming language is installed on your machine

Create a new CSV file with the headers `sis_id` and `course_id` -
See the sample CSV for details

Install all dependencies by running `mix deps.get`

Compile the project by running `mix compile`

Open the interactive Elixir console by running `iex -S mix`, then to run the
script, `UpdateBlankCourseSisIds.update_courses()`

The script will then ask you to enter your api token, domain (the name of your
institution as it appears just before `.instructure.com` in your Canvas URL) and
the full filepath to your CSV file.

To exit the interactive Elixir console, hit ctrl c and select `a` for abort
