require_relative "downloader"
require_relative "extractor"
require_relative "importer"

dl = Downloader.new
ex = Extractor.new
im = Importer.new
doc = dl.download("https://www.systembolaget.se/api/assortment/products/xml")
ext = ex.extract(doc) 
im.import(ext)
