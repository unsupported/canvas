# Working as of 11/25/2016

# This script corrects 2 issues facing Schoology imports after a package has been uploaded to Canvas.
#    - Content pages are imported as HTML files. This script will convert them
#      to native Canvas content pages.
#    - Folder names are stripped and replaced with 'CCRESXXXXXX' format. This
#      script converts them back to their correct folder name

# This script assumes that the Schoology Common Cartridge package has been imported into courses.
# This script will iterate row-by-row through a CSV mapping document, updating course content as
# found in the ims manifest file.

# Create a 2 column CSV mapping document with the following headers:
# course_id - should be the Canvas course id (NOT the SIS ID)
# folder_name - should be the name of the content package that contains the ims manifest file (without the .imscc extension)

# Save your CSV file to the same directory where your .imscc exports are. This script will convert all
# imscc files to zips, unzip the file, then parse both the Canvas course and the export package, correcting
# the above listed issues.

# Install dependencies by running bundle install
# Run script with ruby xmlparser.rb and set domain, file path and token

require 'csv'
require 'json'
require 'zip'
require 'nokogiri'
require 'typhoeus'
require 'bearcat'
require 'byebug'
require 'colorize'
require 'fileutils'
require 'active_support'
require 'active_support/core_ext'

def kickoff
  puts 'Enter Canvas domain (e.g. stanford in https://stanford.instructure.com)'
  @domain = gets.chomp!.downcase
  puts 'Enter path to CSV mapping file (e.g. path/to/file.csv)'
  @file_path = gets.chomp!
  @parent_folder = (File.dirname @file_path) + "/"
  puts 'Enter your API token'
  @token = gets.chomp!
end

def get_csv # Iterates through 2 column CSV file. (course_id, folder_name)
  begin
    CSV.foreach(@file_path, headers: true) do |row|
      if row['course_id'].nil?
        puts 'No data in course_id'
        raise 'Valid CSV headers not found (no data in course_id)'
      elsif row['folder_name'].nil?
        puts 'No data in folder_name'
        raise 'Valid CSV headers not found (no data in folder_name)'
      else
        @course_id = row['course_id']
        folder = row['folder_name'].gsub('.imscc', '') # smarter, so it will always gather just folder name.
        xml_file_path = @parent_folder + folder + "/imsmanifest.xml"
        zip_folder = @parent_folder + folder + ".zip"
        destination = @parent_folder + folder
        convert_package
        unzip_package(zip_folder, destination)
        parse_manifest(xml_file_path, folder)
      end
    end
  rescue StandardError => e
    puts "Error: #{e}"
  end
end

def convert_package
  Dir.glob("#{@parent_folder}*.imscc").each do |f|
    FileUtils.mv f, "#{File.dirname(f)}/#{File.basename(f,'.*')}.zip"
  end
end

def unzip_package(file, destination) # This step requires that the file has been converted from imscc to a zip file.  Unzips package.
  puts "unzipping package... #{file}"
  FileUtils.mkdir_p(destination)
  Zip::File.open(file) do |zip_file|
    zip_file.each do |f|
      fpath = File.join(destination, f.name)
      zip_file.extract(f, fpath) unless File.exist?(fpath)
    end
  end
end

def parse_manifest(xml_file_path, folder) # Searches manifest for content pages and file paths
  doc = File.open("#{xml_file_path}") { |f| Nokogiri::XML(f) }
  filepaths = []
  pages = doc.xpath('.//xmlns:resource[contains(@type,"associatedcontent/imscc_xmlv1p2/learning-application-resource")]')
  pages.each_with_index do |ele, index|
    node = ele.attribute('href')
    path = node.value
    filepaths << path
  end
  filepaths.each do |filepath|
    content = File.open("#{@parent_folder}#{folder}/#{filepath}", "rb").read
    res_name = filepath.split('/')[0]
    path = doc.xpath(".//xmlns:item[contains(@identifierref, '#{res_name}')]")
    page_title = path.text
    create_page(content, page_title)
  end
  store_folders doc # Saves folder id's to an array
end

def create_page(content, page_title) # Creates a Canvas page when correct identifier in manifest is found
  response = Typhoeus.post(
  "https://#{@domain}.instructure.com/api/v1/courses/#{@course_id}/pages",
  headers: { authorization: "Bearer #{@token}" },
  body: {
    wiki_page: {
      title: "#{page_title}",
      body: "#{content}"
      }
    }
  )
  if response.code == 200
    puts "Page #{page_title}" + " successfully created".green
  else
    puts "Page #{page_title}" + " failure creating page".red
  end
end

def store_folders(doc) # Stores legacy/imscc folders to an array of hashes for later reference
  folders = []
  node = doc.xpath('.//xmlns:item[@identifierref]')
  node.each do |item|
    folder = {}
    attributes = item.attributes
    children = item.children
    meta = children.children
    folder[:imscc] = attributes['identifierref'].value
    folder[:correct] = meta.text
    folders << folder
  end
  parse_canvas_folders(folders)
end

def parse_canvas_folders(folders) # Gathers folder names in a Canvas course and compares them against the Hashes in the folders array
  client = Bearcat::Client.new token: @token, prefix: "https://#{@domain}.instructure.com"
  resp = client.list_course_folders(@course_id).all_pages!
  canvas_folders = resp.to_a
  canvas_folders.each do |folder|
    folder_id = folder['id']
    folder_name = folder['name']
    results = folders.select { |f| f[:imscc].to_s ==  "#{folder_name}" }
    item = results.first
    correct_name = item.try(:[], :correct)
    unless correct_name.nil?
      replace_folder_name(folder_id, correct_name)
    end
  end
end

def replace_folder_name(folder_id, correct_name) # Replaces the imscc folder identifier with the folder's appropriate name
  response = Typhoeus.put(
    "https://#{@domain}.instructure.com/api/v1/folders/#{folder_id}",
    headers: { authorization: "Bearer #{@token}", 'Content-Type': "application/x-www-form-urlencoded" },
    body: {
      name: correct_name
    }
  )
  if response.code == 200
    puts "folder id " + folder_id.to_s + " successfully renamed".green
  else
    puts "folder id " + folder_id.to_s + " failure".red
  end
end

kickoff
get_csv

# < /> with <3 by Colin Cromar, ccromar@instructure.com
