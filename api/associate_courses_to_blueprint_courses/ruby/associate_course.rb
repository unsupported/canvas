require 'byebug'
require 'colorize'
require 'typhoeus'
require 'io/console'
require 'csv'
require 'json'

# Create a 2-column CSV with headers course_id and blueprint_course_id

# Install required dependencies by running bundle install
# Run script with ruby associate_course.rb, it will prompt you to set values

# Note all your blueprint courses must be in a published state prior to running

def init
  puts 'Enter domain - e.g. domain in https://domain.instructure.com'
  @domain = gets.chomp!
  puts 'What environment should this run in? Hit enter for production, or type test or beta'
  @env = gets.chomp!
  @env != '' ? @env << '.' : @env
  puts 'Enter API token (input will be hidden)'
  @token = STDIN.noecho(&:gets).chomp!
  puts 'Enter path to Provisioning CSV - e.g. /Users/jdoe/Downloads/mapping.csv'
  @csv_path = gets.chomp!
end

def csv_to_arr
  hashes = []

  CSV.foreach(@csv_path, headers: true) do |row|
    hash = {}
    hash[:course_id] = row['course_id']
    hash[:blueprint_course_id] = row['blueprint_course_id']
    hashes << hash
  end

  csv = CSV.parse(File.open(@csv_path, 'r', &:read), headers: true)
  all_blueprint_course_ids = csv.map { |row| row['blueprint_course_id'] }.uniq!

  all_blueprint_course_ids.each do |bp_id|
    ids_to_add = []
    to_set = hashes.select { |x| x[:blueprint_course_id] == bp_id }
    to_set.each { |x| ids_to_add << x[:course_id] }
    ids_to_add.uniq!
    associate_course(ids_to_add, bp_id)
  end
end

def associate_course(ids_to_add, blueprint_course_id)
  url = "https://#{@domain}.instructure.com/api/v1/courses/#{blueprint_course_id}" \
          "/blueprint_templates/default/update_associations"
  auth = { authorization: "Bearer #{@token}" }
  body = { course_ids_to_add: ids_to_add.map(&:to_i) }
  resp = Typhoeus.put(url, headers: auth, body: body)
  if resp.code == 200
    puts resp.code.to_s.green
  else
    puts resp.code.to_s.red
  end
end

init
csv_to_arr
