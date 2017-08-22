#Working as of 03/30/2016
# Edit these below, or you will be prompted in the CLI
access_token = ''          #your token acquired in your canvas user profile
domain = ''                #the domain of your URL, such as school in school.instructure.com
env = ''                   #leave empty for prod, or use test or beta
input_file = ''            #input file for courses to export
output_file = ''            #output file for courses that have been exported
#============
# Don't edit from here down unless you know what you're doing.

require 'typhoeus'
require 'csv'
require 'json'

unless access_token
  puts "what is your access token?"
  access_token = gets.chomp
end

unless domain
  puts "what is your Canvas domain?"
  domain = gets.chomp
end

unless input_file
  puts "where is your input CSV, listing courses to migrate, located?"
  input_file = gets.chomp
end

unless output_file
  puts "where would you like to output your CSV to?"
  output_file = gets.chomp
end

raise "Error: can't locate the input CSV" unless File.exist?(input_file)

unless File.exist?(output_file)
  CSV.open(output_file, 'wb') do |csv|
    csv << ["course_id", "export_url"]
  end
end

env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com/api/v1"
default_header = { Authorization: "Bearer #{access_token}" }

CSV.foreach(input_file, { headers: true }) do |row|
  url = "#{base_url}/courses/#{row['course_id']}/content_exports"
  export_course = Typhoeus::Request.new(url, headers: default_header, method: :post,
                                        params: { export_type: 'common_cartridge', skip_notifications: true })

  export_course.on_complete do |response|
    response_body = JSON.parse(response.body)
    while (response_body['workflow_state'] == 'created' || response_body['workflow_state'] == 'exporting' ) && (response_body['progress'] != 100)
      puts 'exporting'
      sleep(5)
      export_status = Typhoeus.get("#{url}/#{response_body['id']}", headers: default_header)
      response_body = JSON.parse(export_status.body)
    end

    if response_body['processing_errors']
      puts "An error occurred exporting this job. -- #{response_body}"
    end

    if response_body['processing_warnings']
      puts "Processing Warning: #{response_body['processing_errors']}"
    end

    CSV.open(output_file, 'ab') do |csv|
      csv << ["#{response_body['course_id']}", "#{response_body['attachment']['url']}"]
    end
  end
  export_course.run
end

puts "Exported Files."
