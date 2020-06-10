require_relative "downloader"
require_relative "extractor"
require_relative "importer"

puts ""
puts Time.now

dl = Downloader.new(max_attempts: 7, backoff: 2.5)
ex = Extractor.new
im = Importer.new
doc = dl.download("https://www.systembolaget.se/api/assortment/products/xml")
ext = ex.extract(doc) 
im.import(ext, "apk.db")

puts ""

