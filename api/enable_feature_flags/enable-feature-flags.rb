require 'csv'
require 'typhoeus'
require 'byebug'

### CHANGE THESE VALUES
domain = '' # e.g. 'domain' in 'https://domain.instructure.com'
token = ''  # api token for account admin user
csv = 'courses.csv'
feature = 'new_gradebook'

#================
# Don't edit from here down unless you know what you're doing.

base_url = "https://#{domain}.instructure.com"
test_url = "#{base_url}/accounts/self"

raise "Error: can't locate the update CSV" unless File.exist?(csv)


test = Typhoeus.get(test_url, followlocation: true)
raise "Error: The token, domain, or env variables are not set correctly" unless test.code == 200

CSV.foreach(csv, {:headers => true}) do |row|
  create_user = Typhoeus.put(
            base_url + "/api/v1/courses/" + row['canvas_course_id'] + "/features/flags/#{feature}?state=on",
            headers: {:authorization => 'Bearer ' + token }
            )
  if create_user.code == 200
    puts "Course #{row['canvas_course_id']} has feature flag enabled."
  elsif create_user.code == 400
    puts "Error: #{row['canvas_course_id']} had not been enabled. Error 400."
  else
    puts "Course #{row['canvas_course_id']} had failed to enable feature flag."
    puts "Moving right along..."
  end
end
puts "Finished enabling course feature flag."