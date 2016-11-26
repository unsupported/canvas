require 'bearcat'
require 'csv'
# WORKING AS OF 11/25/2016
# Account-Level Question Bank QTI Importer
# https://canvas.instructure.com/doc/api/content_migrations.html
# https://canvas.instructure.com/doc/api/file.file_uploads.html

# Create a 1-column CSV mapping file and save it in the same directory as the QTI
# you wish to import. You should have 'file_name' as your header, and it should
# contain a list of filenames to import.

def kickoff
  puts 'Enter your Canvas URL ~> e.x. https://canvas.instructure.com'
  @canvas_url = gets.chomp!
  puts 'Enter the Account ID to import QTI files to (numerical ID, not SIS)'
  @account_id = gets.chomp!
  puts 'Enter your API token'
  @token = gets.chomp!
  puts 'Enter the full path/to/file of your CSV filenames file-
    e.g. /Users/jsmith/Downloads/mapping.csv'
  @csv = gets.chomp!
  @parent_folder = (File.dirname @csv) + "/"
end

def get_csv file_path
  begin
    CSV.foreach(file_path, headers: true) do |row|
      if row['file_name'].nil?
        puts 'No data in file_name'
        raise 'Valid CSV headers not found (no data in file_name)'
      else
        file_name = row['file_name']
        create_migration file_name
      end
    end
  rescue StandardError => e
      puts "Error: #{e}"
      puts e.backtrace
  end
end

def create_migration file_name
  api_path = "#{@canvas_url}/api/v1/accounts/#{@account_id}/content_migrations"
  file_path = @parent_folder + file_name
  params = { migration_type: 'qti_converter', pre_attachment: { name: "#{file_name}" } }
  client = Bearcat::Client.new token: @token, prefix: @canvas_url
  response = client.upload_content_package(api_path, file_path, params)
  declare_response = client.declare_file(api_path, client.file_params(file_path).merge(params))
  if declare_response['workflow_state'] == 'pre_processing'
    puts "Migration created: uploading #{file_name} to #{@canvas_url}/accounts/#{@account_id}"
  else
    puts "Migration failed for #{file_name}"
  end
end

kickoff
get_csv @csv
