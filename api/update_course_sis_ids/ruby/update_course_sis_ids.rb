#Working as of 03/30/2016
require 'typhoeus'
require 'csv'
require 'json'

################################# CHANGE THESE VALUES ###########################
access_token = ''				#your API token that was generated from your account user
domain = '' 						#domain.instructure.com, use domain only
env = nil 							#Leave nil if pushing to Production
csv_file = ''     			#Use the full path /Users/XXXXX/Path/To/File.csv
############################## DO NOT CHANGE THESE VALUES #######################

default_headers = {"Authorization" => "Bearer #{access_token}"}
env ? env << "." : env
base_url = "https://#{domain}.#{env}instructure.com/"
hydra = Typhoeus::Hydra.new(max_concurrency: 20)

CSV.foreach(csv_file, {headers: true}) do |row|
	if row.headers[0] != 'old_course_id' || row.headers[1] != 'new_course_id'
		puts 'First column needs to be old_course_id, and second column needs to be new_course_id.'
	else
	api_get_oldcourse = Typhoeus::Request.new("#{base_url}/api/v1/courses/sis_course_id:#{row['old_course_id']}",
										  headers: default_headers)
		api_get_oldcourse.on_complete do |response|
			if response.code == 200
				change_course_id = Typhoeus::Request.new("#{base_url}/api/v1/courses/sis_course_id:#{row['old_course_id']}",
														method: :put,
														headers: default_headers,
														params: {'course[sis_course_id]' => row['new_course_id']})
				change_course_id.run
				puts "Successfully updated course #{row['new_course_id']}"
			else
				puts "Unable to locate course #{row['old_course_id']}"
			end
		end

	end
	hydra.queue(api_get_oldcourse)
end

hydra.run

puts 'Finished processing file.'
