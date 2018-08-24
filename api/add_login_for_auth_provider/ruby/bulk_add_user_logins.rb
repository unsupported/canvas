# Working as of 3/11/2018
require 'typhoeus'
require 'csv'
require 'json'

### Prompts to set ENV, DOMAIN, TOKEN, and CSV FILE PATH

## ENV
puts "For prod, hit enter. For Beta, enter 'beta'. For Test, enter 'test'"
@env = gets.chomp!.downcase
@env != '' ? @env << '.' : @env

## DOMAIN
puts 'Enter the domain, EX: <domain>.instructure.com'
@domain = gets.chomp!.downcase

## TOKEN
puts 'Enter a valid access token to perform the API calls within this script'
@token = gets.chomp!

## CSV FILE ##
puts 'Enter the full file path for CSV data. EX: /Users/person/file/to/path.csv'
@csv_file = gets.chomp!

@base_url = "https://#{@domain}.#{@env}instructure.com/api/v1/accounts/self/logins/"
@default_headers = { Authorization: 'Bearer ' + @token }

CSV.foreach(@csv_file, headers: true) do |row|
  return raise "Invalid CSV headers: 'canvas_user_id' not found" if row['canvas_user_id'].nil?
  return raise "Invalid CSV headers: 'login_id' not found" if row['login_id'].nil?
  # return raise "Invalid CSV headers: 'authentication_provider_id' not found" if row['authentication_provider_id'].nil? # || ENABLE IF SETTING AUTHENTICAION PROVIDER
  # return raise "Invalid CSV headers: 'sis_user_id' not found" if row['sis_user_id'].nil? # || ENABLE IF NEW LOGIN NEEDS TO HAVE AN SIS ID
  response = Typhoeus.post(
    @base_url,
    headers: @default_headers,
    body: {
      user: {
        id: row['canvas_user_id']
      },
      login: {
        unique_id: row['login_id'],
        ## If not using sis_user_id, remove the trailing comma on the next line.
        # authentication_provider_id: "#{row['authentication_provider_id']}", # || ENABLE IF SETTING AUTHENTICAION PROVIDER
        # sis_user_id: row['sis_user_id'] # || ENABLE IF NEW LOGIN NEEDS TO HAVE AN SIS ID
      }
    }
  )
  # parse JSON data to save in readable array
  data = JSON.parse(response.body)
  puts data
end
