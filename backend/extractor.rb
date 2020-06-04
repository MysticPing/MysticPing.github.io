# Converts XML string into list of article hashes.

require "nokogiri"

class Extractor
    def extract(file)
        print "Extracting values... "
        apk_xml = Nokogiri::XML(file)
        apk_list = []
        apk_xml.xpath('//artikel').each do |article|
            article_hash = Hash.new()
            article.children.each do |row|
                article_hash[row.node_name.downcase.to_sym] = row.content
            end
            apk_list << article_hash
        end
        print "done\n"
        return apk_list
    end
end