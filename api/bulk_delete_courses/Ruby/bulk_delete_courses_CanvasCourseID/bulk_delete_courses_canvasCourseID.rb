# Working as of 10/18/2017
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
  if row['canvas_course_id'].nil?
    puts 'No data in canvas_course_id field'
    raise 'Valid CSV headers not found (Expecting canvas_course_id)'
  else
    canvas_course_id = row['canvas_course_id']
    response = Typhoeus.delete(
            @base_url + "api/v1/courses/#{canvas_course_id}",
            headers: {:authorization => 'Bearer ' + @access_token},
            body: {
                    :event => "delete"
            }
        )

    #parse JSON data to save in readable array
    data = JSON.parse(response.body)
    puts data
  end
end