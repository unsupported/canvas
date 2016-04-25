require 'fileutils'
require 'date'
require 'json'
require 'unirest'
require 'zip'

#=======================================
# Edit this so you don't have to fill it in every time.
access_token = nil
domain = nil
env = nil # production (leave as nil), "test" or "beta"
source_folder = nil
archive_folder = nil

# Don't edit from here down unless you know what you're doing.
#=======================================
env ? env << "." : env
test_url = "https://#{domain}.#{env}instructure.com/api/v1/accounts/self"
endpoint_url = "#{test_url}/sis_imports.json?import_type=instructure_csv"

# Make generic API call to test token, domain, and env.
test = Unirest.get(test_url, headers: { "Authorization" => "Bearer #{access_token}" })

unless test.code == 200
	raise "Error: The token, domain, or env variables are not set correctly"
end

# Methods to check if the source_folder works
unless Dir.exists?(source_folder)
	raise "Error: source_folder isn't a directory, or can't be located."
end

unless Dir.entries(source_folder).detect {|f| f.match /.*(.csv)/}
	raise "Error: There are no CSV's in the source directory"
end

unless Dir.exists?(archive_folder)
	Dir.mkdir archive_folder
	puts "Created archive folder at #{archive_folder}"
end

files_to_zip = []
Dir.foreach(source_folder) { |file| files_to_zip.push(file) }

zipfile_name = "#{source_folder}/archive.zip"
Zip::File.open(zipfile_name, Zip::File::CREATE) do |zipfile|
	files_to_zip.each do |file|
		zipfile.add(file, "#{source_folder}/#{file}")
	end
end

#Push to the CSV API endpoint.
upload = Unirest.post(endpoint_url,
	headers: {
		"Authorization" => "Bearer #{access_token}"
  },
	parameters: {
		attachment: File.new(zipfile_name, "r")
	}
)
job = upload.body

import_status_url = "#{test_url}/sis_imports/#{job['id']}"

while job["workflow_state"] == "created" || job["workflow_state"] == "importing"
	puts "importing"
	sleep(3)

  import_status = Unirest.get(import_status_url,
  	headers: {
  	  "Authorization" => "Bearer #{access_token}"
    }
  )
	job = import_status.body
end

if job["processing_errors"]
	File.delete(zipfile_name)
	raise "An error occurred uploading this file. \n #{job}"
end

if job["processing_warnings"]
	puts "Processing Errors: #{job["processing_errors"]}"
end

puts "Successfully uploaded files"
timestamp = Time.now.to_s.gsub(/\s/, '-').gsub(/:/, '-')
FileUtils.mv(zipfile_name, "#{archive_folder}/archive-#{timestamp}.zip")
FileUtils.rm Dir.glob("#{source_folder}/*")
