# Working as of 1/22/2018
require 'typhoeus'
require 'csv'
require 'json'

#----------------------------------------------------------------------------#
# Setting variables: token, domain, env, csv_file path, and grading_standard #
#----------------------------------------------------------------------------#

## access token
puts 'Enter a valid access token to perform the API calls within this script'
access_token = gets.chomp!

## domain
puts 'Enter the targeted domain: <domain>.instructure.com'
domain = gets.chomp!

## env
puts "For production, hit enter.  For Beta, 'beta' and for Test, 'test'"
env = gets.chomp!

## CSV file path
puts 'Enter the full file path to your csv_file'
csv_file = gets.chomp!

## grading_standard: https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index
puts 'Enter ID for the grading_standard to be set (integer)'
@grading_standard = gets.chomp!

#-----------------------------#
# Do not edit below this line #
#-----------------------------#

env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com/"
default_headers = { authorization: 'Bearer ' + access_token}

CSV.foreach(csv_file, {headers: true }) do |row|
  if row['sis_course_id'].nil?
    puts 'No data in sis_course_id field'
    raise 'Valid CSV headers not found (Expecting sis_course_id)'
  else
    sis_course_id = row['sis_course_id']
    response = Typhoeus.put(base_url + "api/v1/courses/sis_course_id:#{sis_course_id}",
							headers: default_headers,
                			params: {
                 			  'course[grading_standard_id]': @grading_standard
                 			}
     			)
    
    #parse JSON data to save in readable array
    data = JSON.parse(response.body)
    puts data
    puts "Grading standard set to ID " + data['grading_standard_id'].to_s
  end
end
