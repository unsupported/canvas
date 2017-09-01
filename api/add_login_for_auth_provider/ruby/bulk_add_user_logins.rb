#Working as of August 22nd, 2017
require 'typhoeus'
require 'csv'
require 'json'

################################################################################
################# USER AREA: COMPLETE THE EQUIVALENCIES BELOW ##################

### Replace ONLY underscores
### Leave in single quotations surrounding the underscores (where pertinent)

@access_token = '___'
  #Replace underscores with API token generated from account user in Canvas

@domain = '___'
  #Replace underscores with the sub-domain for your Canvas instance
  #Example: If Canvas URL is canvasstuff.instructure.com, use canvasstuff

@env = nil
  #To use script with Production, leave as-is
  #For use with test/beta environments, replace nil with test or with beta

@csv_file = '___'
  #Replace underscores with the full file path to the CSV file being used
  #Example File Path: /Users/XXXXX/Path/To/File.csv

@root_account = '___'
  #Replace underscores with the numeric ID of your root account.  This is the number that will display after '.com/accounts/' when on your Canvas root account admin settings page. It's usually 1.

########## END OF USER AREA: DO NOT EDIT ANY VALUES BEYOND THIS POINT ##########
################################################################################

@env ? @env << "." : @env
@base_url = "https://#{@domain}.#{@env}instructure.com/"


CSV.foreach(@csv_file, {headers: true}) do |row|
  if row['canvas_user_id'].nil?
    puts 'No data in needed canvas_user_id column'
    raise 'Valid CSV headers not found (Expecting canvas_user_id)'
  elsif row['login_id'].nil?
    puts 'No data in needed login_id csv column'
    raise 'Valid CSV headers not found (Expecting login_id)'
  elsif row['authentication_provider_id'].nil?
    puts 'No data in needed authentication_provider_id csv column'
    raise 'Valid CSV headers not found (Expecting authentication_provider_id)'
  elsif row['sis_user_id'].nil?
    puts 'No data in needed sis_user_id csv column'
    raise 'Valid CSV headers not found (Expecting sis_user_id)'
  else
    canvas_user_id = row['canvas_user_id']
    login_id = row['login_id']
    authentication_provider_id = row['authentication_provider_id']
    sis_user_id = row['sis_user_id']
    response = Typhoeus.put
        (
            @base_url + "api/v1/accounts/" + @root_account + "/logins/",
            headers: {
                      :authorization => 'Bearer ' + @access_token , 'Content-Type' => 'application/x-www-form-urlencoded'
                    },
            body: {
                  user: {
                        :id => canvas_user_id
                      },
                  login: {
                      :unique_id => login_id,
                      :authentication_provider_id => authentication_provider_id,
                      :sis_user_id => sis_user_id
                      }
                  }
        )
    #parse JSON data to save in readable array
    data = JSON.parse(response.body)
    puts data
  end
end
