#Working as of 03/24/2016

require 'unirest'
require 'csv'

# Edit these variables below

access_token = ''                       # access token from Canvas
domain = ''                             # the domain only, such as canvas instead of canvas.instructure.com
env = ''                                # set to nil/leave as is for prod, or enter test or beta for the environment you want
csv_file = "full/path/to/the/file.csv"  # full path to the csv file


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
  puts "Where is your SIS ID update CSV located?"
  csv_file = gets.chomp
end

raise "Error: can't locate the update CSV" unless File.exist?(csv_file)

env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com/api/v1"
test_url = "#{base_url}/accounts/self"

Unirest.default_header("Authorization", "Bearer #{access_token}")

# Make generic API call to test token, domain, and env.
test = Unirest.get(test_url)

raise "Error: The token, domain, or env variables are not set correctly" unless test.code.eql?(200)

CSV.foreach(csv_file, { headers: true }) do |row|
  url = "#{base_url}/users/sis_user_id:#{row['old_user_sis_id']}/logins"
  login_response = Unirest.get(url)
  logins = login_response.body

  unless logins
    puts "User #{row['old_user_sis_id']} wasn't found."
    next
  end

  logins.each do |login|
    hashed = login.to_h #if you get `to_h': wrong element type String at 0 (expected array) (TypeError) check the headers and SIS ID values are correct

    if hashed['sis_user_id'] == row['old_user_sis_id']
      update_id = Unirest.put("#{base_url}/accounts/self/logins/#{hashed['id']}", parameters: { 'login[sis_user_id]' => row['new_user_sis_id'] })
      puts "Successfully updated \n #{update_id.body}"
    else
      puts "User #{row['old_user_sis_id']} wasn't found... Moving right along."
    end
  end
end

puts "Finished updating user SIS IDs."
