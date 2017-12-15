# Working as of 12/15/2017

require 'csv'
require 'typhoeus'
require 'json'
#------------------Replace these values-----------------------------#

access_token = '' # API token
url = 'https://canvas.instructure.com' # Enter the full URL to the domain you want to merge files. Must begin with https://
csv_file = 'full/path/to/the/file.csv' # Enter the full path to the file. /Users/XXXXXX/Path/To/File.csv

#-------------------Do not edit below this line---------------------#
# First column is user account that will be merged into second column. #
raise 'Unable to run script, please check token, and/or URL.' unless Typhoeus.get(url).code == 200 || 302

raise "Can't locate the CSV file." unless File.exist?(csv_file)

hydra = Typhoeus::Hydra.new(max_concurrency: 10)

CSV.foreach(csv_file, { headers: true }) do |row|

  api_call = "#{url}/api/v1/users/sis_user_id:#{row['to_be_merged']}/merge_into/sis_user_id:#{row['merged']}"
	merge_api = Typhoeus::Request.new(api_call, method: :put, headers: { Authorization: "Bearer #{access_token}" })
	merge_api.on_complete do |response|
		if response.code.eql?(200)
			puts "Merged user #{row['to_be_merged']} into #{row['merged']}"
		else
			puts "Unable to merge #{row['to_be_merged']} into #{row['merged']}, check to verify users exist with correct SIS ID values."
		end
	end
	hydra.queue(merge_api)
end
hydra.run

puts 'Successfully merged users.'
