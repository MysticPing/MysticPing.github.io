import pandas as pd
import openpyxl as op
import urllib.request
import os
# Downloads xls file
def download_xls():
    url = "https://www.systembolaget.se/api/assortment/products/xls"
    urllib.request.urlretrieve(url, "old_format.xls")

# Converts from xls to xslx using pandas. Takes a while.
# Also rather inefficient, i'd prefer to manipulate the old file driectly
# but can't find any good libraries for xls files, even though its really
# a html file...
def convert():
    old_format = pd.read_html("old_format.xls")
    old_format[0].to_excel("new_format.xlsx")

# Uncomment these two functions when you want to update the spreadsheets
#download_xls()
#convert()

wb = op.load_workbook("new_format.xlsx")
ws = wb.active

APKList = []

iterRow = iter(tuple(ws.rows))
next(iterRow)
for row in iterRow:
    # ID, used to link to Systembolaget website
    ID = row[1].value
    # Volume in ml
    volume = row[8].value
    # Alkohok by %. Stored as a string
    # Convert to actual value by removing % and converting to float
    ABVstr = row[23].value.strip('%')
    ABV = float(ABVstr)/100
    # Price. row 7 is sometimes empty. Row 7 is deposit
    price = row[6].value
    if (row[7].value != None):
        price += row[7].value
    APK = (ABV*volume)/price
    # Name
    name1 = str(row[4].value)
    if (name1 == 'None'):
        name1 = ""
    name2 =  str(row[5].value)
    if (name2 == 'None'):
        name2 = ""
    name = name1 + " " + name2
    # Type
    itemtype = row[12].value
    # More specific type
    spectype = str(row[13].value)
    if (spectype == 'None'):
        spectype = '' 
    # Style
    style = str(row[14].value)
    if (style == 'None'):
        style = ''
    # Add to list, APK and Name
    APKList.append((APK, name, itemtype, style, spectype, ID, ABVstr, volume, price))

# Sorted for highest APK first
APKList.sort(reverse=True)

#os.remove("apk.txt")

# Save existing lines
f = open("apk.html", "r", encoding="utf-8")
data = f.readlines()
lines = iter(data)
f.close()

# Keep all existing lines except when you encounter table_location, then replace next line
f = open("apk.html", "w", encoding="utf-8")

for line in lines:
    if line == "<!--table_location-->\n":
        # header and table start
        f.write("<!--table_location-->")
        f.write('\n<table id = "apktable">')
        f.write("<tr><th>APK</th><th>Name</th><th>Type</th><th>Style</th><th>ABV</th><th>Volume</th><th>Price</th></tr>")
        for i in range(len(APKList)):
            f.write("<tr>")

            # APK
            f.write("<td>")
            f.write(("%.3f" % APKList[i][0]))
            f.write("</td>")
            
            # Name
            f.write('<td><a href="https://www.systembolaget.se/')
            f.write(str(APKList[i][5]))
            f.write('">')
            f.write(APKList[i][1])
            f.write("</a></td>")
            
            # Type
            f.write("<td>")
            f.write((APKList[i][2]))
            f.write("</td>")

            # Style. If it contains more details add those with a dash seperator
            f.write("<td>")
            f.write(APKList[i][4])

            if APKList[i][3] != "":
                f.write(" — " + APKList[i][3])
            f.write("</td>")

            # ABV
            f.write("<td>")
            f.write((APKList[i][6]))
            f.write("</td>")           
            
             # Volume
            f.write("<td>")
            f.write(str(APKList[i][7]))
            f.write(" ml")
            f.write("</td>")

            # Volume
            f.write("<td>")
            f.write(str(APKList[i][8]))
            f.write(" kr")
            f.write("</td>")

            f.write("</tr>")
        f.write("</table>\n")
        # this skips the next line, which includes the old table
        next(lines)
    else:
        f.writelines(line)

f.close()
