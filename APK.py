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
    ABV = row[23].value.strip('%')
    ABV = float(ABV)/100
    # Price
    price = row[6].value
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
    APKList.append((APK, name, itemtype, style, spectype, ID))

# Sorted for highest APK first
APKList.sort(reverse=True)

os.remove("apk.txt")
f = open("apk.txt", "wb")

f.write('<table id = "apktable">'.encode("utf-8"))
f.write("<tr><th>APK</th><th>Name</th><th>Type</th><th></th><th>Style</th></tr>".encode("utf-8"))
for i in range(len(APKList)):
    f.write("<tr>".encode("utf-8"))

    # APK
    f.write("<td>".encode("utf-8"))
    f.write(("%.2f" % APKList[i][0]).encode("utf-8"))
    f.write("</td>".encode("utf-8"))
    
    # Name
    f.write('<td><a href="https://www.systembolaget.se/'.encode("utf-8"))
    f.write(str(APKList[i][5]).encode("utf-8"))
    f.write('">'.encode("utf-8"))
    f.write((APKList[i][1].encode("utf-8")))
    f.write("</a></td>".encode("utf-8"))
    
    # Type
    f.write("<td>".encode("utf-8"))
    f.write((APKList[i][2].encode("utf-8")))
    f.write("</td>".encode("utf-8"))

    # Other Type
    f.write("<td>".encode("utf-8"))
    f.write((APKList[i][4].encode("utf-8")))
    f.write("</td>".encode("utf-8"))

    #Style
    f.write("<td>".encode("utf-8"))
    f.write((APKList[i][3].encode("utf-8")))
    f.write("</td>".encode("utf-8"))

    f.write("</tr>".encode("utf-8"))
f.write("</table>".encode("utf-8"))
f.close()