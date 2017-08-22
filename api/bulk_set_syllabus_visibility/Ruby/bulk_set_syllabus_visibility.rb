#Working as of March 7, 2017
require 'typhoeus'
require 'csv'
require 'json'

################################################################################
################# USER AREA: COMPLETE THE EQUIVALENCIES BELOW ##################

### Replace ONLY underscores
### Leave in single quotations surrounding the underscores (where pertinent)

@access_token = '___'
  #Replace underscores with API token generated from account user in Canvas

@domain = '___'
  #Replace underscores with the sub-domain for your Canvas instance
  #Example: If Canvas URL is canvasstuff.instructure.com, use canvasstuff

@env = nil
  #To use script with Production, leave as-is
  #For use with test/beta environments, replace nil with test or with beta

@csv_file = '___'
  #Replace underscores with the full file path to the CSV file being used
  #Example File Path: /Users/XXXXX/Path/To/File.csv

@public_visibility = ___
  #Replace the underscores with true or false (see combinations key below)

@institution_visibility = ___
  #Replace underscores with true or false (see combinations key below)

#~~~~~~~~~~~~# True/False Combinations Key #~~~~~~~~~~~~#
#To set course(s) visibility to "Course":
  #Set @public_visibility=false and @institution_visibility=false
  #Only those who are enrolled AND authenticated will see the syllabus

#To set course(s) visibility to "Institution":
  #Set @public_visibility=false and @institution_visibility=true
  #Anyone who is authenticated will see the syllabus

#To set course(s) visibility to "Public":
  #Set @public_visibility=true
  #CAVEAT:
    #If @public_visibility=true BUT @institution_visibility=false:
      #ONLY enrolled users and UNauthenticated users will see the syllabus
      #Users who are authenticated but not enrolled won't see the syllabus
    #If @public_visibility=true AND @institution_visibility=true:
      #Anyone can view the syllabus under these conditions.
      #Same result as setting "Public" visibility from the course settings UI
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

########## END OF USER AREA: DO NOT EDIT ANY VALUES BEYOND THIS POINT ##########
################################################################################

@env ? @env << "." : @env
@base_url = "https://#{@domain}.#{@env}instructure.com/"


CSV.foreach(@csv_file, {headers: true}) do |row|
  if row['canvas_course_id'].nil?
    puts 'No data in Canvas course id fields'
    raise 'Valid CSV headers not found (Expecting canvas_course_id)'
  else
    canvas_course_id = row['canvas_course_id']
    response = Typhoeus.put(
            @base_url + "api/v1/courses/" + canvas_course_id,
            headers: {:authorization => 'Bearer ' + @access_token , 'Content-Type' => 'application/x-www-form-urlencoded' },
            body: {
                course: {
                  public_syllabus: @public_visibility,
                  public_syllabus_to_auth: @institution_visibility
                }
            }
        )

    #parse JSON data to save in readable array
    data = JSON.parse(response.body)
    puts data
  end
end
