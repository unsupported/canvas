# Ruby 2+ SIS Integration Example
This folder includes examples of code that can be used to integrate SIS systems with Canvas. These are relatively simple but can serve as a framework on which you can build.

This script requires the following to be true:

* Ruby 2.0.0+ installed.
* You know how to schedule tasks to run regularly with crontab (\*nix).

## Setup/Installation
* Copy the scripts to the desired location
* Edit the script
  * Change the `access_token` variable
  * Change the `domain` variable
  * Change the `env` variable
  * Change the `source_folder` variable
  * Change the `archive_folder` variable

## Usage
Create the cron job or scheduled task to run regularly. For example to run this hourly you could create a job like this:

    0 * * * * /path/to/sis_script.rb -e

## Support
As always, this is provided AS-IS, without warranty, and without any support beyond this document and anyone kind enough to help from the community.

This is an unsupported, community-created project. Keep that in mind. Instructure won't be able to help you fix or debug this. That said, the community will hopefully help support and keep both the script and this documentation up-to-date.

Good luck!
