import urllib
import urllib2
from bs4 import BeautifulSoup

# prepare the header
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# first page
url = "http://casesearch.courts.state.md.us/casesearch/"
request = urllib2.Request(url, headers=headers)
page = urllib2.urlopen(url)

# parse the page
soup = BeautifulSoup(str(page.read()), 'html.parser')
# and save it
with open('q5-1.html', 'w') as outfile2:
    outfile2.write(soup.prettify().encode('utf-8'))

# find all necessary info
# which url to go to next
form_url = soup.select("body > div > table:nth-child(2) > form")[0]['action']
# text in the form
textarea = soup.select("textarea.button")[0]
text = textarea.text
# button value
button = soup.select("input.button")[0]
buttonvalue = button.attrs['value']
# checkbox value
checkbox = soup.select("input[type=checkbox]")[0]
checkboxvalue = checkbox.attrs['value']

# combine all values and encode them
params = urllib.urlencode({'text': text,
'action': buttonvalue,
'disclaimer': checkboxvalue})

# set up the request
request = urllib2.Request(url+form_url, params, headers=headers)
# open the page and save it
response = urllib2.urlopen(request)
with open('q5-2.html', 'w') as otherfile:
    otherfile.write(response.read())