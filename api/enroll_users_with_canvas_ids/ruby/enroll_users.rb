 # Working as of 03/31/2016
 # Enroll users in sections using Canvas IDs instead of SIS IDs.
 #
 # This script allows a user to be enrolled in a section without the need for the user nor section to have an SIS ID assigned.
 #
 # Notes:
 # => This script is only for ADDING users. It will not remove enrollments.
 # => The script alters the role information if you are using the student, ta, teacher or desgner coure role to match the expected role names
 #
 # Sample input CSV format:
 # canvas_user_id,canvas_section_id,role
 # 12,34245,student

require 'csv'
require 'typhoeus'
require 'json'
#------------------Replace these values-----------------------------#

access_token = ''				#Enter the access token Canvas provides in your user settings
url = ''  							#Enter the full URL to the domain you want to merge files. This is the full Canvas URL exculding the https:// such as canvas.instructure.com
csv_file = '' 					#Enter the full path to the file. /Users/XXXXXX/Path/To/File.csv

#-------------------Do not edit below this line---------------------#
# First column is user account that will be merged into second column. #
url = "https://#{url}"
unless Typhoeus.get(url).code == 200 || 302
	raise 'Unable to run script, please check token, and/or URL.'
end

unless File.exists?(csv_file)
	raise "Can't locate the CSV file."
end

hydra = Typhoeus::Hydra.new(max_concurrency: 10)

CSV.foreach(csv_file, {:headers => true}) do |row|
	case row['role'].downcase
	when "student"
		user_role = "StudentEnrollment"
	when "teacher"
		user_role = "TeacherEnrollment"
	when "ta"
		user_role = "TaEnrollment"
	when "designer"
		user_role = "DesignerEnrollment"
	else
		user_role = row['role']
	end

	api_call = "#{url}/api/v1/sections/#{row['canvas_section_id']}/enrollments"
	canvas_api = Typhoeus::Request.new(api_call,
										method: :post,
										params: {'enrollment[user_id]' => row['canvas_user_id'],
															'enrollment[role]' => user_role,
															'enrollment[enrollment_state]' => 'active',
															'enrollment[notify]' => 0},
										headers: { "Authorization" => "Bearer #{access_token}" })
		canvas_api.on_complete do |response|
			if response.code == 200
				puts "Enrolled user #{row['canvas_user_id']} into section #{row['canvas_section_id']} as a #{row['role']}"
			else
				puts "Unable to enroll user #{row['canvas_user_id']} into section #{row['canvas_section_id']} as a #{row['role']}. (Code: #{response.code}) #{response.body}"

			end
		end
	hydra.queue(canvas_api)
end
hydra.run

puts 'Successfully enrolled users.'
