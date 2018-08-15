# Working as of 5/25/2018

require 'csv'
require 'typhoeus'
require 'byebug'

### CHANGE THESE VALUES
domain = '' # e.g. 'domain' in 'https://domain.instructure.com'
token = ''  # api token for account admin user
env = ''	#Either blank for prod, or type test or beta
feature = '' # ex. new_gradebook. GET list of features API Endpoint: https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index
status = 'on' # use 'off' to disable feature
csv = '' # Path to file that should contain a canvas_course_id header

#================
# Don't edit from here down unless you know what you're doing.

env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com/"
test_url = "#{base_url}/accounts/self"

raise "Error: can't locate the update CSV" unless File.exist?(csv)


test = Typhoeus.get(test_url, followlocation: true)
raise "Error: The token, domain, or env variables are not set correctly" unless test.code == 200

CSV.foreach(csv, {:headers => true}) do |row|
  enable_feature_flag = Typhoeus.put(
            base_url + "/api/v1/courses/" + row['canvas_course_id'] + "/features/flags/#{feature}?state=#{status}",
            headers: {:authorization => 'Bearer ' + token }
            )
  if enable_feature_flag.code == 200
    puts "Course #{row['canvas_course_id']} feature flag is now #{status}."
  elsif enable_feature_flag.code == 400
    puts "Error: #{row['canvas_course_id']} that didn't work Error 400."
  else
    puts "Course #{row['canvas_course_id']} had failed to turn feature flag #{status}."
    puts "Moving right along..."
  end
end
puts "Finished enabling course feature flag."