# Uses the extracted info to create or update the sqlite database. 

require "sqlite3"

class Importer
    def import(apk_list, path)
        print("Importing values... ")
        db = SQLite3::Database.new path
        db.execute <<-SQL
        DROP TABLE IF EXISTS apk;
        SQL
        db.execute <<-SQL
        CREATE TABLE IF NOT EXISTS apk (
            id           INTEGER PRIMARY KEY,
            apk          REAL,
            art_name     TEXT,
            price        TEXT,
            volume       TEXT,
            art_type     TEXT,
            art_style    TEXT,
            abv          TEXT,
            availability TEXT
            );
        SQL
        db.transaction
        apk_list.each do |article|
            id           = article[:artikelid]
            name         = article.fetch(:namn, "") + " " + article.fetch(:namn2, "") 
            price        = (article.fetch(:prisinklmoms, 0).to_f + article.fetch(:pant, 0).to_f).round(1)
            price        = if (price == price.to_i) then price.to_i.to_s else price.to_s end + " kr"
            volume       = article.fetch(:volymiml, "") + " ml"
            type         = article.fetch(:varugrupp, "")
            style        = article.fetch(:stil, "")
            abv          = article[:alkoholhalt]
            availability = article[:sortiment]
            abv_num = abv.tr('%', '').to_f
            price_num = price.tr(' kr', '').to_f
            volume_num = volume.tr(' ml', '').to_f
            apk = (((abv_num/100)*volume_num)/price_num).round(3)
            insert = db.prepare <<-SQL
                INSERT INTO apk (id, apk, art_name, price, volume, art_type, art_style, abv, availability)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            SQL
            rs = insert.execute id, apk, name, price, volume, type, style, abv, availability
        end
        db.commit
        puts ("done")
        return db
    end
end