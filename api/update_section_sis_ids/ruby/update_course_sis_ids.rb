#Working as of 03/30/2016
require 'typhoeus'
require 'csv'
require 'json'

################################# CHANGE THESE VALUES ###########################
access_token = '' 			#your API token that was generated from your account user
domain = '' 						# domain.instructure.com, use domain
env = ''  							# leave blank or nil is pushing to production
csv_file = ''						# use the full path to the file /Users/XXXXX/Path/To/File.csv
############################## DO NOT CHANGE THESE VALUES #######################

default_headers = {"Authorization" => "Bearer #{access_token}"}
env ? env << "." : env
base_url = "https://#{domain}.#{env}instructure.com/"
hydra = Typhoeus::Hydra.new(max_concurrency: 20)

CSV.foreach(csv_file, {headers: true}) do |row|
	if row.headers[0] != 'old_section_id' || row.headers[1] != 'new_section_id'
		puts 'First column needs to be old_section_id, and second column needs to be new_section_id.'
	else
	api_get_oldsection = Typhoeus::Request.new("#{base_url}/api/v1/sections/sis_section_id:#{row['old_section_id']}",
										  headers: default_headers)

		api_get_oldsection.on_complete do |response|
			if response.code == 200
				change_section_id = Typhoeus::Request.new("#{base_url}/api/v1/sections/sis_section_id:#{row['old_section_id']}",
														method: :put,
														headers: default_headers,
														params: {'course_section[sis_section_id]' => row['new_section_id']})
				change_section_id.run
				puts "Successfully updated section #{row['new_section_id']}"
			else
				puts "Unable to locate section #{row['old_section_id']}"
			end
		end

	end
	hydra.queue(api_get_oldsection)
end

hydra.run

puts 'Finished processing file.'
