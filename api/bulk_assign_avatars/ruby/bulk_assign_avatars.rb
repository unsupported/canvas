#Working as of 04/12/2016
# Change these
access_token = ''
domain = ''
env = ''
csv_file = ''

#================
# Don't edit from here down unless you know what you're doing.
require 'unirest'
require 'csv'

unless access_token
  puts "What is your access token?"
  access_token = gets.chomp
end

unless domain
  puts "What is your Canvas domain?"
  domain = gets.chomp
end

unless csv_file
  puts "Where is your avatar update CSV located?"
  csv_file = gets.chomp
end

raise "Error: can't locate the update CSV" unless File.exist?(csv_file)

env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com/api/v1"
test_url = "#{base_url}/accounts/self"

Unirest.default_header("Authorization", "Bearer #{access_token}")

# Make generic API call to test token, domain, and env.
test = Unirest.get(test_url)

raise "Error: The token, domain, or env variables are not set correctly" unless test.code == 200

CSV.foreach(csv_file, {:headers => true}) do |row|
  url = "#{base_url}/users/#{row['user_id_column']}.json"
  update = Unirest.put(url, parameters: { "user[avatar][url]" => row['user_image_column'] })
  if update.code == 200
    puts "User #{row['user_id_column']}'s avatar updated."
  else
    puts "User #{row['user_id_column']}'s avatar failed to update."
    puts "Moving right along."
  end
end
puts "Finished updating avatars."
