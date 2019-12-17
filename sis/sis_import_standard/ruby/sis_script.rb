# Working as of 12/17/2019
require 'zip'
require 'date'
require 'json'
require 'typhoeus'
require 'fileutils'

#=======================================
# Edit this so you don't have to fill it in every time.
$access_token = ''
$domain = ''
$env = '' # Leave empty for production, or use 'test' or 'beta'
$source_folder = ''
$archive_folder = ''

# Don't edit from here down unless you know what you're doing.
#=======================================
$env != '' ? $env << '.' : $env
$test_url = "https://#{$domain}.#{$env}instructure.com/api/v1/accounts/self"
$endpoint_url = "#{$test_url}/sis_imports.json?import_type=instructure_csv"
$headers = { 'Authorization' => "Bearer #{$access_token}" }

# Make generic API call to test token, domain, and env.
test = Typhoeus.get($test_url, headers: $headers)
raise 'Error: The token, domain, or env variables are not set correctly' unless test.code == 200

# Methods to check if the source_folder works
raise "Error: source_folder isn't a directory, or can't be located." unless Dir.exist?($source_folder)
raise "Error: There are no CSV's in the source directory" unless Dir.entries($source_folder).detect { |f| f.match(/.*(.csv)/) }

unless Dir.exist?($archive_folder)
  Dir.mkdir $archive_folder
  puts "Created archive folder at #{$archive_folder}"
end

files_to_zip = []
Dir.foreach($source_folder) { |file| files_to_zip.push(file) }

$zipfile_name = "#{$source_folder}/archive.zip"
Zip::File.open($zipfile_name, Zip::File::CREATE) do |zipfile|
  files_to_zip.each do |file|
    zipfile.add(file, "#{$source_folder}/#{file}")
  end
end

# Push to the CSV API endpoint.
$upload = Typhoeus::Request.new(
  $endpoint_url,
  method: :post,
  headers: $headers,
  body: { attachment: File.new($zipfile_name, 'r') }
)
$upload.on_complete do |response|
  @job = JSON.parse(response.body)
  $id = @job['id']
  while @job['workflow_state'] == 'created' || @job['workflow_state'] == 'importing'
    puts 'importing'
    sleep(3)
    $import_status.run
  end
  puts 'Successfully uploaded files'
  timestamp = Time.now.to_s.gsub(/\s/, '-').gsub(/:/, '-')
  FileUtils.mv($zipfile_name, "#{$archive_folder}/archive-#{timestamp}.zip")
  FileUtils.rm Dir.glob("#{$source_folder}/*")
end

$import_status = Typhoeus::Request.new(
  "#{$test_url}/sis_imports/#{$id}",
  method: :get,
  headers: $headers
)
$import_status.on_complete do |response|
  @job = JSON.parse(response.body)
  if @job['processing_errors']
    puts "Processing Errors: #{@job['processing_errors']}"
    File.delete($zipfile_name)
    raise "An error occurred uploading this file. \n #{job}"
  end
end

$upload.run
