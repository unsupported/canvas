#Working as of August 22, 2017
require 'typhoeus'
require 'csv'
require 'json'

################################################################################
################# USER AREA: COMPLETE THE EQUIVALENCIES BELOW ##################

### Replace ONLY underscores
### Do not replace the single quotations surrounding the underscores

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

@is_announcement = '___'
  #Replace underscores with TRUE if you want to post an announcement
  #Replace underscores with FALSE if you want to post a discussion

@post_title = '___'
  #Replace underscores with the desired title for your Discussion/Announcement

@post_body = '___'
  #Replace underscores with the message body for your Discusssion/Announcement

@published = '___'
  #Replace underscores with TRUE to publish your post.
  #Use FALSE to make the post in an unpublished draft state.

########## END OF USER AREA: DO NOT EDIT ANY VALUES BEYOND THIS POINT ##########
################################################################################

@env ? @env << "." : @env
@base_url = "https://#{@domain}.#{@env}instructure.com/"


CSV.foreach(@csv_file, {headers: true}) do |row|
  if row['canvas_course_id'].nil?
    puts 'No data found in necessary canvas_course_id column'
    raise 'Valid CSV headers not found (Expecting canvas_course_id)'
  else
    canvas_course_id = row['canvas_course_id']
    response = Typhoeus.post(
            @base_url + "api/v1/courses/" + canvas_course_id + "/discussion_topics/",
            headers: {
                      :authorization => 'Bearer ' + @access_token , 'Content-Type' => 'application/x-www-form-urlencoded'
                    },
            body: {
                  :is_announcement => @is_announcement,
                  :title => @post_title,
                  :message => @post_body,
                  :published => @published
                  }
        )
    #parse JSON data to save in readable array
    data = JSON.parse(response.body)
    puts data
  end
end
