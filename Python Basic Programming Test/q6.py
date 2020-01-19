import json
import os
import urllib2
import unicodedata
import re
from bs4 import BeautifulSoup

dirpath = os.getcwd()
# a list of rows for simpler printing
list_of_rows = ['Viewed', 'Date', 'Action Text', 'Disposition', 'Image']

for x in range(1,4):
    dict_list = []
    file_name = 'q6-%d.html' % x
    # Read in the file
    with open(file_name, 'r') as html_file :
        filedata = html_file.read()

    # Replace the target string because html.parser breaks when trying to parse this tag
    filedata = filedata.replace('</A>', '')

    # Write the file out again
    with open(file_name, 'w') as html_file:
        html_file.write(filedata)
        
    # create path, open the page and parse it
    path = "file:\\\\%s\\%s" % (dirpath, file_name)
    page = urllib2.urlopen(path)
    soup = BeautifulSoup(page, 'html.parser')

    # first find the next sibling of the first table, then find all siblings of the first tr as the first one is a header
    first = soup.table.find_next_sibling("table").find("tr").find_next_siblings("tr")
    for row in first:
        # for each row we need to init dict and find the first td
        dictionary = {}
        d = row.find("td")
        # counter is for printing the titles
        i = 0
        for string in d.find_all(string=True):
            # find all strings in the current td and strip them of trailing whitespace
            dictionary[list_of_rows[i]] = string.strip()
            i+=1

        for a in d.find_all("a", href=True):
            # try to find any links and if there are put them in their own location
            dictionary['href'] = a['href']
        # append the created dict to the list
        dict_list.append(dictionary)

    with open('q6-%d.json' % x, 'w') as outfile:
        # dump the list to the appropriately named file
        json.dump(dict_list, outfile, indent=4)
