# Working as of 09/07/2016
require 'typhoeus'
require 'csv'
require 'json'

################################# CHANGE THESE VALUES ###########################
csv_file = ''     			# Use the full path /Users/XXXXX/Path/To/File.csv
access_token = ''				# your API token that was generated from your account user
domain = '' 						# domain.instructure.com, use domain only
env = '' 						  	# Leave nil if pushing to Production
output_csv = ''         # put the full path to a blank csv file to have the errors written in.

############################## DO NOT CHANGE THESE VALUES #######################
env != '' ? env << '.' : env
base_url = "https://#{domain}.#{env}instructure.com"

def start(csv_file, access_token, base_url, output_csv)
    hydra = Typhoeus::Hydra.new(max_concurrency: 10)
    CSV.foreach(csv_file, headers: true) do |row|
        if row.headers[0] != 'sis_user_id' || row.headers[1] != 'sis_login_id' || row.headers[2] != 'new_password'
            puts 'First column needs to be sis_user_id, second column needs to be sis_login_id, and third column needs to be new_password.'
        else
            # puts base_url, access_token
            get_response = Typhoeus::Request.new("#{base_url}/api/v1/users/sis_user_id:#{row['sis_user_id']}/logins?per_page=100",
                                                 method: :get,
                                                 headers: { Authorization: "Bearer #{access_token}" })

            get_response.on_complete do |response|
                export_id = ''
                unique_id = ''
                parsed_data = nil

                if response.code.eql?(200)
                    parsed_data = JSON.parse(response.body)
                    parsed_data.each do |login|
                        next unless login['unique_id'].eql?(row['sis_login_id'])
                        export_id = login['id'] unless nil
                        unique_id = login['unique_id'] unless nil
                        break
                    end
                    if parsed_data && unique_id.eql?(row['sis_login_id'])
                        # binding.pry
                        put_response = Typhoeus::Request.new("#{base_url}/api/v1/accounts/1/logins/#{export_id}",
                                                             method: :put,
                                                             headers: { Authorization: "Bearer #{access_token}", 'Content-Type' => 'application/x-www-form-urlencoded' },
                                                             params: { 'login[password]' => row['new_password'] })
                        # parse JSON data to save in readable array
                        put_response.on_complete do |response|
                            if response.code.eql?(200)
                                puts "Successfully updated password for user #{row['sis_user_id']} for login #{unique_id}"
                            else
                                puts "Unable to update password for user #{row['sis_user_id']}. Trying again..."
                                hydra.queue(put_response)
                            end
                        end

                        hydra.queue(put_response)
                    else
                        puts "Unique_id #{unique_id} is different than the sis_login_id #{row['sis_login_id']} for user #{row['sis_user_id']}"
                        CSV.open(output_csv, 'a') do |csv|
                            csv << ['2', 'User', (row['sis_user_id']).to_s, 'has a different Unique_id in Canvas than the sis_login_id', (row['sis_login_id']).to_s]
                        end
                    end
                else
                    if response.code.eql?(404)
                        puts "User #{row['sis_user_id']} does not exist in Canvas"
                        CSV.open(output_csv, 'a') do |csv|
                            csv << ['1', 'User', (row['sis_user_id']).to_s, 'does not exist in Canvas']
                        end
                    else
                        puts "Trouble connecting to the server while doing API call for user #{row['sis_user_id']}. Trying again..."
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
