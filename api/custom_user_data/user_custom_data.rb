#This is a community script and is not supported by Instructure
#Functional as of May 3, 2016

require 'unirest'
require 'csv'

#================
# Change these
access_token = "your api token here" # api access token
domain = "" # e.g. the 'schoolname' in 'schoolname.instructure.com'
env = "test" # production = nil, "test" = test, "beta" = beta
csv_file = "custom_data.csv" # point to the file location
account = "1" # what account? nil is not acceptable

#================
# Don't edit from here down unless you know what you're doing.

unless access_token
  puts "What is your access token?"
  access_token = gets.chomp
end

unless domain
  puts "What is your Canvas domain?"
  domain = gets.chomp
end

unless csv_file
  puts "Where is your Custom Data CSV located?"
  csv_file = gets.chomp
end

raise "Error: can't locate the Data CSV" unless File.exists?(csv_file)

env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com/api/v1"
test_url = "#{base_url}/accounts/self"

Unirest.default_header("Authorization", "Bearer #{access_token}")

# Make generic API call to test token, domain, and env.
test = Unirest.get(test_url)

raise "Error: The token, domain, or env variables are not set correctly" unless test.code == 200

CSV.foreach(csv_file, {:headers => true}) do |row|
  url = "#{base_url}/users/#{row[0]}/custom_data/#{row[1]}"

  create_data = Unirest.put(url, parameters: { 'ns' => row[2], 'data' => row[3] })
  puts "API Call Successful \n #{create_data.body} \n\n"
end

puts "Finished creating custom data"
