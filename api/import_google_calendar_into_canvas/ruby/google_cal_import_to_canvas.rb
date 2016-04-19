require 'rubygems'
require 'icalendar'
require 'date'
require 'typhoeus'
require 'open-uri'
require 'json'
require 'cgi'

# note will create calendar event times based upon the user's token
# Variables that are required to be populated.
canvas_url = ''                               #https://canvas.instructure.com/
api_token = ''                                #canvas API Token
course_id = ''                                #canvas course ID, shown in the URL and will be an integer
cal_file = File.open('')                      #full path to .ICS File
tz = URI.escape("Central Time (US & Canada)") #edit the timezone

#--------------------- DO NOT EDIT -----------------------------

cals = Icalendar.parse(cal_file)
hydra = Typhoeus::Hydra.new(max_concurrency: 10)
cals.each do |cal|
  events = cal.events.each do |event|

    puts "Name: " + event.summary
    cal_title = CGI.escape(event.summary)
    puts "Start: " + event.dtstart.to_s
    cal_start_at = CGI.escape(event.dtstart.to_s)
    puts "End: " + event.dtend.to_s
    cal_end_at = URI.escape(event.dtend.to_s)
    puts event.location
    cal_loc = event.location ? CGI.escape(event.location) : ''
    #cal_desc = event.description ? URI::encode(event.description) : ''

    request = Typhoeus::Request.new(
      "#{canvas_url}/api/v1/calendar_events?calendar_event[context_code]=course_#{course_id}&calendar_event[title]=#{cal_title}&calendar_event[start_at]=#{cal_start_at}&calendar_event[end_at]=#{cal_end_at}&calendar_event[location_name]=#{cal_loc}&calendar_event[time_zone_edited]=#{tz}",
      method: :post,
      headers: {
        Authorization: "Bearer #{api_token}",
        Accept: "application/JSON"
      }
    )
    request.on_complete do |response|
      if response.success?
        puts "Success!"
      elsif
        puts "Oops: " + response.body
      end
    end
    hydra.queue(request)
  end
  hydra.run
end
