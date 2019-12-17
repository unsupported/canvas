# Working as of 12/17/2019
require 'zip'
require 'date'
require 'json'
require 'typhoeus'
require 'fileutils'
require 'io/console'

## TOKEN
puts 'Enter a valid access token to perform the API calls within this script'
token = STDIN.noecho(&:gets).chomp!

## DOMAIN
puts 'Enter the domain, EX: <domain>.instructure.com'
domain = gets.chomp!.downcase

## ENV
puts "For prod, hit enter. For Beta, enter 'beta'. For Test, enter 'test'"
env = gets.chomp!.downcase
env != '' ? env << '.' : env

## SOURCE FOLDER
puts 'Enter the full path to the directory where your SIS import CSV files are located'
source_folder = gets.chomp!

## ARCHIVE FOLDER
puts 'Enter the full path to the directory where the current SIS import files will be stored after upload'
archive_folder = gets.chomp!

test_url = "https://#{domain}.#{env}instructure.com/api/v1/accounts/self"
endpoint_url = "#{test_url}/sis_imports.json?import_type=instructure_csv"
headers = { 'Authorization': "Bearer #{token}" }

# Make generic API call to test token, domain, and env.
test = Typhoeus.get(test_url, headers: headers)
raise 'Error: The token, domain, or env variables are not set correctly' unless test.code == 200

# Methods to check if the source_folder works
raise "Error: source_folder isn't a directory, or can't be located." unless Dir.exist?(source_folder)
raise "Error: There are no CSV's in the source directory" unless Dir.entries(source_folder).detect { |f| f.match(/.*(.csv)/) }

Dir.mkdir(archive_folder) unless Dir.exist?(archive_folder)

files_to_zip = []
Dir.foreach(source_folder) { |file| files_to_zip.push(file) }

zipfile_name = "#{source_folder}/archive.zip"
Zip::File.open(zipfile_name, Zip::File::CREATE) do |zipfile|
  files_to_zip.each do |file|
    zipfile.add(file, "#{source_folder}/#{file}")
  end
end

# Push to the CSV API endpoint.
upload = Typhoeus::Request.new(
  endpoint_url,
  method: :post,
  headers: headers,
  body: { attachment: File.new(zipfile_name, 'r') }
)

import_status = Typhoeus::Request.new(
  "#{test_url}/sis_imports/#{$id}",
  method: :get,
  headers: headers
)

import_status.on_complete do |response|
  @job = JSON.parse(response.body)
  if @job['processing_errors']
    puts "Processing Errors: #{@job['processing_errors']}"
    File.delete(zipfile_name)
    raise "An error occurred uploading this file. \n #{job}"
  end
end

upload.on_complete do |response|
  @job = JSON.parse(response.body)
  $id = @job['id']
  @import_check = import_status.run
  while @job['workflow_state'] == 'created' || @job['workflow_state'] == 'importing'
    puts 'importing'
    sleep(3)
    @import_check
  end
  puts 'Successfully uploaded files'
  timestamp = Time.now.to_s.gsub(/\s/, '-').gsub(/:/, '-')
  FileUtils.mv(zipfile_name, "#{archive_folder}/archive-#{timestamp}.zip")
  FileUtils.rm Dir.glob("#{source_folder}/*")
end

upload.run
