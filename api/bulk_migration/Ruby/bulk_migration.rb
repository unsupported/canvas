# WORKING AS OF NONE!

#------------------Edit these variables---------------------#
#Access token generated by an account admin
$auth_token = ''

#If your instance is utah.instructure.com, this is just 'utah'
$school_domain = ''

#The full path to the CSV mapping file
$mapping_file_path = "/path/to/file.csv"

#The full path to save the status report
$export_file_path = "/path/to/export/file/dir/"

#No need to edit this
$api_base_url = "https://#{$school_domain}.instructure.com/api/v1/"

#Change this to 'true' if you want to create the courses on the fly
#NOTE: this will require the course_name column of the csv file
$create_courses = false

#----------------------------------------------------------#
#  Don't edit from here unless you know what you are doing #
#----------------------------------------------------------#
#Required gems - INSTALL THESE BEFORE STARTING
require 'rubygems'
require 'json'
require 'typhoeus'
require 'csv'
require 'bearcat'

#------------------Get Course Info------------------------#
# - Pulls information from the CSV File
#---------------------------------------------------------#

def read_file_data
  #open mapping file
  CSV.foreach($mapping_file_path, headers: true) do |row|

    #Check that headers are correct
    if row['source'].nil? || row['sis_id'].nil?
      raise 'Valid CSV headers not found (Expecting source,sis_id)'
    else
      #If create courses is enabled, create the course before importing
      if $create_courses
        if row['course_name'].nil?
          raise 'Valid CSV headers not found (Expecting source,sis_id,course_name)'
        end
        create_course(row['sis_id'],row['course_name'])
      end

      migrate_content(row['source'],row['sis_id'])

    end
  end
end


#-------------------Create Course-------------------------#
# - Creates a course shell
#---------------------------------------------------------#
def create_courses(sis_id, course_name)

end

#------------------Migrate Content -----------------------#
# - Creates a course shell
#---------------------------------------------------------#
def migrate_content(source, sis_id)
  client = Bearcat::Client.new token: $auth_token,
                              prefix: "https://#{$school_domain}.instructure.com"

  
end

#------------------Generate Report------------------------#
# - Generates a status report
#---------------------------------------------------------#
def create_courses

end