# Downloads a file. In the future it will retry if download fails with exponential backoff up to some max tries.

require "net/http"
require "uri"

class Downloader
    def download(file_uri)
        uri = URI.parse(file_uri)
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        request = Net::HTTP::Get.new(uri.request_uri)
        print "Downloading #{file_uri}... "
        response = http.request(request)

        if response.code == "200"
            print "done\n"
            return response.body
        else
            puts "Error downloading file, response code: #{response.code}"
        end
    end
end