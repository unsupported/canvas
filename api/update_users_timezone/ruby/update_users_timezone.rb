# Working as of 12/17/2019
require 'csv'
require 'json'
require 'typhoeus'
require 'io/console'

## TOKEN
puts 'Enter a valid access token to perform the API calls within this script'
token = STDIN.noecho(&:gets).chomp!

## DOMAIN
puts 'Enter the domain, EX: <domain>.instructure.com'
domain = gets.chomp!.downcase

## ENV
puts "For prod, hit enter. For Beta, enter 'beta'. For Test, enter 'test'"
env = gets.chomp!.downcase
env != '' ? env << '.' : env

## SOURCE FILE
puts 'Enter the full path to the file containing your user_sis_ids and timezones'
source_folder = gets.chomp!

url = "https://#{domain}.#{env}instructure.com/api/v1/" # remove or add test & beta if needed

hydra = Typhoeus::Hydra.new(max_concurrency: 10)

CSV.foreach(source_folder, headers: true) do |row|
  put_response = Typhoeus::Request.new(
    "#{url}users/sis_user_id:#{row['user_sis_id']}",
    method: :put,
    params: {
      'user[time_zone]': row['timezone']
    },
    headers: {
      authorization: "Bearer #{token}"
    }
  )

  put_response.on_complete do |response|
    if response.success?
      puts "Updated user #{row['user_sis_id']} with new time zone settings."
    elsif response.code != 200
      puts response.body
    else
      puts "Unable to update user #{row['user_sis_id']}'s time zone value."
    end
  end
  hydra.queue(put_response)
end

hydra.run
puts 'Completely Done'
