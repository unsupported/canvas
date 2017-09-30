# Outcomes exporter

Running this script will fetch all account-level outcomes and print their attributes to a
CSV file that can then be processed through the existing outcomes importer script.

If you don't already have the bundler gem, run `gem install bundler`, then navigate to this script directory
and run `bundle install`. Set the values in the script as outlined.

One funny caveat regarding this script is that there isn't really an API endpoint to fetch all outcomes for a given account.
Because of this, I'm generically setting the id's to be an array of numbers 1-2500. You may need to feel out how many outcomes
live at the account-level, then adjust that array as necessary. You can do this with a little Chrome DevTools/Network tab searching while making an edit to an outcome. This should give you a pretty good idea of the range of ID's you're working with.

You can then run the script by running `ruby outcome_exporter.rb`
