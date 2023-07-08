#Univerzalni scraper za pretraživa.rs

from urllib.request import urlopen
import certifi
import ssl
import json
import sys
from urllib.error import HTTPError, URLError
import time

BLANK_PAGE_SZ = 6350   # Not Found Web page size
magazine = "NAME"
urlpath  = "https://pretraziva.rs/pregled/" + magazine
urlpath2 = "https://pretraziva.rs/prikaz/" + magazine
urlpath3 = "https://pretraziva.rs/download/" + magazine + "--"

# Make a list of all available issues

# Get a list of all issues from the JavaScript variable "publicationYears"
str1 = urlopen(urlpath, timeout=10, context=ssl.create_default_context(cafile=certifi.where()))
htmlstr = str1.read().decode('utf-8')
i1 = htmlstr.index("{")
i2 = htmlstr.index("};")
dictionary = eval(htmlstr[i1:i2+1])

# Print the information

print("\nYears:", flush=True)
for y in dictionary:
    print(y, end=" ", flush=True)

print("\nAll issues by date:", flush=True)
for y in dictionary:
    print(y)
    issues = dictionary[y]
    for i in issues:
        print("  " + i[1].replace(" ","") + y + ".", flush=True)
print()

# Move the text of an issue to a file

# Iterate all pages by year/issue and write the plain text to new files
for y in dictionary:    # years
    
    issues = dictionary[y]

    for i in issues:    # issues
        ymd = y + "-" + i[1][4:6] + "-" + i[1][0:2]
        iurlpath = urlpath2 + "/" + ymd
        print(y, iurlpath, flush=True)
        
        # Iterate pages

        # Number of pages
        iurlpath2 = iurlpath + "/1"
        istr2 = urlopen(iurlpath2, timeout=10, context=ssl.create_default_context(cafile=certifi.where()))
        html2 = istr2.read().decode('utf-8')
        i1 = html2.index("var lastPage = ")
        lp = html2[i1+15:i1+19]
        i2 = lp.index(";")
        npg = eval(lp[:i2])
        print(npg, "pages", flush=True)
        
        # Write text to a new file
        ioutpath = ymd + " " + magazine + ".xml"
        print("Writing text to:", ioutpath, flush=True)
        f = open(ioutpath, "w", encoding='utf-8',newline='')
        
        # Add TEI header
        print('Adding header', flush=True)
        with open("TEI header.txt") as header:
            for line in header:
                f.write(line)

        for pg in range(1, npg+1):
            print("  page", pg, flush=True)
            try:
                try:
                    iurlpath3 = urlpath3 + ymd + "--" + str(pg) + ".txt"
                    str3 = urlopen(iurlpath3, timeout=10, context=ssl.create_default_context(cafile=certifi.where()))
                    txt  = str3.read().decode('utf-8')
                    f.write(txt)
                except:
                    iurlpath3 = urlpath3 + ymd + "--0" + str(pg) + ".txt"
                    str3 = urlopen(iurlpath3, timeout=10, context=ssl.create_default_context(cafile=certifi.where()))
                    txt  = str3.read().decode('utf-8')
                    f.write(txt)
            except:
                pass
        
        # Add TEI closed tags at the end
        print('Adding footer', flush=True)
        with open("TEI closed tags.txt") as footer:
            for line in footer:
                f.write(line)
    
        f.close()
        
print('Done.', flush=True)
