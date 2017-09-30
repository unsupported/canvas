# LAST WORKING AS OF 09/30/2017

require 'csv'
require 'json'
require 'byebug'
require 'typhoeus'
require 'ruby-progressbar'

### CHANGE THESE VALUES

@domain = '' # e.g. 'domain' in 'https://domain.instructure.com'
@token = '' # api token for account admin user
@env = '' # leave blank for production, or use test or beta.

# =======================
# Do not edit from here unless you know what you're doing.

@env != '' ? @env << '.' : @env
@base_url = "https://#{@domain}.#{@env}instructure.com/api/v1"

def fetch_outcomes
  outcomes = []
  ids = [*1..2500]

  puts 'Fetching outcomes...'

  progressbar = ProgressBar.create(total: ids.count)

  ids.each do |id|
    outcome = {}
    resp = Typhoeus.get(@base_url + '/outcomes/' + id.to_s,
                        headers: { authorization: "Bearer #{@token}" })
    next unless resp.code == 200
    data = JSON.parse(resp.body)

    outcome[:outcome_group_vendor_guid] = ''
    outcome[:parent_outcome_group_vendor_guid] = ''

    outcome[:vendor_guid]        = data['vendor_guid']
    outcome[:title]              = data['title']
    outcome[:ratings]            = data['ratings']
    outcome[:description]        = data['description']
    outcome[:calculation_method] = data['calculation_method']
    outcome[:calculation_int]    = data['calculation_int']
    outcome[:mastery_points]     = data['mastery_points']
    outcomes << outcome

    progressbar.increment
  end
  puts 'Preparing CSV...'
  print_to_csv(outcomes)
end

def create_csv
  headers = 'vendor_guid,outcome_group_vendor_guid,parent_outcome_group_vendor_guid,' \
  "title,description,calculation_method,calculation_int,mastery_points,0,1,2,3,4,5,6,7,8,9,10\n"

  File.open("./#{@domain}_outcomes_export_log.csv", 'w'){ |x| x.write(headers) }
end

def print_to_csv(outcomes)
  headers = %w[vendor_guid outcome_group_vendor_guid parent_outcome_group_vendor_guid
               title description calculation_method calculation_int mastery_points
               0 1 2 3 4 5 6 7 8 9 10]
  outcomes.each do |oc|
    CSV.open("./#{@domain}_outcomes_export_log.csv",'a') do |csv|
      row = CSV::Row.new(headers, [])
      row['vendor_guid']                      = oc[:vendor_guid]
      row['outcome_group_vendor_guid']        = oc[:outcome_group_vendor_guid]
      row['parent_outcome_group_vendor_guid'] = oc[:parent_outcome_group_vendor_guid]
      row['title']                            = oc[:title]
      row['description']                      = oc[:description]
      row['calculation_method']               = oc[:calculation_method]
      row['calculation_int']                  = oc[:calculation_int]
      row['mastery_points']                   = oc[:mastery_points]
      oc[:ratings].each do |rating|
        description             = rating['description']
        points_as_int           = rating['points'].to_i
        row[points_as_int.to_s] = description
      end
      csv << row
    end
  end
  puts 'Done'
end

create_csv
fetch_outcomes
