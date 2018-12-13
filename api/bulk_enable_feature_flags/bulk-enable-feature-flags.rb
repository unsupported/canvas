# Working as of 5/25/2018

require 'csv'
require 'byebug'
require 'typhoeus'
require 'io/console'

##################################
# STATIC VARIABLES - DO NOT EDIT #
##################################

puts "For production, hit enter. For Beta, 'beta' and for Test, 'test'"
env = gets.chomp!

# env check
env != '' ? env << '.' : env

puts 'Enter the domain - EX: <domain>.instructure.com'
domain = gets.chomp!

puts 'Enter a valid access token to perform the API calls within this script'
token = STDIN.noecho(&:gets).chomp!

puts 'Enter the full file path for CSV data. EX: /Users/person/file/to/path.csv'
csv_file = gets.chomp!

base_url = "https://#{domain}.#{env}instructure.com"
test_url = "#{base_url}/accounts/self"

########################
# EDIT THESE VARIABLES #
########################

# The value of 'feature' will reflect the feature flag to be toggled off/on (EX: `student_outcome_gradebook`)
# Use this API request to GET available feature flags => https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index)

feature = ''

#########################
# END OF VARIABLE SETUP #
#########################

# Error if CSV file path is incorrect
raise "Error: can't locate the update CSV" unless File.exist?(csv_file)

# Test for valid token, domain, and env
test = Typhoeus.get(test_url, followlocation: true)
raise 'Error: The token, domain, or env variables are not set correctly' unless test.code == 200

# Main process for the feature flags to be toggled
CSV.foreach(csv_file, headers: true) do |row|
  enable_feature_flag = Typhoeus.put(
    "#{base_url}/api/v1/courses/#{row['course_id']}/features/flags/#{feature}",
    headers: { Authorization: "Bearer  #{token}" },
    params: {
      state: row['state']
    }
  )
  if enable_feature_flag.success?
    puts "#{feature} for Course #{row['course_id']} has been updated to be #{row['state']}."
  else
    puts enable_feature_flag.code
    puts "ERROR: #{enable_feature_flag.code}\n#{feature} for Course #{row['course_id']} has failed to update."
  end
end
puts "Course feature flags updated according to values in #{csv_file}."
