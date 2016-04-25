require 'net/http'


http = Net::HTTP.new('cwt.instructure.com',443);
#http.use_ssl = true
path = '/api/v1/courses/?access_token=token_here'

resp, data = http.get(path,nil)

puts resp
