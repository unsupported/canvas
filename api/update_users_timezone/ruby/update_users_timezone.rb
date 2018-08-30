# Working as of 08/30/2018
require 'typhoeus'
require 'csv'

# variables that you would want to change to match your domain to update timezones
access_token = ''
domain = '' # this would be canvas or canvas.test/canvas.beta
csv_path = "full/path/to/file.csv"

########################### DO NOT EDIT ##############################
url = "https://#{domain}.test.instructure.com/api/v1/" # remove or add test & beta if needed

hydra = Typhoeus::Hydra.new(max_concurrency: 10)

CSV.foreach(csv_path, { headers: true }) do |row|

	put_response = Typhoeus::Request.new("#{url}users/sis_user_id:#{row['user_sis_id']}",
	method: :put,
	params: { 'user[time_zone]' => row['timezone'] },
	headers: { Authorization: "Bearer #{access_token}" }
	)

	put_response.on_complete do |response|
		if response.code.eql?(200)
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
