#Working as of 03/30/2016
require 'typhoeus'
require 'csv'
require 'json'

################### Change these values only ##################
access_token = ''				#Your access token for Canvas
domain = ''							#The should be the first part of the url
env = ''								#Either blank for prod, or type test or beta
csv_file = ''						#The full path to the location of the mapping file /full/path/to/the/file.csv
################### Do not change these #######################

default_headers = { 'Authorization' => "Bearer #{access_token}"}

hydra = Typhoeus::Hydra.new(max_concurrency: 40)

env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com/"

CSV.foreach(csv_file, {headers: true}) do |row|
	if row.headers[0] != 'canvas_course_id' || row.headers[1] != 'new_course_id'
		puts "First column needs to be 'canvas_course_id', and second row needs to be 'new_course_id'."
	else
	get_course = Typhoeus::Request.new(base_url + "api/v1/accounts/self/courses/#{row['canvas_course_id']}",
									  method: :get,
									  headers: default_headers)
	get_course.on_complete do |response|
		if response.success?
			update_course = Typhoeus::Request.new(base_url + "api/v1/courses/#{row['canvas_course_id']}",
												  method: :put,
												  headers: default_headers,
												  params: { 'course[sis_course_id]' => row['new_course_id']})
				update_course.on_complete do |response|
					if response.success?
						puts "Updated old course number of #{row['canvas_course_id']} with SIS ID of #{row['new_course_id']}"
					elsif response.timed_out?
				        puts "Unable to find the course #{row['canvas_course_id']}, response timed out"
					elsif response.code == 0
				        puts response.return_message
					else
				    	puts "HTTP request failed: " + response.code.to_s
					end
				end
				hydra.queue(update_course)
		elsif response.timed_out?
			puts "Unable to find the course #{row['canvas_course_id']}, response timed out"
		elsif response.code == 0
			puts response.return_message
		else
			puts "HTTP request failed: " + response.code.to_s
		end
	end
	hydra.queue(get_course)
end
	hydra.run
end
	puts 'Completed blank course SIS updates'
