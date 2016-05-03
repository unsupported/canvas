#Working as of 03/30/2016
require 'typhoeus'
require 'csv'
require 'json'

######################### Edit these variables ##########################
access_token = '' 					#Access token for the user to run the API call
domain = ''									#Domain of the institution to run against ex. https://domain.instructre.com (use only the domain)
env = nil										#Leave nil for prod, or enter test or beta
csv_filename = ''						#Full path the CSV file /full/path/to/the/file.csv
########################### Do not edit past this line ##################

default_headers = {"Authorization" => "Bearer #{access_token}"}
env ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com/"

hydra = Typhoeus::Hydra.new(max_concurrency: 20)
CSV.foreach(csv_filename, { headers: true }) do |row|

	get_request = Typhoeus::Request.new(base_url + "api/v1/courses/sis_course_id:#{row['course_id']}",
									   headers: default_headers,
									   method: :get)

	get_request.on_complete do |response|
		if response.success?
			update = Typhoeus::Request.new(base_url + "api/v1/courses/sis_course_id:#{row['course_id']}",
								  headers: default_headers,
								  	  method: :put,
								  	  params: { 'course[storage_quota_mb]' => row['quota'].to_i })
						hydra.queue(update)
		elsif response.timed_out?
			puts "Response timed out"
		elsif response.code == 0
			puts "Could not get a response"
		else
			puts "HTTP request failed: " + response.code.to_s + " for course " + row['course_id']
		end
	end
hydra.queue(get_request)
end
hydra.run
puts "Updated all courses"

#    if (get_response.code == 200 && get_response.body['storage_quota_mb'] * 1000000.to_i < @file_size)
#      size_increase = Unirest.put("https://#{@domain}.#{@env}instructure.com/api/v1/courses/sis_course_id:#{@course_id}", parameter
#         'course[storage_quota_mb]' => ((@file_size + 5000000) / 1000000).to_i })
#     elsif (get_response.code == 200 && get_response.body['storage_quota_mb'] * 1000000 > @file_size)
#     else
#       create_course = Unirest.post("https://#{@domain}.#{@env}instructure.com/api/v1/accounts/self/courses",
#                                    parameters: { 'account_id' => 'self',
#                                      'course[name]' => @course_name,
#                                      'course[sis_course_id]' => @course_id,
#                                      'course[storage_quota_mb]' => (@file_size + 5000000) / 1000000.to_i })
#     end
