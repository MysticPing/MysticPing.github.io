import pandas as pd
import openpyxl as op
import urllib.request
import os
import sys
import json
from datetime import datetime
import subprocess

# Downloads xls file
def download_xls():
    print("Downloading xls.")
    url = "https://www.systembolaget.se/api/assortment/products/xls"
    urllib.request.urlretrieve(url, "old_format.xls")

# Converts from xls to xslx using pandas. Takes a while.
# Also rather inefficient, i'd prefer to manipulate the old file driectly
# but can't find any good libraries for xls files, even though its really
# a html file...
def convert():
    print("Converting to xlsx.")
    old_format = pd.read_html("old_format.xls")
    old_format[0].to_excel("new_format.xlsx")


# Set working directory to script location
os.chdir(sys.path[0])

# Debug information
print("\nAutomatic update " + datetime.now().strftime('%Y-%m-%d %H:%M'))
# Uncomment these two functions when you want to update the spreadsheets
download_xls()
convert()

print("Loading into openpyxl.")
wb = op.load_workbook("new_format.xlsx")
ws = wb.active

APKList = []

iterRow = iter(tuple(ws.rows))
next(iterRow)
print("Parsing sheet.")
for row in iterRow:
    # ID, used to link to Systembolaget website
    ID = row[1].value
    # Volume in ml
    volume = row[8].value
    # Alkohok by %. Stored as a string
    # Convert to actual value by removing % and converting to float
    ABV = float(row[23].value.strip('%'))
    ABVRounded = round(ABV,2)
    # Price. row 7 is sometimes empty. Row 7 is deposit
    price = row[6].value
    if (row[7].value != None):
        price += row[7].value
    APK = ((ABV/100)*volume)/price
    # Name
    name1 = str(row[4].value)
    if (name1 == 'None'):
        name1 = ""
    name2 =  str(row[5].value)
    if (name2 == 'None'):
        name2 = ""
    name = name1 + " " + name2
    # Type
    itemType = str(row[12].value)
    if (itemType == 'None'):
        itemType = ''
    # Style
    itemStyle = str(row[14].value)
    itemStyle = "" if (itemStyle == 'None') else itemStyle

    # Availability
    # FS ordinarie sortiment
    # FSN Ordinarie
    # FSB Ordinarie
    # BS Övrigt (beställning?)
    # TSLS Lokalt
    # TSE Små partier

    # TSS Seasonal
    availability = row[24].value
    # Add to list, APK and Name
    if (APK != 0):
        APKList.append([round(APK,3), 0, ID, name, itemType, itemStyle, ABVRounded, volume, round(price,2), availability])

# Sorted for highest APK first
APKList.sort(reverse=True)

# Add index after sorting
for i,v in enumerate(iter(APKList)):
    APKList[i][1] = (i+1)
# Write to json file
print("Creating json data")
f = open('data.json', 'w')
json.dump(APKList, f)
f.close()

# Save existing lines
f = open("index.html", "r", encoding="utf-8")
data = f.readlines()
lines = iter(data)
f.close()
# Writing initial table
print("Creaint initial html table")
# Keep all existing lines except when you encounter table_location, then replace next line
f = open("index.html", "w", encoding="utf-8")
print ("Creating html table.")
for i, line in enumerate(lines):
    if line == "<!--table_location-->\n":
        # header and table start
        f.write("<!--table_location-->")
        f.write('\n<table id = "apktable">')
        f.write('<thead><tr><th></th><th>APK</th><th>Namn <input id="nameFilter""></th><th>Typ <input id="typeFilter"></th><th>Alkohol</th><th>Volym</th><th>Pris</th></tr></thead>')
        for i in range(0,200):
            APKItem = APKList[i]
            f.write("<tr>")
            # Number
            f.write("<td><strong>")
            f.write(str(APKItem[1]))
            f.write("</strong></td>")

            # APK
            f.write("<td>")
            f.write(str(APKItem[0]))
            f.write("</td>")
            
            # Name
            f.write('<td><a href="https://www.systembolaget.se/')
            f.write(str(APKItem[2]))
            f.write('">')
            f.write(APKItem[3])
            f.write("</a></td>")
            
            # Type
            f.write("<td>")
            f.write(APKItem[4] if APKItem[5] == "" else APKItem[4] + "    <i>"+APKItem[5]+"</i>")
            f.write("</td>")
            '''
            # Type If it contains more details add those with a dash seperator
            f.write("<td>")
            f.write(APKItem[5])
            '''
            # ABV
            f.write("<td>")
            f.write(str(APKItem[6]))
            f.write("%")
            f.write("</td>")           
            
             # Volume
            f.write("<td>")
            f.write(str(APKItem[7]))
            f.write(" ml")
            f.write("</td>")

            # Price
            f.write("<td>")
            f.write(str(APKItem[8]))
            f.write(" kr")
            f.write("</td>")

            # Availability
            f.write('<td style="display: none;">')
            f.write(APKItem[9])
            f.write("</td>")

            f.write("</tr>")
        f.write("</table>\n")
        # this skips the next line, which includes the old table
        next(lines)
    elif "Senast uppdaterad: " in line:
        f.write("Senast uppdaterad: ")
        print ("Updating last updated text.")
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M'))
        f.write('\n')
    else:
        f.writelines(line)
f.close()

print("Cleaning sheet files.")
os.remove("old_format.xls")
os.remove("new_format.xlsx")

print("Making and pushing commit.")
subprocess.call(["git", "commit", "-am", "Automatic Update "+datetime.now().strftime('%Y-%m-%d')])
subprocess.call(["git", "push"])
print("Done!")
