# Working as of 09/07/2016
require 'rubygems'
require 'bundler/setup'

require 'typhoeus'
require 'csv'
require 'json'

################################# CHANGE THESE VALUES ###########################
csv_file = 'example_info.csv'     			# Use the full path /Users/XXXXX/Path/To/File.csv
access_token = ''				# your API token that was generated from your account user
domain = '' 						# domain.instructure.com, use domain only
env = '' 						  # Leave empty for production, or use beta or test.
output_csv = 'example_output.csv'         # put the full path to a blank csv file to have the errors written in.

############################## DO NOT CHANGE THESE VALUES #######################
env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com"

def start(csv_file, access_token, base_url, output_csv)
    hydra = Typhoeus::Hydra.new(max_concurrency: 20)
    CSV.foreach(csv_file, headers: true) do |row|
        if row.headers[0] != 'old_sis_user_id' || row.headers[1] != 'new_sis_user_id'
            puts 'First column needs to be old_user_id, second column needs to be new_login_id'
        else
            get_response = Typhoeus::Request.new("#{base_url}/api/v1/users/sis_user_id:#{row['old_sis_user_id']}/logins?per_page=100",
                                                 method: :get,
                                                 headers: { Authorization: "Bearer #{access_token}" })

            get_response.on_complete do |response|
                export_id = ''
                exported_sis_id = ''
                parsed_data = nil

                if response.code.eql?(200)
                    parsed_data = JSON.parse(response.body)
                    parsed_data.each do |login|
                        next unless login['sis_user_id'].eql?(row['old_sis_user_id'])
                        export_id = login['id'] unless nil
                        exported_sis_id = login['sis_user_id'] unless nil
                        break
                    end
                    if parsed_data && exported_sis_id.eql?(row['old_sis_user_id'])
                        # binding.pry
                        put_response = Typhoeus::Request.new("#{base_url}/api/v1/accounts/1/logins/#{export_id}",
                                                             method: :put,
                                                             headers: { Authorization: "Bearer #{access_token}", 'Content-Type' => 'application/x-www-form-urlencoded' },
                                                             params: { 'login[sis_user_id]' => row['new_sis_user_id'] })
                        # parse JSON data to save in readable array
                        put_response.on_complete do |response|
                            if response.code.eql?(200)
                                puts "Successfully updated sis_user_id for user #{exported_sis_id} to user #{row['new_sis_user_id']}"
                            else
                                puts response.body
                                puts "Unable to update sis_user_id for user #{exported_sis_id}. Trying again..."
                                hydra.queue(put_response)
                            end
                        end

                        hydra.queue(put_response)
                    else
                        puts "Exported sis_user_id is different than the old_user_sis_id #{row['old_sis_user_id']} row in the csv file"
                        # CSV.open(output_csv, 'a') do |csv|
                        #     csv << ['2', 'User', (row['old_sis_user_id']).to_s, 'has a different sis_user_id in Canvas than the sis_login_id']
                        # end
                    end
                else
                    if response.code.eql?(404)
                        puts "User #{row['old_sis_user_id']} does not exist in Canvas"
                        CSV.open(output_csv, 'a') do |csv|
                            csv << ['User', (row['old_sis_user_id']).to_s, 'does not exist in Canvas']
                        end
                    else
                        puts "Trouble connecting to the server while doing API call for user #{row['old_sis_user_id']}. Trying again..."
                        hydra.queue(get_response)
                    end
                end
            end
            hydra.queue(get_response)
       end
    end
    hydra.run
end

start(csv_file, access_token, base_url, output_csv)
