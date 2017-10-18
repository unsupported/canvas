#Working as of 10/18/2017
require 'typhoeus'
require 'csv'
require 'json'

################################# CHANGE THESE VALUES ###########################
@access_token = ''        #your API token that was generated from your account user
@domain = ''            #domain.instructure.com, use domain only
@env = ''               # leave empty for production, or use beta or test
@csv_file = ''          #Use the full path /Users/XXXXX/Path/To/File.csv
############################## DO NOT CHANGE THESE VALUES #######################

@env != '' ? @env << '.' : @env
@base_url = "https://#{@domain}.#{@env}instructure.com/"


CSV.foreach(@csv_file, {headers: true}) do |row|
  if row['sis_course_id'].nil?
    puts 'No data in course SIS id field'
    raise 'Valid CSV headers not found (Expecting sis_course_id)'
  else
    sis_course_id = row['sis_course_id']
    response = Typhoeus.put(
            @base_url + "api/v1/accounts/1/courses",
            headers: {:authorization => 'Bearer ' + @access_token},
            params: {
                'course_ids[]' => "sis_course_id:#{sis_course_id}",
                :event => "delete"
            }
        )

    #parse JSON data to save in readable array
    data = JSON.parse(response.body)
    puts data
  end
end